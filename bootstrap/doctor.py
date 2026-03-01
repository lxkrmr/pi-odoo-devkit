#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path


class CheckResult:
    def __init__(self, name: str, status: str, message: str):
        self.name = name
        self.status = status  # PASS | WARN | FAIL
        self.message = message


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def resolve_erp_dir(devkit_dir: Path, positional: str | None) -> Path | None:
    if positional:
        return Path(positional).expanduser()

    env_val = os.environ.get("ODOO_REPO_PATH")
    if env_val:
        return Path(env_val).expanduser()

    sibling = devkit_dir.parent / "erp"
    if sibling.exists():
        return sibling

    cwd = Path.cwd()
    if (cwd / "docker-compose.yml").exists():
        return cwd

    return None


def check_symlink(path: Path, expected: Path, name: str) -> CheckResult:
    if not path.exists() and not path.is_symlink():
        return CheckResult(name, "FAIL", f"missing: {path}")
    if not path.is_symlink():
        return CheckResult(name, "FAIL", f"not a symlink: {path}")
    actual = path.resolve()
    if actual != expected.resolve():
        return CheckResult(name, "WARN", f"points to {actual} (expected {expected})")
    return CheckResult(name, "PASS", f"ok: {path} -> {actual}")


def check_http(url: str, name: str) -> CheckResult:
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            if 200 <= r.status < 400:
                return CheckResult(name, "PASS", f"reachable: {url} (HTTP {r.status})")
            return CheckResult(name, "WARN", f"unexpected HTTP status {r.status}: {url}")
    except urllib.error.URLError as e:
        return CheckResult(name, "WARN", f"not reachable: {url} ({e})")


def scan_content_hygiene(devkit_dir: Path) -> CheckResult:
    exclude_dirs = {".git", "node_modules", ".venv", ".direnv"}
    patterns = [
        (re.compile(r"/Users/[A-Za-z0-9._-]+"), "hardcoded macOS user path"),
        (re.compile(r"/home/[A-Za-z0-9._-]+"), "hardcoded Linux home path"),
        (re.compile(r"~/workspace/"), "hardcoded workspace home shortcut"),
        (re.compile(r"\bphiloro\b", re.IGNORECASE), "company-specific identifier"),
    ]

    hits: list[str] = []
    for path in devkit_dir.rglob("*"):
        if not path.is_file():
            continue

        if any(part in exclude_dirs for part in path.parts):
            continue

        # Skip lockfiles/binaries where pattern noise is expected
        if path.suffix in {".lock", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf"}:
            continue

        # Skip this checker source file (contains regex patterns as literals)
        if path.name == "doctor.py" and path.parent.name == "bootstrap":
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        for idx, line in enumerate(text.splitlines(), start=1):
            for rx, label in patterns:
                if rx.search(line):
                    rel = path.relative_to(devkit_dir)
                    hits.append(f"{rel}:{idx} ({label})")
                    if len(hits) >= 10:
                        break
            if len(hits) >= 10:
                break
        if len(hits) >= 10:
            break

    if hits:
        preview = "; ".join(hits[:3])
        more = "" if len(hits) <= 3 else f" (+{len(hits)-3} more)"
        return CheckResult("content-hygiene", "WARN", f"Potentially non-generic content found: {preview}{more}")

    return CheckResult("content-hygiene", "PASS", "No obvious personal paths/company-specific identifiers found")


def main() -> int:
    parser = argparse.ArgumentParser(description="Doctor checks for Odoo devkit setup.")
    parser.add_argument("project_repo_path", nargs="?", help="Path to Odoo project repo")
    args = parser.parse_args()

    devkit_dir = Path(__file__).resolve().parent.parent
    project_dir_raw = resolve_erp_dir(devkit_dir, args.project_repo_path)
    if not project_dir_raw:
        print("Could not resolve Odoo project repo path.")
        parser.print_help()
        return 1

    erp_dir = project_dir_raw.expanduser().resolve()
    if not erp_dir.exists() or not (erp_dir / "docker-compose.yml").exists():
        print(f"Invalid Odoo project repo path: {erp_dir}")
        return 1

    results: list[CheckResult] = []

    # Tools
    for tool, required in [
        ("python3", True),
        ("docker", True),
        ("node", False),
        ("npm", False),
        ("direnv", False),
    ]:
        ok = command_exists(tool)
        if ok:
            results.append(CheckResult(f"tool:{tool}", "PASS", "installed"))
        elif required:
            results.append(CheckResult(f"tool:{tool}", "FAIL", "missing required tool"))
        else:
            results.append(CheckResult(f"tool:{tool}", "WARN", "missing optional tool"))

    # Project links
    results.append(
        check_symlink(
            erp_dir / ".pi" / "skills" / "shared-devkit",
            devkit_dir / "skills",
            "link:skills/shared-devkit",
        )
    )
    results.append(
        check_symlink(
            erp_dir / ".pi" / "tools" / "shared-devkit",
            devkit_dir / "commands",
            "link:tools/shared-devkit",
        )
    )

    devkit_cmd = erp_dir / ".pi" / "tools" / "devkit"
    if devkit_cmd.exists() or devkit_cmd.is_symlink():
        if devkit_cmd.is_symlink() and devkit_cmd.resolve() == (devkit_dir / "commands" / "dev").resolve():
            results.append(CheckResult("link:tools/devkit", "PASS", "ok"))
        else:
            results.append(CheckResult("link:tools/devkit", "WARN", "exists but not linked to devkit command"))
    else:
        results.append(CheckResult("link:tools/devkit", "WARN", "missing"))

    # Local include notes
    notes = erp_dir / ".pi" / "DEVKIT_AGENT_NOTES.md"
    if notes.exists():
        results.append(CheckResult("notes:DEVKIT_AGENT_NOTES", "PASS", "present"))
    else:
        results.append(CheckResult("notes:DEVKIT_AGENT_NOTES", "WARN", "missing"))

    # Env setup status
    envrc = devkit_dir / ".envrc"
    venv = devkit_dir / ".venv"
    results.append(CheckResult("env:.envrc", "PASS" if envrc.exists() else "WARN", "present" if envrc.exists() else "missing"))
    results.append(CheckResult("env:.venv", "PASS" if venv.exists() else "WARN", "present" if venv.exists() else "missing"))

    # Browser-tools deps status
    bt_dir = devkit_dir / "skills" / "browser-tools" / "browser-tools"
    bt_node_modules = bt_dir / "node_modules"
    if bt_dir.exists():
        results.append(CheckResult("browser-tools:code", "PASS", "present"))
        if bt_node_modules.exists():
            results.append(CheckResult("browser-tools:deps", "PASS", "node_modules present"))
        else:
            results.append(CheckResult("browser-tools:deps", "WARN", "node_modules missing (run install with --with-browser-tools)"))
    else:
        results.append(CheckResult("browser-tools:code", "FAIL", f"missing directory: {bt_dir}"))

    # Runtime reachability
    results.append(check_http("http://localhost:8069", "odoo:web"))
    results.append(check_http("http://localhost:9222/json/version", "browser:cdp"))

    # Content hygiene
    results.append(scan_content_hygiene(devkit_dir))

    # Pi availability guidance
    results.append(
        CheckResult(
            "pi.dev",
            "WARN",
            "Cannot fully auto-detect account/session. Open pi.dev manually and verify repo access.",
        )
    )

    # Print results
    print(f"Odoo devkit doctor report\n- devkit: {devkit_dir}\n- project: {erp_dir}\n")

    fail_count = 0
    warn_count = 0
    for r in results:
        icon = "✅" if r.status == "PASS" else ("⚠️" if r.status == "WARN" else "❌")
        print(f"{icon} [{r.status}] {r.name}: {r.message}")
        if r.status == "FAIL":
            fail_count += 1
        elif r.status == "WARN":
            warn_count += 1

    print("\nSummary:")
    print(f"- FAIL: {fail_count}")
    print(f"- WARN: {warn_count}")

    print("\nSuggested next actions:")
    print(f"1) Run installer: {devkit_dir}/bootstrap/install.sh {erp_dir} --yes --with-browser-tools")
    print("2) If using recommended env: cd {0} && direnv allow".format(devkit_dir))
    print("3) Start local stack: cd {0} && docker compose up -d".format(erp_dir))
    print("4) Open pi.dev and start in your Odoo project repo")

    return 1 if fail_count else 0


if __name__ == "__main__":
    raise SystemExit(main())

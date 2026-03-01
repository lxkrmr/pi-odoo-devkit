#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path


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


def remove_symlink_if_matches(link_path: Path, target_path: Path) -> str:
    if not link_path.exists() and not link_path.is_symlink():
        return f"SKIP: not found: {link_path}"

    if not link_path.is_symlink():
        return f"SKIP: not a symlink (left untouched): {link_path}"

    current_target = link_path.resolve()
    if current_target != target_path.resolve():
        return f"SKIP: symlink points elsewhere (left untouched): {link_path} -> {current_target}"

    link_path.unlink()
    return f"REMOVED: {link_path}"


def remove_local_exclude(erp_dir: Path) -> str:
    exclude_file = erp_dir / ".git" / "info" / "exclude"
    if not exclude_file.exists():
        return f"SKIP: no local exclude file: {exclude_file}"

    lines = exclude_file.read_text(encoding="utf-8").splitlines()
    new_lines: list[str] = []
    removed = False

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == ".pi/":
            removed = True
            # remove preceding marker if present in output list
            if new_lines and new_lines[-1].strip() == "# local pi files":
                new_lines.pop()
            i += 1
            continue
        new_lines.append(line)
        i += 1

    if not removed:
        return f"SKIP: '.pi/' not present in {exclude_file}"

    content = "\n".join(new_lines).rstrip() + "\n"
    exclude_file.write_text(content, encoding="utf-8")
    return f"UPDATED: removed '.pi/' from {exclude_file}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Uninstall Odoo devkit links from a project repo safely.")
    parser.add_argument("project_repo_path", nargs="?", help="Path to Odoo project repo")
    parser.add_argument(
        "--remove-local-exclude",
        action="store_true",
        help="Also remove '.pi/' from <erp>/.git/info/exclude if present",
    )
    args = parser.parse_args()

    devkit_dir = Path(__file__).resolve().parent.parent
    project_dir_raw = resolve_erp_dir(devkit_dir, args.project_repo_path)
    if not project_dir_raw:
        print("Could not resolve Odoo project repo path.")
        parser.print_help()
        return 1

    erp_dir = project_dir_raw.expanduser().resolve()
    if not erp_dir.exists():
        print(f"Project repo path does not exist: {erp_dir}")
        return 1

    if not (erp_dir / "docker-compose.yml").exists():
        print(f"Not an Odoo project repo (missing docker-compose.yml): {erp_dir}")
        return 1

    actions = [
        remove_symlink_if_matches(
            erp_dir / ".pi" / "skills" / "shared-devkit",
            devkit_dir / "skills",
        ),
        remove_symlink_if_matches(
            erp_dir / ".pi" / "tools" / "shared-devkit",
            devkit_dir / "commands",
        ),
        remove_symlink_if_matches(
            erp_dir / ".pi" / "tools" / "devkit",
            devkit_dir / "commands" / "dev",
        ),
    ]

    notes = erp_dir / ".pi" / "DEVKIT_AGENT_NOTES.md"
    if notes.exists():
        text = notes.read_text(encoding="utf-8")
        if "managed-by: erp-devkit installer" in text:
            notes.unlink()
            actions.append(f"REMOVED: {notes}")
        else:
            actions.append(f"SKIP: notes file not managed by installer (left untouched): {notes}")
    else:
        actions.append(f"SKIP: not found: {notes}")

    if args.remove_local_exclude:
        actions.append(remove_local_exclude(erp_dir))

    print(f"Uninstall summary for project repo: {erp_dir}")
    for line in actions:
        print(f"- {line}")

    print("\nNote: existing local .pi skills/tools you created manually remain untouched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

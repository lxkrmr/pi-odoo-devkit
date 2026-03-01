# Getting Started (Clone → Start)

This guide is for new team members.

## 1) Clone repositories

```bash
cd /path/to/workspace
git clone <odoo-project-repo-url> odoo-project
git clone <erp-devkit-repo-url> erp-devkit
```

(Your directories can be different; pass explicit paths to scripts.)

## 2) Install devkit into project repo

```bash
cd /path/to/erp-devkit
./bootstrap/install.sh /path/to/odoo-project --yes --with-browser-tools --add-local-exclude
```

What this does:
- links shared skills/commands into `odoo-project/.pi`
- sets up recommended `.envrc + .venv` in devkit
- installs browser-tools npm dependencies
- hides local `.pi/` from git status (local-only)

## 3) Enable direnv (recommended)

```bash
cd /path/to/erp-devkit
direnv allow
```

## 4) Run doctor check

```bash
./bootstrap/doctor.sh /path/to/odoo-project
```

Fix reported FAIL items first.

## 5) Start working

```bash
cd /path/to/odoo-project
./.pi/tools/devkit help
./.pi/tools/devkit up
```

If using browser skills, follow `skills/browser-tools/SKILL.md` to start Chromium/CDP.

---

## If you already have `AGENTS.md` / `CLAUDE.md`

Installer does not modify those files automatically.

Check:
- `/path/to/odoo-project/.pi/DEVKIT_AGENT_NOTES.md`

Copy the suggested include note manually if you want.

---

## Quick uninstall

```bash
cd /path/to/erp-devkit
./bootstrap/uninstall.sh /path/to/odoo-project --remove-local-exclude
```

This removes devkit-managed links/files only.

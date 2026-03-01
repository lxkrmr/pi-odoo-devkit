# ERP Devkit

Shared skills and helper commands for local ERP development.

## Repository layout

- `skills/` — reusable skills (for Pi users)
- `commands/` — helper CLI scripts (useful for all team members)
- `templates/` — templates for creating new skills
- `bootstrap/install.sh` — installer that links this repo into an ERP repo

## Install into an ERP checkout

```bash
# from erp-devkit repo
./bootstrap/install.sh /path/to/erp
```

Or with environment variable:

```bash
ERP_REPO_PATH=/path/to/erp ./bootstrap/install.sh
```

### Optional: hide local `.pi` files from git status (local-only)

Use installer opt-in flag:

```bash
./bootstrap/install.sh /path/to/erp --add-local-exclude
```

This adds `.pi/` to `<erp>/.git/info/exclude` (not committed, local machine only).

Installer creates links in ERP repo:

- `.pi/skills/shared-devkit -> <erp-devkit>/skills`
- `.pi/tools/shared-devkit  -> <erp-devkit>/commands`
- `.pi/tools/devkit         -> <erp-devkit>/commands/dev` (if free)

## Works with different directory hierarchies

No hardcoded absolute paths are required. Provide ERP path explicitly if your repos are not siblings.

Examples:

```bash
# sibling layout
~/workspace/erp
~/workspace/erp-devkit

# custom layout
~/src/company/erp
~/tools/erp-devkit
./bootstrap/install.sh ~/src/company/erp
```

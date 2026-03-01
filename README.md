# Odoo Devkit (repository: `erp-devkit`)

Shared skills and helper commands for local Odoo development and agentic coding workflows.

## Repository layout

- `skills/` — reusable skills (for Pi users)
- `commands/` — helper CLI scripts (useful for all team members)
  - includes `dev new-skill <name>` scaffold helper
- `templates/` — templates for creating new skills
- `bootstrap/install.py` — main installer (interactive + non-interactive)
- `bootstrap/install.sh` — shell wrapper around `install.py`
- `bootstrap/doctor.py` / `bootstrap/doctor.sh` — setup diagnostics
- `bootstrap/uninstall.py` / `bootstrap/uninstall.sh` — cleanup
- `THIRD_PARTY.md` + `LICENSES/` — attribution and license texts
- `SECURITY.md` — security/privacy authoring rules

## Recommended setup (direnv + .venv)

This devkit recommends a local Python environment managed by `direnv`:

- `.envrc` at devkit root
- `.venv` for Python tooling isolation
- `commands/` added to PATH via `.envrc`

Installer can create this automatically.

## Install into an Odoo project checkout

```bash
# from devkit repo
./bootstrap/install.sh /path/to/odoo-project
```

Or with environment variable:

```bash
ODOO_REPO_PATH=/path/to/odoo-project ./bootstrap/install.sh
```


### Optional: hide local `.pi` files from git status (local-only)

Use installer opt-in flag:

```bash
./bootstrap/install.sh /path/to/odoo-project --add-local-exclude
```

This adds `.pi/` to `<project>/.git/info/exclude` (not committed, local machine only).

### Browser tools batteries included

`browser-tools` code is vendored under:

- `skills/browser-tools/browser-tools/`

Installer can install runtime deps (`npm install`) and report missing dependencies.

## What installer sets up

Links in project repo:

- `.pi/skills/shared-devkit -> <devkit>/skills`
- `.pi/tools/shared-devkit  -> <devkit>/commands`
- `.pi/tools/devkit         -> <devkit>/commands/dev` (if free)

Additional local support file:

- `.pi/DEVKIT_AGENT_NOTES.md`

This helps users integrate devkit guidance manually into existing `AGENTS.md` / `CLAUDE.md`.
Installer is non-invasive and does **not** edit those files automatically.

Optional setup:

- add `.pi/` to local git exclude
- create `.envrc` + `.venv`
- install browser-tools npm dependencies

## Install options

```bash
./bootstrap/install.sh --help
```

Key options:

- `--add-local-exclude`
- `--with-browser-tools` / `--without-browser-tools`
- `--without-envrc`
- `--yes` (non-interactive with recommended defaults)

## Doctor checks

```bash
./bootstrap/doctor.sh /path/to/odoo-project
```

Doctor checks tool availability, symlinks, env setup status, browser-tools deps, and local runtime reachability hints (`:8069`, `:9222`).

## Uninstall / cleanup

```bash
./bootstrap/uninstall.sh /path/to/odoo-project
```

Optional local git exclude cleanup:

```bash
./bootstrap/uninstall.sh /path/to/odoo-project --remove-local-exclude
```

Cleanup removes only devkit-managed links/files; existing custom local `.pi` files remain untouched.

## Works with different directory hierarchies

No hardcoded absolute paths are required. Provide project path explicitly if your repos are not siblings.

Examples:

```bash
# sibling layout (example only)
/path/to/odoo-project
/path/to/erp-devkit

# custom layout
/path/a/odoo-project
/path/b/erp-devkit
./bootstrap/install.sh /path/a/odoo-project
```

## Credits

Browser tooling is adapted from Mario Zechner's `pi-skills` project.
See `THIRD_PARTY.md` and `LICENSES/`.

---
name: odoo-addon-lifecycle
description: Manage local Odoo addon lifecycle with tools/octo (list, install, upgrade, uninstall) in a safe, repeatable way.
---

# Odoo Addon Lifecycle (Local)

_This skill follows `.pi/skills/_template/SKILL.md` conventions._

Use this skill for local addon state changes via `tools/octo`.

## Prerequisites

- Local stack is running:
  ```bash
  docker compose up -d
  ```
- `tools/octo` can authenticate to Odoo.

If needed, set auth/DB env vars explicitly:

```bash
export DATABASE=<db_name>
export DB_USER=<odoo_login>
export DB_PASSWORD=<odoo_password>
```


## Safety Rules

- Prefer `list`/`upgrade` over `uninstall`.
- `uninstall` can remove data and break dependencies; run it only with explicit confirmation.
- Change only the requested addon(s).

## Commands

### List module states

```bash
tools/octo list
```

Filter for one addon:

```bash
tools/octo list | rg '^<addon_name>\s*:'
```

### Install addon

```bash
tools/octo install <addon_name>
```

### Upgrade addon

```bash
tools/octo upgrade <addon_name>
```

### Uninstall addon (destructive)

```bash
tools/octo uninstall <addon_name>
```

Only run when explicitly requested.

## Recommended Workflow

1. Check current state:
   ```bash
   tools/octo list | rg '^<addon_name>\s*:'
   ```
2. Apply action (`install` / `upgrade` / `uninstall`).
3. Verify resulting state:
   ```bash
   tools/octo list | rg '^<addon_name>\s*:'
   ```

## Troubleshooting

- **Connection/auth errors**
  - Ensure Odoo is running and env vars are correct.
- **Addon not found**
  - Confirm addon technical name and that it is present in `addons/custom` or `addons/3rd_party`.
- **Upgrade/install fails**
  - Check Odoo logs for dependency, data, or migration errors.

## Notes

- `tools/octo` operates via Odoo RPC against local Odoo.
- For deeper ORM/data checks after lifecycle changes, use `odoo-shell-debug` and `local-db` skills.

## Credential Hygiene

- Use local/dev credentials only.
- Do not commit real credential values into docs, scripts, or checklists.

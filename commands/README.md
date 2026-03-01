# Dev Commands

Shared helper scripts for local Odoo development.

## Recommended usage (from Odoo project repo)

After running `bootstrap/install.sh`, use:

```bash
./.pi/tools/devkit help
```

Main commands:

- `./.pi/tools/devkit up`
- `./.pi/tools/devkit db`
- `./.pi/tools/devkit shell [db_name]`
- `./.pi/tools/devkit test [args...]`
- `./.pi/tools/devkit lint [args...]`
- `./.pi/tools/devkit doctor`
- `./.pi/tools/devkit new-skill <skill-name>`

## Direct usage (without installer)

You can also run directly from this repo by passing the project path:

```bash
ODOO_REPO_PATH=/path/to/odoo-project /path/to/erp-devkit/commands/dev help
```


## Notes

- `shell` uses `--no-http` to avoid conflicts with Odoo on `8069`.
- `db` reads DB config from `docker/odoo_base.conf` + `docker/odoo_local.conf`.
- If local `psql` is missing, `db` falls back to container `psql`.

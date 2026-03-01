# Dev Commands

Shared helper scripts for ERP local development.

## Recommended usage (from ERP repo)

After running `erp-devkit/bootstrap/install.sh`, use:

```bash
./.pi/tools/devkit help
```

Main commands:

- `./.pi/tools/devkit up`
- `./.pi/tools/devkit db`
- `./.pi/tools/devkit shell [db_name]`
- `./.pi/tools/devkit test [args...]`
- `./.pi/tools/devkit lint [args...]`

## Direct usage (without installer)

You can also run directly from this repo:

```bash
~/workspace/erp-devkit/commands/dev help
```

## Notes

- `shell` uses `--no-http` to avoid conflicts with Odoo on `8069`.
- `db` reads DB config from `docker/odoo_base.conf` + `docker/odoo_local.conf`.
- If local `psql` is missing, `db` falls back to container `psql`.

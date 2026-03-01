---
name: local-db
description: Access the local Odoo PostgreSQL database for development. Use when you need to query, inspect, or debug data in the local dev database.
---

# Local Database Access

_This skill follows `.pi/skills/_template/SKILL.md` conventions._

Access the local Odoo PostgreSQL DB (Docker `postgres` service) with `psql`.

## Prerequisites

- From repo root, ensure services are up:
  ```bash
  docker compose up -d
  ```
- `psql` is installed locally.

## Connection Source of Truth

Read DB settings from:

- `docker/odoo_base.conf`
- `docker/odoo_local.conf` (overrides base)

Relevant keys in `[options]`: `db_host`, `db_port`, `db_name`, `db_user`, `db_password`.

## Quick Setup (recommended)

Run this once per shell to load connection env vars automatically:

```bash
eval "$(python3 - <<'PY'
import configparser

cfg = configparser.ConfigParser()
cfg.read(['docker/odoo_base.conf', 'docker/odoo_local.conf'])
opt = cfg['options']

vals = {
    'PGHOST': opt.get('db_host', 'localhost'),
    'PGPORT': opt.get('db_port', '5432'),
    'PGDATABASE': opt.get('db_name', 'postgres'),
    'PGUSER': opt.get('db_user', 'odoo'),
    'PGPASSWORD': opt.get('db_password', 'odoo'),
}

# Local docker-compose exposes postgres on localhost
if vals['PGHOST'] in ('postgres', 'db'):
    vals['PGHOST'] = 'localhost'

for k, v in vals.items():
    v = v.replace('"', '\\"')
    print(f'export {k}="{v}"')
PY
)"
```

Then use:

```bash
psql
```

## Safety Defaults (read-only)

For inspection/debugging, prefer read-only sessions:

```bash
PGOPTIONS='-c default_transaction_read_only=on' psql
```

For one-off read-only queries:

```bash
PGOPTIONS='-c default_transaction_read_only=on' psql -c "SELECT id, name FROM res_partner ORDER BY id DESC LIMIT 10;"
```

## Query Examples

### Basic one-liner

```bash
psql -c "SELECT id, name FROM res_partner ORDER BY id DESC LIMIT 5;"
```

### Multi-line query

```bash
psql -c "
SELECT
    id,
    name,
    create_date
FROM res_partner
ORDER BY id DESC
LIMIT 10;
"
```

### Interactive session

```bash
psql
```

## Odoo-Focused Handy Queries

### Installed module states

```bash
psql -c "
SELECT name, state, latest_version
FROM ir_module_module
ORDER BY name;
"
```

### Recent cron definitions

```bash
psql -c "
SELECT id, name, active, nextcall, lastcall
FROM ir_cron
ORDER BY id DESC
LIMIT 20;
"
```

### Recent queue jobs (if `queue_job` installed)

```bash
psql -c "
SELECT id, name, state, date_created, date_done
FROM queue_job
ORDER BY id DESC
LIMIT 20;
"
```

## Useful `psql` Meta Commands

```bash
psql -c "\\dt"                 # list tables
psql -c "\\dt *purchase*"       # list tables by pattern
psql -c "\\d+ res_partner"      # table structure
```

## Troubleshooting

- **Connection refused**
  - Ensure services are running: `docker compose up -d`
  - Verify port mapping in `docker-compose.yml` (`5432:5432`)
- **Authentication failed**
  - Re-run the Quick Setup block to refresh `PG*` variables
- **Wrong database selected**
  - Check `PGDATABASE`:
    ```bash
    echo "$PGDATABASE"
    ```

## Notes

- Do not run destructive SQL (`DELETE`, `TRUNCATE`, mass `UPDATE`) unless explicitly requested.
- For exploratory work, keep sessions read-only by default.

## Credential Hygiene

- Use local/dev credentials only.
- Do not commit real credential values into docs, scripts, or checklists.

---
name: odoo-shell-debug
description: Use Odoo shell in local Docker to inspect ORM state, computed fields, and business logic that is not visible via raw SQL.
---

# Odoo Shell Debug (Local Docker)

_This skill follows `.pi/skills/_template/SKILL.md` conventions._

Use this skill when SQL is not enough (e.g. non-stored computed fields, record rules, context/company-dependent values, ORM methods).

## Prerequisites

- Start services from repo root:
  ```bash
  docker compose up -d
  ```
- Odoo container is running.

## Start Odoo Shell

`odoo shell` starts a **separate Odoo process** (it does not attach to the already running server process).

### Interactive shell (recommended)

```bash
docker compose exec odoo odoo shell --no-http
```

### Interactive shell for a specific DB

```bash
docker compose exec odoo odoo shell --no-http -d postgres
```

Use `--no-http` by default to avoid port `8069` conflicts while your normal dev server is running.

## Safety Rules

- Prefer **read-only inspection**.
- Do not create/write/unlink records unless explicitly requested.
- Avoid calling methods with side effects (posting, sending, cron triggers) unless asked.
- If you are unsure whether a method has side effects, do not run it without confirmation.

## Common Inspection Snippets

Inside `odoo shell`:

```python
# Environment quick info
env.cr.dbname
env.user.name
env.company.name

# Basic ORM read
partners = env['res.partner'].search([], limit=5)
partners.read(['id', 'name'])

# Count records
env['sale.order'].search_count([])
```

## Computed / Non-Stored Fields

```python
# Example: inspect a computed field value
order = env['sale.order'].search([], limit=1)
order.amount_total

# Check if field is stored
env['sale.order']._fields['amount_total'].store
```

If `store` is `False`, the value is computed at access time and may not exist in PostgreSQL as a persisted column.

## Context / Company / Access Behavior

```python
# Context-dependent read
env['product.product'].with_context(lang='de_DE').search([], limit=1).display_name

# Company-dependent read
company = env['res.company'].search([], limit=1)
env['account.account'].with_company(company).search([], limit=5).read(['code', 'name'])

# Access-rule comparison (only when needed)
env['res.partner'].search_count([])          # current user rules
env['res.partner'].sudo().search_count([])   # bypass rules
```

## Compare ORM vs SQL (quick pattern)

```python
partner = env['res.partner'].search([], limit=1)
partner.name

env.cr.execute("SELECT name FROM res_partner WHERE id = %s", [partner.id])
env.cr.fetchone()
```

Use this to understand differences between raw DB state and ORM-transformed values.

## Non-Interactive Script Mode

Run a small snippet without opening a prompt:

```bash
docker compose exec -T odoo odoo shell --no-http -d postgres <<'PY'
partners = env['res.partner'].search([], limit=3)
print(partners.read(['id', 'name']))
PY
```

## Troubleshooting

- **`database ... does not exist`**
  - Pass explicit DB: `docker compose exec odoo odoo shell --no-http -d <db_name>`
- **`service "odoo" is not running`**
  - Start stack: `docker compose up -d`
- **Model/field missing**
  - Verify addon is installed/updated in that DB

## Parallel Usage

- You can keep the browser-based dev Odoo open while using `odoo shell`.
- With `--no-http`, shell and web UI run in parallel without port conflicts.

## Notes

- Use `local-db` skill for SQL-first diagnostics.
- Use this skill when behavior depends on ORM, computed fields, context, or access rights.

## Credential Hygiene

- Use local/dev credentials only.
- Do not commit real credential values into docs, scripts, or checklists.

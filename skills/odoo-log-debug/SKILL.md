---
name: odoo-log-debug
description: Inspect local Docker logs for Odoo services (odoo/nginx/postgres/ffdb) with safe defaults and repeatable filters.
---

# Odoo Log Debug (Local Docker)

_This skill follows `templates/SKILL.md` conventions._

Use this skill to diagnose runtime issues from container logs before changing code.

## When to Use

- Odoo UI/API behavior is failing and you need traceback/error context.
- Background jobs, cron, imports, or integrations fail intermittently.
- You need fast correlation across `odoo`, `nginx`, `postgres`, and `ffdb` logs.

## Prerequisites

- Start services from repo root:
  ```bash
  docker compose up -d
  ```
- Confirm target services are running:
  ```bash
  docker compose ps
  ```

## Safety Rules

- Prefer read-only log inspection.
- Do not restart containers unless explicitly requested.
- Do not execute destructive DB/actions from logs unless explicitly requested.

## Quick Commands

### Recent logs (last 15 minutes)

```bash
docker compose logs --since=15m odoo
```

### Follow live logs

```bash
docker compose logs -f --tail=200 odoo
```

### Multi-service correlation

```bash
docker compose logs --since=15m odoo nginx postgres ffdb
```

### Limit output size

```bash
docker compose logs --tail=300 odoo
```

## Common Filters

### Errors / Tracebacks

```bash
docker compose logs --since=30m odoo | rg -n "ERROR|CRITICAL|Traceback|Exception"
```

### Queue jobs / cron issues

```bash
docker compose logs --since=30m odoo | rg -n "queue|job|cron|failed|retry|timeout"
```

### HTTP / gateway problems

```bash
docker compose logs --since=30m nginx | rg -n " 4[0-9][0-9] | 5[0-9][0-9] |upstream|timeout"
```

### Postgres connection/query issues

```bash
docker compose logs --since=30m postgres | rg -n "ERROR|FATAL|deadlock|timeout|canceling statement"
```

## Minimal Workflow

1. Confirm service scope (`odoo` first, then related services).
2. Pull bounded logs (`--since` + `--tail`) to avoid noise.
3. Filter for error signatures (`ERROR`, `Traceback`, integration keyword).
4. Correlate timestamps across services if needed.
5. Summarize: symptom, first failing point, likely component, next check.

## Troubleshooting

- **`service "..." is not running`**
  - Start stack: `docker compose up -d`
- **No useful lines in current window**
  - Expand time range: `--since=2h`
  - Increase lines: `--tail=2000`
- **Too noisy logs**
  - Narrow by service and keyword with `rg`

## Notes

- For ORM-only behavior (computed fields/context/rules), switch to `odoo-shell-debug`.
- For SQL-first diagnostics, use `local-db`.
- For UI-visible issues, combine with `odoo-ui-check`.

## Credential Hygiene

- Use local/dev credentials only.
- Do not commit real credential values into docs, scripts, or checklists.

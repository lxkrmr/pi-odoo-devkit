---
name: odoo-translate
description: Export and update German translations (de.po) for Odoo addons. Use when asked to update/add translations for an addon.
---

# Odoo Translation Workflow

_This skill follows `.pi/skills/_template/SKILL.md` conventions._

## Prerequisites

- Local Odoo is running and reachable by `tools/octo`.
- Addon is installed in Odoo (required for export).
- German language `de_DE` is installed in Odoo.
- Translation terms for `de_DE` are loaded/updated (especially after fresh DB/init).

If auth/DB is not detected correctly, set env vars explicitly before running `tools/octo`:

```bash
export DATABASE=<db_name>
export DB_USER=<odoo_login>
export DB_PASSWORD=<odoo_password>
```


## Steps

### 0. Fresh instance only: update German translation terms in UI

After a new local DB/init, update terms once in Odoo UI before exporting:

- Settings → Translations → Application Terms → **Load a Translation** / **Update Terms**
- Language: `German / de_DE`

If this is skipped, exported `de.po` may be incomplete.

### 1. Download translations from Odoo

```bash
tools/octo translation download <addon_name>
```

This exports to:

- `addons/custom/<addon_name>/i18n/de.po`

### 2. Preview auto-fill from existing translations (dry run)

```bash
tools/octo translation from-existing <addon_name> --dry-run
```

### 3. Apply auto-fill from existing translations

Use `--no-backup` by default in this repo (Git already provides restore/history):

```bash
tools/octo translation from-existing <addon_name> --no-backup
```

### 4. Review remaining untranslated entries manually

For each empty `msgstr` in `addons/custom/<addon_name>/i18n/de.po`:

- **Identical in EN/DE** (e.g., "Material", "Status") → leave `msgstr ""` empty
- **Needs translation** → provide German translation

When editing, verify placeholders and formatting are preserved:

- `%s`, `%d`, `%(name)s`
- HTML/XML tags
- line breaks / punctuation

### 5. Summarize changes

Report:

- auto-filled count,
- manual translations added,
- entries intentionally left empty,
- entries still untranslated.

## Troubleshooting

- **Addon not found / not installed**
  - Ensure addon exists and is installed in target DB.
- **`de_DE` missing**
  - Install German language in Odoo first.
- **Exported file misses expected translations**
  - In Odoo UI, run Translation Terms update for `de_DE` (Load/Update Terms), then export again.
- **Connection/auth errors**
  - Ensure Odoo is running and env vars (`DATABASE`, `DB_USER`, `DB_PASSWORD`) are correct.

## Credential Hygiene

- Use local/dev credentials only.
- Do not commit real credential values into docs, scripts, or checklists.

---
name: odoo-ui-check
description: Check local Odoo UI in Chromium via Chrome DevTools Protocol (browser-tools), so the agent can inspect and validate UI behavior reliably.
---

# Odoo UI Check (Local Odoo)

Use this skill when you need to verify behavior in local Odoo UI (`http://localhost:8069`).

This skill uses the browser JS tooling adapted from Mario Zechner's `pi-skills` project:
https://github.com/badlogic/pi-skills

## Prerequisites

1. Start local stack:
   ```bash
   docker compose up -d
   ```
2. Ensure Odoo is reachable:
   - `http://localhost:8069`
3. Ensure browser-tools deps are installed (tooling lives in `skills/browser-tools/browser-tools`). Use the global `pi-odoo-skill-manager` command so automation and human usage stay consistent:
   ```bash
   pi-odoo-skill-manager wizard /path/to/odoo-project --yes
   ```
4. Ensure CDP is reachable:
   ```bash
   curl -s http://localhost:9222/json/version
   ```
5. Ensure local dev login is available in `.pi/local-secrets.md` (untracked).
   - If missing, create it from template:
     ```bash
     cp .pi/local-secrets.example.md .pi/local-secrets.md
     ```

## How browser access works

This skill opens Odoo in Chromium with Chrome DevTools Protocol (CDP) enabled on `:9222`.
That lets the browser JS helpers inspect and interact with the page deterministically.

Typical start commands (from `skills/browser-tools/browser-tools`):

```bash
./browser-start.js
./browser-nav.js http://localhost:8069
```

After Chromium is open, the user can:
- log in manually,
- navigate to the target menu/view,
- switch company/user context,
- ask for a concrete UI check.

Then the skill can run DOM checks (`browser-eval.js`), guided picker (`browser-pick.js`),
and screenshot (`browser-screenshot.js`) only when explicitly requested.

## Minimal Workflow

1. Open target Odoo page in Chromium.
2. Confirm context: correct user + company.
3. Check expected UI state (buttons/fields/labels/visibility).
4. Do minimal interaction needed.
5. Re-check expected result.
6. Report pass/fail and observed vs expected.

## UI Demo Mode (Show Records to Developer)

Use this mode when the user asks to *show records in the UI* (not only pass/fail validation).

1. Open Odoo and login (manual by user or local dev creds, if configured).
2. Navigate to the exact menu/list view.
3. Apply user-visible filters/sort/group in UI.
4. Return:
   - exact click path,
   - active filters,
   - visible record names/count.
5. If DOM automation is unavailable, provide deterministic manual steps immediately.

This keeps the output useful even when CDP automation is flaky.

## Required Behavior (Shared Skill Compliance)

When this skill is used, the agent must:

1. Check whether `.pi/local-secrets.md` exists.
2. If it does not exist, create it from `.pi/local-secrets.example.md`.
3. Read credentials only from `.pi/local-secrets.md` for local UI login automation.
4. Never write real credentials into tracked files (`SKILL.md`, `README.md`, addon code, etc.).
5. If credentials are still missing/placeholder, stop and ask the user to fill them.

## Rules

- Prefer DOM checks over screenshots.
- Screenshots only on explicit user request.
- Avoid side effects (create/post/delete) unless requested.
- If UI result is ambiguous, cross-check with:
  - `odoo-shell-debug`
  - `local-db`

## Useful DOM snippets

### Page context

```javascript
(function () {
  return {
    title: document.title,
    breadcrumb: Array.from(document.querySelectorAll('.breadcrumb-item, .o_breadcrumb li')).map(e => e.textContent.trim()).filter(Boolean),
  };
})()
```

### Visible action buttons

```javascript
(function () {
  return Array.from(document.querySelectorAll('button, a.btn, .o_form_button_save, .o_list_button_add'))
    .map(e => ({
      text: (e.textContent || '').trim(),
      disabled: !!e.disabled || e.classList.contains('disabled'),
      visible: !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length),
    }))
    .filter(b => b.text)
    .slice(0, 80);
})()
```

## Troubleshooting

- **CDP not reachable**
  - restart browser-tools Chrome and retry `curl` check.
- **`browser-eval.js` timeout while `browser-nav.js` works**
  - restart Chrome with `browser-start.js` and retry.
  - verify no stale debug process blocks tab attachment.
  - if still failing, continue with manual UI instructions and report limitation.
- **Wrong user/company behavior**
  - re-login / switch company and re-run check.
- **Flaky selector**
  - use browser element picker.

## Credential Hygiene

- Use local/dev credentials only.
- Do not commit real credential values into docs, scripts, or checklists.
- Store local UI credentials in an untracked file: `.pi/local-secrets.md`.
- Keep only placeholders/templates in tracked files (for example: `.pi/local-secrets.example.md`).
- If a project uses default/public dev creds, label them clearly as **LOCAL DEV ONLY**.
- If `.pi/local-secrets.md` is absent, create it from template before UI login attempts.

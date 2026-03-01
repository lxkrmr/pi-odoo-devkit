# Skills in `.pi/skills`

This directory contains local project skills used by the coding agent.

## Create a New Skill

1. Copy the template:

```bash
cp .pi/skills/_template/SKILL.md .pi/skills/<new-skill>/SKILL.md
```

2. Fill in frontmatter:

- `name`
- `description`

3. Replace placeholders in all sections.

4. Keep the standard sections where applicable:

- When to Use
- Prerequisites
- Steps
- Validation (User-Run)
- Troubleshooting
- Notes / Risks
- Credential Hygiene

## Conventions

- Keep commands copy-paste friendly.
- Prefer local/dev-safe defaults.
- Avoid hardcoded personal paths and real credential values.
- Include explicit safety notes for destructive actions.
- Keep scope tight: one skill = one clear workflow.

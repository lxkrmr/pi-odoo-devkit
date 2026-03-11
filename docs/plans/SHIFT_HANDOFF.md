# Shift Handoff — 2026-03-11

## Current state
- Release progression completed: `v0.2.0` → `v0.2.1` → `v0.3.0` (version in `pyproject.toml` is `0.3.0`).
- CLI contract v1 is defined and documented in `docs/cli-contract.md`.
- Deterministic contract coverage exists for automation commands:
  - `--output json`
  - `--describe`
  - `--dry-run` on mutating commands
- Runtime project targeting is now explicit-capable via `--project <path>` for:
  - automation: `components`, `enable-skill`, `disable-skill`
  - human-ops: `up`, `db`, `shell`, `test`, `lint`
- `doctor --output json` includes:
  - `checks_structured[]`
  - `recommendations_structured[]`
- `components --output json` includes:
  - `reason_code`
  - `requirement_failures[]`
- TUI was visually aligned closer to otto style:
  - cleaner section layout
  - stable white frame rendering using curses line drawing
  - status/footer polish

## Quality gates
- `./scripts/smoke-test.sh` is green.
- Contract checks: `scripts/test-cli-contracts.sh`.
- Golden snapshot checks: `scripts/test-cli-golden.sh`.
- Golden matcher supports `__path__` token for path-like fields.

## Docs added/updated
- `docs/cli-contract.md`
- `docs/operator-cheatsheet.md`
- `docs/releases/README.md`
- `docs/releases/RELEASE_CHECKLIST.md`
- `docs/releases/v0.2.0.md`
- `docs/releases/v0.2.1.md`
- `docs/releases/v0.3.0.md`
- `docs/plans/v0.3.0-delivery-plan.md`

## Operational notes
- For normal pipx installs, update with:
  - `pipx upgrade osmo`
- For local editable installs, refresh with:
  - `pipx uninstall osmo`
  - `pipx install --editable .`
- `pipx reinstall --editable .` is not valid.

## Suggested next steps
1. Add optional live filter UX in TUI (`/` filter, clear filter), aligned with otto feel.
2. Extend doctor recommendations with more command-ready `next_command` variants for common failures.
3. Prepare and tag `v0.3.0` on remote if not already done in current operator flow.

## Quick commands
```bash
# setup + gates
./scripts/bootstrap.sh
./scripts/install-git-hooks.sh
./scripts/smoke-test.sh

# contract visibility
osmo help --output json
osmo doctor --output json <PROJECT_REPO_PATH>
osmo components --project <PROJECT_REPO_PATH> --output json

# release flow
./scripts/smoke-test.sh
git tag -a v0.3.0 -m "osmo v0.3.0"
git push origin main --tags
```

# Work Package: Full rename to `osmo`

Date: 2026-03-10
Status: in progress
Owner: coding-agent

## Scope
Hard rename to `osmo` with zero legacy naming left in tracked files.

## Constraints
- No compatibility aliases.
- No "formerly ..." wording.
- Keep changes small and commit continuously.

## Execution Plan
1. Cleanup local global install first.
   - Uninstall previous pipx app/package.
   - Verify `pipx list` no longer contains the previous package.
2. Rename code/package entrypoints to `osmo`.
   - Python module file
   - `pyproject.toml` package + script entry
   - all internal references in scripts/tests/docs
3. Remove legacy name from all tracked content.
   - README, design docs, skills docs, plan docs, logs
   - verify via grep that no legacy token remains
4. Validate determinism.
   - run `./scripts/smoke-test.sh`
5. Finalize commits.
   - small semantic commits with Conventional Commit messages
6. Post-rename manual steps (user-owned).
   - user renames folder + repository
7. Final remote wiring (agent-owned after user step).
   - set `origin` to new repository URL

## Progress
- [x] (1) pipx cleanup executed
- [x] (2) core rename applied in working tree
- [x] (3) legacy token replacement applied in working tree
- [x] (4) smoke validation
- [ ] (5) commit split/finalization
- [x] (6) user repo rename
- [x] (7) set `origin` URL

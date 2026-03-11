# Work Package: Odoo Test Runner Tool (long-term)

Date: 2026-03-11
Status: queued

## Context
A dedicated tool should eventually replace project-local test wrapper scripts like:
- `../erp/run-tests.sh`

This aligns with single-responsibility architecture:
- `otto`: Odoo custom-addon workflows
- `osmo`: skill management
- test execution: separate focused tool

## Goal
Build a standalone deterministic CLI for running Odoo tests across projects.

## Scope (v0)
1. Execute standard Odoo test flows with explicit project targeting.
2. Support deterministic machine output (`--output json`).
3. Provide dry-run/planning mode where meaningful.
4. Return actionable exit codes and failure summaries.

## Non-goals (v0)
- No skill management logic.
- No coupling to osmo internals.
- No hidden dependency on otto runtime state.

## Interface direction
- one command surface
- one clear config path
- explicit inputs over cwd guessing

## Migration idea
1. Introduce new test runner tool in parallel.
2. Validate parity against existing `run-tests.sh` behavior.
3. Deprecate script usage gradually.
4. Remove legacy script path once parity is stable.

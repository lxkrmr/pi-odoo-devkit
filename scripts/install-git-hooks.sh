#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

git -C "$ROOT" config core.hooksPath .githooks
chmod +x "$ROOT/.githooks/pre-commit"

echo "Installed local git hooks (core.hooksPath=.githooks)"
echo "pre-commit now runs: ./scripts/smoke-test.sh"

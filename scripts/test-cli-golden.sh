#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
CLI="$ROOT/osmo.py"
CHECK="$ROOT/scripts/check-json-golden.py"
GOLDEN_DIR="$ROOT/tests/golden"

if [ ! -x "$PY" ]; then
  echo "Missing $PY" >&2
  echo "Run: ./scripts/bootstrap.sh" >&2
  exit 1
fi

TMP_PROJECT="$(mktemp -d)"
OUT="$(mktemp)"
cleanup() {
  rm -rf "$TMP_PROJECT"
  rm -f "$OUT"
}
trap cleanup EXIT

cat >"$TMP_PROJECT/docker-compose.yml" <<'YAML'
services: {}
YAML
mkdir -p "$TMP_PROJECT/.pi/skills/shared-osmo"
mkdir -p "$TMP_PROJECT/.pi"
printf "managed-by: osmo installer\n" >"$TMP_PROJECT/.pi/DEVKIT_AGENT_NOTES.md"

echo "[golden] wizard --dry-run"
"$PY" "$CLI" wizard "$TMP_PROJECT" --dry-run --output json >"$OUT"
"$PY" "$CHECK" "$GOLDEN_DIR/wizard-dry-run.json" "$OUT"

echo "[golden] cleanup --dry-run"
"$PY" "$CLI" cleanup "$TMP_PROJECT" --dry-run --output json >"$OUT"
"$PY" "$CHECK" "$GOLDEN_DIR/cleanup-dry-run.json" "$OUT"

echo "[golden] components --output json"
(
  cd "$TMP_PROJECT"
  "$PY" "$CLI" components --output json >"$OUT"
)
"$PY" "$CHECK" "$GOLDEN_DIR/components.json" "$OUT"

echo "[golden] doctor --output json"
TMP_DOCTOR="$(mktemp -d)"
cat >"$TMP_DOCTOR/docker-compose.yml" <<'YAML'
services: {}
YAML
set +e
"$PY" "$CLI" doctor "$TMP_DOCTOR" --output json >"$OUT"
DOCTOR_RC=$?
set -e
rm -rf "$TMP_DOCTOR"
if [ "$DOCTOR_RC" -ne 1 ]; then
  echo "Expected doctor exit code 1 on failing checks, got $DOCTOR_RC" >&2
  exit 1
fi
"$PY" "$CHECK" "$GOLDEN_DIR/doctor.json" "$OUT"

echo "[golden] done"

#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
CLI="$ROOT/osmo.py"

if [ ! -x "$PY" ]; then
  echo "Missing $PY" >&2
  echo "Run: ./scripts/bootstrap.sh" >&2
  exit 1
fi

OUT="$(mktemp)"
TMP_PROJECT=""
cleanup() {
  rm -f "$OUT"
  if [ -n "$TMP_PROJECT" ] && [ -d "$TMP_PROJECT" ]; then
    rm -rf "$TMP_PROJECT"
  fi
}
trap cleanup EXIT

assert_json_error() {
  local cmd="$1"
  local expected_code="$2"
  set +e
  eval "$cmd" >"$OUT" 2>/dev/null
  local rc=$?
  set -e
  if [ "$rc" -ne 2 ]; then
    echo "Expected exit code 2, got $rc for: $cmd" >&2
    exit 1
  fi
  "$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["ok"] is False; assert d["error"]["code"]==sys.argv[2]' "$OUT" "$expected_code"
}

test_help_contract_metadata() {
  echo "[contract] help contract metadata"
  "$PY" "$CLI" help --output json >"$OUT"
  "$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["ok"]; data=d["data"]; assert data["contract_version"]=="v1"; assert data["contract_spec"]=="docs/cli-contract.md"; details=data["details"]; assert isinstance(details,list) and details; first=details[0]; assert {"name","summary","contract_scope","automation_relevant","supports_dry_run","params"}.issubset(first.keys());
for item in details:
  for p in item["params"]:
    assert "kind" in p and "name" in p and "required" in p
    if p["kind"]=="option":
      assert "opts" in p
    elif p["kind"]=="argument":
      assert "nargs" in p
    else:
      raise AssertionError(f"unknown param kind: {p['kind']}")' "$OUT"
  "$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); details={x["name"]:x for x in d["data"]["details"]}; comp_opts={opt for p in details["components"]["params"] if p["kind"]=="option" for opt in p.get("opts", [])}; assert "--project" in comp_opts' "$OUT"
}

test_validation_errors() {
  echo "[contract] validation errors"
  assert_json_error "\"$PY\" \"$CLI\" wizard --yes --output json" "validation_error"
  assert_json_error "\"$PY\" \"$CLI\" cleanup --yes --output json" "validation_error"
}

test_cleanup_dry_run_no_mutation() {
  echo "[contract] dry-run must not mutate"
  TMP_PROJECT="$(mktemp -d)"
  cat >"$TMP_PROJECT/docker-compose.yml" <<'YAML'
services: {}
YAML
  mkdir -p "$TMP_PROJECT/.pi/skills/shared-osmo"
  mkdir -p "$TMP_PROJECT/.pi"
  printf "managed-by: osmo installer\n" >"$TMP_PROJECT/.pi/DEVKIT_AGENT_NOTES.md"

  "$PY" "$CLI" cleanup "$TMP_PROJECT" --dry-run --output json >"$OUT"
  "$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["ok"]; assert d["data"]["dry_run"] is True; assert any("PLAN:" in a for a in d["data"]["actions"])' "$OUT"

  if [ ! -d "$TMP_PROJECT/.pi/skills/shared-osmo" ]; then
    echo "cleanup --dry-run removed skills dir" >&2
    exit 1
  fi
  if [ ! -f "$TMP_PROJECT/.pi/DEVKIT_AGENT_NOTES.md" ]; then
    echo "cleanup --dry-run removed notes file" >&2
    exit 1
  fi
}

test_components_contract_fields() {
  echo "[contract] components reason codes"
  "$PY" "$CLI" components --project "$TMP_PROJECT" --output json >"$OUT"
  "$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["ok"]; skills=d["data"]["skills"]; assert isinstance(skills,list) and skills; required={"name","enabled","available","reason","reason_code","requirement_failures","description"}; assert required.issubset(skills[0].keys())' "$OUT"
}


test_project_option_runtime_commands() {
  echo "[contract] runtime commands support --project"
  "$PY" "$CLI" enable-skill dev-workbench --project "$TMP_PROJECT" --dry-run --output json >"$OUT"
  "$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["ok"]; assert d["command"]=="enable-skill"; assert d["data"]["dry_run"] is True' "$OUT"

  "$PY" "$CLI" disable-skill dev-workbench --project "$TMP_PROJECT" --dry-run --output json >"$OUT"
  "$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["ok"]; assert d["command"]=="disable-skill"; assert d["data"]["dry_run"] is True' "$OUT"
}

test_doctor_structured_contract() {
  echo "[contract] doctor structured recommendations"
  local tmp_doctor
  tmp_doctor="$(mktemp -d)"
  cat >"$tmp_doctor/docker-compose.yml" <<'YAML'
services: {}
YAML
  set +e
  "$PY" "$CLI" doctor "$tmp_doctor" --output json >"$OUT"
  local doctor_rc=$?
  set -e
  rm -rf "$tmp_doctor"
  if [ "$doctor_rc" -ne 1 ]; then
    echo "Expected doctor exit code 1 on failing checks, got $doctor_rc" >&2
    exit 1
  fi
  "$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["ok"]; rs=d["data"]["recommendations_structured"]; assert isinstance(rs,list) and rs; req={"code","severity","message","next_command"}; assert req.issubset(rs[0].keys()); assert any(r["code"] for r in rs); cs=d["data"]["checks_structured"]; assert isinstance(cs,list) and cs; req2={"name","check_code","category","resource","status","severity","message"}; assert req2.issubset(cs[0].keys()); assert any(c["check_code"]=="shared_skills_installed" for c in cs)' "$OUT"
}

main() {
  test_help_contract_metadata
  test_validation_errors
  test_cleanup_dry_run_no_mutation
  test_components_contract_fields
  test_project_option_runtime_commands
  test_doctor_structured_contract
  echo "[contract] done"
}

main

#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: bootstrap/install.sh [ERP_REPO_PATH] [--add-local-exclude]

Installs erp-devkit links into an ERP repo (.pi directory).

Options:
  --add-local-exclude   Add '.pi/' to <erp>/.git/info/exclude (local-only)
  -h, --help            Show this help

Resolution order for ERP repo path:
1) positional ERP_REPO_PATH
2) ERP_REPO_PATH environment variable
3) sibling directory named "erp" next to this devkit repo
4) current working directory (if it looks like the ERP repo)

Examples:
  ./bootstrap/install.sh /Users/me/workspace/erp
  ./bootstrap/install.sh /Users/me/workspace/erp --add-local-exclude
  ERP_REPO_PATH=~/workspace/erp ./bootstrap/install.sh --add-local-exclude
EOF
}

DEVKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ERP_ARG=""
ADD_LOCAL_EXCLUDE=0

for arg in "$@"; do
  case "$arg" in
    -h|--help)
      usage
      exit 0
      ;;
    --add-local-exclude)
      ADD_LOCAL_EXCLUDE=1
      ;;
    -*)
      echo "Unknown option: $arg" >&2
      usage
      exit 1
      ;;
    *)
      if [[ -n "$ERP_ARG" ]]; then
        echo "Only one ERP_REPO_PATH positional argument is supported." >&2
        usage
        exit 1
      fi
      ERP_ARG="$arg"
      ;;
  esac
done

resolve_erp_dir() {
  if [[ -n "${1:-}" ]]; then
    echo "$1"
    return
  fi

  if [[ -n "${ERP_REPO_PATH:-}" ]]; then
    echo "$ERP_REPO_PATH"
    return
  fi

  local sibling
  sibling="$(cd "$DEVKIT_DIR/.." && pwd)/erp"
  if [[ -d "$sibling" ]]; then
    echo "$sibling"
    return
  fi

  if [[ -f "docker-compose.yml" && -d ".pi" ]]; then
    pwd
    return
  fi

  echo ""
}

ERP_DIR="$(resolve_erp_dir "$ERP_ARG")"

if [[ -z "$ERP_DIR" ]]; then
  echo "Could not resolve ERP repo path." >&2
  usage
  exit 1
fi

ERP_DIR="$(cd "$ERP_DIR" && pwd)"

if [[ ! -d "$ERP_DIR" ]]; then
  echo "ERP repo path does not exist: $ERP_DIR" >&2
  exit 1
fi

if [[ ! -f "$ERP_DIR/docker-compose.yml" ]]; then
  echo "Not an ERP repo (missing docker-compose.yml): $ERP_DIR" >&2
  exit 1
fi

mkdir -p "$ERP_DIR/.pi/skills" "$ERP_DIR/.pi/tools"

# Create stable shared links (do not overwrite existing unrelated paths)
ln -sfn "$DEVKIT_DIR/skills" "$ERP_DIR/.pi/skills/shared-devkit"
ln -sfn "$DEVKIT_DIR/commands" "$ERP_DIR/.pi/tools/shared-devkit"

# Optional convenience link for command runner if not already present
if [[ ! -e "$ERP_DIR/.pi/tools/devkit" ]]; then
  ln -s "$DEVKIT_DIR/commands/dev" "$ERP_DIR/.pi/tools/devkit"
fi

if [[ "$ADD_LOCAL_EXCLUDE" -eq 1 ]]; then
  EXCLUDE_FILE="$ERP_DIR/.git/info/exclude"
  mkdir -p "$(dirname "$EXCLUDE_FILE")"

  if [[ -f "$EXCLUDE_FILE" ]] && grep -Fxq '.pi/' "$EXCLUDE_FILE"; then
    echo "Local git exclude already contains '.pi/': $EXCLUDE_FILE"
  else
    printf "\n# local pi files\n.pi/\n" >> "$EXCLUDE_FILE"
    echo "Added local git exclude '.pi/' to: $EXCLUDE_FILE"
  fi
fi

echo "Installed erp-devkit links into: $ERP_DIR"
echo "  .pi/skills/shared-devkit -> $DEVKIT_DIR/skills"
echo "  .pi/tools/shared-devkit  -> $DEVKIT_DIR/commands"
if [[ -L "$ERP_DIR/.pi/tools/devkit" ]]; then
  echo "  .pi/tools/devkit          -> $DEVKIT_DIR/commands/dev"
fi

echo
if [[ "$ADD_LOCAL_EXCLUDE" -eq 0 ]]; then
  echo "Tip: to hide local .pi changes from git status, rerun with --add-local-exclude"
  echo "  ./bootstrap/install.sh ${ERP_ARG:-<path-to-erp>} --add-local-exclude"
  echo
fi

echo "Usage examples:"
echo "  $ERP_DIR/.pi/tools/devkit help"
echo "  $ERP_DIR/.pi/tools/devkit up"

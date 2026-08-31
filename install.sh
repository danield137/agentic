#!/usr/bin/env bash
#
# Links this repo's Copilot customizations into the Copilot CLI home directory.
#
# Usage:
#   ./install.sh                  link everything this repo provides
#   ./install.sh instructions     link only the named components
#   ./install.sh --dry-run        show what would happen, change nothing
#   ./install.sh --force          replace existing targets without prompting
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COPILOT_DIR="${COPILOT_HOME:-$HOME/.copilot}"
BACKUP_DIR="$COPILOT_DIR/.agentic-backup/$(date +%Y%m%d-%H%M%S)"

# Everything this repo may own inside the Copilot home directory. Entries that
# do not exist in the repo are skipped, so new ones can simply be created here.
ALL_COMPONENTS=(
  instructions
  skills
  agents
  hooks
  mcp-config.json
)

DRY_RUN=0
FORCE=0
COMPONENTS=()

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --force) FORCE=1 ;;
    -h|--help) sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown option: $arg" >&2; exit 2 ;;
    *)
      for known in "${ALL_COMPONENTS[@]}"; do
        if [ "$arg" = "$known" ]; then
          COMPONENTS+=("$arg")
          continue 2
        fi
      done
      echo "unknown component: $arg (expected one of: ${ALL_COMPONENTS[*]})" >&2
      exit 2
      ;;
  esac
done

[ ${#COMPONENTS[@]} -eq 0 ] && COMPONENTS=("${ALL_COMPONENTS[@]}")

say() { printf '%s\n' "$*"; }
run() { if [ "$DRY_RUN" -eq 1 ]; then say "  would: $*"; else "$@"; fi; }

backup() {
  local target="$1"
  run mkdir -p "$BACKUP_DIR"
  run mv "$target" "$BACKUP_DIR/"
  say "  backed up existing $(basename "$target") -> $BACKUP_DIR/"
}

link_one() {
  local name="$1"
  local src="$REPO_DIR/$name"
  local dst="$COPILOT_DIR/$name"

  if [ ! -e "$src" ]; then
    say "skip $name (not in repo)"
    return
  fi

  say "link $name"

  if [ -L "$dst" ]; then
    if [ "$(readlink "$dst")" = "$src" ]; then
      say "  already linked"
      return
    fi
    run rm "$dst"
  elif [ -e "$dst" ]; then
    if [ "$FORCE" -ne 1 ] && [ "$DRY_RUN" -ne 1 ]; then
      read -r -p "  $dst exists. Back it up and replace? [y/N] " reply
      case "$reply" in
        [yY]*) ;;
        *) say "  skipped"; return ;;
      esac
    fi
    backup "$dst"
  fi

  run ln -s "$src" "$dst"
  say "  $dst -> $src"
}

say "repo:    $REPO_DIR"
say "copilot: $COPILOT_DIR"
say "linking: ${COMPONENTS[*]}"
[ "$DRY_RUN" -eq 1 ] && say "(dry run)"
say ""

run mkdir -p "$COPILOT_DIR"
for name in "${COMPONENTS[@]}"; do
  link_one "$name"
done

say ""
say "Done. Start a new session, or run '/skills reload' in an active one."

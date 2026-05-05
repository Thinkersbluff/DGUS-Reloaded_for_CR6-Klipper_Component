#!/usr/bin/env bash
set -euo pipefail

# Add host-local git excludes for DGUS files so Moonraker won't flag the repo dirty.
# Usage: run this on the Klipper host (it defaults to $HOME/klipper). It edits
# $KLIPPER_DIR/.git/info/exclude so no commits are created.

KLIPPER_DIR_DEFAULT="${KLIPPER_DIR_DEFAULT:-$HOME/klipper}"
EXCLUDE_FILE="$KLIPPER_DIR_DEFAULT/.git/info/exclude"

PATTERNS=(
  "klippy/extras/t5uid1/"
  "klippy/extras/"
  "src/stm32/t5uid1/"
  "src/generic/t5uid1/"
)

if [ ! -d "$KLIPPER_DIR_DEFAULT" ]; then
  printf 'ERROR: Klipper directory not found: %s\n' "$KLIPPER_DIR_DEFAULT" >&2
  exit 2
fi

mkdir -p "$(dirname "$EXCLUDE_FILE")"

for p in "${PATTERNS[@]}"; do
  # add pattern if not already present
  if ! grep -Fxq "$p" "$EXCLUDE_FILE" 2>/dev/null; then
    echo "$p" >> "$EXCLUDE_FILE"
    echo "Added: $p"
  else
    echo "Already present: $p"
  fi
done

echo "Host-local git exclude updated: $EXCLUDE_FILE"
echo "Run 'git status --porcelain' in $KLIPPER_DIR_DEFAULT to verify."

#!/usr/bin/env bash
set -euo pipefail

# backup_klipper.sh
# Creates a timestamped tar.gz backup of ~/klipper and records the current
# git commit (if the tree is a git repo).

BACKUP_DIR="${1:-$HOME/klipper_backups}"
KLIPPER_DIR="${2:-$HOME/klipper}"
TS=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

if [ ! -d "$KLIPPER_DIR" ]; then
  echo "Error: klipper directory not found at $KLIPPER_DIR" >&2
  exit 1
fi

ARCHIVE="$BACKUP_DIR/klipper.$TS.tar.gz"
COMMIT_FILE="$BACKUP_DIR/klipper.$TS.commit"

echo "Creating backup of $KLIPPER_DIR -> $ARCHIVE"
tar -C "$(dirname "$KLIPPER_DIR")" -czf "$ARCHIVE" "$(basename "$KLIPPER_DIR")"

# If the klipper tree is a git repository, record the current commit SHA
if [ -d "$KLIPPER_DIR/.git" ]; then
  if git -C "$KLIPPER_DIR" rev-parse --verify HEAD >/dev/null 2>&1; then
    git -C "$KLIPPER_DIR" rev-parse HEAD > "$COMMIT_FILE" || true
    echo "Recorded commit SHA in $COMMIT_FILE"
  fi
fi

echo "Backup complete: $ARCHIVE"
echo "Backups kept in: $BACKUP_DIR"

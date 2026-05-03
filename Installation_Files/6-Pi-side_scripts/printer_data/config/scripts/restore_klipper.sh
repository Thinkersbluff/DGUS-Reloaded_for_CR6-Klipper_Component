#!/usr/bin/env bash
set -euo pipefail

# restore_klipper.sh
# Restores a tar.gz backup created by backup_klipper.sh into ~/klipper.
# Usage:
#   restore_klipper.sh /path/to/klipper.20260308_123456.tar.gz
# Options:
#   --no-build   : do not run `make` after restoring (useful if you will build separately)


# Parse args: accept optional archive path or a directory, and optional --no-build flag.
ARCHIVE=""
BACKUP_DIR_DEFAULT="$HOME/klipper_backups"
# Default: do not build after restore. Use --build to run make after restoring.
NO_BUILD=1

while [ "$#" -gt 0 ]; do
  case "$1" in
    --build)
      NO_BUILD=0; shift ;;
    --help)
      echo "Usage: $0 [archive.tar.gz | backup_dir] [--build]" >&2
      exit 0 ;;
    *)
      if [ -z "$ARCHIVE" ]; then
        ARCHIVE="$1"
      else
        echo "Unknown extra arg: $1" >&2; exit 1
      fi
      shift ;;
  esac
done

choose_archive() {
  local dir="$1"
  mapfile -t files < <(ls -1rt "$dir"/klipper.*.tar.gz 2>/dev/null || true)
  if [ "${#files[@]}" -eq 0 ]; then
    echo "No backup archives found in $dir" >&2
    return 1
  fi
  echo "Available backups in $dir:"
  local i=1
  for f in "${files[@]}"; do
    echo "  $i) $(basename "$f")"
    i=$((i+1))
  done
  while true; do
    read -rp "Enter number to restore (or q to cancel): " sel
    case "$sel" in
      [Qq]) echo "Aborted."; return 2 ;;
      '' ) echo "Please enter a number.";;
      *)
        if ! echo "$sel" | grep -Eq '^[0-9]+$'; then
          echo "Invalid selection"; continue
        fi
        if [ "$sel" -ge 1 ] && [ "$sel" -le "${#files[@]}" ]; then
          ARCHIVE="${files[$((sel-1))]}"
          echo "Selected: $ARCHIVE"
          return 0
        else
          echo "Selection out of range"; continue
        fi
        ;;
    esac
  done
}

# If user provided a directory or nothing, prompt to choose an archive
if [ -z "$ARCHIVE" ]; then
  if choose_archive "$BACKUP_DIR_DEFAULT"; then
    :
  else
    exit 1
  fi
elif [ -d "$ARCHIVE" ]; then
  # user passed a directory
  if choose_archive "$ARCHIVE"; then
    :
  else
    exit 1
  fi
fi

if [ -z "$ARCHIVE" ]; then
  echo "Error: no archive selected." >&2
  exit 1
fi

if [ ! -f "$ARCHIVE" ]; then
  echo "Error: archive not found: $ARCHIVE" >&2
  exit 1
fi

KLIPPER_DIR="$HOME/klipper"

read -rp "This will overwrite $KLIPPER_DIR. Continue? [y/N]: " yn
case $yn in
  [Yy]*) ;;
  *) echo "Aborted."; exit 1;;
esac

echo "Stopping klipper service (if running)"
sudo systemctl stop klipper || true

echo "Removing existing $KLIPPER_DIR"
rm -rf "$KLIPPER_DIR"

echo "Extracting $ARCHIVE to $HOME"
tar -C "$HOME" -xzf "$ARCHIVE"

if [ "$NO_BUILD" -eq 0 ]; then
  if [ -f "$KLIPPER_DIR/Makefile" ]; then
    echo "Running make -j\$(nproc) in $KLIPPER_DIR"
    (cd "$KLIPPER_DIR" && make -j"$(nproc)") || echo "Build failed; please inspect output"
  else
    echo "No Makefile found in restored tree; skipping build"
  fi
else
  echo "Default: skipping build step (use --build to run make after restore)"
fi

echo "Starting klipper service"
sudo systemctl start klipper || true

echo "Restore complete. Verify logs with: sudo journalctl -u klipper -n 200 --no-pager"

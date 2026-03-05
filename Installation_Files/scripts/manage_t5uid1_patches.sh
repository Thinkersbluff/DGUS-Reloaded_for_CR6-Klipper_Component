#!/usr/bin/env bash
set -euo pipefail

# Manage T5UID1 patches in a Klipper tree
# - prepare : remove DGUS added lines from Kconfig/Makefile and save backups (use before updating Klipper)
# - reapply : add the DGUS include lines back to updated Kconfig/Makefile (use after updating Klipper)

KLIPPER_DIR_DEFAULT="${KLIPPER_DIR_DEFAULT:-$HOME/klipper}"
KCONFIG_PATH="$KLIPPER_DIR_DEFAULT/src/stm32/Kconfig"
MAKEFILE_PATH="$KLIPPER_DIR_DEFAULT/src/stm32/Makefile"

TS() { date +%Y%m%d%H%M%S; }

usage() {
  cat <<EOF
Usage: $0 prepare|reapply|status

Commands:
  prepare   Remove previously-added DGUS lines from Kconfig/Makefile and save backups.
            Use this before pulling upstream Klipper changes.
  reapply   Re-add the DGUS include lines to the (possibly updated) Kconfig/Makefile.
            Use this after updating Klipper and before building firmware.
  status    Show whether the DGUS lines are present in the target files.

This script only edits the two files listed above; it creates timestamped backups
under ~/.dgus_patch_backups/ so you can recover if needed.
EOF
}

require_file() {
  local f="$1"
  if [ ! -f "$f" ]; then
    printf 'ERROR: expected file not found: %s\n' "$f" >&2
    exit 2
  fi
}

backup_dir() {
  local tag="$1"
  local dir="$HOME/.dgus_patch_backups/${tag}_$(TS)"
  mkdir -p "$dir"
  echo "$dir"
}

remove_added_lines() {
  local file="$1"
  local dir="$2"
  local tmp
  tmp="$(mktemp)"
  cp -a "$file" "$dir/" || true
  # remove the specific include/source line and any comment line we add
  grep -v -F 'src/stm32/t5uid1/Kconfig' "$file" | grep -v -F '# Added by install_dgus_minimal.sh' > "$tmp" || true
  mv "$tmp" "$file"
}

remove_makefile_lines() {
  local file="$1"
  local dir="$2"
  local tmp
  tmp="$(mktemp)"
  cp -a "$file" "$dir/" || true
  grep -v -F 'src/stm32/t5uid1/Makefile' "$file" | grep -v -F '# Added by install_dgus_minimal.sh' > "$tmp" || true
  mv "$tmp" "$file"
}

add_kconfig_line() {
  local file="$1"
  # idempotent: skip if already present
  if grep -Fq 'src/stm32/t5uid1/Kconfig' "$file" 2>/dev/null; then
    echo "Kconfig already contains t5uid1 entry"
    return
  fi
  printf "\n# Added by install_dgus_minimal.sh\nsource \"src/stm32/t5uid1/Kconfig\"\n" >> "$file"
}

add_makefile_line() {
  local file="$1"
  if grep -Fq 'src/stm32/t5uid1/Makefile' "$file" 2>/dev/null; then
    echo "Makefile already contains t5uid1 entry"
    return
  fi
  printf "\n# Added by install_dgus_minimal.sh\ninclude src/stm32/t5uid1/Makefile\n" >> "$file"
}

cmd="$1"
case "$cmd" in
  prepare)
    require_file "$KCONFIG_PATH"
    require_file "$MAKEFILE_PATH"
    BDIR="$(backup_dir prepare)"
    echo "Backing up originals to $BDIR"
    cp -a "$KCONFIG_PATH" "$BDIR/" 
    cp -a "$MAKEFILE_PATH" "$BDIR/" 

    echo "Removing DGUS lines from Kconfig and Makefile (preferred: restore tracked files)"
    # Prefer restoring tracked files to HEAD so local edits are discarded cleanly
    if command -v git >/dev/null 2>&1 && [ -d "${KLIPPER_DIR_DEFAULT}/.git" ]; then
      echo "Restoring tracked files to HEAD using git restore"
      (cd "$KLIPPER_DIR_DEFAULT" && git restore src/stm32/Kconfig src/stm32/Makefile) || true
    else
      echo "Git not available or not a git repo; falling back to line removal"
      remove_added_lines "$KCONFIG_PATH" "$BDIR"
      remove_makefile_lines "$MAKEFILE_PATH" "$BDIR"
    fi

    echo "Done. You can now update Klipper (git pull) and then run '$0 reapply'."
    ;;

  reapply)
    require_file "$KCONFIG_PATH"
    require_file "$MAKEFILE_PATH"
    BDIR="$(backup_dir reapply)"
    echo "Backing up current files to $BDIR"
    cp -a "$KCONFIG_PATH" "$BDIR/"
    cp -a "$MAKEFILE_PATH" "$BDIR/"

    echo "Adding DGUS lines back to Kconfig and Makefile (idempotent)"
    add_kconfig_line "$KCONFIG_PATH"
    add_makefile_line "$MAKEFILE_PATH"

    echo "Done. You may now run make to build klipper.bin for your board."
    ;;

  status)
    echo "Kconfig:"
    if [ -f "$KCONFIG_PATH" ] && grep -Fq 'src/stm32/t5uid1/Kconfig' "$KCONFIG_PATH" 2>/dev/null; then
      echo "  contains t5uid1 include"
    else
      echo "  does NOT contain t5uid1 include"
    fi
    echo "Makefile:"
    if [ -f "$MAKEFILE_PATH" ] && grep -Fq 'src/stm32/t5uid1/Makefile' "$MAKEFILE_PATH" 2>/dev/null; then
      echo "  contains t5uid1 include"
    else
      echo "  does NOT contain t5uid1 include"
    fi
    ;;

  *)
    usage
    exit 1
    ;;
esac

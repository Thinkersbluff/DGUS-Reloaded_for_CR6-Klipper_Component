#!/usr/bin/env bash
set -euo pipefail

# Lightweight installer for DGUS-Reloaded assets
# - sparse-clones only the Installation_Files tree
# - copies extras and src/t5uid1 if present
# - idempotently patches ~/klipper/src/stm32/Kconfig and Makefile

REPO_URL="https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component.git"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/dgus_install.XXXXXX")"
SPARSE_PATHS=("Installation_Files")
KLIPPER_DIR_DEFAULT="$HOME/klipper"

prompt_yesno() {
  while true; do
    read -rp "$1 [y/n]: " yn
    case $yn in
      [Yy]*) return 0;;
      [Nn]*) return 1;;
      *) echo "Please answer y or n.";;
    esac
  done
}

backup_file() {
  local f="$1"
  if [ -f "$f" ]; then
    cp -a "$f" "${f}.bak.$(date +%Y%m%d%H%M%S)"
  fi
}

patch_kconfig_idempotent() {
  local kconfig="$1"
  local line='source "src/stm32/t5uid1/Kconfig"'
  if grep -Fq 'src/stm32/t5uid1/Kconfig' "$kconfig" 2>/dev/null; then
    echo "Kconfig already patched: $kconfig"
    return 0
  fi
  echo "Patching $kconfig to include t5uid1 Kconfig (idempotent)"
  backup_file "$kconfig"
  # Append the source line if not present
  printf "\n# Added by install_dgus_minimal.sh\n%s\n" "$line" >> "$kconfig"
}

patch_makefile_idempotent() {
  local makefile="$1"
  local line='include src/stm32/t5uid1/Makefile'
  if grep -Fq 'src/stm32/t5uid1/Makefile' "$makefile" 2>/dev/null; then
    echo "Makefile already patched: $makefile"
    return 0
  fi
  echo "Patching $makefile to include t5uid1 Makefile (idempotent)"
  backup_file "$makefile"
  printf "\n# Added by install_dgus_minimal.sh\n%s\n" "$line" >> "$makefile"
}

echo "Preflight: checking for a Klipper tree..."
# Ensure required external commands are available
for cmd in git rsync; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    printf 'Required command not found: %s\n' "$cmd" >&2
    printf 'Please install %s and re-run this script.\n' "$cmd" >&2
    exit 1
  fi
done
if [ -d "$KLIPPER_DIR_DEFAULT" ] && [ -f "$KLIPPER_DIR_DEFAULT/src/stm32/Makefile" ]; then
  echo "Found Klipper at $KLIPPER_DIR_DEFAULT"
else
  echo "No Klipper detected at $KLIPPER_DIR_DEFAULT."
  if prompt_yesno "Install KIAUH (installer helper) now? (or Cancel to abort)"; then
    git clone https://github.com/angristan/kiauh.git "$HOME/kiauh" || true
    echo "Run '$HOME/kiauh/kiauh.sh' to install Klipper interactively, then re-run this script."
    exit 0
  else
    echo "Aborting installation.";
    exit 1
  fi
fi

echo "Sparse-cloning Installation_Files to $TMP_DIR (only necessary files)..."
rm -rf "$TMP_DIR"
git clone --no-checkout --depth 1 --filter=blob:none "$REPO_URL" "$TMP_DIR"
cd "$TMP_DIR"
git sparse-checkout init --cone
git sparse-checkout set "${SPARSE_PATHS[@]}"
git checkout

echo "Select motherboard target for printer configs (choose 0 to skip):"
echo "  1) Creality 4.5.3 (or ERA 1.1.0.3)"
echo "  2) Creality 4.5.2"
echo "  3) BTT SKR CR6 V1.0"
echo "  0) None / stage/apply only core files"
read -rp "Enter 0-3: " mb_choice

case "$mb_choice" in
  1)
    SRC_DIR_REL="Development_Project/Related Changes/Creality CR6 Mobo/Custom Klipper host files/For ERA 1.1.0.3 and 4.5.3 MB/"
    ;;
  2)
    SRC_DIR_REL="Development_Project/Related Changes/Creality CR6 Mobo/Custom Klipper host files/For 4.5.2 MB/"
    ;;
  3)
    SRC_DIR_REL="Development_Project/Related Changes/BTT SKR CR6 Only/Custom Klipper host files/"
    ;;
  *)
    SRC_DIR_REL=""
    echo "No board-specific configs will be staged/applied."
    ;;
esac

# If a board was selected, ensure its folder exists in the sparse-cloned tree.
if [ -n "$SRC_DIR_REL" ]; then
  if [ ! -d "$TMP_DIR/Installation_Files/$SRC_DIR_REL" ]; then
    echo "ERROR: Selected board-specific folder not found in fetched install tree:" >&2
    echo "  $TMP_DIR/Installation_Files/$SRC_DIR_REL" >&2
    echo "Aborting to avoid applying incomplete board-specific files." >&2
    rm -rf "$TMP_DIR"
    exit 1
  fi
fi

echo "Files fetched. Next: choose how to deploy files:"
echo "  1) Overwrite live Klipper files"
echo "  2) Stage printer_data for manual compare/edit (recommended)"
echo "  3) Cancel"
echo "  4) Apply from existing staging area (apply files previously staged at ~/t5uid1_staging)"
read -rp "Enter 1,2,3 or 4: " choice

if [ "$choice" = "3" ]; then
  echo "Cancelling. Cleaning up..."
  rm -rf "$TMP_DIR"
  exit 0
fi

if [ "$choice" = "2" ]; then
  echo "Staging targeted files into $HOME/t5uid1_staging"
  STAGE_DIR="$HOME/t5uid1_staging"
  rm -rf "$STAGE_DIR"
  mkdir -p "$STAGE_DIR"

  # stage extras
  if [ -d "$TMP_DIR/Installation_Files/klippy_extras_Extensions/klippy/extras/t5uid1" ]; then
    rsync -av --progress "$TMP_DIR/Installation_Files/klippy_extras_Extensions/klippy/extras/t5uid1/" "$STAGE_DIR/klippy_extras_Extensions/klippy/extras/t5uid1/"
  fi

  # stage source trees if present
  if [ -d "$TMP_DIR/Installation_Files/src/stm32/t5uid1" ]; then
    rsync -av --progress "$TMP_DIR/Installation_Files/src/stm32/t5uid1/" "$STAGE_DIR/src/stm32/t5uid1/"
  fi
  if [ -d "$TMP_DIR/Installation_Files/src/generic/t5uid1" ]; then
    rsync -av --progress "$TMP_DIR/Installation_Files/src/generic/t5uid1/" "$STAGE_DIR/src/generic/t5uid1/"
  fi

  # stage board-specific printer configs if selected
  if [ -n "$SRC_DIR_REL" ]; then
    SRC_PATH="$TMP_DIR/Installation_Files/$SRC_DIR_REL"
    if [ -d "$SRC_PATH" ]; then
      rsync -av --progress "$SRC_PATH" "$STAGE_DIR/printer_data/"
    else
      echo "Board-specific config not found at $SRC_PATH; skipping that part."
    fi
  fi

  # stage entire scripts folder so users can review all helpers locally
  if [ -d "$TMP_DIR/Installation_Files/scripts" ]; then
    mkdir -p "$STAGE_DIR/scripts/dgus-reloaded"
    rsync -av --progress "$TMP_DIR/Installation_Files/scripts/" "$STAGE_DIR/scripts/dgus-reloaded/"
  fi

  echo "Staged files at $STAGE_DIR. Review before copying to your live Klipper tree."
else
  echo "Applying files into $KLIPPER_DIR_DEFAULT (will preserve local files; stop Klipper first)."
  if prompt_yesno "Stop klipper service now before copying?"; then
    sudo systemctl stop klipper || true
  fi

  # copy extras
  mkdir -p "$KLIPPER_DIR_DEFAULT/klippy/extras"
  if [ -d "$TMP_DIR/Installation_Files/klippy_extras_Extensions/klippy/extras/t5uid1" ]; then
    rsync -av --progress "$TMP_DIR/Installation_Files/klippy_extras_Extensions/klippy/extras/t5uid1/" "$KLIPPER_DIR_DEFAULT/klippy/extras/t5uid1/"
    echo "Copied klippy extras."
  fi

  # copy src trees if present in the cloned Installation_Files
  if [ -d "$TMP_DIR/Installation_Files/src/stm32/t5uid1" ] || [ -d "$TMP_DIR/Installation_Files/src/generic/t5uid1" ]; then
    mkdir -p "$KLIPPER_DIR_DEFAULT/src/stm32"
    mkdir -p "$KLIPPER_DIR_DEFAULT/src/generic"
    if [ -d "$TMP_DIR/Installation_Files/src/stm32/t5uid1" ]; then
      rsync -av --progress "$TMP_DIR/Installation_Files/src/stm32/t5uid1/" "$KLIPPER_DIR_DEFAULT/src/stm32/t5uid1/"
    fi
    if [ -d "$TMP_DIR/Installation_Files/src/generic/t5uid1" ]; then
      rsync -av --progress "$TMP_DIR/Installation_Files/src/generic/t5uid1/" "$KLIPPER_DIR_DEFAULT/src/generic/t5uid1/"
    fi
  fi

  # Idempotently patch Kconfig and Makefile in the target Klipper tree
  if [ -f "$KLIPPER_DIR_DEFAULT/src/stm32/Kconfig" ]; then
    patch_kconfig_idempotent "$KLIPPER_DIR_DEFAULT/src/stm32/Kconfig"
  else
    echo "Warning: $KLIPPER_DIR_DEFAULT/src/stm32/Kconfig not found; skipping Kconfig patch."
  fi

  if [ -f "$KLIPPER_DIR_DEFAULT/src/stm32/Makefile" ]; then
    patch_makefile_idempotent "$KLIPPER_DIR_DEFAULT/src/stm32/Makefile"
  else
    echo "Warning: $KLIPPER_DIR_DEFAULT/src/stm32/Makefile not found; skipping Makefile patch."
  fi

  # copy Additional files (printer_data etc) optionally
  if prompt_yesno "Overwrite contents of your printer_data/printer config files with repo copies?"; then
    if [ -n "$SRC_DIR_REL" ]; then
      SRC_PATH="$TMP_DIR/Installation_Files/$SRC_DIR_REL"
      if [ -d "$SRC_PATH" ]; then
        echo "Copying printer config files from chosen source to $HOME/printer_data/"
        rsync -av --progress "$SRC_PATH" "$HOME/printer_data/" || true
      else
        echo "Expected files not found in $SRC_PATH — falling back to generic 'Related Changes' if present."
        if [ -d "$TMP_DIR/Installation_Files/Related Changes/" ]; then
          rsync -av --progress "$TMP_DIR/Installation_Files/Related Changes/" "$HOME/printer_data/" || true
        else
          echo "No printer_data found in the fetched install tree."
        fi
      fi
    else
      echo "No board selected earlier; skipping printer_data copy."
    fi
  else
    echo "Skipping overwrite of printer_data. You can manually copy staged files from $TMP_DIR."
  fi

  if prompt_yesno "Start klipper service now?"; then
    sudo systemctl start klipper || true
  else
    echo "Remember to start klipper when ready."
  fi
fi

  # install git_ignore helper into the Klipper scripts folder so user can run it if needed
  if [ -f "$TMP_DIR/Installation_Files/scripts/git_ignore.sh" ]; then
    mkdir -p "$KLIPPER_DIR_DEFAULT/scripts/dgus-reloaded"
    # copy all scripts into the Klipper scripts folder
    rsync -av --progress "$TMP_DIR/Installation_Files/scripts/" "$KLIPPER_DIR_DEFAULT/scripts/dgus-reloaded/"
    chmod +x "$KLIPPER_DIR_DEFAULT/scripts/dgus-reloaded"/*.sh || true
    echo "Installed scripts to $KLIPPER_DIR_DEFAULT/scripts/dgus-reloaded/ (run git_ignore.sh when you need to add host-local ignores)"
  fi

if [ "$choice" = "4" ]; then
  STAGE_DIR="$HOME/t5uid1_staging"
  if [ ! -d "$STAGE_DIR" ]; then
    echo "ERROR: staging directory not found at $STAGE_DIR" >&2
    echo "Run the script in staging mode first, edit files in $STAGE_DIR, then re-run with option 4." >&2
    rm -rf "$TMP_DIR"
    exit 1
  fi

  echo "Applying files from staging directory $STAGE_DIR into $KLIPPER_DIR_DEFAULT"
  if prompt_yesno "Stop klipper service now before copying?"; then
    sudo systemctl stop klipper || true
  fi

  # copy extras from staging
  if [ -d "$STAGE_DIR/klippy_extras_Extensions/klippy/extras/t5uid1" ]; then
    mkdir -p "$KLIPPER_DIR_DEFAULT/klippy/extras"
    rsync -av --progress "$STAGE_DIR/klippy_extras_Extensions/klippy/extras/t5uid1/" "$KLIPPER_DIR_DEFAULT/klippy/extras/t5uid1/"
  fi

  # copy src trees from staging
  if [ -d "$STAGE_DIR/src/stm32/t5uid1" ]; then
    mkdir -p "$KLIPPER_DIR_DEFAULT/src/stm32"
    rsync -av --progress "$STAGE_DIR/src/stm32/t5uid1/" "$KLIPPER_DIR_DEFAULT/src/stm32/t5uid1/"
  fi
  if [ -d "$STAGE_DIR/src/generic/t5uid1" ]; then
    mkdir -p "$KLIPPER_DIR_DEFAULT/src/generic"
    rsync -av --progress "$STAGE_DIR/src/generic/t5uid1/" "$KLIPPER_DIR_DEFAULT/src/generic/t5uid1/"
  fi

  # apply board-specific printer configs from staging if present and selected earlier
  if [ -n "$SRC_DIR_REL" ]; then
    # staged board configs are under $STAGE_DIR/printer_data or similar
    if [ -d "$STAGE_DIR/printer_data/" ]; then
      rsync -av --progress "$STAGE_DIR/printer_data/" "$HOME/printer_data/" || true
    else
      echo "No staged printer_data found in $STAGE_DIR/printer_data/; skipping printer_data copy."
    fi
  fi

  # copy git_ignore helper from staging if present
  if [ -d "$STAGE_DIR/scripts/dgus-reloaded" ]; then
    mkdir -p "$KLIPPER_DIR_DEFAULT/scripts/dgus-reloaded"
    rsync -av --progress "$STAGE_DIR/scripts/dgus-reloaded/" "$KLIPPER_DIR_DEFAULT/scripts/dgus-reloaded/"
    chmod +x "$KLIPPER_DIR_DEFAULT/scripts/dgus-reloaded"/*.sh || true
    echo "Installed staged scripts to $KLIPPER_DIR_DEFAULT/scripts/dgus-reloaded/"
  fi

  # idempotent patches
  if [ -f "$KLIPPER_DIR_DEFAULT/src/stm32/Kconfig" ]; then
    patch_kconfig_idempotent "$KLIPPER_DIR_DEFAULT/src/stm32/Kconfig"
  fi
  if [ -f "$KLIPPER_DIR_DEFAULT/src/stm32/Makefile" ]; then
    patch_makefile_idempotent "$KLIPPER_DIR_DEFAULT/src/stm32/Makefile"
  fi

  if prompt_yesno "Start klipper service now?"; then
    sudo systemctl start klipper || true
  else
    echo "Remember to start klipper when ready."
  fi

  echo "Applied staged files from $STAGE_DIR."
fi

# Cleanup
if prompt_yesno "Remove cloned install tree at $TMP_DIR?"; then
  rm -rf "$TMP_DIR"
  echo "Cleaned up."
else
  echo "Left install files in $TMP_DIR for inspection."
fi

echo "Done. Verify installed files with:"
echo "  ls -la $KLIPPER_DIR_DEFAULT/klippy/extras/t5uid1"
echo "  grep -n 't5uid1' $KLIPPER_DIR_DEFAULT/src/stm32/Kconfig || true"

#!/usr/bin/env bash
set -euo pipefail

# verify_installation.sh
# Automated verification script for install_dgus_minimal.sh test plan.
# Usage: run from Installation_Files/scripts or pass full path to installer.
# By default this script runs safe, non-destructive checks (dry-run + staging).
# To allow apply-mode tests (which modify ~/klipper), pass --allow-apply.

ALLOW_APPLY=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --allow-apply) ALLOW_APPLY=1; shift;;
    --branch) BRANCH="$2"; shift 2;;
    --help) echo "Usage: $0 [--allow-apply] [--branch <branch>]"; exit 0;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

BRANCH="${BRANCH:-Implement_scripted_download_install}"
INSTALLER="$(cd "$(dirname "$0")" && pwd)/install_dgus_minimal.sh"

echo "Running verification script against branch=$BRANCH"
echo "Installer: $INSTALLER"

fail() { echo "FAIL: $1"; exit 2; }
pass() { echo "PASS: $1"; }

echo "\n== Test 1: dry-run with --keep-temp =="
DGUS_BRANCH="$BRANCH" bash "$INSTALLER" --dry-run --keep-temp || true
if [ -f /tmp/dgus_install/dryrun_report.txt ]; then
  head -n 6 /tmp/dgus_install/dryrun_report.txt || true
  grep -q '^Timestamp:' /tmp/dgus_install/dryrun_report.txt || fail "missing Timestamp in dryrun_report.txt"
  grep -q '^Branch:' /tmp/dgus_install/dryrun_report.txt || fail "missing Branch in dryrun_report.txt"
  grep -q '\[DRY-RUN\] SOURCE:' /tmp/dgus_install/dryrun_report.txt || echo "WARN: no SOURCE lines found"
  pass "dry-run with --keep-temp produced /tmp/dgus_install/dryrun_report.txt"
else
  fail "/tmp/dgus_install/dryrun_report.txt not found"
fi

echo "\n== Test 2: dry-run without --keep-temp (auto-cleanup prompt) =="
# Answer 'y' to clean-up prompt at end so temp tree is removed
printf 'y\n' | DGUS_BRANCH="$BRANCH" bash "$INSTALLER" --dry-run || true
if [ -d /tmp/dgus_install ]; then
  echo "/tmp/dgus_install still exists (you answered no at prompt?)"
else
  pass "dry-run without --keep-temp cleaned /tmp/dgus_install"
fi

echo "\n== Test 3: staging (interactive choice 2) =="
# Use board 3 (BTT SKR CR6) example and keep temp for inspection
printf '3\n2\n' | DGUS_BRANCH="$BRANCH" bash "$INSTALLER" --keep-temp || true
if [ -d "$HOME/t5uid1_staging/klippy_extras_Extensions/klippy/extras/t5uid1" ]; then
  ls -la "$HOME/t5uid1_staging/klippy_extras_Extensions/klippy/extras/t5uid1" | sed -n '1,5p'
  pass "staging copied extras into ~/t5uid1_staging"
else
  fail "staging did not create expected extras folder"
fi

if [ "$ALLOW_APPLY" -eq 1 ]; then
  echo "\n== Test 4: apply-from-staging (choice 4) [DEStructive] =="
  printf '4\nn\nn\n' | DGUS_BRANCH="$BRANCH" bash "$INSTALLER" --keep-temp || true
  # basic checks for live files
  if [ -f "$HOME/klipper/klippy/extras/t5uid1/t5uid1.py" ]; then
    pass "apply-from-staging copied extras into live klipper"
  else
    fail "apply-from-staging did not copy extras to live klipper"
  fi
else
  echo "Skipping apply-from-staging (pass --allow-apply to enable)"
fi

echo "\n== Test 5: --clean interactive removal =="
# Answer y to each prompt to remove
printf 'y\ny\ny\n' | bash "$INSTALLER" --clean || true
if [ -d /tmp/dgus_install ] || ls -d /tmp/dgus_install.* 2>/dev/null | grep -q .; then
  echo "WARN: some temp trees remain"
else
  pass "--clean removed temp trees"
fi

echo "\nVerification script complete. Review PASS/WARN/FAIL lines above."
echo "Note: destructive apply-mode tests are only run when invoked with --allow-apply."

#!/usr/bin/env bash
set -euo pipefail

# Run this on the Klipper host from anywhere. It checks shell syntax for all
# scripts placed in ~/printer_data/config/scripts.

DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Running syntax checks for scripts in: $DIR"

failed=0
for f in "$DIR"/*.sh; do
  [ -f "$f" ] || continue
  echo "Checking: $f"
  if ! bash -n "$f"; then
    echo "Syntax error detected in: $f"
    failed=1
  fi
done

if [ "$failed" -eq 0 ]; then
  echo "All syntax checks passed"
  exit 0
else
  echo "One or more syntax checks failed"
  exit 2
fi

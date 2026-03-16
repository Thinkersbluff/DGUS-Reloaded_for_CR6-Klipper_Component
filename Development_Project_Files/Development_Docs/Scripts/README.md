# Development Scripts

This folder contains PowerShell scripts used to enforce release quality checks and path/script reference integrity.

## Scripts

### `Invoke-PreReleaseGate.ps1`
Primary pre-release gate runner. It verifies:

- required documentation files exist
- release notes exist and include the target version
- compatibility mapping includes the target version
- no Git merge-conflict markers are present
- working tree is clean (local mode)
- claims verification passes via `Validate-ClaimsFile.ps1`

### `Validate-ClaimsFile.ps1`
Validates a claims verification file:

- no unchecked checklist items (`- [ ]`)
- no empty `Evidence:` entries

### `Run_Script_Integrity_Checks.ps1`
Targeted migration checker/fixer for known stale references (old script names and old path patterns).

- writes findings to:  
  `Development_Project_Files/Development_Docs/Verification/Script_Integrity_Findings_<date>_<time>.txt`
- supports dry-run (default) and `-Apply` mode
- supports `-FailOnFindings` for CI/policy use

## Prerequisites

- PowerShell 7+ (`pwsh`)
- Git available in `PATH`
- Run commands from repository root (or pass paths explicitly)

## Usage

### Run pre-release gate (local)
```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File ".\Development_Project_Files\Development_Docs\Scripts\Invoke-PreReleaseGate.ps1" `
  -Version "2.0.0" `
  -ClaimsFile ".\Development_Project_Files\Development_Docs\Verification\Claims_v2.0.0.md"
```

### Run pre-release gate (CI mode)
```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File ".\Development_Project_Files\Development_Docs\Scripts\Invoke-PreReleaseGate.ps1" `
  -Version "2.0.0" `
  -ClaimsFile ".\Development_Project_Files\Development_Docs\Verification\Claims_v2.0.0.md" `
  -CI
```

### Run script integrity checks (dry-run)
```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File ".\Development_Project_Files\Development_Docs\Scripts\Run_Script_Integrity_Checks.ps1"
```

### Run script integrity checks and apply fixes
```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File ".\Development_Project_Files\Development_Docs\Scripts\Run_Script_Integrity_Checks.ps1" -Apply
```

### Fail if findings exist
```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File ".\Development_Project_Files\Development_Docs\Scripts\Run_Script_Integrity_Checks.ps1" -FailOnFindings
```

## Rule lifecycle for `Run_Script_Integrity_Checks.ps1`

This is a **targeted migration utility**, not a general typo/path validator.

Add a new rule only when all are true:

1. stale pattern is recurring or high risk
2. replacement is deterministic
3. regex/pattern can be made precise (low false positives)
4. dry-run output is reviewed before any `-Apply`

Recommended process:

1. add rule
2. run dry-run
3. inspect findings log
4. run with `-Apply` on a branch
5. review `git diff`
6. commit and document rule intent

## Path safety policy

- Do not commit absolute local paths (example: `B:\...`).
- Use repository-relative paths in docs and scripts.
- Scripts should resolve repo root dynamically, not assume current directory.
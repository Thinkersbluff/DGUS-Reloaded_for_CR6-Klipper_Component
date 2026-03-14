# Quick Primer (Return to Project)

## 5-minute restart
1. Confirm branch:
   - `git status -sb`
2. Sync refs:
   - `git fetch origin --prune`
3. Confirm clean tree:
   - `git status`
4. Read current release context:
   - `Development_Project_Files/Development_Docs/Checklists/Release_Gate_Checklist.md`
   - latest file in `Development_Project_Files/Development_Docs/Verification/`
5. Run preflight locally before pushing:
   - `pwsh -File Development_Project_Files/Development_Docs/Scripts/Invoke-PreReleaseGate.ps1 -Version <x.y.z> -ClaimsFile Development_Project_Files/Development_Docs/Verification/Claims_v<x.y.z>.md`

## Before pushing
- Run `Invoke-PreReleaseGate.ps1` locally and confirm it passes.
- Fix any failures before pushing to `New-At-1.4.4`.

## After pushing
- Confirm the `Dev Release Gate` GitHub Actions workflow passes (green check).
- Check at: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/actions`
- Do not open a PR until the gate passes.

## If interrupted mid-task
- Do not publish until checklist is fully complete.
- Do not trust memory; trust checklist state.
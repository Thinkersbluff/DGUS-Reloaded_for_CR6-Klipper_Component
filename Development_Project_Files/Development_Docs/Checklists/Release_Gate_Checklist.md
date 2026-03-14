# Release Gate Checklist

## Branch and sync
- [ ] Correct working branch checked out
- [ ] `git fetch origin --prune` completed
- [ ] Working tree clean (`git status`)

## Scope and versioning
- [ ] Release version defined
- [ ] Version incremented correctly per Version Numbering SOP
- [ ] Compatibility table updated (`Development_Project_Files/Development_Docs/Compatibility_and_Version_Mapping.md`)
- [ ] Release notes file created/updated for this version
- [ ] Release notes state required paired DWIN component version
- [ ] Installation docs updated and sequence-consistent with release notes

## Bug-fix claim verification (mandatory)
- [ ] Claims file created from template (`Development_Project_Files/Development_Docs/Templates/Claims_Verification_Template.md`)
- [ ] Every claimed fix has validation steps documented
- [ ] Every claimed fix has evidence recorded
- [ ] No unchecked items remain in claims file

## Pre-release automation
- [ ] Local script passed: `Invoke-PreReleaseGate.ps1`
- [ ] Local script passed: `Validate-ClaimsFile.ps1`

## PR gate
- [ ] `Dev Release Gate` GitHub Actions workflow passed (green check)
- [ ] Check at: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/actions`
- [ ] No unresolved review comments
- [ ] Final sanity check of all changed files confirms scope is correct
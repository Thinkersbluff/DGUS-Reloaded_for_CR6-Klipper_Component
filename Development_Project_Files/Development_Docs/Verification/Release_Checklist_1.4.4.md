# Release Checklist

## Scope and Branch
- [x] Correct branch checked out
- [x] Branch synced with origin
- [x] Scope matches milestone/release goal

## Versioning
- [x] Version updated in all required files
- [x] Date stamps updated
- [x] Compatibility map updated

## Testing
- [x] Core functional tests passed
- [x] Regression tests passed
- [x] Installation-path validation passed
  - Pass only if all are true:
    - [x] Install or upgrade was performed by following `Installation_Files/README.md` exactly
    - [x] Validation was performed on a real target system or representative test environment
    - [x] No undocumented manual fixes, extra commands, or guessed steps were required
    - [x] Required files were placed in the documented locations
    - [x] Required configuration edits matched the documentation
    - [x] All required services started or restarted successfully
    - [x] Display/UI and Klipper component communicated correctly after install
    - [x] Basic smoke test passed after install

## Documentation
- [x] Installation docs updated for this release
- [x] Release notes updated
- [x] Cross-links and filenames verified

## Git/PR Hygiene
- [x] `git status` clean
- [x] No unresolved conflicts
- [x] PR base/compare correct
  - base: `DGUS-ReloadedForCR6`
  - compare: `New-At-1.4.4`

## Release
- [x] Tag created
- [x] Assets uploaded/verified
- [ ] Post-release smoke check complete
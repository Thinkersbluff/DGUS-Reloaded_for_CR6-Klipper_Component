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
- [ ] Installation-path validation passed
  - Pass only if all are true:
    - [ ] Install or upgrade was performed by following `Installation_Files/README.md` exactly
    - [ ] Validation was performed on a real target system or representative test environment
    - [ ] No undocumented manual fixes, extra commands, or guessed steps were required
    - [ ] Required files were placed in the documented locations
    - [ ] Required configuration edits matched the documentation
    - [ ] All required services started or restarted successfully
    - [ ] Display/UI and Klipper component communicated correctly after install
    - [ ] Basic smoke test passed after install

## Documentation
- [x] Installation docs updated for this release
- [x] Release notes updated
- [x] Cross-links and filenames verified

## Git/PR Hygiene
- [x] `git status` clean
- [ ] No unresolved conflicts
- [ ] PR base/compare correct

## Release
- [ ] Tag created
- [ ] Assets uploaded/verified
- [ ] Post-release smoke check complete
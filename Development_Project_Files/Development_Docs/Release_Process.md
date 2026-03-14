# Release Process (Standard)

## 1) Prepare Branch
- Create/update release branch.
- Merge/rebase from upstream baseline as defined in Development_Manual.
- Confirm clean working tree.

## 2) Implement and Freeze
- Complete feature/fix scope.
- Update all version references.
- Freeze new feature changes.

## 3) Validate
- Run defined test matrix.
- Confirm compatibility mapping (back-end vs DWIN_SET).
- Resolve all blockers.

## 4) Documentation Pass
- Update Installation files.
- Update release notes.
- Run Docs Consistency Checklist.

## 5) Finalize
- Commit in logical chunks.
- Open PR with checklist evidence.
- Tag and publish release assets.
- Post-release verification.
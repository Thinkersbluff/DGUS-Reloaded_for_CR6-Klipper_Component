# Development Manual

## Purpose
Standardize development and release behavior for consistency and memory safety after project breaks.

## Non-negotiable rules
1. No release without completed release gate checklist.
2. No bug-fix claim without explicit verification evidence.
3. No merge with unresolved conflicts or dirty tree.
4. Installation docs and release notes must stay sequence-consistent.

## Standard release flow
1. Sync branch from upstream target.
2. Implement changes.
3. Validate bug-fix claims.
4. Update docs (Installation + Release Notes).
5. Run PowerShell pre-release checks.
6. Open PR and pass GitHub gate workflow.
7. Merge only after all gate items pass.

## Required evidence
For each claimed fix:
- reproducible pre-fix behavior summary,
- post-fix validation steps,
- observed result,
- artifact references (logs/screenshots/commit hash).

## Fast return workflow
Use `SOPs/00-Quick_Primer.md` every time returning to the project.
# SOP: Release Process

1. Branch prep
   - sync from origin target branch,
   - resolve conflicts,
   - confirm clean state.

2. Change implementation
   - perform scoped changes only,
   - update versioned files and notes.

3. Bug-fix claim verification
   - create `Development_Project_Files/Development_Docs/Verification/Claims_v<version>.md` from template,
   - verify every release-note claim with evidence.

4. Documentation alignment
   - Installation sequence and release notes must agree,
   - update dates/versions/links.

5. GitHub Actions gate
   - The `Dev Release Gate` workflow runs automatically on push and PR to `New-At-2.0.0`.
   - It runs `Invoke-PreReleaseGate.ps1 -CI` in the GitHub runner.
   - If it fails, the PR is blocked until the failure is resolved.
   - Check run results at: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/actions`
   - Do not merge a PR with a failed gate run.

6. Gate execution
   - complete `Checklists/Release_Gate_Checklist.md`,
   - run PowerShell checks locally.

7. PR and merge
   - open PR,
   - GitHub Actions must pass,
   - merge only after all gate checks pass.
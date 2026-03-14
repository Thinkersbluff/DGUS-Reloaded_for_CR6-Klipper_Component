# Development Workflow SOP: Researching and Recording Fix Commit Evidence for Claims Verification

## Purpose
This SOP defines how to research and record the correct `Fix commit(s)` evidence for each claim in a Claims Verification file.

This process is required because:
- some fixes may span both the Klipper and DWIN repositories
- issue tracking and code changes may exist in different repositories
- commit messages may not always clearly identify the related claim or issue

## Scope
Use this SOP when completing:

- `Development_Project_Files/Development_Docs/Verification/Claims_v<version>.md`

Use it for every release claim that requires evidence of implementation.

---

## Evidence Standard

For each claim, record the best available implementation evidence in this priority order:

1. **Exact fix commit URL**
2. **Pull request URL** that contains the fix
3. **Issue URL** that directly references the fix
4. **Compare URL** covering the smallest reasonable commit range

### Minimum expectation
Each claim should contain:

- an **Issue** link, if an issue exists
- a **Fix commit(s)** entry pointing to the most direct code evidence available

Do not invent or guess a commit.

---

## Required Research Method

Complete each claim one at a time.

### Step 1: Start from the claim text
For the selected claim, identify:

- claim number
- exact release-note wording
- referenced issue number, if present
- whether the claim affected:
  - back-end
  - front-end
  - both

### Step 2: Determine the likely repository
Use the claim description to decide where the fix most likely occurred.

#### Usually Klipper component repo
Typical examples:
- `t5uid1.py`
- config `.cfg` changes
- macro or script logic
- `mcu.py`
- printer-side behavior
- `printer_data` changes

#### Usually DWIN component repo
Typical examples:
- screen layout changes
- button property changes
- font or color changes
- screen-only behavior changes
- UI config edits

#### Possibly both repositories
Typical examples:
- a new UI control that also required back-end support
- timing/behavior changes requiring UI and script updates
- screen variable/address coordination

---

## Commit Research Procedure

### Method A: Search commit messages by issue number
Run in the repository most likely to contain the fix.

#### PowerShell commands
    git log --all --oneline --decorate --grep '#84'
    git log --all --oneline --decorate --grep 'Issue 84'
    git log --all --oneline --decorate --grep '84'

If results appear relevant, inspect the full commit:

    git show <sha>

If the commit is correct, record the full GitHub commit URL in `Fix commit(s)`.

---

### Method B: Search by likely changed files
If commit messages are weak or inconsistent, search file history.

#### Klipper repo examples
    git log --oneline -- Development_Project_Files/Development_Environment/klippy/extras/t5uid1.py
    git log --oneline -- Development_Project_Files/Development_Environment/klippy/extras/mcu.py
    git log --oneline -- Development_Project_Files/Development_Environment/klippy/extras/*.cfg

#### Generic file-history review
    git log --follow --oneline -- <path-to-file>
    git show <sha>

Use this method when the issue number is not present in commit messages.

---

### Method C: Limit search by date range
If the release work happened within a known time period, narrow the search window.

    git log --since="2026-01-01" --until="2026-03-12" --oneline -- Development_Project_Files/Development_Environment/klippy/extras/t5uid1.py

This is useful when multiple unrelated changes touched the same file.

---

### Method D: Use the issue timeline
When the issue is in the DWIN repository but the fix may be in the Klipper repository, inspect the issue page for:

- linked commits
- linked pull requests
- closing comments
- references to branch names
- references to commit SHAs

Record the most direct linked code evidence.

---

### Method E: Use GitHub Blame
If the final code location of the fix is known, use GitHub **Blame** to locate the commit that last changed the relevant line.

Use this when:
- the exact file and line are known
- the claim is tied to a small and specific code change
- commit messages are unclear

---

## What to Record in `Fix commit(s)`

### Single-commit fix
    - Fix commit(s): https://github.com/<owner>/<repo>/commit/<sha>

### Multi-commit fix in one repo
    - Fix commit(s):
      - https://github.com/<owner>/<repo>/commit/<sha1>
      - https://github.com/<owner>/<repo>/commit/<sha2>

### Multi-repo fix
    - Fix commit(s):
      - https://github.com/<owner>/<klipper-repo>/commit/<sha1>
      - https://github.com/<owner>/<dwin-repo>/commit/<sha2>

### PR used as best available evidence
    - Fix commit(s): https://github.com/<owner>/<repo>/pull/<id>

### Compare URL used as temporary fallback
    - Fix commit(s): https://github.com/<owner>/<repo>/compare/<oldsha>...<newsha>

Use a compare URL only if the exact fix commit cannot yet be isolated with confidence.

---

## Documentation Rules

### Rule 1: Prefer exact evidence
Prefer a direct commit URL whenever possible.

### Rule 2: Do not guess
If unsure, use:
- the issue URL
- the PR URL
- a compare URL

Do not enter an uncertain commit SHA.

### Rule 3: Cross-repo references must be explicit
If the issue is in one repository and the fix is in another, include full URLs.

Do not rely on short references such as:
- `Issue #84`
- `fixed in latest commit`

### Rule 4: Keep the evidence traceable
A future reviewer should be able to open the links and confirm:
- what changed
- where it changed
- why it changed

---

## Claim Completion Workflow

For each claim:

1. Read the exact claim text.
2. Identify the likely affected component:
   - Klipper
   - DWIN
   - both
3. Search by issue number.
4. Search by file history if needed.
5. Inspect candidate commits with `git show`.
6. Record the best evidence link in `Fix commit(s)`.
7. Record the issue link in `Issue:`.
8. Repeat for the next claim.

---

## Recommended Commands

### Search recent history
    git log --since="2025-01-01" --oneline --decorate

### Search by issue number
    git log --all --oneline --decorate --grep '#84'

### Search one file's history
    git log --follow --oneline -- <path-to-file>

### Inspect a commit
    git show --stat <sha>
    git show <sha>

### Show files changed in a commit range
    git diff --name-only <oldsha>..<newsha>

---

## Practical Fallback Rule
If the exact fix commit cannot be confidently identified:

1. record the issue URL
2. record the PR URL, if available
3. record a compare URL covering the smallest valid range
4. leave a note for later refinement if needed

This is acceptable and better than entering a guessed commit.

---

## Process Improvement Requirement
For future work, commit messages should include the issue number whenever possible.

### Preferred example
    fix: resolve auto unload toggle handling (#84)

This allows future searches such as:

    git log --grep '#84'

and greatly reduces evidence-research time during release verification.

---

## Exit Criteria
A claim's evidence research is complete when:

- the issue link is present, if applicable
- the fix commit(s) entry contains the most direct reliable implementation evidence available
- the recorded links are sufficient for an independent reviewer to trace the change history
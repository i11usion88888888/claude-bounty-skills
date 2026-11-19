---
name: check-criteria
description: Compare an issue's acceptance criteria against the work completed and report what is still missing.
when_to_use: Use after implementing changes for an issue, before opening a pull request, to confirm every acceptance criterion is satisfied.
allowed-tools: Bash(python scripts/check_criteria.py *)
---

# check-criteria

Verify that every acceptance criterion from `issue.json` is covered.

## Steps

1. Decide which criteria are genuinely finished. Only count a criterion once
   you have verified it (code written AND tested or otherwise confirmed).

2. Run the checker, passing one `--done` per finished criterion. Use the text
   exactly as it appears in `issue.json` (matching is case-insensitive):

   ```bash
   python scripts/check_criteria.py issue.json --done "Fixed bug" --done "Added tests"
   ```

3. Read the checklist on stdout:
   - Exit code 0: every criterion is done, so continue to the pull request.
   - Exit code 1: at least one criterion is missing. Finish it, or explain to
     the user why it cannot be done. Do not open the PR as if it were complete.
   - Exit code 2: the input file could not be read.

4. If the script warns that a `--done` value matched no criterion, fix the
   spelling and run it again.

## Notes

- Never pass `--done` for work that has not been verified.
- Criteria already marked done in `issue.json` count as done automatically.

---
name: generate-pr
description: Generate a Markdown pull request description from a parsed issue (summary, changes, acceptance criteria, how to test).
when_to_use: Use when the implementation is finished and the user needs a pull request title and description for the issue being solved.
allowed-tools: Bash(python scripts/generate_pr.py *)
---

# generate-pr

Produce a ready-to-use pull request description for the issue in `issue.json`.

## Steps

1. Generate the draft (`--branch` is the base branch the PR targets):

   ```bash
   python scripts/generate_pr.py issue.json --branch main
   ```

2. The first line (`# ...`) is the PR title. Use it as the title, not as part
   of the body.

3. Complete the draft before handing it over:
   - Replace the `TODO` under **Changes** with a real summary of what changed and why.
   - Tick the Acceptance Criteria boxes that were verified; leave the others unticked.
   - Replace the `TODO` under **How to test** with exact commands or steps.

4. Keep `Closes #N`. Keep the `/claim #N` line only for Algora bounties;
   remove it for ordinary issues.

## Notes

- Never claim a criterion is done unless it was verified.
- Optionally write the draft to a file with `-o pr.md`.

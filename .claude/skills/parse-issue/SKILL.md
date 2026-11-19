---
name: parse-issue
description: Parse a GitHub issue URL into structured JSON with its acceptance-criteria checkboxes.
when_to_use: Use when the user shares a GitHub issue or Algora bounty link and wants to know what has to be done before starting work.
allowed-tools: Bash(python scripts/parse_issue.py *)
---

# parse-issue

Turn a GitHub issue into structured data so the work can be planned and tracked.

## Steps

1. Run the script with the issue URL and save the result:

   ```bash
   python scripts/parse_issue.py <issue-url> -o issue.json
   ```

2. Read `issue.json` and summarize for the user:
   - the issue title and repository
   - every acceptance criterion (`criteria[].text`), noting which are already `done`

3. If `criteria` is empty, tell the user the issue has no `- [ ]` checkboxes and
   ask them to state the acceptance criteria manually.

## Output format

```json
{
  "owner": "...", "repo": "...", "number": 123,
  "title": "...", "url": "...",
  "criteria": [{ "text": "...", "done": false }]
}
```

## Notes

- Works for public repositories without a token (60 requests per hour).
  If the script reports a rate limit, ask the user to set `GITHUB_TOKEN`.
- Only `- [ ]` and `- [x]` checkboxes are recognized.
- Exit code 2 means a usage or network error; the message is printed to stderr.

# claude-bounty-skills

Claude Code skills that make it faster to pick up paid bounties on
[Algora](https://algora.io) and GitHub. They turn an issue into a checklist,
track which criteria are done, and produce a ready-to-paste PR description.

## Skills

| Skill | What it does |
|-------|--------------|
| `parse-issue` | Fetches a GitHub issue and extracts its `- [ ]` acceptance criteria as JSON |
| `check-criteria` | Compares the criteria with what you completed; exits with code 1 if anything is missing |
| `generate-pr` | Builds a Markdown PR description: summary, changes, criteria, how to test |

## Install

```bash
git clone https://github.com/<your-user>/claude-bounty-skills.git
cd claude-bounty-skills
pip install -r requirements.txt
```

Requires Python 3.10+.

## Usage

```bash
# 1. Parse the issue into issue.json
python scripts/parse_issue.py https://github.com/owner/repo/issues/123 -o issue.json

# 2. After implementing, check which criteria are still open
python scripts/check_criteria.py issue.json --done "Fixed bug" --done "Added tests"

# 3. Generate the PR description
python scripts/generate_pr.py issue.json --branch main
```

`issue.json` has this shape:

```json
{
  "owner": "owner",
  "repo": "repo",
  "number": 123,
  "title": "Issue title",
  "url": "https://github.com/owner/repo/issues/123",
  "criteria": [{ "text": "Fixed bug", "done": false }]
}
```

### With Claude Code

Open Claude Code in this folder. The skills in `.claude/skills/` are picked up
automatically, so you can ask Claude to "parse this issue" or call
`/parse-issue <url>`, `/check-criteria`, `/generate-pr` directly.

### Rate limits

Without a token GitHub allows 60 API requests per hour. Set `GITHUB_TOKEN` to
raise the limit (and to read private repositories your token can access):

```bash
export GITHUB_TOKEN=ghp_xxx          # bash
$env:GITHUB_TOKEN = "ghp_xxx"        # PowerShell
```

## Limitations

- Only checkboxes written as `- [ ]` / `- [x]` are parsed.
- GitHub only (no GitLab or Bitbucket).
- Network errors are reported, but requests are not retried.
- The SKILL.md files target Claude Code, not other agents.
- MVP: no unit tests and no CI yet.

## License

MIT

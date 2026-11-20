# Claude Bounty Skills

A set of [Claude Code](https://code.claude.com/docs/en/skills) skills and Python CLI tools for hunters who take paid bounties on [Algora](https://algora.io) and GitHub.

Instead of re-reading the same issue and re-typing the same PR template every time, let Claude handle the boring parts.

## Features

- **`parse-issue`** — fetches a GitHub issue and extracts its `- [ ]` acceptance criteria as JSON.
- **`check-criteria`** — compares the criteria with what you completed; exits with code 1 if anything is missing.
- **`generate-pr`** — builds a Markdown PR description: summary, changes, criteria, how to test.

## Prerequisites

- Python 3.10+
- Git
- Optional: [Claude Code](https://code.claude.com) for the skills integration

## Installation

Clone the repository:

```bash
git clone https://github.com/i11usion88888888/claude-bounty-skills.git
cd claude-bounty-skills
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Option 1: With Claude Code (recommended)

Open Claude Code in this folder. The skills in `.claude/skills/` are picked up automatically.

You can simply ask Claude:

- "Parse this issue: https://github.com/owner/repo/issues/123"
- "Check if I missed any acceptance criteria"
- "Generate a PR description for this branch"

Or call the skills directly: `/parse-issue`, `/check-criteria`, `/generate-pr`.

### Option 2: Manual CLI

If you prefer to run the Python scripts directly:

**1. Parse an issue**

```bash
python scripts/parse_issue.py https://github.com/owner/repo/issues/123 -o issue.json
```

**2. Check your progress** (after making changes)

```bash
python scripts/check_criteria.py issue.json --done "Fixed bug" --done "Added tests"
```

> **Note:** matching is case-insensitive. If any criterion is still open, the script exits with code 1.

**3. Generate the PR description**

```bash
python scripts/generate_pr.py issue.json --branch main
```

Copy the output and paste it into your pull request on GitHub.

## Rate limits

Without a token, GitHub allows 60 API requests per hour. If you hit the limit, set a `GITHUB_TOKEN` environment variable:

```bash
export GITHUB_TOKEN=ghp_xxx          # bash
```

```powershell
$env:GITHUB_TOKEN = "ghp_xxx"        # PowerShell
```

## Limitations

- Only checkboxes written as `- [ ]` / `- [x]` are parsed.
- GitHub only (no GitLab or Bitbucket support yet).
- MVP: no unit tests or CI pipelines.

## License

MIT

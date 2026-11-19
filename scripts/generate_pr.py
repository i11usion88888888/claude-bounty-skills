#!/usr/bin/env python3
"""Generate a Markdown pull request description from a parsed issue."""

import argparse
import json
import sys


def load_issue(path):
    """Read issue JSON; tolerates UTF-8 BOM and UTF-16 (PowerShell '>' redirects)."""
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = raw.decode("utf-16")
    else:
        text = raw.decode("utf-8-sig")
    return json.loads(text)


def build_description(issue, branch):
    number = issue["number"]
    lines = [
        f"# {issue['title']}",
        "",
        "## Summary",
        "",
        f"Closes #{number}",
        "",
        f"/claim #{number}",
        "",
        f"Issue: {issue['url']}",
        "",
        "## Changes",
        "",
        "- TODO: describe what changed and why",
        "",
        "## Acceptance Criteria",
        "",
    ]

    criteria = issue.get("criteria", [])
    if criteria:
        for c in criteria:
            lines.append(f"- [{'x' if c.get('done') else ' '}] {c['text']}")
    else:
        lines.append("_No checkbox criteria were found in the issue._")

    lines += [
        "",
        "## How to test",
        "",
        f"1. Check out this branch (based on `{branch}`):",
        "",
        "   ```bash",
        f"   git clone https://github.com/{issue['owner']}/{issue['repo']}.git",
        f"   cd {issue['repo']}",
        "   git checkout <this-branch>",
        "   ```",
        "",
        "2. Run the project's test suite.",
        "3. Walk through each acceptance criterion above and confirm it holds.",
        "4. TODO: add exact commands or manual steps for this change",
    ]
    return "\n".join(lines) + "\n"


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Generate a PR description from issue.json.")
    parser.add_argument("issue", help="path to issue.json produced by parse_issue.py")
    parser.add_argument("--branch", default="main", help="base branch the PR targets (default: main)")
    parser.add_argument("-o", "--output", help="write the description to this file instead of stdout")
    args = parser.parse_args(argv)

    try:
        issue = load_issue(args.issue)
        text = build_description(issue, args.branch)
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: cannot read {args.issue}: {exc}", file=sys.stderr)
        return 2

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"Saved {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

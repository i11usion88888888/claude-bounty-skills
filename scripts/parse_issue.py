#!/usr/bin/env python3
"""Fetch a GitHub issue and extract its checkbox acceptance criteria as JSON."""

import argparse
import json
import os
import re
import sys

import requests

API_URL = "https://api.github.com/repos/{owner}/{repo}/issues/{number}"
ISSUE_URL_RE = re.compile(
    r"^https?://(?:www\.)?github\.com/(?P<owner>[^/\s]+)/(?P<repo>[^/\s]+)/issues/(?P<number>\d+)"
)
CHECKBOX_RE = re.compile(r"^[ \t]*- \[([ xX])\] (.+?)[ \t]*$", re.MULTILINE)
TIMEOUT = 15


def parse_url(url):
    match = ISSUE_URL_RE.match(url.strip())
    if not match:
        raise ValueError(f"Not a GitHub issue URL: {url}")
    return match["owner"], match["repo"], int(match["number"])


def extract_criteria(body):
    text = (body or "").replace("\r\n", "\n")
    return [
        {"text": m.group(2), "done": m.group(1).lower() == "x"}
        for m in CHECKBOX_RE.finditer(text)
    ]


def fetch_issue(owner, repo, number, token=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "claude-bounty-skills",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = API_URL.format(owner=owner, repo=repo, number=number)
    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise RuntimeError(f"Network error: {exc}") from exc

    if resp.status_code == 404:
        raise RuntimeError("Issue not found (for private repos set GITHUB_TOKEN).")
    if resp.status_code in (403, 429) and resp.headers.get("X-RateLimit-Remaining") == "0":
        raise RuntimeError("GitHub rate limit exceeded. Set GITHUB_TOKEN to raise the limit.")
    if not resp.ok:
        raise RuntimeError(f"GitHub API error {resp.status_code}: {resp.text[:200]}")
    return resp.json()


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Parse a GitHub issue into JSON.")
    parser.add_argument("url", help="e.g. https://github.com/owner/repo/issues/123")
    parser.add_argument("-o", "--output", help="write JSON to this file instead of stdout")
    args = parser.parse_args(argv)

    try:
        owner, repo, number = parse_url(args.url)
        data = fetch_issue(owner, repo, number, os.environ.get("GITHUB_TOKEN"))
        if "pull_request" in data:
            raise RuntimeError("This URL is a pull request, not an issue.")
    except (ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    result = {
        "owner": owner,
        "repo": repo,
        "number": number,
        "title": data.get("title", ""),
        "url": data.get("html_url", args.url),
        "criteria": extract_criteria(data.get("body")),
    }
    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output + "\n")
        print(f"Saved {args.output} ({len(result['criteria'])} criteria)", file=sys.stderr)
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())

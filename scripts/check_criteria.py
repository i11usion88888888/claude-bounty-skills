#!/usr/bin/env python3
"""Compare an issue's acceptance criteria with the work that was completed."""

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


def normalize(text):
    return " ".join(text.split()).casefold()


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Check acceptance criteria against completed work.")
    parser.add_argument("issue", help="path to issue.json produced by parse_issue.py")
    parser.add_argument(
        "--done",
        action="append",
        default=[],
        metavar="TEXT",
        help="text of a completed criterion (case-insensitive, repeatable)",
    )
    args = parser.parse_args(argv)

    try:
        issue = load_issue(args.issue)
        criteria = issue["criteria"]
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: cannot read {args.issue}: {exc}", file=sys.stderr)
        return 2

    if not criteria:
        print("No acceptance criteria found in the issue.")
        return 0

    done_set = {normalize(t) for t in args.done}
    known = {normalize(c["text"]) for c in criteria}

    missing = 0
    for c in criteria:
        is_done = bool(c.get("done")) or normalize(c["text"]) in done_set
        print(f"- [{'x' if is_done else ' '}] {c['text']}")
        if not is_done:
            missing += 1

    total = len(criteria)
    print(f"\n{total - missing}/{total} criteria done")

    for t in args.done:
        if normalize(t) not in known:
            print(f"warning: --done matched no criterion: {t!r}", file=sys.stderr)

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

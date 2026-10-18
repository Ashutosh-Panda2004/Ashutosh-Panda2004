"""Keep the merged-PR count in the README highlights subline current.

Runs inside the Update profile art workflow, whose commits are authored by
github-actions[bot], so the daily count refresh never counts as the owner's
own contribution. Only the number in the subline inside the
<!-- oss-highlights:start/end --> markers is touched; the heading wording
and the top-7 table rows are curated separately and never rewritten here.
"""
import os
import re
import sys

import requests

USERNAME = "Ashutosh-Panda2004"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.environ.get("PROFILE_README", os.path.join(ROOT, "README.md"))
START = "<!-- oss-highlights:start -->"
END = "<!-- oss-highlights:end -->"


def merged_total():
    token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = requests.get(
        "https://api.github.com/search/issues",
        params={"q": f"author:{USERNAME} type:pr is:merged"},
        headers=headers, timeout=30)
    payload = resp.json()
    if "total_count" not in payload:
        raise RuntimeError(f"merged PR search failed: {str(payload)[:200]}")
    return payload["total_count"]


def main():
    with open(README, encoding="utf-8") as f:
        text = f.read()
    if START not in text or END not in text:
        print("highlights markers not found; leaving README unchanged")
        return
    head, rest = text.split(START, 1)
    block, tail = rest.split(END, 1)
    total = merged_total()
    new_block, n = re.subn(r"\d+ merged pull requests",
                           f"{total} merged pull requests", block, count=1)
    if n == 0:
        print("no count line inside highlights block; leaving README unchanged")
        return
    if new_block == block:
        print(f"highlights count already {total}; no change")
        return
    with open(README, "w", encoding="utf-8") as f:
        f.write(head + START + new_block + END + tail)
    print(f"highlights count updated to {total}")


if __name__ == "__main__":
    sys.exit(main())

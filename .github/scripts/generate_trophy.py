#!/usr/bin/env python3
"""Generate a self-hosted GitHub trophy card SVG.

Usage: generate_trophy.py <username> <output_path> [theme]

Uses a single GitHub GraphQL query (needs GITHUB_TOKEN env) and the
standard library only, so the profile README never depends on an
external image service again.
"""

import json
import os
import sys
import urllib.request
from datetime import date

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, first: 100,
                 orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      nodes { stargazers { totalCount } }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
    }
  }
}
"""

THEMES = {
    "tokyonight": {
        "bg": "#0d1117", "card": "#161b22", "border": "#30363d",
        "title": "#00f5ff", "number": "#f0f6fc", "label": "#8b949e",
        "footer": "#6e7681",
    },
    "default": {
        "bg": "#ffffff", "card": "#f6f8fa", "border": "#d0d7de",
        "title": "#0969da", "number": "#1f2328", "label": "#59636e",
        "footer": "#818b98",
    },
}


def fmt(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".rstrip("0").rstrip(".")
    if n >= 1_000:
        return f"{n / 1_000:.1f}k".rstrip("0").rstrip(".")
    return str(n)


def fetch_stats(username, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": username}}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-trophy-generator",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise RuntimeError(payload["errors"][0].get("message", "GraphQL error"))
    u = payload["data"]["user"]
    cc = u["contributionsCollection"]
    stars = sum(r["stargazers"]["totalCount"] for r in u["repositories"]["nodes"])
    return [
        ("Commit", "Commits", cc["totalCommitContributions"]),
        ("GitPullRequest", "Pull Requests", cc["totalPullRequestContributions"]),
        ("IssueOpened", "Issues", cc["totalIssueContributions"]),
        ("Eye", "Code Reviews", cc["totalPullRequestReviewContributions"]),
        ("Star", "Stars Earned", stars),
        ("People", "Followers", u["followers"]["totalCount"]),
    ]


ICONS = {
    "Commit": "&#x1F4BB;",
    "GitPullRequest": "&#x1F500;",
    "IssueOpened": "&#x1F41B;",
    "Eye": "&#x1F440;",
    "Star": "&#x2B50;",
    "People": "&#x1F465;",
}


def render(username, stats, theme):
    t = THEMES.get(theme, THEMES["tokyonight"])
    W, pad, gap, cols = 810, 20, 12, 3
    cell_w = (W - pad * 2 - gap * (cols - 1)) // cols
    cell_h = 80
    top = 64
    rows = (len(stats) + cols - 1) // cols
    H = top + rows * cell_h + (rows - 1) * gap + 44

    cells = []
    for i, (icon, label, value) in enumerate(stats):
        r, c = divmod(i, cols)
        x = pad + c * (cell_w + gap)
        y = top + r * (cell_h + gap)
        cells.append(f"""
      <g>
        <rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="8"
              fill="{t['card']}" stroke="{t['border']}" stroke-width="1"/>
        <text x="{x + 16}" y="{y + 34}" font-size="22">{ICONS[icon]}</text>
        <text x="{x + 52}" y="{y + 36}" font-size="24" font-weight="700"
              fill="{t['number']}" font-family="Segoe UI,Helvetica,Arial,sans-serif">{fmt(value)}</text>
        <text x="{x + 16}" y="{y + 60}" font-size="12"
              fill="{t['label']}" font-family="Segoe UI,Helvetica,Arial,sans-serif">{label}</text>
      </g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10"
        fill="{t['bg']}" stroke="{t['border']}" stroke-width="1.5"/>
  <text x="{pad}" y="38" font-size="19" font-weight="700"
        fill="{t['title']}" font-family="Segoe UI,Helvetica,Arial,sans-serif">&#x1F3C6; GitHub Trophies</text>
  {''.join(cells)}
  <text x="{pad}" y="{H - 16}" font-size="11"
        fill="{t['footer']}" font-family="Segoe UI,Helvetica,Arial,sans-serif">@{username} &#183; contributions in the last 12 months &#183; refreshed {date.today().isoformat()}</text>
</svg>
"""


def main():
    if len(sys.argv) < 3:
        print("usage: generate_trophy.py <username> <output_path> [theme]",
              file=sys.stderr)
        return 1
    username, output_path = sys.argv[1], sys.argv[2]
    theme = sys.argv[3] if len(sys.argv) > 3 else "tokyonight"
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN env var is required", file=sys.stderr)
        return 1
    try:
        stats = fetch_stats(username, token)
    except Exception as e:  # noqa: BLE001 - fail loudly so CI shows it
        print(f"failed to fetch GitHub stats: {e}", file=sys.stderr)
        return 1
    svg = render(username, stats, theme)
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

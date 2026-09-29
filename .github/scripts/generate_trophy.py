#!/usr/bin/env python3
"""Generate a GitHub-style trophy showcase SVG using only the standard library.

Uses the *unauthenticated* GitHub REST API (public data, 60 req/hour is plenty
for a twice-daily cron). No token needed: the GITHUB_TOKEN available in Actions
is an integration token that cannot query user-profile data via GraphQL
("Resource not accessible by integration"), so we avoid auth entirely.

Usage: generate_trophy.py <username> <output_path> [theme]
"""

import json
import os
import sys
import traceback
import urllib.request

THEMES = {
    "tokyonight": {
        "bg": "#1a1b27",
        "border": "#414868",
        "title": "#7aa2f7",
        "text": "#a9b1d6",
        "accent": "#bb9af7",
    },
}

ICONS = {
    "Star": "M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z",
    "People": "M16 11c1.7 0 3 1.3 3 3v4h-5v-4c0-.6-.4-1-1-1h-2c-.6 0-1 .4-1 1v4H5v-4c0-1.7 1.3-3 3-3h8zM8 3a3 3 0 110 6 3 3 0 010-6zm8 0a3 3 0 110 6 3 3 0 010-6z",
    "Repo": "M4 3h6l2 2h6v14H4V3zm3 4v2h4V7H7zm0 4v2h6v-2H7z",
    "Fork": "M6 3a3 3 0 013 3c0 1.2-.7 2.2-1.7 2.7V10h5.4V8.7C11.7 8.2 11 7.2 11 6a3 3 0 016 0c0 1.2-.7 2.2-1.7 2.7V10h1.7a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6a1 1 0 011-1h1.7V8.7C4.7 8.2 4 7.2 4 6a3 3 0 012-2.8V3h0z",
}


def rest(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={"User-Agent": "profile-trophy-generator",
                 "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def fetch_stats(username):
    user = rest(f"/users/{username}")
    repos = rest(f"/users/{username}/repos?per_page=100&type=owner")
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    forks = sum(r.get("forks_count", 0) for r in repos)
    return [
        ("Star", "Stars Earned", stars),
        ("Fork", "Total Forks", forks),
        ("People", "Followers", user.get("followers", 0)),
        ("Repo", "Repositories", user.get("public_repos", 0)),
    ]


def render(username, stats, theme):
    t = THEMES.get(theme, THEMES["tokyonight"])
    cards = []
    x = 16
    for icon, label, value in stats:
        cards.append(
            f'<g transform="translate({x},64)">'
            f'<rect width="148" height="96" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>'  # noqa: E501
            f'<path d="{ICONS[icon]}" fill="{t["accent"]}" transform="translate(14,12) scale(1.1)"/>'  # noqa: E501
            f'<text x="14" y="62" font-family="sans-serif" font-size="26" font-weight="bold" fill="{t["title"]}">{value}</text>'  # noqa: E501
            f'<text x="14" y="82" font-family="sans-serif" font-size="12" fill="{t["text"]}">{label}</text>'  # noqa: E501
            "</g>"
        )
        x += 160
    width = x - 12
    body = "".join(cards)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="176" viewBox="0 0 {width} 176">'  # noqa: E501
        f'<rect width="{width}" height="176" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>'  # noqa: E501
        f'<text x="16" y="34" font-family="sans-serif" font-size="18" font-weight="bold" fill="{t["title"]}">{username}&#39;s Trophy Case</text>'  # noqa: E501
        f"{body}</svg>"
    )


def main():
    if len(sys.argv) < 3:
        print("usage: generate_trophy.py <username> <output_path> [theme]",
              file=sys.stderr)
        return 1
    username, output_path = sys.argv[1], sys.argv[2]
    theme = sys.argv[3] if len(sys.argv) > 3 else "tokyonight"
    try:
        stats = fetch_stats(username)
    except Exception:  # noqa: BLE001 - fail loudly so CI shows it
        traceback.print_exc()
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

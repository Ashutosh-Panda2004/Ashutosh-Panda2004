"""Fetch live GitHub data into data/*.json (profile, PR counts, contributions).

Uses GITHUB_TOKEN when present (CI) to avoid the anonymous rate limit.
The contributions calendar is read from the public contributions page.
"""
import json
import os
import re
import urllib.parse
from collections import Counter, defaultdict
from datetime import date

import requests
from bs4 import BeautifulSoup

USERNAME = "Ashutosh-Panda2004"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.github.com"


def save(name, obj):
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    with open(os.path.join(ROOT, "data", name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def fetch_profile(s):
    user = s.get(f"{API}/users/{USERNAME}", timeout=30).json()
    repos = s.get(f"{API}/users/{USERNAME}/repos",
                  params={"per_page": 100, "type": "owner"}, timeout=30).json()
    langs = Counter()
    for r in repos:
        if r["fork"]:
            continue
        resp = s.get(r["languages_url"], timeout=30)
        if resp.ok:
            langs.update(resp.json())
    save("profile.json", {
        "name": user.get("name"),
        "username": USERNAME,
        "created_at": user.get("created_at"),
        "public_repos": user.get("public_repos", len(repos)),
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "stars": sum(r["stargazers_count"] for r in repos),
        "languages": dict(langs.most_common()),
    })
    print("profile.json saved")


def fetch_counts(s):
    def total(q):
        return s.get(f"{API}/search/issues",
                     params={"q": q}, timeout=30).json()["total_count"]
    save("github.json", {
        "prs_opened": total(f"author:{USERNAME} type:pr"),
        "prs_merged": total(f"author:{USERNAME} type:pr is:merged"),
        "prs_open": total(f"author:{USERNAME} type:pr is:open"),
        "issues_opened": total(f"author:{USERNAME} type:issue"),
        "prs_reviewed": total(f"reviewed-by:{USERNAME} type:pr"),
    })
    print("github.json saved")


def fetch_contributions():
    html = requests.get(f"https://github.com/users/{USERNAME}/contributions",
                        headers={"User-Agent": "profile-art"}, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    tips = {}
    for tip in soup.find_all("tool-tip"):
        m = re.match(r"\s*(\d[\d,]*) contributions?", tip.get_text())
        tips[tip.get("for")] = int(m.group(1).replace(",", "")) if m else 0
    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        days.append({
            "date": cell["data-date"],
            "level": int(cell.get("data-level", 0)),
            "count": tips.get(cell.get("id"), 0),
        })
    if not days:
        raise SystemExit("No contribution cells found; GitHub markup may have changed.")
    days.sort(key=lambda d: d["date"])
    counts = [d["count"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    for c in reversed(tail):
        if not c:
            break
        current += 1
    best = max(days, key=lambda d: d["count"])
    monthly = defaultdict(int)
    weekday = Counter()
    for d in days:
        monthly[d["date"][:7]] += d["count"]
        weekday[date.fromisoformat(d["date"]).strftime("%A")] += d["count"]
    save("contributions.json", {
        "username": USERNAME,
        "days": days,
        "stats": {
            "total": sum(counts),
            "current_streak": current,
            "longest_streak": longest,
            "best_day": {"date": best["date"], "count": best["count"]},
            "active_days": sum(1 for c in counts if c),
            "busiest_weekday": weekday.most_common(1)[0][0] if sum(counts) else "-",
            "monthly": dict(monthly),
            "range": [days[0]["date"], days[-1]["date"]],
        },
    })
    print("contributions.json saved")


def fetch_activity(s):
    """Category counts + top merged-PR repos for the GitHub activity card."""
    path = os.path.join(ROOT, "data", "activity.json")
    act = {}
    if os.path.exists(path):
        with open(path) as f:
            act = json.load(f)
    def total(q):
        return s.get(f"{API}/search/issues", params={"q": q},
                     timeout=30).json()["total_count"]
    repos = []
    for repo, label in [("checkstyle/checkstyle", "checkstyle"),
                        ("apache/fineract", "Fineract"),
                        ("servo/rust-smallvec", "rust-smallvec"),
                        ("sagar2395/snowopslabs", "snowopslabs"),
                        ("oras-project/oras", "oras"),
                        ("chrissnell/graywolf", "graywolf")]:
        n = total(f"author:{USERNAME} type:pr is:merged repo:{repo}")
        if n:
            repos.append([label, n])
    repos.sort(key=lambda r: -r[1])
    if repos:
        act["repos"] = repos[:6]
    try:
        from datetime import timedelta
        end = date.today()
        start = end - timedelta(days=365)
        query = {"query": "query($u:String!,$from:DateTime!,$to:DateTime!)"
                 "{user(login:$u){contributionsCollection(from:$from,to:$to)"
                 "{totalCommitContributions totalPullRequestContributions "
                 "totalIssueContributions totalPullRequestReviewContributions}}}",
                 "variables": {"u": USERNAME,
                               "from": f"{start.isoformat()}T00:00:00Z",
                               "to": f"{end.isoformat()}T23:59:59Z"}}
        cc = s.post("https://api.github.com/graphql", json=query,
                    timeout=30).json()["data"]["user"]["contributionsCollection"]
        act.update({"commits": cc["totalCommitContributions"],
                    "pull_requests": cc["totalPullRequestContributions"],
                    "issues": cc["totalIssueContributions"],
                    "reviews": cc["totalPullRequestReviewContributions"]})
    except Exception as e:
        print("activity graphql skipped:", e)
    save("activity.json", act)
    print("activity:", act)


def main():
    s = requests.Session()
    s.headers["Accept"] = "application/vnd.github+json"
    if os.environ.get("GITHUB_TOKEN"):
        s.headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    fetch_profile(s)
    fetch_counts(s)
    fetch_contributions()
    fetch_activity(s)


if __name__ == "__main__":
    main()

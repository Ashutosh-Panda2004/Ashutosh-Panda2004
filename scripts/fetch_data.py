"""Fetch live GitHub data into data/*.json (profile, PR counts, contributions).

Data sources, all GitHub's own APIs so the cards match the profile exactly:
- Contributions calendar and category totals: GraphQL contributionsCollection,
  the same data behind the profile contribution graph. Needs a token:
  PROFILE_TOKEN (a PAT, includes private contributions when the account shows
  them) or GITHUB_TOKEN. If the GraphQL fetch fails, the previous
  contributions.json is kept only while it is less than 48 hours old;
  after that this script fails loudly instead of rendering stale numbers.
- Profile, languages, PR/issue counts: REST + search APIs.
"""
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone

import requests

USERNAME = "Ashutosh-Panda2004"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.github.com"
GRAPHQL = "https://api.github.com/graphql"

CC_QUERY = """query($u: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $u) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""


def save(name, obj):
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    with open(os.path.join(ROOT, "data", name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def load_existing(name):
    path = os.path.join(ROOT, "data", name)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def fetch_contributions_collection(s):
    """One GraphQL call: calendar + category totals for the last 365 days."""
    end = date.today()
    start = end - timedelta(days=364)
    resp = s.post(GRAPHQL, json={
        "query": CC_QUERY,
        "variables": {"u": USERNAME,
                      "from": f"{start.isoformat()}T00:00:00Z",
                      "to": f"{end.isoformat()}T23:59:59Z"},
    }, timeout=30)
    payload = resp.json()
    if resp.status_code != 200 or "errors" in payload or not payload.get("data"):
        raise RuntimeError(f"GraphQL contributions fetch failed: "
                           f"{str(payload)[:300]}")
    return payload["data"]["user"]["contributionsCollection"]


def compute_levels(days):
    """GitHub-style intensity levels 0-4 from the year's nonzero counts."""
    nonzero = sorted(d["count"] for d in days if d["count"] > 0)
    if not nonzero:
        return
    def pct(p):
        return nonzero[min(len(nonzero) - 1, int(p * len(nonzero)))]
    q1, q2, q3 = pct(0.25), pct(0.50), pct(0.75)
    for d in days:
        c = d["count"]
        d["level"] = (0 if c == 0 else
                      1 if c <= q1 else
                      2 if c <= q2 else
                      3 if c <= q3 else 4)


def compute_stats(days):
    counts = [d["count"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    tail = list(counts)
    while tail and tail[-1] == 0:
        tail.pop()
    current = 0
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
    return {
        "total": sum(counts),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "active_days": sum(1 for c in counts if c),
        "busiest_weekday": weekday.most_common(1)[0][0] if sum(counts) else "-",
        "monthly": dict(monthly),
        "range": [days[0]["date"], days[-1]["date"]],
    }


def fetch_contributions(s, cc):
    cal = cc["contributionCalendar"]
    days = []
    seen = set()
    for week in cal["weeks"]:
        for day in week["contributionDays"]:
            if day["date"] in seen:
                continue
            seen.add(day["date"])
            days.append({"date": day["date"], "count": day["contributionCount"]})
    days.sort(key=lambda d: d["date"])
    if not days:
        raise RuntimeError("GraphQL returned an empty contribution calendar")
    compute_levels(days)
    stats = compute_stats(days)
    if stats["total"] != cal["totalContributions"]:
        print(f"warning: day sum {stats['total']} != calendar total "
              f"{cal['totalContributions']}", file=sys.stderr)
    save("contributions.json", {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "days": days,
        "stats": stats,
    })
    print("contributions.json saved:", stats)


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


def search_total(s, q):
    import time
    last = None
    for attempt in range(3):
        payload = s.get(f"{API}/search/issues",
                        params={"q": q}, timeout=30).json()
        if "total_count" in payload:
            return payload["total_count"]
        last = payload
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"search failed for {q!r}: {str(last)[:200]}")


def fetch_counts(s):
    def total(q):
        return search_total(s, q)
    save("github.json", {
        "prs_opened": total(f"author:{USERNAME} type:pr"),
        "prs_merged": total(f"author:{USERNAME} type:pr is:merged"),
        "prs_open": total(f"author:{USERNAME} type:pr is:open"),
        "issues_opened": total(f"author:{USERNAME} type:issue"),
        "prs_reviewed": total(f"reviewed-by:{USERNAME} type:pr"),
    })
    print("github.json saved")


def fetch_activity(s, cc):
    """Category totals come from the same GraphQL call as the calendar, so
    the donut always agrees with the heatmap. Repo chips are merged-PR
    counts per repo from search."""
    def total(q):
        return search_total(s, q)
    repos = []
    for repo, label in [("checkstyle/checkstyle", "checkstyle"),
                        ("apache/fineract", "Fineract"),
                        ("smallvec/smallvec", "rust-smallvec"),
                        ("snowops-oss/snowopslabs", "snowopslabs"),
                        ("oras-project/oras", "oras"),
                        ("chrissnell/graywolf", "graywolf")]:
        try:
            n = total(f"author:{USERNAME} type:pr is:merged repo:{repo}")
        except Exception as e:
            print(f"warning: repo chip skipped for {repo}: {e}")
            continue
        if n:
            repos.append([label, n])
    repos.sort(key=lambda r: -r[1])
    act = {
        "commits": cc["totalCommitContributions"],
        "pull_requests": cc["totalPullRequestContributions"],
        "issues": cc["totalIssueContributions"],
        "reviews": cc["totalPullRequestReviewContributions"],
    }
    if repos:
        act["repos"] = repos[:6]
    save("activity.json", act)
    print("activity.json saved:", act)


def main():
    s = requests.Session()
    s.headers["Accept"] = "application/vnd.github+json"
    token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    try:
        cc = fetch_contributions_collection(s)
    except Exception as e:
        existing = load_existing("contributions.json") or {}
        fetched_at = existing.get("fetched_at")
        fresh = False
        if fetched_at:
            age = datetime.now(timezone.utc) - datetime.fromisoformat(fetched_at)
            fresh = age < timedelta(hours=48)
        if fresh:
            print(f"WARNING: contributions fetch failed ({e}); keeping "
                  f"contributions.json from {fetched_at} (under 48h old)")
            cc = None
        else:
            raise SystemExit(
                f"Contributions fetch failed and saved data is stale or "
                f"missing: {e}. Set the PROFILE_TOKEN repo secret (a GitHub "
                f"PAT) so the workflow can read the contribution calendar.")
    fetch_profile(s)
    fetch_counts(s)
    if cc is not None:
        fetch_contributions(s, cc)
        fetch_activity(s, cc)
    else:
        print("activity.json left as-is (depends on the same GraphQL call)")


if __name__ == "__main__":
    main()

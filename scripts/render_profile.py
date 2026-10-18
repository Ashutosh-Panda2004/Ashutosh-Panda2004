"""Render Ashutosh Panda's profile SVGs from data/*.json.

Original renderer written for this profile. Run: python3 scripts/render_profile.py
The portrait step reads work/source-prepped.png (made by prep_portrait.py).
"""
import json
import math
import os
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

FONT = ("ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, "
        "'Liberation Mono', monospace")
BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
FG = "#c9d1d9"
MUTED = "#8b949e"
GREEN = "#39d353"
CYAN = "#58d5e8"
PURPLE = "#bc8cff"
ORANGE = "#ffa657"
PINK = "#ff7b9c"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]


def esc(s):
    return escape(str(s), quote=True)


def load(name, default=None):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_svg(name, svg):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {name} ({len(svg) // 1024} KB)")


def window(width, height, title, body, extra_defs="", finish=True):
    """Terminal window chrome shared by every card."""
    chrome_defs, overlay = "", ""
    if finish:
        chrome_defs = f"""
<radialGradient id="vig" cx="0.5" cy="0.42" r="0.78"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.20"/></radialGradient>
<linearGradient id="accentBar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#39d353"/><stop offset="0.5" stop-color="#58d5e8"/><stop offset="1" stop-color="#bc8cff"/></linearGradient>
<linearGradient id="cardSheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.05"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="cardClip"><rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10"/></clipPath>"""
        overlay = f"""
<g clip-path="url(#cardClip)"><rect x="0" y="32" width="{width}" height="2" fill="url(#accentBar)" opacity="0.55"/><rect x="0" y="0" width="{width}" height="70" fill="url(#cardSheen)"/><rect x="0" y="0" width="{width}" height="{height}" fill="url(#vig)"/></g>
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="9" fill="none" stroke="#ffffff" stroke-opacity="0.05"/>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">
<defs>{extra_defs}{chrome_defs}</defs>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>
<path d="M0.5 32 V10.5 a10 10 0 0 1 10 -10 H{width - 10.5} a10 10 0 0 1 10 10 V32 Z" fill="{PANEL}"/>
<line x1="0.5" y1="32" x2="{width - 0.5}" y2="32" stroke="{BORDER}"/>
<circle cx="18" cy="16" r="5.5" fill="#ff5f56"/><circle cx="36" cy="16" r="5.5" fill="#ffbd2e"/><circle cx="54" cy="16" r="5.5" fill="#27c93f"/>
<text x="{width / 2}" y="20.5" fill="{MUTED}" font-size="12" text-anchor="middle">{esc(title)}</text>
{body}{overlay}
</svg>
"""


# ---------------------------------------------------------------- header
NAME = "Ashutosh Panda"
PROMPT_USER = "ashutosh"
PROMPT_HOST = "github"
ROLES = [
    "SDE-1 @ Honeywell",
    "Open Source Contributor",
    "Building TokenLens and ShutdownCheck",
    "Backend Systems and AI Engineering",
]
TAGLINE = "SDE-1 at Honeywell · Bengaluru, IN"


def header_svg():
    W, H = 860, 210
    char_w = 9.6
    slot, total_t = 5.0, 5.0 * len(ROLES)
    roles = []
    for k, role in enumerate(ROLES):
        w = len(role) * char_w
        t0 = k * slot
        typed, held, gone = t0 + len(role) * 0.055, t0 + slot - 1.1, t0 + slot - 0.35
        stops = sorted({0.0, t0 / total_t, typed / total_t, held / total_t,
                        gone / total_t, 1.0})
        keys = ";".join(f"{v:.4f}" for v in stops)
        width_at = {0.0: 0, t0 / total_t: 0, typed / total_t: w,
                    held / total_t: w, gone / total_t: 0, 1.0: 0}
        widths = ";".join(f"{width_at[v]:.1f}" for v in stops)
        xs = ";".join(f"{60 + width_at[v]:.1f}" for v in stops)
        roles.append(f"""<clipPath id="r{k}"><rect x="60" y="132" width="0" height="22">
<animate attributeName="width" values="{widths}" keyTimes="{keys}" dur="{total_t}s" repeatCount="indefinite"/></rect></clipPath>
<text x="60" y="148" font-size="16" fill="{FG}" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#r{k})">{esc(role)}</text>
<rect x="60" y="134" width="9" height="18" fill="{GREEN}" opacity="0">
<animate attributeName="x" values="{xs}" keyTimes="{keys}" dur="{total_t}s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{t0 / total_t:.4f};{gone / total_t:.4f};{min(gone / total_t + 0.0001, 0.9999):.4f};1" dur="{total_t}s" repeatCount="indefinite" calcMode="discrete"/>
</rect>""")
    prompt = f"{PROMPT_USER}@{PROMPT_HOST}:~$"
    cmd = "./hello.sh"
    cmd_x = 40 + len(prompt) * 8.4 + 8
    defs = f"""
<linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{GREEN}"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="8s" repeatCount="indefinite"/>
</linearGradient>
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#ffffff" opacity="0.05"/></pattern>
<radialGradient id="auroraG" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{GREEN}" stop-opacity="0.13"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>
<radialGradient id="auroraP" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{PURPLE}" stop-opacity="0.10"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0.08"/></linearGradient>
<linearGradient id="nameSheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0.42" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.38"/><stop offset="0.58" stop-color="#ffffff" stop-opacity="0"/><animateTransform attributeName="gradientTransform" type="translate" values="-1.2 0;1.2 0" dur="5.5s" repeatCount="indefinite"/></linearGradient>
<clipPath id="inner"><rect x="1" y="33" width="{W - 2}" height="{H - 34}" rx="9"/></clipPath>
<clipPath id="cmdClip"><rect x="{cmd_x}" y="40" width="0" height="20"><animate attributeName="width" from="0" to="{len(cmd) * 8.4 + 2}" begin="0.3s" dur="0.6s" fill="freeze"/></rect></clipPath>
<style>.fade {{ opacity: 0; animation: in .7s ease-out forwards; }} @keyframes in {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}</style>"""
    body = f"""
<g clip-path="url(#inner)">
  <rect x="0" y="32" width="{W}" height="{H}" fill="url(#dots)"/>
  <ellipse cx="180" cy="122" rx="300" ry="92" fill="url(#auroraG)"><animate attributeName="cx" values="180;265;180" dur="11s" repeatCount="indefinite"/></ellipse>
  <ellipse cx="645" cy="98" rx="260" ry="82" fill="url(#auroraP)"><animate attributeName="cx" values="645;560;645" dur="13s" repeatCount="indefinite"/></ellipse>
  <rect x="0" y="-40" width="{W}" height="40" fill="url(#scan)"><animate attributeName="y" values="-10;{H}" dur="5s" repeatCount="indefinite"/></rect>
</g>
<text x="40" y="55" font-size="14"><tspan fill="{GREEN}">{esc(prompt)}</tspan></text>
<text x="{cmd_x}" y="55" font-size="14" fill="{FG}" textLength="{len(cmd) * 8.4:.1f}" clip-path="url(#cmdClip)">{esc(cmd)}</text>
<g class="fade" style="animation-delay:1s">
  <text x="40" y="112" font-size="46" font-weight="800" letter-spacing="2" fill="url(#nameGrad)" filter="url(#glow)">{esc(NAME.upper())}</text>
  <text x="40" y="112" font-size="46" font-weight="800" letter-spacing="2" fill="url(#nameSheen)">{esc(NAME.upper())}</text>
</g>
<g class="fade" style="animation-delay:1.7s"><rect x="40" y="126" width="0" height="2" fill="url(#nameGrad)" opacity="0.85"><animate attributeName="width" from="0" to="400" begin="1.8s" dur="0.9s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect></g>
<g class="fade" style="animation-delay:1.4s"><text x="40" y="148" font-size="16" fill="{MUTED}">&gt;</text></g>
<g class="fade" style="animation-delay:1.6s">{''.join(roles)}</g>
<g class="fade" style="animation-delay:1.9s"><text x="40" y="182" font-size="13" fill="{MUTED}">{esc(TAGLINE)}</text></g>
"""
    write_svg("header.svg", window(W, H, f"~/{PROMPT_USER}: zsh", body, defs))




# ---------------------------------------------------------------- portrait
def portrait_svg():
    src = os.path.join(ROOT, "work", "source-prepped.png")
    if not os.path.exists(src):
        raise FileNotFoundError(src)
    import numpy as np
    from PIL import Image
    W, H = 370, 420
    ramp = " .`:-=+*cs#%@"
    cols, font, lh = 92, 6.2, 7.0
    cw = font * 0.6
    img = Image.open(src).convert("L")
    w, h = img.size
    img = img.crop((int(0.04 * w), 0, int(0.96 * w), int(0.88 * h)))
    rows = int(cols * cw / lh * img.height / img.width)
    max_rows = int((H - 52) / lh)
    if rows > max_rows:
        keep = int(img.height * max_rows / rows)
        img, rows = img.crop((0, 0, img.width, keep)), max_rows
    a = np.asarray(img.resize((cols, rows), Image.LANCZOS), dtype=np.float32) / 255
    nz = a[a > 0.04]
    lo, hi = np.percentile(nz, [5, 99]) if nz.size else (0, 1)
    a = np.where(a > 0.04, np.clip((a - lo) / (hi - lo), 0, 1) ** 0.8, 0)
    grid_w = cols * cw
    x0 = (W - grid_w) / 2
    y0 = 32 + (H - 32 - rows * lh) / 2 + lh * 0.8
    out = []
    for r in range(rows):
        line = "".join(ramp[int(v * (len(ramp) - 1))] for v in a[r])
        if not line.strip():
            continue
        y = y0 + r * lh
        begin, dur = 0.3 + r * 0.045, 0.55
        text = esc(line).replace(" ", " ")
        out.append(
            f'<clipPath id="c{r}"><rect x="{x0:.1f}" y="{y - lh:.1f}" width="0" height="{lh + 1}">'
            f'<animate attributeName="width" from="0" to="{grid_w:.1f}" begin="{begin:.2f}s" dur="{dur}s" fill="freeze"/></rect></clipPath>'
            f'<text x="{x0:.1f}" y="{y:.1f}" textLength="{grid_w:.1f}" lengthAdjust="spacing" clip-path="url(#c{r})">{text}</text>'
            f'<rect x="{x0:.1f}" y="{y - lh + 1:.1f}" width="{cw:.1f}" height="{lh - 1}" fill="{GREEN}" opacity="0">'
            f'<set attributeName="opacity" to="1" begin="{begin:.2f}s"/>'
            f'<animate attributeName="x" from="{x0:.1f}" to="{x0 + grid_w:.1f}" begin="{begin:.2f}s" dur="{dur}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0" begin="{begin + dur:.2f}s"/></rect>')
    shimmer = 0.3 + rows * 0.045 + 0.6
    defs = f"""
<linearGradient id="ink" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
  <stop offset="0" stop-color="{GREEN}"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="0 0;{W} {H};0 0" begin="{shimmer:.2f}s" dur="10s" repeatCount="indefinite"/>
</linearGradient>"""
    body = f"""
<g fill="url(#ink)" font-size="{font}">{''.join(out)}</g>"""
    write_svg("ascii-portrait.svg", window(W, H, "portrait.txt", body, defs, finish=False))


# ---------------------------------------------------------------- info card
LANG_COLORS = {
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Python": "#3572A5",
    "CSS": "#663399", "HTML": "#e34c26", "Go": "#00ADD8", "Java": "#b07219",
    "Shell": "#89e051", "Dockerfile": "#384d54", "C++": "#f34b7d",
    "C#": "#178600", "Rust": "#dea584", "SCSS": "#c6538c", "Dart": "#00B4AB",
    "C": "#555555", "Kotlin": "#A97BFF", "Swift": "#F05138", "HCL": "#844FBA",
    "Jupyter Notebook": "#DA5B0B", "CMake": "#DA3434",
}
KEY_COLORS = [GREEN, CYAN, PURPLE, ORANGE, PINK]


def _uptime(created_iso):
    from datetime import datetime, timezone
    c = datetime.fromisoformat(created_iso.replace("Z", "+00:00"))
    months = (datetime.now(timezone.utc) - c).days * 12 // 365
    y, m = divmod(months, 12)
    parts = ([f"{y} yr" + ("s" if y != 1 else "")] if y else [])
    if m or not y:
        parts.append(f"{m} mo" + ("s" if m != 1 else ""))
    return ", ".join(parts)


def _info_rows(prof, gh, st, langs):
    return [
        ("Role", "SDE-1 @ Honeywell · Ex-SWE Intern @ Nielsen"),
        ("Now", "Backend work on a migration platform"),
        ("OSS", "checkstyle · Fineract · SW360"),
        ("Uptime", f"{_uptime(prof['created_at'])} on GitHub"
         if prof.get("created_at") else "-"),
        ("Langs", " · ".join(list(langs)[:3]) or "-"),
        ("Backend", "Go · C# · .NET · Node.js"),
        ("Frontend", "React · Vite · Tailwind"),
        ("Projects", "TokenLens · ShutdownCheck"),
        ("PRs", f"{gh.get('prs_merged', '-')} merged · {gh.get('prs_opened', '-')} opened"),
        ("Reviews", f"{gh.get('prs_reviewed', '-')} PRs reviewed · {gh.get('issues_opened', '-')} issues"),
        ("Repos", f"{prof.get('public_repos', '-')} public · {prof.get('stars', '-')} stars"),
        ("Streak", f"{st.get('current_streak', 0)}d current · {st.get('longest_streak', 0)}d best"),
    ]


def info_card_svg():
    W, H = 490, 420
    prof = load("profile.json", {})
    gh = load("github.json", {})
    st = load("contributions.json", {}).get("stats", {})
    langs = prof.get("languages", {})
    rows = _info_rows(prof, gh, st, langs)
    x, y = 24, 60
    head = f"{PROMPT_USER}@{PROMPT_HOST}"
    lines = [
        f'<g class="ln" style="animation-delay:0.50s"><text x="{x}" y="{y}" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> neofetch</text></g>',
        f'<g class="ln" style="animation-delay:0.59s"><text x="{x}" y="{y + 28}" font-size="15" font-weight="700"><tspan fill="{GREEN}">{PROMPT_USER}</tspan><tspan fill="{FG}">@</tspan><tspan fill="{CYAN}">{PROMPT_HOST}</tspan></text>'
        f'<text x="{x}" y="{y + 42}" font-size="13" fill="{MUTED}">{"-" * len(head)}</text></g>',
    ]
    ry = y + 64
    lines.insert(0, '<ellipse cx="120" cy="86" rx="150" ry="52" fill="url(#infoGlow)"/>')
    for hk in range(1, len(rows)):
        lines.append(f'<line x1="{x}" y1="{ry + hk * 20 - 15}" x2="{W - x}" y2="{ry + hk * 20 - 15}" stroke="#ffffff" stroke-opacity="0.045"/>')
    for k, (key, val) in enumerate(rows):
        color = KEY_COLORS[k % len(KEY_COLORS)]
        lines.append(
            f'<g class="ln" style="animation-delay:{0.68 + k * 0.09:.2f}s"><text x="{x}" y="{ry + k * 20}" font-size="13"><tspan fill="{color}" font-weight="700">{esc(key)}</tspan>'
            f'<tspan x="{x + 92}" fill="{FG}">{esc(val)}</tspan></text></g>')
    # language bar over the six biggest languages
    top = list(langs.items())[:6]
    shown_total = sum(langs.values()) or 1
    by = ry + len(rows) * 20 + 4
    bar_w = W - 2 * x
    segs, legend, cx, lx, ly = [], [], x, x, by + 28
    for lang, size in top:
        w = bar_w * size / shown_total
        c = LANG_COLORS.get(lang, MUTED)
        segs.append(f'<rect x="{cx:.1f}" y="{by}" width="{max(w, 1):.1f}" height="8" fill="{c}"/>')
        cx += w
        label = f"{lang} {100 * size / shown_total:.1f}%"
        if lx + len(label) * 6.6 + 18 > W - x:
            lx, ly = x, ly + 17
        legend.append(f'<circle cx="{lx + 4}" cy="{ly - 4}" r="4" fill="{c}"/><text x="{lx + 13}" y="{ly}" font-size="11" fill="{MUTED}">{esc(label)}</text>')
        lx += len(label) * 6.6 + 30
    lines.append(
        f'<clipPath id="barClip"><rect x="{x}" y="{by}" width="0" height="8" rx="4"><animate attributeName="width" from="0" to="{bar_w}" begin="1.6s" dur="1.2s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect></clipPath>'
        f'<rect x="{x}" y="{by}" width="{bar_w}" height="8" rx="4" fill="{BORDER}"/>'
        f'<g clip-path="url(#barClip)" filter="url(#barGlow)">{"".join(segs)}</g>'
        f'<g class="ln" style="animation-delay:1.94s">{"".join(legend)}</g>')
    lines.append(
        f'<clipPath id="infoClip"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10"/></clipPath>'
        f'<g clip-path="url(#infoClip)"><g transform="rotate(18 245 210)"><rect x="-240" y="-60" width="120" height="{H + 120}" fill="url(#infoSheen)">'
        f'<animate attributeName="x" values="-240;640;640" keyTimes="0;0.26;1" dur="9s" repeatCount="indefinite"/></rect></g></g>')
    defs = f"""<style>.ln {{ opacity: 0; animation: ln .5s ease-out forwards; }} @keyframes ln {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; transform: none; }} }}</style>
<linearGradient id="infoSheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="infoGlow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{GREEN}" stop-opacity="0.07"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>
<filter id="barGlow" x="-5%" y="-120%" width="110%" height="340%"><feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="{GREEN}" flood-opacity="0.30"/></filter>"""
    write_svg("info-card.svg", window(W, H, f"{PROMPT_USER}@{PROMPT_HOST}: ~",
                                      "\n".join(lines), defs))




# ---------------------------------------------------------------- globe
HOME = ("Bengaluru", 12.97, 77.59)
REGIONS = [
    ("checkstyle", 50.11, 14.42),
    ("Apache Fineract", 38.90, -77.04),
    ("Eclipse SW360", 48.14, 11.58),
    ("OpenMRS", 39.77, -86.16),
]
GLOBE_R = 132
GLOBE_C = (215, 205)
GLOBE_TILT = math.radians(22)
GLOBE_PERIOD = 36
GLOBE_SAMPLES = 36
ARC_COLORS = [CYAN, PURPLE, ORANGE, PINK, "#79c0ff"]


def _slerp_point(p, q, t):
    def vec(lat, lon):
        la, lo = math.radians(lat), math.radians(lon)
        return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo),
                math.sin(la))
    v1, v2 = vec(*p), vec(*q)
    om = math.acos(max(-1.0, min(1.0, sum(x * y for x, y in zip(v1, v2)))))
    if om < 1e-6:
        return p
    s1 = math.sin((1 - t) * om) / math.sin(om)
    s2 = math.sin(t * om) / math.sin(om)
    v = tuple(s1 * x + s2 * y for x, y in zip(v1, v2))
    return (math.degrees(math.asin(max(-1.0, min(1.0, v[2])))),
            math.degrees(math.atan2(v[1], v[0])))


def globe_svg():
    W, H = 430, 400
    CX, CY, R = GLOBE_C[0], GLOBE_C[1], GLOBE_R
    lp = os.path.join(ROOT, "scripts", "land_points.json")
    land = [tuple(p) for p in json.load(open(lp))] if os.path.exists(lp) else []
    rings = {}
    for lat, lon in land:
        rings.setdefault(lat, []).append(lon)
    keyframes = []

    def ring(lat, lons, color, r, alt=1.0, back=0.0, anim="", samples=None):
        ns = samples or GLOBE_SAMPLES
        phi = math.radians(lat)
        a = alt * R * math.cos(phi)
        b = a * math.sin(GLOBE_TILT)
        ty = CY - alt * R * math.sin(phi) * math.cos(GLOBE_TILT)
        c0 = -math.tan(phi) * math.tan(GLOBE_TILT)
        if alt > 1:
            c0 -= (alt - 1) * 0.6
        k = len(keyframes)
        steps = " ".join(
            f"{100.0 * i / ns:.2f}%{{transform:translate({CX + a * math.sin(2 * math.pi * i / ns):.1f}px,{ty + b * math.cos(2 * math.pi * i / ns):.1f}px)}}"
            for i in range(ns + 1))
        keyframes.append(f"@keyframes k{k}{{{steps}}}.k{k}{{animation:k{k} {GLOBE_PERIOD}s linear infinite}}")
        dots = "".join(
            f'<circle r="{r}" class="k{k}" style="animation-delay:-{((lon - HOME[2]) % 360) / 360 * GLOBE_PERIOD:.2f}s">{anim}</circle>'
            for lon in lons)
        out = []
        if c0 < 1:
            out.append(f'<clipPath id="f{k}"><rect x="0" y="{ty + b * max(c0, -1.5):.2f}" width="{W}" height="{H}"/></clipPath>'
                       f'<g clip-path="url(#f{k})" fill="{color}">{dots}</g>')
        if back and c0 > -1:
            out.append(f'<clipPath id="b{k}"><rect x="0" y="0" width="{W}" height="{ty + b * min(c0, 1.5):.2f}"/></clipPath>'
                       f'<g clip-path="url(#b{k})" fill="{color}" opacity="{back}">{dots}</g>')
        return "".join(out)

    layers = []
    for lat in range(-60, 61, 30):
        phi = math.radians(lat)
        a = R * math.cos(phi)
        ty = CY - R * math.sin(phi) * math.cos(GLOBE_TILT)
        layers.append(f'<ellipse cx="{CX}" cy="{ty:.1f}" rx="{a:.1f}" ry="{a * math.sin(GLOBE_TILT):.1f}" fill="none" stroke="#2d3a4a" stroke-width="0.8"/>')
    for lat in sorted(rings):
        layers.append(ring(lat, rings[lat], GREEN, 1.7, back=0.14, samples=72))
    arcs = []
    home = (HOME[1], HOME[2])
    for n, (_name, la, lo) in enumerate(REGIONS):
        color = ARC_COLORS[n % len(ARC_COLORS)]
        for s in range(1, 16):
            t = s / 16
            plat, plon = _slerp_point(home, (la, lo), t)
            alt = 1 + 0.22 * math.sin(math.pi * t)
            begin = (t * 1.4 + n * 0.5) % 2.8
            pulse = f'<animate attributeName="opacity" values="0.15;1;0.15" dur="2.8s" begin="{begin:.2f}s" repeatCount="indefinite"/>'
            arcs.append(ring(plat, [plon], color, 1.3, alt=alt, anim=pulse))
        arcs.append(ring(la, [lo], color, 2.8))
    pin = (ring(HOME[1], [HOME[2]], ORANGE, 3,
                anim='<animate attributeName="r" values="3;13" dur="1.8s" repeatCount="indefinite"/>'
                     '<animate attributeName="opacity" values="0.8;0" dur="1.8s" repeatCount="indefinite"/>')
           + ring(HOME[1], [HOME[2]], "#fff", 3.2))
    names = " · ".join(r[0] for r in REGIONS[:3]) + \
        (f" +{len(REGIONS) - 3}" if len(REGIONS) > 3 else "")
    def orbit_path(rx, ry, rot_deg):
        rot = math.radians(rot_deg)
        pts = []
        for k in range(49):
            t = 2 * math.pi * k / 48
            ex, ey = rx * math.cos(t), ry * math.sin(t)
            pts.append((CX + ex * math.cos(rot) - ey * math.sin(rot),
                        CY + ex * math.sin(rot) + ey * math.cos(rot)))
        return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z'
    orb = orbit_path(170, 58, -14)
    import random
    rng = random.Random(42)
    stars = []
    while len(stars) < 70:
        sx_, sy_ = rng.uniform(22, 408), rng.uniform(42, 386)
        if (sx_ - CX) ** 2 + (sy_ - CY) ** 2 < 158 ** 2:
            continue
        stars.append(f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="{rng.uniform(0.5, 1.3):.1f}" fill="#d7ecff" class="tw" style="animation-delay:{rng.uniform(0, 4):.1f}s;animation-duration:{rng.uniform(2.4, 4.6):.1f}s"/>')
    defs = f"""
<radialGradient id="ocean" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="#16324a"/><stop offset="0.7" stop-color="#0c1724"/><stop offset="1" stop-color="#070b12"/></radialGradient>
<radialGradient id="shade" cx="0.5" cy="0.5" r="0.5"><stop offset="0.72" stop-color="#05080d" stop-opacity="0"/><stop offset="1" stop-color="#05080d" stop-opacity="0.75"/></radialGradient>
<radialGradient id="atmo" cx="0.5" cy="0.5" r="0.5"><stop offset="0.86" stop-color="{CYAN}" stop-opacity="0"/><stop offset="0.92" stop-color="{CYAN}" stop-opacity="0.22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<style>{''.join(keyframes)}.tw{{opacity:.14;animation:tw 3.4s ease-in-out infinite}}@keyframes tw{{0%,100%{{opacity:.10}}50%{{opacity:.55}}}}.fin{{opacity:0;animation:fin 1s ease-out .3s forwards}}@keyframes fin{{to{{opacity:1}}}}</style>
<radialGradient id="floorGlow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{GREEN}" stop-opacity="0.10"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>"""
    body = f"""
<text x="20" y="56" font-size="12" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ./open-source --from bengaluru</text>
{''.join(stars)}
<ellipse cx="215" cy="352" rx="150" ry="26" fill="url(#floorGlow)"/>
<g class="fin">
<circle cx="{CX}" cy="{CY}" r="{R * 1.16:.0f}" fill="url(#atmo)"/>
<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#ocean)"/>
{''.join(layers)}
<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#shade)"/>
{''.join(arcs)}
{pin}
<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{CYAN}" stroke-opacity="0.25"/>
</g>
<path d="{orb}" fill="none" stroke="#58d5e8" stroke-opacity="0.13" stroke-dasharray="2 5"/>
<g><circle r="6" fill="#58d5e8" opacity="0.18"/><circle r="2.5" fill="#58d5e8"/><animateMotion dur="18s" repeatCount="indefinite" path="{orb}"/></g>
<text x="215" y="378" font-size="10.5" fill="{MUTED}" text-anchor="middle"><tspan fill="{ORANGE}">●</tspan> {esc(HOME[0])} → {esc(names)}</text>
"""
    write_svg("globe.svg", window(W, H, "globe.sh", body, defs))



# ---------------------------------------------------------------- tech sphere
TECH = {
    "languages": ["Go", "TypeScript", "C#", "Python", "Java"],
    "backend": [".NET", "Node.js", "Fastify", "REST APIs"],
    "frontend": ["React", "Vite", "Tailwind CSS", "Framer Motion"],
    "platform": ["Azure", "Docker", "GitHub Actions", "SQLite"],
    "tools": ["Git", "Linux", "GitHub", "SQL"],
}
TECH_COLORS = [CYAN, GREEN, ORANGE, PURPLE, PINK]


def tech_sphere_svg():
    W, H = 430, 400
    CX, CY, R = 215, 212, 128
    TILT = math.radians(18)
    PERIOD, SAMPLES = 30, 60

    def project(v, theta):
        x, y, z = v
        x, z = x * math.cos(theta) + z * math.sin(theta), \
            -x * math.sin(theta) + z * math.cos(theta)
        y, z = y * math.cos(TILT) - z * math.sin(TILT), \
            y * math.sin(TILT) + z * math.cos(TILT)
        return CX + R * x, CY - R * y, z

    labels = [(t, cat) for cat, items in TECH.items() for t in items]
    color = {cat: TECH_COLORS[k % len(TECH_COLORS)]
             for k, cat in enumerate(TECH)}
    n = len(labels)
    golden = math.pi * (3 - math.sqrt(5))
    pts = []
    for i in range(n):
        y = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(max(0.0, 1 - y * y))
        pts.append((r * math.cos(golden * i), y, r * math.sin(golden * i)))
    thetas = [2 * math.pi * k / SAMPLES for k in range(SAMPLES + 1)]
    texts = []
    for (label, cat), v in zip(labels, pts):
        xs, ys, sizes, ops = [], [], [], []
        for th in thetas:
            x, y, z = project(v, th)
            d = (z + 1) / 2
            xs.append(f"{x:.1f}")
            ys.append(f"{y + 4:.1f}")
            sizes.append(f"{8.5 + 8 * d:.1f}")
            ops.append(f"{0.18 + 0.82 * d ** 1.6:.2f}")
        a = f'dur="{PERIOD}s" repeatCount="indefinite"'
        texts.append(
            f'<text text-anchor="middle" fill="{color[cat]}" paint-order="stroke" stroke="#0d1117" stroke-width="1.2" stroke-linejoin="round" font-weight="700" x="{xs[0]}" y="{ys[0]}" font-size="{sizes[0]}" opacity="{ops[0]}">{esc(label)}'
            f'<animate attributeName="x" values="{";".join(xs)}" {a}/>'
            f'<animate attributeName="y" values="{";".join(ys)}" {a}/>'
            f'<animate attributeName="font-size" values="{";".join(sizes)}" {a}/>'
            f'<animate attributeName="opacity" values="{";".join(ops)}" {a}/></text>')
    wire = []
    for lat in (-60, -30, 0, 30, 60):
        p = math.radians(lat)
        rx = R * math.cos(p)
        wire.append(f'<ellipse cx="{CX}" cy="{CY - R * math.sin(p) * math.cos(TILT):.1f}" rx="{rx:.1f}" ry="{rx * math.sin(TILT):.1f}" fill="none" stroke="#2d3a4a"/>')
    for m in range(0, 180, 30):
        rxs = ";".join(f"{abs(R * math.sin(math.radians(m) + th)):.1f}"
                       for th in thetas)
        wire.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{R}" ry="{R}" fill="none" stroke="#2d3a4a">'
                    f'<animate attributeName="rx" values="{rxs}" dur="{PERIOD}s" repeatCount="indefinite"/></ellipse>')
    legend = []
    total_w = sum(len(c) + 4 for c in TECH) * 6.4
    lx = (W - total_w) / 2
    for c in TECH:
        wch = (len(c) + 4) * 6.4 - 8
        legend.append(f'<rect x="{lx:.1f}" y="{H - 40}" width="{wch:.1f}" height="20" rx="10" fill="{PANEL}" stroke="{BORDER}"/>'
                      f'<circle cx="{lx + 11:.1f}" cy="{H - 30}" r="7" fill="{color[c]}" opacity="0.20"/><circle cx="{lx + 11:.1f}" cy="{H - 30}" r="3.5" fill="{color[c]}"/>'
                      f'<text x="{lx + 19:.1f}" y="{H - 26}" font-size="10.5" fill="{MUTED}">{esc(c)}</text>')
        lx += (len(c) + 4) * 6.4
    import random
    rng = random.Random(11)
    stars = []
    while len(stars) < 26:
        sx_, sy_ = rng.uniform(22, 408), rng.uniform(42, 380)
        if (sx_ - CX) ** 2 + (sy_ - CY) ** 2 < 152 ** 2:
            continue
        stars.append(f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="{rng.uniform(0.5, 1.2):.1f}" fill="#d7ecff" class="tw" style="animation-delay:{rng.uniform(0, 4):.1f}s;animation-duration:{rng.uniform(2.6, 5):.1f}s"/>')

    def orbit_path(rx, ry, rot_deg, reverse=False):
        rot = math.radians(rot_deg)
        n = 48
        idxs = range(n, -1, -1) if reverse else range(n + 1)
        pts = []
        for k in idxs:
            t = 2 * math.pi * k / n
            ex, ey = rx * math.cos(t), ry * math.sin(t)
            pts.append((CX + ex * math.cos(rot) - ey * math.sin(rot),
                        CY + ex * math.sin(rot) + ey * math.cos(rot)))
        return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z'

    orb1 = orbit_path(172, 54, -16)
    orb2 = orbit_path(188, 68, 14, reverse=True)
    defs = f"""
<radialGradient id="core" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{PURPLE}" stop-opacity="0.18"/><stop offset="0.6" stop-color="{CYAN}" stop-opacity="0.05"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="shade" cx="0.5" cy="0.5" r="0.5"><stop offset="0.62" stop-color="#04070b" stop-opacity="0"/><stop offset="1" stop-color="#04070b" stop-opacity="0.42"/></radialGradient>
<style>.tw{{opacity:.12;animation:tw 3.8s ease-in-out infinite}}@keyframes tw{{0%,100%{{opacity:.08}}50%{{opacity:.5}}}}.fin{{opacity:0;animation:fin 1s ease-out .3s forwards}}@keyframes fin{{to{{opacity:1}}}}</style>"""
    body = f"""
<text x="20" y="56" font-size="12" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ls ~/stack --3d</text>
{''.join(stars)}
<g class="fin">
<circle cx="{CX}" cy="{CY}" r="{R * 1.25:.0f}" fill="url(#core)"><animate attributeName="r" values="{R * 1.25:.0f};{R * 1.34:.0f};{R * 1.25:.0f}" dur="6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.85;1;0.85" dur="6s" repeatCount="indefinite"/></circle>
{''.join(wire)}
<ellipse cx="215" cy="212" rx="128" ry="39.6" fill="none" stroke="#58d5e8" stroke-opacity="0.10" stroke-width="1.2"/>
<circle cx="215" cy="212" r="128" fill="url(#shade)"/>
<circle cx="215" cy="212" r="128" fill="none" stroke="#58d5e8" stroke-opacity="0.16"/>
{''.join(texts)}
<path d="{orb1}" fill="none" stroke="#58d5e8" stroke-opacity="0.13" stroke-dasharray="2 5"/>
<path d="{orb2}" fill="none" stroke="#ffa657" stroke-opacity="0.10" stroke-dasharray="2 5"/>
<g><circle r="6" fill="#58d5e8" opacity="0.18"/><circle r="2.6" fill="#58d5e8"/><animateMotion dur="16s" repeatCount="indefinite" path="{orb1}"/></g>
<g><circle r="5" fill="#ffa657" opacity="0.16"/><circle r="2.2" fill="#ffa657"/><animateMotion dur="23s" repeatCount="indefinite" path="{orb2}"/></g>
</g>
<line x1="40" y1="348" x2="390" y2="348" stroke="#30363d" stroke-opacity="0.6"/>
{''.join(legend)}
"""
    write_svg("tech-sphere.svg", window(W, H, "stack.sh", body, defs))



# ---------------------------------------------------------------- skyline
def _weeks(days):
    """Group contribution days into Sunday-start weeks."""
    from datetime import date, timedelta
    if not days:
        return []
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    by_date = {d["date"]: d["count"] for d in days}
    weeks, cur = [], start
    last = date.fromisoformat(days[-1]["date"])
    while cur <= last:
        total = sum(by_date.get((cur + timedelta(days=i)).isoformat(), 0)
                    for i in range(7))
        weeks.append((cur, total))
        cur += timedelta(days=7)
    return weeks


def skyline_svg():
    W, H = 860, 470
    IX, IY = 11.2, 4.8
    JX, JY = -11.2, 6.0
    HMAX = 105
    INSET = 0.1
    TOPS = ["#1f2630", "#1a6b3c", "#1f9a4b", "#33c25a", "#5ae27a", "#9dffbe"]
    LEFT = ["#171d25", "#0f4a29", "#137034", "#22903f", "#36ad54", "#6fe597"]
    RIGHT = ["#12171e", "#0a3520", "#0d5226", "#196c30", "#26843f", "#4cc173"]
    from datetime import date, timedelta
    data = load("contributions.json", {})
    days, st = data.get("days", []), data.get("stats", {})
    if not days:
        return
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    cols = (date.fromisoformat(days[-1]["date"]) - start).days // 7 + 1
    peak = max(1, max(d["count"] for d in days))
    ox = (W - (cols + 7) * IX) / 2 + 7 * IX - 10
    oy = 92

    def P(i, j, h=0.0):
        return ox + i * IX + j * JX, oy + i * IY + j * JY - h

    def poly(pts, fill):
        return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}"/>'

    cells = []
    for d in days:
        off = (date.fromisoformat(d["date"]) - start).days
        cells.append((off // 7, off % 7, d))
    cells.sort(key=lambda t: (t[0] + t[1], t[1]))
    out, best_top, lights = [], None, []
    a, b = INSET, 1 - INSET
    for i, j, d in cells:
        lvl = d["level"]
        if d["count"] == peak:
            lvl = 5
        h = 0 if d["count"] == 0 else 3 + math.sqrt(d["count"] / peak) * HMAX
        top = [P(i + a, j + a, h), P(i + b, j + a, h),
               P(i + b, j + b, h), P(i + a, j + b, h)]
        delay = 0.4 + i * 0.035 + j * 0.03
        tip = f"<title>{d['count']} contributions on {d['date']}</title>"
        if h == 0:
            out.append(f'<g class="t" style="animation-delay:{delay:.2f}s">{poly(top, TOPS[0])}{tip}</g>')
            continue
        left = [P(i + a, j + b, h), P(i + b, j + b, h),
                P(i + b, j + b), P(i + a, j + b)]
        right = [P(i + b, j + a, h), P(i + b, j + b, h),
                 P(i + b, j + b), P(i + b, j + a)]
        out.append(f'<g class="b" style="animation-delay:{delay:.2f}s">'
                   f'{poly(left, LEFT[lvl])}{poly(right, RIGHT[lvl])}{poly(top, TOPS[lvl])}{tip}</g>')
        if h > 58:
            tcx = sum(p[0] for p in top) / 4
            tcy = sum(p[1] for p in top) / 4
            lights.append((h, f'<circle cx="{tcx:.1f}" cy="{tcy:.1f}" r="1.1" fill="#d9fbe8" opacity="0.55"/>'))
        if d["count"] == peak and best_top is None:
            best_top = (P(i + 0.5, j + 0.5, h), d)
    months, seen = [], set()
    for i, j, d in cells:
        dt = date.fromisoformat(d["date"])
        if j == 0 and dt.day <= 7 and dt.month not in seen:
            seen.add(dt.month)
            x, y = P(i + 0.2, 7.5)
            ang = math.degrees(math.atan2(IY, IX))
            months.append(f'<text x="{x:.1f}" y="{y + 8:.1f}" font-size="10" fill="{MUTED}" transform="rotate({ang:.1f} {x:.1f} {y + 8:.1f})">{dt.strftime("%b")}</text>')
    beacon = ""
    if best_top:
        (bx, by), bd = best_top
        label = f"{bd['count']} · {date.fromisoformat(bd['date']).strftime('%b %d')}"
        beacon = (
            f'<g class="fin" style="animation-delay:3.2s">'
            f'<rect x="{bx - 1.5:.1f}" y="{by - 46:.1f}" width="3" height="46" fill="url(#beam)"/>'
            f'<circle cx="{bx:.1f}" cy="{by - 48:.1f}" r="4" fill="{ORANGE}"><animate attributeName="r" values="3;6;3" dur="1.6s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{bx:.1f}" cy="{by - 48:.1f}" r="4" fill="none" stroke="{ORANGE}"><animate attributeName="r" values="4;16" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.9;0" dur="1.6s" repeatCount="indefinite"/></circle>'
            f'<text x="{bx + 12:.1f}" y="{by - 52:.1f}" font-size="11" fill="{ORANGE}">peak {esc(label)}</text></g>')
    def fmt_range(r):
        try:
            a_ = date.fromisoformat(r[0]).strftime("%b %Y")
            b_ = date.fromisoformat(r[1]).strftime("%b %Y")
            return f"{a_} → {b_}"
        except Exception:
            return ""
    rows = [
        ("current streak", f"{st.get('current_streak', 0)} day{'s' if st.get('current_streak', 0) != 1 else ''}", CYAN),
        ("longest streak", f"{st.get('longest_streak', 0)} day{'s' if st.get('longest_streak', 0) != 1 else ''}", PURPLE),
        ("active days", f"{st.get('active_days', 0)} / {len(days)}", GREEN),
        ("busiest weekday", esc(st.get('busiest_weekday', '-')), ORANGE),
    ]
    stats_bl = "".join(
        f'<g class="fin" style="animation-delay:{2.6 + k * 0.15:.2f}s"><text x="36" y="{H - 104 + k * 22}" font-size="12" fill="{MUTED}">{lbl}<tspan x="168" fill="{c}" font-weight="700">{v}</tspan></text></g>'
        for k, (lbl, v, c) in enumerate(rows))
    gx, gy = P(cols / 2, 3.5)
    import random
    rng = random.Random(7)
    stars = []
    while len(stars) < 46:
        sx_, sy_ = rng.uniform(28, 832), rng.uniform(68, 215)
        stars.append(f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="{rng.uniform(0.5, 1.2):.1f}" fill="#d7ecff" class="tw" style="animation-delay:{rng.uniform(0, 4):.1f}s;animation-duration:{rng.uniform(2.6, 5):.1f}s"/>')
    lights_svg = ''.join(s for _, s in sorted(lights, reverse=True)[:26])
    defs = f"""
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{GREEN}" stop-opacity="0.22"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>
<radialGradient id="moonGlow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#e6edf3" stop-opacity="0.16"/><stop offset="1" stop-color="#e6edf3" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{ORANGE}" stop-opacity="0.9"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></linearGradient>
<linearGradient id="txt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<style>.tw{{opacity:.10;animation:tw 3.8s ease-in-out infinite}}@keyframes tw{{0%,100%{{opacity:.06}}50%{{opacity:.4}}}}.b{{transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);animation:rise .9s cubic-bezier(.2,1.3,.4,1) forwards}}@keyframes rise{{to{{transform:scaleY(1)}}}}.t,.fin{{opacity:0;animation:fin .6s ease-out forwards}}@keyframes fin{{to{{opacity:1}}}}</style>"""
    body = f"""
<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="380" ry="170" fill="url(#glow)"/>
{''.join(stars)}
<circle cx="74" cy="104" r="27" fill="url(#moonGlow)"/>
<circle cx="74" cy="104" r="11" fill="#e6edf3" opacity="0.92"/>
<circle cx="79.5" cy="100" r="9.5" fill="#0d1117" opacity="0.5"/>
<text x="36" y="62" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ./skyline --user {esc(data.get('username', 'Ashutosh-Panda2004'))} --3d</text>
{''.join(out)}
{lights_svg}
{''.join(months)}
{beacon}
<g class="fin" style="animation-delay:2.4s" text-anchor="end">
  <text x="{W - 36}" y="98" font-size="44" font-weight="800" fill="url(#txt)">{st.get('total', 0):,}</text>
  <text x="{W - 36}" y="120" font-size="13" fill="{FG}">contributions in the last year</text>
  <text x="{W - 36}" y="139" font-size="11" fill="{MUTED}">{esc(fmt_range(st.get('range', [])))}</text>
</g>
{stats_bl}
"""
    write_svg("contrib-skyline.svg", window(W, H, "skyline.sh", body, defs))



# ---------------------------------------------------------------- heatmap
def heatmap_svg():
    W, H = 860, 270
    CELL, GAP = 12, 3.2
    STEP = CELL + GAP
    from datetime import date, timedelta
    data = load("contributions.json", {})
    days, st = data.get("days", []), data.get("stats", {})
    if not days:
        return
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    cols = (date.fromisoformat(days[-1]["date"]) - start).days // 7 + 1
    grid_w = cols * STEP - GAP
    x0 = (W - grid_w) / 2 + 14
    y0 = 92
    cells, months, seps, last_month = [], [], [], None
    best_xy = None
    last_xy = None
    best_count = max(1, st.get("best_day", {}).get("count", 1))
    for d in days:
        dt = date.fromisoformat(d["date"])
        off = (dt - start).days
        c, r = divmod(off, 7)
        x, y = x0 + c * STEP, y0 + r * STEP
        lvl = d["level"]
        if d["count"] == best_count:
            lvl = 5
        delay = (c + r * 1.5) * 0.018
        cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[lvl]}" class="c" style="animation-delay:{delay:.3f}s"><title>{d["count"]} on {d["date"]}</title></rect>')
        if d["count"] == best_count and best_xy is None:
            best_xy = (x, y)
        last_xy = (x, y)
        if r == 0 and dt.month != last_month and dt.day <= 7 and c < cols - 2:
            months.append(f'<text x="{x:.1f}" y="{y0 - 9}" font-size="11" fill="{MUTED}">{dt.strftime("%b")}</text>')
            if last_month is not None:
                seps.append(f'<line x1="{x - STEP / 2:.1f}" y1="{y0}" x2="{x - STEP / 2:.1f}" y2="{y0 + 7 * STEP}" stroke="#ffffff" stroke-opacity="0.05"/>')
            last_month = dt.month
    wd = "".join(
        f'<text x="{x0 - 10}" y="{y0 + r * STEP + 10}" font-size="10" fill="{MUTED}" text-anchor="end">{n}</text>'
        for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    legend_x = x0 + grid_w - 6 * 15 - 40
    ly = y0 + 7 * STEP + 14
    legend = (
        f'<text x="{legend_x - 8}" y="{ly + 10}" font-size="11" fill="{MUTED}" text-anchor="end">Less</text>'
        + "".join(f'<rect x="{legend_x + i * 15}" y="{ly}" width="{CELL}" height="{CELL}" rx="2.5" fill="{p}"/>' for i, p in enumerate(PALETTE))
        + f'<text x="{legend_x + 6 * 15 + 4}" y="{ly + 10}" font-size="11" fill="{MUTED}">More</text>')
    best = st.get("best_day", {})
    try:
        best_label = date.fromisoformat(best.get("date", "")).strftime("%b %d")
    except Exception:
        best_label = ""
    groups = [
        (f"{st.get('total', 0):,}", "contributions", GREEN),
        (f"{st.get('current_streak', 0)}d", "current streak", CYAN),
        (f"{st.get('longest_streak', 0)}d", "longest streak", PURPLE),
        (f"{best.get('count', 0)}", f"best day · {best_label}", ORANGE),
    ]
    foot, sx = [], x0
    for i, (v, label, color) in enumerate(groups):
        foot.append(f'<g class="f" style="animation-delay:{1.6 + i * 0.15:.2f}s"><text x="{sx:.1f}" y="{H - 20}" font-size="15" font-weight="700" fill="{color}">{esc(v)}<tspan font-size="11" font-weight="400" fill="{MUTED}" dx="6">{esc(label)}</tspan></text></g>')
        sx += (len(v) + len(label)) * 7.2 + 44
    clip_cells = "".join(c.split("<title>")[0].replace(' class="c"', "") + "</rect>" for c in cells)
    defs = f"""
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="gridClip">{clip_cells}</clipPath>
<style>.c{{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .45s cubic-bezier(.2,1.6,.4,1) forwards}}@keyframes pop{{from{{opacity:0;transform:scale(.2)}}to{{opacity:1;transform:scale(1)}}}}.bp{{animation:bp 2.2s ease-in-out infinite}}@keyframes bp{{0%,100%{{opacity:.2}}50%{{opacity:.95}}}}.f{{opacity:0;animation:fin .6s ease-out forwards}}@keyframes fin{{to{{opacity:1}}}}</style>"""
    body = f"""
<text x="{x0}" y="{y0 - 34}" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> git log --since="1 year ago" | heatmap</text>
{''.join(months)}{wd}
{''.join(seps)}
{''.join(cells)}
{f'<rect x="{best_xy[0] - 1.5:.1f}" y="{best_xy[1] - 1.5:.1f}" width="{CELL + 3}" height="{CELL + 3}" rx="3.5" fill="none" stroke="#69f0a0" stroke-width="1.4" class="bp"/>' if best_xy else ''}
{f'<rect x="{last_xy[0] - 1:.1f}" y="{last_xy[1] - 1:.1f}" width="{CELL + 2}" height="{CELL + 2}" rx="3" fill="none" stroke="#c9d1d9" stroke-width="1" opacity="0.7"/>' if last_xy else ''}
<g clip-path="url(#gridClip)"><rect x="{x0 - 160}" y="{y0}" width="160" height="{7 * STEP}" fill="url(#sweep)"><animate attributeName="x" values="{x0 - 160};{x0 + grid_w + 160}" begin="2.2s" dur="3.2s" repeatCount="indefinite"/></rect></g>
{legend}
{''.join(foot)}
"""
    write_svg("contrib-heatmap.svg", window(W, H, "contributions.sh", body, defs))


# ---------------------------------------------------------------- github activity
def activity_svg():
    W, H = 860, 400
    gh = load("github.json", {})
    act = load("activity.json", {})
    data = load("contributions.json", {})
    days, st = data.get("days", []), data.get("stats", {})
    total = st.get("total", 0) or 1
    commits = act.get("commits", 0)
    prs = act.get("pull_requests", 0) or gh.get("prs_opened", 0)
    issues_reviews = act.get("issues", 0) + act.get("reviews", 0)
    other = max(total - commits - prs - issues_reviews, 0)
    # donut, mirroring the reference stats card: thin ring, animated segments
    DCX, DCY, DR = 132, 168, 60
    circ = 2 * math.pi * DR
    items = [(commits, GREEN), (prs, CYAN), (issues_reviews, PURPLE),
             (other, "#6e7681")]
    gap = 3 if sum(1 for v, _ in items if v) > 1 else 0
    segs, cum = [], 0.0
    for k, (val, color) in enumerate(items):
        seg = circ * val / total
        if seg > gap:
            segs.append(
                f'<circle cx="{DCX}" cy="{DCY}" r="{DR}" fill="none" stroke="{color}" stroke-width="10" '
                f'stroke-dasharray="0 {circ:.1f}" stroke-dashoffset="{-cum:.1f}" transform="rotate(-90 {DCX} {DCY})">'
                f'<animate attributeName="stroke-dasharray" from="0 {circ:.1f}" to="{seg - gap:.1f} {circ:.1f}" '
                f'begin="{0.6 + k * 0.45:.2f}s" dur="0.7s" fill="freeze" calcMode="spline" keySplines=".3 .7 .3 1" keyTimes="0;1"/></circle>')
        cum += seg
    donut = (f'<circle cx="{DCX}" cy="{DCY}" r="{DR}" fill="none" stroke="{BORDER}" stroke-width="10"/>'
             + "".join(segs)
             + f'<g class="fin" style="animation-delay:.4s" text-anchor="middle">'
               f'<text x="{DCX}" y="{DCY + 6}" font-size="34" font-weight="800" fill="{FG}">{total:,}</text>'
               f'<text x="{DCX}" y="{DCY + 26}" font-size="11" fill="{MUTED}">contributions</text></g>')
    rows_svg = []
    for k, (label, val, color) in enumerate(
            [("Commits", commits, GREEN), ("Pull Requests", prs, CYAN),
             ("Issues + Reviews", issues_reviews, PURPLE)]):
        ry = 118 + k * 52
        share = 100 * val / total
        rows_svg.append(
            f'<g class="fin" style="animation-delay:{0.5 + k * 0.15:.2f}s">'
            f'<text x="248" y="{ry}" font-size="13" font-weight="700" fill="{color}">{esc(label)}</text>'
            f'<text x="382" y="{ry}" font-size="15" font-weight="700" fill="{FG}">{val}<tspan font-size="11" font-weight="400" fill="{MUTED}"> / {total:,}</tspan></text>'
            f'<text x="548" y="{ry}" font-size="11" fill="{MUTED}" text-anchor="end">share <tspan dx="4" fill="{color}" font-weight="700">{share:.1f}%</tspan></text>'
            f'<rect x="248" y="{ry + 10}" width="300" height="6" rx="3" fill="{BORDER}"/>'
            f'<rect x="248" y="{ry + 10}" width="0" height="6" rx="3" fill="{color}">'
            f'<animate attributeName="width" from="0" to="{300 * val / total:.1f}" begin="{0.9 + k * 0.2:.2f}s" dur="1.1s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect></g>')
    merged = gh.get("prs_merged", 0)
    opened = gh.get("prs_opened", 0) or 1
    block_rows = [
        f'<text x="610" y="106" font-size="11" fill="{MUTED}">merged pull requests</text>',
        f'<text x="610" y="146" font-size="40" font-weight="800" fill="url(#ghGrad)" filter="url(#numGlow)">{merged}</text>',
        f'<text x="610" y="170" font-size="12" fill="{FG}">{100 * merged / opened:.1f}% merge rate<tspan fill="{MUTED}">  ·  {opened} opened</tspan></text>',
        f'<text x="610" y="208" font-size="20" font-weight="800" fill="{ORANGE}">{st.get("current_streak", 0)}d<tspan font-size="11" font-weight="400" fill="{MUTED}" dx="6">current streak</tspan></text>',
        f'<text x="610" y="230" font-size="11" fill="{MUTED}">{st.get("longest_streak", 0)}d best  ·  {st.get("active_days", 0)} active days</text>',
    ]
    block = "".join(f'<g class="fin" style="animation-delay:{0.7 + k * 0.12:.2f}s">{r}</g>'
                    for k, r in enumerate(block_rows))
    grid = ""
    # weekly bars
    from datetime import timedelta
    weeks = _weeks(days)
    nweeks = len(weeks) or 1
    step = (W - 72) / nweeks
    bw = step - 3.5
    peakw = max((c for _, c in weeks), default=1) or 1
    bars, wlabels, last_month = [], [], None
    for w, (start, count) in enumerate(weeks):
        x = 36 + w * step
        tip = f"<title>{count} contributions · week of {start.strftime('%b %d')}</title>"
        if count:
            h = 4 + 42 * count / peakw
            op = 0.45 + 0.55 * count / peakw
            bars.append(f'<rect class="b" style="animation-delay:{1.2 + w * 0.02:.2f}s" x="{x:.1f}" y="{322 - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="2" fill="url(#barGrad)" opacity="{op:.2f}">{tip}</rect>')
        else:
            bars.append(f'<rect x="{x:.1f}" y="320" width="{bw:.1f}" height="2" rx="1" fill="{BORDER}">{tip}</rect>')
        for i in range(7):
            d = start + timedelta(days=i)
            if d.day == 1 and d.month != last_month and w < nweeks - 2:
                wlabels.append(f'<text x="{x:.1f}" y="337" font-size="10" fill="{MUTED}">{d.strftime("%b")}</text>')
                last_month = d.month
    if weeks:
        pw, (pstart, pcount) = max(enumerate(weeks), key=lambda t: t[1][1])
        if pcount:
            ph = 4 + 42 * pcount / peakw
            bars.append(f'<text x="{36 + pw * step + bw / 2:.1f}" y="{322 - ph - 7:.1f}" font-size="9.5" fill="{ORANGE}" text-anchor="middle">{pcount}</text>')
    glines = []
    for gv in (40, 80, 120):
        if gv < peakw:
            gyv = 4 + 42 * gv / peakw
            glines.append(f'<line x1="36" y1="{322 - gyv:.1f}" x2="824" y2="{322 - gyv:.1f}" stroke="{BORDER}" stroke-opacity="0.45" stroke-dasharray="2 4"/>')
            glines.append(f'<text x="36" y="{322 - gyv - 3:.1f}" font-size="8.5" fill="{MUTED}">{gv}</text>')
    bars[0:0] = glines
    badge_text = f"◆ Best day · {st.get('best_day', {}).get('count', 0)}"
    chips_max = W - 36 - (len(badge_text) + 2) * 6.6 - 16
    chips, chip_x = [], 36.0
    for k, (name, count) in enumerate(act.get("repos", [])):
        wch = len(name) * 6.6 + 6 + len(str(count)) * 6.6 + 20
        if chip_x + wch > chips_max:
            break
        chips.append(
            f'<g class="fin" style="animation-delay:{2.2 + k * 0.08:.2f}s">'
            f'<rect x="{chip_x:.1f}" y="364" width="{wch:.1f}" height="20" rx="10" fill="{PANEL}" stroke="{BORDER}"/>'
            f'<text x="{chip_x + 10:.1f}" y="378" font-size="11" fill="{FG}">{esc(name)}<tspan dx="6" fill="{ORANGE}">{count}</tspan></text></g>')
        chip_x += wch + 8
    defs = f"""
<linearGradient id="ghGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="barGrad" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffa116"/><stop offset="1" stop-color="#ffc01e"/></linearGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{GREEN}" stop-opacity="0.14"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>
<filter id="numGlow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="{GREEN}" flood-opacity="0.45"/></filter>
<style>.fin{{opacity:0;animation:fin .6s ease-out forwards}}@keyframes fin{{to{{opacity:1}}}}.b{{transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);animation:rise .7s cubic-bezier(.2,1.3,.4,1) forwards}}@keyframes rise{{to{{transform:scaleY(1)}}}}</style>"""
    body = f"""
<text x="36" y="62" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> github --user Ashutosh-Panda2004 --stats</text>
<text x="824" y="62" font-size="11" fill="{MUTED}" text-anchor="end">github.com/Ashutosh-Panda2004</text>
<circle cx="{DCX}" cy="{DCY}" r="96" fill="url(#halo)"><animate attributeName="opacity" values="0.6;1;0.6" dur="5s" repeatCount="indefinite"/></circle>
{donut}
{''.join(rows_svg)}
<line x1="582" y1="96" x2="582" y2="238" stroke="{BORDER}"/>
{block}
{grid}
<g class="fin" style="animation-delay:1s"><text x="36" y="262" font-size="11" fill="{MUTED}">contributions per week  ·  <tspan fill="{FG}">{total:,}</tspan> in the last year  ·  busiest on {esc(st.get('busiest_weekday', '-'))}s</text></g>
{''.join(bars)}
{''.join(wlabels)}
{''.join(chips)}
<g class="fin" style="animation-delay:2.6s"><text x="824" y="378" font-size="11" fill="{ORANGE}" text-anchor="end">{esc(badge_text)}</text></g>
"""
    write_svg("github-activity.svg", window(W, H, "github.sh", body, defs))


def main():
    header_svg()
    try:
        portrait_svg()
    except (FileNotFoundError, ImportError):
        print("skip ascii-portrait.svg (work/source-prepped.png not present)")
    info_card_svg()
    globe_svg()
    tech_sphere_svg()
    skyline_svg()
    activity_svg()
    heatmap_svg()
    projects_svg()


# ---------------------------------------------------------------- projects
PROJECT_CARDS = [
    ("TokenLens", "tokenlens.sh", CYAN, "tokenslens.vercel.app", "lens",
     ["Copilot credit ledger with waste",
      "attribution across 14 named causes,",
      "savings simulation and policy",
      "compilation. Fully local, zero",
      "network calls."]),
    ("ShutdownCheck", "shutdowncheck.sh", ORANGE, "shutdowncheck.vercel.app", "power",
     ["Terminates your service the way",
      "your orchestrator will, under real",
      "load. A 7-stage termination model",
      "with named findings and",
      "deterministic scoring."]),
    ("InterviewCoach AI", "interviewcoach.sh", PURPLE, "interview-coach-ai-steel.vercel.app", "voice",
     ["Voice-based mock interviews with",
      "an AI that knows your resume.",
      "Realistic questions, detailed",
      "structured feedback after every",
      "session."]),
]


def _project_icon(kind, color):
    if kind == "lens":
        return (f'<circle cx="37" cy="60" r="11" fill="none" stroke="{color}" stroke-width="2"/>'
                f'<circle cx="37" cy="60" r="4.5" fill="{color}"/>')
    if kind == "power":
        return (f'<path d="M29.5 53.5 a10.5 10.5 0 1 0 15 0" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
                f'<line x1="37" y1="46" x2="37" y2="57" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>')
    return (f'<rect x="27" y="55" width="4.5" height="10" rx="2.25" fill="{color}"/>'
            f'<rect x="34.75" y="50" width="4.5" height="20" rx="2.25" fill="{color}"/>'
            f'<rect x="42.5" y="53.5" width="4.5" height="13" rx="2.25" fill="{color}"/>')


def projects_svg():
    W, H = 277, 210
    for name, slug, color, domain, icon, desc in PROJECT_CARDS:
        fname = "project-" + name.split()[0].lower() + ".svg"
        lines = [f'<text x="24" y="{104 + i * 16}" font-size="11.5" fill="{FG}">{esc(t)}</text>'
                 for i, t in enumerate(desc)]
        defs = (f'<style>.fin{{opacity:0;animation:fin .7s ease-out forwards}}'
                f'@keyframes fin{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}</style>'
                f'<radialGradient id="pGlow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{color}" stop-opacity="0.20"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'
                f'<linearGradient id="pSheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                f'<clipPath id="pClip"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10"/></clipPath>')
        body = f"""
<g class="fin">
  <circle cx="37" cy="60" r="21" fill="url(#pGlow)"/>
  {_project_icon(icon, color)}
  <text x="58" y="58" font-size="16.5" font-weight="800" fill="{FG}">{esc(name)}</text>
  <text x="58" y="76" font-size="9.5" fill="{MUTED}">{esc(domain)}</text>
  <line x1="24" y1="88" x2="{W - 24}" y2="88" stroke="{BORDER}" stroke-opacity="0.7"/>
  {''.join(lines)}
  <rect x="24" y="{H - 32}" width="92" height="18" rx="9" fill="{PANEL}" stroke="{BORDER}"/>
  <circle cx="36" cy="{H - 23}" r="3" fill="{color}"><animate attributeName="opacity" values="1;0.35;1" dur="2.2s" repeatCount="indefinite"/></circle>
  <text x="44" y="{H - 19.5}" font-size="10" fill="{FG}">Live site</text>
  <text x="104" y="{H - 19.5}" font-size="10" fill="{color}">↗</text>
</g>
<g clip-path="url(#pClip)"><g transform="rotate(18 138 105)"><rect x="-240" y="-40" width="110" height="{H + 80}" fill="url(#pSheen)"><animate attributeName="x" values="-240;560;560" keyTimes="0;0.26;1" dur="8s" repeatCount="indefinite"/></rect></g></g>"""
        write_svg(fname, window(W, H, slug, body, defs))


if __name__ == "__main__":
    main()

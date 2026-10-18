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


def window(width, height, title, body, extra_defs=""):
    """Terminal window chrome shared by every card."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">
<defs>{extra_defs}</defs>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>
<path d="M0.5 32 V10.5 a10 10 0 0 1 10 -10 H{width - 10.5} a10 10 0 0 1 10 10 V32 Z" fill="{PANEL}"/>
<line x1="0.5" y1="32" x2="{width - 0.5}" y2="32" stroke="{BORDER}"/>
<circle cx="18" cy="16" r="5.5" fill="#ff5f56"/><circle cx="36" cy="16" r="5.5" fill="#ffbd2e"/><circle cx="54" cy="16" r="5.5" fill="#27c93f"/>
<text x="{width / 2}" y="20.5" fill="{MUTED}" font-size="12" text-anchor="middle">{esc(title)}</text>
{body}
</svg>
"""


# ---------------------------------------------------------------- header
NAME = "Ashutosh Panda"
PROMPT_USER = "ashutosh"
PROMPT_HOST = "github"
ROLES = [
    "Backend Engineer at Honeywell",
    "Open Source Contributor",
    "77 merged pull requests",
    "Building TokenLens and ShutdownCheck",
    "Backend systems in Go and TypeScript",
]
TAGLINE = "Bengaluru, IN  ·  Go, TypeScript and backend systems"


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
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0.08"/></linearGradient>
<clipPath id="inner"><rect x="1" y="33" width="{W - 2}" height="{H - 34}" rx="9"/></clipPath>
<clipPath id="cmdClip"><rect x="{cmd_x}" y="40" width="0" height="20"><animate attributeName="width" from="0" to="{len(cmd) * 8.4 + 2}" begin="0.3s" dur="0.6s" fill="freeze"/></rect></clipPath>
<style>.fade {{ opacity: 0; animation: in .7s ease-out forwards; }} @keyframes in {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}</style>"""
    body = f"""
<g clip-path="url(#inner)">
  <rect x="0" y="32" width="{W}" height="{H}" fill="url(#dots)"/>
  <rect x="0" y="-40" width="{W}" height="40" fill="url(#scan)"><animate attributeName="y" values="-10;{H}" dur="5s" repeatCount="indefinite"/></rect>
</g>
<text x="40" y="55" font-size="14"><tspan fill="{GREEN}">{esc(prompt)}</tspan></text>
<text x="{cmd_x}" y="55" font-size="14" fill="{FG}" textLength="{len(cmd) * 8.4:.1f}" clip-path="url(#cmdClip)">{esc(cmd)}</text>
<g class="fade" style="animation-delay:1s">
  <text x="40" y="112" font-size="46" font-weight="800" letter-spacing="2" fill="url(#nameGrad)" filter="url(#glow)">{esc(NAME.upper())}</text>
</g>
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
        text = esc(line).replace(" ", " ")
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
    write_svg("ascii-portrait.svg", window(W, H, "portrait.txt", body, defs))


# ---------------------------------------------------------------- info card
LANG_COLORS = {
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Python": "#3572A5",
    "CSS": "#663399", "HTML": "#e34c26", "Go": "#00ADD8", "Java": "#b07219",
    "Shell": "#89e051", "Dockerfile": "#384d54", "C++": "#f34b7d",
    "C#": "#178600", "Rust": "#dea584",
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


def info_card_svg():
    W, H = 490, 420
    prof = load("profile.json", {})
    gh = load("github.json", {})
    st = load("contributions.json", {}).get("stats", {})
    langs = prof.get("languages", {})
    rows = [
        ("Role", "Backend Engineer · Honeywell"),
        ("Now", "Backend work on a migration platform"),
        ("OSS", "checkstyle · Fineract · SW360"),
        ("Uptime", f"{_uptime(prof['created_at'])} on GitHub"
         if prof.get("created_at") else "-"),
        ("Langs", " · ".join(list(langs)[:3]) or "-"),
        ("Backend", "Go · .NET · Node.js"),
        ("Frontend", "React · Vite · Tailwind"),
        ("Projects", "TokenLens · ShutdownCheck"),
        ("PRs", f"{gh.get('prs_opened', '-')} opened · {gh.get('prs_merged', '-')} merged"),
        ("Reviews", f"{gh.get('prs_reviewed', '-')} PRs reviewed · {gh.get('issues_opened', '-')} issues"),
        ("Repos", f"{prof.get('public_repos', '-')} public · {prof.get('stars', '-')} stars"),
        ("Streak", f"{st.get('current_streak', 0)}d current · {st.get('longest_streak', 0)}d best"),
    ]
    x, y = 24, 60
    head = f"{PROMPT_USER}@{PROMPT_HOST}"
    lines = [
        f'<g class="ln" style="animation-delay:0.50s"><text x="{x}" y="{y}" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> neofetch</text></g>',
        f'<g class="ln" style="animation-delay:0.59s"><text x="{x}" y="{y + 28}" font-size="15" font-weight="700"><tspan fill="{GREEN}">{PROMPT_USER}</tspan><tspan fill="{FG}">@</tspan><tspan fill="{CYAN}">{PROMPT_HOST}</tspan></text>'
        f'<text x="{x}" y="{y + 42}" font-size="13" fill="{MUTED}">{"-" * len(head)}</text></g>',
    ]
    ry = y + 64
    for k, (key, val) in enumerate(rows):
        color = KEY_COLORS[k % len(KEY_COLORS)]
        lines.append(
            f'<g class="ln" style="animation-delay:{0.68 + k * 0.09:.2f}s"><text x="{x}" y="{ry + k * 20}" font-size="13"><tspan fill="{color}" font-weight="700">{esc(key)}</tspan>'
            f'<tspan x="{x + 92}" fill="{FG}">{esc(val)}</tspan></text></g>')
    # language bar over the six biggest languages
    top = list(langs.items())[:6]
    shown_total = sum(v for _, v in top) or 1
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
        f'<clipPath id="barClip"><rect x="{x}" y="{by}" width="0" height="8" rx="4"><animate attributeName="width" from="0" to="{bar_w}" begin="1.6s" dur="1.2s" fill="freeze"/></rect></clipPath>'
        f'<rect x="{x}" y="{by}" width="{bar_w}" height="8" rx="4" fill="{BORDER}"/>'
        f'<g clip-path="url(#barClip)">{"".join(segs)}</g>'
        f'<g class="ln" style="animation-delay:2.3s">{"".join(legend)}</g>')
    defs = """<style>.ln { opacity: 0; animation: ln .5s ease-out forwards; } @keyframes ln { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: none; } }</style>"""
    write_svg("info-card.svg", window(W, H, f"{PROMPT_USER}@{PROMPT_HOST}: ~",
                                      "\n".join(lines), defs))


# ---------------------------------------------------------------- globe
# Coarse hand-drawn land grid, 5 degree cells. '#' is land.
WORLD_MAP = [
    "............####.........######......#........#.......#.......#.........",
    "..........########......#########.....##......##......##......##........",
    "..###....##########....###########...###......##......##.......##.......",
    ".######..###########..############....##..#...###.....###.......###......",
    "..######.############.#############...##.##..####....####........##.......",
    "...##################.#############...#####.#####..#####.........##......",
    "....################.########.####....#######################....##......",
    ".....##############..#####...####.....#########################...#......",
    "......############...####....###..##############################.........",
    ".......##########....###.....##..###############################.........",
    "........########.....##......#..####.##########################..........",
    ".........######......##..........########################################",
    ".........#####.......##.........####..##################################.",
    "..........####.......#..........###....################################..",
    "..........###...................##......########..###################....",
    "..........##....................#........######......################....",
    "...............................##.........####........##############.....",
    "......................##.......###.........##..........############......",
    ".....................####......####.....................#########........",
    ".....................#####.....#####......................#######........",
    "......................####......####........................#####.........",
    "......................###.......#####.......................####.........",
    "......................##.........####.......................###..........",
    "......................##..........###.......................##...........",
    "......................#............##....................................",
    "...................................#.....................................",
    "........................................................................",
    "........................................................................",
    "........................................................................",
    "........................................................................",
    "........................................................................",
    "........................................................................",
    "........................................................................",
]
HOME = ("Bengaluru", 12.97, 77.59)
REGIONS = [
    ("checkstyle", 50.11, 14.42),
    ("Apache Fineract", 38.90, -77.04),
    ("Eclipse SW360", 48.14, 11.58),
    ("OpenMRS", 39.77, -86.16),
]
GLOBE_R = 150
GLOBE_C = (215, 205)
VIEW_LON = 35.0
VIEW_LAT = 16.0


def _project(lat, lon, center_lon=VIEW_LON, tilt=VIEW_LAT):
    """Orthographic projection. Returns (x, y, z) with z > 0 on the front."""
    la, lo = math.radians(lat), math.radians(lon - center_lon)
    t = math.radians(tilt)
    x = GLOBE_C[0] + GLOBE_R * math.cos(la) * math.sin(lo)
    y = GLOBE_C[1] - GLOBE_R * (math.sin(la) * math.cos(t)
                                - math.cos(la) * math.cos(lo) * math.sin(t))
    z = math.sin(la) * math.sin(t) + math.cos(la) * math.cos(lo) * math.cos(t)
    return x, y, z


def _land_points():
    pts = []
    rows = len(WORLD_MAP)
    for r, row in enumerate(WORLD_MAP):
        lat = 82.5 - r * 5
        row = (row + "." * 72)[:72]
        for c, ch in enumerate(row):
            if ch == "#" and (r + c) % 2 == 0:
                pts.append((lat, -177.5 + c * 5))
    return pts


def globe_svg():
    W, H = 430, 400
    period, steps = 36, 18
    keys, dots = [], []
    for i, (lat, lon) in enumerate(_land_points()):
        frames, last = [], None
        for s in range(steps + 1):
            rot = 360.0 * s / steps
            x, y, z = _project(lat, lon + rot, center_lon=lon + VIEW_LON
                               if False else VIEW_LON, tilt=VIEW_LAT)
            # rotate the view instead: shift longitude by -rot
            x, y, z = _project(lat, lon, center_lon=VIEW_LON + rot, tilt=VIEW_LAT)
            op = 0.95 if z > 0.02 else 0.0
            fr = (f"{100.0 * s / steps:.2f}%{{transform:translate({x:.1f}px,{y:.1f}px);"
                  f"opacity:{op:.2f}}}")
            if fr != last:
                frames.append(fr)
                last = fr
        keys.append(f"@keyframes k{i}{{{''.join(frames)}}}")
        dots.append(f'<circle class="dot" r="1.7" fill="{CYAN}" '
                    f'style="animation:k{i} {period}s linear infinite"/>')
    hx, hy, _ = _project(*HOME[1:], center_lon=VIEW_LON, tilt=VIEW_LAT)
    arcs, pins = [], [f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="4" fill="{ORANGE}"/>']
    for name, lat, lon in REGIONS:
        ex, ey, ez = _project(lat, lon, center_lon=VIEW_LON, tilt=VIEW_LAT)
        if ez <= 0:  # far side: land the arc on the limb instead
            ex, ey = GLOBE_C[0] - GLOBE_R + 8, GLOBE_C[1] - 30
        mx, my = (hx + ex) / 2, min(hy, ey) - 55
        arcs.append(f'<path d="M{hx:.1f},{hy:.1f} Q{mx:.1f},{my:.1f} {ex:.1f},{ey:.1f}" '
                    f'fill="none" stroke="{PURPLE}" stroke-width="1.4" '
                    f'stroke-dasharray="4 4" opacity="0.85"/>')
        pins.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.2" fill="{GREEN}"/>')
    legend = " · ".join([HOME[0]] + [r[0] for r in REGIONS])
    defs = ("<style>" + "".join(keys) +
            ".dot{opacity:0}.fin{opacity:0;animation:fin 1s ease-out .3s forwards}"
            "@keyframes fin{to{opacity:1}}</style>")
    body = f"""
<text x="36" y="58" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ./open-source --from bengaluru</text>
<circle cx="{GLOBE_C[0]}" cy="{GLOBE_C[1]}" r="{GLOBE_R}" fill="#0b1526" stroke="{BORDER}"/>
{''.join(dots)}
<g class="fin">{''.join(arcs)}{''.join(pins)}
<text x="{hx + 9:.1f}" y="{hy + 4:.1f}" font-size="11" fill="{ORANGE}">Bengaluru</text></g>
<text x="215" y="382" font-size="11.5" fill="{MUTED}" text-anchor="middle">● {esc(legend)}</text>
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
    cx, cy, radius = 215, 205, 140
    period, steps = 30, 16
    labels, keys = [], []
    idx = 0
    for ci, (cat, items) in enumerate(TECH.items()):
        color = TECH_COLORS[ci % len(TECH_COLORS)]
        for j, label in enumerate(items):
            # spread labels on the sphere with a golden-angle spiral
            frac = (idx + 0.5) / 21.0
            lat = math.degrees(math.acos(1 - 2 * frac)) - 90
            lon = (idx * 137.5) % 360 - 180
            frames = []
            for s in range(steps + 1):
                rot = 360.0 * s / steps
                lo = math.radians(lon + rot)
                la = math.radians(lat)
                z = math.cos(la) * math.cos(lo)
                x = cx + radius * math.cos(la) * math.sin(lo)
                y = cy - radius * math.sin(la) * 0.92
                scale = 0.55 + 0.45 * (z + 1) / 2
                op = 0.12 + 0.88 * (z + 1) / 2 if z > -0.9 else 0.05
                frames.append(f"{100.0 * s / steps:.2f}%{{transform:translate({x:.1f}px,{y:.1f}px) scale({scale:.2f});opacity:{op:.2f}}}")
            keys.append(f"@keyframes t{idx}{{{''.join(frames)}}}")
            labels.append(
                f'<text class="tlabel" text-anchor="middle" fill="{color}" font-weight="700" '
                f'font-size="13" style="animation:t{idx} {period}s linear infinite">{esc(label)}</text>')
            idx += 1
    legend = []
    lx = 40
    for ci, cat in enumerate(TECH):
        legend.append(f'<circle cx="{lx + 4}" cy="368" r="4" fill="{TECH_COLORS[ci]}"/>'
                      f'<text x="{lx + 13}" y="372" font-size="11" fill="{MUTED}">{esc(cat)}</text>')
        lx += len(cat) * 6.8 + 34
    defs = ("<style>" + "".join(keys) +
            ".tlabel{opacity:0}.fin{opacity:0;animation:fin 1s ease-out .3s forwards}"
            "@keyframes fin{to{opacity:1}}</style>")
    body = f"""
<text x="36" y="58" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ls ~/stack --3d</text>
<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{BORDER}" stroke-dasharray="3 5"/>
{''.join(labels)}
<g class="fin">{''.join(legend)}</g>
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
    data = load("contributions.json", {})
    days, st = data.get("days", []), data.get("stats", {})
    weeks = _weeks(days)
    base_y, top_y = 392, 120
    max_count = max((c for _, c in weeks), default=1) or 1
    bw = (W - 90) / max(len(weeks), 1)
    bars, month_labels, seen_months = [], [], set()
    for i, (start, count) in enumerate(weeks):
        x = 45 + i * bw
        h = 6 + (math.sqrt(count / max_count)) * (base_y - top_y - 6) if count else 3
        y = base_y - h
        level = 0 if count == 0 else min(5, 1 + int(4 * count / max_count))
        top_c, side_c = PALETTE[level], PALETTE[max(level - 1, 0)]
        depth = min(7, bw * 0.45)
        delay = 0.3 + i * 0.03
        bars.append(
            f'<g class="bar" style="animation-delay:{delay:.2f}s">'
            f'<polygon points="{x:.1f},{y:.1f} {x + bw - 2:.1f},{y:.1f} {x + bw - 2 + depth:.1f},{y - depth:.1f} {x + depth:.1f},{y - depth:.1f}" fill="{top_c}"/>'
            f'<polygon points="{x + bw - 2:.1f},{y:.1f} {x + bw - 2 + depth:.1f},{y - depth:.1f} {x + bw - 2 + depth:.1f},{base_y - depth:.1f} {x + bw - 2:.1f},{base_y:.1f}" fill="{side_c}"/>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw - 2:.1f}" height="{h:.1f}" fill="{PALETTE[level]}" opacity="0.92"/></g>')
        mon = start.strftime("%b")
        if mon not in seen_months or start.day <= 7:
            if start.strftime("%Y-%m") not in seen_months:
                seen_months.add(start.strftime("%Y-%m"))
                month_labels.append(f'<text x="{x:.1f}" y="{base_y + 24}" font-size="11" fill="{MUTED}">{mon}</text>')
    best = st.get("best_day", {})
    rng = st.get("range", ["", ""])
    def fmt_range(r):
        from datetime import date
        try:
            a = date.fromisoformat(r[0]).strftime("%b %Y")
            b = date.fromisoformat(r[1]).strftime("%b %Y")
            return f"{a} to {b}"
        except Exception:
            return ""
    body = f"""
<text x="36" y="58" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ./skyline --user Ashutosh-Panda2004 --3d</text>
<line x1="36" y1="{base_y}" x2="{W - 30}" y2="{base_y}" stroke="{BORDER}"/>
{''.join(bars)}
{''.join(month_labels)}
<g class="fin" style="animation-delay:2.2s" text-anchor="end">
  <text x="{W - 36}" y="92" font-size="30" font-weight="800" fill="{FG}">{st.get('total', 0):,}</text>
  <text x="{W - 36}" y="112" font-size="12" fill="{MUTED}">contributions in the last year</text>
  <text x="{W - 36}" y="132" font-size="12" fill="{MUTED}">{esc(fmt_range(rng))}</text>
</g>
<g class="fin" style="animation-delay:2.5s">
  <text x="36" y="92" font-size="12" fill="{MUTED}">peak {best.get('count', 0)} · {esc(best.get('date', ''))}</text>
  <text x="36" y="112" font-size="12" fill="{MUTED}">current streak {st.get('current_streak', 0)} days · longest {st.get('longest_streak', 0)} days</text>
  <text x="36" y="132" font-size="12" fill="{MUTED}">active days {st.get('active_days', 0)} / {len(days)} · busiest {esc(st.get('busiest_weekday', '-'))}</text>
</g>
"""
    defs = """<style>.bar{opacity:0;animation:rise .7s cubic-bezier(.2,1.3,.4,1) forwards}@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}.fin{opacity:0;animation:fin .6s ease-out forwards}@keyframes fin{to{opacity:1}}</style>"""
    write_svg("contrib-skyline.svg", window(W, H, "skyline.sh", body, defs))


# ---------------------------------------------------------------- heatmap
def heatmap_svg():
    W, H = 860, 270
    data = load("contributions.json", {})
    days, st = data.get("days", []), data.get("stats", {})
    cell, gap = 11, 3
    x0, y0 = 46, 64
    cols = (len(days) + 6) // 7
    cells, month_labels, seen = [], [], set()
    from datetime import date
    for i, d in enumerate(days):
        col, row = divmod(i, 7)
        x, y = x0 + col * (cell + gap), y0 + row * (cell + gap)
        delay = (col + row) * 0.018
        cells.append(f'<rect class="cell" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{PALETTE[d["level"]]}"><title>{d["date"]}: {d["count"]}</title></rect>')
        dt = date.fromisoformat(d["date"])
        if dt.day <= 7 and dt.strftime("%Y-%m") not in seen:
            seen.add(dt.strftime("%Y-%m"))
            month_labels.append(f'<text x="{x}" y="{y0 - 10}" font-size="11" fill="{MUTED}">{dt.strftime("%b")}</text>')
    weekdays = "".join(
        f'<text x="{x0 - 8}" y="{y0 + r * (cell + gap) + 10}" font-size="10" fill="{MUTED}" text-anchor="end">{label}</text>'
        for r, label in [(0, "Sun"), (1, "Mon"), (3, "Wed"), (5, "Fri")])
    legend_x = x0
    legend = [f'<text x="{legend_x}" y="{y0 + 7 * (cell + gap) + 22}" font-size="11" fill="{MUTED}">Less</text>']
    for i, c in enumerate(PALETTE[1:]):
        legend.append(f'<rect x="{legend_x + 34 + i * (cell + gap)}" y="{y0 + 7 * (cell + gap) + 12}" width="{cell}" height="{cell}" rx="2.5" fill="{c}"/>')
    legend.append(f'<text x="{legend_x + 34 + 5 * (cell + gap) + 4}" y="{y0 + 7 * (cell + gap) + 22}" font-size="11" fill="{MUTED}">More</text>')
    stats = (f"{st.get('total', 0):,} contributions · {st.get('current_streak', 0)}d current streak · "
             f"{st.get('longest_streak', 0)}d longest streak · {st.get('best_day', {}).get('count', 0)} best day")
    body = f"""
<text x="36" y="58" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> git log --since="1 year ago" | heatmap</text>
{weekdays}
{''.join(month_labels)}
{''.join(cells)}
{''.join(legend)}
<text x="{W - 36}" y="{y0 + 7 * (cell + gap) + 22}" font-size="12" fill="{FG}" text-anchor="end">{esc(stats)}</text>
"""
    defs = """<style>.cell{opacity:0;animation:cell .4s ease-out forwards}@keyframes cell{from{opacity:0}to{opacity:1}}</style>"""
    write_svg("contrib-heatmap.svg", window(W, H, "contributions.sh", body, defs))


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
    heatmap_svg()


if __name__ == "__main__":
    main()

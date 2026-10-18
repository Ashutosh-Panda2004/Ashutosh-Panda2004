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
    cols, font, lh = 94, 6.0, 6.9
    cw = font * 0.6
    img = Image.open(src).convert("L")
    a_full = np.asarray(img, dtype=np.float32) / 255
    ys, xs = np.nonzero(a_full > 0.04)
    if len(xs) == 0:
        raise ValueError("portrait source is empty")
    subj = a_full[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    sh, sw = subj.shape
    band = subj[:max(1, int(sh * 0.18))]
    bx = np.nonzero(band > 0.04)[1]
    head_cx = float(np.median(bx)) if len(bx) else sw / 2
    half = sw * 0.26
    cx0 = int(max(0, head_cx - half))
    cx1 = int(min(sw, head_cx + half))
    crop = subj[:int(sh * 0.58), cx0:cx1]
    ch, cw_px = crop.shape
    rows = int(cols * cw / lh * ch / cw_px)
    max_rows = int((H - 52) / lh)
    if rows > max_rows:
        keep = int(ch * max_rows / rows)
        crop, rows = crop[:keep], max_rows
    small = np.asarray(
        Image.fromarray((crop * 255).astype("uint8")).resize(
            (cols, rows), Image.LANCZOS), dtype=np.float32) / 255
    nz = small[small > 0.04]
    lo, hi = np.percentile(nz, [2, 99.5]) if nz.size else (0, 1)
    a = np.where(small > 0.04,
                 np.clip((small - lo) / max(hi - lo, 1e-6), 0, 1) ** 0.6, 0)
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
HOME = ("Bengaluru", 12.97, 77.59)
REGIONS = [
    ("checkstyle", 50.11, 14.42),
    ("Apache Fineract", 38.90, -77.04),
    ("Eclipse SW360", 48.14, 11.58),
    ("OpenMRS", 39.77, -86.16),
]
GLOBE_R = 132
GLOBE_C = (215, 205)
GLOBE_TILT = 22.0
GLOBE_PERIOD = 36
VIEW_LON = 35.0


def _land_points():
    """Fallback coarse grid, used only if scripts/land_points.json is missing."""
    return [(lat, lon) for lat in range(-56, 81, 8)
            for lon in range(-180, 180, 8)]


def _globe_pos(lat, theta_deg):
    la, th = math.radians(lat), math.radians(theta_deg)
    t = math.radians(GLOBE_TILT)
    x = GLOBE_C[0] + GLOBE_R * math.cos(la) * math.sin(th)
    y = GLOBE_C[1] - GLOBE_R * (math.sin(la) * math.cos(t)
                                - math.cos(la) * math.cos(th) * math.sin(t))
    return x, y


def _globe_split(lat):
    return GLOBE_C[1] - GLOBE_R * math.sin(math.radians(lat)) * math.cos(
        math.radians(GLOBE_TILT))


def _slerp(lat1, lon1, lat2, lon2):
    def vec(lat, lon):
        la, lo = math.radians(lat), math.radians(lon)
        return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo),
                math.sin(la))
    A, B = vec(lat1, lon1), vec(lat2, lon2)
    dot = max(-1.0, min(1.0, sum(a * b for a, b in zip(A, B))))
    ang = math.degrees(math.acos(dot))
    n = max(5, int(round(ang / 7.0)))
    pts, s = [], math.sin(math.radians(ang))
    for i in range(1, n + 1):
        f = i / n
        ka = math.sin((1 - f) * math.radians(ang)) / s
        kb = math.sin(f * math.radians(ang)) / s
        v = tuple(ka * a + kb * b for a, b in zip(A, B))
        pts.append((round(math.degrees(math.asin(max(-1.0, min(1.0, v[2])))), 1),
                    round(math.degrees(math.atan2(v[1], v[0])), 1)))
    return pts


def globe_svg():
    W, H = 430, 400
    lp = os.path.join(ROOT, "scripts", "land_points.json")
    land = [tuple(p) for p in json.load(open(lp))] if os.path.exists(lp) \
        else _land_points()
    rows = {}
    def row(lat):
        return rows.setdefault(round(float(lat), 1),
                               {"land": [], "route": [], "home": False})
    for lat, lon in land:
        row(lat)["land"].append(lon)
    for _name, rlat, rlon in REGIONS:
        for lat, lon in _slerp(HOME[1], HOME[2], rlat, rlon):
            row(lat)["route"].append(lon)
    row(HOME[1])["home"] = True
    home_delay = ((HOME[2] - VIEW_LON) % 360) / 360 * GLOBE_PERIOD
    keys, groups = [], []
    for i, lat in enumerate(sorted(rows)):
        frames = []
        for s in range(37):
            x, y = _globe_pos(lat, s * 10)
            frames.append(f"{100.0 * s / 36:.2f}%{{transform:translate({x:.1f}px,{y:.1f}px)}}")
        keys.append(f"@keyframes kf{i}{{{''.join(frames)}}}.k{i}{{animation:kf{i} {GLOBE_PERIOD}s linear infinite}}")
        split = _globe_split(lat)
        r = 1.7 if abs(lat) <= 55 else 1.4
        def circles(lons, twinkle=False):
            out = []
            for j, lon in enumerate(lons):
                delay = ((lon - VIEW_LON) % 360) / 360 * GLOBE_PERIOD
                tw = (f'<animate attributeName="opacity" values="0.15;1;0.15" dur="2.8s" '
                      f'begin="{(j * 0.37) % 2.8:.2f}s" repeatCount="indefinite"/>') if twinkle else ""
                out.append(f'<circle r="{r}" class="k{i}" style="animation-delay:-{delay:.2f}s">{tw}</circle>')
            return "".join(out)
        info = rows[lat]
        if info["land"]:
            dots = circles(sorted(info["land"]))
            groups.append(f'<clipPath id="f{i}"><rect x="0" y="{split:.2f}" width="{W}" height="{H}"/></clipPath>'
                          f'<g clip-path="url(#f{i})" fill="{GREEN}">{dots}</g>')
            groups.append(f'<clipPath id="b{i}"><rect x="0" y="0" width="{W}" height="{split:.2f}"/></clipPath>'
                          f'<g clip-path="url(#b{i})" fill="{GREEN}" opacity="0.14">{dots}</g>')
        if info["route"]:
            groups.append(f'<clipPath id="r{i}"><rect x="0" y="{split:.2f}" width="{W}" height="{H}"/></clipPath>'
                          f'<g clip-path="url(#r{i})" fill="{ORANGE}">{circles(sorted(info["route"]), twinkle=True)}</g>')
        if info["home"]:
            groups.append(
                f'<clipPath id="hf{i}"><rect x="0" y="{split:.2f}" width="{W}" height="{H}"/></clipPath>'
                f'<g clip-path="url(#hf{i})">'
                f'<circle r="2.8" fill="{ORANGE}" class="k{i}" style="animation-delay:-{home_delay:.2f}s"/>'
                f'<circle r="3" fill="{ORANGE}" class="k{i}" style="animation-delay:-{home_delay:.2f}s">'
                f'<animate attributeName="r" values="3;13" dur="1.8s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.8;0" dur="1.8s" repeatCount="indefinite"/></circle>'
                f'<circle r="3.2" fill="#ffffff" class="k{i}" style="animation-delay:-{home_delay:.2f}s"/></g>')
    grat = []
    for lat in (-60, -30, 0, 30, 60):
        rx = GLOBE_R * math.cos(math.radians(lat))
        grat.append(f'<ellipse cx="{GLOBE_C[0]}" cy="{_globe_split(lat):.1f}" rx="{rx:.1f}" '
                    f'ry="{rx * math.sin(math.radians(GLOBE_TILT)):.1f}" fill="none" stroke="#2d3a4a" stroke-width="0.8"/>')
    legend = "Bengaluru → checkstyle · Fineract · SW360 · OpenMRS"
    defs = f"""
<radialGradient id="ocean" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="#16324a"/><stop offset="0.7" stop-color="#0c1724"/><stop offset="1" stop-color="#070b12"/></radialGradient>
<radialGradient id="shade" cx="0.5" cy="0.5" r="0.5"><stop offset="0.72" stop-color="#05080d" stop-opacity="0"/><stop offset="1" stop-color="#05080d" stop-opacity="0.75"/></radialGradient>
<radialGradient id="atmo" cx="0.5" cy="0.5" r="0.5"><stop offset="0.86" stop-color="{CYAN}" stop-opacity="0"/><stop offset="0.92" stop-color="{CYAN}" stop-opacity="0.22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<style>{''.join(keys)}.fin{{opacity:0;animation:fin 1s ease-out .3s forwards}}@keyframes fin{{to{{opacity:1}}}}</style>"""
    body = f"""
<text x="20" y="56" font-size="12" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ./open-source --from bengaluru</text>
<g class="fin">
<circle cx="{GLOBE_C[0]}" cy="{GLOBE_C[1]}" r="153" fill="url(#atmo)"/>
<circle cx="{GLOBE_C[0]}" cy="{GLOBE_C[1]}" r="{GLOBE_R}" fill="url(#ocean)"/>
{''.join(grat)}
{''.join(groups)}
<circle cx="{GLOBE_C[0]}" cy="{GLOBE_C[1]}" r="{GLOBE_R}" fill="url(#shade)"/>
<circle cx="{GLOBE_C[0]}" cy="{GLOBE_C[1]}" r="{GLOBE_R}" fill="none" stroke="{CYAN}" stroke-opacity="0.25"/>
</g>
<text x="215" y="378" font-size="10.5" fill="{MUTED}" text-anchor="middle"><tspan fill="{ORANGE}">●</tspan> {esc(legend)}</text>
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
    cx, cy, R = 215, 208, 128
    steps, period = 48, 30
    cats = list(TECH.items())
    order, idxs, remaining = [], [0] * len(cats), sum(len(v) for _, v in cats)
    ci = 0
    while remaining:
        k = ci % len(cats)
        cat, items = cats[k]
        if idxs[k] < len(items):
            order.append((cat, items[idxs[k]], TECH_COLORS[k]))
            idxs[k] += 1
            remaining -= 1
        ci += 1
    labels = []
    for i, (cat, label, color) in enumerate(order):
        frac = (i + 0.5) / len(order)
        lat = math.degrees(math.asin(1 - 2 * frac))
        lon0 = (i * 137.508) % 360
        xs, ys, fs, os_ = [], [], [], []
        for s in range(steps + 1):
            th, la = math.radians(lon0 + 360.0 * s / steps), math.radians(lat)
            z = math.cos(la) * math.cos(th)
            xs.append(f"{cx + R * math.cos(la) * math.sin(th):.1f}")
            ys.append(f"{cy - R * math.sin(la):.1f}")
            fs.append(f"{9.5 + 5.5 * (z + 1) / 2:.1f}")
            os_.append(f"{0.14 + 0.86 * max(0.0, (z + 1) / 2):.2f}")
        labels.append(
            f'<text x="{xs[0]}" y="{ys[0]}" text-anchor="middle" fill="{color}" font-weight="700" font-size="{fs[0]}">'
            f'<animate attributeName="x" values="{";".join(xs)}" dur="{period}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{";".join(ys)}" dur="{period}s" repeatCount="indefinite"/>'
            f'<animate attributeName="font-size" values="{";".join(fs)}" dur="{period}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{";".join(os_)}" dur="{period}s" repeatCount="indefinite"/>'
            f'{esc(label)}</text>')
    rings = []
    for j in range(5):
        vals = ";".join(f"{R * abs(math.sin(math.radians(360.0 * s / steps + j * 36))):.1f}"
                        for s in range(steps + 1))
        rings.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="{R}" fill="none" stroke="#2d3a4a" stroke-width="0.8" opacity="0.8">'
                     f'<animate attributeName="rx" values="{vals}" dur="{period}s" repeatCount="indefinite"/></ellipse>')
    for lat in (-40, 0, 40):
        rx = R * math.cos(math.radians(lat))
        rings.append(f'<ellipse cx="{cx}" cy="{cy - R * math.sin(math.radians(lat)):.1f}" rx="{rx:.1f}" '
                     f'ry="{rx * math.sin(math.radians(22)):.1f}" fill="none" stroke="#2d3a4a" stroke-width="0.8" opacity="0.8"/>')
    legend, total_w = [], 0
    widths = [len(c) * 6.4 + 24 for c in TECH]
    total_w = sum(widths) - 8
    lx = (W - total_w) / 2
    for k, cat in enumerate(TECH):
        legend.append(f'<circle cx="{lx + 3.5:.1f}" cy="374" r="3.5" fill="{TECH_COLORS[k]}"/>'
                      f'<text x="{lx + 10.5:.1f}" y="378" font-size="10.5" fill="{MUTED}">{esc(cat)}</text>')
        lx += widths[k]
    defs = f"""
<radialGradient id="core" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{PURPLE}" stop-opacity="0.18"/><stop offset="0.6" stop-color="{CYAN}" stop-opacity="0.05"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<style>.fin{{opacity:0;animation:fin 1s ease-out .3s forwards}}@keyframes fin{{to{{opacity:1}}}}</style>"""
    body = f"""
<text x="20" y="56" font-size="12" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ls ~/stack --3d</text>
<g class="fin">
<circle cx="{cx}" cy="{cy}" r="150" fill="url(#core)"/>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#2d3a4a"/>
{''.join(rings)}
{''.join(labels)}
{''.join(legend)}
</g>
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
    maxc = max((d["count"] for d in days), default=1) or 1
    OX, OY = 150.0, 88.0
    WX, WY, DX, DY = 11.2, 4.8, -11.2, 6.0
    LEVELS = {
        1: ("#1a6b3c", "#0f4a29", "#0a3520"),
        2: ("#26a641", "#177245", "#0e4d2e"),
        3: ("#39d353", "#27a844", "#1c7f33"),
        4: ("#69f0a0", "#3fce74", "#27a854"),
    }
    PEAK = ("#c9f7dc", "#69f0a0", "#39d353")
    towers = []
    for i, d in enumerate(days):
        w, wd = divmod(i, 7)
        towers.append((OY + w * WY + wd * DY, w, wd,
                       OX + w * WX + wd * DX, OY + w * WY + wd * DY, d))
    towers.sort(key=lambda t: (t[0], t[1], t[2]))
    parts, month_labels, seen_months = [], [], set()
    peak_pos = None
    for oi, (_, w, wd, cxp, cyp, d) in enumerate(towers):
        c = d["count"]
        delay = 0.3 + oi * 0.004
        title = f"<title>{c} contributions on {d['date']}</title>"
        if wd == 6:
            from datetime import date
            mon = date.fromisoformat(d["date"]).strftime("%b")
            key = date.fromisoformat(d["date"]).strftime("%Y-%m")
            if key not in seen_months:
                seen_months.add(key)
                lx, ly = OX + w * WX + 6 * DX + 2, OY + w * WY + 6 * DY + 47
                month_labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="10" fill="{MUTED}" transform="rotate(23.2 {lx:.1f} {ly:.1f})">{mon}</text>')
        if c == 0:
            parts.append(f'<g class="t" style="animation-delay:{delay:.2f}s"><polygon points="{cxp:.1f},{cyp - 4.3:.1f} {cxp + 9:.1f},{cyp - 0.5:.1f} {cxp:.1f},{cyp + 4.3:.1f} {cxp - 9:.1f},{cyp + 0.5:.1f}" fill="#1f2630"/>{title}</g>')
            continue
        h = 3 + math.sqrt(c / maxc) * 96
        ratio = c / maxc
        top_c, left_c, right_c = PEAK if c == maxc else LEVELS[
            1 if ratio <= 0.25 else 2 if ratio <= 0.5 else 3 if ratio <= 0.75 else 4]
        ty = cyp - h
        parts.append(
            f'<g class="b" style="animation-delay:{delay:.2f}s">'
            f'<polygon points="{cxp - 9:.1f},{ty + 0.5:.1f} {cxp:.1f},{ty + 4.3:.1f} {cxp:.1f},{cyp + 4.3:.1f} {cxp - 9:.1f},{cyp + 0.5:.1f}" fill="{left_c}"/>'
            f'<polygon points="{cxp + 9:.1f},{ty - 0.5:.1f} {cxp:.1f},{ty + 4.3:.1f} {cxp:.1f},{cyp + 4.3:.1f} {cxp + 9:.1f},{cyp - 0.5:.1f}" fill="{right_c}"/>'
            f'<polygon points="{cxp:.1f},{ty - 4.3:.1f} {cxp + 9:.1f},{ty - 0.5:.1f} {cxp:.1f},{ty + 4.3:.1f} {cxp - 9:.1f},{ty + 0.5:.1f}" fill="{top_c}"/>'
            f'{title}</g>')
        if c == maxc:
            peak_pos = (cxp, ty)
    beam, peak_label = "", ""
    if peak_pos:
        from datetime import date
        px, pty = peak_pos
        best = st.get("best_day", {})
        try:
            bdate = date.fromisoformat(best.get("date", "")).strftime("%b %d")
        except Exception:
            bdate = best.get("date", "")
        beam = f'<polygon points="{px - 3:.1f},{pty + 4:.1f} {px + 3:.1f},{pty + 4:.1f} {px + 1:.1f},{pty - 44:.1f} {px - 1:.1f},{pty - 44:.1f}" fill="url(#beam)"/>'
        peak_label = f'<text x="{px + 12:.1f}" y="{pty - 48:.1f}" font-size="11" fill="{ORANGE}">peak {best.get("count", 0)} · {esc(bdate)}</text>'
    def fmt_range(r):
        from datetime import date
        try:
            a = date.fromisoformat(r[0]).strftime("%b %Y")
            b = date.fromisoformat(r[1]).strftime("%b %Y")
            return f"{a} → {b}"
        except Exception:
            return ""
    stats_rows = [
        ("current streak", CYAN, f"{st.get('current_streak', 0)} days"),
        ("longest streak", PURPLE, f"{st.get('longest_streak', 0)} days"),
        ("active days", GREEN, f"{st.get('active_days', 0)} / {len(days)}"),
        ("busiest weekday", ORANGE, esc(st.get('busiest_weekday', '-'))),
    ]
    stats = "".join(
        f'<text x="36" y="{366 + k * 22}" font-size="12" fill="{MUTED}">{label}<tspan x="168" fill="{color}" font-weight="700">{val}</tspan></text>'
        for k, (label, color, val) in enumerate(stats_rows))
    defs = """
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#39d353" stop-opacity="0.16"/><stop offset="1" stop-color="#39d353" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffa657" stop-opacity="0.9"/><stop offset="1" stop-color="#ffa657" stop-opacity="0"/></linearGradient>
<linearGradient id="txt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#39d353"/><stop offset="1" stop-color="#58d5e8"/></linearGradient>
<style>.b{transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);animation:rise .9s cubic-bezier(.2,1.3,.4,1) forwards}@keyframes rise{to{transform:scaleY(1)}}.t,.fin{opacity:0;animation:fin .6s ease-out forwards}@keyframes fin{to{opacity:1}}</style>"""
    body = f"""
<text x="36" y="62" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ./skyline --user Ashutosh-Panda2004 --3d</text>
<ellipse cx="430" cy="240" rx="400" ry="180" fill="url(#glow)"/>
{''.join(parts)}
{''.join(month_labels)}
{beam}{peak_label}
<g class="fin" style="animation-delay:2.2s" text-anchor="end">
  <text x="824" y="98" font-size="44" font-weight="800" fill="url(#txt)">{st.get('total', 0):,}</text>
  <text x="824" y="120" font-size="13" fill="{FG}">contributions in the last year</text>
  <text x="824" y="139" font-size="11" fill="{MUTED}">{esc(fmt_range(st.get('range', [])))}</text>
</g>
<g class="fin" style="animation-delay:2.5s">{stats}</g>
"""
    write_svg("contrib-skyline.svg", window(W, H, "skyline.sh", body, defs))



# ---------------------------------------------------------------- heatmap
def heatmap_svg():
    W, H = 860, 270
    data = load("contributions.json", {})
    days, st = data.get("days", []), data.get("stats", {})
    cell, step = 12, 15.2
    x0, y0 = 42.8, 92
    cells, month_labels, seen = [], [], set()
    from datetime import date
    for i, d in enumerate(days):
        col, row = divmod(i, 7)
        x, y = x0 + col * step, y0 + row * step
        delay = (col + row) * 0.018
        cells.append(f'<rect class="cell" style="animation-delay:{delay:.3f}s" x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2.5" fill="{PALETTE[d["level"]]}"><title>{d["date"]}: {d["count"]}</title></rect>')
        dt = date.fromisoformat(d["date"])
        if row == 0 and dt.strftime("%Y-%m") not in seen:
            seen.add(dt.strftime("%Y-%m"))
            if not (col == 0 and dt.day != 1):
                month_labels.append(f'<text x="{x:.1f}" y="{y0 - 9}" font-size="11" fill="{MUTED}">{dt.strftime("%b")}</text>')
    weekdays = "".join(
        f'<text x="{x0 - 10}" y="{y0 + r * step + 10}" font-size="10" fill="{MUTED}" text-anchor="end">{label}</text>'
        for r, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")])
    legend = [f'<text x="707" y="{y0 + 7 * step + 24}" font-size="11" fill="{MUTED}" text-anchor="end">Less</text>']
    for i, c in enumerate(PALETTE[1:]):
        legend.append(f'<rect x="{715 + i * (cell + 3.2):.1f}" y="{y0 + 7 * step + 12}" width="{cell}" height="{cell}" rx="2.5" fill="{c}"/>')
    legend.append(f'<text x="809" y="{y0 + 7 * step + 24}" font-size="11" fill="{MUTED}">More</text>')
    best = st.get("best_day", {})
    groups = [
        (42.8, GREEN, f"{st.get('total', 0):,}", "contributions"),
        (202, CYAN, f"{st.get('current_streak', 0)}d", "current streak"),
        (368.4, PURPLE, f"{st.get('longest_streak', 0)}d", "longest streak"),
        (534.8, ORANGE, f"{best.get('count', 0)}", "best day"),
    ]
    stats = "".join(
        f'<text x="{gx}" y="250" font-size="15" font-weight="700" fill="{color}">{num}<tspan font-size="11" font-weight="400" fill="{MUTED}" dx="6">{label}</tspan></text>'
        for gx, color, num, label in groups)
    body = f"""
<text x="{x0}" y="58" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> git log --since="1 year ago" | heatmap</text>
{''.join(month_labels)}
{weekdays}
{''.join(cells)}
{''.join(legend)}
{stats}
"""
    defs = """<style>.cell{opacity:0;animation:cell .4s ease-out forwards}@keyframes cell{from{opacity:0}to{opacity:1}}</style>"""
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
    rows = [("Commits", commits, GREEN), ("Pull Requests", prs, CYAN),
            ("Issues + Reviews", issues_reviews, PURPLE)]
    other = max(total - sum(v for _, v, _ in rows), 0)
    cx, cy, r = 132, 176, 62
    circ = 2 * math.pi * r
    segs, cum = [], 0.0
    for val, color in [(commits, GREEN), (prs, CYAN), (issues_reviews, PURPLE),
                       (other, "#30363d")]:
        if val <= 0:
            continue
        frac = val / total
        segs.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="22" '
                    f'stroke-dasharray="{frac * circ:.1f} {circ:.1f}" transform="rotate({-90 + cum * 360:.1f} {cx} {cy})"/>')
        cum += frac
    row_svg = []
    for k, (label, val, color) in enumerate(rows):
        y = 118 + k * 52
        share = 100 * val / total
        row_svg.append(
            f'<text x="248" y="{y}" font-size="13" font-weight="700" fill="{color}">{esc(label)}</text>'
            f'<text x="382" y="{y}" font-size="15" font-weight="700" fill="{FG}">{val}<tspan font-size="11" font-weight="400" fill="{MUTED}"> / {total:,}</tspan></text>'
            f'<text x="548" y="{y}" font-size="11" fill="{MUTED}" text-anchor="end">share <tspan dx="4" fill="{color}" font-weight="700">{share:.1f}%</tspan></text>'
            f'<rect x="248" y="{y + 10}" width="300" height="6" rx="3" fill="#30363d"/>'
            f'<rect x="248" y="{y + 10}" width="0" height="6" rx="3" fill="{color}">'
            f'<animate attributeName="width" from="0" to="{300 * val / total:.1f}" begin="0.8s" dur="1s" fill="freeze"/></rect>')
    merged = gh.get("prs_merged", 0)
    opened = gh.get("prs_opened", 0) or 1
    weeks = _weeks(days)
    maxw = max((c for _, c in weeks), default=1) or 1
    bars, wlabels, seen = [], [], set()
    for i, (start, count) in enumerate(weeks):
        x = 36 + i * 14.86
        h = 3 + (count / maxw) * 49 if count else 2
        bars.append(f'<rect class="b" style="animation-delay:{0.4 + i * 0.02:.2f}s" x="{x:.1f}" y="{325 - h:.1f}" width="11" height="{h:.1f}" rx="1.5" fill="url(#barGrad)"><title>{count} contributions in the week of {start.isoformat()}</title></rect>')
        key = start.strftime("%Y-%m")
        if key not in seen:
            seen.add(key)
            if not (i == 0 and start.day != 1):
                wlabels.append(f'<text x="{x - 2:.1f}" y="337" font-size="10" fill="{MUTED}">{start.strftime("%b")}</text>')
    chips, chip_x = [], 46.0
    for name, count in act.get("repos", []):
        chips.append(f'<text x="{chip_x:.1f}" y="378" font-size="11" fill="{FG}">{esc(name)}<tspan dx="6" fill="{ORANGE}">{count}</tspan></text>')
        chip_x += len(name) * 6.6 + 6 + len(str(count)) * 6.6 + 26
    best = st.get("best_day", {})
    defs = """
<linearGradient id="ghGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#39d353"/><stop offset="1" stop-color="#58d5e8"/></linearGradient>
<linearGradient id="barGrad" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffa657"/><stop offset="1" stop-color="#ffc01e"/></linearGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#39d353" stop-opacity="0.12"/><stop offset="1" stop-color="#39d353" stop-opacity="0"/></radialGradient>
<style>.fin{opacity:0;animation:fin .6s ease-out forwards}@keyframes fin{to{opacity:1}}.b{transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);animation:rise .7s cubic-bezier(.2,1.3,.4,1) forwards}@keyframes rise{to{transform:scaleY(1)}}</style>"""
    body = f"""
<text x="36" y="62" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> github --user Ashutosh-Panda2004 --stats</text>
<text x="824" y="62" font-size="11" fill="{MUTED}" text-anchor="end">github.com/Ashutosh-Panda2004</text>
<g class="fin">
<circle cx="{cx}" cy="{cy}" r="86" fill="url(#halo)"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#21262d" stroke-width="22"/>
{''.join(segs)}
<text x="{cx}" y="{cy + 4}" font-size="34" font-weight="800" fill="{FG}" text-anchor="middle">{total:,}</text>
<text x="{cx}" y="{cy + 24}" font-size="11" fill="{MUTED}" text-anchor="middle">contributions</text>
{''.join(row_svg)}
<text x="610" y="106" font-size="11" fill="{MUTED}">merged pull requests</text>
<text x="610" y="146" font-size="40" font-weight="800" fill="url(#ghGrad)">{merged}</text>
<text x="610" y="170" font-size="12" fill="{FG}">{100 * merged / opened:.1f}% merge rate<tspan fill="{MUTED}">  ·  {opened} opened</tspan></text>
<text x="610" y="208" font-size="20" font-weight="800" fill="{ORANGE}">{st.get('current_streak', 0)}d<tspan font-size="11" font-weight="400" fill="{MUTED}" dx="6">current streak</tspan></text>
<text x="610" y="230" font-size="11" fill="{MUTED}">{st.get('longest_streak', 0)}d best  ·  {st.get('active_days', 0)} active days</text>
<text x="36" y="262" font-size="11" fill="{MUTED}">contributions per week  ·  <tspan fill="{FG}">{total:,}</tspan> in the last year  ·  busiest on {esc(st.get('busiest_weekday', '-'))}s</text>
{''.join(bars)}
{''.join(wlabels)}
{''.join(chips)}
<text x="824" y="378" font-size="11" fill="{ORANGE}" text-anchor="end">◆ best day · {best.get('count', 0)} contributions</text>
</g>
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


if __name__ == "__main__":
    main()

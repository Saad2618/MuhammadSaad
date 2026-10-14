#!/usr/bin/env python3
"""Generates the SVG banner art for the portfolio (hero + one per project).
Run:  python3 tools/make_banners.py   (from the project root)
Edit PROJECTS / PALETTES below to restyle everything at once."""
import random, os, re, json, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "images")

PALETTES = {  # accent -> (primary, secondary)
    "cyan":   ("#2DE2E6", "#4F7CFF"),
    "blue":   ("#6C9BFF", "#B18CFF"),
    "violet": ("#B18CFF", "#FF4D8D"),
    "teal":   ("#2DD4BF", "#B6F25C"),
    "amber":  ("#FFC857", "#FF7A45"),
    "rose":   ("#FF5C8A", "#FFB86B"),
}

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visuals
from projects_data import PROJECTS
def defs(uid, c1, c2, bg1="#0B0C24", bg2="#06071A"):
    return f'''<defs>
  <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient>
  <linearGradient id="ac{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
  <linearGradient id="bar{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}" stop-opacity=".55"/></linearGradient>
  <linearGradient id="glass{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity=".04"/></linearGradient>
  <radialGradient id="g1{uid}"><stop offset="0" stop-color="{c1}" stop-opacity=".85"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2{uid}"><stop offset="0" stop-color="{c2}" stop-opacity=".8"/><stop offset="1" stop-color="{c2}" stop-opacity="0"/></radialGradient>
  <filter id="blur{uid}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="soft{uid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="shadow{uid}" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="22" stdDeviation="20" flood-color="#000" flood-opacity=".5"/></filter>
  <pattern id="star{uid}" width="64" height="64" patternUnits="userSpaceOnUse">
    <path d="M32 6 L38 20 L52 14 L46 28 L60 32 L46 36 L52 50 L38 44 L32 58 L26 44 L12 50 L18 36 L4 32 L18 28 L12 14 L26 20 Z" fill="none" stroke="#fff" stroke-opacity=".09" stroke-width="1"/>
    <circle cx="32" cy="32" r="3" fill="#fff" fill-opacity=".08"/>
  </pattern>
  <radialGradient id="mask{uid}" cx=".5" cy=".5" r=".75"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
  <mask id="m{uid}"><rect width="100%" height="100%" fill="url(#mask{uid})"/></mask>
</defs>'''

def bars(u, x, y, n, w, gap, hmax, rng, hmin=0.25):
    out = []
    for i in range(n):
        h = hmax * (hmin + (1 - hmin) * rng.random())
        out.append(f'<rect x="{x + i*(w+gap)}" y="{y + hmax - h:.1f}" width="{w}" height="{h:.1f}" rx="6" fill="url(#bar{u})"/>')
    return "".join(out)

def line_chart(u, x, y, w, h, rng, n=9):
    pts = []
    for i in range(n):
        pts.append((x + i * w / (n - 1), y + h * (0.15 + 0.7 * rng.random())))
    d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return (f'<path d="{d}" fill="none" stroke="url(#ac{u})" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="url(#ac{u})" stroke-width="9" opacity=".25" filter="url(#soft{u})"/>'
            + "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4" fill="#0B0C24" stroke="url(#ac{u})" stroke-width="2.5"/>' for a, b in pts[1::2]))

def bar_row(x, y, w, h=8, op=.35, r=4):
    return visuals.bar(x, y, w, h, op, r)

def card(x, y, w, h, u, r=14, stroke=.14, fill=None):
    f = fill or f"url(#glass{u})"
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}" stroke="#fff" stroke-opacity="{stroke}"/>'

# ---- layouts, drawn in a 620 x 294 content box ------------------------------
def L_dashboard(u, rng):
    s = ""
    for i in range(5):
        w = rng.choice([58, 70, 78, 64])
        s += (f'<rect x="0" y="{10+i*28}" width="{w}" height="10" rx="5" fill="url(#ac{u})"/>' if i == 0
              else bar_row(0, 10 + i * 28, w, 10, .22, 5))
    for i in range(3):
        x = 116 + i * 172
        s += card(x, 0, 158, 66, u) + bar_row(x + 14, 14, 54, 6, .4) + bar_row(x + 14, 32, 92, 16, .9, 8)
        s += f'<rect x="{x+118}" y="14" width="26" height="6" rx="3" fill="url(#ac{u})"/>'
    s += card(116, 80, 504, 130, u)
    s += bars(u, 134, 94, 12, 28, 10, 100, rng)
    s += line_chart(u, 142, 100, 440, 90, rng)
    for i in range(2):
        s += card(116, 224 + i * 36, 504, 28, u, 9, .1) + bar_row(130, 234 + i * 36, rng.choice([180, 240, 290]), 8, .38) + f'<rect x="560" y="{233+i*36}" width="44" height="10" rx="5" fill="url(#ac{u})"/>'
    return s

def L_board(u, rng):
    s = ""
    for c in range(3):
        x = c * 210
        s += card(x, 0, 196, 294, u, 16, .12) + bar_row(x + 16, 16, 70, 9, .55) + f'<circle cx="{x+172}" cy="20" r="6" fill="url(#ac{u})"/>'
        y = 44
        for k in range(rng.choice([2, 3, 3, 4])):
            h = rng.choice([52, 64, 78])
            if y + h > 280: break
            hot = (c == 1 and k == 0)
            s += (f'<rect x="{x+12}" y="{y}" width="172" height="{h}" rx="11" fill="url(#ac{u})" fill-opacity=".22" stroke="url(#ac{u})" stroke-width="1.5"/>' if hot
                  else card(x + 12, y, 172, h, u, 11, .1))
            s += bar_row(x + 24, y + 14, 100, 8, .7) + bar_row(x + 24, y + 30, 138, 6, .28)
            if h > 60: s += f'<rect x="{x+24}" y="{y+h-20}" width="38" height="9" rx="4.5" fill="url(#ac{u})"/>'
            y += h + 10
    return s

def L_pipeline(u, rng):
    s = ""
    counts = [4, 3, 2, 1]
    for c in range(4):
        x = c * 158
        s += card(x, 0, 142, 294, u, 16, .12) + bar_row(x + 14, 16, 60, 9, .55)
        s += f'<rect x="{x+14}" y="32" width="{114-c*18}" height="5" rx="2.5" fill="url(#ac{u})"/>'
        y = 54
        for k in range(counts[c]):
            h = 50
            s += card(x + 10, y, 122, h, u, 10, .1) + bar_row(x + 20, y + 12, 70, 7, .65) + bar_row(x + 20, y + 28, 92, 6, .26)
            y += h + 10
        if c < 3: s += f'<path d="M{x+146} 147 l8 0 m-4 -4 l4 4 l-4 4" stroke="url(#ac{u})" stroke-width="2" fill="none" stroke-linecap="round"/>'
    return s

def L_kiosk(u, rng):
    s = card(110, 0, 400, 294, u, 22, .16)
    s += f'<rect x="130" y="16" width="360" height="40" rx="12" fill="url(#ac{u})" fill-opacity=".9"/>' + bar_row(148, 32, 120, 9, .9)
    for i in range(4):
        x = 130 + (i % 2) * 184; y = 70 + (i // 2) * 84
        s += card(x, y, 176, 76, u, 14, .14) + f'<circle cx="{x+34}" cy="{y+38}" r="17" fill="url(#ac{u})" fill-opacity="{.95 if i==0 else .55}"/>' + bar_row(x + 66, y + 28, 84, 9, .75) + bar_row(x + 66, y + 46, 58, 6, .3)
    s += f'<rect x="130" y="244" width="360" height="34" rx="17" fill="#fff" fill-opacity=".12" stroke="#fff" stroke-opacity=".2"/>' + bar_row(270, 258, 80, 8, .7)
    return s

def L_chat(u, rng):
    s = ""
    rows = [(False, 330), (True, 250), (False, 400), (True, 300)]
    y = 4
    for me, w in rows:
        x = 620 - w - 20 if me else 20
        h = 52
        s += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="url(#ac{u})" fill-opacity=".85"/>' if me else card(x, y, w, h, u, 18, .14))
        s += bar_row(x + 18, y + 16, w - 80, 8, .85 if me else .6) + bar_row(x + 18, y + 32, w - 140, 6, .5 if me else .28)
        y += h + 14
    s += card(20, 244, 580, 44, u, 22, .18) + bar_row(40, 262, 160, 8, .4) + f'<circle cx="570" cy="266" r="14" fill="url(#ac{u})"/>'
    s += f'<circle cx="64" cy="{y-2}" r="0"/>'
    return s

def L_doc(u, rng):
    s = f'<g transform="rotate(-3 150 150)"><rect x="20" y="0" width="240" height="294" rx="14" fill="#F6F4FF"/>'
    s += f'<rect x="40" y="22" width="90" height="12" rx="6" fill="#201A4A" fill-opacity=".85"/>'
    for i in range(9):
        w = rng.choice([180, 200, 150, 190, 120])
        s += f'<rect x="40" y="{54+i*24}" width="{w}" height="7" rx="3.5" fill="#201A4A" fill-opacity=".16"/>'
    for yy in (78, 150, 222):
        s += f'<rect x="38" y="{yy-5}" width="{rng.choice([110,140,90])}" height="17" rx="4" fill="url(#ac{u})" fill-opacity=".38"/>'
    s += "</g>"
    for i in range(5):
        y = 14 + i * 56
        s += f'<path d="M262 {[84,156,228,60,200][i]} C 300 {[84,156,228,60,200][i]}, 300 {y+22}, 340 {y+22}" fill="none" stroke="url(#ac{u})" stroke-width="2" stroke-opacity=".7" stroke-dasharray="5 5"/>'
        s += card(340, y, 280, 44, u, 12, .14) + bar_row(356, y + 12, 70, 6, .38) + bar_row(356, y + 25, rng.choice([120, 150, 180]), 9, .85)
        s += f'<circle cx="596" cy="{y+22}" r="8" fill="url(#ac{u})"/>'
    return s

def L_endpoints(u, rng):
    s = ""
    verbs = [("GET", "/api/events", "200"), ("POST", "/api/sync/run", "201"), ("GET", "/api/status", "200"), ("PUT", "/api/rules/7", "200"), ("GET", "/api/health", "200"), ("POST", "/api/hooks", "202")]
    for i, (v, p, c) in enumerate(verbs):
        y = i * 48
        s += card(0, y, 620, 40, u, 11, .12 if i != 1 else .35, f"url(#ac{u})" if False else None)
        s += f'<rect x="12" y="{y+9}" width="50" height="22" rx="7" fill="url(#ac{u})" fill-opacity="{.95 if v!="GET" else .35}"/>'
        s += f'<text x="37" y="{y+25}" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11.5" font-weight="700" fill="#fff">{v}</text>'
        s += f'<text x="78" y="{y+25}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13" fill="#fff" fill-opacity=".82">{p}</text>'
        s += bar_row(380, y + 16, rng.choice([90, 130, 160]), 7, .22)
        s += f'<text x="596" y="{y+25}" text-anchor="end" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="12.5" font-weight="700" fill="{PALETTES["teal"][0]}">{c}</text>'
    return s

LAYOUTS = dict(dashboard=L_dashboard, board=L_board, pipeline=L_pipeline, kiosk=L_kiosk, chat=L_chat, doc=L_doc, endpoints=L_endpoints)
LAYOUTS.update(visuals.EXTRA)

def window(u, layout, title, rng):
    s = f'<g filter="url(#shadow{u})"><rect width="660" height="372" rx="24" fill="#0E1030" fill-opacity=".72"/></g>'
    s += f'<rect width="660" height="372" rx="24" fill="url(#glass{u})" stroke="#fff" stroke-opacity=".18"/>'
    s += '<circle cx="28" cy="24" r="5" fill="#FF6B8B"/><circle cx="46" cy="24" r="5" fill="#FFC857"/><circle cx="64" cy="24" r="5" fill="#4ADE9A"/>'
    s += f'<text x="86" y="28" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif" font-size="12.5" fill="#fff" fill-opacity=".6">{title}</text>'
    s += '<line x1="0" y1="46" x2="660" y2="46" stroke="#fff" stroke-opacity=".1"/>'
    s += f'<g transform="translate(20 60)">{LAYOUTS[layout](u, rng)}</g>'
    return s

def project_banner(p, W, H):
    rng = random.Random(p["id"])
    u = re.sub(r"\W", "", p["id"])[:10] + str(W)
    c1, c2 = PALETTES[p["accent"]]
    visuals.PAL["c1"], visuals.PAL["c2"] = c1, c2
    visuals.set_ctx(p)
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{p["title"]} banner illustration">'
    s += defs(u, c1, c2)
    s += f'<rect width="{W}" height="{H}" fill="url(#bg{u})"/>'
    gx1, gy1 = rng.uniform(0.0, 0.35) * W, rng.uniform(0.0, 0.5) * H
    gx2, gy2 = rng.uniform(0.6, 1.0) * W, rng.uniform(0.5, 1.0) * H
    s += f'<circle cx="{gx1:.0f}" cy="{gy1:.0f}" r="{H*0.62:.0f}" fill="url(#g1{u})" opacity=".55" filter="url(#blur{u})"/>'
    s += f'<circle cx="{gx2:.0f}" cy="{gy2:.0f}" r="{H*0.7:.0f}" fill="url(#g2{u})" opacity=".5" filter="url(#blur{u})"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#star{u})" mask="url(#m{u})"/>'
    sc = min(W * 0.84 / 660, H * 0.78 / 372)
    tx, ty = (W - 660 * sc) / 2, (H - 372 * sc) / 2 + H * 0.02
    s += f'<g transform="translate({tx:.1f} {ty:.1f}) scale({sc:.3f}) rotate(-1.6 330 186)">{window(u, p["layout"], p["mockTitle"], rng)}</g>'
    # floating status chip
    cx, cy = W - 150 * (W/800 if W < 1000 else 1.3) , H - 62
    cx = tx + 660 * sc - 175 * sc; cy = ty + 372 * sc - 18 * sc
    s += (f'<g transform="translate({cx:.0f} {cy:.0f}) scale({sc:.3f})" filter="url(#shadow{u})"><rect width="190" height="54" rx="27" fill="#12143A" stroke="url(#ac{u})" stroke-opacity=".9"/>'
          f'<circle cx="28" cy="27" r="9" fill="url(#ac{u})"/><circle cx="28" cy="27" r="16" fill="url(#ac{u})" opacity=".25"/>'
          f'<text x="52" y="24" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif" font-size="12.5" font-weight="700" fill="#fff">{"Illustrative preview" if p["status"]=="professional" else "Concept preview"}</text>'
          f'<text x="52" y="40" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif" font-size="10.5" fill="#fff" fill-opacity=".6">Demo data only</text></g>')
    s += f'<rect x="0" y="{H-6}" width="{W}" height="6" fill="url(#ac{u})"/>'
    s += "</svg>"
    return s

# ---- hero banner: aurora + lattice + Riyadh-style skyline -------------------
def skyline(u, W, base):
    g = f'<g fill="#07081C">'
    x = 0
    rng = random.Random(7)
    # low filler blocks
    while x < W:
        w = rng.randint(34, 80); h = rng.randint(30, 120)
        g += f'<rect x="{x}" y="{base-h}" width="{w}" height="{h+200}"/>'
        x += w + rng.randint(0, 6)
    g += "</g>"
    # signature towers (stylised silhouettes, not exact replicas)
    def kingdom(cx, h):  # tall slab with a parabolic opening near the top
        top = base - h
        return (f'<path d="M{cx-46} {base+2} V{top+60} Q{cx-46} {top} {cx-16} {top} H{cx+16} Q{cx+46} {top} {cx+46} {top+60} V{base+2} Z" fill="#090A22"/>'
                f'<path d="M{cx-20} {top+8} Q{cx} {top+62} {cx+20} {top+8} Z" fill="#2a1a5e"/>'
                f'<path d="M{cx-46} {top+60} Q{cx-46} {top} {cx-16} {top}" stroke="url(#ac{u})" stroke-width="2" fill="none" opacity=".9"/>'
                f'<path d="M{cx+46} {top+60} Q{cx+46} {top} {cx+16} {top}" stroke="url(#ac{u})" stroke-width="2" fill="none" opacity=".9"/>')
    def faisaliah(cx, h):  # tapering shaft with a sphere
        top = base - h
        return (f'<path d="M{cx-30} {base+2} L{cx-8} {top+34} H{cx+8} L{cx+30} {base+2} Z" fill="#090A22"/>'
                f'<circle cx="{cx}" cy="{top+26}" r="22" fill="#0C0D2B" stroke="url(#ac{u})" stroke-width="2"/>'
                f'<path d="M{cx} {top-34} V{top+4}" stroke="url(#ac{u})" stroke-width="3"/>'
                f'<path d="M{cx-30} {base+2} L{cx-8} {top+34}" stroke="url(#ac{u})" stroke-width="1.5" opacity=".6"/>'
                f'<path d="M{cx+30} {base+2} L{cx+8} {top+34}" stroke="url(#ac{u})" stroke-width="1.5" opacity=".6"/>')
    def tower(cx, w, h):
        top = base - h
        win = "".join(f'<rect x="{cx-w//2+6}" y="{top+14+i*16}" width="{w-12}" height="2" fill="#fff" fill-opacity=".08"/>' for i in range(h // 16))
        return f'<rect x="{cx-w//2}" y="{top}" width="{w}" height="{h+4}" fill="#090A22"/><rect x="{cx-w//2}" y="{top}" width="{w}" height="3" fill="url(#ac{u})" opacity=".9"/>{win}'
    g += tower(int(W*0.50), 70, 230) + tower(int(W*0.60), 56, 300) + faisaliah(int(W*0.68), 360) + tower(int(W*0.76), 60, 210)
    g += kingdom(int(W*0.86), 440) + tower(int(W*0.95), 66, 250) + tower(int(W*0.43), 58, 180) + tower(int(W*0.36), 80, 140)
    # lit windows
    lit = random.Random(3)
    for _ in range(90):
        wx = lit.randint(int(W*0.34), W - 10); wy = lit.randint(base - 300, base - 14)
        g += f'<rect x="{wx}" y="{wy}" width="3" height="3" fill="#FFC857" fill-opacity="{lit.uniform(.25,.8):.2f}"/>'
    return g

def _off():
    visuals.CTX['on'] = False

def hero_banner(W=1920, H=1000):
    u = "hero"
    c1, c2 = "#8B6CFF", "#FF4D8D"
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Abstract night skyline with aurora light and geometric lattice">'
    s += defs(u, c1, c2, "#0C0B2C", "#05061A")
    s += f'<rect width="{W}" height="{H}" fill="url(#bg{u})"/>'
    s += f'<circle cx="{W*0.78:.0f}" cy="{H*0.18:.0f}" r="560" fill="url(#g1{u})" opacity=".62" filter="url(#blur{u})"/>'
    s += f'<circle cx="{W*0.95:.0f}" cy="{H*0.62:.0f}" r="520" fill="url(#g2{u})" opacity=".5" filter="url(#blur{u})"/>'
    s += f'<circle cx="{W*0.12:.0f}" cy="{H*0.1:.0f}" r="420" fill="#2DE2E6" opacity=".16" filter="url(#blur{u})"/>'
    s += f'<circle cx="{W*0.55:.0f}" cy="{H*0.92:.0f}" r="480" fill="#FFC857" opacity=".22" filter="url(#blur{u})"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#star{u})" mask="url(#m{u})" opacity="1"/>'
    # crescent moon (masked so it stays a true crescent on any background)
    mx, my = W*0.5, H*0.15
    s += f'<mask id="moon"><rect width="{W}" height="{H}" fill="#000"/><circle cx="{mx:.0f}" cy="{my:.0f}" r="46" fill="#fff"/><circle cx="{mx+22:.0f}" cy="{my-12:.0f}" r="40" fill="#000"/></mask>'
    s += f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="90" fill="#FFE9B8" opacity=".12" filter="url(#blur{u})"/><rect width="{W}" height="{H}" fill="#FFE9B8" mask="url(#moon)"/>'
    rng = random.Random(11)
    for _ in range(70):
        s += f'<circle cx="{rng.randint(0,W)}" cy="{rng.randint(0,int(H*0.55))}" r="{rng.choice([1,1,1.5,2])}" fill="#fff" opacity="{rng.uniform(.2,.8):.2f}"/>'
    s += skyline(u, W, H - 150)
    s += f'<rect y="{H-150}" width="{W}" height="150" fill="#07081C"/>'
    s += f'<rect y="{H-152}" width="{W}" height="3" fill="url(#ac{u})"/>'
    s += f'<rect y="{H-150}" width="{W}" height="150" fill="url(#bg{u})" opacity="0"/>'
    s += "</svg>"
    return s


# ---- extra section banners ----------------------------------------------------
def _inside(pt, poly):
    x, y = pt; n = len(poly); c = False; j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi: c = not c
        j = i
    return c

LAND = [
    [(-168,66),(-140,70),(-95,72),(-60,62),(-55,48),(-70,42),(-80,26),(-97,18),(-108,24),(-125,40),(-125,50),(-150,60)],
    [(-80,10),(-60,10),(-35,-6),(-40,-22),(-58,-38),(-68,-55),(-75,-40),(-72,-18),(-80,-4)],
    [(-10,36),(0,44),(-5,50),(5,58),(25,70),(40,68),(40,50),(30,42),(20,38),(5,37)],
    [(-17,21),(-5,36),(10,37),(32,31),(43,12),(51,11),(40,-15),(33,-27),(20,-35),(12,-18),(9,4),(-8,5),(-17,14)],
    [(40,68),(60,75),(100,78),(140,72),(170,66),(142,50),(122,30),(122,22),(108,10),(100,2),(92,22),(78,8),(72,20),(58,24),(56,26),(52,16),(43,12),(35,30),(36,34),(40,50)],
    [(114,-22),(130,-12),(142,-11),(153,-26),(146,-39),(130,-32),(115,-34)],
]
CITIES = [("London", -0.1, 51.5), ("Dubai", 55.3, 25.3), ("Karachi", 67.0, 24.9), ("New York", -74.0, 40.7), ("Singapore", 103.8, 1.3), ("Sydney", 151.2, -33.9)]
RIYADH = (46.7, 24.7)

def global_banner(W=1920, H=640):
    u = "glob"; c1, c2 = "#8B6CFF", "#FF4D8D"
    sx = W / 360.0; sy = H / 124.0
    X = lambda lon: (lon + 180) * sx
    Y = lambda lat: (72 - lat) * sy
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Dotted world map with connections from Riyadh to cities around the world">'
    s += defs(u, c1, c2, "#0C0B2C", "#05061A")
    s += f'<rect width="{W}" height="{H}" fill="url(#bg{u})"/>'
    s += f'<circle cx="{X(46.7):.0f}" cy="{Y(24.7):.0f}" r="520" fill="url(#g1{u})" opacity=".5" filter="url(#blur{u})"/><circle cx="{W*0.1:.0f}" cy="{H*0.9:.0f}" r="420" fill="url(#g2{u})" opacity=".4" filter="url(#blur{u})"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#star{u})" mask="url(#m{u})" opacity=".7"/>'
    lon = -170.0
    while lon < 180:
        lat = 72.0
        while lat > -52:
            if any(_inside((lon, lat), poly) for poly in LAND):
                d = ((lon - RIYADH[0]) ** 2 + (lat - RIYADH[1]) ** 2) ** .5
                op = .55 if d < 22 else .26
                s += f'<circle cx="{X(lon):.1f}" cy="{Y(lat):.1f}" r="2.4" fill="#fff" fill-opacity="{op}"/>'
            lat -= 3
        lon += 3
    rx, ry = X(RIYADH[0]), Y(RIYADH[1])
    for name, lo, la in CITIES:
        x, y = X(lo), Y(la)
        mx, my = (rx + x) / 2, min(ry, y) - (abs(x - rx) ** 2 + abs(y - ry) ** 2) ** .5 * .32
        s += f'<path d="M{rx:.0f} {ry:.0f} Q{mx:.0f} {my:.0f} {x:.0f} {y:.0f}" fill="none" stroke="url(#ac{u})" stroke-width="2.4" stroke-opacity=".9" stroke-linecap="round"/>'
        s += f'<path d="M{rx:.0f} {ry:.0f} Q{mx:.0f} {my:.0f} {x:.0f} {y:.0f}" fill="none" stroke="url(#ac{u})" stroke-width="8" stroke-opacity=".22" filter="url(#soft{u})"/>'
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="#FFC857" fill-opacity=".2"/><circle cx="{x:.0f}" cy="{y:.0f}" r="5.5" fill="#FFC857"/>'
        s += f'<text x="{x+12:.0f}" y="{y+22:.0f}" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif" font-size="15" font-weight="600" fill="#fff" fill-opacity=".85">{name}</text>'
    s += f'<circle cx="{rx:.0f}" cy="{ry:.0f}" r="44" fill="url(#ac{u})" opacity=".25"/><circle cx="{rx:.0f}" cy="{ry:.0f}" r="24" fill="none" stroke="url(#ac{u})" stroke-width="3"/><circle cx="{rx:.0f}" cy="{ry:.0f}" r="9" fill="#fff"/>'
    s += f'<text x="{rx+16:.0f}" y="{ry-20:.0f}" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif" font-size="19" font-weight="800" fill="#fff">Riyadh</text>'
    return s + "</svg>"

def stack_banner(W=1600, H=720):
    u = "stk"; c1, c2 = "#8B6CFF", "#2DE2E6"
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Abstract orbits and glowing nodes">'
    s += defs(u, c1, c2, "#0D0B31", "#06071C")
    s += f'<rect width="{W}" height="{H}" fill="url(#bg{u})"/>'
    s += f'<circle cx="{W*0.78:.0f}" cy="{H*0.45:.0f}" r="520" fill="url(#g1{u})" opacity=".55" filter="url(#blur{u})"/><circle cx="{W*0.1:.0f}" cy="{H*0.9:.0f}" r="420" fill="url(#g2{u})" opacity=".45" filter="url(#blur{u})"/><circle cx="{W*0.95:.0f}" cy="{H*0.95:.0f}" r="360" fill="#FF4D8D" opacity=".28" filter="url(#blur{u})"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#star{u})" mask="url(#m{u})" opacity=".8"/>'
    cx, cy = W * 0.74, H * 0.5
    rng = random.Random(21)
    for i, rad in enumerate((120, 200, 290, 390, 500, 620)):
        s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rad}" fill="none" stroke="#fff" stroke-opacity="{.16-i*.017:.3f}" stroke-width="1.5"/>'
        a0 = rng.uniform(0, 6.28)
        s += f'<circle cx="{cx+rad*math.cos(a0):.0f}" cy="{cy+rad*math.sin(a0):.0f}" r="{6-i*.5:.1f}" fill="url(#ac{u})"/><circle cx="{cx+rad*math.cos(a0):.0f}" cy="{cy+rad*math.sin(a0):.0f}" r="{16-i}" fill="url(#ac{u})" opacity=".22"/>'
        a1 = a0 + 3.3
        s += f'<circle cx="{cx+rad*math.cos(a1):.0f}" cy="{cy+rad*math.sin(a1):.0f}" r="4" fill="#FFC857"/>'
        s += f'<path d="M{cx+rad*math.cos(a0+.2):.0f} {cy+rad*math.sin(a0+.2):.0f} A{rad} {rad} 0 0 1 {cx+rad*math.cos(a0+1.3):.0f} {cy+rad*math.sin(a0+1.3):.0f}" fill="none" stroke="url(#ac{u})" stroke-width="3" stroke-linecap="round" opacity=".8"/>'
    s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="64" fill="url(#ac{u})" opacity=".3"/><circle cx="{cx:.0f}" cy="{cy:.0f}" r="34" fill="url(#ac{u})"/>'
    for _ in range(50): s += f'<circle cx="{rng.randint(0,W)}" cy="{rng.randint(0,H)}" r="{rng.choice([1,1,1.5])}" fill="#fff" opacity="{rng.uniform(.15,.6):.2f}"/>'
    return s + "</svg>"

def cta_banner(W=1920, H=560):
    u = "cta"; c1, c2 = "#8B6CFF", "#FF4D8D"
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Abstract glowing orbs and light arcs">'
    s += defs(u, c1, c2, "#120B35", "#070720")
    s += f'<rect width="{W}" height="{H}" fill="url(#bg{u})"/>'
    s += f'<circle cx="{W*0.12:.0f}" cy="{H*0.2:.0f}" r="460" fill="url(#g1{u})" opacity=".7" filter="url(#blur{u})"/><circle cx="{W*0.82:.0f}" cy="{H*0.7:.0f}" r="520" fill="url(#g2{u})" opacity=".65" filter="url(#blur{u})"/><circle cx="{W*0.55:.0f}" cy="{H*0.05:.0f}" r="300" fill="#FFC857" opacity=".2" filter="url(#blur{u})"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#star{u})" mask="url(#m{u})"/>'
    for i in range(9):
        r0 = 180 + i * 58
        s += f'<circle cx="{W*0.86:.0f}" cy="{H*0.62:.0f}" r="{r0}" fill="none" stroke="#fff" stroke-opacity="{.2-i*.02:.3f}" stroke-width="1.6"/>'
    s += f'<path d="M{W*0.62:.0f} {H} C {W*0.72:.0f} {H*0.55:.0f}, {W*0.85:.0f} {H*0.5:.0f}, {W} {H*0.18:.0f}" fill="none" stroke="url(#ac{u})" stroke-width="4" stroke-linecap="round"/><path d="M{W*0.62:.0f} {H} C {W*0.72:.0f} {H*0.55:.0f}, {W*0.85:.0f} {H*0.5:.0f}, {W} {H*0.18:.0f}" fill="none" stroke="url(#ac{u})" stroke-width="14" opacity=".25" filter="url(#soft{u})"/>'
    rng = random.Random(5)
    for _ in range(40):
        x, y = rng.randint(int(W*0.45), W), rng.randint(0, H)
        s += f'<path d="M{x} {y-7} L{x+2} {y-2} L{x+7} {y} L{x+2} {y+2} L{x} {y+7} L{x-2} {y+2} L{x-7} {y} L{x-2} {y-2}Z" fill="#fff" fill-opacity="{rng.uniform(.2,.7):.2f}"/>'
    return s + "</svg>"

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)

if __name__ == "__main__":
    write(os.path.join(OUT, "hero-banner.svg"), hero_banner())
    write(os.path.join(OUT, "banner-global.svg"), global_banner())
    write(os.path.join(OUT, "banner-stack.svg"), stack_banner())
    write(os.path.join(OUT, "banner-cta.svg"), cta_banner())
    for p in PROJECTS:
        write(os.path.join(OUT, "projects", p["id"] + ".svg"), project_banner(p, 800, 500))
        write(os.path.join(OUT, "projects", p["id"] + "-wide.svg"), project_banner(p, 1600, 640))
    print("projects:", len(PROJECTS))

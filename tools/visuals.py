"""Bespoke banner illustrations, one drawing per project type.
Each drawer paints a 620 x 294 box. `u` is a unique id suffix, `r` a seeded Random,
and PAL holds the project's two accent colours."""
import math
PAL = {"c1": "#fff", "c2": "#fff"}
MONO = "ui-monospace,Menlo,Consolas,monospace"
SANS = "Inter,Segoe UI,Helvetica,Arial,sans-serif"

def A(u): return f"url(#ac{u})"
def card(x, y, w, h, u, r=14, stroke=.14, fill=None):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or f"url(#glass{u})"}" stroke="#fff" stroke-opacity="{stroke}"/>'
import random as _random, html as _html
CTX = {"on": False}
NAMES = ["Sara Al-Qahtani", "Omar Khan", "Lina Haddad", "Yusuf Malik", "Noor Siddiqui", "Faisal Rahman", "Aisha Noor", "Hassan Ali", "Mariam Saeed", "Ahmed Raza", "Rania Youssef", "Bilal Ahmed"]
STATUS = ["Active", "Approved", "Open", "New", "Done", "Draft", "Pending", "Paid", "Review", "Live"]
LABELS = ["Status", "Owner", "Updated", "Priority", "Amount", "Date", "Team", "Region", "Type", "Due", "Name", "Ref", "Branch", "Role"]
SECOND = ["Updated 2h ago", "Riyadh", "Jeddah", "Dammam", "Due Sunday", "Updated today", "Ref #2048", "Team A", "In review", "Draft saved", "Muhammad S.", "Created Mon", "3 attachments", "Head office"]

def set_ctx(p):
    import re as _re
    raw = [_html.unescape(x) for x in (list(p.get("functionality") or []) + list(p.get("features") or []))]
    bank = []
    for t in raw + [p["title"], p["mockTitle"], p["type"]]:
        t = _re.sub(r"<[^>]+>", "", t).strip().rstrip(".")
        bank.append(t)
        for part in _re.split(r",| and | with | for | from | to |, ", t):
            part = part.strip()
            if 6 <= len(part) < len(t): bank.append(part[0].upper() + part[1:])
    CTX.update(on=True, rng=_random.Random(p["id"]), bank=sorted(set(bank), key=len), used=[])

def _pick(n):
    """a phrase from the project's own vocabulary, close to n characters"""
    r = CTX["rng"]; cands = [b for b in CTX["bank"] if len(b) <= n]
    if not cands: 
        b = r.choice(CTX["bank"]); cut = b[:n]; sp = cut.rfind(" ")
        return cut[:sp] if sp > n * .5 else cut
    used = CTX.setdefault("used", [])
    fresh = [c for c in cands if c not in used[-8:]] or cands
    top = fresh[-5:] if len(fresh) > 5 else fresh
    pick = r.choice(top); used.append(pick)
    return pick

def _num():
    r = CTX["rng"]; k = r.randint(0, 3)
    return [f"{r.randint(12, 980)}", f"SAR {r.randint(2, 90)},{r.randint(100, 999)}", f"{r.randint(3, 48)}", f"{r.randint(2, 9)}.{r.randint(0, 9)}k"][k]

def _txt(x, y, w, h, s, fs, op, weight=600, fill="#fff", anchor="start"):
    s = _html.escape(s, quote=False); ax = x if anchor == "start" else x + w / 2
    nat = max(8, len(s) * fs * .56)
    return (f'<text x="{ax}" y="{y + h/2 + fs*.34:.1f}" text-anchor="{anchor}" font-family="{SANS}" font-size="{fs:.1f}" font-weight="{weight}" fill="{fill}" fill-opacity="{op}" '
            f'stroke="#0B0C24" stroke-opacity=".3" stroke-width="2" paint-order="stroke" textLength="{min(w, nat):.0f}" lengthAdjust="spacingAndGlyphs">{s}</text>')

def bar(x, y, w, h=8, op=.35, r=None):
    if CTX["on"] and h >= 5.5 and w >= 22 and op < 1:
        rng = CTX["rng"]
        if h >= 13 and op >= .8:
            t = _num(); fs = h * 1.05; return _txt(x, y, w, h, t, fs, .95, 800)
        if w < 44:
            t = rng.choice([_num(), rng.choice(STATUS), f"{rng.randint(1,28)} Oct"]); fs = max(8, h * 1.25)
            if len(t) * fs * .56 > w: t = t[:max(2, int(w / (fs * .56)))]
            return _txt(x, y, w, h, t, fs, .8 if op >= .6 else .55)
        fs = max(8.5, h * 1.3); n = max(4, int(w / (fs * .56)))
        if op >= .6: t = rng.choice(NAMES) if rng.random() < .4 and n >= 9 else _pick(n); wt, o = 650, .92
        elif op >= .4: t = rng.choice(LABELS); wt, o = 600, .6; fs *= .88
        else: t = rng.choice(SECOND) if rng.random() < .6 else _pick(n); wt, o = 500, .5
        if len(t) > n: cut = t[:n]; sp = cut.rfind(" "); t = cut[:sp] if sp > n * .5 else cut
        return _txt(x, y, w, h, t, fs, o, wt)
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r if r is not None else h/2}" fill="#fff" fill-opacity="{op}"/>'
def chip(x, y, w, u, h=12, op=1):
    base = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{A(u)}" fill-opacity="{op}"/>'
    if CTX["on"] and w >= 30 and h >= 12:
        fs = min(h * .62, 11); t = CTX["rng"].choice(STATUS)
        if len(t) * fs * .58 > w - 8: t = t[:max(2, int((w - 8) / (fs * .58)))]
        base += (f'<text x="{x + w/2}" y="{y + h/2 + fs*.34:.1f}" text-anchor="middle" font-family="{SANS}" font-size="{fs:.1f}" font-weight="700" '
                 f'fill="{"#0B0C24" if op >= .7 else "#fff"}" fill-opacity="{.82 if op >= .7 else .85}">{t}</text>')
    return base
def dot(cx, cy, r, u, op=1): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{A(u)}" fill-opacity="{op}"/>'
def ring(cx, cy, r, u, w=3, op=1): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{A(u)}" stroke-width="{w}" stroke-opacity="{op}"/>'
def avatar(cx, cy, r, u, op=.9):
    if CTX["on"] and r >= 9:
        nm = CTX["rng"].choice(NAMES).split(); ini = (nm[0][0] + nm[-1][0]).upper()
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{A(u)}" fill-opacity="{op}"/>'
                f'<text x="{cx}" y="{cy + r*.34:.1f}" text-anchor="middle" font-family="{SANS}" font-size="{r*.88:.1f}" font-weight="800" fill="#0B0C24" fill-opacity=".72">{ini}</text>')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{A(u)}" fill-opacity="{op}"/>'
            f'<circle cx="{cx}" cy="{cy-r*.2:.1f}" r="{r*.32:.1f}" fill="#0B0C24" fill-opacity=".55"/>'
            f'<path d="M{cx-r*.55:.1f} {cy+r*.7:.1f} q{r*.55:.1f} -{r*.7:.1f} {r*1.1:.1f} 0" fill="#0B0C24" fill-opacity=".55"/>')
def T(x, y, s, size=11, op=.8, anchor="start", weight=600, mono=False, fill="#fff"):
    ff = MONO if mono else SANS
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{ff}" font-size="{size}" font-weight="{weight}" fill="{fill}" fill-opacity="{op}">{s}</text>'
def line(x1, y1, x2, y2, u, w=2, op=.8, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{A(u)}" stroke-width="{w}" stroke-opacity="{op}" fill="none" stroke-linecap="round"{d}/>'
def sparkle(cx, cy, s, u, op=1):
    return f'<path d="M{cx} {cy-s} Q{cx} {cy} {cx+s} {cy} Q{cx} {cy} {cx} {cy+s} Q{cx} {cy} {cx-s} {cy} Q{cx} {cy} {cx} {cy-s}Z" fill="{A(u)}" fill-opacity="{op}"/>'
def area(u, x, y, w, h, r, n=8):
    pts = [(x + i * w / (n - 1), y + h * (0.12 + 0.72 * r.random())) for i in range(n)]
    d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return (f'<path d="{d} L{x+w},{y+h} L{x},{y+h} Z" fill="url(#bar{u})" fill-opacity=".45"/>'
            f'<path d="{d}" fill="none" stroke="{A(u)}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{A(u)}" stroke-width="9" opacity=".22" filter="url(#soft{u})"/>')
def bars(u, x, y, n, w, gap, hmax, r, hmin=.25):
    o = ""
    for i in range(n):
        h = hmax * (hmin + (1 - hmin) * r.random())
        o += f'<rect x="{x+i*(w+gap)}" y="{y+hmax-h:.1f}" width="{w}" height="{h:.1f}" rx="5" fill="url(#bar{u})"/>'
    return o
def donut(u, cx, cy, rad, parts, w=16):
    o = f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="#fff" stroke-opacity=".1" stroke-width="{w}"/>'
    circ = 2 * math.pi * rad; off = 0
    for i, p in enumerate(parts):
        col = A(u) if i % 2 == 0 else PAL["c2"]
        o += f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{col}" stroke-width="{w}" stroke-dasharray="{circ*p-4:.1f} {circ:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 {cx} {cy})" stroke-linecap="round" stroke-opacity="{.95 if i%2==0 else .8}"/>'
        off += circ * p
    return o
def cols(u, x, y, n, w, gap, h):  # kanban frames
    return "".join(card(x + i * (w + gap), y, w, h, u, 14, .12) for i in range(n))

# ---------------------------------------------------------------- drawers ---
def iam(u, r):
    s = f'<g transform="translate(0 8)"><path d="M85 8 L160 38 V120 C160 180 125 220 85 240 C45 220 10 180 10 120 V38 Z" fill="url(#glass{u})" stroke="{A(u)}" stroke-width="2.5"/>'
    s += f'<path d="M85 40 L135 60 V120 C135 158 112 186 85 200 C58 186 35 158 35 120 V60 Z" fill="{A(u)}" fill-opacity=".18"/>'
    s += f'<path d="M62 118 L80 136 L112 98" stroke="{A(u)}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
    for i in range(5): s += bar(250 + i * 74, 14, 46, 7, .4)
    for row in range(5):
        y = 40 + row * 50
        s += card(190, y, 430, 40, u, 11, .1) + avatar(214, y + 20, 11, u) + bar(236, y + 12, 50, 7, .7) + bar(236, y + 24, 34, 5, .3)
        for c in range(5):
            on = r.random() > .42
            s += (dot(273 + c * 74, y + 20, 8, u) if on else f'<circle cx="{273+c*74}" cy="{y+20}" r="8" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="2"/>')
    return s

def profiles(u, r):
    s = ""
    for i in range(5):
        y = i * 58
        s += (f'<rect x="0" y="{y}" width="226" height="50" rx="13" fill="{A(u)}" fill-opacity=".2" stroke="{A(u)}" stroke-width="1.6"/>' if i == 1 else card(0, y, 226, 50, u, 13, .1))
        s += avatar(28, y + 25, 15, u, .9 if i == 1 else .55) + bar(54, y + 14, 90, 8, .8) + bar(54, y + 29, 120, 6, .3)
    s += card(246, 0, 374, 294, u, 18, .14) + avatar(298, 56, 30, u) + bar(344, 38, 130, 11, .85) + bar(344, 58, 90, 7, .35) + chip(530, 40, 62, u, 18)
    for i in range(6):
        x = 268 + (i % 2) * 176; y = 112 + (i // 2) * 46
        s += bar(x, y, 52, 6, .35) + card(x, y + 12, 160, 26, u, 8, .16)
        s += bar(x + 10, y + 21, rr(r, 60, 110), 7, .6)
    s += chip(268, 254, 96, u, 28, 1) + card(376, 254, 84, 28, u, 14, .22)
    return s
def rr(r, a, b): return r.randint(a, b)

def policy(u, r):
    s = ""
    for i in range(3):
        x = i * 210
        s += card(x, 0, 196, 132, u, 16, .14) + f'<circle cx="{x+34}" cy="38" r="20" fill="{A(u)}" fill-opacity=".9"/>'
        s += f'<path d="M{x+22} 42 a12 12 0 0 1 24 0 Z M{x+34} 42 v12" stroke="#0B0C24" stroke-width="3" fill="none" stroke-linecap="round"/>'
        s += bar(x + 66, 26, 100, 9, .8) + bar(x + 66, 44, 70, 6, .3) + bar(x + 18, 80, 150, 6, .25) + bar(x + 18, 96, 110, 6, .25) + chip(x + 18, 110, 60, u, 12)
    s += card(0, 150, 620, 144, u, 16, .12) + line(40, 214, 580, 214, u, 3, .35)
    for i in range(5):
        x = 40 + i * 135
        s += (dot(x, 214, 11, u) if i < 3 else f'<circle cx="{x}" cy="214" r="10" fill="#0B0C24" stroke="#fff" stroke-opacity=".3" stroke-width="2.5"/>')
        s += bar(x - 30, 242, 60, 7, .5 if i < 3 else .22) + bar(x - 22, 174, 44, 6, .3)
    s += line(40, 214, 40 + 3 * 135, 214, u, 4, 1)
    return s

def metro(u, r):
    c2 = PAL["c2"]
    s = card(0, 0, 400, 294, u, 18, .12)
    for gx in range(30, 400, 40): s += f'<path d="M{gx} 0 V294" stroke="#fff" stroke-opacity=".04"/>'
    s += f'<path d="M24 242 L124 242 L204 162 L330 162 L376 96" fill="none" stroke="{A(u)}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="M36 64 L140 64 L204 162 L268 242 L376 242" fill="none" stroke="{c2}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    for x, y in [(24, 242), (124, 242), (330, 162), (376, 96), (36, 64), (140, 64), (268, 242), (376, 242)]:
        s += f'<circle cx="{x}" cy="{y}" r="8" fill="#0B0C24" stroke="#fff" stroke-width="3"/>'
    s += f'<circle cx="204" cy="162" r="14" fill="#fff"/><circle cx="204" cy="162" r="8" fill="#0B0C24"/>'
    s += card(150, 14, 120, 34, u, 10, .2) + dot(168, 31, 7, u) + bar(182, 24, 70, 7, .8) + bar(182, 35, 44, 5, .3)
    s += card(424, 0, 196, 294, u, 22, .22, "#0E1030") + card(438, 14, 168, 266, u, 14, .1, "#0B0C24")
    s += f'<rect x="450" y="26" width="144" height="40" rx="10" fill="{A(u)}"/>' + bar(464, 42, 70, 8, .9)
    for i in range(3):
        y = 80 + i * 56
        s += card(450, y, 144, 46, u, 10, .16) + dot(474, y + 23, 11, u, .9 if i == 0 else .5) + bar(494, y + 14, 80, 8, .75) + bar(494, y + 28, 50, 5, .3)
    s += f'<rect x="450" y="248" width="144" height="22" rx="11" fill="#fff" fill-opacity=".14"/>' + bar(496, 256, 52, 6, .7)
    return s

def cases(u, r):
    s = card(0, 0, 424, 294, u, 16, .12)
    s += bar(18, 16, 40, 7, .5) + bar(110, 16, 70, 7, .5) + bar(250, 16, 50, 7, .5) + bar(350, 16, 40, 7, .5) + '<path d="M0 36 H424" stroke="#fff" stroke-opacity=".12"/>'
    for i in range(6):
        y = 46 + i * 41
        hot = i == 2
        if hot: s += f'<rect x="8" y="{y-4}" width="408" height="36" rx="10" fill="{A(u)}" fill-opacity=".2" stroke="{A(u)}" stroke-width="1.3"/>'
        s += chip(18, y + 6, 46, u, 14, .9 if hot else .5) + bar(110, y + 8, rr(r, 80, 120), 8, .7) + avatar(274, y + 13, 10, u, .7)
        s += f'<rect x="346" y="{y+4}" width="58" height="18" rx="9" fill="{A(u) if i%3!=1 else "#fff"}" fill-opacity="{.85 if i%3!=1 else .18}"/>'
    s += card(444, 0, 176, 294, u, 16, .12) + bar(462, 18, 70, 8, .6)
    s += line(472, 56, 472, 262, u, 3, .35)
    for i in range(5):
        y = 56 + i * 52
        s += dot(472, y, 7, u, 1 if i < 4 else .35) + bar(490, y - 8, 100, 7, .7) + bar(490, y + 6, 66, 5, .28)
    return s

def ai_chat_sources(u, r):
    s = card(0, 0, 396, 294, u, 18, .12)
    s += f'<rect x="150" y="16" width="226" height="40" rx="16" fill="{A(u)}" fill-opacity=".85"/>' + bar(168, 30, 170, 8, .9) + bar(168, 43, 90, 5, .5)
    s += dot(30, 94, 14, u) + sparkle(30, 94, 7, u) .replace(A(u), "#0B0C24")
    s += card(52, 72, 316, 112, u, 16, .16)
    for i, w in enumerate([270, 250, 280, 180]): s += bar(68, 88 + i * 17, w - 40, 7, .7 if i < 3 else .5)
    s += chip(68, 160, 34, u, 16) + chip(110, 160, 34, u, 16, .7) + chip(152, 160, 34, u, 16, .5)
    s += card(14, 232, 368, 44, u, 22, .18) + bar(34, 250, 150, 8, .4) + dot(354, 254, 13, u)
    s += bar(14, 202, 60, 6, .25)
    for i in range(3):
        y = i * 98
        s += card(414, y, 206, 88, u, 14, .14 if i != 0 else .4) + f'<rect x="428" y="{y+12}" width="26" height="34" rx="4" fill="#F6F4FF" fill-opacity=".9"/>' + bar(466, y + 14, 120, 8, .7) + bar(466, y + 30, 80, 5, .3)
        s += bar(428, y + 58, 170, 5, .25) + f'<rect x="428" y="{y+68}" width="{rr(r,70,130)}" height="8" rx="3" fill="{A(u)}" fill-opacity=".45"/>'
    for yy in (50, 148, 246): s += f'<path d="M368 {yy-34 if yy==50 else 128} C 392 128, 400 {yy-10}, 412 {yy-10}" fill="none" stroke="{A(u)}" stroke-width="1.5" stroke-dasharray="4 4" stroke-opacity=".6"/>' if yy == 50 else ""
    return s

def billing(u, r):
    s = ""
    for i, w in enumerate((200, 200, 200)):
        x = i * 210
        s += card(x, 0, w, 70, u, 14) + bar(x + 14, 14, 56, 6, .4) + bar(x + 14, 34, 96, 16, .9, 8) + chip(x + 150, 14, 36, u, 12)
    s += card(0, 84, 410, 210, u, 16) + area(u, 22, 104, 366, 150, r, 9) + bar(22, 272, 366, 4, .12)
    s += card(430, 84, 190, 210, u, 16) + bar(446, 100, 70, 7, .5)
    for i in range(5):
        y = 122 + i * 34
        s += avatar(456, y + 12, 10, u, .6) + bar(476, y + 4, 70, 7, .65) + bar(476, y + 17, 44, 5, .25) + f'<rect x="570" y="{y+6}" width="36" height="14" rx="7" fill="{A(u) if i%2==0 else "#fff"}" fill-opacity="{.85 if i%2==0 else .18}"/>'
    return s

def warehouse(u, r):
    s = card(0, 0, 400, 294, u, 18, .12)
    for row in range(3):
        y = 24 + row * 90
        s += f'<rect x="16" y="{y+66}" width="368" height="6" rx="3" fill="#fff" fill-opacity=".3"/>'
        x = 22
        while x < 360:
            w = r.choice([40, 52, 62, 46]); h = r.choice([40, 50, 58])
            hot = (row == 1 and 150 < x < 230)
            s += f'<rect x="{x}" y="{y+66-h}" width="{w}" height="{h}" rx="5" fill="{A(u) if hot else "#fff"}" fill-opacity="{.9 if hot else r.choice([.1,.16,.22])}" stroke="#fff" stroke-opacity=".18"/>'
            s += f'<path d="M{x} {y+66-h+12} H{x+w}" stroke="#fff" stroke-opacity=".25"/>'
            x += w + 8
    s += card(420, 0, 200, 190, u, 16) + bar(436, 16, 70, 7, .5)
    for i in range(4):
        y = 40 + i * 36
        s += bar(436, y, 60, 6, .4) + f'<rect x="436" y="{y+12}" width="168" height="9" rx="4.5" fill="#fff" fill-opacity=".12"/><rect x="436" y="{y+12}" width="{rr(r,50,150)}" height="9" rx="4.5" fill="{A(u)}"/>'
    s += card(420, 204, 200, 90, u, 16) + "".join(f'<rect x="{438+i*6}" y="224" width="{rr(r,2,4)}" height="42" fill="#fff" fill-opacity=".8"/>' for i in range(26)) + chip(540, 252, 62, u, 18)
    return s

def calendar(u, r):
    s = card(0, 0, 410, 294, u, 16)
    for i in range(7): s += bar(20 + i * 54, 16, 30, 6, .4)
    for row in range(5):
        for c in range(7):
            s += f'<rect x="{14+c*54}" y="{38+row*50}" width="48" height="44" rx="8" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".08"/>'
    for (row, c, span) in [(0, 1, 3), (1, 4, 2), (2, 0, 4), (3, 3, 3), (3, 0, 2)]:
        s += f'<rect x="{18+c*54}" y="{50+row*50}" width="{span*54-10}" height="20" rx="10" fill="{A(u)}" fill-opacity="{r.choice([.95,.7,.55])}"/>' + bar(28 + c * 54, 57 + row * 50, 40, 6, .85)
    s += card(430, 0, 190, 294, u, 16) + bar(446, 16, 80, 8, .6)
    for i in range(3):
        y = 40 + i * 84
        s += card(444, y, 162, 74, u, 12, .12) + avatar(466, y + 22, 11, u) + bar(486, y + 14, 80, 7, .75) + bar(486, y + 28, 50, 5, .3)
        s += chip(456, y + 48, 68, u, 18) + f'<rect x="532" y="{y+48}" width="64" height="18" rx="9" fill="#fff" fill-opacity=".14"/>'
    return s

def school(u, r):
    s = card(0, 0, 380, 294, u, 16) + "".join(bar(70 + i * 60, 18, 40, 6, .45) for i in range(5))
    for rw in range(5):
        y = 40 + rw * 50
        s += bar(14, y + 16, 40, 7, .5)
        for c in range(5):
            on = r.random() > .35
            s += f'<rect x="{62+c*60}" y="{y}" width="54" height="42" rx="9" fill="{A(u) if on else "#fff"}" fill-opacity="{r.choice([.9,.6,.4]) if on else .06}"/>'
            if on: s += bar(70 + c * 60, y + 14, 34, 6, .8) + bar(70 + c * 60, y + 26, 22, 5, .4)
    s += card(400, 0, 220, 150, u, 16) + donut(u, 466, 76, 40, [.46, .3, .24], 14) + bar(526, 52, 70, 8, .7) + bar(526, 70, 50, 6, .3) + bar(526, 94, 60, 8, .7) + bar(526, 112, 40, 6, .3)
    for i in range(3):
        y = 162 + i * 44
        s += card(400, y, 220, 38, u, 11, .12) + avatar(422, y + 19, 11, u, .7) + bar(442, y + 11, 80, 7, .7) + bar(442, y + 23, 50, 5, .28) + chip(566, y + 11, 40, u, 16)
    return s

def booking(u, r):
    s = ""
    for i in range(3):
        y = i * 98
        sel = i == 1
        s += (f'<rect x="0" y="{y}" width="210" height="88" rx="16" fill="{A(u)}" fill-opacity=".2" stroke="{A(u)}" stroke-width="1.6"/>' if sel else card(0, y, 210, 88, u, 16, .12))
        s += dot(36, y + 44, 20, u, .95 if sel else .5) + bar(68, y + 28, 110, 9, .8) + bar(68, y + 46, 80, 6, .3) + bar(68, y + 60, 50, 6, .45)
    s += card(230, 0, 390, 294, u, 18) + "".join(f'<rect x="{248+i*54}" y="18" width="46" height="46" rx="12" fill="{A(u) if i==2 else "#fff"}" fill-opacity="{.95 if i==2 else .08}"/>' + bar(260 + i * 54, 30, 22, 6, .8 if i == 2 else .45) + bar(264 + i * 54, 44, 14, 8, .9 if i == 2 else .5) for i in range(7))
    for i in range(12):
        x = 248 + (i % 4) * 92; y = 86 + (i // 4) * 52
        sel = i == 6
        s += f'<rect x="{x}" y="{y}" width="82" height="40" rx="11" fill="{A(u) if sel else "#fff"}" fill-opacity="{.95 if sel else .07}" stroke="#fff" stroke-opacity=".12"/>' + bar(x + 20, y + 16, 42, 8, .9 if sel else .45)
    s += chip(248, 252, 130, u, 28) + bar(266, 262, 90, 8, .9).replace('fill="#fff" fill-opacity=".9"', 'fill="#0B0C24" fill-opacity=".6"')
    return s

def store(u, r):
    s = card(0, 0, 620, 294, u, 18, .16, "#0E1030") + '<path d="M0 36 H620" stroke="#fff" stroke-opacity=".1"/>'
    s += dot(26, 18, 8, u) + bar(44, 14, 60, 8, .8) + "".join(bar(220 + i * 56, 15, 38, 6, .4) for i in range(4))
    s += f'<g transform="translate(572 8)"><path d="M0 4 H5 L9 16 H22 L25 8 H7" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="11" cy="21" r="2" fill="#fff"/><circle cx="20" cy="21" r="2" fill="#fff"/><circle cx="26" cy="2" r="7" fill="{A(u)}"/></g>'
    s += f'<rect x="14" y="48" width="592" height="82" rx="16" fill="{A(u)}" fill-opacity=".85"/>' + bar(36, 68, 200, 14, .95) + bar(36, 92, 140, 7, .6) + f'<rect x="36" y="108" width="74" height="14" rx="7" fill="#0B0C24" fill-opacity=".55"/>'
    s += f'<circle cx="520" cy="86" r="52" fill="#fff" fill-opacity=".16"/><circle cx="548" cy="70" r="30" fill="#fff" fill-opacity=".18"/>'
    for i in range(4):
        x = 14 + i * 150
        s += card(x, 144, 140, 140, u, 14, .14) + f'<rect x="{x+8}" y="152" width="124" height="64" rx="10" fill="{A(u)}" fill-opacity="{r.choice([.55,.4,.7,.3])}"/>'
        s += f'<circle cx="{x+70}" cy="184" r="{rr(r,14,22)}" fill="#fff" fill-opacity=".28"/>' + bar(x + 12, 226, 90, 7, .75) + bar(x + 12, 241, 56, 7, .9) + f'<circle cx="{x+118}" cy="260" r="10" fill="{A(u)}"/>'
    return s

def referral(u, r):
    s = card(0, 0, 400, 294, u, 18, .12)
    cx, cy = 200, 150
    mids = [(90, 70), (310, 70), (200, 240)]
    for mx, my in mids: s += line(cx, cy, mx, my, u, 2.5, .6)
    leaves = [(30, 30), (150, 24), (260, 28), (370, 38), (350, 140), (30, 150), (100, 250), (300, 250)]
    for i, (lx, ly) in enumerate(leaves):
        mx, my = min(mids, key=lambda m: (m[0] - lx) ** 2 + (m[1] - ly) ** 2)
        s += line(mx, my, lx, ly, u, 1.8, .4, "4 4") + dot(lx, ly, 9, u, .6) 
    for mx, my in mids: s += f'<circle cx="{mx}" cy="{my}" r="20" fill="#0B0C24" stroke="{A(u)}" stroke-width="3"/>' + avatar(mx, my, 12, u)
    s += f'<circle cx="{cx}" cy="{cy}" r="38" fill="{A(u)}" fill-opacity=".25"/><circle cx="{cx}" cy="{cy}" r="28" fill="{A(u)}"/>' + T(cx, cy + 7, "%", 22, .9, "middle", 800).replace('fill="#fff"', 'fill="#0B0C24"')
    s += card(420, 0, 200, 294, u, 16) + bar(436, 16, 80, 8, .6) + bar(436, 40, 60, 6, .3)
    s += bars(u, 440, 70, 6, 20, 8, 110, r) + '<path d="M436 188 H604" stroke="#fff" stroke-opacity=".15"/>'
    for i in range(3): s += avatar(450, 214 + i * 24, 8, u, .7) + bar(466, 209 + i * 24, 70, 7, .65) + chip(556, 208 + i * 24, 40, u, 12)
    return s

def feed(u, r):
    s = card(0, 0, 200, 294, u, 18, .12)
    for rad in (90, 66, 42): s += f'<circle cx="100" cy="132" r="{rad}" fill="none" stroke="{A(u)}" stroke-opacity="{.15 if rad==90 else .3 if rad==66 else .55}" stroke-width="2"/>'
    s += f'<path d="M100 98 c-22 0 -34 16 -34 38 v18 l-10 12 h88 l-10 -12 v-18 c0 -22 -12 -38 -34 -38z" fill="{A(u)}"/><circle cx="100" cy="182" r="9" fill="{A(u)}"/><circle cx="132" cy="102" r="12" fill="#FF4D6D" stroke="#0B0C24" stroke-width="3"/>'
    s += chip(46, 236, 108, u, 28, .9) + bar(66, 246, 68, 8, .9).replace('fill="#fff" fill-opacity=".9"', 'fill="#0B0C24" fill-opacity=".6"')
    for i in range(5):
        y = i * 59
        new = i == 0
        s += (f'<rect x="220" y="{y}" width="400" height="52" rx="13" fill="{A(u)}" fill-opacity=".2" stroke="{A(u)}" stroke-width="1.5"/>' if new else card(220, y, 400, 52, u, 13, .1))
        s += dot(244, y + 26, 11, u, .95 if new else .45) + bar(268, y + 14, rr(r, 150, 250), 8, .8) + bar(268, y + 30, rr(r, 90, 170), 6, .3) + bar(560, y + 20, 40, 7, .3)
    return s

def analytics(u, r):
    s = ""
    for i in range(4):
        x = i * 158
        s += card(x, 0, 146, 60, u, 13) + bar(x + 12, 12, 46, 6, .4) + bar(x + 12, 30, 70, 14, .9, 7) + chip(x + 104, 14, 30, u, 10)
    s += card(0, 74, 250, 220, u, 16) + donut(u, 125, 168, 56, [.4, .27, .2, .13], 20) + bar(86, 156, 78, 12, .8, 6) + bar(100, 176, 50, 6, .35)
    s += "".join(dot(26 + i * 60, 262, 5, u, 1 if i % 2 == 0 else .5) + bar(36 + i * 60, 259, 30, 6, .35) for i in range(4))
    s += card(266, 74, 354, 220, u, 16) + area(u, 286, 98, 314, 120, r, 10) + bars(u, 286, 232, 14, 14, 8, 40, r, .2)
    return s

def modernize(u, r):
    s = ""
    # legacy monolith
    for i in range(5):
        y = 20 + i * 52
        s += f'<rect x="{rr(r,0,10)}" y="{y}" width="{rr(r,186,214)}" height="42" rx="3" fill="#fff" fill-opacity=".07" stroke="#fff" stroke-opacity=".3" stroke-dasharray="6 4"/>' + bar(18, y + 16, rr(r, 70, 120), 7, .3) 
    s += T(105, 288, "LEGACY", 11, .5, "middle", 700, True)
    for i in range(3):
        x = 236 + i * 30
        s += f'<path d="M{x} 130 l22 17 l-22 17" stroke="{A(u)}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="{.4+i*.3}"/>'
    # new layered architecture
    s += card(344, 0, 276, 294, u, 18, .2)
    for i, h in enumerate((54, 90, 54)):
        y = [14, 76, 178][i]
        s += f'<rect x="360" y="{y}" width="244" height="{h}" rx="12" fill="{A(u)}" fill-opacity="{.28+i*.0 if i!=1 else .16}" stroke="{A(u)}" stroke-opacity=".7"/>'
    s += bar(376, 30, 90, 8, .8) + bar(376, 46, 60, 5, .35)
    for i in range(3): s += card(374 + i * 78, 96, 66, 56, u, 10, .2) + dot(407 + i * 78, 114, 8, u) + bar(386 + i * 78, 134, 42, 5, .55)
    s += bar(376, 194, 90, 8, .8) + bar(376, 210, 60, 5, .35) + chip(530, 202, 60, u, 20)
    s += f'<g transform="translate(360 242)"><rect width="244" height="40" rx="10" fill="#fff" fill-opacity=".07" stroke="#fff" stroke-opacity=".15"/>{"".join(dot(30+i*40,20,9,u,.9) for i in range(6))}</g>'
    return s

def vault(u, r):
    s = card(0, 0, 190, 294, u, 16)
    for i, (ind, w) in enumerate([(0, 90), (1, 80), (1, 70), (2, 100), (1, 90), (0, 80), (1, 70)]):
        y = 16 + i * 38
        s += f'<path d="M{16+ind*18} {y+4} h10 l3 4 h14 v16 h-27z" fill="{A(u)}" fill-opacity="{.9 if i==3 else .45}"/>' + bar(58 + ind * 18, y + 10, w - ind * 12, 7, .7 if i == 3 else .4)
    s += card(206, 0, 250, 294, u, 16) + bar(222, 16, 80, 7, .5)
    for i in range(6):
        y = 40 + i * 42
        s += f'<rect x="222" y="{y}" width="26" height="32" rx="4" fill="#F6F4FF" fill-opacity=".85"/>' + bar(260, y + 6, 110, 7, .75) + bar(260, y + 19, 70, 5, .28) 
        s += (f'<g transform="translate(414 {y+6})"><rect y="8" width="20" height="14" rx="3" fill="{A(u)}"/><path d="M4 8 v-3 a6 6 0 0 1 12 0 v3" stroke="{A(u)}" stroke-width="3" fill="none"/></g>' if i % 2 == 0 else chip(414, y + 9, 24, u, 12, .4))
    s += card(472, 0, 148, 294, u, 16, .2) + f'<path d="M546 24 L586 40 V90 C586 118 566 134 546 142 C526 134 506 118 506 90 V40Z" fill="{A(u)}" fill-opacity=".25" stroke="{A(u)}" stroke-width="2.5"/><path d="M530 84 l12 12 l22 -26" stroke="{A(u)}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    for i in range(4):
        y = 166 + i * 30
        s += bar(488, y + 4, 62, 7, .6) + f'<rect x="574" y="{y}" width="32" height="16" rx="8" fill="{A(u) if i!=2 else "#fff"}" fill-opacity="{.9 if i!=2 else .2}"/><circle cx="{598 if i!=2 else 582}" cy="{y+8}" r="6" fill="#fff"/>'
    return s

def tenants(u, r):
    s = ""
    for i in range(6):
        x = (i % 3) * 210; y = (i // 3) * 138
        hot = i == 1
        s += f'<rect x="{x}" y="{y}" width="196" height="124" rx="18" fill="{A(u) if hot else "#fff"}" fill-opacity="{.16 if hot else .04}" stroke="{A(u)}" stroke-opacity="{.9 if hot else .45}" stroke-dasharray="{"" if hot else "7 5"}" stroke-width="{2 if hot else 1.4}"/>'
        s += f'<circle cx="{x+34}" cy="{y+34}" r="18" fill="{A(u)}" fill-opacity="{.95 if hot else .6}"/>' + bar(x + 62, y + 24, 90, 9, .8) + bar(x + 62, y + 40, 60, 6, .3)
        s += card(x + 14, y + 66, 168, 44, u, 10, .12) + bar(x + 24, y + 76, 50, 5, .3) + f'<rect x="{x+24}" y="{y+90}" width="148" height="8" rx="4" fill="#fff" fill-opacity=".12"/><rect x="{x+24}" y="{y+90}" width="{rr(r,40,130)}" height="8" rx="4" fill="{A(u)}"/>'
    s += card(220, 276, 180, 18, u, 9, .2) if False else ""
    return s

def recon(u, r):
    s = card(0, 0, 220, 294, u, 16) + card(400, 0, 220, 294, u, 16) + bar(16, 14, 80, 7, .5) + bar(416, 14, 80, 7, .5)
    ys = [44 + i * 48 for i in range(5)]
    for i, y in enumerate(ys):
        bad = i == 3
        s += card(12, y, 196, 38, u, 10, .14) + bar(24, y + 10, rr(r, 70, 120), 7, .7) + bar(24, y + 23, 44, 5, .3)
        s += card(412, y, 196, 38, u, 10, .14) + bar(424, y + 10, rr(r, 70, 120), 7, .7) + bar(424, y + 23, 44, 5, .3)
        if bad: s += f'<path d="M208 {y+19} L412 {y+19+0}" stroke="#FF6B8B" stroke-width="2" stroke-dasharray="6 5" fill="none"/><rect x="278" y="{y+6}" width="64" height="26" rx="13" fill="#FF6B8B"/>' + bar(292, y + 16, 36, 6, .95).replace('fill="#fff"', 'fill="#0B0C24"')
        else:
            tgt = ys[(i + (1 if i == 4 else 0)) % 5] if False else y
            s += f'<path d="M208 {y+19} C 280 {y+19}, 340 {tgt+19}, 412 {tgt+19}" stroke="{A(u)}" stroke-width="2.5" fill="none"/>' + dot(310, y + 19, 6, u)
    s += card(12, 292 - 0, 0, 0, u) if False else ""
    s += f'<rect x="12" y="278" width="596" height="10" rx="5" fill="#fff" fill-opacity=".12"/><rect x="12" y="278" width="470" height="10" rx="5" fill="{A(u)}"/>'
    return s

def chatbot(u, r):
    s = card(0, 0, 620, 294, u, 18, .12, "#0E1030") + '<path d="M0 34 H620" stroke="#fff" stroke-opacity=".1"/>' + dot(22, 17, 7, u) + bar(38, 13, 50, 8, .7) + "".join(bar(380 + i * 56, 14, 40, 6, .35) for i in range(4))
    s += bar(28, 60, 250, 18, .75) + bar(28, 90, 190, 18, .5) + bar(28, 122, 160, 8, .3) + bar(28, 138, 130, 8, .3) + chip(28, 164, 92, u, 26)
    for i in range(3): s += card(28 + i * 118, 210, 108, 70, u, 12, .12) + dot(50 + i * 118, 232, 9, u, .6) + bar(40 + i * 118, 252, 70, 6, .35)
    s += card(366, 36, 236, 232, u, 18, .3, "#12143A") + f'<path d="M366 54 a18 18 0 0 1 18 -18 h200 a18 18 0 0 1 18 18 v30 h-236z" fill="{A(u)}"/>' + avatar(392, 60, 14, u).replace(A(u), "#fff") + bar(416, 52, 80, 8, .95) + bar(416, 66, 50, 5, .6)
    s += f'<rect x="382" y="100" width="150" height="34" rx="14" fill="#fff" fill-opacity=".1"/>' + bar(394, 112, 110, 7, .7) + f'<rect x="438" y="144" width="148" height="34" rx="14" fill="{A(u)}" fill-opacity=".9"/>' + bar(452, 156, 100, 7, .95)
    s += f'<rect x="382" y="188" width="116" height="34" rx="14" fill="#fff" fill-opacity=".1"/>' + "".join(dot(404 + i * 14, 205, 3.5, u, .5 + i * .25) for i in range(3))
    s += card(380, 232, 208, 26, u, 13, .2) + bar(394, 242, 90, 6, .4) + dot(574, 245, 8, u)
    return s

def support(u, r):
    s = card(0, 0, 250, 294, u, 16)
    for i in range(6):
        y = 12 + i * 46
        hot = i == 1
        if hot: s += f'<rect x="8" y="{y-4}" width="234" height="42" rx="11" fill="{A(u)}" fill-opacity=".2" stroke="{A(u)}" stroke-width="1.4"/>'
        s += f'<circle cx="26" cy="{y+16}" r="6" fill="{["#FF6B8B","#FFC857","#4ADE9A"][i%3]}"/>' + bar(44, y + 8, rr(r, 100, 170), 8, .75) + bar(44, y + 22, rr(r, 60, 110), 5, .3) + bar(206, y + 12, 26, 6, .3)
    s += card(266, 0, 354, 120, u, 16) + avatar(296, 34, 14, u) + bar(320, 24, 100, 8, .8) + bar(320, 38, 60, 5, .3)
    for i, w in enumerate((300, 270, 190)): s += bar(284, 66 + i * 16, w, 7, .45)
    s += f'<rect x="266" y="132" width="354" height="102" rx="16" fill="{A(u)}" fill-opacity=".14" stroke="{A(u)}" stroke-width="1.6"/>' + sparkle(290, 156, 9, u) + bar(308, 150, 110, 8, .9)
    for i, w in enumerate((310, 290, 230)): s += bar(284, 176 + i * 16, w, 7, .6)
    s += chip(284, 214 + 0, 0, u, 0) if False else ""
    s += chip(266, 248, 110, u, 32) + card(388, 248, 90, 32, u, 16, .22) + f'<path d="M520 276 a38 38 0 0 1 76 0" fill="none" stroke="#fff" stroke-opacity=".15" stroke-width="10" stroke-linecap="round"/><path d="M520 276 a38 38 0 0 1 56 -33" fill="none" stroke="{A(u)}" stroke-width="10" stroke-linecap="round"/>'
    return s

def docqa(u, r):
    s = f'<g transform="rotate(-2 120 150)"><rect x="8" y="0" width="250" height="294" rx="14" fill="#F6F4FF"/><rect x="28" y="22" width="100" height="12" rx="6" fill="#201A4A" fill-opacity=".85"/>'
    for i in range(10):
        s += f'<rect x="28" y="{52+i*24}" width="{rr(r,140,208)}" height="7" rx="3.5" fill="#201A4A" fill-opacity=".16"/>'
    for yy in (100, 172): s += f'<rect x="24" y="{yy-4}" width="212" height="16" rx="4" fill="{A(u)}" fill-opacity=".4"/>'
    s += "</g>"
    s += card(280, 0, 340, 56, u, 14) + f'<rect x="294" y="14" width="28" height="28" rx="8" fill="{A(u)}" fill-opacity=".9"/>' + bar(334, 22, 130, 8, .7) + chip(540, 20, 62, u, 16, .8)
    s += f'<rect x="372" y="72" width="248" height="38" rx="15" fill="{A(u)}" fill-opacity=".85"/>' + bar(388, 87, 190, 8, .95)
    s += card(280, 124, 340, 138, u, 16, .22) + sparkle(306, 150, 9, u)
    for i, w in enumerate((290, 270, 300, 150)): s += bar(298, 166 + i * 18, w - 20, 7, .65)
    s += chip(298, 240, 52, u, 16) + chip(358, 240, 52, u, 16, .6)
    s += card(280, 272, 340, 22, u, 11, .2)
    return s

def aiinsight(u, r):
    s = card(0, 0, 380, 294, u, 16) + bars(u, 22, 150, 11, 22, 10, 100, r, .3) + area(u, 22, 34, 336, 110, r, 9)
    s += f'<circle cx="214" cy="78" r="12" fill="none" stroke="#FFC857" stroke-width="3"/><circle cx="214" cy="78" r="22" fill="#FFC857" fill-opacity=".18"/>' + card(228, 28, 112, 36, u, 10, .3, "#12143A") + sparkle(244, 46, 7, u) + bar(258, 42, 66, 7, .8)
    s += bar(22, 268, 120, 6, .3)
    s += card(398, 0, 222, 294, u, 16, .16) + sparkle(420, 24, 8, u) + bar(436, 18, 80, 8, .8)
    for i in range(3):
        y = 44 + i * 70
        s += f'<rect x="410" y="{y}" width="198" height="62" rx="12" fill="{A(u)}" fill-opacity="{.2 if i==0 else .07}" stroke="{A(u)}" stroke-opacity="{.8 if i==0 else .25}"/>' + bar(424, y + 12, 130, 8, .8) + bar(424, y + 28, 160, 5, .35) + bar(424, y + 40, 110, 5, .35) + chip(560, y + 12, 34, u, 12, .8)
    s += bar(414, 262, 190, 6, .45) + bar(414, 276, 140, 6, .3)
    return s

def kbsearch(u, r):
    s = card(0, 0, 620, 46, u, 23, .3) + f'<circle cx="28" cy="23" r="9" fill="none" stroke="#fff" stroke-width="3" stroke-opacity=".8"/><path d="M35 30 l8 8" stroke="#fff" stroke-width="3" stroke-opacity=".8" stroke-linecap="round"/>' + bar(58, 18, 220, 9, .6) + chip(540, 12, 66, u, 22)
    s += "".join(chip(14 + i * 82, 60, 72, u, 18, .65 if i else 1) for i in range(5))
    s += f'<rect x="0" y="94" width="620" height="92" rx="16" fill="{A(u)}" fill-opacity=".14" stroke="{A(u)}" stroke-width="1.6"/>' + sparkle(26, 118, 9, u)
    for i, w in enumerate((560, 520, 340)): s += bar(48 if i == 0 else 20, 112 + i * 20 if i else 112, w if i else 300, 7, .75 if i == 0 else .55) if i == 0 else bar(20, 112 + i * 20 + 8, w, 7, .6)
    s += chip(20, 164, 56, u, 14) + chip(84, 164, 56, u, 14, .6)
    for i in range(3):
        y = 198 + i * 32
        s += card(0, y, 620, 26, u, 9, .1) + f'<rect x="12" y="{y+5}" width="14" height="16" rx="3" fill="#F6F4FF" fill-opacity=".8"/>' + bar(38, y + 9, rr(r, 160, 300), 7, .7) + f'<rect x="470" y="{y+9}" width="136" height="8" rx="4" fill="#fff" fill-opacity=".12"/><rect x="470" y="{y+9}" width="{[118,90,64][i]}" height="8" rx="4" fill="{A(u)}"/>'
    return s

def resume(u, r):
    s = f'<g transform="rotate(-2.5 120 150)"><rect x="6" y="0" width="210" height="294" rx="12" fill="#F6F4FF"/><circle cx="46" cy="40" r="20" fill="{A(u)}"/><rect x="76" y="28" width="100" height="10" rx="5" fill="#201A4A" fill-opacity=".85"/><rect x="76" y="46" width="70" height="7" rx="3.5" fill="#201A4A" fill-opacity=".3"/>'
    for sec in range(3):
        y0 = 84 + sec * 70
        s += f'<rect x="22" y="{y0}" width="64" height="9" rx="4.5" fill="{A(u)}"/>'
        for l in range(3): s += f'<rect x="22" y="{y0+18+l*14}" width="{rr(r,120,170)}" height="6" rx="3" fill="#201A4A" fill-opacity=".16"/>'
    s += "</g>"
    s += card(240, 0, 200, 150, u, 16) + bar(256, 14, 70, 7, .5)
    xs = [(256, 38, 56), (320, 38, 70), (256, 64, 44), (308, 64, 62), (256, 90, 74), (336, 90, 52), (256, 116, 60)]
    for i, (x, y, w) in enumerate(xs): s += f'<rect x="{x}" y="{y}" width="{w}" height="20" rx="10" fill="{A(u) if i not in (3,6) else "#fff"}" fill-opacity="{.85 if i not in (3,6) else .1}" stroke="{A(u) if i in (3,6) else "none"}" stroke-dasharray="4 3"/>'
    s += card(460, 0, 160, 150, u, 16) + f'<circle cx="540" cy="80" r="44" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="12"/><circle cx="540" cy="80" r="44" fill="none" stroke="{A(u)}" stroke-width="12" stroke-linecap="round" stroke-dasharray="{2*math.pi*44*.78:.1f} 400" transform="rotate(-90 540 80)"/>' + bar(516, 74, 48, 12, .9, 6) + bar(480, 14, 60, 7, .5)
    s += card(240, 164, 380, 130, u, 16) + bar(256, 178, 90, 7, .5)
    for i in range(3):
        y = 200 + i * 30
        s += avatar(268, y + 10, 10, u, .6 + .1 * (2 - i)) + bar(288, y + 4, 70, 7, .7) + f'<rect x="388" y="{y+4}" width="214" height="10" rx="5" fill="#fff" fill-opacity=".12"/><rect x="388" y="{y+4}" width="{[190,150,110][i]}" height="10" rx="5" fill="{A(u)}"/>'
    return s

def collab(u, r):
    s = card(0, 0, 400, 294, u, 16) + "".join(f'<circle cx="{26+i*22}" cy="26" r="11" fill="{A(u)}" fill-opacity="{.95-i*.15}" stroke="#0B0C24" stroke-width="3"/>' for i in range(4)) + bar(130, 20, 90, 8, .5) + chip(330, 14, 56, u, 22)
    s += cols(u, 12, 54, 3, 120, 8, 228)
    for c in range(3):
        y = 68
        for k in range([3, 3, 2][c]):
            h = [50, 62, 44][(c + k) % 3]
            s += (f'<rect x="{20+c*128}" y="{y}" width="104" height="{h}" rx="9" fill="{A(u)}" fill-opacity=".22" stroke="{A(u)}"/>' if (c, k) == (1, 0) else card(20 + c * 128, y, 104, h, u, 9, .1)) + bar(28 + c * 128, y + 10, 70, 6, .7) + bar(28 + c * 128, y + 24, 50, 5, .3) + avatar(94 + c * 128, y + h - 14, 7, u)
            y += h + 8
    for i in range(4):
        x = 420 + (i % 2) * 104; y = (i // 2) * 104
        s += card(x, y, 96, 96, u, 14, .16) + avatar(x + 48, y + 40, 22, u, .6 + i * .1) + bar(x + 14, y + 76, 60, 6, .45)
    s += "".join(f'<g transform="translate({436+i*60} 224)"><circle cx="22" cy="22" r="22" fill="url(#glass{u})" stroke="#fff" stroke-opacity=".3"/><path d="M22 22 V8 M22 22 L32 28" stroke="{A(u)}" stroke-width="3" stroke-linecap="round"/></g>' for i in range(3))
    s += bar(436, 276, 60, 5, .35) + bar(496, 276, 60, 5, .35) + bar(556, 276, 40, 5, .35)
    return s

def website(u, r):
    s = card(0, 0, 620, 294, u, 18, .16, "#0E1030") + '<path d="M0 38 H620" stroke="#fff" stroke-opacity=".1"/>' + dot(24, 19, 8, u) + bar(40, 15, 60, 8, .8) + "".join(bar(230 + i * 56, 16, 38, 6, .4) for i in range(4))
    s += f'<rect x="530" y="9" width="76" height="22" rx="11" fill="#fff" fill-opacity=".1" stroke="#fff" stroke-opacity=".2"/>' + T(568, 24, "EN | AR", 10, .85, "middle", 700, True)
    s += bar(28, 70, 260, 18, .9) + bar(28, 98, 220, 18, .65) + bar(28, 132, 230, 7, .35) + bar(28, 146, 200, 7, .35) + chip(28, 172, 96, u, 30) + card(136, 172, 96, 30, u, 15, .3)
    s += f'<circle cx="470" cy="128" r="86" fill="{A(u)}" fill-opacity=".25"/><circle cx="470" cy="128" r="60" fill="{A(u)}" fill-opacity=".45"/><circle cx="500" cy="100" r="32" fill="#fff" fill-opacity=".2"/>'
    s += card(380, 156, 120, 54, u, 12, .3, "#12143A") + dot(402, 178, 10, u) + bar(420, 170, 60, 7, .8) + bar(420, 184, 40, 5, .3)
    for i in range(3): s += card(28 + i * 196, 222, 184, 60, u, 12, .12) + dot(52 + i * 196, 252, 12, u, .8) + bar(74 + i * 196, 244, 90, 8, .7) + bar(74 + i * 196, 260, 60, 5, .28)
    return s

def cloud(u, r):
    s = f'<path d="M110 250 h380 a50 50 0 0 0 6 -99 a74 74 0 0 0 -140 -22 a52 52 0 0 0 -90 24 a46 46 0 0 0 -156 97z" fill="{A(u)}" fill-opacity=".08" stroke="{A(u)}" stroke-opacity=".4" stroke-width="2" stroke-dasharray="8 6"/>'
    nodes = [(70, 40, "Angular"), (250, 20, "Gateway"), (430, 40, "API"), (150, 150, "Cache"), (310, 150, "SQL"), (480, 150, "Storage"), (230, 240, "Queue"), (400, 240, "Monitor")]
    links = [(0, 1), (1, 2), (2, 4), (1, 3), (2, 5), (4, 6), (4, 7)]
    P = {i: (x + 50, y + 22) for i, (x, y, _) in enumerate(nodes)}
    for a, b in links: s += line(P[a][0], P[a][1], P[b][0], P[b][1], u, 2, .5, "5 4")
    for i, (x, y, name) in enumerate(nodes):
        s += card(x, y, 100, 44, u, 12, .28, "#12143A") + dot(x + 20, y + 22, 9, u, .95) + T(x + 36, y + 26, name, 11, .9)
    s += chip(530, 10, 80, u, 22) + bar(544, 18, 52, 6, .9).replace('fill="#fff"', 'fill="#0B0C24"')
    return s

def globe_crm(u, r):
    s = card(0, 0, 300, 294, u, 18, .12)
    cx, cy, R = 150, 148, 118
    s += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{A(u)}" fill-opacity=".1" stroke="{A(u)}" stroke-opacity=".7" stroke-width="2"/>'
    for k in (30, 70): s += f'<ellipse cx="{cx}" cy="{cy}" rx="{R*k/100*1.0:.0f}" ry="{R}" fill="none" stroke="#fff" stroke-opacity=".15"/>'
    for yy in (-60, -20, 25, 65): s += f'<ellipse cx="{cx}" cy="{cy+yy}" rx="{math.sqrt(max(R*R-yy*yy,1)):.0f}" ry="10" fill="none" stroke="#fff" stroke-opacity=".12"/>'
    pts = [(95, 90), (190, 70), (215, 130), (130, 150), (175, 200), (100, 210), (240, 190)]
    for i in range(len(pts) - 1): s += line(*pts[i], *pts[i + 1], u, 1.8, .55, "4 4")
    for x, y in pts: s += f'<circle cx="{x}" cy="{y}" r="12" fill="{A(u)}" fill-opacity=".25"/><circle cx="{x}" cy="{y}" r="5.5" fill="{A(u)}"/>'
    s += card(320, 0, 300, 294, u, 18, .12)
    for i, cur in enumerate(["SAR", "USD", "EUR", "GBP", "AED"]):
        y = 14 + i * 54
        s += card(332, y, 276, 44, u, 11, .1) + avatar(354, y + 22, 12, u, .5 + i * .1) + bar(376, y + 11, 76, 8, .75) + bar(376, y + 25, 50, 5, .28)
        s += f'<rect x="470" y="{y+12}" width="42" height="20" rx="10" fill="#fff" fill-opacity=".1" stroke="#fff" stroke-opacity=".2"/>' + T(491, y + 26, cur, 9.5, .85, "middle", 700, True) + chip(522, y + 14, 74, u, 16, .5 + .1 * (i % 3))
    return s

def portal(u, r):
    s = card(0, 0, 130, 294, u, 16)
    for i in range(6): s += (f'<rect x="10" y="{14+i*34}" width="110" height="26" rx="9" fill="{A(u)}"/>' if i == 0 else "") + dot(26, 27 + i * 34, 5, u, .35 if i else .1) + bar(40, 24 + i * 34, 60 - i * 3, 6, .55 if i == 0 else .35)
    for i in range(3):
        x = 146 + i * 156
        s += card(x, 0, 146, 128, u, 14) + bar(x + 12, 14, 80, 8, .8) + bar(x + 12, 30, 50, 5, .3) + f'<rect x="{x+12}" y="62" width="122" height="10" rx="5" fill="#fff" fill-opacity=".12"/><rect x="{x+12}" y="62" width="{[96,60,112][i]}" height="10" rx="5" fill="{A(u)}"/>' + chip(x + 12, 88, 46, u, 14, .7) + "".join(avatar(x + 102 + j * 14 - 8, 106, 8, u, .5 + j * .2) for j in range(2))
    s += card(146, 144, 270, 150, u, 14) + bar(160, 158, 70, 7, .5)
    for i in range(4):
        y = 180 + i * 28
        s += bar(160, y + 4, 90, 7, .65) + bar(282, y + 4, 50, 6, .3) + f'<rect x="354" y="{y}" width="48" height="16" rx="8" fill="{A(u) if i<2 else "#fff"}" fill-opacity="{.85 if i<2 else .15}"/>'
    s += card(430, 144, 190, 150, u, 14) + avatar(454, 172, 12, u) + bar(474, 166, 80, 7, .7)
    s += f'<rect x="444" y="196" width="124" height="28" rx="12" fill="#fff" fill-opacity=".1"/>' + f'<rect x="500" y="232" width="106" height="28" rx="12" fill="{A(u)}" fill-opacity=".85"/>' + bar(510, 243, 80, 6, .9)
    return s

def phone(u, r):
    def ph(x, y, content):
        return (f'<rect x="{x}" y="{y}" width="156" height="294" rx="28" fill="#0E1030" stroke="#fff" stroke-opacity=".35" stroke-width="2.5"/>'
                f'<rect x="{x+7}" y="{y+7}" width="142" height="280" rx="22" fill="#0B0C24"/><rect x="{x+54}" y="{y+13}" width="48" height="10" rx="5" fill="#fff" fill-opacity=".18"/>' + content)
    m = '<rect x="0" y="0" width="128" height="150" rx="14" fill="#fff" fill-opacity=".06"/>' + "".join(f'<path d="M{x} 0 V150 M0 {y} H128" stroke="#fff" stroke-opacity=".07"/>' for x in (32, 64, 96) for y in (37, 75, 112))
    m += f'<path d="M20 120 C40 100 50 140 70 90 S100 70 112 40" fill="none" stroke="{A(u)}" stroke-width="5" stroke-linecap="round"/><circle cx="20" cy="120" r="6" fill="#fff"/><circle cx="112" cy="40" r="9" fill="{A(u)}"/>'
    p1 = f'<g transform="translate(163 52)">{m}</g>' + card(163, 214, 128, 58, u, 14, .2) + dot(184, 236, 9, u) + bar(200, 228, 70, 7, .8) + bar(200, 242, 46, 5, .3) + chip(176, 254, 60, u, 12)
    p2 = bar(361, 44, 70, 9, .8) + f'<circle cx="426" cy="52" r="0"/>'
    for i in range(4):
        y = 70 + i * 46
        p2 += card(361, y, 128, 38, u, 11, .12) + (f'<rect x="371" y="{y+10}" width="18" height="18" rx="5" fill="{A(u)}"/><path d="M375 19 l4 4 l6 -8" stroke="#0B0C24" stroke-width="2.5" fill="none" stroke-linecap="round"/>' if i < 2 else f'<rect x="371" y="{y+10}" width="18" height="18" rx="5" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>') + bar(398, y + 12, 70, 7, .7) + bar(398, y + 24, 44, 5, .25)
    p2 += f'<rect x="361" y="258" width="128" height="26" rx="13" fill="{A(u)}"/>' + bar(402, 268, 48, 6, .9).replace('fill="#fff"', 'fill="#0B0C24"')
    s = ph(156, 0, p1) + ph(328, 0, p2)
    s += card(8, 40, 128, 54, u, 14, .16) + dot(30, 67, 10, u) + bar(48, 58, 70, 7, .8) + bar(48, 72, 44, 5, .3)
    s += card(496, 150, 124, 54, u, 14, .16) + dot(518, 177, 10, u, .7) + bar(536, 168, 70, 7, .8) + bar(536, 182, 44, 5, .3)
    s += f'<circle cx="60" cy="220" r="30" fill="{A(u)}" fill-opacity=".18"/><circle cx="60" cy="220" r="16" fill="{A(u)}" fill-opacity=".5"/>'
    return s

# unchanged originals are provided by make_banners (dashboard, board, pipeline, kiosk, chat, doc, endpoints)
EXTRA = dict(iam=iam, profiles=profiles, policy=policy, metro=metro, cases=cases, ai_chat_sources=ai_chat_sources, billing=billing,
             warehouse=warehouse, calendar=calendar, school=school, booking=booking, store=store, referral=referral, feed=feed,
             analytics=analytics, modernize=modernize, vault=vault, tenants=tenants, recon=recon, chatbot=chatbot, support=support,
             docqa=docqa, aiinsight=aiinsight, kbsearch=kbsearch, resume=resume, collab=collab, website=website, cloud=cloud,
             globe_crm=globe_crm, portal=portal, phone=phone)

# ------------------------------------------------------ batch 3 drawers -----
def clinic(u, r):
    s = card(0, 0, 330, 294, u, 16) + bar(16, 14, 80, 8, .6) + chip(260, 12, 54, u, 16)
    for i in range(6):
        y = 40 + i * 42
        s += bar(14, y + 14, 28, 6, .35) + '<path d="M56 %d H316" stroke="#fff" stroke-opacity=".08"/>' % (y + 20)
        if i in (0, 2, 3, 5):
            h = 34 if i != 2 else 70
            if i == 3: continue
            s += f'<rect x="64" y="{y+2}" width="{rr(r,180,246)}" height="{h}" rx="10" fill="{A(u)}" fill-opacity="{.9 if i==0 else .45}"/>' + avatar(84, y + 19, 9, u, .9).replace(A(u), "#fff") + bar(102, y + 11, 90, 7, .9) + bar(102, y + 24, 56, 5, .5)
    s += card(350, 0, 270, 294, u, 16, .2) + avatar(388, 42, 22, u) + bar(422, 28, 110, 10, .85) + bar(422, 46, 70, 6, .35) + chip(556, 24, 48, u, 16)
    s += f'<path d="M366 130 h34 l8 -26 l12 52 l10 -36 l8 10 h150" fill="none" stroke="{A(u)}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/><path d="M366 130 h34 l8 -26 l12 52 l10 -36 l8 10 h150" fill="none" stroke="{A(u)}" stroke-width="9" opacity=".22" filter="url(#soft{u})"/>'
    for i in range(3): s += card(366, 168 + i * 36, 238, 30, u, 9, .1) + dot(384, 183 + i * 36, 7, u, .7) + bar(400, 177 + i * 36, 100, 7, .7) + bar(560, 178 + i * 36, 34, 6, .3)
    s += chip(366, 272, 100, u, 14, .8)
    return s

def realestate(u, r):
    s = card(0, 0, 620, 40, u, 20, .24) + f'<circle cx="26" cy="20" r="8" fill="none" stroke="#fff" stroke-width="2.5" stroke-opacity=".8"/>' + bar(46, 16, 160, 8, .5) + chip(520, 8, 84, u, 24)
    s += "".join(chip(0 + i * 92, 52, 82, u, 20, 1 if i == 0 else .35) for i in range(5))
    for i in range(3):
        x = i * 210
        s += card(x, 86, 196, 150, u, 14, .14) + f'<rect x="{x+8}" y="94" width="180" height="78" rx="10" fill="{A(u)}" fill-opacity="{[.55,.4,.7][i]}"/>'
        s += f'<path d="M{x+68} 150 l30 -26 l30 26 v22 h-60z" fill="#fff" fill-opacity=".4"/><rect x="{x+90}" y="150" width="16" height="22" fill="#0B0C24" fill-opacity=".4"/>'
        s += f'<rect x="{x+14}" y="100" width="54" height="18" rx="9" fill="#0B0C24" fill-opacity=".55"/>' + bar(x + 22, 106, 38, 6, .9) + bar(x + 12, 184, 110, 8, .8) + bar(x + 12, 200, 78, 6, .3) + chip(x + 12, 214, 40, u, 12, .8) + chip(x + 58, 214, 40, u, 12, .5)
    s += card(0, 248, 620, 46, u, 13, .14) + avatar(26, 271, 12, u) + bar(48, 262, 110, 8, .75) + bar(48, 276, 70, 5, .3) + chip(520, 260, 84, u, 22)
    return s

def fleet(u, r):
    s = card(0, 0, 400, 294, u, 18, .12)
    for gx in range(0, 400, 50): s += f'<path d="M{gx} 0 V294" stroke="#fff" stroke-opacity=".05"/>'
    for gy in range(0, 294, 49): s += f'<path d="M0 {gy} H400" stroke="#fff" stroke-opacity=".05"/>'
    s += '<path d="M0 90 L140 90 L200 150 L400 150 M120 294 L120 200 L200 150 L260 60 L400 60" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="12" stroke-linejoin="round"/>'
    s += f'<path d="M30 250 L120 200 L200 150 L300 150 L370 60" fill="none" stroke="{A(u)}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 0"/><path d="M30 250 L120 200 L200 150 L300 150 L370 60" fill="none" stroke="{A(u)}" stroke-width="14" opacity=".2" filter="url(#soft{u})"/>'
    for x, y, c in [(30, 250, 0), (200, 150, 1), (370, 60, 2), (90, 100, 1), (300, 220, 1)]:
        s += f'<circle cx="{x}" cy="{y}" r="22" fill="{A(u)}" fill-opacity=".2"/><circle cx="{x}" cy="{y}" r="9" fill="{A(u) if c else "#fff"}" stroke="#0B0C24" stroke-width="3"/>'
    s += card(14, 14, 130, 30, u, 10, .24, "#12143A") + dot(32, 29, 6, u) + bar(46, 25, 80, 7, .8)
    s += card(420, 0, 200, 294, u, 16)
    for i in range(5):
        y = 14 + i * 56
        s += card(432, y, 176, 48, u, 11, .1 if i != 1 else .4) + f'<rect x="444" y="{y+14}" width="26" height="18" rx="4" fill="{A(u)}" fill-opacity=".85"/><circle cx="450" cy="{y+34}" r="3" fill="#fff"/><circle cx="464" cy="{y+34}" r="3" fill="#fff"/>' + bar(480, y + 12, 70, 7, .75) + f'<rect x="480" y="{y+28}" width="110" height="7" rx="3.5" fill="#fff" fill-opacity=".12"/><rect x="480" y="{y+28}" width="{rr(r,30,100)}" height="7" rx="3.5" fill="{A(u)}"/>'
    return s

def kitchen(u, r):
    s = ""
    for i in range(4):
        x = i * 158; h = [200, 150, 232, 176][i]; hot = i == 0
        s += f'<path d="M{x} 0 h146 v{h} l-9 8 l-9 -8 l-9 8 l-9 -8 l-9 8 l-9 -8 l-9 8 l-9 -8 l-9 8 l-9 -8 l-9 8 l-9 -8 l-9 8 l-9 -8 z" fill="url(#glass{u})" stroke="#fff" stroke-opacity=".16"/>'
        s += f'<rect x="{x}" y="0" width="146" height="38" rx="0" fill="{A(u)}" fill-opacity="{.95 if hot else .5}"/><path d="M{x} 0 h146 v38 h-146z" fill="none"/>' + bar(x + 14, 14, 50, 9, .95) + f'<circle cx="{x+122}" cy="19" r="11" fill="none" stroke="#fff" stroke-width="2.5" stroke-opacity=".9"/><path d="M{x+122} 13 v6 l4 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>'
        for k in range((h - 60) // 30):
            y = 52 + k * 30
            s += f'<rect x="{x+14}" y="{y}" width="14" height="14" rx="4" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="1.6"/>' + bar(x + 36, y + 3, rr(r, 50, 92), 8, .75) + bar(x + 36, y + 17, rr(r, 30, 60), 5, .25)
    s += card(0, 252, 620, 42, u, 21, .16) + "".join(chip(14 + i * 100, 262, 88, u, 22, 1 if i == 0 else .35) for i in range(5)) + bar(520, 270, 80, 7, .4)
    return s

def lms(u, r):
    s = card(0, 0, 392, 210, u, 18, .16, "#0E1030") + f'<rect x="0" y="0" width="392" height="210" rx="18" fill="{A(u)}" fill-opacity=".22"/><circle cx="196" cy="94" r="38" fill="#fff" fill-opacity=".92"/><path d="M186 76 L216 94 L186 112Z" fill="#0B0C24"/>'
    s += f'<rect x="20" y="178" width="352" height="8" rx="4" fill="#fff" fill-opacity=".2"/><rect x="20" y="178" width="{rr(r,150,230)}" height="8" rx="4" fill="{A(u)}"/>' + bar(20, 20, 120, 9, .8)
    for i in range(3): s += card(i * 134, 226, 124, 68, u, 12, .12) + f'<rect x="{i*134+8}" y="234" width="108" height="30" rx="7" fill="{A(u)}" fill-opacity="{[.55,.35,.45][i]}"/>' + bar(i * 134 + 10, 272, 90, 6, .6)
    s += card(412, 0, 208, 294, u, 16) + donut(u, 466, 54, 26, [.68, .32], 9) + bar(506, 38, 90, 8, .75) + bar(506, 54, 60, 6, .3)
    for i in range(6):
        y = 100 + i * 31
        s += (dot(430, y + 8, 7, u) + f'<path d="M426 {y+8} l3 3 l5 -6" stroke="#0B0C24" stroke-width="2" fill="none" stroke-linecap="round"/>' if i < 3 else f'<circle cx="430" cy="{y+8}" r="6.5" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>') + bar(446, y + 4, rr(r, 90, 150), 7, .7 if i < 4 else .35) + bar(446, y + 16, 50, 4, .22)
    return s

def invoice(u, r):
    s = f'<g transform="rotate(-2 170 150)"><rect x="8" y="0" width="300" height="294" rx="14" fill="#F6F4FF"/><rect x="28" y="22" width="86" height="12" rx="6" fill="#201A4A" fill-opacity=".85"/><rect x="214" y="22" width="76" height="8" rx="4" fill="#201A4A" fill-opacity=".3"/><rect x="214" y="36" width="52" height="6" rx="3" fill="#201A4A" fill-opacity=".2"/>'
    for i in range(5):
        y = 70 + i * 26
        s += f'<rect x="28" y="{y}" width="{rr(r,100,150)}" height="7" rx="3.5" fill="#201A4A" fill-opacity=".2"/><rect x="214" y="{y}" width="60" height="7" rx="3.5" fill="#201A4A" fill-opacity=".28"/>'
    s += f'<rect x="170" y="206" width="104" height="26" rx="8" fill="{A(u)}"/>'
    q = 6; sx, sy = 30, 200
    for i in range(q):
        for j in range(q):
            if (i < 2 and j < 2) or r.random() > .5: s += f'<rect x="{sx+i*12}" y="{sy+j*12}" width="10" height="10" fill="#201A4A"/>'
    s += "</g>"
    s += card(334, 0, 286, 130, u, 16) + bar(350, 14, 70, 7, .5) + area(u, 350, 36, 254, 78, r, 7)
    for i in range(3):
        y = 144 + i * 50
        s += card(334, y, 286, 42, u, 11, .12) + avatar(358, y + 21, 10, u, .6) + bar(378, y + 11, 90, 7, .75) + bar(378, y + 25, 56, 5, .28) + f'<rect x="548" y="{y+12}" width="58" height="18" rx="9" fill="{A(u) if i!=1 else "#fff"}" fill-opacity="{.9 if i!=1 else .2}"/>'
    return s

def tickets(u, r):
    s = ""
    for i in range(2):
        y = i * 100
        s += f'<path d="M0 {y+14} a14 14 0 0 1 14 -14 h358 a14 14 0 0 1 14 14 v20 a12 12 0 0 0 0 24 v18 a14 14 0 0 1 -14 14 h-358 a14 14 0 0 1 -14 -14 v-18 a12 12 0 0 0 0 -24z" fill="url(#glass{u})" stroke="#fff" stroke-opacity=".2"/>'
        s += f'<rect x="14" y="{y+14}" width="62" height="62" rx="12" fill="{A(u)}" fill-opacity="{.9 if i==0 else .55}"/>' + bar(92, y + 20, 140, 10, .85) + bar(92, y + 38, 100, 7, .35) + chip(92, y + 56, 52, u, 14) + chip(152, y + 56, 52, u, 14, .5)
        s += f'<path d="M290 {y+8} V{y+84}" stroke="#fff" stroke-opacity=".3" stroke-dasharray="5 5"/>'
        for a in range(5):
            for b in range(5):
                if r.random() > .45: s += f'<rect x="{304+a*13}" y="{y+16+b*13}" width="10" height="10" fill="#fff" fill-opacity=".8"/>'
    s += f'<g transform="translate(0 208)">' + card(0, 0, 386, 86, u, 14, .12) + bars(u, 16, 14, 14, 18, 8, 52, r) + bar(16, 72, 80, 5, .3) + "</g>"
    s += card(406, 0, 214, 294, u, 16) + bar(424, 16, 80, 8, .6) + f'<circle cx="513" cy="96" r="44" fill="{A(u)}" fill-opacity=".2" stroke="{A(u)}" stroke-width="3"/><path d="M492 96 l16 16 l30 -34" stroke="{A(u)}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    s += bar(450, 166, 126, 9, .8) + bar(470, 184, 86, 6, .3)
    for i in range(3): s += card(424, 204 + i * 28, 178, 22, u, 8, .1) + dot(438, 215 + i * 28, 5, u) + bar(452, 211 + i * 28, 90, 6, .6) + chip(566, 209 + i * 28, 26, u, 12, .6)
    return s

def approvals(u, r):
    s = card(0, 0, 620, 80, u, 16)
    names = 4
    for i in range(names):
        x = 56 + i * 170
        if i < names - 1: s += line(x + 18, 40, x + 152, 40, u, 3, 1 if i < 2 else .3)
        s += (dot(x, 40, 17, u) + f'<path d="M{x-7} {40} l5 5 l10 -11" stroke="#0B0C24" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' if i < 2 else f'<circle cx="{x}" cy="40" r="17" fill="#0B0C24" stroke="{A(u)}" stroke-width="3" stroke-opacity="{1 if i==2 else .35}"/>')
        s += bar(x - 24, 64, 48, 5, .5 if i < 3 else .25)
    s += card(0, 96, 250, 198, u, 16, .22) + bar(16, 112, 90, 8, .6) + bar(16, 134, 160, 14, .9, 7) + f'<rect x="16" y="162" width="218" height="46" rx="10" fill="#fff" fill-opacity=".07" stroke="#fff" stroke-opacity=".15" stroke-dasharray="5 4"/>' + bar(70, 180, 110, 7, .4)
    s += chip(16, 240, 104, u, 36) + card(130, 240, 104, 36, u, 18, .3)
    for i in range(4):
        y = 96 + i * 50
        s += card(270, y, 350, 42, u, 11, .1 if i != 2 else .4) + dot(294, y + 21, 11, u, .5 + i * .12) + bar(314, y + 11, rr(r, 100, 160), 7, .75) + bar(314, y + 25, 60, 5, .28) + chip(470, y + 12, 52, u, 18, .8) + bar(540, y + 17, 62, 8, .7)
    return s

EXTRA.update(clinic=clinic, realestate=realestate, fleet=fleet, kitchen=kitchen, lms=lms, invoice=invoice, tickets=tickets, approvals=approvals)

# ------------------------------------------------------ batch 4 drawers (ERP family) ---
def erp(u, r):
    s = card(0, 0, 286, 294, u, 18, .14) + bar(16, 14, 70, 8, .6)
    for i in range(9):
        x = 14 + (i % 3) * 88; y = 38 + (i // 3) * 84
        hot = i == 4
        s += (f'<rect x="{x}" y="{y}" width="80" height="76" rx="14" fill="{A(u)}" fill-opacity=".25" stroke="{A(u)}" stroke-width="1.6"/>' if hot else card(x, y, 80, 76, u, 14, .12))
        s += f'<circle cx="{x+24}" cy="{y+26}" r="13" fill="{A(u)}" fill-opacity="{.95 if hot else .55}"/>' + bar(x + 12, y + 50, 56, 7, .75) + bar(x + 12, y + 63, 34, 5, .28)
    for i in range(3):
        x = 304 + i * 108
        s += card(x, 0, 100, 62, u, 13) + bar(x + 12, 12, 40, 6, .4) + bar(x + 12, 30, 62, 14, .9, 7)
    s += card(304, 76, 316, 130, u, 16) + area(u, 322, 94, 280, 90, r, 9)
    for i in range(2): s += card(304, 218 + i * 40, 316, 34, u, 10, .1) + dot(324, 235 + i * 40, 8, u, .7) + bar(342, 229 + i * 40, 120, 7, .7) + chip(552, 228 + i * 40, 52, u, 14)
    return s

def payroll(u, r):
    s = card(0, 0, 360, 294, u, 16) + bar(16, 14, 70, 8, .6) + chip(290, 10, 54, u, 16)
    for i in range(6):
        y = 38 + i * 42
        s += card(10, y, 340, 36, u, 10, .1 if i != 1 else .4) + avatar(32, y + 18, 11, u, .5 + i * .08) + bar(52, y + 9, 80, 7, .75) + bar(52, y + 21, 50, 5, .28) + f'<rect x="188" y="{y+14}" width="90" height="8" rx="4" fill="#fff" fill-opacity=".12"/><rect x="188" y="{y+14}" width="{rr(r,30,86)}" height="8" rx="4" fill="{A(u)}"/>' + chip(294, y + 10, 46, u, 16, .8 if i % 2 == 0 else .4)
    s += f'<g transform="rotate(2 490 150)"><rect x="380" y="0" width="226" height="262" rx="12" fill="#F6F4FF"/><rect x="398" y="18" width="80" height="10" rx="5" fill="#201A4A" fill-opacity=".85"/><rect x="398" y="34" width="54" height="6" rx="3" fill="#201A4A" fill-opacity=".3"/>'
    for i in range(6): s += f'<rect x="398" y="{62+i*24}" width="{rr(r,70,100)}" height="6" rx="3" fill="#201A4A" fill-opacity=".2"/><rect x="540" y="{62+i*24}" width="50" height="6" rx="3" fill="#201A4A" fill-opacity=".3"/>'
    s += f'<rect x="398" y="214" width="190" height="30" rx="9" fill="{A(u)}"/></g>'
    s += donut(u, 592, 276, 0, [.5], 0) if False else ""
    return s

def ledger(u, r):
    s = card(0, 0, 404, 294, u, 16) + bar(16, 16, 60, 7, .5) + bar(214, 16, 40, 7, .5) + bar(318, 16, 40, 7, .5) + '<path d="M0 36 H404" stroke="#fff" stroke-opacity=".12"/>'
    for i in range(6):
        y = 46 + i * 36
        s += (f'<rect x="8" y="{y-3}" width="388" height="30" rx="8" fill="{A(u)}" fill-opacity=".14"/>' if i % 2 == 0 else "") + chip(16, y + 5, 28, u, 14, .6) + bar(54, y + 8, rr(r, 80, 130), 7, .7)
        if i % 2 == 0: s += bar(214, y + 8, rr(r, 30, 60), 7, .8)
        else: s += bar(318, y + 8, rr(r, 30, 60), 7, .8)
    s += f'<rect x="8" y="262" width="388" height="26" rx="8" fill="{A(u)}" fill-opacity=".9"/>' + bar(18, 271, 70, 8, .95).replace('fill="#fff"', 'fill="#0B0C24"') 
    s += card(424, 0, 196, 190, u, 16) + bar(440, 14, 80, 7, .5)
    for i in range(5):
        y = 38 + i * 30; neg = i == 3
        s += bar(440, y + 4, 40, 6, .4) + f'<rect x="{500 if not neg else 500-rr(r,20,50)}" y="{y}" width="{rr(r,30,80) if not neg else 0}" height="14" rx="5" fill="{A(u)}"/>' + (f'<rect x="{470}" y="{y}" width="30" height="14" rx="5" fill="#FF6B8B"/>' if neg else "")
    s += card(424, 204, 196, 90, u, 16, .3) + f'<circle cx="466" cy="249" r="22" fill="{A(u)}" fill-opacity=".25" stroke="{A(u)}" stroke-width="2.5"/><path d="M456 249 l8 8 l14 -17" stroke="{A(u)}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' + bar(500, 238, 90, 9, .85) + bar(500, 256, 60, 6, .3)
    return s

def procurement(u, r):
    s = ""
    for i in range(4):
        x = i * 158
        s += card(x, 0, 140, 104, u, 14, .16 if i < 3 else .4) + f'<circle cx="{x+28}" cy="30" r="14" fill="{A(u)}" fill-opacity="{.95 if i < 3 else .45}"/>' + bar(x + 50, 22, 70, 8, .8) + bar(x + 14, 58, 108, 6, .3) + bar(x + 14, 72, 80, 6, .3) + chip(x + 14, 86, 52, u, 12, .8 if i < 3 else .3)
        if i < 3: s += f'<path d="M{x+142} 52 l12 0 m-5 -5 l5 5 l-5 5" stroke="{A(u)}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
    s += card(0, 120, 380, 174, u, 16) + bar(16, 134, 80, 7, .5)
    for i in range(4):
        y = 156 + i * 34
        s += avatar(32, y + 12, 11, u, .5 + i * .1) + bar(52, y + 4, 90, 7, .75) + bar(52, y + 17, 56, 5, .28) + "".join(dot(250 + k * 14, y + 12, 4.5, u, 1 if k < 4 - i % 3 else .2) for k in range(5)) + chip(330, y + 6, 36, u, 14, .7)
    s += card(400, 120, 220, 174, u, 16, .2) + bar(416, 134, 70, 7, .5)
    for k in range(3):
        x = 416 + k * 66
        s += f'<rect x="{x}" y="{200-[60,80,46][k]}" width="52" height="{[60,80,46][k]+26}" rx="8" fill="{A(u) if k==1 else "#fff"}" fill-opacity="{.9 if k==1 else .14}"/>' + bar(x + 8, 232, 36, 6, .6) + bar(x + 8, 246, 24, 5, .3)
    s += chip(416, 266, 188, u, 16, .5)
    return s

def pos(u, r):
    s = ""
    for i in range(9):
        x = (i % 3) * 138; y = (i // 3) * 98
        s += card(x, y, 128, 90, u, 14, .14) + f'<rect x="{x+8}" y="{y+8}" width="112" height="44" rx="9" fill="{A(u)}" fill-opacity="{r.choice([.3,.45,.6,.75])}"/><circle cx="{x+64}" cy="{y+30}" r="{rr(r,10,15)}" fill="#fff" fill-opacity=".3"/>' + bar(x + 10, y + 62, 72, 7, .75) + chip(x + 10, y + 76, 36, u, 10, .9)
    s += f'<g transform="rotate(1.5 520 150)"><rect x="428" y="0" width="192" height="294" rx="12" fill="#F6F4FF"/><rect x="448" y="18" width="80" height="10" rx="5" fill="#201A4A" fill-opacity=".85"/>'
    for i in range(6): s += f'<rect x="448" y="{48+i*24}" width="{rr(r,60,90)}" height="6" rx="3" fill="#201A4A" fill-opacity=".22"/><rect x="570" y="{48+i*24}" width="32" height="6" rx="3" fill="#201A4A" fill-opacity=".3"/>'
    s += f'<path d="M448 204 H602" stroke="#201A4A" stroke-opacity=".3" stroke-dasharray="4 3"/><rect x="448" y="214" width="70" height="12" rx="6" fill="#201A4A" fill-opacity=".8"/><rect x="560" y="214" width="42" height="12" rx="6" fill="#201A4A" fill-opacity=".8"/><rect x="448" y="242" width="154" height="34" rx="10" fill="{A(u)}"/></g>'
    return s

def production(u, r):
    s = card(0, 0, 620, 294, u, 16) + "".join(f'<path d="M{150+i*58} 30 V284" stroke="#fff" stroke-opacity=".07"/>' + bar(158 + i * 58, 14, 30, 6, .4) for i in range(8))
    rows = [(0, 3), (2, 4), (4, 3), (3, 4), (5, 2), (4, 3), (6, 2)]
    for i, (st, ln) in enumerate(rows):
        y = 40 + i * 35
        s += bar(16, y + 8, rr(r, 60, 100), 7, .65) + bar(16, y + 21, 40, 5, .25)
        hot = i in (1, 3)
        s += f'<rect x="{150+st*58}" y="{y+4}" width="{ln*58-6}" height="22" rx="11" fill="{A(u) if hot else PAL["c2"]}" fill-opacity="{.95 if hot else .55}"/><rect x="{150+st*58}" y="{y+4}" width="{(ln*58-6)*[.8,.5,.2,.65,0,0,0][i]:.0f}" height="22" rx="11" fill="#fff" fill-opacity=".22"/>'
        if i < len(rows) - 1 and rows[i + 1][0] >= st + ln - 1:
            s += f'<path d="M{150+(st+ln)*58-6} {y+15} q12 0 12 14 v6" stroke="#fff" stroke-opacity=".45" stroke-width="1.6" fill="none"/>'
    s += f'<path d="M{150+7*58-20} 30 V284" stroke="#FFC857" stroke-width="2" stroke-dasharray="5 4"/><path d="M{150+7*58-20} 270 l8 -9 l8 9 l-8 9z" fill="#FFC857"/>'
    return s

EXTRA.update(erp=erp, payroll=payroll, ledger=ledger, procurement=procurement, pos=pos, production=production)

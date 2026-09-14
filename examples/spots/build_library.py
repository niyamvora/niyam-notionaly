"""Build library.html: every spot inlined, animation-ready, light/dark.

Draw — the spots are filled tapered paths (taper.py output), so stroke-dashoffset has
nothing to dash. Each brush stroke gets its centreline back (a taper path is the left run
followed by the reversed right run; the centre is their mean) and that centre is drawn as a
thick stroked path inside a <mask>. Dashing the mask reveals the fill like a pen.

Morph — the OpCreative model (apps/dashboard/src/components/ui/custom/morph): a base icon
morphs into a semantic, louder TWIN on hover — Bell into BellRing, Package into PackageOpen —
driven by morphicons. TWINS below is that pair table for the spots. The page runs the real
morphicons engine (morphicons.iife.js, MIT) on the ink: every stroke's centreline and every
solid mass is a subpath, the engine pairs subpaths between base and twin (extras are born out
of the nearest existing line, rotation is solved by Procrustes), and each frame the
interpolated centrelines are re-tapered into brush strokes so the style survives the morph.
Paper backings, tints and accent dots pair by index and lerp on the side.

    python3 build_library.py [spots-dir] [out.html]    # default: this folder -> library.html
"""
import copy
import glob
import html as htmlmod
import json
import math
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "skill", "assets"))
from taper import _smooth, arc, stroke  # noqa: E402

STAGGER_MS, DRAW_MS, VARIANTS, JITTER = 70, 450, 2, 2.6
NUM = r"-?\d*\.?\d+"


# ----------------------------------------------------------------------------- parsing
def _pairs(nums):
    return [(nums[i], nums[i + 1]) for i in range(0, len(nums), 2)]


def parse_taper(d):
    """left, right_rev point lists for a taper.stroke() path, or None if it is not one."""
    toks = [(c, [float(x) for x in re.findall(NUM, body)])
            for c, body in re.findall(r"([MLQZa])([^MLQZa]*)", d)]
    if any(c == "a" for c, _ in toks):
        return None
    runs, cur = [], None
    for c, nums in toks:
        if c == "M":
            cur = [_pairs(nums)[0]]
        elif c == "Q":
            cur.append(_pairs(nums)[0])          # control point == original sample
        elif c == "L":
            ps = _pairs(nums)
            cur.append(ps[0])
            runs.append(cur)
            cur = ps[1:]                          # implicit lineto starts the return run
    if len(runs) != 2 or len(runs[0]) != len(runs[1]):
        return None
    return runs[0], runs[1]


def parse_mass(d):
    """Sample points of a blob (one smoothed run) or polygon; None for arcs/tapers."""
    if "a" in d or parse_taper(d):
        return None
    pts = []
    for c, body in re.findall(r"([MLQZ])([^MLQZ]*)", d):
        nums = [float(x) for x in re.findall(NUM, body)]
        if c in "ML":
            pts += _pairs(nums)
        elif c == "Q":
            pts.append(_pairs(nums)[0])
    return pts


DISC = re.compile(rf"^M({NUM}) ({NUM})a({NUM}) {NUM} 0 1 0 {NUM} 0a")


def parse(svg_text):
    """A spot as a flat element list: stroke (L/R runs), mass (points) or dot."""
    body = re.search(r"<g[^>]*>(.*?)</g>", svg_text, re.S).group(1)
    els = []
    for m in re.finditer(r"<(path|circle)([^>]*)/>", body):
        tag, attrs = m.group(1), m.group(2)
        flags = dict(paper="#FFFFFF" in attrs, tint="opacity" in attrs, plane='class="plane"' in attrs)
        if tag == "circle":
            g = lambda k: float(re.search(rf'{k}="({NUM})"', attrs).group(1))
            els.append(dict(kind="dot", cx=g("cx"), cy=g("cy"), r=g("r"), **flags))
            continue
        d = re.search(r'd="([^"]+)"', attrs).group(1)
        if dm := DISC.match(d):                   # disc() from the generator -> a dot
            x, y, r = map(float, dm.groups())
            els.append(dict(kind="dot", cx=x + r, cy=y, r=r, **flags))
        elif tp := parse_taper(d):
            els.append(dict(kind="stroke", L=tp[0], R=tp[1], **flags))
        else:
            els.append(dict(kind="mass", pts=parse_mass(d), smooth="Q" in d, **flags))
    return els


def ink(e):
    """What morphicons animates: brush strokes and solid masses. Not backings, tints, dots."""
    return e["kind"] != "dot" and not e["paper"] and not e["tint"]


def centre(e):
    n = len(e["L"])
    return [((e["L"][j][0] + e["R"][n - 1 - j][0]) / 2, (e["L"][j][1] + e["R"][n - 1 - j][1]) / 2)
            for j in range(n)]


def width(e):
    n = len(e["L"])
    return max(math.dist(e["L"][j], e["R"][n - 1 - j]) for j in range(n))


def profile(e):
    """[start, end, peak] width of a stroke — enough to rebuild its taper after a morph."""
    n = len(e["L"])
    w = lambda j: math.dist(e["L"][j], e["R"][n - 1 - j])
    return [round(w(0), 1), round(w(n - 1), 1), round(max(w(j) for j in range(n)), 1)]


# ----------------------------------------------------------------------------- geometry
def res(pts, n=20):
    """Resample a polyline to n evenly spaced points."""
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(seg) or 1.0
    out = []
    for i in range(n):
        d, j = total * i / (n - 1), 0
        while j < len(seg) - 1 and d > seg[j]:
            d -= seg[j]; j += 1
        t = d / seg[j] if seg[j] else 0.0
        out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * t,
                    pts[j][1] + (pts[j + 1][1] - pts[j][1]) * t))
    return out


def jitter(pts, k, seed):
    """Low-frequency hand wobble, variant k, for the boil. Same offset both sides keeps width."""
    return [(x + JITTER * math.sin(i * 0.9 + k * 2.1 + seed),
             y + JITTER * math.cos((i * 0.9 + k * 2.1 + seed) * 0.7 + 1.0))
            for i, (x, y) in enumerate(pts)]


def taper_d(left, right_rev):
    return _smooth(left) + " " + _smooth(right_rev)[1:] + " Z"


def mass_d(pts, smooth):
    return (_smooth(pts) if smooth else
            "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)) + " Z"


def el_d(el):
    return taper_d(el["L"], el["R"]) if el["kind"] == "stroke" else mass_d(el["pts"], el["smooth"])


def poly_d(pts, closed):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + ("Z" if closed else "")


# ------------------------------------------------------------------------- twin authoring
def _xf(els, idxs, fn):
    for i in idxs:
        e = els[i]
        e.setdefault("xf", []).append(fn)         # replayed onto a v2 plane that follows this element
        if e["kind"] == "stroke":
            e["L"], e["R"] = [fn(p) for p in e["L"]], [fn(p) for p in e["R"]]
        elif e["kind"] == "mass":
            e["pts"] = [fn(p) for p in e["pts"]]
        else:
            e["cx"], e["cy"] = fn((e["cx"], e["cy"]))


def _pivot(els, idxs, cx, cy):
    """A rotated/scaled element's centroid must orbit the pivot, not cut the chord —
    morphicons' block term, which it only derives on its own for a globally congruent icon."""
    for i in idxs:
        els[i]["pivot"] = (cx, cy)


def rot(els, idxs, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    _xf(els, idxs, lambda p: (cx + (p[0] - cx) * c - (p[1] - cy) * s,
                              cy + (p[0] - cx) * s + (p[1] - cy) * c))
    _pivot(els, idxs, cx, cy)


def mov(els, idxs, dx, dy):
    _xf(els, idxs, lambda p: (p[0] + dx, p[1] + dy))


def scl(els, idxs, k, cx, cy, ky=None):
    ky = k if ky is None else ky
    _xf(els, idxs, lambda p: (cx + (p[0] - cx) * k, cy + (p[1] - cy) * ky))
    _pivot(els, idxs, cx, cy)
    for i in idxs:
        if els[i]["kind"] == "dot":
            els[i]["r"] *= k


def add_stroke(base, twin, pts, w=3, w0=7, w1=7, n=12):
    """An extra stroke in the twin only. morphicons pairs it with the nearest existing line
    and it grows out of that — the BellRing effect — so the base needs no counterpart."""
    L, R = parse_taper(stroke(res(pts, n), w=w, w0=w0, w1=w1))
    twin.append(dict(kind="stroke", L=L, R=R, paper=False, tint=False))


def restroke(twin, i, pts, w=3, w0=7, w1=7, n=12):
    """Replace a twin stroke with a freshly drawn one. Use it when a transform would leave a
    near-straight line slightly bent: morphicons scores a line's two traversals by residual
    first, and a bend can tip it into rotating the long way round."""
    L, R = parse_taper(stroke(res(pts, n), w=w, w0=w0, w1=w1))
    twin[i] = dict(twin[i], L=L, R=R)


def add_ring(base, twin, cx, cy, r, gap=12):
    for a0, a1 in ((gap, 180 - gap / 2), (180 + gap / 2, 360 - gap)):
        add_stroke(base, twin, arc(cx, cy, r, a0, a1, n=14), w=3, w0=6, w1=6, n=14)


def rbox(x0, y0, x1, y1, r, n=6):
    """Points round a rounded rectangle, closed — an extra drawn as one near-closed stroke."""
    pts = (arc(x1 - r, y0 + r, r, -90, 0, n=n) + arc(x1 - r, y1 - r, r, 0, 90, n=n)
           + arc(x0 + r, y1 - r, r, 90, 180, n=n) + arc(x0 + r, y0 + r, r, 180, 270, n=n))
    return pts + pts[:1]


def add_rays(base, twin, cx, cy, r0, r1, angles):
    for a in angles:
        a = math.radians(a)
        add_stroke(base, twin, [(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
                                (cx + r1 * math.cos(a), cy + r1 * math.sin(a))], w=3, w0=6, w1=6, n=6)


# Element indices refer to file order. Same idea as OpCreative's MORPH_PAIRS: base -> louder
# twin; keep the meaning, raise the volume. Keep symmetric lines (clock hands) under 90° —
# morphicons resolves a line's orientation by minimal rotation, so 180° reads as a flip.
TWINS = {
    "01-suitcase": lambda b, t: (rot(t, range(0, 11), -7, 260, 338),               # rolling
                                 add_stroke(b, t, [(38, 250), (76, 250)]),
                                 add_stroke(b, t, [(28, 286), (70, 286)])),
    "02-clock": lambda b, t: (rot(t, [3], 80, 200, 200), rot(t, [4], 30, 200, 200)),  # time passes
    "03-train": lambda b, t: (scl(t, range(0, 9), 1.06, 200, 205),                 # approaching
                              add_stroke(b, t, [(52, 150), (90, 150)]),
                              add_stroke(b, t, [(44, 190), (86, 190)])),
    "04-two-days": lambda b, t: (rot(t, range(9, 15), -9, 226, 314),               # page lifts
                                 mov(t, [4, 5], 0, -8)),
    "05-coffee": lambda b, t: (rot(t, range(0, 8), 5, 200, 320),                   # fresh pour
                               mov(t, [8, 9], 0, -16), scl(t, [8, 9], 1.25, 200, 115),
                               add_stroke(b, t, [(206, 108), (200, 84), (208, 60), (202, 40)], w=3, w0=5, w1=3)),
    "06-bicycle": lambda b, t: (rot(t, [0, 1], 90, 122, 262), rot(t, [2, 3], 90, 288, 262),  # riding
                                rot(t, [10], 90, 205, 262),
                                add_stroke(b, t, [(36, 214), (70, 214)]),
                                add_stroke(b, t, [(26, 250), (64, 250)])),
    "07-paper-plane": lambda b, t: (rot(t, range(0, 4), -14, 200, 200), mov(t, range(0, 4), 18, -22),  # in flight
                                    add_stroke(b, t, [(58, 292), (96, 272)]),
                                    add_stroke(b, t, [(46, 328), (82, 312)])),
    "08-lightbulb": lambda b, t: (scl(t, [0], 1.04, 200, 168),                     # switched on
                                  add_rays(b, t, 200, 168, 96, 124, (-150, -118, -90, -62, -30))),
    "09-camera": lambda b, t: (scl(t, [7], 0.56, 200, 222),                        # flash, aperture
                               add_rays(b, t, 288, 178, 20, 46, (-155, -115, -75, -35))),
    "10-umbrella": lambda b, t: (rot(t, range(0, 7), 12, 200, 240),                # rain
                                 *[add_stroke(b, t, [(x, 42), (x - 9, 74)]) for x in (74, 146, 232, 306, 350)]),
    "11-key": lambda b, t: (rot(t, range(0, 6), 32, 150, 150),),                   # turning
    "12-envelope": lambda b, t: (restroke(t, 2, [(80, 138), (200, 82)]),               # flap opens
                                 restroke(t, 3, [(200, 82), (320, 138)]),
                                 mov(t, [4, 5], 0, -22)),
    "13-mountain": lambda b, t: (add_ring(b, t, 312, 108, 24),                     # sunrise
                                 add_rays(b, t, 312, 108, 34, 52, (-160, -115, -65, -20))),
    # launch: lift stays under the window ring's arc spacing (~40px) or the engine pairs the arcs crosswise
    "14-rocket": lambda b, t: (mov(t, range(0, 8), 0, -16), scl(t, [7], 2.3, 200, 254),
                               add_stroke(b, t, [(200, 340), (200, 374)]),
                               add_stroke(b, t, [(176, 336), (168, 362)]),
                               add_stroke(b, t, [(224, 336), (232, 362)])),
    "15-globe": lambda b, t: (rot(t, range(0, 5), -12, 200, 200), mov(t, [2, 3], 36, 0)),  # spins
    "16-house": lambda b, t: (add_stroke(b, t, [(262, 92), (254, 74), (266, 56)], w=3, w0=6, w1=5),   # chimney smoke
                              add_stroke(b, t, [(270, 66), (262, 46), (274, 28)], w=3, w0=6, w1=5)),
    "17-bell": lambda b, t: (rot(t, range(0, 4), 14, 200, 90),                     # BellRing
                             add_stroke(b, t, arc(200, 200, 140, 205, 235, n=8), w=3, w0=6, w1=6, n=8),
                             add_stroke(b, t, arc(200, 200, 140, -55, -25, n=8), w=3, w0=6, w1=6, n=8)),
    "18-plant": lambda b, t: (scl(t, [5, 6, 7], 1.12, 200, 232), scl(t, [4], 1, 200, 232, ky=1.08),  # grows
                              add_stroke(b, t, [(198, 150), (172, 142), (152, 120)], w=3, w0=6, w1=4)),
    "19-laptop": lambda b, t: (scl(t, [0, 1], 1.02, 200, 166),                     # wakes: text appears
                               add_stroke(b, t, [(140, 136), (240, 136)]), add_stroke(b, t, [(140, 166), (210, 166)]),
                               add_stroke(b, t, [(140, 196), (256, 196)])),
    "20-headphones": lambda b, t: (mov(t, range(0, 7), 0, -8),                     # music
                                   add_stroke(b, t, [(296, 104), (296, 54)], w=3, w0=6, w1=6),
                                   add_stroke(b, t, [(296, 54), (318, 66)], w=3, w0=6, w1=5),
                                   add_stroke(b, t, [(338, 78), (338, 32)], w=3, w0=6, w1=6),
                                   add_stroke(b, t, [(338, 32), (358, 42)], w=3, w0=6, w1=5)),
    "21-pencil": lambda b, t: (rot(t, range(0, 5), -8, 86, 314),                   # writes
                               add_stroke(b, t, [(56, 332), (84, 342), (112, 334), (140, 344), (168, 336)], w=3, w0=6, w1=6, n=16)),
    "22-shopping-bag": lambda b, t: (mov(t, range(0, 4), 0, -10), scl(t, range(0, 4), 1.03, 200, 240),  # bought
                                     mov(t, [5], 8, -34), add_rays(b, t, 330, 118, 14, 34, (-120, -75, -30))),
    "23-chat-bubble": lambda b, t: (mov(t, [3], 0, -6), mov(t, [4], 0, -14), mov(t, [5], 0, -6),   # reply arrives
                                    mov(t, [7], 14, -26),
                                    add_stroke(b, t, rbox(240, 40, 340, 108, 16), w=3, w0=6, w1=6, n=28),
                                    add_stroke(b, t, [(318, 106), (330, 132), (290, 106)], w=3, w0=6, w1=6, n=12)),
    "24-map-pin": lambda b, t: (mov(t, [0, 1], 0, -22), scl(t, [2, 3], 1.25, 200, 328),   # bounces
                                add_stroke(b, t, [(122, 300), (104, 284)], w=3, w0=6, w1=5),
                                add_stroke(b, t, [(278, 300), (296, 284)], w=3, w0=6, w1=5)),
    "25-trophy": lambda b, t: (scl(t, range(0, 6), 1.04, 200, 236),                # win
                               add_rays(b, t, 200, 130, 70, 96, (-150, -115, -90, -65, -30))),
    "26-calendar": lambda b, t: (mov(t, [3, 4], 0, -8), scl(t, [11], 1.3, 224, 262),   # a date is circled
                                 add_ring(b, t, 224, 262, 22, gap=14)),
    "27-magnifying-glass": lambda b, t: (rot(t, range(0, 5), -10, 316, 316),       # looks closer
                                         scl(t, [4], 1.3, 170, 170)),
    "28-book": lambda b, t: (scl(t, [6], 1, 264, 106, ky=1.25), mov(t, [7, 8, 9], 0, -4),   # reads on
                             add_stroke(b, t, [(228, 200), (300, 180)], w=2, w0=6, w1=6),
                             add_stroke(b, t, [(228, 234), (300, 214)], w=2, w0=6, w1=6),
                             add_stroke(b, t, [(228, 268), (280, 254)], w=2, w0=6, w1=6)),
}


# v2: which v1 element an inserted tint plane moves with (its own surface); absent = static
PLANE_FOLLOWS = {"07-paper-plane": 0, "08-lightbulb": 0, "10-umbrella": 0, "11-key": 0, "14-rocket": 0, "15-globe": 0,
                 "17-bell": 0, "19-laptop": 0, "20-headphones": 0, "21-pencil": 0, "22-shopping-bag": 0,
                 "24-map-pin": 0, "25-trophy": 0, "27-magnifying-glass": 0}


def make_pair(slug, base):
    twin = copy.deepcopy(base)
    lead = next((i for i, e in enumerate(base) if not e.get("plane")), len(base))  # v2 inserts; TWINS indices are v1 order
    if slug in TWINS:
        b, t = base[lead:], twin[lead:]
        TWINS[slug](b, t)
        twin.extend(t[len(b):])                        # extras were appended to the slice
        if lead and (k := PLANE_FOLLOWS.get(slug)) is not None:
            for fn in t[k].get("xf", []):
                _xf(twin, range(lead), fn)
            for j in range(lead):
                if "pivot" in t[k]:
                    twin[j]["pivot"] = t[k]["pivot"]
    return base, twin


# ----------------------------------------------------------------------------- emitting
def morph_cfg(slug, base, twin):
    """What the page hands morphicons: ink subpaths of both frames, a brush width, and the
    pivot (if any) of each base subpath so its centroid can orbit instead of cutting the chord."""
    sub = lambda e: poly_d(centre(e), False) if e["kind"] == "stroke" else poly_d(e["pts"], True)
    prof = lambda e: profile(e) if e["kind"] == "stroke" else None
    return dict(name=slug,
                **{"from": "".join(sub(e) for e in base if ink(e))},
                to="".join(sub(e) for e in twin if ink(e)),
                ws=[prof(e) for e in base if ink(e)], wt=[prof(e) for e in twin if ink(e)],
                piv=[twin[i].get("pivot") for i, e in enumerate(base) if ink(e)])


def convert(svg_text, slug):
    base, twin = make_pair(slug, parse(svg_text))
    seed = sum(map(ord, slug)) % 7
    defs, out, n_strokes = [], [], 0
    last_under = max([i for i, e in enumerate(base) if e["kind"] == "mass" and not ink(e)], default=-1)
    for i, a in enumerate(base):
        b = twin[i]                                   # twins derive from base: index-aligned
        fill = ' fill="var(--paper)"' if a["paper"] else (' fill="var(--tint)"' if a["tint"] else "")
        if a["kind"] == "dot":
            out.append(f'<circle cx="{a["cx"]:.1f}" cy="{a["cy"]:.1f}" r="{a["r"]:.1f}"{fill} '
                       f'class="pop" data-b="{b["cx"]:.1f} {b["cy"]:.1f} {b["r"]:.1f}"/>')
            continue
        d = el_d(a)
        boil = (f'<animate attributeName="d" values="{";".join([d] + [el_d(v) for v in _variants(a, seed + i)] + [d])}" '
                f'begin="indefinite"/>')
        if not ink(a):                                # backing / tint: lerped on the side
            piv = f' data-p="{b["pivot"][0]:.1f} {b["pivot"][1]:.1f}"' if "pivot" in b else ""
            out.append(f'<path d="{d}" class="pop"{fill} data-b="{el_d(b)}"{piv}>{boil}</path>')
        elif a["kind"] == "stroke":
            mid = f"m-{slug}-{i}"
            defs.append(f'<mask id="{mid}" maskUnits="userSpaceOnUse"><path d="{poly_d(centre(a), False)}" '
                        f'fill="none" stroke="#fff" stroke-width="{width(a) + 6:.0f}" stroke-linecap="round" '
                        f'stroke-linejoin="round" pathLength="1" class="draw" style="--i:{n_strokes}"/></mask>')
            out.append(f'<path d="{d}" mask="url(#{mid})" class="stroke ink">{boil}</path>')
            n_strokes += 1
        else:
            out.append(f'<path d="{d}" class="pop ink">{boil}</path>')
        if i == last_under:                           # morph layer sits above backings, below dots
            out.append('<g class="morph"></g>')
    if last_under < 0:
        out.insert(0, '<g class="morph"></g>')
    pop_delay = n_strokes * STAGGER_MS + DRAW_MS // 2
    cfg = htmlmod.escape(json.dumps(morph_cfg(slug, base, twin), separators=(",", ":")), quote=True)
    return (f'<svg viewBox="0 0 400 400" style="--pop:{pop_delay}ms" data-morph="{cfg}">'
            f'<defs>{"".join(defs)}</defs><g fill="currentColor">{"".join(out)}</g></svg>')


def _variants(el, seed):
    """Boil frames: the element re-drawn with a different hand wobble."""
    vs = []
    for k in range(1, VARIANTS + 1):
        v = copy.deepcopy(el)
        if el["kind"] == "stroke":
            v["L"], v["R"] = jitter(el["L"], k, seed), jitter(el["R"][::-1], k, seed)[::-1]
        else:
            v["pts"] = jitter(el["pts"], k, seed)
        vs.append(v)
    return vs


# Notion-style icon colours: name, light rgb, dark rgb, alpha. Gray is the style's own ink at 20%.
PALETTE = [("gray", "35 31 32", "237 232 225", .2), ("brown", "159 107 83", "186 133 111", .3),
           ("orange", "217 115 13", "199 125 72", .3), ("yellow", "203 145 47", "202 152 57", .3),
           ("green", "68 131 97", "82 158 114", .3), ("blue", "51 126 169", "94 135 201", .32),
           ("purple", "144 101 176", "157 104 211", .3), ("pink", "193 76 138", "209 87 150", .3),
           ("red", "212 76 71", "223 84 82", .3)]
TINT_CSS = "".join(f":root[data-tint={n}]{{--tl:{l};--td:{d};--ta:{a}}}\n" for n, l, d, a in PALETTE[1:])
TINT_BTNS = "".join(f'<button data-tint="{n if n != "gray" else ""}" style="--l:{l};--d:{d};--a:{a}" aria-label="{n.title()}" title="{n.title()}"></button>'
                    for n, l, d, a in PALETTE)

PAGE = """<!doctype html>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Notionaly spots __VER__ — animated</title>
<style>
:root{--paper:#fff;--ink:#231F20;--muted:#231F2099;--line:#231F2014;color-scheme:light}
:root[data-theme=dark]{--paper:#1a1918;--ink:#EDE8E1;--muted:#EDE8E199;--line:#EDE8E114;color-scheme:dark}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--paper:#1a1918;--ink:#EDE8E1;--muted:#EDE8E199;--line:#EDE8E114;color-scheme:dark}}
/* tint: the style's secondary-surface plane. Gray is ink at 20%; a picked colour swaps the triple. */
:root{--tl:35 31 32;--td:237 232 225;--ta:.2;--tint:rgb(var(--tl)/var(--ta))}
:root[data-theme=dark]{--tint:rgb(var(--td)/var(--ta))}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--tint:rgb(var(--td)/var(--ta))}}
__TINT_CSS__
.tints{display:flex;gap:6px;margin-right:10px}
/* a swatch is painted with exactly the tint the icons get — the muted Notion look, not the solid colour */
.tints button{--sw:rgb(var(--l)/var(--a));width:22px;height:22px;border-radius:50%;padding:0;border:2px solid var(--paper);background:var(--sw);box-shadow:0 0 0 1px var(--line)}
:root[data-theme=dark] .tints button{--sw:rgb(var(--d)/var(--a))}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]) .tints button{--sw:rgb(var(--d)/var(--a))}}
.tints button[aria-pressed=true]{background:var(--sw);border-color:var(--paper);box-shadow:0 0 0 1.5px var(--ink)}  /* outranks the mode buttons' solid pressed rule */
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 -apple-system,system-ui,sans-serif;padding:28px clamp(16px,4vw,48px) 64px;transition:background .25s,color .25s}
header{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between;margin-bottom:28px}
h1{font-size:19px;font-weight:600;margin:0;letter-spacing:-.01em}
h1 small{font-weight:400;color:var(--muted);margin-left:8px}
.ctl{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
button{font:inherit;color:var(--ink);background:none;border:1px solid var(--line);border-radius:8px;padding:6px 12px;cursor:pointer}
button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:12px}
.card{border:1px solid var(--line);border-radius:14px;padding:14px 12px 10px;text-align:center;cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent}
.card svg{width:100%;height:auto;display:block;aspect-ratio:1;overflow:visible}
.card span{display:block;font-size:12.5px;color:var(--muted);margin-top:4px}
.note{margin-top:32px;color:var(--muted);font-size:13px;max-width:62ch}

/* draw: the mask's centreline is dashed from 1 -> 0, stroke by stroke in authoring order */
.draw{stroke-dasharray:1;stroke-dashoffset:0}
[data-fx=draw] .card:is(:hover,.play) .draw{animation:draw __DRAW__ms cubic-bezier(.25,.1,.25,1) both;animation-delay:calc(var(--i)*__STAGGER__ms)}
[data-fx=draw] .card:is(:hover,.play) .pop{animation:pop .32s cubic-bezier(.2,.9,.3,1.3) both;animation-delay:var(--pop);transform-box:fill-box;transform-origin:center}
[data-fx=boil] .stroke{mask:none}
/* morph: the ink is re-rendered by the morph layer; the static ink and its masks step aside */
.morph{display:none}
[data-fx=morph] .morph{display:inline}
[data-fx=morph] .ink{display:none}
@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes pop{from{transform:scale(0);opacity:0}to{transform:scale(1);opacity:1}}
@media(prefers-reduced-motion:reduce){.draw,.pop{animation:none!important}}
</style>
<header>
  <h1>Notionaly spots __VER__<small>hover to play · __COUNT__ assets</small></h1>
  <div class="ctl">
    <div class="tints" role="group" aria-label="Icon colour">__TINT_BTNS__</div>
    <button data-fx="draw">Draw</button>
    <button data-fx="morph">Morph</button>
    <button data-fx="boil">Boil</button>
    <button id="theme" aria-label="Toggle dark mode" style="margin-left:8px">◐</button>
  </div>
</header>
<div class="grid">__CARDS__</div>
<p class="note"><b>Draw</b> replays each brush stroke in authoring order, then pops the masses and dots.
<b>Morph</b> is the OpCreative pattern on the real morphicons engine: every spot has a louder twin — the bulb
switches on, the envelope opens, the rocket launches — and springs into it while hovered. New lines peel off
the nearest existing one, rotation is solved from the geometry, and every frame the interpolated centrelines
are re-tapered into brush strokes. <b>Boil</b> steps between hand-jittered redraws at 6 fps — the classic
hand-drawn line boil. Same source SVGs as the PNGs. The <b>colour dots</b> tint every spot's secondary
surface — the ink-at-20% plane of the style; gray is the style itself, the rest are Notion's icon colours.</p>
<script>__MORPHICONS__</script>
<script>
const root=document.documentElement,q=new URLSearchParams(location.search);
let fx=q.get('fx')||'morph';
const setFx=v=>{fx=v;root.dataset.fx=v;document.querySelectorAll('[data-fx]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.fx===v))};
setFx(fx);
document.querySelectorAll('button[data-fx]').forEach(b=>b.onclick=()=>setFx(b.dataset.fx));
const theme=document.getElementById('theme');
try{if(localStorage.theme)root.dataset.theme=localStorage.theme}catch(e){}
if(q.get('theme'))root.dataset.theme=q.get('theme');
theme.onclick=()=>{const dark=root.dataset.theme?root.dataset.theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches;
  root.dataset.theme=dark?'light':'dark';try{localStorage.theme=root.dataset.theme}catch(e){}};
const tints=document.querySelectorAll('.tints button');
const setTint=v=>{if(v)root.dataset.tint=v;else delete root.dataset.tint;tints.forEach(b=>b.setAttribute('aria-pressed',b.dataset.tint===v));try{localStorage.tint=v}catch(e){}};
let tint='';try{tint=localStorage.tint||''}catch(e){}if(q.has('tint'))tint=q.get('tint');setTint(tint);
tints.forEach(b=>b.onclick=()=>setTint(b.dataset.tint));

/* ---- morph. Ink: morphicons (resample -> plan -> interpPolar), re-tapered per frame.
        Backings, tints, dots: index-paired, Procrustes + polar lerp of the same shape (a port of interpPolar). */
const MI=morphicons, NUM=/-?\\d*\\.?\\d+/g, nums=s=>s.match(NUM).map(Number), SVGNS='http://www.w3.org/2000/svg';
function taperD(o,[w0,w1,W]){ // sampled centreline -> closed brush outline, taper.py's envelope: ends w0/w1, peak W
  const n=o.length/2,L=[],R=[],w=W-(w0+w1)/2;
  for(let i=0;i<n;i++){const a=Math.max(i-1,0),b=Math.min(i+1,n-1),dx=o[2*b]-o[2*a],dy=o[2*b+1]-o[2*a+1],l=Math.hypot(dx,dy)||1,nx=-dy/l,ny=dx/l,t=i/(n-1);
    const h=(w*(i===0||i===n-1?0:Math.sqrt(Math.sin(Math.PI*t)))+w0*(1-t)+w1*t)/2;
    L.push((o[2*i]+nx*h).toFixed(1)+' '+(o[2*i+1]+ny*h).toFixed(1));R.push((o[2*i]-nx*h).toFixed(1)+' '+(o[2*i+1]-ny*h).toFixed(1))}
  return 'M'+L.join('L')+'L'+R.reverse().join('L')+'Z'}
const polyD=o=>{let d='M';for(let i=0;i<o.length;i+=2)d+=(i?'L':'')+o[i].toFixed(1)+' '+o[i+1].toFixed(1);return d+'Z'};
const centroid=a=>{let x=0,y=0;const n=a.length/2;for(let i=0;i<n;i++){x+=a[2*i]/n;y+=a[2*i+1]/n}return [x,y]};
const nearest=(c,cs)=>{let k=0,best=Infinity;for(let i=0;i<cs.length;i++){const d=(cs[i][0]-c[0])**2+(cs[i][1]-c[1])**2;if(d<best){best=d;k=i}}return k};
function annotate(plan,from,to,cfg){ // which source/target subpath each item came from: its width profile and pivot
  const fc=from.map(s=>centroid(s.pts)),tc=to.map(s=>centroid(s.pts));
  for(const it of plan.items){const si=nearest(it.ca,fc),di=nearest(centroid(it.bO),tc);
    it.pa=cfg.ws[si]||[8,8,12];it.pb=cfg.wt[di]||it.pa;
    const p=cfg.piv[si];if(it.block||!p)continue;           // morphicons' block term, from the twin table's pivot
    const s1=Math.exp(it.lnSigma),c1=Math.cos(it.theta)*s1,n1=Math.sin(it.theta)*s1,ox=it.ca[0]-p[0],oy=it.ca[1]-p[1];
    it.block={off:[ox,oy],drift:[it.cb[0]-it.ca[0]-(ox*c1-oy*n1-ox),it.cb[1]-it.ca[1]-(ox*n1+oy*c1-oy)]}}}
function plan(a,b,pivot){ // side elements: a, b flat [x,y,...] of equal length; pivot [x,y] or null
  const n=a.length/2,ca=centroid(a),cb=centroid(b);let sxx=0,syy=0,sxy=0,syx=0,na=0,nb=0;
  for(let i=0;i<n;i++){const ax=a[2*i]-ca[0],ay=a[2*i+1]-ca[1],bx=b[2*i]-cb[0],by=b[2*i+1]-cb[1];
    sxx+=ax*bx;syy+=ay*by;sxy+=ax*by;syx+=ay*bx;na+=ax*ax+ay*ay;nb+=bx*bx+by*by}
  const flat=na<1e-6||nb<1e-6,theta=flat?0:Math.atan2(sxy-syx,sxx+syy),lnS=flat?0:.5*Math.log(nb/na);
  const c=Math.cos(-theta)/Math.exp(lnS),s=Math.sin(-theta)/Math.exp(lnS),aC=new Float64Array(2*n),bT=new Float64Array(2*n);
  for(let i=0;i<n;i++){aC[2*i]=a[2*i]-ca[0];aC[2*i+1]=a[2*i+1]-ca[1];const bx=b[2*i]-cb[0],by=b[2*i+1]-cb[1];bT[2*i]=bx*c-by*s;bT[2*i+1]=bx*s+by*c}
  let block=null;if(pivot){const ox=ca[0]-pivot[0],oy=ca[1]-pivot[1],c1=Math.cos(theta)*Math.exp(lnS),s1=Math.sin(theta)*Math.exp(lnS);
    block={ox,oy,dx:cb[0]-ca[0]-(ox*c1-oy*s1-ox),dy:cb[1]-ca[1]-(ox*s1+oy*c1-oy)}}
  return {n,ca,cb,theta,lnS,aC,bT,block,out:new Float64Array(2*n)}}
function interp(p,t){const s=Math.exp(p.lnS*t),ang=p.theta*t,cos=Math.cos(ang)*s,sin=Math.sin(ang)*s;let cx,cy;
  if(p.block){const b=p.block;cx=p.ca[0]+b.dx*t+(b.ox*cos-b.oy*sin-b.ox);cy=p.ca[1]+b.dy*t+(b.ox*sin+b.oy*cos-b.oy)}
  else{cx=p.ca[0]+(p.cb[0]-p.ca[0])*t;cy=p.ca[1]+(p.cb[1]-p.ca[1])*t}
  for(let i=0;i<p.n;i++){const px=p.aC[2*i]+(p.bT[2*i]-p.aC[2*i])*t,py=p.aC[2*i+1]+(p.bT[2*i+1]-p.aC[2*i+1])*t;
    p.out[2*i]=cx+px*cos-py*sin;p.out[2*i+1]=cy+px*sin+py*cos}return p.out}
const K=420,C=30;                                         // morphicons "snappy": zeta 0.73
const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
const morphs=new Map();
for(const card of document.querySelectorAll('.card')){
  const svg=card.querySelector('svg'),cfg=JSON.parse(svg.dataset.morph),items=[];
  const from=MI.resampleIcon(cfg.from),to=MI.resampleIcon(cfg.to),pl=MI.buildPlan(from,to);
  annotate(pl,from,to,cfg);
  const g=svg.querySelector('.morph'),paths=pl.items.map(()=>g.appendChild(document.createElementNS(SVGNS,'path')));
  const mi={plan:pl,out:MI.allocOutputs(pl),paths};
  for(const p of svg.querySelectorAll('path[data-b]')){const d=p.getAttribute('d');
    items.push({el:p,tpl:d.split(NUM),pl:plan(nums(d),nums(p.dataset.b),p.dataset.p?nums(p.dataset.p):null)})}
  for(const c of svg.querySelectorAll('circle[data-b]')){
    items.push({el:c,dot:true,a:['cx','cy','r'].map(k=>+c.getAttribute(k)),b:nums(c.dataset.b)})}
  const m={mi,items,x:0,v:0,target:0,live:false};morphs.set(card,m);render(m);
}
function render(m){const t=m.x,{plan:pl,out,paths}=m.mi;MI.interpPolar(pl,t,out);
  for(let k=0;k<paths.length;k++){const it=pl.items[k];
    paths[k].setAttribute('d',it.closed?polyD(out[k]):taperD(out[k],it.pa.map((v,i)=>v+(it.pb[i]-v)*t)))}
  for(const it of m.items){
    if(it.dot){const [cx,cy,r]=it.a.map((v,i)=>v+(it.b[i]-v)*t);it.el.setAttribute('cx',cx);it.el.setAttribute('cy',cy);it.el.setAttribute('r',Math.max(0,r));continue}
    const o=interp(it.pl,t),tpl=it.tpl;let d=tpl[0];for(let i=0;i<o.length;i++)d+=o[i].toFixed(1)+tpl[i+1];it.el.setAttribute('d',d)}}
let last=0,raf=0;
function tick(now){const dt=Math.min(.064,(now-last)/1000||0);last=now;let any=false;
  for(const m of morphs.values()){if(!m.live)continue;
    const steps=Math.max(1,Math.min(16,Math.ceil(dt/(1/240)))),h=dt/steps;
    for(let i=0;i<steps;i++){m.v+=(K*(m.target-m.x)-C*m.v)*h;m.x+=m.v*h}
    if(Math.abs(m.target-m.x)<.001&&Math.abs(m.v)<.02){m.x=m.target;m.v=0;m.live=false}
    render(m);any=any||m.live}
  raf=any?requestAnimationFrame(tick):0}
const morphTo=(card,target)=>{const m=morphs.get(card);m.target=target;
  if(reduce){m.x=target;m.v=0;render(m);return}
  m.v=Math.max(-14,Math.min(14,m.v));m.live=true;if(!raf){last=performance.now();raf=requestAnimationFrame(tick)}};

/* ---- boil drives the SMIL <animate d>; draw is pure CSS on the masks */
const boil=(card,on)=>card.querySelectorAll('animate').forEach(a=>{if(!on)return a.endElement();
  a.setAttribute('calcMode','discrete');a.setAttribute('dur','.5s');a.setAttribute('repeatCount','indefinite');a.beginElement()});
const enter=card=>{if(fx==='morph')morphTo(card,1);else if(fx==='boil')boil(card,true)};
const leave=card=>{if(fx==='morph')morphTo(card,0);else if(fx==='boil')boil(card,false)};
document.querySelectorAll('.card').forEach(c=>{
  c.addEventListener('pointerenter',e=>{if(e.pointerType!=='touch')enter(c)});
  c.addEventListener('pointerleave',()=>leave(c));
  c.addEventListener('click',()=>{c.classList.add('play');enter(c);setTimeout(()=>{c.classList.remove('play');leave(c)},1600)});});
if(q.get('play'))document.querySelectorAll('.card').forEach(c=>{c.classList.add('play');enter(c)});
</script>
"""


def main():
    src = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
    out = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(src, "library.html")
    ver = os.path.basename(src).removeprefix("spots").lstrip("-")
    cards = []
    for f in sorted(glob.glob(os.path.join(src, "[0-9][0-9]-*.svg"))):
        slug = os.path.basename(f)[:-4]
        cards.append(f'<div class="card">{convert(open(f).read(), slug)}'
                     f'<span>{slug[3:].replace("-", " ")}</span></div>')
    engine = open(os.path.join(HERE, "morphicons.iife.js")).read()
    html = (PAGE.replace("__CARDS__", "".join(cards)).replace("__COUNT__", str(len(cards)))
            .replace("__DRAW__", str(DRAW_MS)).replace("__STAGGER__", str(STAGGER_MS))
            .replace("__MORPHICONS__", engine).replace("__VER__", ver).replace("__TINT_CSS__", TINT_CSS)
            .replace("__TINT_BTNS__", TINT_BTNS))
    shape = lambda s: re.sub(r"[^MLQZ]", "", s)
    for d, bd in re.findall(r'<path d="([^"]+)"[^>]*data-b="([^"]+)"', html):
        assert shape(d) == shape(bd), "side element and its twin diverged"
    for values in re.findall(r'<animate attributeName="d" values="([^"]+)"', html):
        assert len({shape(v) for v in values.split(";")}) == 1, "boil variants diverged"
    open(out, "w").write(html)
    print(f"{os.path.relpath(out)}: {len(cards)} spots, {len(TWINS)} twins, {len(html) // 1024} KB")
    # OpCreative's morph-pairs test, on the real engine: every pair must morph to a drawable path halfway
    bun = shutil.which("bun") or os.path.expanduser("~/.bun/bin/bun")
    if os.path.exists(bun):
        subprocess.run([bun, os.path.join(HERE, "check_morph.js"), out], check=True)
    else:
        print("bun not found — skipped check_morph.js")


if __name__ == "__main__":
    # self-check: a taper path round-trips to one decimal; extras live only in the twin
    d = stroke([(0, 0), (40, 10), (80, 0), (120, 20)], w=10)
    left, right_rev = parse_taper(d)
    assert len(left) == 4 and len(right_rev) == 4, "4 samples per side"
    shape = lambda s: re.sub(r"[^MLQZ]", "", s)
    nums = lambda s: [float(x) for x in re.findall(NUM, s)]
    rt = taper_d(left, right_rev)
    assert shape(rt) == shape(d) and all(abs(a - b) < 0.11 for a, b in zip(nums(rt), nums(d)))
    b, t = [], []
    add_stroke(b, t, [(10, 10), (50, 50)])
    assert (len(b), len(t)) == (0, 1) and ink(t[0]), "an extra is twin-only ink"
    assert parse(open(os.path.join(HERE, "09-camera.svg")).read())[7]["kind"] == "dot", "disc() parses as a dot"
    main()

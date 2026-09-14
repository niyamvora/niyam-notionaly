"""Notion-style spot illustrations, 400x400, ink #231F20. Built on skill/assets/taper.py."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "skill", "assets"))
from taper import stroke, arc, blob, svg

OUT = HERE
BASE, SWELL = 8.0, 4.0   # a brush stroke: ~8px at the ends, swelling to ~12 mid-run

def P(d, fill=None):
    return f'<path d="{d}"/>' if fill is None else f'<path d="{d}" fill="{fill}"/>'

def dot(x, y, r=5):
    return f'<circle cx="{x}" cy="{y}" r="{r}"/>'

def res(pts, n=20):
    """Resample a polyline to n evenly spaced points — taper needs samples to swell over."""
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

def line(pts, base=BASE, swell=SWELL, tip=False, n=20):
    """A brush stroke. tip=True points the far end (hands, teeth, flames)."""
    return P(stroke(res(pts, n), w=swell, w0=base, w1=0.0 if tip else base))

def loop(pts, base=BASE, swell=SWELL, gap=2):
    """A closed contour drawn as two runs with gaps — the style never seals a shape."""
    n, h = len(pts), len(pts) // 2
    return [P(stroke(pts[gap:h - gap], w=swell, w0=base, w1=base)),
            P(stroke(pts[h + gap:n - gap], w=swell, w0=base, w1=base))]

def ring(cx, cy, r, base=BASE, swell=SWELL, gap=13, wobble=1.8):
    return [P(stroke(arc(cx, cy, r, gap, 180 - gap / 2, wobble=wobble), w=swell, w0=base, w1=base)),
            P(stroke(arc(cx, cy, r, 180 + gap / 2, 360 - gap, wobble=wobble), w=swell, w0=base, w1=base))]

def disc(cx, cy, r):
    return P(f'M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0Z')

def poly(pts):
    """A closed solid mass with sharp corners — blob() smooths them into a leaf."""
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"

def rbox(x0, y0, x1, y1, r, n=7):
    return (res([(x0 + r, y0), (x1 - r, y0)], n) + arc(x1 - r, y0 + r, r, -90, 0, n=n)
            + res([(x1, y0 + r), (x1, y1 - r)], n) + arc(x1 - r, y1 - r, r, 0, 90, n=n)
            + res([(x1 - r, y1), (x0 + r, y1)], n) + arc(x0 + r, y1 - r, r, 90, 180, n=n)
            + res([(x0, y1 - r), (x0, y0 + r)], n) + arc(x0 + r, y0 + r, r, 180, 270, n=n))

def ellipse(cx, cy, rx, ry, n=40):
    return [(cx + rx * math.cos(math.radians(i * 360 / (n - 1))),
             cy + ry * math.sin(math.radians(i * 360 / (n - 1)))) for i in range(n)]

def write(name, parts):
    open(f"{OUT}/{name}.svg", "w").write(svg(400, parts))

# ---------------------------------------------------------------- 06 bicycle
write("06-bicycle", ring(122, 262, 54, base=7) + ring(288, 262, 54, base=7) + [
    line([(122, 262), (148, 208), (174, 158)], base=7),
    line([(174, 158), (214, 157), (254, 156)], base=7),
    line([(254, 156), (272, 206), (288, 262)], base=7),
    line([(205, 262), (230, 209), (254, 156)], base=7),
    line([(152, 150), (174, 148), (194, 149)], base=6, swell=3),
    line([(254, 156), (270, 144), (284, 139)], base=6, swell=3),
    dot(205, 262, 10), dot(74, 166, 5), dot(334, 148, 5), dot(196, 88, 4)])

# ------------------------------------------------------------ 07 paper-plane
write("07-paper-plane", [P(poly([(320, 94), (230, 308), (190, 206)])),
    line([(320, 94), (204, 130), (86, 170)]),
    line([(86, 170), (138, 188), (190, 206)]),
    line([(190, 206), (255, 150), (320, 94)]),
    dot(68, 258, 5), dot(110, 304, 4), dot(336, 176, 5), dot(256, 62, 4)])

# -------------------------------------------------------------- 08 lightbulb
write("08-lightbulb", [
    P(stroke(arc(200, 168, 72, 126, 414, wobble=2.2), w=SWELL, w0=BASE, w1=BASE)),
    line([(164, 230), (163, 246), (164, 258)], base=6, swell=3),
    line([(236, 230), (237, 246), (236, 258)], base=6, swell=3),
    P(blob([(167, 259), (233, 259), (230, 286), (170, 286)])),
    line([(176, 302), (200, 303), (224, 302)], base=6, swell=3),
    line([(184, 320), (200, 321), (216, 320)], base=6, swell=3),
    dot(82, 130, 5), dot(318, 116, 5), dot(96, 226, 4), dot(314, 236, 4)])

# ----------------------------------------------------------------- 09 camera
write("09-camera", loop(rbox(78, 144, 322, 298, 30)) + [
    line([(152, 146), (163, 118), (178, 108)], base=7),
    line([(178, 108), (212, 107), (246, 108)], base=7),
    line([(246, 108), (257, 120), (268, 146)], base=7)]
    + ring(200, 222, 52, base=7) + [disc(200, 222, 25), dot(288, 178, 8),
    dot(46, 106, 5), dot(354, 90, 4), dot(52, 322, 5)])

# --------------------------------------------------------------- 10 umbrella
write("10-umbrella", [
    P(stroke(arc(200, 218, 116, 181, 359, wobble=2.5), w=SWELL, w0=BASE, w1=BASE))]
    + [P(stroke(arc(114 + i * 57, 216, 28, 0, 180, n=14), w=3, w0=7, w1=7))
       for i in range(4)]
    + [line([(200, 224), (200, 278), (200, 314)], base=7),
       line([(200, 314), (195, 340), (164, 341)], base=7),
       dot(70, 102, 5), dot(332, 116, 5), dot(318, 302, 4), dot(88, 308, 4)])

# -------------------------------------------------------------------- 11 key
write("11-key", ring(150, 150, 60) + [disc(150, 150, 22),
    line([(193, 193), (250, 250), (306, 306)]),
    line([(266, 266), (252, 282), (238, 296)], base=6, swell=3),
    line([(292, 292), (278, 308), (264, 322)], base=6, swell=3),
    dot(302, 106, 5), dot(342, 168, 4), dot(72, 266, 5), dot(118, 318, 4)])

# --------------------------------------------------------------- 12 envelope
write("12-envelope", loop(rbox(74, 130, 326, 278, 22)) + [
    line([(80, 138), (140, 186), (200, 232)]),
    line([(200, 232), (262, 186), (320, 138)]),
    dot(54, 90, 5), dot(350, 102, 4), dot(44, 316, 5), dot(340, 322, 4)])

# --------------------------------------------------------------- 13 mountain
write("13-mountain", [P(poly([(216, 300), (277, 180), (338, 300)])),
    line([(88, 300), (137, 219), (186, 136), (222, 200), (258, 264)], n=32),
    line([(70, 305), (200, 307), (346, 305)], base=7),
    line([(162, 180), (186, 174), (210, 184)], base=6, swell=3),
    dot(80, 106, 5), dot(324, 88, 5), dot(124, 72, 4)])

# ----------------------------------------------------------------- 14 rocket
write("14-rocket", [
    line([(200, 74), (154, 170), (158, 268)], n=26),
    line([(200, 74), (246, 170), (242, 268)], n=26),
    line([(158, 268), (200, 275), (242, 268)], base=7)]
    + ring(200, 172, 33, base=7, gap=5) + [
    P(poly([(157, 210), (160, 266), (116, 300), (112, 248)])),
    P(poly([(243, 210), (240, 266), (284, 300), (288, 248)])),
    line([(182, 288), (200, 324), (218, 288)], base=6, swell=3),
    dot(88, 146, 5), dot(312, 128, 5), dot(200, 38, 4), dot(328, 220, 4)])

# ------------------------------------------------------------------ 15 globe
write("15-globe", ring(200, 200, 112, gap=8) + loop(ellipse(200, 200, 56, 110), base=7, gap=1)
    + [line([(90, 200), (200, 196), (310, 200)], base=7),
       dot(56, 86, 5), dot(348, 104, 4), dot(54, 332, 4), dot(344, 320, 5)])

print("ok")


# ------------------------------------------------------------------- 16 house
write("16-house", [
    line([(70, 200), (200, 86), (330, 200)], n=30),                  # roof
    line([(100, 192), (100, 318)], base=7), line([(300, 192), (300, 318)], base=7),
    line([(86, 320), (314, 320)]),
    P(poly([(172, 320), (172, 246), (228, 246), (228, 320)])),      # solid mass: door
    line(rbox(232, 218, 278, 262, 4, n=4) + [(236, 218)], base=6, swell=3, n=28),   # window: one run, a tiny loop has no room for gaps
] + [
    line([(262, 134), (262, 104)], base=7), line([(250, 102), (274, 102)], base=6),   # chimney
    dot(56, 122, 5), dot(346, 116, 5), dot(60, 302, 4), dot(344, 300, 4)])

# -------------------------------------------------------------------- 17 bell
write("17-bell", [
    line([(118, 262), (122, 200), (150, 120), (200, 96), (250, 120), (278, 200), (282, 262)], n=32),
    line([(96, 268), (304, 268)]),
    dot(200, 302, 13), dot(200, 88, 9),                              # clapper, knob
    dot(64, 160, 5), dot(336, 150, 5), dot(80, 318, 4), dot(326, 320, 4)])

# ------------------------------------------------------------------- 18 plant
write("18-plant", [
    line([(130, 238), (140, 322)], base=7), line([(270, 238), (260, 322)], base=7),
    line([(140, 324), (260, 324)], base=7), line([(116, 232), (284, 232)]),
    line([(200, 232), (200, 118)], base=7),
    P(blob([(200, 190), (150, 170), (122, 128), (160, 132)])),      # solid masses: leaves
    P(blob([(200, 160), (250, 140), (280, 96), (240, 102)])),
    P(blob([(200, 128), (180, 96), (200, 54), (222, 96)])),
    dot(70, 200, 5), dot(330, 210, 5), dot(96, 302, 4), dot(318, 306, 4)])

# ------------------------------------------------------------------ 19 laptop
write("19-laptop", loop(rbox(104, 96, 296, 236, 10), gap=1) + [
    line([(104, 242), (296, 242)], base=7), line([(70, 272), (330, 272)], base=9),
    dot(56, 140, 5), dot(344, 130, 5), dot(66, 316, 4), dot(334, 318, 4)])

# -------------------------------------------------------------- 20 headphones
write("20-headphones", [P(stroke(arc(200, 210, 120, 195, 345, wobble=2.0), w=SWELL, w0=BASE, w1=BASE))]
    + loop(rbox(70, 190, 126, 290, 16), base=7, gap=1) + loop(rbox(274, 190, 330, 290, 16), base=7, gap=1)
    + [dot(98, 240, 14), dot(302, 240, 14),                          # solid masses: cushions
       dot(60, 120, 5), dot(340, 118, 5), dot(200, 330, 4)])

# ------------------------------------------------------------------ 21 pencil
write("21-pencil", [
    line([(109, 269), (279, 99)]), line([(131, 291), (301, 121)]),
    P(poly([(86, 314), (109, 269), (131, 291)])),                    # solid mass: sharpened tip
    line([(279, 99), (301, 121)], base=7), line([(266, 112), (288, 134)], base=6),
    dot(60, 140, 5), dot(330, 60, 5), dot(64, 332, 4), dot(330, 300, 4)])

# ------------------------------------------------------------ 22 shopping-bag
write("22-shopping-bag", loop(rbox(100, 150, 300, 324, 12)) + [
    P(stroke(arc(200, 150, 50, 180, 360, n=20), w=3, w0=7, w1=7)),  # handle
    P(poly([(100, 150), (300, 150), (300, 182), (100, 182)])),      # solid mass: band
    dot(66, 120, 5), dot(334, 110, 5), dot(70, 300, 4), dot(332, 296, 4)])

# ------------------------------------------------------------- 23 chat-bubble
write("23-chat-bubble", loop(rbox(80, 100, 320, 264, 26)) + [
    line([(128, 262), (112, 304), (166, 262)], base=7, n=16),        # tail
    dot(150, 182, 11), dot(200, 182, 11), dot(250, 182, 11),         # solid masses: typing
    dot(56, 80, 5), dot(344, 70, 5), dot(340, 300, 4)])

# ----------------------------------------------------------------- 24 map-pin
pin = [(200, 318)] + arc(200, 170, 74, 140, 400, n=26) + [(200, 318)]
write("24-map-pin", [line(pin, n=44)] + [dot(200, 170, 26)]          # teardrop as one run, seam at the tip; solid mass: centre
    + loop(ellipse(200, 328, 60, 14), base=6, swell=2, gap=1)
    + [dot(70, 110, 5), dot(330, 120, 5), dot(90, 292, 4), dot(322, 282, 4)])

# ------------------------------------------------------------------ 25 trophy
write("25-trophy", [
    line([(118, 100), (122, 170), (150, 224), (200, 236), (250, 224), (278, 170), (282, 100)], n=32),
    line([(104, 98), (296, 98)]),
    P(stroke(arc(118, 150, 40, 90, 270, n=14), w=3, w0=6, w1=6)),   # handles
    P(stroke(arc(282, 150, 40, -90, 90, n=14), w=3, w0=6, w1=6)),
    line([(200, 236), (200, 286)]),
    P(poly([(140, 288), (260, 288), (272, 318), (128, 318)])),      # solid mass: base
    dot(66, 80, 5), dot(334, 70, 5), dot(72, 300, 4), dot(330, 296, 4)])

# ---------------------------------------------------------------- 26 calendar
write("26-calendar", loop(rbox(76, 108, 324, 316, 18)) + [
    P(poly(arc(306, 126, 18, -90, 0, n=6) + [(324, 162), (76, 162)] + arc(94, 126, 18, 180, 270, n=6))),  # solid mass: header band, flush with the page top
    line([(136, 76), (136, 128)], base=7), line([(264, 76), (264, 128)], base=7),   # binder rings
] + [dot(x, y, 8) for y in (212, 262) for x in (128, 176, 224, 272)]  # the month, as a grid
  + [dot(50, 168, 5), dot(350, 150, 5), dot(58, 328, 4), dot(344, 322, 4)])

# --------------------------------------------------------- 27 magnifying-glass
write("27-magnifying-glass", ring(170, 170, 96, base=9, gap=10) + [
    line([(240, 240), (326, 326)], base=14, swell=2),               # handle
    dot(316, 316, 18),                                              # solid mass: grip
    P(stroke(arc(170, 170, 62, 195, 245, n=10), w=2, w0=6, w1=4)),  # glint
    dot(66, 296, 5), dot(330, 72, 5), dot(72, 60, 4), dot(210, 340, 4)])

# ------------------------------------------------------------------- 28 book
write("28-book", [
    line([(200, 130), (200, 312)], base=7),                          # spine
    line([(72, 116), (120, 104), (200, 130), (280, 104), (328, 116)], n=30),     # top edge
    line([(72, 116), (72, 300)], base=7), line([(328, 116), (328, 300)], base=7),
    line([(72, 300), (124, 290), (200, 312)], n=16), line([(200, 312), (276, 290), (328, 300)], n=16),
    P(poly([(226, 128), (302, 106), (302, 152), (226, 174)])),      # solid mass: a read block
    line([(100, 176), (172, 196)], base=6, swell=2), line([(100, 210), (172, 230)], base=6, swell=2),
    line([(100, 244), (152, 258)], base=6, swell=2),
    dot(50, 82, 5), dot(350, 84, 5), dot(56, 322, 4), dot(346, 320, 4)])

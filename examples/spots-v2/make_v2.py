"""v2 of the spots: every spot gets a tint plane — the style's ink-at-20% "secondary surface" —
under its ink, so a colour picker can tint the set (library.html sets `--tint`).

v1 stays untouched in ../spots. Two ways a spot gets its plane:
  • 01-05 already carry white backing shapes for their main surface; those become the plane.
  • 06-15 have none, so a plane polygon is inserted first in the ink group, tagged class="plane"
    (build_library.py needs to know it is an insert, so the twin table's indices still hold).

    python3 make_v2.py      # writes NN-*.svg and NN-*.png here
"""
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(HERE, "..", "spots")
sys.path.insert(0, os.path.join(HERE, "..", "..", "skill", "assets"))
from taper import arc  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TINT = 'fill="#231F20" fill-opacity="0.2"'


def disc(cx, cy, r, n=32):
    return arc(cx, cy, r, 0, 360 - 360 / n, n=n)


def rbox(x0, y0, x1, y1, r, n=6):
    return (arc(x1 - r, y0 + r, r, -90, 0, n=n) + arc(x1 - r, y1 - r, r, 0, 90, n=n)
            + arc(x0 + r, y1 - r, r, 90, 180, n=n) + arc(x0 + r, y0 + r, r, 180, 270, n=n))


# element indices (file order) of white backings that become the plane
RECOLOUR = {"01-suitcase": [0], "02-clock": [0], "03-train": [0], "04-two-days": [0, 9], "05-coffee": [0, 5]}
# a backing whose shape never matched its surface (invisible while white): redraw it, same index
RESHAPE = {"05-coffee": {0: [(129, 158), (265, 158), (243, 320), (151, 320)]}}

# a plane polygon for the spots that have no backing: the object's main surface
PLANES = {
    "06-bicycle": [(122, 262), (174, 158), (254, 156), (205, 262)],            # frame
    "07-paper-plane": [(320, 94), (86, 170), (190, 206)],                       # near wing
    "08-lightbulb": disc(200, 168, 66),                                         # glass
    "09-camera": rbox(78, 144, 322, 298, 30),                                   # body
    "10-umbrella": arc(200, 216, 112, 180, 360, n=28),                          # canopy
    "11-key": disc(150, 150, 54),                                               # bow
    "12-envelope": rbox(74, 130, 326, 278, 22),                                 # body
    "13-mountain": [(90, 300), (186, 138), (257, 262), (240, 300)],             # near peak
    "14-rocket": [(200, 76), (154, 170), (158, 268), (242, 268), (246, 170)],  # hull
    "15-globe": disc(200, 200, 108),                                            # sphere
    "16-house": [(100, 196), (300, 196), (300, 320), (100, 320)],               # walls
    "17-bell": [(118, 262), (122, 200), (150, 120), (200, 96), (250, 120), (278, 200), (282, 262)],
    "18-plant": [(130, 236), (270, 236), (260, 324), (140, 324)],               # pot
    "19-laptop": rbox(104, 96, 296, 236, 10),                                   # screen
    "20-headphones": [rbox(70, 190, 126, 290, 16), rbox(274, 190, 330, 290, 16)],  # both cups
    "21-pencil": [(109, 269), (279, 99), (301, 121), (131, 291)],               # body
    "22-shopping-bag": [(100, 182), (300, 182), (300, 324), (100, 324)],        # bag
    "23-chat-bubble": rbox(80, 100, 320, 264, 26),                              # bubble
    "24-map-pin": [(200, 318)] + arc(200, 170, 74, 140, 400, n=20),             # pin
    "25-trophy": [(118, 100), (122, 170), (150, 224), (200, 236), (250, 224), (278, 170), (282, 100)],
}


def convert(slug, svg):
    head, body, tail = re.match(r"(.*?<g[^>]*>)(.*?)(</g>.*)", svg, re.S).groups()
    if slug in RECOLOUR:
        els = list(re.finditer(r"<(path|circle)[^>]*/>", body))
        for i in RECOLOUR[slug]:
            e = els[i].group(0)
            assert 'fill="#FFFFFF"' in e, f"{slug}[{i}] is not a white backing"
            new = e.replace('fill="#FFFFFF"', TINT)
            if pts := RESHAPE.get(slug, {}).get(i):
                new = re.sub(r'd="[^"]*"', 'd="M' + " L".join(f"{x} {y}" for x, y in pts) + ' Z"', new)
            body = body.replace(e, new, 1)
    else:
        planes = PLANES[slug]
        if isinstance(planes[0], tuple):              # one polygon, or a list of them
            planes = [planes]
        for pts in reversed(planes):
            d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
            body = f'\n  <path class="plane" d="{d}" {TINT}/>' + body
    return head + body + tail


def main():
    for f in sorted(os.listdir(V1)):
        if not re.match(r"\d\d-.*\.svg$", f):
            continue
        slug = f[:-4]
        out = convert(slug, open(os.path.join(V1, f)).read())
        assert out.count("fill-opacity") >= 1, slug
        open(os.path.join(HERE, f), "w").write(out)
        html = f'<style>body{{margin:0;background:#fff}}img{{width:300px;height:300px;display:block}}</style><img src="{HERE}/{f}">'
        open(os.path.join(HERE, "_r.html"), "w").write(html)
        subprocess.run([CHROME, "--headless", "--disable-gpu", f"--screenshot={HERE}/{slug}.png", "--window-size=300,300",
                        "--hide-scrollbars", f"file://{HERE}/_r.html"], capture_output=True)
    os.remove(os.path.join(HERE, "_r.html"))
    print("v2:", len([f for f in os.listdir(HERE) if f.endswith(".svg")]), "svgs")


if __name__ == "__main__":
    # self-check: the two routes both yield exactly one new tint on a minimal spot
    mini = '<svg><rect/><g fill="#231F20">\n  <path d="M0 0" fill="#FFFFFF"/>\n  <path d="M1 1"/>\n  </g></svg>'
    assert convert("01-suitcase", mini).count("fill-opacity") == 1
    assert convert("15-globe", mini).count('class="plane"') == 1
    main()

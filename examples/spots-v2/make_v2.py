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
RECOLOUR = {"01-suitcase": [0], "02-clock": [0], "03-train": [0], "04-two-days": [0, 9], "05-coffee": [0]}

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
}


def convert(slug, svg):
    head, body, tail = re.match(r"(.*?<g[^>]*>)(.*?)(</g>.*)", svg, re.S).groups()
    if slug in RECOLOUR:
        els = list(re.finditer(r"<(path|circle)[^>]*/>", body))
        for i in RECOLOUR[slug]:
            e = els[i].group(0)
            assert 'fill="#FFFFFF"' in e, f"{slug}[{i}] is not a white backing"
            body = body.replace(e, e.replace('fill="#FFFFFF"', TINT), 1)
    else:
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in PLANES[slug]) + " Z"
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

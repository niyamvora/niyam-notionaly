"""Tapered-stroke path generator for hand-authored Notion-style SVG.

SVG has no variable-width stroke, so every tapered line must be a closed filled
path. Computing those by hand produces dead, uniform-looking geometry — which is
the single most common way a hand-authored figure fails the style. Use this.

    from taper import stroke, arc, circle, blob, svg

    d = stroke([(10, 90), (50, 20), (95, 15)], w=9)
    print(svg(1024, [f'<path d="{d}"/>']))
"""
import math

INK = "#231F20"


def _norm(pts, i):
    """Unit normal to the centreline at point i."""
    a = pts[max(i - 1, 0)]
    b = pts[min(i + 1, len(pts) - 1)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1.0
    return -dy / L, dx / L


def _widths(n, w, w0, w1, bulge):
    """Half-width at each point: thin at the ends, fattest through the middle."""
    out = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0.5
        # exact 0 at the ends: sin(pi) is only ~1e-16, which leaves a blunt tail
        env = 0.0 if i in (0, n - 1) else math.sin(math.pi * t) ** bulge
        out.append((w * env + w0 * (1 - t) + w1 * t) / 2)
    return out


def _smooth(pts):
    """Quadratic-smoothed polyline through pts."""
    if len(pts) < 3:
        return " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}"
                        for i, (x, y) in enumerate(pts))
    d = [f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"]
    for i in range(1, len(pts) - 1):
        mx = (pts[i][0] + pts[i + 1][0]) / 2
        my = (pts[i][1] + pts[i + 1][1]) / 2
        d.append(f"Q{pts[i][0]:.1f} {pts[i][1]:.1f} {mx:.1f} {my:.1f}")
    d.append(f"L{pts[-1][0]:.1f} {pts[-1][1]:.1f}")
    return " ".join(d)


def stroke(pts, w=10, w0=0.0, w1=0.0, bulge=0.5):
    """One tapered stroke as a closed filled path.

    pts    centreline points
    w      peak stroke width through the middle
    w0/w1  width forced at the start/end (0 = a point, the default)
    bulge  <1 keeps it fat for longer, >1 makes a sharper spindle
    """
    ws = _widths(len(pts), w, w0, w1, bulge)
    ns = [_norm(pts, i) for i in range(len(pts))]
    left = [(p[0] + n[0] * t, p[1] + n[1] * t) for p, n, t in zip(pts, ns, ws)]
    right = [(p[0] - n[0] * t, p[1] - n[1] * t) for p, n, t in zip(pts, ns, ws)]
    return _smooth(left) + " " + _smooth(right[::-1])[1:].replace("M", "L", 1) + " Z"


def arc(cx, cy, r, a0, a1, n=36, wobble=0.0):
    """Points along an arc. Degrees. wobble adds a hand-drawn radius drift."""
    out = []
    for i in range(n):
        t = i / (n - 1)
        a = math.radians(a0 + (a1 - a0) * t)
        rr = r + (math.sin(t * 7.3) * wobble if wobble else 0.0)
        out.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return out


def circle(cx, cy, r, w=9, wobble=1.5, gap=14):
    """A hand-drawn circle: two tapered arcs with a small gap, as a pen would."""
    return [
        stroke(arc(cx, cy, r, gap, 180 - gap / 2, wobble=wobble), w=w, w0=w * .5, w1=w * .5),
        stroke(arc(cx, cy, r, 180 + gap / 2, 360 - gap, wobble=wobble), w=w, w0=w * .5, w1=w * .5),
    ]


def blob(pts):
    """A closed solid mass (hair, trousers, shoes) through smoothed points."""
    return _smooth(list(pts) + [pts[0]]) + " Z"


def svg(size, parts, fill=INK, background="#FFFFFF"):
    """Assemble an SVG. Solid white ground by default — transparent assets show as a
    checkerboard in most viewers. Pass background=None if you need to composite."""
    body = "\n  ".join(parts)
    bg = (f'  <rect id="bg" width="{size}" height="{size}" fill="{background}"/>\n'
          if background else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">\n'
            f'{bg}  <g fill="{fill}">\n  {body}\n  </g>\n</svg>\n')


if __name__ == "__main__":
    # self-check: a taper must be fat in the middle and pointed at both ends
    pts = [(0, 0), (50, 0), (100, 0)]
    ws = _widths(3, 20, 0, 0, 0.5)
    assert ws[0] == 0 and ws[-1] == 0, "ends must come to a point"
    assert ws[1] > ws[0] and ws[1] > ws[2], "middle must be widest"
    d = stroke(pts, w=20)
    assert d.startswith("M") and d.endswith("Z"), "must be a closed path"
    assert "Q" in d, "must be smoothed"
    assert len(circle(50, 50, 40)) == 2, "circle is two arcs with a gap"
    print("taper.py self-check passed")

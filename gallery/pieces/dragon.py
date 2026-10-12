import numpy as np
from PIL import Image, ImageDraw

from ..render import hex_rgb

TITLE = "Dragon Curves"
FORMULA = [
    "fold a strip of paper in half n times, unfold every crease to 90 degrees",
    "turn n is left if ((n & -n) << 1) & n == 0, else right",
]
PARAMS = "4 curves of 2^11 segments, rotated 90 degrees apart, corners cut"
CAPTION = (
    "Fold a strip of paper in half again and again, then open each fold to a "
    "right angle. The strip never crosses itself, and four copies turned a "
    "quarter turn apart fit together around a point with no gaps and no "
    "overlaps. Cutting each corner on a diagonal keeps neighboring turns "
    "from touching, so you can follow every strip from end to end."
)
KIND = "Plane-filling curve"
ABOUT = [
    (
        "NASA physicists John Heighway, Bruce Banks and William Harter found the "
        "dragon curve in the 1960s, and Martin Gardner wrote about it in his "
        "Mathematical Games column in 1967. It is the shape you get by folding a "
        "strip of paper in half again and again and opening every fold to a right "
        "angle."
    ),
    (
        "Each curve here has 2,047 segments, and the direction of every turn can "
        "be read straight off the binary digits of its position. Four copies "
        "turned a quarter turn apart fit around a common point with no gaps and "
        "no overlaps, and copies of the dragon can go on to tile the whole plane."
    ),
]

PALETTES = [
    ("#ffd166", "#ef476f"),
    ("#06d6a0", "#118ab2"),
    ("#f4a261", "#e76f51"),
    ("#a8dadc", "#457b9d"),
]


def dragon(n_segments):
    """Corner points of a dragon curve starting at the origin."""
    n = np.arange(1, n_segments)
    right = (((n & -n) << 1) & n) != 0
    turns = np.where(right, -1, 1)
    heading = np.concatenate([[0], np.cumsum(turns)]) % 4
    steps = np.array([1, 1j, -1, -1j])[heading]
    return np.concatenate([[0], np.cumsum(steps)])


def chamfer(pts):
    """Replace each corner with a short diagonal: keep the middle half of every segment."""
    a, b = pts[:-1], pts[1:]
    out = np.empty(2 * len(a), dtype=complex)
    out[0::2] = a + (b - a) * 0.25
    out[1::2] = a + (b - a) * 0.75
    return out


def render(size, seed=0):
    w, h = size
    ss = 2
    pts = dragon(2 ** 11)
    curves = [chamfer(pts * (1j ** i)) for i in range(4)]

    allpts = np.concatenate(curves)
    lo = complex(allpts.real.min(), allpts.imag.min())
    hi = complex(allpts.real.max(), allpts.imag.max())
    span = max(hi.real - lo.real, hi.imag - lo.imag)
    scale = 0.9 * min(w, h) * ss / span
    mid = (lo + hi) / 2

    img = Image.new("RGB", (w * ss, h * ss), "#101418")
    draw = ImageDraw.Draw(img)
    width = max(1, int(scale * 0.22))
    for curve, (c0, c1) in zip(curves, PALETTES):
        x = (curve.real - mid.real) * scale + w * ss / 2
        y = h * ss / 2 - (curve.imag - mid.imag) * scale
        c0, c1 = hex_rgb(c0), hex_rgb(c1)
        n = len(x) - 1
        for i in range(n):
            col = c0 + (c1 - c0) * (i / n)
            draw.line((x[i], y[i], x[i + 1], y[i + 1]), fill=tuple(int(v) for v in col), width=width)

    return img.resize((w, h), Image.LANCZOS)

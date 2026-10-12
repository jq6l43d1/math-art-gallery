import numpy as np
from PIL import Image, ImageDraw

from ..render import hex_rgb

TITLE = "Hilbert Curve"
FORMULA = [
    "H(n) = four copies of H(n - 1), two rotated, joined end to end",
]
PARAMS = "order 6: one line through all 4,096 cells of a 64 x 64 grid"
CAPTION = (
    "A single unbroken line that visits every square of a grid exactly "
    "once, built by joining four smaller copies of itself. Keep going and "
    "it fills the whole square. Color follows the line from start to "
    "finish, and the blocks show the useful part: cells that are close on "
    "the line are close on the page."
)

STOPS = ["#3a0ca3", "#4361ee", "#4cc9f0", "#80ed99", "#f9c74f", "#f8961e", "#f94144"]


def d2xy(order, d):
    """Position of step d along a Hilbert curve on a 2^order grid."""
    x = y = 0
    s = 1
    while s < 2 ** order:
        rx = 1 & (d // 2)
        ry = 1 & (d ^ rx)
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        d //= 4
        s *= 2
    return x, y


def render(size, seed=0):
    w, h = size
    order = 6
    n = 4 ** order
    side = 2 ** order
    ss = 3

    cell = 0.92 * min(w, h) * ss / side
    ox = (w * ss - cell * side) / 2 + cell / 2
    oy = (h * ss - cell * side) / 2 + cell / 2
    pts = [d2xy(order, d) for d in range(n)]
    xy = [(ox + x * cell, oy + (side - 1 - y) * cell) for x, y in pts]

    img = Image.new("RGB", (w * ss, h * ss), "#0b0b12")
    draw = ImageDraw.Draw(img)
    stops = [hex_rgb(c) for c in STOPS]
    width = int(cell * 0.45)
    for i in range(n - 1):
        t = i / (n - 1) * (len(stops) - 1)
        j = min(int(t), len(stops) - 2)
        col = tuple(int(v) for v in stops[j] + (stops[j + 1] - stops[j]) * (t - j))
        (x0, y0), (x1, y1) = xy[i], xy[i + 1]
        draw.line((x0, y0, x1, y1), fill=col, width=width)
        r = width / 2
        draw.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=col)

    return img.resize((w, h), Image.LANCZOS)

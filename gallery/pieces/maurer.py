import numpy as np
from PIL import Image

from ..render import Canvas, ink

TITLE = "Maurer Rose"
FORMULA = [
    "r = sin(n theta)",
    "connect the points at theta = k d degrees, k = 0..360",
]
PARAMS = "n = 6, d = 71"
CAPTION = (
    "Start with the rose curve r = sin(6 theta), then ignore it and walk "
    "around it in jumps of 71 degrees, joining each landing spot with a "
    "straight line. The rose (in red) is hidden inside its own web."
)
KIND = "Polar curve"
ABOUT = [
    (
        "Peter Maurer introduced these roses in a 1987 article in the American "
        "Mathematical Monthly. They start from the familiar rose curve, r = sin(n "
        "theta), but instead of tracing it smoothly they jump around it in fixed "
        "steps of d degrees and join each landing point with a straight line."
    ),
    (
        "The step size decides everything. Some values of d just retrace the rose "
        "with straight segments. Others, like 71 here, make the 361 points form a "
        "dense web that looks random but closes up perfectly. The rose itself is "
        "drawn on top in red so you can see what the web is built on."
    ),
]


def segments(xs, ys, per_unit):
    """Sample points densely along the polyline through xs, ys."""
    out_x, out_y = [], []
    for x0, y0, x1, y1 in zip(xs[:-1], ys[:-1], xs[1:], ys[1:]):
        n = max(2, int(np.hypot(x1 - x0, y1 - y0) * per_unit))
        s = np.linspace(0, 1, n)
        out_x.append(x0 + (x1 - x0) * s)
        out_y.append(y0 + (y1 - y0) * s)
    return np.concatenate(out_x), np.concatenate(out_y)


def render(size, seed=0):
    n, d = 6, 71
    k = np.arange(361)
    theta = np.radians(k * d)
    r = np.sin(n * theta)
    web = segments(r * np.cos(theta), r * np.sin(theta), per_unit=size[0] * 4)

    theta = np.linspace(0, 2 * np.pi, 4000)
    r = np.sin(n * theta)
    rose = segments(r * np.cos(theta), r * np.sin(theta), per_unit=size[0] * 8)

    bounds = (-1, 1, -1, 1)
    a = Canvas(size, bounds)
    a.add(*web)
    b = Canvas(size, bounds)
    b.add(*rose)

    img = np.asarray(ink(a.tone(gamma=0.6), paper="#fbfaf7", ink_color="#222222")).astype(float)
    red = np.array([200, 40, 40], dtype=float)
    t = b.tone(gamma=0.5)[..., None]
    img = img * (1 - t) + red * t
    return Image.fromarray(img.astype(np.uint8))

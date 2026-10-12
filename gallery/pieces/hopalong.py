import math

import numpy as np

from ..render import Canvas, bounds_of, glow

TITLE = "Hopalong"
FORMULA = [
    "x' = y - sign(x) sqrt(|b x - c|)",
    "y' = a - x",
]
PARAMS = "a = 1.1, b = 0.5, c = 1, 4 million steps from (0, 0), colored by time"
CAPTION = (
    "One point hops around the plane four million times. It never repeats, "
    "but it keeps returning to the same family of tiles, and coloring it by "
    "time shows the pattern slowly growing outward."
)
KIND = "Orbit of a map"
ABOUT = [
    (
        "Barry Martin of Aston University devised this map, and A. K. Dewdney "
        "featured it in his Computer Recreations column in Scientific American in "
        "1986 under the name Hopalong."
    ),
    (
        "Unlike the attractors elsewhere in the gallery, the picture depends on "
        "where the point starts, so this is a single orbit computed four million "
        "times in a plain loop. The orbit is cut into six equal stretches of "
        "time, each drawn in its own color, so you can see how the pattern "
        "spreads as the point keeps hopping."
    ),
]

COLORS = ["#ff4d6d", "#ffb347", "#f9f871", "#4dd599", "#4da6ff", "#b46bff"]


def render(size, seed=0):
    a, b, c = 1.1, 0.5, 1.0
    steps = 4_000_000

    # The orbit depends on where it starts, so the walker trick from the
    # attractors doesn't apply. A plain loop over floats is fast enough.
    xs = np.empty(steps)
    ys = np.empty(steps)
    x = y = 0.0
    sqrt, copysign = math.sqrt, math.copysign
    for i in range(steps):
        x, y = y - copysign(sqrt(abs(b * x - c)), x), a - x
        xs[i] = x
        ys[i] = y

    bounds = bounds_of(xs, ys, 0.001, 0.999)
    layers = []
    for chunk, color in zip(np.array_split(np.arange(steps), len(COLORS)), COLORS):
        canvas = Canvas(size, bounds, margin=0.04)
        canvas.add(xs[chunk], ys[chunk])
        layers.append((canvas.tone(gamma=0.9) * 0.85, color))
    return glow(layers, background="#0d0d12")

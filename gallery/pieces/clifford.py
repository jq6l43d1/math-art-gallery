import numpy as np

from ..maps import iterate
from ..render import ink

TITLE = "Clifford Attractor"
FORMULA = [
    "x' = sin(a y) + c cos(a x)",
    "y' = sin(b x) + d cos(b y)",
]
PARAMS = "a = -1.3, b = -1.3, c = -1.8, d = -1.9, 10 million points"
CAPTION = (
    "Two lines of trigonometry, iterated ten million times. Each point is "
    "computed from the one before it, and the orbit never settles into a "
    "repeating loop, yet it always traces the same tangle of ribbons. Darker "
    "ink means more visits."
)


def render(size, seed=0):
    a, b, c, d = -1.3, -1.3, -1.8, -1.9

    def step(x, y):
        return np.sin(a * y) + c * np.cos(a * x), np.sin(b * x) + d * np.cos(b * y)

    canvas = iterate(step, size, total=10_000_000, seed=seed)
    return ink(canvas.tone(gamma=0.8), paper="#efdfd3", ink_color="#111111")

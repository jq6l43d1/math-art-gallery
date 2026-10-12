import numpy as np

from ..maps import iterate
from ..render import gradient

TITLE = "Peter de Jong Attractor"
FORMULA = [
    "x' = sin(a y) - cos(b x)",
    "y' = sin(c x) - cos(d y)",
]
PARAMS = "a = 1.4, b = -2.3, c = 2.4, d = -2.1, 12 million points"
CAPTION = (
    "A close cousin of the Clifford map with the cosines subtracted instead "
    "of added. The same idea, a different personality: it folds into smoke "
    "instead of ribbons. Rendered like a long exposure of light on black."
)


def render(size, seed=0):
    a, b, c, d = 1.4, -2.3, 2.4, -2.1

    def step(x, y):
        return np.sin(a * y) - np.cos(b * x), np.sin(c * x) - np.cos(d * y)

    canvas = iterate(step, size, total=12_000_000, seed=seed)
    t = canvas.tone(gamma=0.9)
    return gradient(t, ["#05060a", "#1b2a4a", "#3f6fa8", "#a9d3f0", "#ffffff"])

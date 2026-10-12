import numpy as np

from ..render import Canvas, gradient

TITLE = "Barnsley Fern"
FORMULA = [
    "pick one of four affine maps at random",
    "(x, y) -> A (x, y) + b",
]
PARAMS = "4 maps chosen with probability 1%, 85%, 7%, 7%, 8 million points"
CAPTION = (
    "A fern drawn by rolling dice. Each map is a simple stretch, rotate and "
    "shift; one makes the stem, one makes each leaf a smaller copy of the "
    "whole, and two make the first left and right leaflets."
)

# Each row: a, b, c, d, e, f, probability
MAPS = np.array([
    [0.00, 0.00, 0.00, 0.16, 0.0, 0.00, 0.01],
    [0.85, 0.04, -0.04, 0.85, 0.0, 1.60, 0.85],
    [0.20, -0.26, 0.23, 0.22, 0.0, 1.60, 0.07],
    [-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07],
])


def render(size, seed=0):
    rng = np.random.default_rng(seed)
    walkers, steps = 200_000, 40
    x = np.zeros(walkers)
    y = np.zeros(walkers)
    a, b, c, d, e, f, p = MAPS.T

    def step(x, y):
        k = rng.choice(4, size=walkers, p=p)
        return a[k] * x + b[k] * y + e[k], c[k] * x + d[k] * y + f[k]

    for _ in range(20):
        x, y = step(x, y)
    canvas = Canvas(size, (-2.2, 2.7, 0, 10))
    for _ in range(steps):
        x, y = step(x, y)
        canvas.add(x, y)

    t = canvas.tone(gamma=0.8)
    return gradient(t, ["#0e1a12", "#1f4d2b", "#4f9a45", "#b9e07a", "#f4ffd8"])

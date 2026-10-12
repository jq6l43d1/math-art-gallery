import numpy as np

from ..maps import iterate
from ..render import gradient

TITLE = "Ikeda Map"
FORMULA = [
    "t = 0.4 - 6 / (1 + x^2 + y^2)",
    "x' = 1 + u (x cos t - y sin t)",
    "y' = u (x sin t + y cos t)",
]
PARAMS = "u = 0.9, 10 million points"
CAPTION = (
    "A model of light circling a ring-shaped laser cavity, losing a little "
    "energy and picking up a twist on every lap. The twist depends on how "
    "far from the center the light is, which is enough to fold the orbit "
    "into this curling wave."
)
KIND = "Strange attractor"
ABOUT = [
    (
        "Kensuke Ikeda proposed this map in 1979 to describe light travelling "
        "around a ring cavity that contains a nonlinear material, the kind of "
        "setup found inside some lasers. Each step is one trip around the ring: "
        "the light loses some energy (the factor u) and its phase shifts by an "
        "amount that depends on its intensity."
    ),
    (
        "At u = 0.9 the attractor shares the plane with a stable fixed point, and "
        "some starting points spiral into that instead. For this render, any "
        "point that has stopped moving after the warm-up is thrown away, leaving "
        "only the curling attractor."
    ),
]


def render(size, seed=0):
    u = 0.9

    def step(x, y):
        t = 0.4 - 6 / (1 + x * x + y * y)
        return 1 + u * (x * np.cos(t) - y * np.sin(t)), u * (x * np.sin(t) + y * np.cos(t))

    canvas = iterate(step, size, total=10_000_000, burn=300, drop_fixed=True, seed=seed)
    return gradient(canvas.tone(gamma=0.9), ["#061417", "#0b3d3a", "#1f8a70", "#bfe3c0", "#ffffff"])

"""Run a 2D iterated map with many walkers at once.

A strange attractor doesn't care where you start, so instead of following one
point for 10 million steps (slow in Python), I follow 200,000 points for 50
steps each. Every walker lands on the same attractor after a short burn-in,
and each step is a single vectorized numpy operation.
"""

import numpy as np

from .render import Canvas, bounds_of


def iterate(step, size, total=10_000_000, walkers=200_000, burn=40, seed=0, drop_fixed=False):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1, 1, walkers)
    y = rng.uniform(-1, 1, walkers)
    for _ in range(burn):
        x, y = step(x, y)

    if drop_fixed:
        # Some maps also have a stable fixed point next to the attractor.
        # Walkers that fell into it sit still; throw them away.
        nx, ny = step(x, y)
        moving = np.hypot(nx - x, ny - y) > 1e-6
        x, y = x[moving], y[moving]
        walkers = x.size

    canvas = Canvas(size, bounds_of(x, y))
    for _ in range(max(1, total // walkers)):
        x, y = step(x, y)
        canvas.add(x, y)
    return canvas

import numpy as np

from ..render import Canvas, glow

TITLE = "Buddhabrot"
FORMULA = [
    "z' = z^2 + c,  z_0 = 0",
    "plot every z along the orbits that escape",
]
PARAMS = "12 million samples of c; orbits escaping in 200-1000 steps paint orange, 40-200 green, 8-40 blue"
CAPTION = (
    "The Mandelbrot set turned inside out. Instead of coloring each c by "
    "whether it escapes, I follow the points that do escape and plot every "
    "place their orbit visits on the way out. Slow escapes paint orange, "
    "quick ones blue. Turned on its side, a seated figure appears."
)
KIND = "Escape-time fractal"
ABOUT = [
    (
        "Melinda Green described this technique in 1993. The usual picture of the "
        "Mandelbrot set throws away the path each point takes on its way to "
        "infinity and keeps only the step count. The Buddhabrot keeps the paths "
        "and stacks them up, revealing a figure that was hiding in the same "
        "equation all along."
    ),
    (
        "Giving orbits of different lengths their own colors is called a "
        "Nebulabrot, because the result looks like a space telescope photo. "
        "Twelve million random values of c are tested; only those that escape "
        "after at least 8 steps are replayed and drawn. It is the slowest piece "
        "in the gallery by far."
    ),
]

# (shortest escape, longest escape, color)
BANDS = [(200, 1000, "#ff8a50"), (40, 200, "#6fe3a0"), (8, 40, "#4f7dff")]


def outside_main_bulbs(c):
    """Skip points that obviously never escape (cardioid and period-2 bulb)."""
    q = (c.real - 0.25) ** 2 + c.imag ** 2
    cardioid = q * (q + (c.real - 0.25)) <= 0.25 * c.imag ** 2
    bulb = (c.real + 1) ** 2 + c.imag ** 2 <= 0.0625
    return ~(cardioid | bulb)


def escape_times(c, max_iter):
    z = np.zeros_like(c)
    n = np.full(c.shape, max_iter)
    alive = np.ones(c.shape, dtype=bool)
    for i in range(max_iter):
        idx = np.flatnonzero(alive)
        if idx.size == 0:
            break
        z[idx] = z[idx] ** 2 + c[idx]
        out = idx[np.abs(z[idx]) > 2]
        n[out] = i
        alive[out] = False
    return n


def render(size, seed=0):
    rng = np.random.default_rng(seed)
    # Real axis runs vertically so the figure sits upright.
    canvases = [Canvas(size, (-1.3, 1.3, -0.75, 2.05), margin=0.03) for _ in BANDS]
    max_iter = BANDS[0][1]

    for _ in range(12):
        c = rng.uniform(-2, 1, 1_000_000) + 1j * rng.uniform(-1.4, 1.4, 1_000_000)
        c = c[outside_main_bulbs(c)]
        n = escape_times(c, max_iter)
        keep = (n >= BANDS[-1][0]) & (n < max_iter)
        c, n = c[keep], n[keep]

        # Second pass: replay only the escaping orbits and splat each step.
        z = np.zeros_like(c)
        for i in range(n.max() + 1):
            live = n >= i
            if not live.all():
                c, n, z = c[live], n[live], z[live]
            z = z ** 2 + c
            for canvas, (lo, hi, _) in zip(canvases, BANDS):
                m = (n >= lo) & (n < hi)
                if m.any():
                    canvas.add(z.imag[m], -z.real[m])

    # Linear scaling here: the log curve that suits the attractors washes
    # this one out to a white blob.
    layers = [(cv.tone(clip=0.9995, log=False), col) for cv, (_, _, col) in zip(canvases, BANDS)]
    return glow(layers, background="#05040a")

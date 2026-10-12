import numpy as np

from ..flows import trace
from ..render import Canvas, bounds_of, gradient

TITLE = "Aizawa Attractor"
FORMULA = [
    "dx/dt = (z - b) x - d y",
    "dy/dt = d x + (z - b) y",
    "dz/dt = c + a z - z^3/3 - (x^2 + y^2)(1 + e z) + f z x^3",
]
PARAMS = "a = 0.95, b = 0.7, c = 0.6, d = 3.5, e = 0.25, f = 0.1, 300 particles"
CAPTION = (
    "Particles spiral around a sphere-like shell, get pulled up a narrow "
    "tube through the middle, and spill back over the top. Seen from the "
    "side and slightly above, the paths look like a spun-glass apple."
)
KIND = "Chaotic flow"
ABOUT = [
    (
        "This system is usually credited to Yoji Aizawa. The first two equations "
        "spin each particle around the vertical axis at a constant speed while "
        "pushing it in or out depending on its height; the third equation "
        "controls the height. Together they wrap the paths around a shell and "
        "send them up the central tube."
    ),
    (
        "Three hundred particles are each followed for 24 time units after a "
        "warm-up. Every step is split into smaller pieces so the paths render as "
        "continuous threads rather than dots. The camera is tilted slightly so "
        "you can see into the top of the shell."
    ),
]


def render(size, seed=0):
    rng = np.random.default_rng(seed)
    a, b, c, d, e, f_ = 0.95, 0.7, 0.6, 3.5, 0.25, 0.1

    def f(p):
        x, y, z = p
        return np.array([
            (z - b) * x - d * y,
            d * x + (z - b) * y,
            c + a * z - z ** 3 / 3 - (x * x + y * y) * (1 + e * z) + f_ * z * x ** 3,
        ])

    start = rng.normal(0, 0.1, (3, 300)) + np.array([[0.1], [0], [0]])
    path = trace(f, start, dt=0.004, steps=6_000, burn=2000, sub=4)

    # Tip the view toward the camera so the top opening shows.
    tilt = 0.35
    x = path[0]
    y = path[2] * np.cos(tilt) + path[1] * np.sin(tilt)

    canvas = Canvas(size, bounds_of(x, y, 0, 1), margin=0.08)
    canvas.add(x, y)
    return gradient(canvas.tone(gamma=0.9), ["#0a0f1f", "#20305a", "#c08a3e", "#ffe2a8", "#fffaf0"])

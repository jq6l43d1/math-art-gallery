import numpy as np

from ..render import Canvas, bounds_of, ink

TITLE = "Harmonograph"
FORMULA = [
    "x(t) = e^(-d1 t) sin(f1 t + p1) + e^(-d2 t) sin(f2 t + p2)",
    "y(t) = e^(-d3 t) sin(f3 t + p3) + e^(-d4 t) sin(f4 t + p4)",
]
PARAMS = "f = 3, 2, 3, 2.006, damping around 0.005 per second"
CAPTION = (
    "A Victorian drawing machine in software: a pen moved by swinging "
    "pendulums that slowly lose energy. Frequencies close to a simple ratio, "
    "but not quite, make the figure drift and spiral inward."
)


def render(size, seed=0):
    t = np.linspace(0, 500, 6_000_000)
    f = [3.0, 2.0, 3.0, 2.006]
    p = [0.0, np.pi / 2, np.pi / 2, 0.0]
    d = [0.004, 0.005, 0.0045, 0.0055]

    x = np.exp(-d[0] * t) * np.sin(f[0] * t + p[0]) + np.exp(-d[1] * t) * np.sin(f[1] * t + p[1])
    y = np.exp(-d[2] * t) * np.sin(f[2] * t + p[2]) + np.exp(-d[3] * t) * np.sin(f[3] * t + p[3])

    canvas = Canvas(size, bounds_of(x, y, 0, 1))
    canvas.add(x, y)
    return ink(canvas.tone(gamma=0.7), paper="#f6f1e7", ink_color="#1d3557")

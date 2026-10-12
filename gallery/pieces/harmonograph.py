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
KIND = "Damped oscillation"
ABOUT = [
    (
        "Harmonographs were a popular parlor device in the Victorian era: a table "
        "with pendulums underneath, some swinging a pen and others swinging the "
        "paper. Friction slowly drains the swing, so the figure shrinks toward "
        "the center as it is drawn."
    ),
    (
        "Here each axis is the sum of two damped sine waves. Frequencies of 3 and "
        "2 alone would trace a stable figure over and over. Detuning one of them "
        "to 2.006 makes the figure rotate a little on every pass, which turns a "
        "single shape into layered petals. Six million points along the curve are "
        "counted into pixels, so overlapping strokes darken like real ink."
    ),
]


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

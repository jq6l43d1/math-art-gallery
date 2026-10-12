import numpy as np

from ..flows import trace
from ..render import Canvas, bounds_of, ink

TITLE = "Lorenz Attractor"
FORMULA = [
    "dx/dt = s (y - x)",
    "dy/dt = x (r - z) - y",
    "dz/dt = x y - b z",
]
PARAMS = "s = 10, r = 28, b = 8/3, RK4 with dt = 0.002, 6 trajectories"
CAPTION = (
    "Edward Lorenz's simplified weather model, the original butterfly. "
    "Six particles start a hair apart and are carried along the flow. "
    "Within seconds they disagree completely about where they are, but all "
    "of them keep circling the same two wings."
)
KIND = "Chaotic flow"
ABOUT = [
    (
        "In 1963 the meteorologist Edward Lorenz reduced a model of atmospheric "
        "convection to three equations and found that tiny differences in the "
        "starting conditions grew until two forecasts had nothing in common. That "
        "observation, later nicknamed the butterfly effect, helped start the "
        "field of chaos theory."
    ),
    (
        "Here six particles begin about a thousandth of a unit apart, and each is "
        "integrated with the fourth-order Runge-Kutta method for 80 time units. "
        "Every step is split into twelve smaller pieces so the fast outer loops "
        "draw as smooth lines instead of dots. The view is turned slightly so the "
        "two wings don't overlap."
    ),
]


def render(size, seed=0):
    rng = np.random.default_rng(seed)
    s, r, b = 10.0, 28.0, 8.0 / 3.0
    n, dt = 6, 0.002

    def f(p):
        x, y, z = p
        return np.array([s * (y - x), x * (r - z) - y, x * y - b * z])

    start = np.array([[1.0], [1.0], [20.0]]) + rng.normal(0, 1e-3, (3, n))
    path = trace(f, start, dt, steps=40_000)

    # Rotate slightly so the two wings don't sit flat on top of each other.
    angle = 0.55
    x = path[0] * np.cos(angle) + path[1] * np.sin(angle)
    y = path[2]

    canvas = Canvas(size, bounds_of(x, y, 0, 1), margin=0.08)
    canvas.add(x, y)

    return ink(canvas.tone(gamma=0.6), paper="#f3efe6", ink_color="#8a1c1c")

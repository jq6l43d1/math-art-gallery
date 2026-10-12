import numpy as np

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


def render(size, seed=0):
    rng = np.random.default_rng(seed)
    s, r, b = 10.0, 28.0, 8.0 / 3.0
    n, dt = 6, 0.002

    def f(p):
        x, y, z = p
        return np.array([s * (y - x), x * (r - z) - y, x * y - b * z])

    def rk4(p):
        k1 = f(p)
        k2 = f(p + dt / 2 * k1)
        k3 = f(p + dt / 2 * k2)
        k4 = f(p + dt * k3)
        return p + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    p = np.array([[1.0], [1.0], [20.0]]) + rng.normal(0, 1e-3, (3, n))
    for _ in range(1000):
        p = rk4(p)

    # Rotate slightly so the two wings don't sit flat on top of each other.
    angle = 0.55
    view = lambda q: (q[0] * np.cos(angle) + q[1] * np.sin(angle), q[2])

    steps = 40_000
    path = np.empty((steps, 3, n))
    for i in range(steps):
        p = rk4(p)
        path[i] = p

    # Fast parts of the orbit move several pixels per step, so fill the gaps
    # between consecutive samples to get continuous strokes instead of dots.
    sub = np.linspace(0, 1, 12, endpoint=False)[:, None, None, None]
    path = (path[:-1] + (path[1:] - path[:-1]) * sub).transpose(2, 1, 0, 3).reshape(3, -1)

    x, y = view(path)
    canvas = Canvas(size, bounds_of(x, y, 0, 1), margin=0.08)
    canvas.add(x, y)

    return ink(canvas.tone(gamma=0.6), paper="#f3efe6", ink_color="#8a1c1c")

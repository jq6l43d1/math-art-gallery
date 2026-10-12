import numpy as np
from PIL import Image

from ..render import gradient

TITLE = "Gray-Scott Reaction-Diffusion"
FORMULA = [
    "du/dt = Du lap(u) - u v^2 + F (1 - u)",
    "dv/dt = Dv lap(v) + u v^2 - (F + k) v",
]
PARAMS = "Du = 0.16, Dv = 0.08, F = 0.029, k = 0.057, 10,000 steps on a 300 x 300 grid"
CAPTION = (
    "Two imaginary chemicals: one is fed in, the other eats it and "
    "reproduces. Both spread out, at different speeds. Starting from a few "
    "random specks, that balance grows into the same maze-like stripes you "
    "see on fish, coral and fingerprints."
)


def laplacian(a):
    return (np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1) - 4 * a)


def render(size, seed=0):
    rng = np.random.default_rng(seed)
    n = 300
    du, dv, feed, kill = 0.16, 0.08, 0.029, 0.057

    u = np.ones((n, n))
    v = np.zeros((n, n))
    for _ in range(18):
        cx, cy = rng.integers(20, n - 20, 2)
        r = rng.integers(3, 8)
        u[cy - r:cy + r, cx - r:cx + r] = 0.5
        v[cy - r:cy + r, cx - r:cx + r] = 0.25

    for _ in range(10_000):
        uvv = u * v * v
        u += du * laplacian(u) - uvv + feed * (1 - u)
        v += dv * laplacian(v) + uvv - (feed + kill) * v

    t = np.clip(v / v.max(), 0, 1)
    small = gradient(t, ["#fdf6ec", "#f2c6a0", "#d1495b", "#3d1e3c"])
    return small.resize(size, Image.BICUBIC)

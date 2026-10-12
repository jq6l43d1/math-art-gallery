import numpy as np
from PIL import Image

from ..render import hex_rgb

TITLE = "Newton Fractal"
FORMULA = [
    "z' = z - p(z) / p'(z)",
    "p(z) = z^3 - 1",
]
PARAMS = "60 iterations, colored by which root each point reaches"
CAPTION = (
    "Newton's method finds roots by sliding down tangent lines. Start it "
    "everywhere on the complex plane and color each point by which of the "
    "three cube roots of 1 it lands on. Between any two colors, the third "
    "always squeezes in, forever."
)
KIND = "Basins of attraction"
ABOUT = [
    (
        "Newton's method is a 17th century technique for finding where a function "
        "equals zero: make a guess, follow the tangent line down to where it "
        "crosses zero, and repeat. For most starting points it homes in quickly. "
        "In 1879 Arthur Cayley asked which root each starting point in the "
        "complex plane would reach, and found the question surprisingly hard for "
        "cubics."
    ),
    (
        "This picture is the answer. Each color is one root of z^3 - 1, and the "
        "shading shows how many steps it took to get there. The boundaries are "
        "fractal: anywhere two colors meet, the third is also present, no matter "
        "how far you zoom in."
    ),
]

COLORS = ["#e4572e", "#2e86ab", "#f3a712"]


def render(size, seed=0):
    w, h = size
    max_iter = 60
    xs = np.linspace(-1.5, 1.5, w)
    ys = np.linspace(-1.5, 1.5, h)
    z = xs[None, :] + 1j * ys[:, None]

    roots = np.exp(2j * np.pi * np.arange(3) / 3)
    which = np.full(z.shape, -1)
    steps = np.zeros(z.shape)

    for i in range(max_iter):
        z = z - (z ** 3 - 1) / (3 * z ** 2 + 1e-12)
        for k, r in enumerate(roots):
            hit = (which < 0) & (np.abs(z - r) < 1e-4)
            which[hit] = k
            steps[hit] = i

    colors = np.array([hex_rgb(c) for c in COLORS])
    rgb = colors[np.clip(which, 0, 2)]
    # Points that take longer to settle get darker, which outlines the basins.
    shade = np.exp(-steps / 14)[..., None]
    rgb = rgb * (0.15 + 0.85 * shade)
    rgb[which < 0] = 0
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))

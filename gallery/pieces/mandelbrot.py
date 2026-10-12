import numpy as np
from PIL import Image

TITLE = "Seahorse Valley"
FORMULA = [
    "z' = z^2 + c,  z_0 = 0",
    "c = the pixel",
]
PARAMS = "centered on -0.7453 + 0.1127i, about 1/500th the width of the full set, 1,500 iterations"
CAPTION = (
    "A zoom into the Mandelbrot set, in the crease between its main body and "
    "the big round bulb to the left. Every swirl here is made of smaller "
    "swirls, and tiny complete copies of the whole set are hidden along "
    "the filaments."
)
KIND = "Escape-time fractal"
ABOUT = [
    (
        "Benoit Mandelbrot made the set famous in 1980 with computer plots made "
        "at IBM. It is the set of numbers c for which z^2 + c, repeated starting "
        "from zero, never runs off to infinity. Its boundary is so tangled that "
        "it has the same dimension as a filled-in area."
    ),
    (
        "Seahorse Valley is the narrow gap between the main heart-shaped body and "
        "the round bulb to its left. This view is about 500 times narrower than "
        "the whole set and uses up to 1,500 iterations per pixel. The colors "
        "cycle through a cosine palette as the escape count rises, so detail "
        "close to the set gets as much color as the background."
    ),
]


def render(size, seed=0):
    w, h = size
    center = complex(-0.7453, 0.1127)
    width = 0.0065
    max_iter = 1500

    xs = center.real + np.linspace(-width / 2, width / 2, w)
    ys = center.imag + np.linspace(width / 2, -width / 2, h) * h / w
    c = (xs[None, :] + 1j * ys[:, None]).ravel()

    z = np.zeros_like(c)
    smooth = np.full(c.shape, -1.0)
    idx = np.arange(c.size)
    for i in range(max_iter):
        z = z * z + c
        out = np.abs(z) > 16
        if out.any():
            # Fractional escape count, for smooth color instead of bands.
            smooth[idx[out]] = i + 1 - np.log2(np.log(np.abs(z[out])))
            keep = ~out
            z, c, idx = z[keep], c[keep], idx[keep]
        if idx.size == 0:
            break

    # A slow cosine palette cycles through colors as the count climbs, so
    # the fine structure near the set gets as much color as the outside.
    t = np.sqrt(np.maximum(smooth, 0)) * 0.9
    rgb = np.stack([
        0.5 + 0.5 * np.cos(t + 3.6),
        0.5 + 0.5 * np.cos(t + 4.1),
        0.5 + 0.5 * np.cos(t + 4.9),
    ], axis=-1) * 255
    rgb[smooth < 0] = (8, 6, 14)
    return Image.fromarray(rgb.reshape(h, w, 3).astype(np.uint8))

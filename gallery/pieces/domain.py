import numpy as np
from PIL import Image

TITLE = "Domain Coloring"
FORMULA = [
    "f(z) = (z^2 - 1)(z - 2 - i)^2 / (z^2 + 2 + 2i)",
    "hue = arg f(z),  brightness bands = log |f(z)|",
]
PARAMS = "-3 to 3 on both axes"
CAPTION = (
    "A way to draw a complex function, which takes a 2D input to a 2D "
    "output and can't be graphed the usual way. Color shows the direction "
    "of f(z) and the shaded rings show its size. Zeros are where all the "
    "colors meet; the double zero at 2 + i spins through the rainbow twice. "
    "Poles look the same with the colors running backwards."
)
KIND = "Complex function"
ABOUT = [
    (
        "A complex function takes a point in the plane and returns another point "
        "in the plane, so an ordinary graph would need four dimensions. Domain "
        "coloring, a name coined by Frank Farris, paints the output onto the "
        "input instead: the hue shows which direction the output points and the "
        "brightness shows how big it is."
    ),
    (
        "This function has simple zeros at 1 and -1, a double zero at 2 + i, and "
        "two poles where z^2 = -2 - 2i. Around each zero the colors circle once "
        "for each order of the zero; around the poles they run backwards. The "
        "rings step every time the size of f(z) doubles, and faint spokes mark "
        "every 30 degrees of phase."
    ),
]


def hsv_to_rgb(h, s, v):
    i = np.floor(h * 6).astype(int) % 6
    f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - f * s), v * (1 - (1 - f) * s)
    choices = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]
    rgb = np.zeros(h.shape + (3,))
    for k, (r, g, b) in enumerate(choices):
        m = i == k
        rgb[m] = np.stack([r[m], g[m], b[m]], axis=-1)
    return rgb


def render(size, seed=0):
    w, h = size
    x = np.linspace(-3, 3, w)[None, :]
    y = np.linspace(3, -3, h)[:, None] * h / w
    z = x + 1j * y

    with np.errstate(divide="ignore", invalid="ignore"):
        f = (z ** 2 - 1) * (z - 2 - 1j) ** 2 / (z ** 2 + 2 + 2j)
        hue = (np.angle(f) / (2 * np.pi)) % 1
        mag = np.log2(np.abs(f))
    mag = np.nan_to_num(mag, nan=0, posinf=40, neginf=-40)

    # Brightness steps every time |f| doubles, giving the ring contours.
    rings = mag - np.floor(mag)
    v = 0.62 + 0.38 * rings ** 0.5
    # Faint lines every 30 degrees of phase.
    phase_lines = np.abs(((np.angle(f) / (np.pi / 6)) % 1) - 0.5)
    v *= 0.8 + 0.2 * np.clip(phase_lines * 8, 0, 1)
    s = np.full(hue.shape, 0.78)

    rgb = hsv_to_rgb(hue, s, v) * 255
    return Image.fromarray(rgb.astype(np.uint8))

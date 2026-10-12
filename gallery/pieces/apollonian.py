import numpy as np
from PIL import Image, ImageDraw

from ..render import hex_rgb

TITLE = "Apollonian Gasket"
FORMULA = [
    "k4 = 2 (k1 + k2 + k3) - k4_old",
    "k4 z4 = 2 (k1 z1 + k2 z2 + k3 z3) - k4_old z4_old",
]
PARAMS = "curvatures from Descartes' circle theorem, circles down to 1 pixel"
CAPTION = (
    "Fill a circle with three touching circles, then fill every curved "
    "triangular gap with the largest circle that fits, forever. Descartes "
    "worked out the size of each new circle in 1643; a later complex-number "
    "version also gives its position. The smaller the circle, the brighter "
    "and warmer its color."
)
KIND = "Circle packing"
ABOUT = [
    (
        "Around 200 BC Apollonius of Perga asked how to draw a circle tangent to "
        "three given circles. Repeating that construction in every gap gives the "
        "gasket. In 1643 Rene Descartes found a simple relation between the "
        "curvatures of four mutually tangent circles, and in 2002 it was extended "
        "to complex numbers so that it gives the centers too."
    ),
    (
        "Starting from three equal circles inside a unit circle, every circle "
        "here comes from applying that relation over and over until the circles "
        "are smaller than a pixel, about 4,500 in all. The dust left between them "
        "is a fractal with a dimension of about 1.31."
    ),
]

COLORS = ["#0d0d14", "#203a5c", "#3f6e9a", "#7fb0c9", "#f2c879", "#fbe6c2"]


def render(size, seed=0):
    w, h = size
    ss = 2
    scale = 0.47 * min(w, h) * ss
    cx, cy = w * ss / 2, h * ss / 2
    min_r = 0.6 / scale * ss  # stop below about half a pixel

    # Each circle is (curvature k, k * center). The outer circle has negative
    # curvature because it touches the others from the outside.
    k_in = 1 + 2 / np.sqrt(3)
    d = 1 - 1 / k_in
    inner = [(k_in, k_in * d * np.exp(1j * (np.pi / 2 + 2 * np.pi * i / 3))) for i in range(3)]
    outer = (-1.0, 0j)

    circles = [outer, *inner]
    # Work queue of (three tangent circles, the circle to reflect away from).
    stack = []
    quad = [outer, *inner]
    for i in range(4):
        rest = [quad[j] for j in range(4) if j != i]
        stack.append((rest, quad[i]))

    while stack:
        (a, b, c), old = stack.pop()
        k = 2 * (a[0] + b[0] + c[0]) - old[0]
        kz = 2 * (a[1] + b[1] + c[1]) - old[1]
        if k <= 0 or 1 / k < min_r:
            continue
        new = (k, kz)
        circles.append(new)
        stack.append(((new, b, c), a))
        stack.append(((a, new, c), b))
        stack.append(((a, b, new), c))

    img = Image.new("RGB", (w * ss, h * ss), "#0d0d14")
    draw = ImageDraw.Draw(img)
    palette = [hex_rgb(c) for c in COLORS]
    gap = 0.9 * ss
    for k, kz in sorted(circles, key=lambda c: c[0]):
        r = abs(1 / k) * scale
        z = kz / k if k > 0 else 0j
        x, y = cx + z.real * scale, cy - z.imag * scale
        if k < 0:
            draw.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(v) for v in palette[0]))
            continue
        t = np.clip(np.log(k) / np.log(300), 0, 1) * (len(palette) - 2) + 1
        j = min(int(t), len(palette) - 2)
        col = palette[j] + (palette[j + 1] - palette[j]) * (t - j)
        rr = max(r - gap, 0.5)
        draw.ellipse((x - rr, y - rr, x + rr, y + rr), fill=tuple(int(v) for v in col))

    return img.resize((w, h), Image.LANCZOS)

import numpy as np
from PIL import Image, ImageDraw

from ..render import hex_rgb

TITLE = "Phyllotaxis"
FORMULA = [
    "theta_k = k * 137.508 degrees",
    "r_k = sqrt(k)",
]
PARAMS = "1,500 seeds, golden angle"
CAPTION = (
    "How a sunflower packs its seeds. Each new seed is placed one golden "
    "angle around from the last. Because the golden ratio is the 'most "
    "irrational' number, the seeds never line up into gaps, and the spiral "
    "families you see come in Fibonacci numbers."
)


def render(size, seed=0):
    w, h = size
    ss = 3  # draw at 3x and shrink for smooth circles
    img = Image.new("RGB", (w * ss, h * ss), "#14110f")
    draw = ImageDraw.Draw(img)

    count = 1500
    radius = 0.44 * min(w, h) * ss
    golden = np.pi * (3 - np.sqrt(5))
    k = np.arange(count)
    r = radius * np.sqrt((k + 0.5) / count)
    theta = k * golden
    cx, cy = w * ss / 2, h * ss / 2

    # With r = sqrt(k) every seed gets the same area, so one dot size fits all.
    dot = radius * np.sqrt(np.pi / count) * 0.42

    stops = [hex_rgb(c) for c in ("#ffe8a3", "#f4a259", "#bc4b51", "#5b2a3a")]
    for i in range(count):
        t = i / count * (len(stops) - 1)
        j = min(int(t), len(stops) - 2)
        col = stops[j] + (stops[j + 1] - stops[j]) * (t - j)
        rad = dot * (0.75 + 0.35 * i / count)
        x = cx + r[i] * np.cos(theta[i])
        y = cy + r[i] * np.sin(theta[i])
        draw.ellipse((x - rad, y - rad, x + rad, y + rad), fill=tuple(int(v) for v in col))

    return img.resize((w, h), Image.LANCZOS)

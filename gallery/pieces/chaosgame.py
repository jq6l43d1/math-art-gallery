import numpy as np
from PIL import Image

from ..render import Canvas, ink

TITLE = "Chaos Game"
FORMULA = [
    "pick a random corner of a pentagon (never the same one twice in a row)",
    "p' = p + (corner - p) / 2",
]
PARAMS = "5 corners, jump ratio 1/2, 10 million points"
CAPTION = (
    "Pick a corner of a pentagon at random and move halfway toward it. "
    "Repeat. With no rules the points fill the shape with mush, but one "
    "small restriction (don't pick the same corner twice in a row) is enough "
    "to carve out this lace. Each point takes the color of its last corner."
)
KIND = "Chaos game"
ABOUT = [
    (
        "Michael Barnsley gave the chaos game its name. With the three corners of "
        "a triangle and no rules at all, the dots form the Sierpinski triangle. "
        "Adding rules about which corners may follow which unlocks a whole family "
        "of other fractals from the same simple game."
    ),
    (
        "A quarter of a million points play at once for 60 rounds, and the first "
        "20 rounds are thrown away while they settle. Each point is colored by "
        "the corner it just jumped toward, and the five colors are multiplied "
        "together like layers of transparent ink."
    ),
]

COLORS = ["#d1495b", "#edae49", "#00798c", "#30638e", "#6a4c93"]


def render(size, seed=0):
    rng = np.random.default_rng(seed)
    k = len(COLORS)
    angle = np.pi / 2 + 2 * np.pi * np.arange(k) / k
    cx, cy = np.cos(angle), np.sin(angle)

    walkers = 250_000
    x = rng.uniform(-0.5, 0.5, walkers)
    y = rng.uniform(-0.5, 0.5, walkers)
    last = rng.integers(0, k, walkers)
    canvases = [Canvas(size, (-1, 1, cy.min(), 1), margin=0.04) for _ in range(k)]

    for step in range(60):
        # Choosing from the other k - 1 corners: shift by 1..k-1.
        last = (last + rng.integers(1, k, walkers)) % k
        x = (x + cx[last]) / 2
        y = (y + cy[last]) / 2
        if step >= 20:
            for i, canvas in enumerate(canvases):
                m = last == i
                canvas.add(x[m], y[m])

    paper = np.full((size[1], size[0], 3), 250.0)
    for canvas, color in zip(canvases, COLORS):
        t = canvas.tone(gamma=0.7)
        layer = np.asarray(ink(t, "#ffffff", color)).astype(float) / 255
        paper *= layer
    return Image.fromarray(paper.astype(np.uint8))

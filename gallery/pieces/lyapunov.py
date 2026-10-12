import numpy as np
from PIL import Image

from ..render import gradient

TITLE = "Lyapunov Fractal"
FORMULA = [
    "x' = r x (1 - x),  r alternates between a and b as 'BBBBBBAAAAAA'",
    "lambda = average of log |r (1 - 2x)|",
]
PARAMS = "a from 2.5 to 3.4 (across), b from 3.4 to 4.0 (up), 600 steps"
CAPTION = (
    "The logistic map is the simplest model of a population that grows "
    "until it runs out of food. Here the growth rate flips between two "
    "values in a fixed rhythm. Gold regions settle down to a steady "
    "pattern; the dark blue regions are chaos. The pattern was named Zircon Zity "
    "by Mario Markus, who first drew these around 1990."
)
KIND = "Stability map"
ABOUT = [
    (
        "A Lyapunov exponent measures whether nearby starting points drift "
        "together or apart. Mario Markus and Benno Hess turned it into pictures "
        "by forcing the logistic map, the textbook model of population growth, to "
        "alternate between two growth rates, a and b, in a fixed pattern."
    ),
    (
        "Each pixel is one pair of rates. The map runs 200 warm-up steps and then "
        "averages the exponent over 400 more. Gold means stable, and the brighter "
        "it is, the more strongly nearby values are pulled together; the glowing "
        "lines are where the system is super-stable. Dark blue means chaos."
    ),
]


def render(size, seed=0):
    w, h = size
    seq = "BBBBBBAAAAAA"
    warmup, steps = 200, 400

    a = np.linspace(2.5, 3.4, w)[None, :] * np.ones((h, 1))
    b = np.linspace(4.0, 3.4, h)[:, None] * np.ones((1, w))

    x = np.full((h, w), 0.5)
    lam = np.zeros((h, w))
    for i in range(warmup + steps):
        r = a if seq[i % len(seq)] == "A" else b
        x = r * x * (1 - x)
        if i >= warmup:
            lam += np.log(np.abs(r * (1 - 2 * x)) + 1e-12)
    lam /= steps

    # Negative lambda (stable) shades from black through gold by how stable;
    # positive lambda (chaotic) gets a dim blue by how chaotic.
    gold = np.asarray(gradient(np.clip(-lam / 1.2, 0, 1) ** 0.6,
                               ["#050505", "#3a2a10", "#a8741a", "#f2c14e", "#fff3c4"]))
    blue = np.asarray(gradient(np.clip(lam / 0.6, 0, 1) ** 0.7, ["#050505", "#0f2240", "#2c5d8f"]))
    return Image.fromarray(np.where((lam > 0)[..., None], blue, gold))

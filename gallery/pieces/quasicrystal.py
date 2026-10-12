import numpy as np

from ..render import gradient

TITLE = "Quasicrystal"
FORMULA = [
    "f(x, y) = sum over k = 0..6 of cos(x cos(k pi/7) + y sin(k pi/7))",
]
PARAMS = "7 plane waves, 7-fold symmetry"
CAPTION = (
    "Seven flat ripples crossing at equal angles. Two, three, four or six "
    "waves would make a repeating tiling, but seven can't: the pattern has "
    "perfect sevenfold symmetry around the center and yet never repeats "
    "anywhere, like the quasicrystals that won the 2011 Nobel Prize in "
    "Chemistry."
)


def render(size, seed=0):
    w, h = size
    span = 70.0
    x = np.linspace(-span, span, w)[None, :]
    y = np.linspace(-span * h / w, span * h / w, h)[:, None]

    k = 7
    total = np.zeros((h, w))
    for i in range(k):
        a = np.pi * i / k
        total += np.cos(x * np.cos(a) + y * np.sin(a))

    # Fold the sum into 0..1 twice per period so bright and dark both make
    # bands, which reads more like a woven pattern than a plain wave sum.
    t = np.abs(np.sin(total * np.pi / 4))
    return gradient(t, ["#1a1033", "#4b2a6b", "#c05c7e", "#f3c98b", "#fff4e0"])

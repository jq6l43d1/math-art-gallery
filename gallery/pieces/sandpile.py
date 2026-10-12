import numpy as np
from PIL import Image

from ..render import hex_rgb

TITLE = "Abelian Sandpile"
FORMULA = [
    "drop N grains on one cell",
    "any cell with 4 or more grains gives 1 to each neighbor",
]
PARAMS = "N = 2^16 grains, colored by 0, 1, 2 or 3 grains left"
CAPTION = (
    "Pour sand onto a single square of a grid. Whenever a square holds four "
    "grains it topples, passing one to each neighbor, which may topple in "
    "turn. When everything finally settles, this fractal of nested triangles "
    "and ovals is what's left."
)
KIND = "Cellular automaton"
ABOUT = [
    (
        "Physicists Per Bak, Chao Tang and Kurt Wiesenfeld introduced the "
        "sandpile in 1987 as a model of self-organized criticality: a system that "
        "drives itself to the edge of an avalanche. Deepak Dhar later proved the "
        "abelian property, that topplings can happen in any order without "
        "changing the outcome."
    ),
    (
        "Here 65,536 grains start on one cell. Each color is the number of grains "
        "left on a cell when everything settles: 0, 1, 2 or 3. For speed, every "
        "unstable cell topples as many times as it can at once, which by the "
        "abelian property gives exactly the same final pile."
    ),
]

# Most cells end with 3 grains, so 3 gets the calmest color.
COLORS = ["#0f1424", "#f2e8cf", "#e0a458", "#2e5c8a"]


def render(size, seed=0):
    grains = 2 ** 16
    n = 2 * int(np.sqrt(grains / 3.0)) + 3
    g = np.zeros((n, n), dtype=np.int64)
    g[n // 2, n // 2] = grains

    # Topple every unstable cell at once, as many times as it can in one go.
    # Much faster than moving one grain at a time, and by the abelian
    # property the final pile is the same.
    while True:
        q = g // 4
        if not q.any():
            break
        g -= 4 * q
        g[1:, :] += q[:-1, :]
        g[:-1, :] += q[1:, :]
        g[:, 1:] += q[:, :-1]
        g[:, :-1] += q[:, 1:]

    # Crop to the pile with a small border.
    rows = np.flatnonzero(g.any(axis=1))
    lo, hi = rows[0] - 4, rows[-1] + 5
    g = g[lo:hi, lo:hi]

    colors = np.array([hex_rgb(c) for c in COLORS])
    img = Image.fromarray(colors[g].astype(np.uint8))
    return img.resize(size, Image.NEAREST)

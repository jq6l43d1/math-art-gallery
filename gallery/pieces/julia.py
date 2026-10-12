import numpy as np

from ..render import gradient

TITLE = "Julia Set"
FORMULA = [
    "z' = z^2 + c",
    "c = -0.8 + 0.156i",
]
PARAMS = "500 iterations, smooth escape-time coloring"
CAPTION = (
    "Every pixel is a starting value of z. Square it, add c, repeat. Points "
    "that stay bounded forever form the set; the color outside shows how "
    "quickly each point escaped. The edge is infinitely detailed."
)


def render(size, seed=0):
    w, h = size
    c = complex(-0.8, 0.156)
    max_iter = 500

    aspect = w / h
    xs = np.linspace(-1.6 * aspect, 1.6 * aspect, w)
    ys = np.linspace(-1.6, 1.6, h)
    z = xs[None, :] + 1j * ys[:, None]

    smooth = np.zeros(z.shape)
    alive = np.ones(z.shape, dtype=bool)
    for i in range(max_iter):
        z[alive] = z[alive] ** 2 + c
        escaped = alive & (np.abs(z) > 4)
        # Fractional iteration count removes the banding between colors.
        smooth[escaped] = i + 1 - np.log2(np.log(np.abs(z[escaped])))
        alive &= ~escaped
        if not alive.any():
            break

    t = np.sqrt(np.clip(smooth / 60, 0, 1))
    t[alive] = 0
    return gradient(t, ["#0b0213", "#3b0a45", "#a4235a", "#f26d3d", "#ffd39a", "#fff8ec"])

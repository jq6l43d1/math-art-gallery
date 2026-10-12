"""Shared rendering helpers.

Most pieces in the gallery work the same way: generate a huge number of
points, count how many land in each pixel, then map those counts to ink on
paper. Doing the counting with numpy (instead of drawing one dot at a time)
is what makes 10+ million points finish in seconds.
"""

import numpy as np
from PIL import Image


def hex_rgb(value):
    value = value.lstrip("#")
    return np.array([int(value[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64)


class Canvas:
    """A 2D histogram that points are splatted into."""

    def __init__(self, size, bounds, margin=0.06):
        self.w, self.h = size
        xmin, xmax, ymin, ymax = bounds

        # Fit the bounds into the canvas without stretching, then pad.
        span = max((xmax - xmin) / self.w, (ymax - ymin) / self.h) * (1 + 2 * margin)
        cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
        self.x0 = cx - span * self.w / 2
        self.y0 = cy - span * self.h / 2
        self.scale = 1 / span
        self.counts = np.zeros(self.w * self.h, dtype=np.float64)

    def add(self, x, y, weight=None):
        px = ((x - self.x0) * self.scale).astype(np.int64)
        # Flip y so that "up" in math space is up in the image.
        py = self.h - 1 - ((y - self.y0) * self.scale).astype(np.int64)
        keep = (px >= 0) & (px < self.w) & (py >= 0) & (py < self.h)
        idx = py[keep] * self.w + px[keep]
        w = None if weight is None else weight[keep]
        self.counts += np.bincount(idx, weights=w, minlength=self.counts.size)

    def tone(self, gamma=1.0, clip=0.999):
        """Log-scale the counts into 0..1 so faint and dense regions both read."""
        c = np.log1p(self.counts.reshape(self.h, self.w))
        top = np.quantile(c[c > 0], clip) if np.any(c > 0) else 1.0
        return np.clip(c / top, 0, 1) ** gamma


def bounds_of(x, y, lo=0.0005, hi=0.9995):
    """Robust bounding box of a point cloud (ignores a few stray outliers)."""
    return (*np.quantile(x, [lo, hi]), *np.quantile(y, [lo, hi]))


def ink(t, paper, ink_color):
    """Blend from paper to ink by t (0..1)."""
    p, k = hex_rgb(paper), hex_rgb(ink_color)
    rgb = p + (k - p) * t[..., None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def gradient(t, stops):
    """Map t (0..1) through a list of hex colors spaced evenly."""
    colors = np.array([hex_rgb(s) for s in stops])
    pos = t * (len(stops) - 1)
    i = np.clip(pos.astype(np.int64), 0, len(stops) - 2)
    f = (pos - i)[..., None]
    rgb = colors[i] * (1 - f) + colors[i + 1] * f
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))

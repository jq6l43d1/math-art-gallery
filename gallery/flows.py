"""Integrate a 3D flow (a system of ODEs) for several particles at once."""

import numpy as np


def trace(f, start, dt, steps, burn=1000, sub=12):
    """Follow every particle in `start` (shape 3 x n) with RK4.

    Returns all positions as one 3 x N array. Fast parts of an orbit move
    several pixels per step, so each step is also split into `sub` linearly
    interpolated points; without that the strokes come out dotted.
    """
    def rk4(p):
        k1 = f(p)
        k2 = f(p + dt / 2 * k1)
        k3 = f(p + dt / 2 * k2)
        k4 = f(p + dt * k3)
        return p + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    p = start
    for _ in range(burn):
        p = rk4(p)

    path = np.empty((steps, *p.shape))
    for i in range(steps):
        p = rk4(p)
        path[i] = p

    t = np.linspace(0, 1, sub, endpoint=False)[:, None, None, None]
    path = path[:-1] + (path[1:] - path[:-1]) * t
    return path.transpose(2, 1, 0, 3).reshape(3, -1)

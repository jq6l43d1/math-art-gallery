import numpy as np
from PIL import Image


TITLE = "Standard Map"
FORMULA = [
    "p' = p + K sin(theta)",
    "theta' = theta + p'      (both mod 2 pi)",
]
PARAMS = "K = 0.97, 700 orbits of 2,500 kicks each, one color per orbit"
CAPTION = (
    "A spinning rotor that gets kicked at regular intervals. Each color is "
    "one starting condition followed for 2,500 kicks. Some orbits stay on "
    "smooth curves or circle inside islands; others scatter across a "
    "chaotic sea, drawn in slate. K is set just below the point where the last smooth "
    "barrier breaks."
)
KIND = "Hamiltonian chaos"
ABOUT = [
    (
        "Boris Chirikov studied this map in 1969 as a model of charged particles "
        "in magnetic fields. It became the standard example of how order breaks "
        "down into chaos in systems that conserve energy, and many physical "
        "problems reduce to it, which is where the name comes from."
    ),
    (
        "As K grows, the smooth curves that stop orbits from wandering break up "
        "one by one. The last one breaks at K of about 0.9716. Each orbit's "
        "Lyapunov exponent is estimated as it is computed, and the chaotic orbits "
        "are drawn in a muted slate so the surviving islands and curves stand "
        "out."
    ),
]


def render(size, seed=0):
    rng = np.random.default_rng(seed)
    w, h = size
    k_param = 0.97
    orbits, steps = 700, 2500
    two_pi = 2 * np.pi

    theta = rng.uniform(0, two_pi, orbits)
    p = rng.uniform(0, two_pi, orbits)
    hue = rng.uniform(0, 1, orbits)
    # Bright, slightly pastel colors spread around the color wheel.
    color = np.stack([
        0.6 + 0.4 * np.cos(two_pi * (hue + 0.0)),
        0.6 + 0.4 * np.cos(two_pi * (hue + 1 / 3)),
        0.6 + 0.4 * np.cos(two_pi * (hue + 2 / 3)),
    ], axis=-1) * 255

    def orbit():
        th, pp = theta.copy(), p.copy()
        for _ in range(steps):
            pp = (pp + k_param * np.sin(th)) % two_pi
            th = (th + pp) % two_pi
            yield th, pp

    # First pass: estimate each orbit's Lyapunov exponent by pushing a small
    # tangent vector through the map's Jacobian. Positive means chaotic.
    dp, dth = np.ones(orbits), np.zeros(orbits)
    growth = np.zeros(orbits)
    th = theta
    for th_next, _ in orbit():
        dp = dp + k_param * np.cos(th) * dth
        dth = dth + dp
        norm = np.hypot(dp, dth)
        growth += np.log(norm)
        dp, dth = dp / norm, dth / norm
        th = th_next
    chaotic = growth / steps > 0.02
    color[chaotic] = (48, 52, 78)

    # Second pass: draw. No blending, each pixel keeps the color of the last
    # orbit to land on it; chaotic orbits go down first so the islands sit
    # on top of the sea.
    img = np.zeros((h, w, 3))
    img[:] = (10, 10, 18)
    for group in (chaotic, ~chaotic):
        for th, pp in orbit():
            px = (th[group] / two_pi * w).astype(int).clip(0, w - 1)
            py = (h - 1 - pp[group] / two_pi * h).astype(int).clip(0, h - 1)
            img[py, px] = color[group]

    return Image.fromarray(img.astype(np.uint8))

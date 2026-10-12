"""Every piece in the gallery, in the order they hang on the wall."""

from . import (
    aizawa, apollonian, buddhabrot, chaosgame, clifford, dejong, domain, dragon, fern,
    grayscott, harmonograph, hilbert, hopalong, ikeda, julia, lorenz, lyapunov, mandelbrot,
    maurer, newton, phyllotaxis, quasicrystal, sandpile, standardmap,
)

PIECES = {
    "clifford": clifford,
    "dejong": dejong,
    "lorenz": lorenz,
    "julia": julia,
    "fern": fern,
    "harmonograph": harmonograph,
    "maurer": maurer,
    "phyllotaxis": phyllotaxis,
    "buddhabrot": buddhabrot,
    "aizawa": aizawa,
    "newton": newton,
    "ikeda": ikeda,
    "grayscott": grayscott,
    "hopalong": hopalong,
    "chaosgame": chaosgame,
    "sandpile": sandpile,
    "mandelbrot": mandelbrot,
    "quasicrystal": quasicrystal,
    "standardmap": standardmap,
    "apollonian": apollonian,
    "lyapunov": lyapunov,
    "dragon": dragon,
    "domain": domain,
    "hilbert": hilbert,
}

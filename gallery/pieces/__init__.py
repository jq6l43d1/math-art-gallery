"""Every piece in the gallery, in the order they hang on the wall."""

from . import clifford, dejong, lorenz, julia, fern, harmonograph, maurer, phyllotaxis

PIECES = {
    "clifford": clifford,
    "dejong": dejong,
    "lorenz": lorenz,
    "julia": julia,
    "fern": fern,
    "harmonograph": harmonograph,
    "maurer": maurer,
    "phyllotaxis": phyllotaxis,
}

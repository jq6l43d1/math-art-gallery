"""Every piece in the gallery, in the order they hang on the wall."""

from . import (
    aizawa, buddhabrot, chaosgame, clifford, dejong, fern, grayscott, harmonograph,
    hopalong, ikeda, julia, lorenz, maurer, newton, phyllotaxis, sandpile,
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
}

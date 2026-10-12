"""Render every piece and build the gallery page.

    python build.py                  # render everything at 1600x1600
    python build.py clifford julia   # render just these
    python build.py --size 4000      # print-quality
    python build.py --page-only      # rebuild index.html from existing images
"""

import argparse
import html
import time
from pathlib import Path

from gallery.pieces import PIECES

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
ART = DOCS / "art"


def render(names, size, seed):
    ART.mkdir(parents=True, exist_ok=True)
    for name in names:
        start = time.perf_counter()
        img = PIECES[name].render((size, size), seed=seed)
        img.save(ART / f"{name}.png", optimize=True)
        thumb = img.resize((800, 800 * img.height // img.width))
        thumb.save(ART / f"{name}.jpg", quality=88)
        print(f"{name:14s} {time.perf_counter() - start:6.1f}s")


def build_page():
    cards = []
    for i, (name, piece) in enumerate(PIECES.items(), 1):
        formula = "\n".join(html.escape(line) for line in piece.FORMULA)
        cards.append(f"""
    <article class="piece" id="{name}">
      <a class="frame" href="art/{name}.png"><img src="art/{name}.jpg" alt="{html.escape(piece.TITLE)}" loading="lazy"></a>
      <div class="plaque">
        <span class="no">No. {i}</span>
        <h2>{html.escape(piece.TITLE)}</h2>
        <pre>{formula}</pre>
        <p class="params">{html.escape(piece.PARAMS)}</p>
        <p>{html.escape(piece.CAPTION)}</p>
        <a class="src" href="https://github.com/jq6l43d1/math-art-gallery/blob/main/gallery/pieces/{name}.py">source</a>
      </div>
    </article>""")

    template = (ROOT / "gallery" / "template.html").read_text()
    (DOCS / "index.html").write_text(template.replace("{{PIECES}}", "".join(cards)))
    print(f"wrote {DOCS / 'index.html'}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", metavar="piece",
                        help=f"pieces to render (default: all). One of: {', '.join(PIECES)}")
    parser.add_argument("--size", type=int, default=1600, help="image width and height in pixels")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--page-only", action="store_true", help="skip rendering")
    args = parser.parse_args()
    unknown = set(args.names) - set(PIECES)
    if unknown:
        parser.error(f"unknown piece: {', '.join(sorted(unknown))}")

    if not args.page_only:
        render(args.names or list(PIECES), args.size, args.seed)
    build_page()


if __name__ == "__main__":
    main()

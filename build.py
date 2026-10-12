"""Render every piece and build the gallery site.

    python build.py                  # render everything at 1600x1600
    python build.py clifford julia   # render just these
    python build.py --size 4000      # print-quality
    python build.py --page-only      # rebuild the HTML from existing images
"""

import argparse
import html
import shutil
import time
from pathlib import Path

from PIL import Image

from gallery.pieces import PIECES

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
ART = DOCS / "art"
SITE = ROOT / "gallery" / "site"


def render(names, size, seed):
    ART.mkdir(parents=True, exist_ok=True)
    for name in names:
        start = time.perf_counter()
        img = PIECES[name].render((size, size), seed=seed)
        img.save(ART / f"{name}.png", optimize=True)
        thumb = img.resize((800, 800 * img.height // img.width), Image.LANCZOS)
        thumb.save(ART / f"{name}.jpg", quality=88)
        print(f"{name:14s} {time.perf_counter() - start:6.1f}s")


def fill(template, **values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", str(value))
    return template


def build_site():
    """Write the entrance hall (index.html) and one room per piece."""
    names = list(PIECES)
    piece_tpl = (SITE / "piece.html").read_text()
    (DOCS / "pieces").mkdir(parents=True, exist_ok=True)
    shutil.copy(SITE / "style.css", DOCS / "style.css")

    exhibits = []
    for i, name in enumerate(names):
        piece = PIECES[name]
        title = html.escape(piece.TITLE)
        kind = html.escape(piece.KIND)
        exhibits.append(f"""
  <a class="exhibit" href="pieces/{name}.html">
    <span class="frame"><img src="art/{name}.jpg" alt="{title}" loading="lazy"></span>
    <div class="label">
      <span class="no">No. {i + 1}</span>
      <h2>{title}</h2>
      <span class="kind">{kind}</span>
    </div>
  </a>""")

        prev_name, next_name = names[i - 1], names[(i + 1) % len(names)]
        with Image.open(ART / f"{name}.png") as img:
            width, height = img.size
        page = fill(
            piece_tpl,
            NAME=name,
            NO=i + 1,
            TOTAL=len(names),
            TITLE=title,
            KIND=kind,
            DESCRIPTION=html.escape(piece.CAPTION, quote=True),
            FORMULA="\n".join(html.escape(line) for line in piece.FORMULA),
            CAPTION=html.escape(piece.CAPTION),
            ABOUT="\n".join(f"    <p>{html.escape(p)}</p>" for p in piece.ABOUT),
            PARAMS=html.escape(piece.PARAMS),
            WIDTH=width,
            HEIGHT=height,
            PREV=prev_name,
            NEXT=next_name,
            PREV_TITLE=html.escape(PIECES[prev_name].TITLE),
            NEXT_TITLE=html.escape(PIECES[next_name].TITLE),
        )
        (DOCS / "pieces" / f"{name}.html").write_text(page)

    index = fill((SITE / "index.html").read_text(), EXHIBITS="".join(exhibits), FIRST=names[0])
    (DOCS / "index.html").write_text(index)
    print(f"wrote {DOCS / 'index.html'} and {len(names)} rooms in {DOCS / 'pieces'}")


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
    build_site()


if __name__ == "__main__":
    main()

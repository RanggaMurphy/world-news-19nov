# SPDX-License-Identifier: MIT
"""Entry program for the news-image-20261119 make.fun competition.

The entry image (entry.png, beside this file) is a one-page editorial
infographic, 'THE DAY IN WORLD NEWS', summing up Thursday
19 November 2026. This program copies it, byte for byte, to the
output location: /output/entry.png in the grader, or the directory
named by MAKEFUN_OUTPUT_DIR when run locally:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Python 3.13 standard library only; no network. Running it twice
writes identical bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_IMAGE = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_IMAGE, out_dir / "entry.png")


if __name__ == "__main__":
    main()

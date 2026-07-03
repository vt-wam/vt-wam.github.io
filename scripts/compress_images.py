"""Compress large PNG assets for the project page."""
from __future__ import annotations

import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(__file__))
IMG_DIR = os.path.join(ROOT, "static", "images")
SRC = os.path.join(IMG_DIR, "VTWAM_fig5_prediction.png")


def main() -> None:
    if not os.path.exists(SRC):
        print("Skip: VTWAM_fig5_prediction.png not found")
        return

    img = Image.open(SRC)
    if img.width > 1600:
        ratio = 1600 / img.width
        img = img.resize((1600, int(img.height * ratio)), Image.Resampling.LANCZOS)

    webp = os.path.join(IMG_DIR, "VTWAM_fig5_prediction.webp")
    jpg = os.path.join(IMG_DIR, "VTWAM_fig5_prediction.jpg")
    img.save(webp, "WEBP", quality=82, method=6)
    img.save(jpg, "JPEG", quality=85, optimize=True)
    print(f"Wrote {webp} ({os.path.getsize(webp) // 1024} KB)")
    print(f"Wrote {jpg} ({os.path.getsize(jpg) // 1024} KB)")


if __name__ == "__main__":
    main()

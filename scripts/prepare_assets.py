"""Convert VT-WAM LaTeX figures for the project page."""
from __future__ import annotations

import glob
import os
import shutil

SRC = r"D:\VT-WAM\VT-WAM-Latex\pics"
DST = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "images")


def main() -> None:
    os.makedirs(DST, exist_ok=True)

    try:
        import fitz  # pymupdf
    except ImportError as exc:
        raise SystemExit(
            "Install pymupdf first: pip install pymupdf"
        ) from exc

    name_map = {
        "VTWAM_fig3_实验场景图": "VTWAM_fig3_setup",
        "VTWAM_fig4_任务进程图": "VTWAM_fig4_tasks",
    }

    for pdf in glob.glob(os.path.join(SRC, "*.pdf")):
        stem = os.path.splitext(os.path.basename(pdf))[0]
        target = name_map.get(stem, stem)
        doc = fitz.open(pdf)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        out = os.path.join(DST, f"{target}.png")
        pix.save(out)
        print(f"Converted {stem}.pdf -> {target}.png ({pix.width}x{pix.height})")
        shutil.copy2(pdf, os.path.join(DST, f"{target}.pdf"))
        print(f"Copied PDF -> {target}.pdf")

    for png in glob.glob(os.path.join(SRC, "*.png")):
        base = os.path.basename(png).lower()
        if "fig5" in base:
            shutil.copy2(png, os.path.join(DST, "VTWAM_fig5_prediction.png"))
            print("Copied fig5 -> VTWAM_fig5_prediction.png")
        elif "fig6" in base and "0617" in base:
            shutil.copy2(png, os.path.join(DST, "VTWAM_fig6_avtag.png"))
            print("Copied fig6 -> VTWAM_fig6_avtag.png")


if __name__ == "__main__":
    main()

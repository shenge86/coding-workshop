"""Read printed text out of an image — what people usually call OCR.

Traditional OCR (Tesseract, ABBYY, etc.) is a dedicated system trained on
piles of text-image pairs and uses character-level segmentation. We do
the same job here by asking a general-purpose vision-language model to
just *read out loud* what it sees.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ai_function import ask

DEFAULT_IMAGE = Path(__file__).resolve().parent.parent / "sample_images" / "text_notice.jpg"


def ai_ocr(image_path: str | Path) -> str:
    return ask(
        "Read all the text visible in this image, exactly as written, preserving "
        "line breaks. Output only the text — no commentary, no quotes, no "
        "summary, no description of the image.",
        image=image_path,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    args = parser.parse_args()

    print(f"Image: {args.image}\n")
    print("--- transcribed text ---")
    print(ai_ocr(args.image))

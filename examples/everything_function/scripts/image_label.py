"""Take a picture, return a short label of what's in it.

Pre-2021, this was an entire subfield: ImageNet classifiers, object
detectors, training pipelines. Here we hand a JPEG to a vision-language
model and ask it the question in plain English.

The default image is `sample_images/animal_dog.jpg`. Pass `--image PATH`
to point at your own picture.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ai_function import ask

DEFAULT_IMAGE = Path(__file__).resolve().parent.parent / "sample_images" / "animal_dog.jpg"


def ai_image_label(image_path: str | Path) -> str:
    return ask(
        "Look at the image and give a short label (one to five words) describing "
        "what is in it. Output only the label, no full sentence and no punctuation.",
        image=image_path,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    args = parser.parse_args()

    print(f"Image: {args.image}")
    print(f"Label: {ai_image_label(args.image)}")

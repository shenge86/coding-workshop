"""Take a picture of food, get a recipe back.

This one is fun because the model has to do two things at once: recognize
what the dish is, then generate plausible instructions for making it.
Neither step is hard-coded anywhere.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ai_function import ask

DEFAULT_IMAGE = Path(__file__).resolve().parent.parent / "sample_images" / "food_pizza.jpg"


def ai_recipe_from_food(image_path: str | Path) -> str:
    return ask(
        "Look at the food in the image. First, on one line, write 'Dish: ' "
        "followed by the dish name. Then write 'Ingredients:' followed by a "
        "bulleted list (one per line, '- ' prefix). Then write 'Steps:' "
        "followed by a numbered list of brief cooking steps. Keep it concise.",
        image=image_path,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    args = parser.parse_args()

    print(f"Image: {args.image}\n")
    print(ai_recipe_from_food(args.image))

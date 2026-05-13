# Sample images

Tiny demo images for the vision scripts. Each was downsized to ~640px on the long side and JPEG-compressed to keep the repo light.

| File | Source | Notes |
|------|--------|-------|
| `food_pizza.jpg` | Wikimedia Commons — `Eq_it-na_pizza-margherita_sep2005_sml.jpg` | Photo of a pizza margherita. Resized from the original. |
| `animal_dog.jpg` | Wikimedia Commons — `Labrador_on_Quantock_(2175262184).jpg` | Photo of a labrador. Resized from the original. |
| `text_notice.jpg` | Generated locally with PIL | Synthetic notice text — used as a controlled OCR target so the script always has predictable content to read. |

If you want to swap any of these out, drop a replacement into this folder and update the corresponding script's `DEFAULT_IMAGE` constant (or just pass `--image YOUR_FILE.jpg`).

Wikimedia source files are typically CC BY-SA / CC BY or public domain — see the file description pages on commons.wikimedia.org for the exact license for each original. The synthetic OCR image is original to this workshop and is covered by the repo's main LICENSE.

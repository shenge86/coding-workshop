"""Summarize a chunk of text down to a target length.

The "function signature" is `summarize(text, max_words)`. Both arguments
get pasted into the prompt. The model handles the rest. There is no
sentence parser, no extractive ranking algorithm, no fine-tuned summarization
head. There is a paragraph of text in, and a paragraph of text out.
"""

from __future__ import annotations

from ai_function import ask


def ai_summarize(text: str, max_words: int = 30) -> str:
    return ask(
        f"Summarize the passage in no more than {max_words} words. "
        "Output only the summary, no preamble.\n"
        "Passage: The Industrial Revolution, which began in Britain in the late "
        "18th century, transformed economies that had been based on agriculture and "
        "handicrafts into ones dominated by industry and machine manufacturing. "
        "It led to mass migration from the countryside to growing cities, dramatic "
        "increases in average income and population, and profound social changes "
        "that reshaped daily life across much of the world.\n"
        "Summary: The Industrial Revolution shifted economies from farming to "
        "factories, drove urban migration, and reshaped daily life.\n"
        f"Passage: {text}\n"
        "Summary: "
    )


def _canned_examples() -> None:
    text = (
        "Photosynthesis is the process by which green plants, algae, and certain "
        "bacteria convert light energy, typically from the sun, into chemical "
        "energy stored in glucose. Inside the chloroplasts of plant cells, "
        "chlorophyll absorbs sunlight and uses it to split water molecules into "
        "oxygen, which is released as a byproduct, and hydrogen, which combines "
        "with carbon dioxide drawn from the air to form sugars. These sugars "
        "fuel the plant's growth and ultimately feed nearly every organism on "
        "Earth, either directly or indirectly. The oxygen released as a byproduct "
        "is also what most life on the planet depends on to breathe."
    )
    print(f"original ({len(text.split())} words):")
    print(text)
    print()
    for limit in (40, 20, 10):
        print(f"--- max {limit} words ---")
        print(ai_summarize(text, max_words=limit))
        print()


def _interactive() -> None:
    print("--- interactive ---")
    print("Paste a passage to summarize, then a max word count. 'q' to quit.\n")
    while True:
        try:
            text = input("passage > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if text.lower() in {"q", "quit", "exit"}:
            return
        if not text:
            continue
        try:
            raw_limit = input("max words [30] > ").strip() or "30"
            limit = int(raw_limit)
        except (EOFError, KeyboardInterrupt):
            print()
            return
        except ValueError:
            print("  not a number, try again")
            continue
        print(f"\noriginal ({len(text.split())} words):")
        print(text)
        print(f"\nsummary (max {limit} words):")
        print(ai_summarize(text, max_words=limit))
        print()


if __name__ == "__main__":
    _canned_examples()
    _interactive()

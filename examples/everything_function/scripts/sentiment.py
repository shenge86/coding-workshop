"""Classify the sentiment of a sentence.

This is the first demo where there isn't a plain-Python alternative to
compare against. Pre-2017, "tell me if this review is positive or negative"
was a research problem — papers, labeled datasets, custom-trained models.
Here it's a few lines of prompt.
"""

from __future__ import annotations

from ai_function import ask


def ai_sentiment(text: str) -> str:
    return ask(
        "Classify the sentiment of the following sentence as exactly one of: "
        "positive, negative, neutral. Output only the single word.\n"
        'Sentence: "I love this product, it changed my life."\n'
        "Sentiment: positive\n"
        'Sentence: "It arrived broken and customer service ignored me."\n'
        "Sentiment: negative\n"
        'Sentence: "The package arrived on Tuesday."\n'
        "Sentiment: neutral\n"
        f'Sentence: "{text}"\n'
        "Sentiment: "
    )


def _canned_examples() -> None:
    samples = [
        "Honestly the best coffee I've had in months.",
        "The hotel was fine, nothing memorable either way.",
        "Worst flight of my life, I'll never fly this airline again.",
        "It works, but the instructions could be a lot clearer.",
    ]
    for s in samples:
        print(f"input:     {s}")
        print(f"sentiment: {ai_sentiment(s)}\n")


def _interactive() -> None:
    print("--- interactive ---")
    print("Type a sentence to classify, or 'q' to quit.\n")
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if text.lower() in {"q", "quit", "exit"}:
            return
        if not text:
            continue
        print(f"sentiment: {ai_sentiment(text)}\n")


if __name__ == "__main__":
    _canned_examples()
    _interactive()

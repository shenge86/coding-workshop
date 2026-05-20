"""Translate arbitrary text into an arbitrary target language.

A few years ago, building this would have meant either licensing Google
Translate, or training your own sequence-to-sequence model per language
pair. Here `target_language` is just a string the model reads.
"""

from __future__ import annotations

from ai_function import ask


def ai_translate(text: str, target_language: str) -> str:
    return ask(
        "Translate the sentence into the target language. Output only the "
        "translation, with no quotes and no explanation.\n"
        "Target language: French\n"
        'Sentence: "Where is the train station?"\n'
        "Translation: Où est la gare ?\n"
        "Target language: Japanese\n"
        'Sentence: "I would like a cup of coffee."\n'
        "Translation: コーヒーを一杯ください。\n"
        f"Target language: {target_language}\n"
        f'Sentence: "{text}"\n'
        "Translation: "
    )


def _canned_examples() -> None:
    sentence = "The library closes at six o'clock on Sundays."
    print(f"original: {sentence}\n")
    for lang in ["Spanish", "German", "Mandarin Chinese", "Brazilian Portuguese"]:
        print(f"{lang:>22}: {ai_translate(sentence, lang)}")


def _interactive() -> None:
    print("\n--- interactive ---")
    print("Translate your own text. 'q' as the text to quit.\n")
    while True:
        try:
            text = input("text > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if text.lower() in {"q", "quit", "exit"}:
            return
        if not text:
            continue
        try:
            lang = input("target language > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not lang:
            print("  no target language, skipping")
            continue
        print(f"original:    {text}")
        print(f"translation: {ai_translate(text, lang)}\n")


if __name__ == "__main__":
    _canned_examples()
    _interactive()

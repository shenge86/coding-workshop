"""Turn a messy stream-of-consciousness description into a clean action list.

This one is closer to how you'll probably actually use AI in your own
projects: glue logic that turns "the way a human thinks about something"
into a structured artifact a program can act on.
"""

from __future__ import annotations

from ai_function import ask


def ai_action_list(description: str) -> str:
    return ask(
        "Read the description and output a clean bulleted list of concrete "
        "actions to take, one per line, each starting with '- '. No preamble, "
        "no closing remarks.\n"
        "Description: ok so I need to like, get groceries — milk, bread, maybe "
        "those frozen dumplings — and then drop off the package at the post "
        "office, oh and call mom back, she texted twice yesterday.\n"
        "Actions:\n"
        "- Buy groceries (milk, bread, frozen dumplings)\n"
        "- Drop off package at the post office\n"
        "- Call mom back\n"
        f"Description: {description}\n"
        "Actions:\n"
        "- "
    )


def _canned_examples() -> None:
    messy = (
        "ugh ok so the dishwasher is making that noise again, I should probably "
        "look at the filter or just call the repair guy, also the lawn is getting "
        "long again it's been like three weeks, and we're almost out of dog food "
        "I keep meaning to grab a bag, oh and Sarah's birthday is on Saturday I "
        "haven't gotten anything yet"
    )
    print("input:")
    print(messy)
    print("\naction list:")
    print("- " + ai_action_list(messy))
    print()


def _interactive() -> None:
    print("--- interactive ---")
    print("Paste a messy description and we'll convert it to an action list. 'q' to quit.\n")
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
        print("\naction list:")
        print("- " + ai_action_list(text))
        print()


if __name__ == "__main__":
    _canned_examples()
    _interactive()

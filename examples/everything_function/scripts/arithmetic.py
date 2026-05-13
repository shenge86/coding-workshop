"""Four "AI functions" that do arithmetic.

The point isn't to replace `+`, `-`, `*`, `/` with a 7-billion-parameter
neural network (please don't). The point is that each of these functions
looks identical in shape to a normal Python function — same `def`, same
arguments, same return value — but the *body* of the function is a prompt
instead of a hand-written rule. The "logic" is whatever the model fills in
next.

Run this script and compare each AI answer to what plain Python computes.
You should see them agree on simple cases. That agreement is doing a lot
of work: it tells you that "predict the next token" is a real and useful
operation, not a parlor trick.
"""

from __future__ import annotations

from ai_function import ask


def ai_add(a: float, b: float) -> str:
    return ask(
        "Output only the answer, no explanation.\n"
        "2 + 3 = 5\n"
        "10 + 7 = 17\n"
        "100 + 25 = 125\n"
        f"{a} + {b} = "
    )


def ai_subtract(a: float, b: float) -> str:
    return ask(
        "Output only the answer, no explanation.\n"
        "9 - 4 = 5\n"
        "20 - 13 = 7\n"
        "100 - 41 = 59\n"
        f"{a} - {b} = "
    )


def ai_multiply(a: float, b: float) -> str:
    return ask(
        "Output only the answer, no explanation.\n"
        "3 * 4 = 12\n"
        "8 * 7 = 56\n"
        "12 * 11 = 132\n"
        f"{a} * {b} = "
    )


def ai_divide(a: float, b: float) -> str:
    return ask(
        "Output only the answer as a decimal rounded to 4 places, no explanation.\n"
        "10 / 4 = 2.5000\n"
        "9 / 3 = 3.0000\n"
        "22 / 7 = 3.1429\n"
        f"{a} / {b} = "
    )


OPS: dict[str, tuple] = {
    "+": (ai_add,      lambda a, b: a + b),
    "-": (ai_subtract, lambda a, b: a - b),
    "*": (ai_multiply, lambda a, b: a * b),
    "/": (ai_divide,   lambda a, b: round(a / b, 4)),
}


def _canned_examples() -> None:
    cases = [
        ("+", 47, 28),
        ("-", 153, 89),
        ("*", 14, 17),
        ("/", 44, 6),
    ]

    print(f"{'op':<4} {'inputs':<14} {'AI':<14} {'python':<14}  match?")
    print("-" * 60)
    for op, a, b in cases:
        ai_fn, py_fn = OPS[op]
        ai_out = ai_fn(a, b).strip().rstrip(".")
        py_out = py_fn(a, b)
        match = "yes" if ai_out == str(py_out) else "no"
        print(f"{op:<4} {f'{a} {op} {b}':<14} {ai_out:<14} {str(py_out):<14}  {match}")


def _interactive() -> None:
    print("\n--- interactive ---")
    print("Type an expression like `47 + 28`, or 'q' to quit. Ops: + - * /\n")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if raw.lower() in {"q", "quit", "exit"}:
            return
        parts = raw.split()
        if len(parts) != 3 or parts[1] not in OPS:
            print("  expected: <number> <op> <number>")
            continue
        try:
            a, b = float(parts[0]), float(parts[2])
        except ValueError:
            print("  those don't look like numbers")
            continue
        op = parts[1]
        ai_fn, py_fn = OPS[op]
        ai_out = ai_fn(a, b).strip().rstrip(".")
        py_out = py_fn(a, b)
        match = "✓" if ai_out == str(py_out) else "✗"
        print(f"  AI:     {ai_out}")
        print(f"  python: {py_out}  {match}\n")


if __name__ == "__main__":
    _canned_examples()
    _interactive()

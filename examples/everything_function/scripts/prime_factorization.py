"""Factor an integer into its prime factors — via AI and via real Python.

Like `arithmetic.py`, the point isn't to suggest that you should replace a
hand-coded factoring routine with a 9-billion-parameter neural network.
It's to point out that the *same kind of prompt that did addition* will
also "do" prime factorization, for small numbers at least. The model
gets it right surprisingly often; it also gets it wrong in interesting
ways once the numbers get big enough to actually require the algorithm.
"""

from __future__ import annotations

from ai_function import ask


def ai_prime_factorize(n: int) -> str:
    return ask(
        "Give the prime factorization of the integer. Output only the answer "
        "in the form 'p1^e1 * p2^e2 * ...', with primes in ascending order and "
        "exponents omitted when they are 1. No explanation.\n"
        "12 = 2^2 * 3\n"
        "60 = 2^2 * 3 * 5\n"
        "1001 = 7 * 11 * 13\n"
        "97 = 97\n"
        f"{n} = "
    )


def py_prime_factorize(n: int) -> str:
    """Return the prime factorization formatted like '2^2 * 3'.

    Trial division. Plenty fast for any number a student will type at a prompt.
    """
    if n < 2:
        return str(n)
    factors: list[tuple[int, int]] = []
    remaining = n
    p = 2
    while p * p <= remaining:
        e = 0
        while remaining % p == 0:
            remaining //= p
            e += 1
        if e:
            factors.append((p, e))
        p += 1
    if remaining > 1:
        factors.append((remaining, 1))

    parts = [f"{p}" if e == 1 else f"{p}^{e}" for p, e in factors]
    return " * ".join(parts)


def _canned_examples() -> None:
    cases = [84, 360, 1024, 2025, 9991]
    print(f"{'n':>8}  {'AI':<24}  {'python':<24}  match?")
    print("-" * 70)
    for n in cases:
        ai_out = ai_prime_factorize(n).strip().rstrip(".")
        py_out = py_prime_factorize(n)
        match = "yes" if ai_out == py_out else "no"
        print(f"{n:>8}  {ai_out:<24}  {py_out:<24}  {match}")


def _interactive() -> None:
    print("\n--- interactive ---")
    print("Type an integer to factor, or 'q' to quit.\n")
    while True:
        try:
            raw = input("n = ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if raw.lower() in {"q", "quit", "exit"}:
            return
        try:
            n = int(raw)
        except ValueError:
            print("  not an integer, try again")
            continue
        ai_out = ai_prime_factorize(n).strip().rstrip(".")
        py_out = py_prime_factorize(n)
        match = "✓" if ai_out == py_out else "✗"
        print(f"  AI:     {ai_out}")
        print(f"  python: {py_out}  {match}\n")


if __name__ == "__main__":
    _canned_examples()
    _interactive()

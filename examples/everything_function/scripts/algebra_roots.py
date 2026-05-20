"""Find the roots of a polynomial by *asking* the model for them.

Compare against numpy's actual numerical root finder. For nice polynomials
with integer roots, the AI often gets there. For uglier ones, it makes
plausible-looking guesses that don't quite check out. Both behaviors are
interesting — and both are what you should expect from a system that
"reasons" by predicting the most likely next characters.
"""

from __future__ import annotations

import numpy as np

from ai_function import ask


def format_polynomial(coeffs: list[float]) -> str:
    """Render coefficients as a readable expression like '2x^3 - 5x + 1'."""
    terms = []
    degree = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        if c == 0:
            continue
        power = degree - i
        # Coefficient formatting: drop trailing zeros, keep sign in front.
        abs_str = f"{abs(c):g}"
        sign = "+" if c > 0 else "-"
        if power == 0:
            body = abs_str
        else:
            coef = "" if abs_str == "1" else abs_str
            var = "x" if power == 1 else f"x^{power}"
            body = f"{coef}{var}"
        terms.append(f"{sign} {body}")
    if not terms:
        return "0"
    expr = " ".join(terms)
    # Drop the leading "+ " if positive.
    if expr.startswith("+ "):
        expr = expr[2:]
    elif expr.startswith("- "):
        expr = "-" + expr[2:]
    return expr


def ai_polynomial_roots(coeffs: list[float]) -> str:
    """Same shape as numpy.roots: pass coefficients high-degree to low-degree."""
    polynomial = format_polynomial(coeffs)
    return ask(
        "Find the real roots of the polynomial. Output only a Python list of "
        "numbers rounded to 3 decimal places, like [1.0, -2.0]. No explanation.\n"
        "Polynomial: x^2 - 5x + 6\n"
        "Roots: [2.0, 3.0]\n"
        "Polynomial: x^2 - 4\n"
        "Roots: [-2.0, 2.0]\n"
        "Polynomial: x^3 - 6x^2 + 11x - 6\n"
        "Roots: [1.0, 2.0, 3.0]\n"
        f"Polynomial: {polynomial}\n"
        "Roots: "
    )


def py_polynomial_roots(coeffs: list[float]) -> list[float]:
    return sorted(np.roots(coeffs).real.round(3).tolist())


def _run_one(coeffs: list[float]) -> None:
    print(f"  coefficients: {coeffs}")
    print(f"  polynomial:   {format_polynomial(coeffs)}")
    ai_out = ai_polynomial_roots(coeffs)
    py_out = py_polynomial_roots(coeffs)
    print(f"  AI says:      {ai_out}")
    print(f"  numpy says:   {py_out}")
    print()


def _canned_examples() -> None:
    cases = [
        [1, -7, 12],         # roots 3, 4
        [1, 0, -9],          # roots -3, 3
        [1, -6, 11, -6],     # roots 1, 2, 3
        [2, -3, -11, 6],     # roots 3, -2, 0.5
    ]
    for coeffs in cases:
        _run_one(coeffs)


def _interactive() -> None:
    print("--- interactive ---")
    print(
        "Enter polynomial coefficients high-degree to low-degree, separated by "
        "commas or spaces. Example: `1, -7, 12` is x^2 - 7x + 12. 'q' to quit.\n"
    )
    while True:
        try:
            raw = input("coefficients > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if raw.lower() in {"q", "quit", "exit"}:
            return
        try:
            coeffs = [float(p) for p in raw.replace(",", " ").split() if p]
        except ValueError:
            print("  could not parse those as numbers, try again")
            continue
        if len(coeffs) < 2:
            print("  need at least 2 coefficients (a linear polynomial)")
            continue
        _run_one(coeffs)


if __name__ == "__main__":
    _canned_examples()
    _interactive()

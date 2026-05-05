# Lesson 09: Error Handling
#
# Errors (called exceptions) happen at runtime — bad input, missing files,
# dividing by zero, etc. Instead of crashing, you can catch and handle them
# gracefully using try/except blocks.
#
# To run this file:
#   python 09_error_handling.py

# ============================================================
# WHY PROGRAMS CRASH
# ============================================================
# Uncomment any line below to see the error it produces, then re-comment it.

# print(10 / 0)            # ZeroDivisionError
# print(int("hello"))      # ValueError
# print([][5])             # IndexError
# print({"a": 1}["z"])    # KeyError
# print(open("nope.txt"))  # FileNotFoundError

# ============================================================
# BASIC TRY / EXCEPT
# ============================================================
# Code inside 'try' runs normally.
# If an error occurs, Python jumps to the matching 'except' block
# instead of crashing.

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# The program continues running after the except block.
print("Program is still running.")

# ============================================================
# CATCHING MULTIPLE EXCEPTION TYPES
# ============================================================

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: division by zero.")
        return None
    except TypeError:
        print("Error: both arguments must be numbers.")
        return None

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # Error message, then None
print(safe_divide(10, "x"))  # Error message, then None

# ============================================================
# THE else AND finally CLAUSES
# ============================================================
# else runs only if NO exception occurred.
# finally always runs, whether or not an exception occurred.
# Use finally for cleanup (closing files, database connections, etc.).

def parse_number(text):
    try:
        number = int(text)
    except ValueError:
        print(f"  '{text}' is not a valid integer.")
    else:
        print(f"  Parsed successfully: {number}")
    finally:
        print("  (parse attempt complete)")   # always runs

print("\nParsing '42':")
parse_number("42")

print("\nParsing 'abc':")
parse_number("abc")

# ============================================================
# GETTING THE ERROR MESSAGE
# ============================================================
# Use 'as e' to capture the exception object and read its message.

try:
    value = int("not a number")
except ValueError as e:
    print(f"\nCaught a ValueError: {e}")

# ============================================================
# RAISING EXCEPTIONS
# ============================================================
# You can deliberately raise an exception to signal that something
# went wrong in your own code.

def set_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer.")
    if age < 0 or age > 150:
        raise ValueError(f"Age {age} is out of realistic range.")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(f"\nInvalid age: {e}")

try:
    set_age("thirty")
except TypeError as e:
    print(f"Type error: {e}")

# ============================================================
# PRACTICAL EXAMPLE: ROBUST USER INPUT
# ============================================================
# In a real program you'd use input() here. For the demo we
# simulate the user typing a value.

def get_positive_number(value_str):
    try:
        number = float(value_str)
        if number <= 0:
            raise ValueError("Number must be positive.")
        return number
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None

test_inputs = ["42", "-3", "0", "abc", "7.5"]
for val in test_inputs:
    result = get_positive_number(val)
    if result is not None:
        print(f"  Accepted: {result}")

# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================
# You can create your own exception classes by inheriting from Exception.
# This is useful when you want callers to catch a specific, named error.

class InsufficientFundsError(Exception):
    pass

class Wallet:
    def __init__(self, balance):
        self.balance = balance

    def spend(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Tried to spend ${amount:.2f} but only have ${self.balance:.2f}."
            )
        self.balance -= amount
        print(f"Spent ${amount:.2f}. Remaining: ${self.balance:.2f}")

wallet = Wallet(50)
try:
    wallet.spend(30)
    wallet.spend(30)   # this will fail
except InsufficientFundsError as e:
    print(f"\nPayment failed: {e}")

# --- Try it yourself ---
# Write a function 'safe_index(lst, i)' that:
#   - Returns lst[i] if i is a valid index
#   - Catches IndexError and prints a friendly message instead of crashing
#   - Returns None when the index is out of range

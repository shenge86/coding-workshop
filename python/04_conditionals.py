# Lesson 04: Conditionals
#
# Conditionals let your program make decisions: "if this is true, do that;
# otherwise, do something else." The keywords are: if, elif, else.
#
# Indentation matters in Python! Everything inside an if block must be
# indented by the same amount (typically 4 spaces).
#
# To run this file:
#   python 04_conditionals.py

# --- Basic if statement ---
temperature = 35

if temperature > 30:
    print("It's hot outside!")

# --- if / else ---
# The else block runs when the if condition is False.
is_raining = False

if is_raining:
    print("Bring an umbrella.")
else:
    print("No umbrella needed.")

# --- if / elif / else ---
# Use elif (short for "else if") to check multiple conditions in sequence.
# Python checks each condition top to bottom and stops at the first True one.
score = 78

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")
else:
    print("Grade: F")

# --- Comparison operators ---
# These return True or False and are used inside conditions.
#
#   ==   equal to
#   !=   not equal to
#   >    greater than
#   <    less than
#   >=   greater than or equal to
#   <=   less than or equal to

x = 10
print(x == 10)   # True
print(x != 5)    # True
print(x > 20)    # False
print(x <= 10)   # True

# --- Logical operators: and, or, not ---
# Combine multiple conditions together.

age = 25
has_id = True

# 'and' requires BOTH sides to be True
if age >= 18 and has_id:
    print("Entry allowed.")

# 'or' requires AT LEAST ONE side to be True
is_weekend = False
is_holiday = True

if is_weekend or is_holiday:
    print("No work today!")

# 'not' flips True to False and False to True
is_logged_in = False

if not is_logged_in:
    print("Please log in.")

# --- Nested conditionals ---
# You can place an if inside another if. Keep nesting shallow when possible.
user_role = "admin"
is_active = True

if is_active:
    if user_role == "admin":
        print("Welcome, administrator.")
    else:
        print("Welcome, user.")
else:
    print("Account is inactive.")

# --- Checking membership with 'in' ---
# 'in' tests whether a value exists inside a collection (like a list or string).
allowed_colors = ["red", "green", "blue"]
chosen_color = "green"

if chosen_color in allowed_colors:
    print(f"{chosen_color} is a valid choice.")
else:
    print(f"{chosen_color} is not allowed.")

# --- Try it yourself ---
# Write an if/elif/else block that:
#   - Takes a variable called 'hour' (an integer 0–23 representing the time of day)
#   - Prints "Good morning" if hour < 12
#   - Prints "Good afternoon" if 12 <= hour < 18
#   - Prints "Good evening" otherwise

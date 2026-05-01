# Lesson 02: Variables
#
# A variable is a named container that holds a value. Think of it like a
# labeled box: you put something inside and can retrieve it later by name.
#
# To run this file:
#   python 02_variables.py

# --- Creating variables ---
# Use the '=' sign to assign a value to a variable name.
name = "Alice"
age = 30
height = 5.6
is_student = True

print(name)
print(age)
print(height)
print(is_student)

# --- Using variables in print ---
print("Name:", name)
print("Age:", age)

# --- Updating variables ---
# You can change the value stored in a variable at any time.
age = 31
print("Next year, age:", age)

# --- Variable naming rules ---
# Good names: descriptive, lowercase, underscores between words
first_name = "Bob"
last_name = "Smith"
total_score = 100

# Bad (but technically valid) names — avoid these:
# x = "Bob"          too vague
# FirstName = "Bob"  use lowercase_underscore style for variables

# --- Combining variables (string formatting) ---
# f-strings let you embed variables directly inside a string.
# Put an 'f' before the opening quote, then use {variable_name} inside.
greeting = f"Hello, my name is {first_name} {last_name}."
print(greeting)

score_message = f"Total score: {total_score}"
print(score_message)

# --- Multiple assignment ---
# You can assign the same value to several variables at once.
x = y = z = 0
print(x, y, z)

# Or assign different values on one line.
a, b, c = 1, 2, 3
print(a, b, c)

# --- Try it yourself ---
# Create variables for your own name, age, and favorite number.
# Print a sentence that uses all three.

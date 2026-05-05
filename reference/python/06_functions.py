# Lesson 06: Functions
#
# A function is a reusable block of code that you define once and can call
# as many times as you need. Functions help you avoid repeating yourself and
# make your code easier to read and test.
#
# Anatomy:
#   def function_name(parameters):
#       # body — indented
#       return value      # optional
#
# To run this file:
#   python 06_functions.py

# ============================================================
# DEFINING AND CALLING A FUNCTION
# ============================================================

def greet():
    print("Hello, World!")

greet()   # call the function
greet()   # call it again — the code runs twice without copy-pasting

# ============================================================
# PARAMETERS AND ARGUMENTS
# ============================================================
# Parameters are the variable names listed in the definition.
# Arguments are the actual values you pass when calling the function.

def greet_person(name):           # 'name' is the parameter
    print(f"Hello, {name}!")

greet_person("Alice")             # "Alice" is the argument
greet_person("Bob")

# Multiple parameters:
def add(a, b):
    result = a + b
    print(f"{a} + {b} = {result}")

add(3, 4)
add(10, 25)

# ============================================================
# RETURN VALUES
# ============================================================
# Use 'return' to send a result back to wherever the function was called.

def multiply(a, b):
    return a * b

product = multiply(6, 7)
print(f"6 x 7 = {product}")

# You can use the return value directly in an expression.
print(multiply(3, 3) + multiply(2, 5))   # 9 + 10 = 19

# A function returns None by default if there is no return statement.

# ============================================================
# DEFAULT PARAMETER VALUES
# ============================================================
# You can give parameters a default value. If the caller omits that
# argument, the default is used instead.

def greet_with_title(name, title="Friend"):
    print(f"Hello, {title} {name}!")

greet_with_title("Alice", "Dr.")   # Hello, Dr. Alice!
greet_with_title("Bob")            # Hello, Friend Bob!

# ============================================================
# KEYWORD ARGUMENTS
# ============================================================
# You can pass arguments by name (in any order) to make calls clearer.

def describe_pet(animal, name, age):
    print(f"{name} is a {age}-year-old {animal}.")

describe_pet(name="Rex", age=3, animal="dog")

# ============================================================
# VARIABLE SCOPE
# ============================================================
# Variables created inside a function only exist inside that function.
# This is called "local scope."

def calculate_area(width, height):
    area = width * height    # 'area' is local — only visible inside here
    return area

print(calculate_area(5, 4))
# print(area)   # ← this would raise a NameError — 'area' doesn't exist out here

# Variables defined outside functions are "global" and readable everywhere,
# but modifying them inside a function requires the 'global' keyword (usually
# best to avoid — prefer passing values as arguments and returning results).

# ============================================================
# FUNCTIONS CALLING OTHER FUNCTIONS
# ============================================================

def square(n):
    return n * n

def sum_of_squares(a, b):
    return square(a) + square(b)

print(sum_of_squares(3, 4))   # 9 + 16 = 25

# ============================================================
# A PRACTICAL EXAMPLE: TEMPERATURE CONVERTER
# ============================================================

def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

temps_c = [0, 20, 37, 100]
for c in temps_c:
    f = celsius_to_fahrenheit(c)
    print(f"{c}°C = {f:.1f}°F")

# ============================================================
# RETURNING MULTIPLE VALUES
# ============================================================
# Python lets a function return several values as a tuple.

def min_max(numbers):
    return min(numbers), max(numbers)

data = [5, 2, 9, 1, 7, 3]
lowest, highest = min_max(data)
print(f"Min: {lowest}, Max: {highest}")

# --- Try it yourself ---
# Write a function called 'is_even' that takes a number and returns
# True if it's even, False if it's odd.
# Then use it in a loop to print only the even numbers from 1 to 20.

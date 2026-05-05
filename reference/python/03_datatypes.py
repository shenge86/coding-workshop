# Lesson 03: Data Types
#
# Every value in Python has a type. The type determines what you can do with
# that value (e.g., you can add numbers but not multiply a word by a word).
#
# The built-in function type() tells you what type a value is.
#
# To run this file:
#   python 03_datatypes.py

# --- Integer (int) ---
# Whole numbers, positive or negative, with no decimal point.
apples = 5
temperature = -10
print(type(apples))        # <class 'int'>

# --- Float ---
# Numbers with a decimal point.
price = 19.99
pi = 3.14159
print(type(price))         # <class 'float'>

# --- String (str) ---
# Text — any sequence of characters wrapped in quotes (single or double).
first_name = "Alice"
last_name = 'Smith'
sentence = "She said, 'hello!'"
print(type(first_name))    # <class 'str'>

# Common string operations:
print(len(first_name))               # number of characters: 5
print(first_name.upper())            # ALICE
print(first_name.lower())            # alice
print(first_name + " " + last_name) # concatenation: Alice Smith
print(first_name * 3)               # repetition: AliceAliceAlice

# --- Boolean (bool) ---
# Only two possible values: True or False.
is_raining = False
is_sunny = True
print(type(is_raining))    # <class 'bool'>

# --- None ---
# Represents the absence of a value — like "nothing" or "not set yet".
result = None
print(type(result))        # <class 'NoneType'>
print(result)              # None

# --- Type conversion ---
# You can convert between types using int(), float(), str(), bool().
number_as_string = "42"
actual_number = int(number_as_string)      # "42" → 42
print(actual_number + 8)                   # 50

float_number = float("3.14")              # "3.14" → 3.14
print(float_number)

number_to_string = str(100)               # 100 → "100"
print("Score: " + number_to_string)

# Booleans from other types:
# 0, empty string "", None, and empty containers are False. Everything else is True.
print(bool(0))     # False
print(bool(1))     # True
print(bool(""))    # False
print(bool("hi"))  # True

# --- Arithmetic with types ---
print(10 + 3)      # addition:       13
print(10 - 3)      # subtraction:    7
print(10 * 3)      # multiplication: 30
print(10 / 3)      # division:       3.3333... (always a float)
print(10 // 3)     # floor division: 3 (integer, rounds down)
print(10 % 3)      # modulus:        1 (the remainder)
print(10 ** 3)     # exponent:       1000

# --- Try it yourself ---
# Create one variable of each type above.
# Use type() on each and print the result.

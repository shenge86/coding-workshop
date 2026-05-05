# Lesson 07: Lists and Dictionaries
#
# Lists and dictionaries are the two most important built-in data structures
# in Python. Lists store ordered sequences; dictionaries store key-value pairs.
#
# To run this file:
#   python 07_lists_and_dicts.py

# ============================================================
# LISTS
# ============================================================
# A list is an ordered, changeable collection. Items keep their position
# and you access them by index (starting at 0).

fruits = ["apple", "banana", "cherry", "date"]

# --- Accessing items by index ---
print(fruits[0])    # apple  (first item)
print(fruits[2])    # cherry
print(fruits[-1])   # date   (last item — negative index counts from the end)

# --- Slicing: fruits[start:stop] — stop is NOT included ---
print(fruits[1:3])  # ['banana', 'cherry']
print(fruits[:2])   # ['apple', 'banana']   (start defaults to 0)
print(fruits[2:])   # ['cherry', 'date']    (stop defaults to end)

# --- Modifying lists ---
fruits[1] = "blueberry"         # replace an item
print(fruits)

fruits.append("elderberry")     # add to the end
print(fruits)

fruits.insert(1, "avocado")    # insert at a specific index
print(fruits)

fruits.remove("cherry")         # remove by value (first match)
print(fruits)

popped = fruits.pop()           # remove and return the last item
print(f"Removed: {popped}, List: {fruits}")

popped_at = fruits.pop(0)       # remove and return item at index 0
print(f"Removed: {popped_at}, List: {fruits}")

# --- Useful list operations ---
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

print(len(numbers))             # 8    — number of items
print(min(numbers))             # 1    — smallest value
print(max(numbers))             # 9    — largest value
print(sum(numbers))             # 31   — total
print(numbers.count(1))         # 2    — how many times 1 appears
print(1 in numbers)             # True — membership test

numbers.sort()                  # sort in place (modifies the list)
print(numbers)

numbers.sort(reverse=True)      # sort descending
print(numbers)

# sorted() returns a new sorted list without changing the original
original = [3, 1, 4, 1, 5]
new_sorted = sorted(original)
print(original, "→", new_sorted)

# --- Nested lists (2D) ---
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
print(grid[1][2])   # 6 — row 1, column 2

# --- List comprehension ---
# A concise way to build a new list by transforming or filtering another.
squares = [x ** 2 for x in range(1, 6)]
print(squares)                      # [1, 4, 9, 16, 25]

evens = [x for x in range(20) if x % 2 == 0]
print(evens)                        # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# ============================================================
# DICTIONARIES
# ============================================================
# A dictionary stores data as key-value pairs.
# Keys must be unique and immutable (usually strings or numbers).
# Use the key to look up the value — like a real dictionary.

person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
}

# --- Accessing values ---
print(person["name"])             # Alice
print(person.get("age"))         # 30
print(person.get("email", "N/A"))  # N/A — .get() returns a default if key missing

# --- Adding and updating entries ---
person["email"] = "alice@example.com"   # add a new key
person["age"] = 31                       # update an existing key
print(person)

# --- Removing entries ---
del person["city"]
removed = person.pop("email")            # removes and returns the value
print(f"Removed email: {removed}")
print(person)

# --- Checking for keys ---
print("name" in person)    # True
print("phone" in person)   # False

# --- Iterating ---
scores = {"math": 95, "english": 88, "science": 92}

for subject in scores:                       # iterate over keys
    print(subject)

for subject, score in scores.items():        # iterate over key-value pairs
    print(f"  {subject}: {score}")

for score in scores.values():                # iterate over values only
    print(score)

# --- Useful dictionary methods ---
print(scores.keys())      # dict_keys(['math', 'english', 'science'])
print(scores.values())    # dict_values([95, 88, 92])
print(len(scores))        # 3

# --- Nested dictionary ---
students = {
    "alice": {"grade": "A", "score": 95},
    "bob":   {"grade": "B", "score": 83},
}
print(students["alice"]["score"])   # 95

# --- Dictionary comprehension ---
words = ["apple", "banana", "cherry"]
word_lengths = {word: len(word) for word in words}
print(word_lengths)    # {'apple': 5, 'banana': 6, 'cherry': 6}

# ============================================================
# OTHER COLLECTION TYPES (brief overview)
# ============================================================

# Tuple — like a list but immutable (cannot be changed after creation).
# Good for fixed data like coordinates or RGB colors.
coordinates = (40.7128, -74.0060)
red, green, blue = (255, 0, 0)
print(red, green, blue)

# Set — unordered collection of unique values. Duplicates are ignored.
# Useful for membership tests and removing duplicates.
unique_numbers = {1, 2, 3, 2, 1}
print(unique_numbers)     # {1, 2, 3}

tags = {"python", "beginner", "tutorial"}
tags.add("code")
print("python" in tags)   # True

# --- Try it yourself ---
# 1. Create a list of 5 of your favorite movies.
#    Sort them alphabetically and print each one with its rank (1, 2, 3...).
#
# 2. Create a dictionary representing a simple contact:
#    name, phone, email. Print each field on its own line.

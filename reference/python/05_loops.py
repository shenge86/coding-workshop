# Lesson 05: Loops
#
# Loops let you repeat a block of code many times without copy-pasting it.
# Python has two kinds of loops: for and while.
#
# To run this file:
#   python 05_loops.py

# ============================================================
# FOR LOOPS
# ============================================================
# A for loop iterates over a sequence (list, string, range, etc.)
# and runs the block once for each item.

print("--- for loop over a list ---")
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

# --- range() ---
# range(n) generates numbers from 0 up to (but not including) n.
print("\n--- range(5) ---")
for i in range(5):
    print(i)          # prints 0, 1, 2, 3, 4

# range(start, stop) starts at 'start', stops before 'stop'.
print("\n--- range(2, 7) ---")
for i in range(2, 7):
    print(i)          # prints 2, 3, 4, 5, 6

# range(start, stop, step) jumps by 'step' each time.
print("\n--- range(0, 20, 5) ---")
for i in range(0, 20, 5):
    print(i)          # prints 0, 5, 10, 15

# --- Iterating over a string ---
print("\n--- iterating over a string ---")
for letter in "hello":
    print(letter)

# --- enumerate() ---
# When you need both the index and the value, use enumerate().
print("\n--- enumerate ---")
colors = ["red", "green", "blue"]

for index, color in enumerate(colors):
    print(f"  [{index}] {color}")

# ============================================================
# WHILE LOOPS
# ============================================================
# A while loop keeps running as long as its condition is True.
# You're responsible for changing something so the condition eventually
# becomes False — otherwise the loop runs forever (infinite loop).

print("\n--- while loop ---")
count = 0

while count < 5:
    print(count)
    count += 1          # same as: count = count + 1

# --- Countdown example ---
print("\n--- countdown ---")
n = 5

while n > 0:
    print(n)
    n -= 1
print("Blast off!")

# ============================================================
# LOOP CONTROL: break AND continue
# ============================================================

# break — exit the loop immediately, no matter what.
print("\n--- break ---")
for i in range(10):
    if i == 5:
        break           # stop when we reach 5
    print(i)

# continue — skip the rest of this iteration and go to the next one.
print("\n--- continue (skip evens) ---")
for i in range(10):
    if i % 2 == 0:
        continue        # skip even numbers
    print(i)            # only odd numbers are printed

# ============================================================
# NESTED LOOPS
# ============================================================
# A loop inside a loop. The inner loop runs completely for every
# single iteration of the outer loop.

print("\n--- multiplication table (3x3) ---")
for row in range(1, 4):
    for col in range(1, 4):
        print(f"{row * col:3}", end="")   # end="" keeps output on same line
    print()                               # newline after each row

# ============================================================
# BUILDING RESULTS WITH LOOPS
# ============================================================

# Summing numbers 1 to 100
total = 0
for i in range(1, 101):
    total += i
print(f"\nSum of 1 to 100: {total}")

# Collecting items that pass a filter
numbers = [3, 17, 2, 41, 8, 99, 5]
big_numbers = []

for n in numbers:
    if n > 10:
        big_numbers.append(n)

print(f"Numbers > 10: {big_numbers}")

# --- Try it yourself ---
# Use a for loop and range() to print every multiple of 3 between 1 and 50.
# Use a while loop to keep asking for user input until they type "quit".
#   Hint: user_input = input("Enter something: ")

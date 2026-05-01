# Lesson 10: File Input and Output
#
# Programs often need to read data from files and write results back.
# Python makes this straightforward with the built-in open() function.
#
# File modes:
#   "r"  — read (default). File must exist.
#   "w"  — write. Creates the file; OVERWRITES if it already exists.
#   "a"  — append. Creates the file; adds to the end if it already exists.
#   "r+" — read and write.
#
# Always use the 'with' statement — it closes the file automatically,
# even if an error occurs.
#
# To run this file:
#   python 10_file_io.py

import os

# ============================================================
# WRITING TO A FILE
# ============================================================

output_path = "sample_output.txt"

with open(output_path, "w") as f:
    f.write("Line 1: Hello from Python!\n")
    f.write("Line 2: Writing to files is easy.\n")
    f.write("Line 3: The 'with' block closes the file for us.\n")

print(f"File written: {output_path}")

# ============================================================
# READING AN ENTIRE FILE AT ONCE
# ============================================================

with open(output_path, "r") as f:
    contents = f.read()

print("\n--- Full file contents ---")
print(contents)

# ============================================================
# READING LINE BY LINE
# ============================================================

print("--- Reading line by line ---")
with open(output_path, "r") as f:
    for line in f:
        # line includes the trailing newline character, so strip it
        print(repr(line.strip()))

# --- readlines() returns a list of all lines ---
with open(output_path, "r") as f:
    lines = f.readlines()

print(f"\nNumber of lines: {len(lines)}")
print(f"First line: {lines[0].strip()}")

# ============================================================
# APPENDING TO A FILE
# ============================================================

with open(output_path, "a") as f:
    f.write("Line 4: Appended after the original content.\n")

with open(output_path, "r") as f:
    print("\n--- After appending ---")
    print(f.read())

# ============================================================
# WRITING MULTIPLE LINES WITH writelines()
# ============================================================

shopping_list = ["eggs\n", "milk\n", "bread\n", "butter\n"]

with open("shopping.txt", "w") as f:
    f.writelines(shopping_list)

print("shopping.txt created.")

# ============================================================
# WORKING WITH CSV-STYLE DATA
# ============================================================
# CSV (comma-separated values) is a common plain-text format for tables.
# Python's csv module handles quoting and edge cases automatically.

import csv

students = [
    {"name": "Alice", "grade": "A", "score": 95},
    {"name": "Bob",   "grade": "B", "score": 83},
    {"name": "Carol", "grade": "A", "score": 91},
]

csv_path = "students.csv"

# Write CSV
with open(csv_path, "w", newline="") as f:
    fieldnames = ["name", "grade", "score"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(students)

print(f"\n{csv_path} written.")

# Read CSV
print("\n--- Reading students.csv ---")
with open(csv_path, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']}: {row['grade']} ({row['score']})")

# ============================================================
# CHECKING IF A FILE EXISTS
# ============================================================

print(f"\nDoes '{output_path}' exist? {os.path.exists(output_path)}")
print(f"Does 'missing.txt' exist?  {os.path.exists('missing.txt')}")

# ============================================================
# SAFE READING WITH ERROR HANDLING
# ============================================================

def read_file_safe(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None

content = read_file_safe("missing.txt")
if content is None:
    print("Could not read file — skipping.")

# ============================================================
# CLEANUP: remove the files we created
# ============================================================

for filename in [output_path, "shopping.txt", csv_path]:
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Removed: {filename}")

# --- Try it yourself ---
# 1. Write a program that asks the user to enter their name and favorite color,
#    then saves those to a file called "profile.txt".
# 2. Read the file back and print a greeting using the saved information.

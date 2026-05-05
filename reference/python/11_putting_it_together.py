# Lesson 11: Putting It All Together
#
# This final lesson builds a small, complete command-line program that
# uses everything from the previous lessons:
#   - variables and data types
#   - conditionals and loops
#   - functions
#   - classes
#   - error handling
#   - file I/O
#
# The program is a simple Student Grade Tracker. It lets you:
#   1. Add a student and their score
#   2. View all students and their grades
#   3. Show class statistics
#   4. Save the roster to a file
#   5. Load a previously saved roster
#
# To run this file:
#   python 11_putting_it_together.py

import csv
import os

# ============================================================
# CONSTANTS
# ============================================================
SAVE_FILE = "roster.csv"

# ============================================================
# CLASSES
# ============================================================

class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = float(score)

    @property
    def grade(self):
        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        elif self.score >= 60:
            return "D"
        else:
            return "F"

    def __str__(self):
        return f"{self.name:<20} Score: {self.score:5.1f}  Grade: {self.grade}"


class Roster:
    def __init__(self):
        self.students = []

    def add_student(self, name, score):
        try:
            score = float(score)
        except ValueError:
            print(f"  Error: '{score}' is not a valid score.")
            return
        if score < 0 or score > 100:
            print("  Error: Score must be between 0 and 100.")
            return
        self.students.append(Student(name, score))
        print(f"  Added: {name} (score: {score})")

    def display(self):
        if not self.students:
            print("  No students in roster.")
            return
        print(f"\n  {'Name':<20} {'Score':>7}  {'Grade':>6}")
        print("  " + "-" * 38)
        for student in sorted(self.students, key=lambda s: s.score, reverse=True):
            print(f"  {student}")

    def statistics(self):
        if not self.students:
            print("  No data yet.")
            return
        scores = [s.score for s in self.students]
        print(f"\n  Students : {len(scores)}")
        print(f"  Average  : {sum(scores) / len(scores):.1f}")
        print(f"  Highest  : {max(scores):.1f}")
        print(f"  Lowest   : {min(scores):.1f}")

        grade_counts = {}
        for student in self.students:
            grade_counts[student.grade] = grade_counts.get(student.grade, 0) + 1
        print("  Grades   :", ", ".join(
            f"{g}: {n}" for g, n in sorted(grade_counts.items())
        ))

    def save(self, path):
        try:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "score"])
                for s in self.students:
                    writer.writerow([s.name, s.score])
            print(f"  Saved {len(self.students)} student(s) to {path}")
        except OSError as e:
            print(f"  Save failed: {e}")

    def load(self, path):
        if not os.path.exists(path):
            print(f"  File not found: {path}")
            return
        try:
            with open(path, "r") as f:
                reader = csv.DictReader(f)
                loaded = 0
                for row in reader:
                    self.students.append(Student(row["name"], row["score"]))
                    loaded += 1
            print(f"  Loaded {loaded} student(s) from {path}")
        except (OSError, KeyError, ValueError) as e:
            print(f"  Load failed: {e}")


# ============================================================
# MENU HELPERS
# ============================================================

def print_menu():
    print("\n" + "=" * 40)
    print("  Student Grade Tracker")
    print("=" * 40)
    print("  1. Add a student")
    print("  2. View all students")
    print("  3. Show statistics")
    print("  4. Save roster")
    print("  5. Load roster")
    print("  6. Quit")
    print("=" * 40)


def get_choice():
    while True:
        choice = input("  Enter choice (1-6): ").strip()
        if choice in ("1", "2", "3", "4", "5", "6"):
            return choice
        print("  Please enter a number from 1 to 6.")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    roster = Roster()

    # Pre-populate with some sample data so the demo is interesting
    # even without any user input.
    sample_data = [
        ("Alice", 95),
        ("Bob", 83),
        ("Carol", 76),
        ("David", 61),
        ("Eve", 100),
    ]
    for name, score in sample_data:
        roster.add_student(name, score)

    while True:
        print_menu()
        choice = get_choice()

        if choice == "1":
            name = input("  Student name: ").strip()
            score = input("  Score (0-100): ").strip()
            roster.add_student(name, score)

        elif choice == "2":
            roster.display()

        elif choice == "3":
            roster.statistics()

        elif choice == "4":
            roster.save(SAVE_FILE)

        elif choice == "5":
            roster.load(SAVE_FILE)

        elif choice == "6":
            print("\n  Goodbye!\n")
            break


# This guard ensures main() only runs when you execute this file directly,
# not when it is imported as a module by another script.
if __name__ == "__main__":
    main()

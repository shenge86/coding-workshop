# Coding Workshop — Python for Beginners

Welcome! This workshop takes you from absolute zero to writing real programs in Python. No prior experience needed.

---

## Table of Contents

1. [Setup](#setup)
   - [Windows](#windows)
   - [Mac](#mac)
2. [How to Run a Script](#how-to-run-a-script)
3. [Lessons](#lessons)
4. [Tips for Beginners](#tips-for-beginners)

---

## Setup

### Windows

**Step 1 — Install Python**

1. Open your browser and go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click the big yellow **"Download Python 3.x.x"** button.
3. Run the installer. **Important:** On the first screen, check the box that says **"Add Python to PATH"** before clicking Install Now.
4. Click **Install Now** and follow the prompts.

**Step 2 — Verify the installation**

1. Press `Windows + R`, type `cmd`, and press Enter to open the Command Prompt.
2. Type the following and press Enter:
   ```
   python --version
   ```
   You should see something like `Python 3.12.0`. If you see an error, try `python3 --version`.

**Step 3 — Get the workshop files**

If you have Git installed:
```
git clone https://github.com/your-org/coding-workshop.git
cd coding-workshop
```

Or download the ZIP from the GitHub page (green "Code" button → "Download ZIP"), then unzip it.

---

### Mac

**Step 1 — Install Python**

Mac may already have Python 2 installed, but we need Python 3.

Option A — Download directly:
1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click **"Download Python 3.x.x"** and run the `.pkg` installer.

Option B — Use Homebrew (recommended if you plan to code regularly):
1. Open **Terminal** (press `Cmd + Space`, type "Terminal", press Enter).
2. Install Homebrew by pasting this command:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Then install Python:
   ```
   brew install python
   ```

**Step 2 — Verify the installation**

In Terminal, run:
```
python3 --version
```
You should see `Python 3.x.x`.

**Step 3 — Get the workshop files**

```
git clone https://github.com/your-org/coding-workshop.git
cd coding-workshop
```

Or download and unzip the ZIP file from GitHub.

---

## How to Run a Script

All workshop scripts live in the `python/` folder.

**Windows (Command Prompt):**
```
cd coding-workshop\python
python 01_hello_world.py
```

**Mac / Linux (Terminal):**
```
cd coding-workshop/python
python3 01_hello_world.py
```

> **Tip:** If `python` doesn't work on Mac/Linux, use `python3`. They refer to the same thing on most systems; it's just a naming difference.

---

## Lessons

Work through the files in order. Each one builds on the previous.

| File | Topic | What You'll Learn |
|------|-------|-------------------|
| `01_hello_world.py` | Hello World | Running your first program; the `print()` function |
| `02_variables.py` | Variables | Storing and naming data; f-strings |
| `03_datatypes.py` | Data Types | int, float, str, bool, None; type conversion; arithmetic |
| `04_conditionals.py` | Conditionals | `if`, `elif`, `else`; comparison and logical operators |
| `05_loops.py` | Loops | `for` loops, `while` loops, `break`, `continue`, `range()` |
| `06_functions.py` | Functions | Defining and calling functions; parameters; return values |
| `07_lists_and_dicts.py` | Lists & Dicts | Python's core data structures; list comprehensions |
| `08_classes.py` | Classes & OOP | Objects, attributes, methods, inheritance |
| `09_error_handling.py` | Error Handling | `try`/`except`; raising exceptions; writing robust code |
| `10_file_io.py` | File I/O | Reading and writing text files and CSV files |
| `11_putting_it_together.py` | Capstone | A complete interactive program combining all concepts |

### How each lesson is structured

Every file follows the same pattern:

1. **Comment header** — explains the topic and how to run the file.
2. **Concept sections** — each major idea is demonstrated with working code and inline comments.
3. **Try it yourself** — a challenge at the bottom for you to attempt on your own.

---

## Tips for Beginners

- **Read the comments.** Lines starting with `#` explain what the code does and why. Don't skip them.
- **Run the code first, then read it.** Seeing the output makes the code much easier to understand.
- **Change things and see what happens.** Break the code on purpose — that's how you learn.
- **Indentation matters in Python.** Each level of indentation is 4 spaces (or one Tab key press). Misaligned code will produce an `IndentationError`.
- **Error messages are your friends.** Python's errors tell you exactly which line failed and why. Read them carefully before asking for help.
- **Look things up.** Even experienced programmers search the web constantly. [docs.python.org](https://docs.python.org/3/) is the official reference.

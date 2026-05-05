# Installing Python

You only need this if your project leads you into Python. Skip it otherwise.

## Windows

1. Open your browser and go to https://www.python.org/downloads/
2. Click the big yellow **"Download Python 3.x.x"** button.
3. Run the installer. **Important:** on the first screen, check the box that says **"Add Python to PATH"** before clicking Install Now.
4. Click **Install Now** and follow the prompts.

Verify:

1. Press `Windows + R`, type `cmd`, press Enter.
2. Run:
   ```
   python --version
   ```
   You should see something like `Python 3.12.0`. If not, try `python3 --version`.

## Mac

Mac may already have Python 2 installed, but we need Python 3.

**Option A — direct download:**

1. Go to https://www.python.org/downloads/
2. Click **"Download Python 3.x.x"** and run the `.pkg` installer.

**Option B — Homebrew (recommended if you'll code regularly):**

1. Open **Terminal** (`Cmd + Space`, type "Terminal", Enter).
2. Install Homebrew:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```
   brew install python
   ```

Verify in Terminal:
```
python3 --version
```

## Linux

Python 3 is almost certainly already installed. Check:
```
python3 --version
```

If not, install it through your distribution's package manager (`apt`, `dnf`, `pacman`, etc.).

## A note on `python` vs `python3`

On Mac and Linux, `python` may not exist or may point to Python 2. Use `python3` if `python` doesn't work. They refer to the same interpreter on most modern systems — it's just a naming difference.

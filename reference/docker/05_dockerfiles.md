# Lesson 05: Writing a Dockerfile

So far we've used images other people made. Now we'll make our own. The recipe is just a text file called `Dockerfile`.

## The smallest useful Dockerfile

Make a new folder somewhere on your machine. We'll call it `my-first-image/`.

```bash
mkdir my-first-image
cd my-first-image
```

Inside it, create two files.

**`app.py`** — a tiny Python program:

```python
print("Hello from a container I built myself!")
```

**`Dockerfile`** — no file extension, capital D, exactly that name:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

Four lines, four instructions. Reading top to bottom:

- `FROM python:3.12-slim` — start from an existing image. Our image inherits everything from `python:3.12-slim`. We rarely build images from scratch; we almost always start from someone else's base.
- `WORKDIR /app` — set the working directory inside the image to `/app`. Like `cd`-ing into a folder. Creates it if it doesn't exist.
- `COPY app.py .` — copy `app.py` from your folder (the "build context") into the image's `/app/` directory.
- `CMD ["python", "app.py"]` — set the default command. This is what runs when someone does `docker run` without giving their own command.

## Build the image

```bash
docker build -t my-first-image .
```

Breaking that down:

- `docker build` — build an image.
- `-t my-first-image` — tag (name) it `my-first-image`.
- `.` — use the current directory as the build context (this is where Docker looks for the Dockerfile and any files you `COPY`).

You'll see Docker work through the Dockerfile step by step. When it's done:

```bash
docker images
```

You'll find `my-first-image` in the list.

## Run it

```bash
docker run my-first-image
```

Output:

```
Hello from a container I built myself!
```

The container ran your script and exited. The image is yours now — you can hand it to someone else, push it to a registry (lesson 08), or run it on any machine with Docker installed.

## A more realistic Dockerfile

Most projects have dependencies. Let's say `app.py` uses the `requests` library.

**`app.py`**:

```python
import requests
r = requests.get("https://api.github.com")
print("GitHub API status:", r.status_code)
```

**`requirements.txt`**:

```
requests
```

**`Dockerfile`**:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy requirements first and install them.
# This step is cached separately from your source code,
# so changing app.py doesn't reinstall dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the source.
COPY . .

CMD ["python", "app.py"]
```

Two new instructions:

- `RUN <command>` — run a shell command *during the build*. The result becomes part of the image. Use this to install packages, compile code, set up directories.
- The order matters for caching: copying `requirements.txt` and installing it *before* copying the rest of the source means that when you only edit `app.py`, Docker reuses the cached "dependencies installed" layer and just redoes the source copy. This is the single biggest performance trick in Dockerfiles.

Build and run:

```bash
docker build -t my-app .
docker run my-app
```

You should see GitHub's API status code (probably `200`).

## The most common Dockerfile instructions

| Instruction | What it does |
|-------------|--------------|
| `FROM` | Base image to start from. Must be the first instruction. |
| `WORKDIR` | Set the working directory for subsequent steps. |
| `COPY <src> <dest>` | Copy files from build context into the image. |
| `RUN <cmd>` | Run a shell command at build time. Used for installs, etc. |
| `ENV KEY=value` | Set an environment variable inside the image. |
| `EXPOSE 8080` | Document that the container listens on a port. (Doesn't actually open it — that's `-p` at run time.) |
| `CMD ["python", "app.py"]` | Default command when the container starts. |
| `ENTRYPOINT ["…"]` | Like `CMD` but harder to override. Use `CMD` until you need `ENTRYPOINT`. |

## Look at a real Dockerfile

Open [`../../examples/image_meaning_db/backend/Dockerfile`](../../examples/image_meaning_db/backend/Dockerfile). It's not much bigger than what we just wrote. Real-world Dockerfiles are usually under 30 lines.

## Layers (a useful 60-second mental model)

Each instruction in a Dockerfile creates a "layer" — basically a diff on top of the previous one. Layers are cached individually. If you change `app.py` and rebuild, Docker reuses every layer up to the `COPY . .` step, then redoes only that and anything after.

This is why people write Dockerfiles in a specific order: things that change least frequently (base image, system packages) go near the top. Things that change most (your source code) go near the bottom. Get this right and your rebuilds are seconds instead of minutes.

## Try it yourself

1. Write a Dockerfile for a script that uses two libraries (e.g., `requests` and `rich`) and prints something fancy. Build and run.
2. Edit just the script (not `requirements.txt`) and rebuild. Notice that Docker reuses the cached pip-install layer.
3. Now edit `requirements.txt` and rebuild. Notice that step 2 onwards now re-runs.
4. Move on to [`06_volumes_and_persistence.md`](06_volumes_and_persistence.md) — your containers can build files, but they vanish when the container is removed. Time to fix that.

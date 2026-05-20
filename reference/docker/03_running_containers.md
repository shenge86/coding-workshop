# Lesson 03: Running Containers (and Pretending You're on a Different OS)

Now we run something with substance. This lesson is mostly about feeling, in your hands, what container isolation actually means.

## Step into Ubuntu — even if you're on a Mac or Windows

```bash
docker run -it ubuntu bash
```

The new flags:

- `-i` — keep STDIN open so you can type into the container.
- `-t` — allocate a pseudo-TTY so the terminal behaves like a real shell.
- (`-it` is just `-i` and `-t` stuck together — you'll see this everywhere.)

`ubuntu` is the image name. `bash` is the command to run inside, overriding the image's default.

After a brief download, your prompt changes to something like:

```
root@a1b2c3d4e5f6:/#
```

You are now in a shell *inside* an Ubuntu container. Try a few commands:

```bash
cat /etc/os-release       # confirm it really is Ubuntu
ls /                      # the container's root filesystem
whoami                    # root, by default, inside a container
apt-get update            # this Ubuntu's package manager (works even on a Mac)
apt-get install -y cowsay # install something
/usr/games/cowsay "I am running inside Docker"
```

You just installed `cowsay` into an Ubuntu system on your machine without touching your real machine at all. To leave:

```bash
exit
```

You're back on your real machine. None of those packages are installed on your host. The container is still around (stopped, but present) — we'll clean it up in the next lesson.

## Now try Alpine — a totally different distro

```bash
docker run -it alpine sh
```

Alpine is a tiny Linux distro often used for containers (the image is around 5MB). It uses `sh` instead of `bash` and `apk` instead of `apt-get`:

```sh
cat /etc/os-release       # now it's Alpine
apk add --no-cache cowsay
cowsay "Different OS, same laptop"
exit
```

Two completely different Linux distributions, one after the other, on the same physical machine, neither one leaving a trace once it stops.

## Now Python, with no Python installed on your host

```bash
docker run -it python:3.12 python
```

You're dropped into a Python 3.12 REPL — running inside a container that has Python 3.12 installed, even if your real machine has Python 3.10, Python 2, or no Python at all. Type:

```python
import sys
sys.version
exit()
```

You just used Python 3.12 without installing it.

## The `:tag` part

Notice `python:3.12`. The part after the colon is the **tag**, usually a version. If you leave it off (`python`), Docker assumes `:latest` which is whatever the maintainers most recently published. You should usually pin a version explicitly so your work is reproducible.

Some examples of tags you'll see:

- `python:3.12` — Python 3.12 on a default base.
- `python:3.12-slim` — same Python, on a much smaller Debian base. Faster to download, smaller disk footprint.
- `python:3.12-alpine` — same Python, on the tiny Alpine base. Even smaller. Occasionally causes issues with packages that expect a glibc-based system.
- `ubuntu:22.04`, `ubuntu:24.04`, `ubuntu:latest` — Ubuntu by version number.
- `postgres:16`, `redis:7`, `nginx:1.27` — pick the major version you want.

When in doubt, look up the image on Docker Hub (https://hub.docker.com/) and read its tag list.

## Run a container in the background

Some containers (web servers, databases) are meant to keep running. Use `-d` (detached) to start one in the background:

```bash
docker run -d --name webserver nginx
```

`--name webserver` gives the container a memorable name instead of a random one like `peaceful_einstein`. Visit `http://localhost` … wait, you can't yet. We haven't told Docker to expose its port. That's lesson 07. For now, just check it's running:

```bash
docker ps
```

You should see one running container. Stop it:

```bash
docker stop webserver
```

## Try it yourself

1. Run an Ubuntu container and a Debian container side-by-side in two terminal windows. Note that `cat /etc/os-release` shows different distros in each, even though they share your machine.
2. Run `docker run -it python:3.11 python` and then `docker run -it python:3.12 python`. Two different Python versions, on the same laptop, in the same minute, without installing anything.
3. Move on to [`04_images_vs_containers.md`](04_images_vs_containers.md) — by now you've created several containers and you may be wondering where they all went.

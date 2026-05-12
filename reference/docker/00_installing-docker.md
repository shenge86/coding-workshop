# Installing Docker

You only need this if your project leads you into Docker. Skip it otherwise.

There are two flavors of Docker install:

- **Docker Desktop** — a graphical app for Mac and Windows that bundles the Docker engine, a small Linux VM, and a GUI. The easiest path on those platforms.
- **Docker Engine** — the command-line daemon, no GUI. The standard way to install Docker on Linux.

Both run the same `docker` command. Pick whichever fits your OS.

## Windows

1. Go to https://docs.docker.com/desktop/install/windows-install/
2. Download **Docker Desktop for Windows**.
3. Run the installer. Note if they ask for your email, you can just skip that part, it isn't necessary.
4. When asked, leave **"Use WSL 2 instead of Hyper-V"** checked (this is the modern, recommended backend).
5. Restart your machine when prompted.
6. Launch Docker Desktop from the Start menu. The first launch takes a minute as it sets up.

Verify in PowerShell or Command Prompt:

```
docker --version
docker compose version
```

You should see versions printed for both.

> Note: Docker Desktop is free for personal use, students, education, and small businesses. Read the license terms if you'll use it at a larger company — they may require a paid subscription. On Linux you don't need Docker Desktop at all.

## Mac

1. Go to https://docs.docker.com/desktop/install/mac-install/
2. Download the version for your chip — **Apple Silicon** (M1/M2/M3/M4) or **Intel**. If you're not sure: click the Apple menu → About This Mac. If it says "Apple M…" pick Apple Silicon.
3. Open the `.dmg` and drag **Docker** to your Applications folder.
4. Launch Docker from Applications. Grant the permissions it asks for. You'll see a whale icon in your menu bar when it's running.

Verify in Terminal:

```
docker --version
docker compose version
```

## Linux

On Linux you install the engine directly — no Desktop app required.

The cleanest path is the official convenience script, which handles all major distros:

```
curl -fsSL https://get.docker.com | sh
```

Then add your user to the `docker` group so you don't have to `sudo` every command:

```
sudo usermod -aG docker $USER
```

**Log out and log back in** for that group change to take effect.

Verify:

```
docker --version
docker compose version
docker run hello-world
```

If you'd rather use your distribution's package manager directly, the official instructions live at https://docs.docker.com/engine/install/ — pick your distro from the sidebar.

## A note on `docker compose` vs `docker-compose`

- `docker compose` (two words, a space) is the modern V2 plugin. Use this.
- `docker-compose` (one word, a hyphen) is the legacy V1 tool. Older tutorials use it. The commands are nearly identical. If you see `docker-compose up` somewhere, mentally translate it to `docker compose up`.

Modern Docker installs include the V2 plugin out of the box. You should not need to install `docker-compose` separately.

## Did it work?

The classic smoke test. From any terminal:

```
docker run hello-world
```

You should see a friendly message ending with "Hello from Docker!". If you see that, you're done — head back to [`01_what_is_docker.md`](01_what_is_docker.md).

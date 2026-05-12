# Lesson 09: Docker Compose — Putting the Run Command in a File

Recall the last `docker run` from lesson 07:

```bash
docker run -d \
  --name my-backend \
  -p 8080:8080 \
  -e DATABASE_URL=postgres://workshop:secret@db:5432/projects \
  -e LOG_LEVEL=info \
  -v ./uploads:/app/uploads \
  my-backend-image:1.0
```

Imagine typing that — correctly — every time. Imagine a friend trying to run your project and you having to send them the right invocation through chat. Imagine having to spin up a backend *and* a database *and* a cache.

This is the problem `docker compose` solves. You describe what you want in a YAML file. Then you run `docker compose up` and Docker does the rest.

## Your first compose file

Make a folder and put this in it as `docker-compose.yml`:

```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

That's it. Three nested lines describe an entire deployment.

In the same folder:

```bash
docker compose up
```

What happens:

- Compose reads the file.
- It pulls `nginx` if needed.
- It creates a network for this stack.
- It starts a container called `web` with port 80 mapped to host 8080.
- It streams logs to your terminal.

Open http://localhost:8080. There's nginx.

Press `Ctrl+C` to stop and (optionally) clean up with:

```bash
docker compose down
```

The whole stack comes down.

## Run in the background

Add `-d` (detached):

```bash
docker compose up -d
```

The stack starts and returns your terminal immediately. To see logs:

```bash
docker compose logs -f
```

To stop:

```bash
docker compose down
```

## A more realistic single-service file

Translating the long `docker run` from the start of this lesson:

```yaml
services:
  backend:
    image: my-backend-image:1.0
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://workshop:secret@db:5432/projects
      - LOG_LEVEL=info
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
```

Same setup as the long shell command. But:

- It's version-controllable (commit it to git).
- A new person can clone your project and `docker compose up` and have the same thing running.
- `restart: unless-stopped` means "if this container crashes or the machine reboots, bring it back automatically." That's a real production-grade behavior with one line of YAML.

## `image:` vs `build:`

A service can either pull an existing image or build one from a Dockerfile in the same project:

```yaml
services:
  backend:
    build: ./backend     # Look for a Dockerfile in ./backend/ and build it
    ports:
      - "8080:8080"
```

When you `docker compose up`, Compose will build the image as part of starting up. Edit the Dockerfile and run `docker compose up --build` to force a rebuild.

This is how most of the real-world Compose projects you'll see work: their own services use `build:`, and standard things like databases use `image:`.

## The lifecycle commands

| Command | What it does |
|---------|--------------|
| `docker compose up` | Start the stack, attach to logs. |
| `docker compose up -d` | Start the stack in the background. |
| `docker compose up --build` | Rebuild any `build:` services before starting. |
| `docker compose down` | Stop and remove containers and networks. **Keeps volumes.** |
| `docker compose down -v` | Same plus delete the named volumes. **Destroys data — be deliberate.** |
| `docker compose logs -f` | Tail the logs of every service. |
| `docker compose logs -f backend` | Logs of one service only. |
| `docker compose ps` | List the containers in this stack. |
| `docker compose exec backend bash` | Open a shell inside a running service. |
| `docker compose restart backend` | Restart one service. |

You can spend years writing software and use only these commands.

## Where `compose.yml` lives

Compose looks for `docker-compose.yml` (or the newer name `compose.yml` — both work) in the current directory. Each project gets its own folder with its own compose file. Running `docker compose up` in different folders gives you independent stacks.

The two example projects in this repo are both Compose-based:

- [`../../examples/image_meaning_db/docker-compose.yml`](../../examples/image_meaning_db/docker-compose.yml)
- [`../../examples/audio_meaning_db/docker-compose.yml`](../../examples/audio_meaning_db/docker-compose.yml)

Both are small enough to read top-to-bottom in a minute. Cross-reference them with what you've learned so far and most lines should make sense.

## Try it yourself

1. Create a folder, put a `docker-compose.yml` with the simple nginx example in it, and `docker compose up`. Visit it in your browser.
2. Add another service to the same file — say, a second nginx on port 8081:

   ```yaml
   services:
     web1:
       image: nginx
       ports:
         - "8080:80"
     web2:
       image: nginx
       ports:
         - "8081:80"
   ```

   Run `docker compose up`. Both are reachable on their respective ports. `docker compose down` brings them both down at once.

3. Move on to [`10_compose_multi_service.md`](10_compose_multi_service.md) where the services actually talk to each other.

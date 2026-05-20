# Lesson 10: A Multi-Service Stack

This is where Docker stops being "a fancier way to run a single program" and starts being "I can describe a whole system on one laptop." We'll build a tiny web app that talks to a real database. Two containers, one file, one command.

## What we're building

- **`db`** — a Postgres database, using the official image, with persistent storage.
- **`adminer`** — a small web-based UI that connects to the database, so we can poke at it without installing any database tools on the host.

This is a deliberately small example. But the pattern — one or more services, plus a database, plus some glue — covers a huge fraction of what people actually deploy.

## The file

In a fresh folder, create `docker-compose.yml`:

```yaml
services:
  db:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_USER: workshop
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: projects
    volumes:
      - pgdata:/var/lib/postgresql/data

  adminer:
    image: adminer:5
    restart: unless-stopped
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  pgdata:
```

Read it carefully. A few things worth noticing:

- **Two services**, `db` and `adminer`. Compose will start each as a separate container.
- **No `ports:` on `db`.** The database is not exposed to your host. It doesn't need to be — only the other container needs to reach it, and they can reach each other on the internal network.
- **`adminer`'s `ports:`** make its UI available at `http://localhost:8080`.
- **`depends_on: - db`** tells Compose to start `db` before `adminer`. (It doesn't wait for Postgres to be *ready* — just for the container to exist. For real production you'd add a healthcheck. For a workshop, this is fine.)
- **A named volume `pgdata`** persists Postgres's data across `down`/`up` cycles.

## Bring it up

```bash
docker compose up -d
```

Then visit http://localhost:8080. You'll see Adminer's login screen. Fill in:

- **System:** PostgreSQL
- **Server:** `db`     ← this is the key part: services reach each other by service name
- **Username:** `workshop`
- **Password:** `secret`
- **Database:** `projects`

You should land in a (mostly empty) Postgres database. Create a table, insert a row, browse it — whatever you like. You're using a database server you didn't install, through a UI you didn't install, both running on your laptop in containers.

## The thing that's quietly amazing

In the Adminer login, you typed `db` as the server. Not an IP address, not `localhost`, not `127.0.0.1`. **Just the service name.** Compose set up a private network for this stack and made every service reachable by its name.

This is the same mechanism that lets a "backend" container reach a "database" container with a URL like `postgres://user:pass@db:5432/projects`. The hostname is just the service's name in the compose file. Rename the service, the hostname changes with it.

## Persistence in action

Stop the stack:

```bash
docker compose down
```

Both containers are gone. Bring it back up:

```bash
docker compose up -d
```

Log back into Adminer. Your table and row are still there — because the `pgdata` volume survived the `down`.

Now (carefully) try the destructive form:

```bash
docker compose down -v
docker compose up -d
```

Log in again. Empty database. The `-v` flag deleted the named volumes. **This is the one Compose flag to fear** — it's how you nuke your data, and it looks like every other innocent flag.

## A taste of what scales from here

What you just did was a two-container stack. The same compose file format, with the same `services:` / `volumes:` / `depends_on:` / `ports:` structure, can describe ten services. Twenty. A frontend, a backend, a worker queue, a Redis cache, a search index, a model server. All in one file.

Some real-world patterns you'll see in compose files:

- **`build:` for your own services, `image:` for stock components.** Your code is in a Dockerfile; the database and cache come from the registry.
- **Healthchecks** so dependent services wait for upstreams to be ready (not just running).
- **Profiles** so you can opt into extra services (`docker compose --profile gpu up`).
- **`.env` files** that Compose reads automatically — you reference `${POSTGRES_PASSWORD}` in the YAML and it gets substituted from `.env`.

When your project grows past what fits comfortably in Compose — usually because you want to run across multiple machines, or want managed health/restart/scaling — the natural next step is Kubernetes. Critically: the *containers* don't change. The compose file becomes a different deployment file. Your `backend:1.0` image is still your `backend:1.0` image.

## Try it yourself

1. Bring up the stack above, log into Adminer, create a table with two columns, insert a row, log out, `down`, `up`, log back in. Confirm the row survived.
2. Now `down -v`. Bring it back up. Confirm the row is gone. Feel that fear; remember it.
3. Add a third service of your own — say, a `python:3.12` container with `command: ["sleep", "infinity"]` so it just sits there. Run `docker compose exec python_service bash` to drop into it. Note that from inside that container, `ping db` (after `apt-get install -y iputils-ping`) works — the database is reachable by name.
4. Look at [`../../examples/image_meaning_db/docker-compose.yml`](../../examples/image_meaning_db/docker-compose.yml) and read it line by line. Almost every concept is one you've now seen.
5. Move on to [`11_cleanup_and_next_steps.md`](11_cleanup_and_next_steps.md) — disk reclamation, and where to go from here.

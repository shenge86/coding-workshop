# Lesson 07: Ports and Environment Variables

A container by itself is an island. Two things you'll almost always want:

1. To reach a server running *inside* the container from your browser or curl.
2. To pass configuration (API keys, database URLs, settings) *into* the container without baking it into the image.

## Exposing a port: `-p`

Run a web server in a container:

```bash
docker run -d --name web -p 8080:80 nginx
```

The new flag:

- `-p 8080:80` — map host port `8080` to container port `80`. Anyone hitting `http://localhost:8080` on your machine lands on port `80` inside the container.

Open http://localhost:8080 in your browser. You should see the default nginx welcome page. That web server is running inside an isolated container, but you can talk to it over the network like any other local service.

Stop it:

```bash
docker stop web
docker rm web
```

### Port-mapping rules of thumb

- Format: `-p HOST_PORT:CONTAINER_PORT`. The first number is what you'll type in your browser. The second is what the program inside the container listens on.
- If two containers want port 80, you can't map both to host port 80. Use different host ports: `-p 8081:80` and `-p 8082:80`. Inside each container, both still see port 80.
- For local-only access, you can bind to localhost: `-p 127.0.0.1:8080:80`. Now nothing outside your machine can reach it, even if your firewall is open.

## Passing config: `-e`

The flag `-e KEY=value` sets an environment variable inside the container.

```bash
docker run --rm \
  -e GREETING="Hello from the env" \
  ubuntu bash -c 'echo $GREETING'
```

(`--rm` means "delete this container as soon as it exits" — handy for one-shot commands so you don't accumulate junk.)

Real-world example: Postgres expects a password via env var.

```bash
docker run -d \
  --name pg \
  -e POSTGRES_PASSWORD=secret \
  -p 5432:5432 \
  postgres:16
```

Now you have a Postgres server reachable at `localhost:5432`, with no installation footprint on your host.

## Env files: `--env-file`

If you have a lot of variables (or you don't want them in your shell history), put them in a file:

**`.env`**:

```
POSTGRES_USER=workshop
POSTGRES_PASSWORD=secret
POSTGRES_DB=projects
```

Then:

```bash
docker run -d --name pg \
  --env-file .env \
  -p 5432:5432 \
  postgres:16
```

> Don't commit `.env` files containing secrets to git. Add `.env` to your `.gitignore` and (if you want a checked-in example) commit `.env.example` with placeholder values.

## A note on networking between containers

Two containers on the same Docker network can reach each other by name. Docker creates a default network automatically; for multi-container setups you'll usually create your own (or let `docker compose` do it for you, lesson 09).

Quick taste — two containers on a shared network:

```bash
docker network create mynet
docker run -d --network mynet --name api nginx
docker run --rm --network mynet curlimages/curl curl -s api
```

The second container reached the first by the name `api`, no IP address required. Compose makes this automatic for you, which is why we recommend going there next.

Clean up:

```bash
docker stop api && docker rm api
docker network rm mynet
```

## Putting it together

A single command that runs a backend container with everything plugged in:

```bash
docker run -d \
  --name my-backend \
  -p 8080:8080 \
  -e DATABASE_URL=postgres://workshop:secret@db:5432/projects \
  -e LOG_LEVEL=info \
  -v ./uploads:/app/uploads \
  my-backend-image:1.0
```

Read it left to right: in the background, named `my-backend`, port 8080 mapped, two env vars set, a folder mounted, using image `my-backend-image:1.0`.

This is the kind of `docker run` command that, once it grows past about four flags, gets annoying to retype every time. Which is the perfect motivation for `docker compose`, coming in lesson 09.

## Try it yourself

1. Run nginx with `-p 8080:80` and visit it in your browser. Stop it and run it again with `-p 9000:80`. Same image, different host port.
2. Run a Postgres container with `-e POSTGRES_PASSWORD=secret` and connect to it from your host with a database tool (DBeaver, `psql`, or `pgcli`). No Postgres installed on your machine, fully working server.
3. Move on to [`08_registries.md`](08_registries.md) — how images get from one machine to another.

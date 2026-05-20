# Lesson 06: Volumes and Persistence

By default, containers are **ephemeral**. Whatever a container writes to its own filesystem disappears the moment that container is removed. That's a feature, not a bug — it's what keeps containers clean — but it's a surprise the first time you run a database in a container and then `docker rm` it.

## See the problem

```bash
docker run -it --name scratch ubuntu bash
```

Inside:

```bash
echo "important data" > /important.txt
cat /important.txt
exit
```

Now remove the container and try again with a fresh one:

```bash
docker rm scratch
docker run -it --name scratch ubuntu bash
cat /important.txt   # No such file or directory
exit
docker rm scratch
```

The file existed only inside the old container's writable layer. New container, new layer, no file.

## Two ways to persist data

Both are called "mounts" — they connect a path *inside* the container to something that survives the container.

### 1. Bind mounts — connect to a folder on your host

A bind mount maps a folder on your real machine to a folder inside the container. Changes show up on both sides instantly.

```bash
mkdir ~/docker-data
docker run -it --name scratch \
  -v ~/docker-data:/data \
  ubuntu bash
```

The flag `-v <host-path>:<container-path>` is the mount. Inside the container:

```bash
echo "important data" > /data/important.txt
exit
```

Back on your host:

```bash
cat ~/docker-data/important.txt
```

The file is there, on your real machine. Remove and re-create the container — the file is still there because it never lived inside the container in the first place.

Bind mounts are great for:

- **Development** — mount your source code into the container so edits on your laptop are picked up immediately.
- **Configs** — point the container at a config file you maintain on your host.
- **"I need to see the files"** — folders you want to open in your file manager.

> On Windows, host paths look like `C:\Users\you\docker-data` or, in PowerShell, `${PWD}\docker-data`. On Mac/Linux, `~/docker-data` or `$(pwd)/docker-data` works.

### 2. Named volumes — Docker-managed storage

A named volume lives somewhere Docker chooses (you don't need to care where), and you refer to it by name.

```bash
docker volume create mydata
docker run -it --name scratch \
  -v mydata:/data \
  ubuntu bash
```

Inside the container, write to `/data` as before, exit, remove the container, run a fresh one with the same `-v mydata:/data`, and your files are still there.

Named volumes are better than bind mounts when:

- You don't care where on disk the data lives — you just want it to *persist*.
- The data is "the database's data" or "the model's cache" — internal to the app, not something a human is going to open.
- You're running on a server and don't want to commit to specific host paths.

List your volumes:

```bash
docker volume ls
```

Remove a volume (only when you're sure):

```bash
docker volume rm mydata
```

## A realistic example: persisting a database

```bash
docker run -d \
  --name pg \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16
```

Run that, connect, create a database, write some rows, then:

```bash
docker stop pg
docker rm pg
```

Now run it again with the **same** `-v pgdata:/var/lib/postgresql/data`. Your database is still there. The volume outlived the container.

Without that volume, removing the container would have erased everything.

## The danger to know about

When you remove a stopped container with `docker rm`, the volume *survives*. Good.

When you bring down a Compose stack (lesson 09) with `docker compose down`, volumes *survive*. Good.

When you bring it down with `docker compose down -v`, the `-v` is "and also nuke the volumes." That command will silently delete your database data. **`down -v` is destructive. Use it deliberately.**

Likewise:

```bash
docker volume prune
```

Removes any volume that no container is currently using. Convenient for cleanup; catastrophic if your database container happened to be stopped at the time.

## Try it yourself

1. Use a bind mount to share your current directory with a Python container: `docker run -it -v "$(pwd)":/work -w /work python:3.12 bash`. Then `ls /work` inside the container — you should see the same files as on your host.
2. Edit a file on your host (in any editor) while that container is running, then `cat` it from inside the container. The change is instant.
3. Move on to [`07_ports_and_env.md`](07_ports_and_env.md) where we'll let containers talk to the outside world.

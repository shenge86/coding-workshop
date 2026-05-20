# Lesson 04: Images vs. Containers

This is the distinction that separates "I'm fumbling" from "I get it." Internalize this and most of Docker stops feeling magical.

## The recipe vs. the cake

- **Image** — a frozen, read-only snapshot of a filesystem with a default command attached. The "recipe." Doesn't run, doesn't change. Examples: `ubuntu:24.04`, `python:3.12-slim`, `postgres:16`.
- **Container** — a running (or stopped) instance of an image. The "cake." Each container is its own thing, with its own writable layer on top of the image's read-only one.

You can make many containers from one image, the same way you can bake many cakes from one recipe. Each container changes independently. None of them changes the image.

```
   IMAGE: python:3.12          (read-only — like a class)
     │
     ├─ CONTAINER A             (a running instance — like an object)
     ├─ CONTAINER B             (another instance, unaffected by A)
     └─ CONTAINER C
```

If you're a programmer: an image is like a class, a container is like an instance of that class. Multiple instances; each has its own state.

## Inspect what you have

```bash
docker images
```

Lists every image on your machine. Columns: repository name, tag, image ID, age, size.

```bash
docker ps
```

Lists **running** containers only.

```bash
docker ps -a
```

Lists **all** containers — running, stopped, exited, whatever. By now you probably have a pile of stopped containers from the previous lessons.

Each container has a name (random or chosen with `--name`) and an ID (a long hex string). You can refer to a container by either; the first few characters of the ID usually suffice.

## Stop, start, restart

```bash
docker stop <name-or-id>           # send SIGTERM, then SIGKILL after 10s
docker start <name-or-id>          # start a stopped container again
docker restart <name-or-id>        # stop and start
```

A stopped container still exists on disk — its filesystem state is preserved. Starting it again resumes from where it left off (process exits, but the writable layer persists until you remove the container).

## Get rid of containers

```bash
docker rm <name-or-id>             # remove a stopped container
docker rm -f <name-or-id>          # force: stop and remove in one shot
```

To clean up *all* stopped containers at once:

```bash
docker container prune
```

It will ask for confirmation. This frees disk and de-clutters `docker ps -a`. It does not delete images.

## Get rid of images

```bash
docker rmi <name-or-id>            # remove an image
```

You can't remove an image while a container (running or stopped) is using it. Remove the containers first, or use `docker rmi -f` to force.

To clean up all images that aren't used by any container:

```bash
docker image prune -a
```

Again, asks for confirmation. Saves a lot of disk on a machine where you've been experimenting.

## The four-step lifecycle

This is essentially all of Docker's container model:

```
   docker pull            docker run             docker stop          docker rm
   ────────────►          ────────────►          ────────────►        ────────────►
   image cached           container running      container stopped    container gone
   (or built locally)                            (still on disk)
```

`docker run` is actually two steps: create a container, then start it. Most of the time you don't care, but it's why you'll occasionally see `docker create` followed by `docker start` in scripts.

## A few extra moves you'll want

Run a command inside a *running* container (useful for debugging):

```bash
docker exec -it <name-or-id> bash
```

This drops you into a shell inside an already-running container. Different from `docker run`, which starts a *new* container.

Stream the logs of a running container:

```bash
docker logs -f <name-or-id>
```

`-f` means "follow" — like `tail -f`. Press `Ctrl+C` to stop following (the container keeps running).

Inspect details:

```bash
docker inspect <name-or-id>
```

Dumps a giant JSON blob with everything Docker knows about a container or image. Most of the time you don't need it; when you do, it's there.

## Try it yourself

1. Run `docker ps -a` and count how many stopped containers you've accumulated from lessons 02 and 03.
2. Pick one of the stopped Ubuntu containers and run `docker start -ai <name>` to wake it back up and reattach. You'll find yourself back inside that container's filesystem, with whatever changes you made still there.
3. Now run `docker container prune` to clean them all up. (Confirm with `y`.) Then `docker ps -a` should be empty (or nearly so).
4. Run `docker images` to see what's left. Even with no containers, the *images* are still there, ready for the next `docker run`.
5. Move on to [`05_dockerfiles.md`](05_dockerfiles.md) where we'll build our own image instead of using other people's.

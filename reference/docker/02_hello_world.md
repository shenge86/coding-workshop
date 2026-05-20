# Lesson 02: Hello World

Yes — Docker has a `hello-world` image, just like programming languages have a "hello world" program. Running it is the canonical first step.

Open a terminal and run:

```bash
docker run hello-world
```

You should see something like:

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon ran a new container from that image, which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which
    sent it to your terminal.
...
```

## What just happened

`docker run hello-world` is a small command doing a surprising amount of work:

1. You asked Docker for an image named `hello-world`.
2. Docker checked your local image cache. Not there.
3. Docker reached out to **Docker Hub** — a public registry of images — and downloaded it.
4. Docker created a new container from that image and started the program inside.
5. The program printed its message and exited.
6. The container stopped (but still exists; we'll deal with that in lesson 04).

The whole thing took a few seconds and didn't install anything onto your system the way a normal program would. The `hello-world` "program" lives entirely inside the image's filesystem.

## The shape of every `docker run` command

```bash
docker run [options]  IMAGE  [command and arguments]
```

- `IMAGE` is the name of the image to run (`hello-world`, `ubuntu`, `python:3.12`, etc.).
- `[options]` go *before* the image name. (Order matters; this catches everyone at first.)
- `[command and arguments]` go *after* the image, and override the image's default command.

For `hello-world` the image's default command is "print the welcome message and exit", and we didn't override it.

## Run it again

```bash
docker run hello-world
```

This time it skips the download — the image is already in your local cache — and just runs the container. Almost instant.

## A first peek at what's there

Docker stores every image it has downloaded. List them:

```bash
docker images
```

You should see `hello-world` with a size of around 14 kilobytes. That's the entire program plus its filesystem. (For comparison, an installed copy of, say, Python 3 takes hundreds of megabytes.)

You can also list every container that's ever existed, even stopped ones:

```bash
docker ps -a
```

You'll see two entries — one for each time you ran `hello-world`. They both ran for a fraction of a second and then exited. Don't worry about them; lesson 04 covers cleaning up.

## Try it yourself

1. Run `docker run hello-world` a third time. Notice how fast it is now that the image is cached.
2. Run `docker images` and find the row for `hello-world`. The `IMAGE ID` column shows its content hash — that's how Docker uniquely identifies images under the hood.
3. Move on to [`03_running_containers.md`](03_running_containers.md), where we'll run something more interesting than a "hello".

# Lesson 11: Cleanup, Disk, and Where to Go Next

After working through this primer your machine has accumulated images, containers, volumes, and build caches. This lesson is the maintenance you'll do every few weeks. It also points at where to learn more.

## See what Docker is using

```bash
docker system df
```

A high-level summary: how much disk space your images, containers, volumes, and build cache are taking up.

For more detail:

```bash
docker images        # all images
docker ps -a         # all containers (running and stopped)
docker volume ls     # all named volumes
```

## Surgical cleanup

If you know exactly what to remove:

```bash
docker rm <container>             # one container
docker rmi <image>                # one image
docker volume rm <volume>         # one volume
```

A container has to be stopped (or removed with `rm -f`) before its image can be removed.

## Broad cleanup

When you just want disk back:

```bash
docker container prune        # remove all stopped containers
docker image prune            # remove dangling images (no tag, not used)
docker image prune -a         # remove ANY image not used by a container right now
docker volume prune           # remove volumes not used by any container
docker network prune          # remove networks not used
docker builder prune          # remove the build cache
```

Each one asks for confirmation.

The atomic "clean everything not currently in use" command:

```bash
docker system prune -a
```

And the scariest version, which also removes volumes:

```bash
docker system prune -a --volumes
```

Read that twice before running it. It will delete data in any stopped database volume. The convenience of one command is balanced by the cost of using it without thinking.

## Patterns that keep your disk tidy

- Use `--rm` on one-shot containers: `docker run --rm -it ubuntu bash`. The container is deleted as soon as it exits, so nothing piles up.
- Run `docker system df` occasionally. If your build cache is 30 GB, `docker builder prune` is the answer.
- When you `docker compose down` a project you're truly done with, follow up with `docker compose down --rmi all -v` to remove its images and volumes too. (Be sure you're truly done.)

## Where to go next

The four pieces of Docker we *didn't* cover, in rough order of when you'll probably want them:

1. **Healthchecks.** Tell Compose how to know a service is actually ready (not just "the process exists"). Add a `healthcheck:` block to a service in `docker-compose.yml`, and use `depends_on: { db: { condition: service_healthy } }` to wait properly.

2. **Multi-stage builds.** A Dockerfile pattern where you build in one image and copy the artifact into a smaller "final" image. Cuts image size dramatically, especially for compiled languages.

3. **`.dockerignore`.** Like `.gitignore` for Docker builds — exclude files from the build context so they don't bloat your image or invalidate your cache.

4. **Container orchestration (Kubernetes, ECS, Nomad).** The next step up from Compose, for running containers across multiple machines. If you find yourself building production systems for paying customers, you'll meet one of these. If you're not, you almost certainly don't need it.

## Resources we trust

- **Official Docker docs** — https://docs.docker.com/ . The "Get Started" guide is excellent. The reference sections (Dockerfile reference, Compose file reference) are the authoritative source when you're hunting for a specific flag.
- **Play with Docker** — https://labs.play-with-docker.com/ . Free, in-browser Docker environment. Great for experimenting without touching your laptop.
- **Docker Curriculum** — https://docker-curriculum.com/ . A longer community-written tutorial, takes you a step further than this primer (deploys a multi-container app to AWS).
- **The Compose spec** — https://compose-spec.io/ . The Compose file format is now an open spec, not just a Docker product. Useful when you want to know every legal field.
- **Awesome Docker** — https://github.com/veggiemonk/awesome-docker . A curated index of tools, tutorials, and useful images.

## And finally

Docker is one of those tools where a small, well-chosen vocabulary covers ninety percent of the work. You now have it:

- `docker run`, `docker ps`, `docker images`, `docker rm`, `docker rmi`
- `docker build`, `Dockerfile`, `FROM/WORKDIR/COPY/RUN/CMD`
- `docker pull`, `docker push`, `docker tag`
- `docker compose up`, `down`, `logs`, `exec`
- `-p`, `-v`, `-e`, `-d`, `-it`, `--name`, `--rm`
- the words *image*, *container*, *volume*, *registry*, *service*

Everything else is a refinement. When your project needs the refinement, look it up. Until then, you've got the toolbox.

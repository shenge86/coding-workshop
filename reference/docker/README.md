# Docker — reference material

This folder is a self-paced Docker primer. It is **not** the spine of the class — your project is. We've put it here because Docker is one of the most useful tools you can have in your toolbox: it lets you run almost any piece of software cleanly on your machine, share it with others, and deploy it to a server later — using the *same* setup the whole way through.

Docker is **free and open source**. The core engine (`containerd`, `runc`, the Docker daemon) is openly developed and you can run it forever without an account, a subscription, or even an internet connection once an image is pulled. There are paid Docker products too, but they're optional — everything in this primer uses the free pieces.

## When to dip in

- You want to run a piece of software (a database, a model server, someone's GitHub project) without installing a dozen system dependencies.
- Your project is starting to need more than one service (a web app + a database, a frontend + a backend) and you want them to start and stop together.
- You've hit "works on my machine" pain and want a way to make the environment portable.
- You want to deploy your project somewhere later and you'd like the deployment to behave the same as your laptop.
- You're tired of Python virtualenvs, Node version managers, Ruby rbenv, and the rest of the per-language environment menagerie. Docker supersedes all of that with one mental model.

## When *not* to dip in

- Out of a sense of obligation. There's no test.
- Before you have a project that benefits from it. The lessons make far more sense once you've felt the pain Docker is solving.

## How it scales

The same `docker run` you type on your laptop is the same command that runs containers in production at companies serving billions of requests. The same `docker-compose.yml` that brings up your two-service hobby project also describes the building blocks of large cloud deployments (Kubernetes, ECS, Nomad — they all eat the same container images). Starting with Docker means starting at the bottom of a ladder that goes very high. You don't have to climb it. But the rung you're on is the same wood as every rung above.

## Lessons

Work in order if you're starting from zero. Skip around if you already know parts of this.

| File | Topic |
|------|-------|
| `01_what_is_docker.md` | What a container is, why it exists, how it differs from a VM |
| `02_hello_world.md` | Your first container: `docker run hello-world` |
| `03_running_containers.md` | Running Ubuntu, Alpine, and Python — OS abstraction in action |
| `04_images_vs_containers.md` | The crucial distinction. `ps`, `images`, `rm`, `rmi` |
| `05_dockerfiles.md` | Writing a `Dockerfile` and building your own image |
| `06_volumes_and_persistence.md` | Ephemeral by default — how to keep data around |
| `07_ports_and_env.md` | Exposing ports (`-p`), passing config (`-e`) |
| `08_registries.md` | Docker Hub, pulling and pushing images |
| `09_compose_basics.md` | `docker compose` — describing a container in a file |
| `10_compose_multi_service.md` | A two-service stack: web app + database |
| `11_cleanup_and_next_steps.md` | Reclaiming disk space, and where to learn more |

If Docker isn't installed yet, see [`installing-docker.md`](installing-docker.md).

## Better resources we trust

This primer covers the slice of Docker we think is useful for the kinds of projects this workshop tends to produce. It is deliberately small. If you want to go deeper, these are good places:

- **The official docs** — https://docs.docker.com/get-started/ . Genuinely well written.
- **Play with Docker** — https://labs.play-with-docker.com/ . Free in-browser Docker environment if you haven't installed it yet or want to experiment without touching your laptop.
- **Docker Curriculum** — https://docker-curriculum.com/ . A community-written end-to-end tutorial that goes a bit further than this primer.
- **"Docker Deep Dive" by Nigel Poulton** — if you end up needing a book.

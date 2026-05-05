# Docker — reference material

*Placeholder.* This folder will cover Docker: a way to run software in self-contained boxes (containers) so it doesn't get tangled up with the rest of your machine.

Planned topics:

- What a container is, and how it differs from a virtual machine
- The two pieces: an *image* (the recipe) and a *container* (a running instance)
- Running someone else's container: `docker run`
- `docker compose` — describing a small stack of services in one file
- Looking at logs: `docker compose logs -f`
- Volumes: keeping data around when containers stop
- Stopping things cleanly: `down` vs. `down -v` (and why the second one nukes your data)
- Writing a minimal `Dockerfile` for your own project
- Cleaning up disk space when your machine gets full

## When to dip in

When a project (yours or someone else's) ships as a Docker setup, or when you want to try a piece of software without installing five other things first. Both example projects in [`../../examples/`](../../examples/) are Docker-based, so this is a good companion to those.

## Installing

Linux: install Docker Engine + the Compose plugin from docs.docker.com.
Mac/Windows: install Docker Desktop.

Detail will go here.

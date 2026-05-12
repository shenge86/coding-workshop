# Lesson 01: What is Docker?

Before any commands, the mental model. Without it, the commands feel like incantations.

## The problem Docker solves

You want to run a piece of software — somebody else's web app, a database, a model server, a tool from a research paper. Normally, that means:

1. Install the right version of Python (or Node, or Java, or…).
2. Install the right system libraries it depends on. Hope they don't conflict with the ones already on your machine.
3. Set environment variables. Edit a config file. Maybe set up a database the app expects.
4. Pray that the README was up to date.

Multiply that by every project you want to try, and your laptop becomes a tangled mess. Worse, when it finally works on your machine, it'll behave differently on a coworker's machine or on a server because *their* tangle is different from yours.

Docker fixes this by giving every piece of software its own little box — a **container** — that already has everything it needs inside it. The box runs on your machine, but its contents are isolated from the rest of your system. You can have ten of them running simultaneously, each with completely different Python versions, system libraries, even different Linux distributions inside, and none of them step on each other or on you.

## What a container actually is

A container is a process running on your computer, just like any other program — but the operating system has lied to that process about what's around it. From inside, the process sees:

- Its own filesystem (a tiny Linux install, or whatever the container's image provides)
- Its own network interface
- Its own process list (it can't see your other programs)

But it shares your computer's kernel, your CPU, and (if you ask) your network and folders. That's why containers are dramatically lighter than virtual machines: a VM ships a whole operating system plus a kernel and runs it on top of yours. A container ships just the parts above the kernel and uses yours. A VM takes minutes to boot and gigabytes of disk. A container takes seconds and tens of megabytes.

```
   Heavy:                          Light:
   ┌─────────────┐                 ┌──────────┐ ┌──────────┐
   │   App       │                 │  App A   │ │  App B   │
   ├─────────────┤                 ├──────────┤ ├──────────┤
   │   Libs      │                 │  Libs A  │ │  Libs B  │
   ├─────────────┤                 └────┬─────┘ └─────┬────┘
   │   Guest OS  │ ← VM                  │             │
   ├─────────────┤                       └──── Docker ─┘
   │  Hypervisor │                              │
   ├─────────────┤                       ┌──────┴───────┐
   │   Host OS   │                       │   Host OS    │
   └─────────────┘                       └──────────────┘
```

## Free and open source

The pieces that actually run containers — `containerd`, `runc`, the Docker engine — are open source under permissive licenses. The format containers use (OCI, the Open Container Initiative spec) is an open standard, so containers built with Docker also run on alternative engines like Podman or Kubernetes' runtime. You are not locked into anyone's product.

There is a company called Docker, Inc. that makes a commercial GUI app (Docker Desktop) and a hosted image registry (Docker Hub). You can use both for free for personal projects, or you can skip both entirely and run pure open-source Docker on Linux pushing to your own registry. Nothing in this primer requires you to pay anyone.

## Why it's a good toolbox item, even if you're not "deploying" anything

The same idea — "describe an environment in a file, run it in a box" — works at every scale:

- **Single command on your laptop.** `docker run somebody/cool-thing` and a moment later it's running. No system pollution.
- **A whole project's worth of services.** One `docker-compose.yml` file describes a database, a backend, a worker, a frontend — and `docker compose up` brings the whole thing online. Stop it with one command. Delete it with one command.
- **Cloud deployment.** The same image you ran locally can be pushed to a registry and pulled down on a server. The behavior is identical.
- **Industrial scale.** Kubernetes — what most of the modern internet runs on — schedules containers. The container you build today is, structurally, the same artifact those systems orchestrate.

You don't have to care about all of those. You can stop at "I can run somebody's cool GitHub project without breaking my laptop" and you've already gotten huge value from Docker.

## Why it supersedes per-language environments

If you've used `venv`, `conda`, `pyenv`, `pipenv`, `poetry`, `rbenv`, `nvm`, or `asdf` — Docker is doing the same job (isolation) but at the operating-system layer instead of the language layer. That has two big advantages:

1. **It's language-agnostic.** A Python project, a Rust binary, and a PostgreSQL database all use the same isolation mechanism. You learn it once.
2. **It captures *system* dependencies too.** Many Python projects need a system library (`ffmpeg`, `libpq`, CUDA drivers, etc.). A `venv` can't install those. A Dockerfile can.

This doesn't mean you should never use `venv` again — for a one-file script, `venv` is fine. But the moment a project starts needing more than one language, more than one service, or system-level dependencies, Docker becomes the easier path.

## The two things you'll keep hearing

Two words, often used loosely, that mean very specific things:

- **Image** — the recipe. A frozen, read-only snapshot of a filesystem plus instructions for what to run when it starts. Images have names like `python:3.12-slim` or `postgres:16`.
- **Container** — a running instance of an image. You can have many containers from the same image, like running the same `.exe` twice.

Lesson 04 belabors this distinction, because confusing the two is the most common stumbling block when starting out.

## Try it yourself

Before doing anything else: do you have Docker installed? If not, see [`installing-docker.md`](installing-docker.md). Otherwise run:

```bash
docker --version
docker compose version
```

If both print versions, you're ready for [`02_hello_world.md`](02_hello_world.md).

# Lesson 08: Registries — Pulling and Pushing Images

A **registry** is a server that stores images. So far, every time you typed `docker run ubuntu`, Docker silently pulled the image from a registry — by default, **Docker Hub** (https://hub.docker.com/).

Registries are how an image you build on your laptop gets onto a server, or into a colleague's hands.

## Pulling explicitly

`docker run` pulls if needed, but you can also pull on its own:

```bash
docker pull postgres:16
```

Useful when you want to grab images ahead of time (before a flight, before a workshop, etc.) without running them.

## Where images live in image names

The full form of an image reference is:

```
<registry-host>/<namespace>/<repository>:<tag>
```

Some examples expanded:

- `ubuntu` → `docker.io/library/ubuntu:latest` (Docker Hub's "official" images live under the `library` namespace, and the registry/tag are filled in by default.)
- `python:3.12-slim` → `docker.io/library/python:3.12-slim`.
- `ghcr.io/myname/myproject:v1` → an image hosted on **GitHub Container Registry**, under your account, version `v1`.
- `registry.example.com/team/service:1.4` → an image in some company's private registry.

If the registry isn't specified, Docker assumes `docker.io` (Docker Hub).

## Hosted registry options (and the FOSS take)

You have choices about where your images live. None of them locks you in — you can move images between registries with `docker pull` and `docker push`.

- **Docker Hub** — the default. Free for public images. Has rate limits on anonymous pulls (a real annoyance for CI, less so for personal use).
- **GitHub Container Registry (`ghcr.io`)** — free for public images, integrates with your GitHub account, no pull rate limit. A good choice if you already use GitHub.
- **GitLab Container Registry** — built into GitLab projects.
- **Self-hosted** — the reference Docker registry is itself open source. `docker run -d -p 5000:5000 registry:2` and you have your own registry running on your machine, no third party involved. Useful if you want full ownership of your images or you're working offline.

## Pushing your own image

1. **Create an account** on whichever registry you want to use. For Docker Hub, sign up at https://hub.docker.com/. For GHCR, you already have one (your GitHub account).

2. **Log in** from the command line:

   ```bash
   docker login                          # Docker Hub
   docker login ghcr.io                  # GitHub Container Registry
   ```

   You'll be prompted for a username and either a password or a personal access token (recommended; treat it like a password and store it carefully).

3. **Tag your image** with the destination address. Suppose you built `my-app` in lesson 05 and your Docker Hub username is `yourname`:

   ```bash
   docker tag my-app yourname/my-app:1.0
   ```

   `docker tag` doesn't copy the image — it just adds another name pointing at the same content. Now `docker images` shows both `my-app` and `yourname/my-app:1.0`.

4. **Push it:**

   ```bash
   docker push yourname/my-app:1.0
   ```

   Docker uploads it layer by layer to the registry.

5. **Confirm:** anyone (or you, from a different machine) can now run:

   ```bash
   docker pull yourname/my-app:1.0
   docker run yourname/my-app:1.0
   ```

That's the whole flow. Tag, push, pull, run.

## Tags as versions

Tags are how you publish multiple versions of the same image. Convention is to:

- Tag specific releases: `yourname/my-app:1.0`, `yourname/my-app:1.1`, …
- Also tag the most recent as `:latest` so people who don't specify a tag get something reasonable.

```bash
docker tag yourname/my-app:1.0 yourname/my-app:latest
docker push yourname/my-app:latest
```

`:latest` is a convention, not magic. It's just a tag named "latest", and you have to explicitly point it at whatever you want to be "latest".

## Public vs private

By default Docker Hub repositories are public. If you want a private one, you set that on the registry's website (Docker Hub has free private repos with limits; GHCR private images are free with reasonable limits tied to your GitHub plan). Pushing to a private repo works exactly the same as pushing to a public one — the only difference is who can pull.

## A small note on supply-chain caution

Anyone can publish an image to Docker Hub. When you run `docker run somebody/cool-thing`, you're trusting that "somebody" to not have put anything malicious in there. Use your judgment:

- **Official images** (the ones in the `library` namespace — `python`, `postgres`, `nginx`, `ubuntu`, etc.) are maintained by the projects themselves and are pretty trustworthy.
- **Verified publisher** images on Docker Hub are vetted by Docker.
- **Random images from random accounts** are the same risk as random code from random GitHub accounts. Read the Dockerfile if it's available; check the publish date and pull count; prefer well-known maintainers.

## Try it yourself

1. Tag the `my-app` image you built in lesson 05 with your registry username, then push it to a public Docker Hub repo.
2. From a different terminal (or after running `docker rmi yourname/my-app:1.0` to clear your local copy), `docker pull yourname/my-app:1.0`. Confirm it runs.
3. Move on to [`09_compose_basics.md`](09_compose_basics.md), where we stop typing long `docker run` commands.

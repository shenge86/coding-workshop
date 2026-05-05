# image_meaning_db

A self-contained semantic image search tool. Upload images (optionally with a description) to build up a database, then search by image to find the nearest neighbors by meaning. Runs as a single Docker service: a FastAPI backend that embeds images locally with CLIP (`clip-ViT-B-32`) and stores vectors in ChromaDB, served behind a minimal browser UI.

On first launch it auto-seeds the database with ~100 sample images from Lorem Picsum so you have something to search against immediately.

## Prerequisites

You need Docker Engine and the Docker Compose plugin. If you don't already have them:

- **Linux (Ubuntu/Debian):** follow the official install guide at https://docs.docker.com/engine/install/ubuntu/. After installing, add your user to the `docker` group so you don't need `sudo`:
  ```bash
  sudo usermod -aG docker $USER
  newgrp docker
  ```
- **macOS / Windows:** install Docker Desktop from https://docs.docker.com/desktop/. Compose is bundled.

Verify it works:
```bash
docker --version
docker compose version
```

## Running it

From the project root:

```bash
docker compose up -d --build
```

(If your Compose is the older standalone binary, use `docker-compose` with a hyphen instead.)

Then open http://localhost:8081 in your browser.

### What to expect on the first run

The first `up --build` is slow because it:

1. Installs Python deps including CPU-only PyTorch (~200 MB pip download).
2. Downloads the CLIP model weights (~600 MB) into a cached volume on first server start.
3. Fetches 100 seed images from picsum.photos and embeds them.

Watch progress with:
```bash
docker compose logs -f backend
```

You'll see `Model clip-ViT-B-32 ready.`, then `Seed: N images indexed...` messages as the database fills. The UI is usable throughout — refresh to see the image count climb.

Subsequent runs reuse the cached model and the existing database, so startup is fast.

## Using the UI

Two tabs:

- **Submit Image** — drop, paste (Ctrl/Cmd+V), or click to select an image. Add an optional description (e.g. `"red coffee mug on wooden desk"`) and click *Submit to Database*. The image is embedded and stored.
- **Search by Image** — drop/paste/select a query image. The backend embeds it and returns the most semantically similar stored images, ranked by cosine similarity, with any descriptions they were submitted with.

## API

If you want to hit the backend directly:

- `POST /api/submit` — multipart form: `file` (image), optional `description` (string). Returns `{id, filename, total_images}`.
- `POST /api/search` — multipart form: `file` (image), optional query param `n` (default 10). Returns ranked list of matches with similarity scores.
- `GET /api/images/{filename}` — serves a stored image.
- `GET /api/stats` — `{total_images: N}`.

## Stopping and resetting

```bash
docker compose down             # stop containers, keep data
docker compose down -v          # also delete the database, cached model, and stored images
```

If you wipe volumes, the next start will re-download the CLIP model and re-seed the 100 sample images.

## Configuration

Environment variables set in `docker-compose.yml`:

- `EMBEDDING_MODEL` — sentence-transformers model name. Default: `clip-ViT-B-32`. If you change this, wipe the `chroma_data` volume — embedding dimensions must match across all stored vectors.
- `SEED_COUNT` — number of sample images to seed on first launch. Default: `100`. Set to `0` to skip seeding.

Host port mapping is also in `docker-compose.yml`; change the left side of `"8081:8080"` if 8081 conflicts with something else on your machine.

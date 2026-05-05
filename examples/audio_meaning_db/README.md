# audio_meaning_db

A self-contained semantic audio search tool for **spoken audio**. Upload audio clips (optionally with a description) to build up a database, then search by audio to find the nearest neighbors by what's being said. Runs as a single Docker service: a FastAPI backend that transcribes speech locally with Whisper (`openai/whisper-base`), embeds the transcripts with a sentence-transformer (`all-MiniLM-L6-v2`), and stores vectors in ChromaDB, served behind a minimal browser UI.

Long uploads are split into **60-second segments**; each segment is transcribed and indexed independently. Search returns the best-matching segment along with a link to the full parent clip.

## Why Whisper + sentence embeddings (and not CLAP)

This tool is optimized for finding audio by *what is said*, not by *how it sounds*. Two recordings of the sentence "I love cats" embedded with CLAP would look similar regardless of content; two recordings saying "I love cats" vs "I'm fond of felines" would look very different. Whisper transcription + text embeddings inverts that: meaning-preserving paraphrases match, and acoustic differences (voice, accent, background noise) are ignored.

If you want music/SFX/ambient similarity instead, swap in CLAP — the plumbing is the same.

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

From this directory:

```bash
docker compose up -d --build
```

Then open http://localhost:8082 in your browser.

### What to expect on the first run

The first `up --build` is slow because it:

1. Installs Python deps including CPU-only PyTorch (~200 MB pip download) and `ffmpeg` + `libsndfile`.
2. Downloads the Whisper model (~150 MB) and the sentence-transformer (~80 MB) into a cached volume on first server start.
3. Starts with an **empty database** — no seeding. Upload your own audio.

Watch progress with:
```bash
docker compose logs -f backend
```

You'll see `ASR model openai/whisper-base ready.` and `Text embedding model ... ready.` once it's warmed up. Subsequent runs reuse the cached models and existing database, so startup is fast.

## Using the UI

Two tabs:

- **Submit Audio** — drop or click to select an audio file (mp3, wav, m4a, flac, ogg). Add an optional description and click *Submit to Database*. The file is chunked into 60-second segments, each transcribed and embedded. You'll see the per-segment transcripts once it's done.
- **Search by Audio** — drop or click to select a query clip (≤ 60 seconds, hard-enforced). The backend transcribes it, embeds the transcript, and returns the most semantically similar stored segments, ranked by cosine similarity. Each result shows the segment's transcript, a playable audio slice of just that segment, and a toggle to play the full parent clip.

## API

Direct endpoints:

- `POST /api/submit` — multipart form: `file` (audio), optional `description` (string). Returns `{parent_id, filename, segments_added, total_segments, duration_sec, segments}` where `segments` includes per-segment timestamps and transcripts.
- `POST /api/search` — multipart form: `file` (audio, ≤ 60 s), optional query param `n` (default 10). Returns `{results, query_transcript}` with ranked matches.
- `GET /api/audio/{filename}` — serves a stored audio file in its original format.
- `GET /api/segment/{parent_filename}?start=<sec>&end=<sec>` — serves a WAV slice of a segment.
- `GET /api/stats` — `{total_segments, total_clips}`.

## Stopping and resetting

```bash
docker compose down             # stop containers, keep data
docker compose down -v          # also delete the database, cached models, and stored audio
```

If you wipe volumes, the next start will re-download both models.

## Configuration

Environment variables set in `docker-compose.yml`:

- `ASR_MODEL` — HuggingFace Whisper model name. Default: `openai/whisper-base`. Smaller/faster: `openai/whisper-tiny`. Better quality: `openai/whisper-small` (~500 MB, slower on CPU). English-only variants (`-base.en`, `-tiny.en`) are slightly better for English-only content. If you change this, existing transcripts stay valid (only query behavior changes).
- `TEXT_EMBEDDING_MODEL` — sentence-transformers model name. Default: `sentence-transformers/all-MiniLM-L6-v2` (384-d). If you change this, wipe the `chroma_data` volume — embedding dimensions must match across all stored vectors.

Host port mapping is also in `docker-compose.yml`; change the left side of `"8082:8080"` if 8082 conflicts with something else.

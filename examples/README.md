# Example projects

Full, working projects you can clone, run, and tear apart. They're not lessons — they're more like worked examples. The point is to give you something concrete to look at when you're trying to imagine what your own project could look like (or to copy-paste from when one of them does roughly what you need).

These are intentionally on equal footing — there's no "beginner / intermediate / advanced" tier. Pick whichever interests you.

## Index

| Project | What it is | What you'll see in it |
|---------|------------|-----------------------|
| [`image_meaning_db/`](image_meaning_db/) | Search a folder of images by meaning, not filename. Drop in a query image, get back the closest matches. | CLIP embeddings, ChromaDB, FastAPI, a tiny browser UI, all in one Docker container. |
| [`audio_meaning_db/`](audio_meaning_db/) | Search spoken audio by what's said in it. Drop in a clip, get back the closest segments from your library. | Whisper transcription, sentence embeddings, segment chunking, FastAPI, Docker. |

More will be added over time.

## How to use these

Three reasonable modes, in increasing order of effort:

1. **Just run one.** Each project's README has a `docker compose up -d --build` line. Try it. Poke at the UI. Get a feel for what's possible.
2. **Read the code.** The backends are deliberately small — a single `main.py` per project. Open it, ask AI to walk you through any part you don't understand. This is one of the best ways to *see* how a complete small thing fits together.
3. **Fork and modify.** Copy the folder somewhere of your own, change things, see what breaks. Swap the embedding model. Change the seed images. Add a "delete by ID" endpoint. This is where it stops being an example and starts being a project.

## Prerequisites

Both current examples need Docker. See [`../reference/docker/`](../reference/docker/) for the basics; each project's README also links the official install guides.

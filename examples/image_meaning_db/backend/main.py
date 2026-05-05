import asyncio
import io
import os
import uuid
from pathlib import Path

import chromadb
import httpx
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "clip-ViT-B-32")
SEED_COUNT = int(os.environ.get("SEED_COUNT", "100"))
IMAGE_DIR = Path("/app/images")
CHROMA_DIR = Path("/app/chroma_data")

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Image Meaning DB")

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_or_create_collection(
    name="images",
    metadata={"hnsw:space": "cosine"},
)

print(f"Loading embedding model {EMBEDDING_MODEL}...")
embedder = SentenceTransformer(EMBEDDING_MODEL)
print(f"Model {EMBEDDING_MODEL} ready.")


def load_image(image_bytes: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    max_dim = 512
    if max(img.size) > max_dim:
        img.thumbnail((max_dim, max_dim), Image.LANCZOS)
    return img


def get_embedding(img: Image.Image) -> list[float]:
    vec = embedder.encode(img, convert_to_numpy=True, normalize_embeddings=True)
    return vec.tolist()


async def _seed_database():
    if SEED_COUNT <= 0:
        print("Seed: SEED_COUNT is 0, skipping.")
        return
    if collection.count() > 0:
        print(f"Seed: collection already has {collection.count()} images, skipping.")
        return
    print(f"Seed: fetching {SEED_COUNT} sample images from picsum.photos...")
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            resp = await client.get(
                "https://picsum.photos/v2/list",
                params={"page": 1, "limit": SEED_COUNT},
            )
            resp.raise_for_status()
            photos = resp.json()

            sem = asyncio.Semaphore(8)

            async def fetch(p):
                async with sem:
                    try:
                        r = await client.get(f"https://picsum.photos/id/{p['id']}/512/512")
                        r.raise_for_status()
                        return p, r.content
                    except Exception as e:
                        print(f"Seed: fetch failed id={p['id']}: {e}")
                        return None

            fetched = await asyncio.gather(*(fetch(p) for p in photos))
    except Exception as e:
        print(f"Seed: list fetch failed: {e}")
        return

    added = 0
    for item in fetched:
        if item is None:
            continue
        p, image_bytes = item
        try:
            img = load_image(image_bytes)
            embedding = await asyncio.to_thread(get_embedding, img)
            image_id = f"seed-{p['id']}"
            filename = f"{image_id}.jpg"
            (IMAGE_DIR / filename).write_bytes(image_bytes)
            collection.add(
                ids=[image_id],
                embeddings=[embedding],
                metadatas=[{
                    "filename": filename,
                    "original_name": f"picsum-{p['id']}.jpg",
                    "description": f"Photo by {p['author']}",
                }],
            )
            added += 1
            if added % 10 == 0:
                print(f"Seed: {added} images indexed...")
        except Exception as e:
            print(f"Seed: embed/store failed id={p['id']}: {e}")
    print(f"Seed: finished, {added} images added.")


@app.on_event("startup")
async def on_startup():
    asyncio.create_task(_seed_database())


@app.post("/api/submit")
async def submit_image(
    file: UploadFile = File(...),
    description: str = Form(""),
):
    """Upload an image, embed it, and store it."""
    image_bytes = await file.read()
    img = load_image(image_bytes)

    embedding = get_embedding(img)

    image_id = str(uuid.uuid4())
    ext = Path(file.filename or "image.png").suffix or ".png"
    filename = f"{image_id}{ext}"
    filepath = IMAGE_DIR / filename
    filepath.write_bytes(image_bytes)

    collection.add(
        ids=[image_id],
        embeddings=[embedding],
        metadatas=[{
            "filename": filename,
            "original_name": file.filename or "unknown",
            "description": description,
        }],
    )

    count = collection.count()
    return {"id": image_id, "filename": filename, "total_images": count}


@app.post("/api/search")
async def search_image(file: UploadFile = File(...), n: int = 10):
    """Upload an image, embed it, and find nearest neighbors."""
    image_bytes = await file.read()
    img = load_image(image_bytes)

    embedding = get_embedding(img)

    count = collection.count()
    if count == 0:
        return {"results": [], "message": "No images in database yet."}

    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(n, count),
        include=["distances", "metadatas"],
    )

    matches = []
    for i, doc_id in enumerate(results["ids"][0]):
        distance = results["distances"][0][i]
        metadata = results["metadatas"][0][i]
        similarity = 1 - distance  # cosine distance -> similarity
        matches.append({
            "id": doc_id,
            "filename": metadata["filename"],
            "original_name": metadata["original_name"],
            "description": metadata.get("description", ""),
            "similarity": round(similarity, 4),
        })

    return {"results": matches}


@app.get("/api/images/{filename}")
async def get_image(filename: str):
    """Serve a stored image."""
    filepath = IMAGE_DIR / filename
    if not filepath.exists():
        return {"error": "Image not found"}
    return FileResponse(filepath)


@app.get("/api/stats")
async def stats():
    """Return database stats."""
    return {"total_images": collection.count()}


@app.get("/", response_class=HTMLResponse)
async def index():
    return Path("static/index.html").read_text()

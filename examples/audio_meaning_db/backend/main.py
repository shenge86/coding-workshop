import asyncio
import io
import os
import uuid
from pathlib import Path

import chromadb
import numpy as np
import soundfile as sf
import soxr
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, Response
from pydub import AudioSegment
from sentence_transformers import SentenceTransformer
from transformers import pipeline

ASR_MODEL = os.environ.get("ASR_MODEL", "openai/whisper-base")
TEXT_EMBEDDING_MODEL = os.environ.get(
    "TEXT_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
)
SEGMENT_LENGTH_SEC = 60
MIN_TAIL_SEGMENT_SEC = 3.0
SEARCH_MAX_SEC = 60.5
TARGET_SAMPLE_RATE = 16000
AUDIO_DIR = Path("/app/audio")
CHROMA_DIR = Path("/app/chroma_data")

AUDIO_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Audio Meaning DB")

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_or_create_collection(
    name="audio_segments",
    metadata={"hnsw:space": "cosine"},
)

print(f"Loading ASR model {ASR_MODEL}...")
asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model=ASR_MODEL,
    chunk_length_s=30,
    device="cpu",
)
print(f"ASR model {ASR_MODEL} ready.")

print(f"Loading text embedding model {TEXT_EMBEDDING_MODEL}...")
text_embedder = SentenceTransformer(TEXT_EMBEDDING_MODEL)
print(f"Text embedding model {TEXT_EMBEDDING_MODEL} ready.")


def _load_with_pydub(audio_bytes: bytes) -> tuple[np.ndarray, int]:
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    if audio.channels > 1:
        samples = samples.reshape(-1, audio.channels)
    max_val = float(2 ** (audio.sample_width * 8 - 1))
    samples = samples / max_val
    return samples, audio.frame_rate


def load_audio(audio_bytes: bytes, filename: str) -> np.ndarray:
    """Decode audio bytes to mono float32 at TARGET_SAMPLE_RATE."""
    ext = Path(filename).suffix.lower().lstrip(".")
    data: np.ndarray
    sr: int
    if ext in ("wav", "flac", "ogg", "oga"):
        try:
            data, sr = sf.read(io.BytesIO(audio_bytes), dtype="float32", always_2d=False)
        except Exception:
            data, sr = _load_with_pydub(audio_bytes)
    else:
        data, sr = _load_with_pydub(audio_bytes)

    if data.ndim > 1:
        data = data.mean(axis=1)
    data = np.asarray(data, dtype=np.float32)

    if sr != TARGET_SAMPLE_RATE:
        data = soxr.resample(data, sr, TARGET_SAMPLE_RATE, quality="HQ").astype(np.float32)

    return data


def segment_audio(audio: np.ndarray) -> list[tuple[float, float, np.ndarray]]:
    """Split into ~60s segments. Returns [(start_sec, end_sec, samples), ...]."""
    sr = TARGET_SAMPLE_RATE
    total_sec = len(audio) / sr
    if total_sec <= SEGMENT_LENGTH_SEC:
        return [(0.0, total_sec, audio)]

    segments: list[tuple[float, float, np.ndarray]] = []
    segment_samples = SEGMENT_LENGTH_SEC * sr
    num_full = len(audio) // segment_samples
    for i in range(num_full):
        start = i * segment_samples
        end = start + segment_samples
        segments.append((start / sr, end / sr, audio[start:end]))

    tail_start = num_full * segment_samples
    tail = audio[tail_start:]
    tail_sec = len(tail) / sr
    if tail_sec >= MIN_TAIL_SEGMENT_SEC:
        segments.append((tail_start / sr, total_sec, tail))

    return segments


def transcribe(audio: np.ndarray) -> str:
    """Transcribe mono 16kHz float32 audio to text."""
    result = asr_pipeline({"array": audio, "sampling_rate": TARGET_SAMPLE_RATE})
    return (result.get("text") or "").strip()


def embed_text(text: str) -> list[float]:
    query = text if text else "(no speech detected)"
    vec = text_embedder.encode(query, convert_to_numpy=True, normalize_embeddings=True)
    return vec.tolist()


def fmt_time(sec: float) -> str:
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


@app.post("/api/submit")
async def submit_audio(
    file: UploadFile = File(...),
    description: str = Form(""),
):
    audio_bytes = await file.read()

    parent_id = str(uuid.uuid4())
    ext = Path(file.filename or "audio.wav").suffix or ".wav"
    filename = f"{parent_id}{ext}"
    filepath = AUDIO_DIR / filename
    filepath.write_bytes(audio_bytes)

    try:
        audio = load_audio(audio_bytes, file.filename or "")
    except Exception as e:
        filepath.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=f"Could not decode audio: {e}")

    total_sec = len(audio) / TARGET_SAMPLE_RATE
    segments = segment_audio(audio)
    is_full_clip = len(segments) == 1

    ids: list[str] = []
    embeddings: list[list[float]] = []
    metadatas: list[dict] = []
    segment_summaries: list[dict] = []

    for i, (start, end, samples) in enumerate(segments):
        transcript = await asyncio.to_thread(transcribe, samples)
        embedding = await asyncio.to_thread(embed_text, transcript)
        segment_id = f"{parent_id}:{i}"
        ids.append(segment_id)
        embeddings.append(embedding)
        metadatas.append({
            "parent_id": parent_id,
            "parent_filename": filename,
            "parent_original_name": file.filename or "unknown",
            "segment_index": i,
            "start_sec": float(start),
            "end_sec": float(end),
            "parent_duration_sec": float(total_sec),
            "description": description,
            "transcript": transcript,
            "is_full_clip": is_full_clip,
        })
        segment_summaries.append({
            "segment_index": i,
            "start_sec": float(start),
            "end_sec": float(end),
            "transcript": transcript,
        })

    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

    return {
        "parent_id": parent_id,
        "filename": filename,
        "segments_added": len(segments),
        "total_segments": collection.count(),
        "duration_sec": total_sec,
        "segments": segment_summaries,
    }


@app.post("/api/search")
async def search_audio(file: UploadFile = File(...), n: int = 10):
    audio_bytes = await file.read()
    try:
        audio = load_audio(audio_bytes, file.filename or "")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not decode audio: {e}")

    duration_sec = len(audio) / TARGET_SAMPLE_RATE
    if duration_sec > SEARCH_MAX_SEC:
        raise HTTPException(
            status_code=400,
            detail=f"Search audio must be at most {SEGMENT_LENGTH_SEC}s. Got {duration_sec:.1f}s.",
        )

    count = collection.count()
    if count == 0:
        return {"results": [], "message": "No audio in database yet.", "query_transcript": ""}

    transcript = await asyncio.to_thread(transcribe, audio)
    embedding = await asyncio.to_thread(embed_text, transcript)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(n, count),
        include=["distances", "metadatas"],
    )

    matches = []
    for i, doc_id in enumerate(results["ids"][0]):
        distance = results["distances"][0][i]
        metadata = results["metadatas"][0][i]
        similarity = 1 - distance
        matches.append({
            "id": doc_id,
            "parent_filename": metadata["parent_filename"],
            "parent_original_name": metadata["parent_original_name"],
            "segment_index": metadata["segment_index"],
            "start_sec": metadata["start_sec"],
            "end_sec": metadata["end_sec"],
            "parent_duration_sec": metadata["parent_duration_sec"],
            "description": metadata.get("description", ""),
            "transcript": metadata.get("transcript", ""),
            "is_full_clip": metadata.get("is_full_clip", True),
            "similarity": round(similarity, 4),
        })

    return {"results": matches, "query_transcript": transcript}


@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    filepath = AUDIO_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(filepath)


@app.get("/api/segment/{parent_filename}")
async def get_segment(parent_filename: str, start: float, end: float):
    filepath = AUDIO_DIR / parent_filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Audio not found")
    if end <= start or start < 0:
        raise HTTPException(status_code=400, detail="Invalid segment range")

    audio_bytes = filepath.read_bytes()
    audio = load_audio(audio_bytes, parent_filename)
    sr = TARGET_SAMPLE_RATE
    start_idx = max(0, int(start * sr))
    end_idx = min(len(audio), int(end * sr))
    if end_idx <= start_idx:
        raise HTTPException(status_code=400, detail="Empty segment slice")

    buf = io.BytesIO()
    sf.write(buf, audio[start_idx:end_idx], sr, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return Response(content=buf.read(), media_type="audio/wav")


@app.get("/api/stats")
async def stats():
    total_segments = collection.count()
    unique_parents = 0
    if total_segments > 0:
        all_meta = collection.get(include=["metadatas"])
        unique_parents = len({m["parent_id"] for m in all_meta["metadatas"]})
    return {"total_segments": total_segments, "total_clips": unique_parents}


@app.get("/", response_class=HTMLResponse)
async def index():
    return Path("static/index.html").read_text()

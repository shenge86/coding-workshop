"""FastAPI backend for the everything_function web UI.

This server doesn't do any AI work itself. It imports the same `ai_xxx`
functions used by the terminal demo scripts and exposes them as HTTP
endpoints so a browser can call them. The point: the web UI is just
another front-end for the *same Python functions* you can run from
`scripts/`. Nothing magic is happening in here.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

SCRIPTS_DIR = Path("/app/scripts")
SAMPLES_DIR = Path("/app/sample_images")
sys.path.insert(0, str(SCRIPTS_DIR))

import action_list  # noqa: E402
import algebra_roots  # noqa: E402
import arithmetic  # noqa: E402
import image_label  # noqa: E402
import ocr  # noqa: E402
import prime_factorization  # noqa: E402
import recipe_from_food  # noqa: E402
import sentiment  # noqa: E402
import summarize  # noqa: E402
import translate  # noqa: E402

app = FastAPI(title="everything_function")


# ------ arithmetic ------------------------------------------------------------

class ArithRequest(BaseModel):
    op: str
    a: float
    b: float


@app.post("/api/arithmetic")
def api_arithmetic(req: ArithRequest):
    if req.op not in arithmetic.OPS:
        raise HTTPException(400, f"unknown op: {req.op!r}")
    ai_fn, py_fn = arithmetic.OPS[req.op]
    ai_result = ai_fn(req.a, req.b).strip().rstrip(".")
    py_result = py_fn(req.a, req.b)
    return {"ai": ai_result, "python": str(py_result)}


# ------ algebra ---------------------------------------------------------------

class AlgebraRequest(BaseModel):
    coefficients: list[float]


@app.post("/api/algebra")
def api_algebra(req: AlgebraRequest):
    if len(req.coefficients) < 2:
        raise HTTPException(400, "need at least 2 coefficients")
    polynomial = algebra_roots.format_polynomial(req.coefficients)
    ai_result = algebra_roots.ai_polynomial_roots(req.coefficients)
    py_result = algebra_roots.py_polynomial_roots(req.coefficients)
    return {"polynomial": polynomial, "ai": ai_result, "python": py_result}


# ------ prime factorization ---------------------------------------------------

class PrimeRequest(BaseModel):
    n: int


@app.post("/api/prime_factorization")
def api_prime(req: PrimeRequest):
    ai_result = prime_factorization.ai_prime_factorize(req.n).strip().rstrip(".")
    py_result = prime_factorization.py_prime_factorize(req.n)
    return {"ai": ai_result, "python": py_result}


# ------ text demos ------------------------------------------------------------

class SentimentRequest(BaseModel):
    text: str


@app.post("/api/sentiment")
def api_sentiment(req: SentimentRequest):
    return {"result": sentiment.ai_sentiment(req.text)}


class TranslateRequest(BaseModel):
    text: str
    target_language: str


@app.post("/api/translate")
def api_translate(req: TranslateRequest):
    return {"result": translate.ai_translate(req.text, req.target_language)}


class SummarizeRequest(BaseModel):
    text: str
    max_words: int = 30


@app.post("/api/summarize")
def api_summarize(req: SummarizeRequest):
    return {"result": summarize.ai_summarize(req.text, max_words=req.max_words)}


class ActionListRequest(BaseModel):
    description: str


@app.post("/api/action_list")
def api_action_list(req: ActionListRequest):
    return {"result": "- " + action_list.ai_action_list(req.description)}


# ------ image demos -----------------------------------------------------------

def _resolve_image(file: UploadFile | None, sample: str | None) -> Path:
    """Save the upload to /tmp, or return the named sample image's path."""
    if file is not None and file.filename:
        suffix = Path(file.filename).suffix.lower() or ".jpg"
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        try:
            tmp.write(file.file.read())
            return Path(tmp.name)
        finally:
            tmp.close()
    if sample:
        path = SAMPLES_DIR / sample
        if not path.exists():
            raise HTTPException(404, f"sample image not found: {sample!r}")
        return path
    raise HTTPException(400, "must provide either an uploaded file or a sample name")


@app.post("/api/image_label")
def api_image_label(
    file: UploadFile | None = File(None),
    sample: str | None = Form(None),
):
    path = _resolve_image(file, sample)
    return {"result": image_label.ai_image_label(path)}


@app.post("/api/recipe_from_food")
def api_recipe(
    file: UploadFile | None = File(None),
    sample: str | None = Form(None),
):
    path = _resolve_image(file, sample)
    return {"result": recipe_from_food.ai_recipe_from_food(path)}


@app.post("/api/ocr")
def api_ocr(
    file: UploadFile | None = File(None),
    sample: str | None = Form(None),
):
    path = _resolve_image(file, sample)
    return {"result": ocr.ai_ocr(path)}


# ------ sample images ---------------------------------------------------------

@app.get("/api/sample_images")
def list_samples():
    return [
        {"name": p.name, "url": f"/api/sample_images/{p.name}"}
        for p in sorted(SAMPLES_DIR.glob("*.jpg"))
    ]


@app.get("/api/sample_images/{name}")
def get_sample(name: str):
    path = SAMPLES_DIR / name
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png"} or not path.exists():
        raise HTTPException(404)
    # Pin to the samples directory so we can't escape via "../" tricks.
    if path.resolve().parent != SAMPLES_DIR.resolve():
        raise HTTPException(404)
    return FileResponse(path)


# Static frontend served from /
app.mount("/", StaticFiles(directory="/app/static", html=True), name="static")

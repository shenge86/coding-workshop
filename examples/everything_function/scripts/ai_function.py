"""The one-and-only AI primitive used by every demo in this folder.

Every script in scripts/ imports `ask` from this module. The whole point of
the example is that *every* "smart function" you'll see is the same call —
just a different prompt going in, and a string coming back out. The model
doesn't know whether it's doing arithmetic, sentiment analysis, or reading
text out of a photo. It is, in every case, predicting what comes next.

The model runs locally inside the `ollama` container started by the
docker-compose file alongside this script. We hit its HTTP API; nothing
about your input ever leaves the machine.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

import httpx

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.5:9b")

# Reasonable timeout for a CPU-only first run; vision calls can be slow.
_TIMEOUT = httpx.Timeout(connect=10.0, read=300.0, write=60.0, pool=10.0)


def ask(prompt: str, image: str | Path | None = None, *, temperature: float = 0.0) -> str:
    """Ask the local model to continue some text.

    Args:
        prompt: The text the model sees. Whatever you write here is the
            "body" of your AI function — the same way regular Python functions
            have a body of code, an AI function has a body of prompt.
        image: Optional path to a local image. When provided, the model
            sees the image alongside the prompt (this needs a vision-capable
            model — `qwen2.5vl` is the default).
        temperature: 0 makes outputs roughly deterministic, which is what we
            want for demos. Crank it up for more variety, down for fewer surprises.

    Returns:
        The model's continuation as a plain string, with surrounding whitespace
        stripped.
    """
    payload: dict = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature},
        # Some Qwen builds support a "thinking" mode where the model writes
        # out an internal monologue before answering. For this workshop we
        # want clean, direct completions, so we ask for that explicitly.
        "think": False,
    }

    if image is not None:
        image_path = Path(image)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        payload["images"] = [base64.b64encode(image_path.read_bytes()).decode("ascii")]

    with httpx.Client(timeout=_TIMEOUT) as client:
        try:
            r = client.post(f"{OLLAMA_URL}/api/generate", json=payload)
        except httpx.ConnectError as e:
            raise RuntimeError(
                f"Could not reach Ollama at {OLLAMA_URL}. "
                "Is the docker-compose stack running? Try `docker compose up -d`."
            ) from e
        r.raise_for_status()
        return r.json()["response"].strip()


if __name__ == "__main__":
    # Sanity check — confirms the model is reachable and answering.
    print(f"Asking {OLLAMA_MODEL} at {OLLAMA_URL} to say hello...")
    print(ask("Say hello in five words or fewer."))

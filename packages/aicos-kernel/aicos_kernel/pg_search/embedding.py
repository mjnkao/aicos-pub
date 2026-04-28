from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass


DEFAULT_MODEL = "text-embedding-3-small"
DEFAULT_DIMENSIONS = 1536
MAX_CHARS = 8000
APPROX_CHARS_PER_TOKEN = 4


@dataclass(frozen=True)
class EmbeddingConfig:
    enabled: bool
    model: str
    dimensions: int
    api_key: str
    reason: str


def embedding_config() -> EmbeddingConfig:
    mode = os.environ.get("AICOS_EMBEDDINGS", "auto").strip().lower()
    if mode in {"0", "false", "off", "disabled", "none"}:
        return EmbeddingConfig(False, DEFAULT_MODEL, DEFAULT_DIMENSIONS, "", "disabled by AICOS_EMBEDDINGS")
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    model = os.environ.get("AICOS_EMBEDDING_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    try:
        dimensions = int(os.environ.get("AICOS_EMBEDDING_DIMENSIONS", str(DEFAULT_DIMENSIONS)))
    except ValueError:
        dimensions = DEFAULT_DIMENSIONS
    if not api_key:
        return EmbeddingConfig(False, model, dimensions, "", "OPENAI_API_KEY not set")
    return EmbeddingConfig(True, model, dimensions, api_key, "enabled")


class EmbeddingClient:
    def __init__(self, config: EmbeddingConfig) -> None:
        self.config = config

    def embed(self, text: str) -> list[float]:
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not self.config.enabled:
            raise RuntimeError(self.config.reason)
        payload = {
            "model": self.config.model,
            "input": [text[:MAX_CHARS] for text in texts],
            "dimensions": self.config.dimensions,
        }
        data = json.dumps(payload).encode("utf-8")
        last_error: Exception | None = None
        for attempt in range(5):
            req = urllib.request.Request(
                "https://api.openai.com/v1/embeddings",
                data=data,
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=60) as response:
                    body = json.loads(response.read().decode("utf-8"))
                rows = sorted(body["data"], key=lambda item: item["index"])
                return [list(map(float, row["embedding"])) for row in rows]
            except urllib.error.HTTPError as exc:
                last_error = exc
                retry_after = exc.headers.get("retry-after")
                if exc.code == 429 and retry_after:
                    try:
                        time.sleep(min(int(retry_after), 120))
                        continue
                    except ValueError:
                        pass
            except Exception as exc:  # noqa: BLE001 - network/client fallback path
                last_error = exc
            if attempt < 4:
                time.sleep(min(4 * (2**attempt), 60))
        raise RuntimeError(f"embedding request failed: {last_error}")


def vector_literal(values: list[float]) -> str:
    return "[" + ",".join(f"{value:.8f}" for value in values) + "]"


def approximate_tokens(text: str) -> int:
    return max(1, round(len(text) / APPROX_CHARS_PER_TOKEN)) if text else 0

# src/services/translator.py
import httpx
from transformers import pipeline, Pipeline
from functools import lru_cache
import logging
from typing import cast, Any

# -------------------------------------------------------------------
# Logging setup
# -------------------------------------------------------------------
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Hugging Face model pipeline helpers
# -------------------------------------------------------------------


@lru_cache(maxsize=32)
def get_translator(model_name: str, model_type: str) -> Pipeline:
    """
    Return a cached Hugging Face pipeline for a given model name and type.

    Uses different pipeline tasks depending on the model type:
      - "marianmt" → translation task
      - "t5" (and similar) → text2text-generation task

    The @lru_cache decorator ensures the model is only loaded once per process.
    Literal[...] restricts `task` to valid pipeline names, helping type checkers
    (MyPy, Pylance) and avoiding false errors.
    """

    task = "translation" if model_type == "marianmt" else "text2text-generation"

    try:
        translator = pipeline(task, model=model_name)
        return translator
    except Exception as e:
        logger.exception(f"Failed to load model '{model_name}': {e}")
        raise


# -------------------------------------------------------------------
# Ollama model client
# -------------------------------------------------------------------


async def ollama_translate(
    model_name: str,
    prompt: str,
    endpoint: str = "http://localhost:11434/api/generate",
    generation_params: dict[str, Any] | None = None,
) -> str:
    """
    Send a translation request to a locally running Ollama instance.

    Args:
        model_name: Name of the Ollama model (e.g. "gemma3-4B").
        prompt: Translation prompt text.
        endpoint: Ollama REST API endpoint URL.
        generation_params: Optional generation parameters (e.g. temperature).

    Returns:
        The translated text returned by the Ollama API.
    """
    payload = {"model": model_name, "prompt": prompt, "stream": False}
    if generation_params:
        payload.update(generation_params)
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()

        translated_text = (
            data.get("response", "").strip() if isinstance(data, dict) else str(data)
        )

        return translated_text

    except httpx.RequestError as e:
        err = cast(httpx.HTTPStatusError, e)
        logger.error(
            "HTTP request to Ollama API failed:",
            err.response.status_code,
            err.response.url,
            err.response.text,
        )
        raise
    except Exception as e:
        logger.exception("Unexpected error while contacting Ollama:", e)
        raise

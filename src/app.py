"""
A lightweight FastAPI-based multi-lingual translation web app.

Features:
- Use Hugging Fce MarianMT models for translation.
- Loads supported language pairs dynamically from a JSON config file.
- Serves as a simple static HTML page for user interaction.
- Provides an API endpoint for programmatic translation.

Usage:
    uvicorn app:app --reload
Then visit: http://127.0.0.1:8000
"""

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, List, Dict, cast

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from transformers import pipeline

# ---------------- CONFIG ----------------

CFG_PATH = Path(__file__).parent.parent / "config.json"
INDEX_HTML_PATH = Path(__file__).parent.parent / "index.html"


def load_config() -> Dict[str, str]:
    """
    Load the translation model mapping from a JSON config file.

    Returns:
        Dict mapping "source-target" language codes (e.g. "de-en") to Hugging Face model names.
    """
    with open(CFG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["supported"]


SUPPORTED_MODELS = load_config()

# ---------------- APP SETUP ----------------

app = FastAPI(title="Multi-lingual Translation App")


class TranslateRequest(BaseModel):
    """Schema for POST /api/translate"""

    text: str
    source_lang: str
    target_lang: str


@lru_cache(maxsize=32)
def get_translator(model_name: str):
    """
    Cache and return a Hugging Face translation pipeline for a given model name.
    The @lru_cache decorator ensures we don't reload models repeatedly.
    """
    return pipeline("translation", model=model_name)


# ---------------- ROUTES ----------------


@app.get("/", response_class=HTMLResponse)
def serve_homepage():
    """Serve the static HTML front-end page."""
    return INDEX_HTML_PATH.read_text(encoding="utf-8")


@app.post("/api/translate")
def translate_text(body: TranslateRequest):
    """
    Translate input text from source_lang to target_lang.

    - Reads model mapping from config.json
    - Loads the appropriate translation model (cached)
    - Returns translated text as JSON

    Example request:
        {
            "text": "Hallo Welt",
            "source_lang": "de",
            "target_lang": "en"
        }
    """
    # Build key like "de-en" and find model
    lang_key = f"{body.source_lang}-{body.target_lang}"

    if lang_key not in SUPPORTED_MODELS:
        return JSONResponse(
            {"error": f"Unsupported language pair: {lang_key}. Check config.json."},
            status_code=400,
        )

    model_name = SUPPORTED_MODELS[lang_key]
    translator = get_translator(model_name)

    # Perform translation
    try:
        # cast() only informs static type checkers (Pylance, MyPy); no runtime type change or validation.
        output = cast(List[Dict[str, Any]], translator(body.text, max_length=512))
        return {"translated_text": output[0]["translation_text"]}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

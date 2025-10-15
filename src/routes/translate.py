import logging
from typing import Any, Dict, List, cast
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from models.schemas import TranslateRequest, TranslateResponse
from services.config_loader import (
    SUPPORTED_MODELS,
    SUPPORTED_LANGS,
    PARAM_WHITELIST,
    INDEX_HTML_PATH,
)
from services.translator import get_translator, ollama_translate
from services.sanitizer import sanitize_generation_params

# -------------------------------------------------------------------
# Router setup
# -------------------------------------------------------------------
router = APIRouter()
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@router.get("/", response_class=HTMLResponse)
def serve_homepage():
    """Serve the static HTML front-end page."""
    return INDEX_HTML_PATH.read_text(encoding="utf-8")


@router.get("/api/models")
def list_models() -> list[dict[str, str]]:
    """
    Return all available models for front-end dropdown
    selection with a list comprehension.
    """
    return [
        {
            "key": key,
            "display_name": val["display_name"],
            "type": val["type"],
        }
        for key, val in SUPPORTED_MODELS.items()
    ]


@router.get("/api/languages")
def list_languages() -> list[dict[str, str]]:
    """
    Return all supported languages as a list of {code, name} objects
    for building dropdowns on the front end.
    """
    return [{"code": code, "name": name} for code, name in SUPPORTED_LANGS.items()]


@router.post("/api/translate", response_model=TranslateResponse)
async def translate_text(body: TranslateRequest):
    """
    Translate input text from source_lang to target_lang
    based on selected model and language pair.

    Example request:
        {
            "text": "Hallo Welt",
            "source_lang": "de",
            "target_lang": "en"
            "model_key": "helsinki-marian"
        }
    """
    # ---------------- Get model info ----------------
    model_info = SUPPORTED_MODELS.get(body.model_key)
    if not model_info:
        raise HTTPException(
            status_code=400, detail=f"Unknown model_key provided: {body.model_key}."
        )

    model_type = model_info["type"]
    generation_params = sanitize_generation_params(
        model_type,
        model_info.get("generation_params", {}),
        PARAM_WHITELIST,
    )

    try:
        # --- Case 1: Helsinki-NLP MarianMT models ---
        if model_type == "marianmt":
            lang_pair = f"{body.source_lang}-{body.target_lang}"
            pairs = model_info.get("pairs", {})
            model_name = pairs.get(lang_pair)
            if not model_name:
                available = ", ".join(sorted(pairs.keys()))
                raise HTTPException(
                    status_code=400,
                    detail=f"Language pair '{lang_pair}' unsupported. Available pairs: {available}",
                )

            translator = get_translator(model_name, model_type)
            output = cast(
                List[Dict[str, Any]], translator(body.text, **generation_params)
            )
            translated_text = output[0]["translation_text"]

        # --- Case 2: Hugging Face text2text models (e.g., Flan-T5)
        elif model_type == "t5":
            source_name = SUPPORTED_LANGS.get(body.source_lang)
            target_name = SUPPORTED_LANGS.get(body.target_lang)
            if not source_name or not target_name:
                raise HTTPException(
                    status_code=400, detail="language code is unsupported."
                )

            prompt = f"Translate {source_name} to {target_name}: \n{body.text}"
            translator = get_translator(model_info["model"], model_type)
            output = cast(List[Dict[str, Any]], translator(prompt, **generation_params))
            translated_text = output[0]["generated_text"]

        # --- Case 3: Ollama-based models (local LLMs) ---
        elif model_type == "ollama":
            source_name = SUPPORTED_LANGS[body.source_lang]
            target_name = SUPPORTED_LANGS[body.target_lang]
            if not source_name or not target_name:
                raise HTTPException(
                    status_code=400, detail="language code is unsupported."
                )

            prompt = f"translate {source_name} to {target_name}: \n{body.text}"

            translated_text = await ollama_translate(
                model_name=model_info["model"],
                prompt=prompt,
                endpoint=model_info.get(
                    "endpoint", "http://localhost:11434/api/generate"
                ),
                generation_params=generation_params,
            )

            if not translated_text:
                raise HTTPException(
                    status_code=502, detail="Empty response from Ollama model."
                )

        else:
            raise HTTPException(
                status_code=400, detail=f"Unsupported model type: {model_type}"
            )

        return TranslateResponse(translated_text=translated_text)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Translation failed for model '%s': %s", body.model_key, e)
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

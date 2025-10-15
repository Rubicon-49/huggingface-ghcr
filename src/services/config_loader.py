# src/services/config_loader.py
import json
from pathlib import Path
from typing import Any
import logging

# -------------------------------------------------------------------
# Logging setup
# -------------------------------------------------------------------

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Configuration file paths
# -------------------------------------------------------------------

CFG_PATH = Path(__file__).parent.parent.parent / "config.json"
INDEX_HTML_PATH = Path(__file__).parent.parent.parent / "index.html"

# -------------------------------------------------------------------
# Load configuration
# -------------------------------------------------------------------


def load_config(path: Path = CFG_PATH) -> dict[str, Any]:
    """
    Load the translation model configuration from a JSON file.

    Args:
        path: Path to the configuration JSON file (defaults to project root config.json).

    Returns:
        A dictionary containing all configuration keys.
    """
    if not path.exists():
        logger.error(f"Configuration file not found at {path}")
        raise FileNotFoundError(f"Configuration file not found at {path}")

    try:
        with open(CFG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from config file: {e}")
        raise


# -------------------------------------------------------------------
# Lazy-loaded global config
# -------------------------------------------------------------------
try:
    CFG = load_config()
    SUPPORTED_MODELS = CFG.get("supported_models", {})
    SUPPORTED_LANGS = CFG.get("supported_languages", {})
    PARAM_WHITELIST = CFG.get("param_whitelist", {})
except Exception as e:
    logger.critical(f"Failed to load configuration: {e}")
    raise


# -------------------------------------------------------------------
# Helper acccessor functions
# -------------------------------------------------------------------
def get_model_info(model_key: str) -> dict[str, Any] | None:
    """
    Retrieve a model configuration by key.
    """
    model = SUPPORTED_MODELS.get(model_key)
    if not model:
        logger.warning(f"Model key '{model_key}' not found in supported models.")
    return model


def get_language_name(lang_code: str) -> str | None:
    """
    Retrieve a human-readable language name by its code.
    """
    return SUPPORTED_LANGS.get(lang_code)

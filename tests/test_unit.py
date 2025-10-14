"""
Unit tests for the translation app.
These tests don't start the FastAPI server - they test internal logic.
"""

import json
from pathlib import Path
from src.app import load_config, get_translator, SUPPORTED_MODELS
from typing import Any, List, Dict, cast

def test_config_loads_correctly():
    """Ensure config.json loads and contains known keys."""
    cfg = load_config()
    assert isinstance(cfg, dict)
    assert "de-en" in cfg, "Expected 'de-en' key in config"
    assert all(isinstance(v, str) for v in cfg.values())
    
def test_get_translator_returns_pipeline():
    """Ensure that get_translator returns a callable pipeline."""
    model_name = SUPPORTED_MODELS["de-en"]
    translator = get_translator(model_name)
    result = cast(List[Dict[str, Any]], translator("Hallo Welt", max_length=30))
    assert isinstance(result, list)
    assert "translation_text" in result[0]

def test_config_file_exists():
    """Ensure config.json file exists and is valid JSON."""
    path = Path(__file__).parent.parent / "config.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "supported" in data
    assert isinstance(data["supported"], dict)  

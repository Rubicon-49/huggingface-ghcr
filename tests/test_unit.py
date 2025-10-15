"""
Unit tests for the translation app.
These tests don't start the FastAPI server - they test internal logic.
"""

import json
from pathlib import Path
from src.services.config_loader import load_config, SUPPORTED_MODELS
from src.services.translator import get_translator
from typing import Any, List, Dict, cast

def test_config_loads_correctly():
    """Ensure config.json loads and contains known keys."""
    cfg = load_config()
    assert isinstance(cfg, dict)
    assert "supported_models" in cfg, "Expected 'supported_models' key at top level"
    assert "helsinki" in cfg["supported_models"], (
        f"Expected 'helsinki' under supported_models, found {list(cfg['supported_models'].keys())}"
    )
    assert all(isinstance(v, dict) for v in cfg.values())
    
def test_get_translator_returns_pipeline():
    """Ensure that get_translator returns a callable pipeline."""
    model_info = SUPPORTED_MODELS["helsinki"]
    model_type = model_info["type"]
    model_name = model_info["pairs"].get("de-en")
    translator = get_translator(model_name, model_type)
    result = cast(List[Dict[str, Any]], translator("Hallo Welt", max_length=30))
    assert isinstance(result, list)
    assert "translation_text" in result[0]

def test_config_file_exists():
    """Ensure config.json file exists and is valid JSON."""
    path = Path(__file__).parent.parent / "config.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "supported_models" in data
    assert isinstance(data["supported_models"], dict)  

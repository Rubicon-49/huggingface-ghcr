"""
Integration tests that spin up the FastAPI app and hit real endpoints.
"""
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_homepage_serves_html():
    """GET / should return HTML content."""
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()
    assert "translator" in response.text.lower()

def test_api_translation_de_en():
    """POST /api/translate should return translation JSON."""
    body = {"text": "Guten Morgen", "source_lang": "de", "target_lang": "en"}
    response = client.post("/api/translate", json=body)
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    assert isinstance(data["translated_text"], str)
    assert len(data["translated_text"]) > 0
    
def test_invalid_language_pair():
    """Should handle unsupported language pairs gracefully."""
    body = {"text": "Bonjour", "source_lang": "fr", "target_lang": "jp"} # not supported in config
    response = client.post("/api/translate", json=body)
    assert response.status_code == 400
    assert "Unsupported" in response.text
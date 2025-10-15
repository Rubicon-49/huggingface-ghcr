"""
A lightweight FastAPI-based multi-lingual translation web app.

Features:
- Use models available from Hugging Face and Ollama for translation.
- Loads supported language pairs dynamically from a JSON config file.
- Serves as a simple static HTML page for user interaction.
- Provides an API endpoint for programmatic translation.

Usage:
    uvicorn app:app --reload
Then visit: http://127.0.0.1:8000
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from logging_config import setup_logging
from routes.translate import router as translate_router

setup_logging()

app = FastAPI(title="Multi-lingual Translation App")

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent / "static"),
    name="static",
)
app.include_router(translate_router)

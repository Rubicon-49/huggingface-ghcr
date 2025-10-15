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

from fastapi import FastAPI
from logging_config import setup_logging
from routes.translate import router as translate_router

setup_logging()

app = FastAPI(title="Multi-lingual Translation App")
app.include_router(translate_router)
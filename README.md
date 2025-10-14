## 🧠 HuggingFace-GHCR — Multilingual Translation Web App

A lightweight FastAPI-based translation web app using Hugging Face MarianMT models.
Translate between multiple languages (German, English, French, Spanish, etc.) directly in your browser, powered by open-source NLP models.
els.

### 💡 About this project

This little project began as a personal experiment — partly curiosity, partly a learning challenge — inspired by the Coursera course **“MLOps: Machine Learning Operations”** by *Alfredo Deza* and *Noah Gift*.

After finishing the course, I wanted to see if I could build something on my own: a small, working application that blends modern MLOps ideas with practical NLP. 
With the help of **Real Python** tutorials and the outstanding open translation models from the **Helsinki Language Technology Research Group (Helsinki-NLP)**, this idea slowly took shape.

The real motivation, though, was much closer to home. I wanted to give my children a simple, distraction-free tool to translate everyday words and phrases into the languages they use most — something fast, private, and free from ads or tracking. 
Something that feels like *ours.*

What started as a follow-up exercise turned into a hands-on exploration of open-source machine translation — and a small, meaningful way to bring technology and language a little closer together.

### 🚀 Features
- 🌍 Multilingual translation with Hugging Face’s Helsinki-NLP MarianMT models
- ⚙️ FastAPI backend with REST API endpoints
- 💻 Simple web interface served via index.html
- 🧠 Config-driven design — easily extend language pairs via config.json
- 🧩 Pythonic architecture using the modern pyproject.toml and Makefile workflow
- 🧪 Automated testing with pytest and pytest-asyncio

### 🗂️ Project structure
<pre>
.
├── config.json # Model/language configuration
├── index.html # Web front-end
├── Makefile # Build, install, and test automation
├── pyproject.toml # Project metadata & dependencies
├── requirements.txt # Auto-generated pinned dependencies
├── src/
│ └── app.py # FastAPI application
└── tests/
├── test_unit.py
└── test_integration.py</pre>

### 🧰 Requirements
- ***Python 3.10 – 3.12*** (recommended 3.11)
- Linux / macOS environment
- make, pip, and venv available in PATH
(optional: pyenv for version management)

### ⚙️ Installation
Clone the repository and build everything with one command:

`make install`

This will:

1. Check your Python version
2. Create a virtual environment (hf_translator/)
3. Install pip-tools
4. Compile requirements.txt automatically from pyproject.toml
5. Install dependencies
6. Register your package in editable mode (pip install -e .)

If it’s your first run, the dependency compilation step (pip-compile) may take a few minutes — it’s resolving all transitive dependencies for deterministic builds.
### 💻 Running the app
Start the FastAPI server locally:

`make run`

or manually

`hf_translator/bin/uvicorn src.app:app --reload`

The open your browser at:

👉 http://127.0.0.1:8000

You’ll see the web interface with two text boxes — enter text in one language, choose target language, and view the translation instantly.

### 🧪 Testing

Run all tests with:

`make test`

This executes both unit and integration tests located in the `tests/` folder.

You can also run pytest directly:

`hf_translator/bin/pytest -vv`

Warnings from third-party libraries (e.g. SWIG, PyTorch, SentencePiece) are filtered automatically via `pyproject.toml`.

### 🧩 Configuration

The app reads from config.json, which defines supported language pairs and their corresponding Hugging Face models:
<pre>
{
  "supported": {
    "de-en": "Helsinki-NLP/opus-mt-de-en",
    "en-de": "Helsinki-NLP/opus-mt-en-de",
    "fr-de": "Helsinki-NLP/opus-mt-fr-de",
    "de-fr": "Helsinki-NLP/opus-mt-de-fr",
    "en-fr": "Helsinki-NLP/opus-mt-en-fr",
    "fr-en": "Helsinki-NLP/opus-mt-fr-en",
    "de-es": "Helsinki-NLP/opus-mt-de-es",
    "es-de": "Helsinki-NLP/opus-mt-es-de"
  }
}
</pre>
To extend it, simply add new pairs and model names — no code change required.

### 🧠 Development workflow
#### Update dependencies
When you change pyproject.toml, regenerate pinned dependencies:

`make compile-deps`

#### Clean build artifacts
`make clean`

#### Full reset
`make clean-all`

### 🧪 API endpoints
| Method | Endpoint   | Description                                                                          
| ------ | ---------------- | ------------------------------------------ |
| `GET`  | `/`              | Serve web interface                                                                         |
| `POST` | `/api/translate` | Translate JSON payload `{ "text": "Hallo Welt", "source_lang": "de", "target_lang": "en" }` |

Example `curl` request:
<pre>curl -X POST http://127.0.0.1:8000/api/translate \
     -H "Content-Type: application/json" \
     -d '{"text": "Hallo Welt", "source_lang": "de", "target_lang": "en"}'
</pre>
Response:
<pre>{"translated_text": "Hello world"}</pre>

### 🧠 Notes on dependencies

- `sentencepiece` → Required by MarianMT for subword tokenization
- `sacremoses` → Optional but recommended for language-specific preprocessing
- `torch` → Backend for Transformer inference
- `fastapi` + `uvicorn` → Web serving layer

All dependencies are declared in `pyproject.toml` and locked automatically by `pip-tools`.
### 🧩 Makefile overview
| Target	| Description      | 
| --------- | ---------------- |
| `make install` |	Setup venv, compile deps, install package
| `make compile-deps`	 |Regenerate `requirements.txt` from `pyproject.toml`
| `make test`	 |Run full test suite
| `make run`	 |Start FastAPI server
| `make clean`	 |Remove build/test caches
| `make clean-all`	 |Remove venv and lockfiles
| `make check-python`	 |Verify Python version compatibility

### 🧠 Tips

- Only recompile dependencies when you change `pyproject.toml? — it’s a heavy operation.
- To add new models or languages, just update config.json.

### 📄 License
MIT License © 2025 Martin Diergardt

### 🙌 Acknowledgements
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) — developers of the [OPUS-MT](https://opus.nlpl.eu/opus-mt/) models, built on the **MarianMT encoder–decoder Transformer architecture** and trained on the large open **OPUS** multilingual corpus. Their work provides high-quality, open translation models covering hundreds of language pairs.  
  (Tiedemann & Thottingal, *OPUS-MT — Building Open Translation Services for the World*, EAMT 2020) [https://huggingface.co/Helsinki-NLP](https://huggingface.co/Helsinki-NLP)
- [Real Python](https://realpython.com/) — for clear guidance on modern Python project structure and packaging.
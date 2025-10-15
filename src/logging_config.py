# src/logging_config.py
import logging
import sys

def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure global logging for the entire application.

    - Formats logs with timestamps, log level, and module name.
    - Sends logs to stdout (for Uvicorn/FastAPI compatibility).
    - Should be called once at startup.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    
    # Optional: lower verbosity of noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("transformers").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.INFO)   
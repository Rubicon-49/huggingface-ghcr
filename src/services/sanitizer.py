import logging
from typing import Any, Dict

# -------------------------------------------------------------------
# Logging setup
# -------------------------------------------------------------------
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Function definition
# -------------------------------------------------------------------

def sanitize_generation_params(
        model_type:str, 
        params: Dict[str, Any],
        whitelist: dict[str, list[str]]
    ) -> dict[str, Any]:
    """
    Keep only generation parameters explicitly allowed for a given model type.

    - Removes invalid or unsupported keys to avoid runtime warnings or errors.
    - Logs dropped parameters for visibility.
    - If no whitelist exists for a model type, all params are passed through.
    
    Args:
        model_type: model type name (e.g., "marianmt", "t5", "ollama").
        params: Dict of generation parameters from config.json.
        whitelist: A dict mapping of model types to allowed parameter keys.
    
    Returns:
        Filtered dict with only allowed generation parameters.
    """
    allowed = set(whitelist.get(model_type, []))
    
    if not allowed:
        logging.warning(
            f"No parameter found for '{model_type}') in whitelist, passing all params."
        )
        return params
    
    unknown = set(params.keys()) - allowed
    if unknown:
        logging.warning(
            f"Warning: Ignoring unsupported generation params for model type '{model_type}': {unknown}"
        )
    
    return {k: v for k, v in params.items() if k in allowed}
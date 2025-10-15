"""
Pydantic data models (schemas) for API requests and responses.
"""

from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    """
    Request body schema for /api/translate endpoint.
    """

    text: str = Field(..., description="The text to be translated")
    source_lang: str = Field(..., description="Source language code (e.g. 'de')")
    target_lang: str = Field(..., description="Target language code (e.g. 'en')")
    model_key: str = Field(..., description="Key of the translation model to use")


class TranslateResponse(BaseModel):
    """
    Response schema for /api/translate endpoint.
    """

    translated_text: str = Field(..., description="The translated text output.")


class ErrorResponse(BaseModel):
    """
    Standardized error response schema.
    """

    error: str = Field(..., description="Error message describing the issue.")

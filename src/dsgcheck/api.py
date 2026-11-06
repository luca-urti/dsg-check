"""Woche 2: HTTP-API mit FastAPI (vergleichbar mit einem Spring @RestController).

Lokal starten:
    uv run uvicorn --factory dsgcheck.api:create_app --reload
Danach: http://127.0.0.1:8000/docs (OpenAPI wird automatisch erzeugt).

    uv run pytest tests/test_w02_api.py
"""

from __future__ import annotations

from fastapi import FastAPI

from dsgcheck import __version__
from dsgcheck.summarize import LLMClient
from dsgcheck.textstats import Tokenizer


def create_app(client: LLMClient | None = None, tokenizer: Tokenizer | None = None) -> FastAPI:
    """App-Factory: Abhängigkeiten kommen als Parameter rein, Tests übergeben Fakes.

    `tokenizer=None` heisst: den echten aus dsgcheck.cli.get_tokenizer() verwenden.
    `client=None` heisst: noch kein LLM konfiguriert (das kommt in Woche 3).
    """
    app = FastAPI(title="DSG-Check", version=__version__)

    @app.get("/health")
    def health() -> dict[str, str]:
        """Fertiges Beispiel-Endpoint."""
        return {"status": "ok", "version": __version__}

    # TODO Woche 2: POST /v1/stats
    #   Request (Pydantic-Modell): text (mind. 1 Zeichen), language ("de" | "fr" | "it" | "en")
    #   Response: language, chars, words, sentences, tokens, tokens_per_word
    #   Ungültige Eingaben beantwortet FastAPI selbst mit 422, wenn dein Modell stimmt.
    #   Tipp: typing.Literal und pydantic.Field(min_length=1)
    #
    # TODO Woche 2: POST /v1/summarize
    #   Request: text. Response: Summary aus dsgcheck.summarize.
    #   Kein client konfiguriert -> 503. TextTooLongError -> 413. Leerer Text -> 422.
    #   Tipp: fastapi.HTTPException(status_code=..., detail=...)

    return app

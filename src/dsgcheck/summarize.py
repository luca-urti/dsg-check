"""Woche 2: Zusammenfassung über ein austauschbares LLM.

Der Summarizer kennt kein konkretes LLM, nur das Protocol `LLMClient`.
Das ist Dependency Injection ohne Framework: In Tests steckt ein Fake dahinter,
in Woche 3 dein echter Anthropic- oder OpenAI-Client.

    uv run pytest tests/test_w02_summarize.py
"""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel

SYSTEM_PROMPT = (
    "Du fasst Datenschutzerklärungen in höchstens drei Sätzen auf Deutsch zusammen. "
    "Nenne Verantwortlichen, Zwecke und Empfänger. Erfinde nichts."
)


class LLMClient(Protocol):
    """Minimales Interface für ein Sprachmodell."""

    def complete(self, system: str, user: str) -> str: ...


class TextTooLongError(Exception):
    """Der Text ist länger als erlaubt.

    TODO Woche 2: Speichere `length` und `max_chars` als Attribute und gib eine
    verständliche Meldung an super().__init__ weiter, z. B.
    "Text ist zu lang: 25000 Zeichen, erlaubt sind 20000".
    """

    def __init__(self, length: int, max_chars: int) -> None:
        raise NotImplementedError("Woche 2: TextTooLongError")


class Summary(BaseModel):
    """Antwort des Summarizers (Pydantic ~ DTO mit Bean Validation)."""

    summary: str
    chars_in: int


class Summarizer:
    def __init__(self, client: LLMClient, max_chars: int = 20_000) -> None:
        self.client = client
        self.max_chars = max_chars

    def summarize(self, text: str) -> Summary:
        """TODO Woche 2, in dieser Reihenfolge:

        1. Leerraum am Anfang und Ende entfernen.
        2. Leerer Text -> ValueError.
        3. Länger als max_chars -> TextTooLongError.
        4. self.client.complete(SYSTEM_PROMPT, <getrimmter Text>) aufrufen.
        5. Antwort trimmen und als Summary zurückgeben.
           chars_in ist die Länge des getrimmten Textes.
        """
        raise NotImplementedError("Woche 2: summarize")

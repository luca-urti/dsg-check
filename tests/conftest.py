"""Gemeinsame Test-Helfer (pytest-Fixtures ~ JUnit @BeforeEach mit Dependency Injection)."""

from __future__ import annotations

import math

import pytest


class FakeTokenizer:
    """Ein Token pro angefangene 6 Zeichen eines Wortes. Deterministisch und ohne Internet."""

    def encode(self, text: str) -> list[int]:
        ids: list[int] = []
        for word in text.split():
            ids.extend(range(math.ceil(len(word) / 6)))
        return ids


class FakeLLM:
    """Gibt immer `reply` zurück und merkt sich alle Aufrufe (wie ein Mockito-Spy)."""

    def __init__(self) -> None:
        self.reply = "Zusammenfassung."
        self.calls: list[tuple[str, str]] = []

    def complete(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        return self.reply


@pytest.fixture
def tokenizer() -> FakeTokenizer:
    return FakeTokenizer()


@pytest.fixture
def fake_llm() -> FakeLLM:
    return FakeLLM()

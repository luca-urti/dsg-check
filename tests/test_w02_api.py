"""Woche 2: HTTP-API. uv run pytest tests/test_w02_api.py"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from dsgcheck import __version__
from dsgcheck.api import create_app


@pytest.fixture
def client(fake_llm, tokenizer) -> TestClient:
    return TestClient(create_app(client=fake_llm, tokenizer=tokenizer))


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__}


def test_stats(client: TestClient) -> None:
    payload = {"text": "Hallo Welt. Zweiter Satz!", "language": "de"}
    response = client.post("/v1/stats", json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "language": "de",
        "chars": 25,
        "words": 4,
        "sentences": 2,
        "tokens": 5,
        "tokens_per_word": 1.25,
    }


@pytest.mark.parametrize(
    "payload",
    [{"text": "Hallo", "language": "es"}, {"text": "", "language": "de"}, {"language": "de"}],
)
def test_stats_validation(client: TestClient, payload: dict) -> None:
    assert client.post("/v1/stats", json=payload).status_code == 422


def test_summarize(client: TestClient, fake_llm) -> None:
    fake_llm.reply = "Kurz."
    response = client.post("/v1/summarize", json={"text": "  Langer Text  "})
    assert response.status_code == 200
    assert response.json() == {"summary": "Kurz.", "chars_in": 11}


def test_summarize_too_long(client: TestClient) -> None:
    response = client.post("/v1/summarize", json={"text": "x" * 20_001})
    assert response.status_code == 413


def test_summarize_empty(client: TestClient) -> None:
    assert client.post("/v1/summarize", json={"text": ""}).status_code == 422


def test_summarize_without_llm_returns_503(tokenizer) -> None:
    client = TestClient(create_app(client=None, tokenizer=tokenizer))
    assert client.post("/v1/summarize", json={"text": "Hallo"}).status_code == 503


def test_openapi_lists_all_endpoints(client: TestClient) -> None:
    paths = set(client.get("/openapi.json").json()["paths"])
    assert {"/health", "/v1/stats", "/v1/summarize"} <= paths

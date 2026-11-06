"""Woche 1: Textstatistik. Starte hier: uv run pytest tests/test_w01_textstats.py -x"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from dsgcheck.textstats import (
    LANGUAGES,
    TextStats,
    analyze,
    count_sentences,
    count_tokens,
    count_words,
    estimate_cost_chf,
    language_from_path,
    overhead_vs,
    rank_by_tokens,
)

SAMPLES = Path(__file__).parent.parent / "samples"


# --- language_from_path -------------------------------------------------------

@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("muster_ag_de.txt", "de"),
        ("muster_ag_fr.txt", "fr"),
        ("policy_it.md", "it"),
        ("a_b_en.txt", "en"),
    ],
)
def test_language_from_path(name: str, expected: str) -> None:
    assert language_from_path(Path("samples") / name) == expected


@pytest.mark.parametrize("name", ["muster_ag.txt", "muster_ag_es.txt", "muster_ag_deutsch.txt"])
def test_language_from_path_rejects_unknown(name: str) -> None:
    with pytest.raises(ValueError, match="Unbekannte Sprache"):
        language_from_path(Path(name))


# --- count_words --------------------------------------------------------------

@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("Hallo Welt", 2),
        ("Die Muster AG, Zürich.", 4),
        ("l'été arrive", 3),
        ("CHE-123.456.788", 4),
        ("Strasse  und\nGrüsse", 3),
    ],
)
def test_count_words(text: str, expected: int) -> None:
    assert count_words(text) == expected


# --- count_sentences ----------------------------------------------------------

@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("   ", 0),
        ("Hallo Welt.", 1),
        ("Wer? Wir! Ja.", 3),
        ("Ohne Punkt am Ende", 1),
        ("Zwei Sätze. Und einer ohne Punkt", 2),
        ("Version 1.5 ist neu.", 1),
        ("Was?!", 1),
    ],
)
def test_count_sentences(text: str, expected: int) -> None:
    assert count_sentences(text) == expected


# --- count_tokens und Kosten ----------------------------------------------------

def test_count_tokens_uses_the_given_tokenizer(tokenizer) -> None:
    # Fake: Datenschutzerklärung = 4, der = 1, Muster = 1, AG. = 1
    assert count_tokens("Datenschutzerklärung der Muster AG.", tokenizer) == 7


@pytest.mark.parametrize(
    ("tokens", "price", "expected"),
    [(1_500, 3.0, 0.0045), (0, 3.0, 0.0), (1_000_000, 0.25, 0.25), (1, 3.0, 0.000003)],
)
def test_estimate_cost_chf(tokens: int, price: float, expected: float) -> None:
    assert estimate_cost_chf(tokens, price) == pytest.approx(expected)


@pytest.mark.parametrize(("tokens", "price"), [(-1, 3.0), (10, -0.5)])
def test_estimate_cost_rejects_negative(tokens: int, price: float) -> None:
    with pytest.raises(ValueError):
        estimate_cost_chf(tokens, price)


# --- TextStats ------------------------------------------------------------------

def test_tokens_per_word() -> None:
    assert TextStats("de", chars=10, words=4, sentences=1, tokens=6).tokens_per_word == 1.5
    assert TextStats("en", chars=10, words=3, sentences=1, tokens=7).tokens_per_word == 2.33


def test_tokens_per_word_without_words() -> None:
    assert TextStats("de", 0, 0, 0, 0).tokens_per_word == 0.0


def test_textstats_is_immutable() -> None:
    stats = TextStats("de", 1, 1, 1, 1)
    with pytest.raises(dataclasses.FrozenInstanceError):
        stats.tokens = 2  # type: ignore[misc]


def test_analyze(tokenizer) -> None:
    stats = analyze("Hallo Welt. Zweiter Satz!", "de", tokenizer)
    assert stats == TextStats(language="de", chars=25, words=4, sentences=2, tokens=5)


# --- Vergleich der Sprachen ----------------------------------------------------

def _s(lang: str, tokens: int) -> TextStats:
    return TextStats(lang, chars=0, words=1, sentences=1, tokens=tokens)


def test_rank_by_tokens_sorts_and_breaks_ties_by_language() -> None:
    stats = [_s("de", 120), _s("en", 100), _s("fr", 130), _s("it", 100)]
    original = list(stats)
    ranked = rank_by_tokens(stats)
    assert [s.language for s in ranked] == ["en", "it", "de", "fr"]
    assert stats == original, "Die Eingabeliste darf nicht verändert werden"


def test_overhead_vs_english() -> None:
    stats = [_s("en", 100), _s("de", 125), _s("fr", 133)]
    assert overhead_vs(stats) == {"en": 0.0, "de": 25.0, "fr": 33.0}


def test_overhead_vs_other_base_and_rounding() -> None:
    stats = [_s("en", 6), _s("de", 7)]
    assert overhead_vs(stats, base="de") == {"en": -14.3, "de": 0.0}


def test_overhead_vs_requires_base() -> None:
    with pytest.raises(ValueError):
        overhead_vs([_s("de", 10)], base="en")


# --- Die echten Beispieltexte ---------------------------------------------------

def test_samples_exist_in_all_languages(tokenizer) -> None:
    files = sorted(SAMPLES.glob("muster_ag_*.txt"))
    langs = {language_from_path(f) for f in files}
    assert langs == set(LANGUAGES)
    for f in files:
        stats = analyze(f.read_text(encoding="utf-8"), language_from_path(f), tokenizer)
        assert stats.words > 50
        assert stats.sentences >= 5

"""Woche 2: Summarizer mit Fake-LLM. uv run pytest tests/test_w02_summarize.py"""

from __future__ import annotations

import pytest

from dsgcheck.summarize import SYSTEM_PROMPT, Summarizer, Summary, TextTooLongError


def test_returns_trimmed_summary(fake_llm) -> None:
    fake_llm.reply = "  Die Muster AG bearbeitet Kundendaten.  \n"
    result = Summarizer(fake_llm).summarize("  Ein Text.  ")
    assert result == Summary(summary="Die Muster AG bearbeitet Kundendaten.", chars_in=9)


def test_sends_system_prompt_and_trimmed_text(fake_llm) -> None:
    Summarizer(fake_llm).summarize("\n Text \n")
    assert fake_llm.calls == [(SYSTEM_PROMPT, "Text")]


@pytest.mark.parametrize("text", ["", "   ", "\n\t"])
def test_empty_text_raises_without_calling_llm(fake_llm, text: str) -> None:
    with pytest.raises(ValueError):
        Summarizer(fake_llm).summarize(text)
    assert fake_llm.calls == []


def test_too_long_raises_with_details(fake_llm) -> None:
    with pytest.raises(TextTooLongError) as exc:
        Summarizer(fake_llm, max_chars=10).summarize("x" * 11)
    assert exc.value.length == 11
    assert exc.value.max_chars == 10
    assert "11" in str(exc.value)
    assert "10" in str(exc.value)
    assert fake_llm.calls == []


def test_exactly_max_chars_is_allowed(fake_llm) -> None:
    Summarizer(fake_llm, max_chars=10).summarize("x" * 10)
    assert len(fake_llm.calls) == 1


def test_length_is_checked_after_trimming(fake_llm) -> None:
    Summarizer(fake_llm, max_chars=3).summarize("  abc  ")
    assert fake_llm.calls == [(SYSTEM_PROMPT, "abc")]

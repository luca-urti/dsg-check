"""Woche 1: der Befehl `dsgcheck stats`. uv run pytest tests/test_w01_cli.py"""

from __future__ import annotations

import contextlib
from pathlib import Path

import pytest
from typer.testing import CliRunner

from dsgcheck import cli

runner = CliRunner()
SAMPLES = Path(__file__).parent.parent / "samples"


@pytest.fixture(autouse=True)
def _offline_tokenizer(monkeypatch, tokenizer) -> None:
    """Ersetzt den echten tiktoken-Tokenizer durch den Fake aus conftest.py."""
    monkeypatch.setattr(cli, "get_tokenizer", lambda: tokenizer)


def _write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def _output(result) -> str:
    """stdout und stderr zusammen, unabhängig von der Click-Version."""
    out = result.output
    with contextlib.suppress(ValueError):
        out += result.stderr
    return out


def test_version_command_works() -> None:
    result = runner.invoke(cli.app, ["version"])
    assert result.exit_code == 0
    assert "dsg-check" in result.output


def test_stats_prints_one_line_per_language(tmp_path: Path) -> None:
    de = _write(tmp_path, "x_de.txt", "Datenschutzerklärung der Muster AG.")
    en = _write(tmp_path, "x_en.txt", "Privacy notice of Muster AG.")
    result = runner.invoke(cli.app, ["stats", str(de), str(en)])
    out = _output(result)
    assert result.exit_code == 0, out
    assert "Tokens" in out
    assert "CHF" in out
    first_words = [line.split()[0] for line in out.splitlines() if line.strip()]
    assert "de" in first_words
    assert "en" in first_words


def test_stats_names_cheapest_language_and_overhead(tmp_path: Path) -> None:
    # Fake-Tokens: de = 7, en = 6, also braucht de 16.7 % mehr
    de = _write(tmp_path, "x_de.txt", "Datenschutzerklärung der Muster AG.")
    en = _write(tmp_path, "x_en.txt", "Privacy notice of Muster AG.")
    result = runner.invoke(cli.app, ["stats", str(de), str(en)])
    out = _output(result)
    assert "Günstigste Sprache: en" in out
    assert "16.7" in out


def test_stats_rejects_unknown_language(tmp_path: Path) -> None:
    es = _write(tmp_path, "x_es.txt", "Declaración de privacidad.")
    result = runner.invoke(cli.app, ["stats", str(es)])
    assert result.exit_code == 1
    assert "Unbekannte Sprache" in _output(result)


def test_stats_on_all_samples() -> None:
    files = [str(p) for p in sorted(SAMPLES.glob("muster_ag_*.txt"))]
    result = runner.invoke(cli.app, ["stats", *files])
    out = _output(result)
    assert result.exit_code == 0, out
    first_words = {line.split()[0] for line in out.splitlines() if line.strip()}
    assert {"de", "fr", "it", "en"} <= first_words

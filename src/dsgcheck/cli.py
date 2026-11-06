"""Kommandozeile von DSG-Check (Typer, vergleichbar mit picocli in Java).

Aufruf nach `uv sync`:
    uv run dsgcheck stats samples/*.txt
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from dsgcheck.textstats import Tokenizer

app = typer.Typer(help="DSG-Check: Datenschutzerklärungen mit KI prüfen.", no_args_is_help=True)


def get_tokenizer() -> Tokenizer:
    """Echter Tokenizer. Tests ersetzen diese Funktion per monkeypatch durch einen Fake.

    tiktoken lädt das Encoding beim ersten Aufruf aus dem Internet und zählt
    Tokens nach OpenAI-Art. Claude zählt anders; das misst du in Woche 3 über die API.
    """
    import tiktoken

    return tiktoken.get_encoding("o200k_base")


@app.command()
def stats(
    files: Annotated[
        list[Path], typer.Argument(exists=True, readable=True, help="Dateien wie muster_ag_de.txt")
    ],
    price: Annotated[float, typer.Option(help="CHF pro Million Input-Tokens")] = 3.0,
    base: Annotated[str, typer.Option(help="Sprache, mit der verglichen wird")] = "en",
) -> None:
    """Zeigt Zeichen, Wörter, Sätze, Tokens und Kosten pro Sprache.

    TODO Woche 1, die Tests in tests/test_w01_cli.py beschreiben das Ergebnis:
      1. Für jede Datei Sprache bestimmen und den Text lesen (Path.read_text, UTF-8).
         Unbekannte Sprache: Meldung ausgeben und mit typer.Exit(code=1) abbrechen.
      2. Mit get_tokenizer() und analyze() die Kennzahlen berechnen.
      3. Pro Sprache eine Zeile mit Sprache, Wörtern, Tokens, Tokens/Wort und CHF ausgeben,
         sortiert mit rank_by_tokens(). Die Kopfzeile enthält das Wort "Tokens".
      4. Zum Schluss: "Günstigste Sprache: <code>" und, falls die Basissprache dabei ist,
         pro Sprache den Mehraufwand aus overhead_vs().
    """
    raise NotImplementedError("Woche 1: stats-Befehl")


@app.command()
def version() -> None:
    """Zeigt die Version (fertiges Beispiel für einen Befehl)."""
    from dsgcheck import __version__

    typer.echo(f"dsg-check {__version__}")


if __name__ == "__main__":
    app()

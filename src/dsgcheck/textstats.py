"""Woche 1: Textstatistik und Token-Zählung.

Ziel der Woche: verstehen, warum dieselbe Datenschutzerklärung je nach Sprache
unterschiedlich viele Tokens kostet, und dabei die Python-Grundlagen lernen.

So arbeitest du:
    uv run pytest tests/test_w01_textstats.py
Die Tests beschreiben, was jede Funktion tun muss. Ersetze jedes
`raise NotImplementedError` durch deinen eigenen Code, bis alles grün ist.

Für Java-/TS-Entwickler:
    - Protocol      ~ Interface (strukturell wie in TypeScript: kein `implements` nötig)
    - @dataclass    ~ record bzw. Lombok @Value
    - X | None      ~ Optional<X>
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

LANGUAGES: tuple[str, ...] = ("de", "fr", "it", "en")


class Tokenizer(Protocol):
    """Alles, was eine Methode `encode(text) -> list[int]` hat, ist ein Tokenizer.

    Die Encodings von tiktoken erfüllen das automatisch. In den Tests steckt
    ein einfacher Fake dahinter, damit sie ohne Internet laufen.
    """

    def encode(self, text: str) -> list[int]: ...


@dataclass(frozen=True)
class TextStats:
    """Kennzahlen eines Textes. `frozen=True` macht die Instanz unveränderlich."""

    language: str
    chars: int
    words: int
    sentences: int
    tokens: int

    @property
    def tokens_per_word(self) -> float:
        """Tokens pro Wort, auf 2 Nachkommastellen gerundet. 0.0, wenn es keine Wörter gibt."""
        raise NotImplementedError("Woche 1: tokens_per_word")


def language_from_path(path: Path) -> str:
    """Liest den Sprachcode aus dem Dateinamen: 'muster_ag_de.txt' -> 'de'.

    Der Code steht nach dem letzten Unterstrich vor der Endung.
    Erlaubt sind nur die Codes in LANGUAGES. Alles andere -> ValueError,
    deren Meldung mit 'Unbekannte Sprache' beginnt.

    Tipp: path.stem, str.rsplit oder ein regulärer Ausdruck.
    """
    raise NotImplementedError("Woche 1: language_from_path")


def count_words(text: str) -> int:
    """Zählt Wörter: Folgen von Buchstaben oder Ziffern, auch mit ä, é oder ß.

    Satzzeichen zählen nicht. "l'été" ergibt zwei Wörter, "CHE-123.456.788" vier.
    Tipp: re.findall mit dem Muster \\w+
    """
    raise NotImplementedError("Woche 1: count_words")


def count_sentences(text: str) -> int:
    """Zählt Sätze.

    Ein Satz endet mit . ! oder ?, gefolgt von Leerraum oder dem Textende.
    Ein letzter Abschnitt ohne Satzzeichen zählt mit, wenn er Wörter enthält.
    Leerer Text hat 0 Sätze. "Version 1.5 ist neu." ist ein Satz.

    Bekannte Grenze, die du nicht lösen musst: Abkürzungen wie "Art. 19".
    """
    raise NotImplementedError("Woche 1: count_sentences")


def count_tokens(text: str, tokenizer: Tokenizer) -> int:
    """Anzahl Tokens laut übergebenem Tokenizer."""
    raise NotImplementedError("Woche 1: count_tokens")


def estimate_cost_chf(tokens: int, chf_per_million: float) -> float:
    """Kosten in CHF für `tokens` Input-Tokens, auf 6 Nachkommastellen gerundet.

    Negative Werte für tokens oder Preis -> ValueError.
    """
    raise NotImplementedError("Woche 1: estimate_cost_chf")


def analyze(text: str, language: str, tokenizer: Tokenizer) -> TextStats:
    """Baut ein TextStats-Objekt. `chars` ist die Länge des ganzen Textes inklusive Leerraum."""
    raise NotImplementedError("Woche 1: analyze")


def rank_by_tokens(stats: list[TextStats]) -> list[TextStats]:
    """Neue Liste, aufsteigend nach Tokens sortiert; bei Gleichstand alphabetisch nach Sprache.

    Die übergebene Liste darf nicht verändert werden.
    """
    raise NotImplementedError("Woche 1: rank_by_tokens")


def overhead_vs(stats: list[TextStats], base: str = "en") -> dict[str, float]:
    """Wie viel Prozent mehr Tokens jede Sprache braucht als die Basissprache.

    Beispiel: en 100 Tokens, de 125 Tokens -> {"en": 0.0, "de": 25.0}.
    Auf eine Nachkommastelle gerundet. Fehlt die Basissprache -> ValueError.
    Tipp: Dict Comprehension.
    """
    raise NotImplementedError("Woche 1: overhead_vs")

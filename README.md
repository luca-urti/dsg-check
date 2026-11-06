# DSG-Check

DSG-Check liest eine Datenschutzerklärung, extrahiert die wichtigsten Angaben und prüft sie mit einem KI-Agenten gegen das Schweizer Datenschutzgesetz (DSG). Jede Aussage im Prüfbericht ist mit einem Gesetzesartikel belegt.

Das Repo ist dein durchgehendes Projekt im AI Engineer Bootcamp. Es wächst über 16 Wochen in drei Releases:

| Release | Wochen | Was es kann |
|---|---|---|
| v0.1 Extraktor | 1–5 | Datenschutzerklärung (PDF, HTML, Text) → strukturierte Angaben, mit Evals |
| v0.2 Gesetzes-RAG | 6–8 | Fragen zu DSG und DSV in DE, FR, IT beantworten, mit Artikelzitat |
| v1.0 Prüf-Agent | 9–14 | Agent prüft eine Erklärung gegen DSG Art. 19, fragt bei Unklarheit nach, erstellt den Bericht; MCP-Server, Tracing, Evals in CI |

Den vollständigen Wochenplan findest du im Bootcamp-Dokument im Tab «DSG-Check».

## Setup

Du brauchst [uv](https://docs.astral.sh/uv/) (ersetzt pip, venv und pyenv, etwa wie Maven Wrapper plus SDKMAN).

```bash
git init && git add . && git commit -m "Start DSG-Check"   # danach öffentliches GitHub-Repo verbinden
uv sync                 # legt .venv an und installiert alles aus pyproject.toml
uv run pytest           # alle Tests (am Anfang sind fast alle rot, das ist der Plan)
uv run ruff check .     # Linter
uv run dsgcheck version # dein CLI
```

## Arbeitsweise

1. **Tests zuerst lesen.** Jede Woche hat Tests unter `tests/test_wXX_*.py`. Sie beschreiben, was dein Code können muss.
2. **Rot → Grün → Aufräumen.** Ersetze jedes `raise NotImplementedError` durch deinen eigenen Code, bis die Tests der Woche grün sind:
   ```bash
   uv run pytest tests/test_w01_textstats.py -x   # -x stoppt beim ersten Fehler
   ```
3. **Kerncode selbst schreiben.** Claude erklärt, deutet Fehlermeldungen und reviewt deinen Code, schreibt aber nicht die Lösung.
4. **Abschliessen.** Lernlog in `LEARNING_LOG.md` nachführen, committen, Woche taggen: `git tag w01 && git push --tags`.

Die CI auf GitHub ist rot, bis die Tests der aktuellen Woche grün sind. Genau das ist das Ziel jeder Woche.

## Woche 1: Textstatistik und Tokens

Datei: `src/dsgcheck/textstats.py` und der Befehl `stats` in `src/dsgcheck/cli.py`.

```bash
uv run pytest tests/test_w01_textstats.py tests/test_w01_cli.py
uv run dsgcheck stats samples/muster_ag_*.txt
```

Du lernst: Module und Packages, Funktionen mit Type Hints, `pathlib`, reguläre Ausdrücke, Comprehensions, `@dataclass`, `Protocol`, pytest mit `parametrize` und Fixtures, ein CLI mit Typer.

Hinweis: `tiktoken` lädt beim ersten Lauf ein Encoding aus dem Internet und zählt Tokens nach OpenAI-Art. Wie Claude dieselben Texte zählt, misst du in Woche 3 über die API.

## Woche 2: API, Fakes und Docker

Dateien: `src/dsgcheck/summarize.py` und `src/dsgcheck/api.py`.

```bash
uv run pytest tests/test_w02_summarize.py tests/test_w02_api.py
uv run uvicorn --factory dsgcheck.api:create_app --reload   # dann http://127.0.0.1:8000/docs
```

Zusätzlich ohne Tests: Schreib ein `Dockerfile`, das die API startet, und prüfe, dass `docker run -p 8000:8000 dsg-check` funktioniert.

Du lernst: Klassen, eigene Exceptions, Pydantic-Modelle, FastAPI, Dependency Injection über Parameter, Fakes statt Mocks, HTTP-Statuscodes.

## Beispieldaten

`samples/` enthält eine erfundene Datenschutzerklärung der Muster AG in vier Sprachen und mit `muster_ag.facts.json` die richtigen Antworten dazu. Ab Woche 4 misst du deine Extraktion daran.

## Regeln

- Nur öffentliche oder erfundene Daten, keine echten Personendaten, nichts aus deiner Arbeit beim Arbeitgeber.
- Das Projekt ist eine Lern- und Demo-Anwendung und ersetzt keine Rechtsberatung.

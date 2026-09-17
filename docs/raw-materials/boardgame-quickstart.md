# Quickstart: Spec-Kit-Projekt mit vorbereiteten Boardgame-Specs

> Historisches Rohmaterial aus dem bisherigen Template. Diese Anleitung wird
> nicht fortgeschrieben. Maßgeblich ist das [DV-Konzept](../DV_KONZEPT.md).

## Zweck

Diese Datei beschreibt den empfohlenen Startablauf für ein neues GitHub-Repository auf Basis der vorbereiteten Markdown-Specs und GitHub Spec Kit.

Ziel ist:

1. Projektordner sauber anlegen
2. vorbereitete Dateien einsortieren
3. ersten Git-Commit erstellen
4. Spec Kit initialisieren
5. danach mit kleinen Feature-Specs weiterarbeiten

---

## Voraussetzungen

Installiert sein sollten:

- Git
- GitHub-Zugang
- `uv`
- Zugriff auf GitHub Spec Kit

Optional, aber empfohlen:

- VS Code
- GitHub Copilot oder eine andere von Spec Kit unterstützte Agent-Integration

---

## 1. Projektordner anlegen

```bash
mkdir boardgame-digital
cd boardgame-digital
git init
```

---

## 2. Ordnerstruktur vorbereiten

Lege diese Struktur an:

```txt
boardgame-digital/
├─ README.md
├─ QUICKSTART.md
├─ docs/
├─ specs/
├─ apps/
│  └─ prototype/
├─ packages/
│  └─ game-core/
└─ .github/
   ├─ ISSUE_TEMPLATE/
   └─ pull_request_template.md
```

Optional per Terminal:

```bash
mkdir -p docs
mkdir -p specs
mkdir -p apps/prototype
mkdir -p packages/game-core
mkdir -p .github/ISSUE_TEMPLATE
```

---

## 3. Vorbereitete Dateien einsortieren

Kopiere die vorbereiteten Dateien an diese Pfade:

```txt
boardgame-digital/README.md
boardgame-digital/QUICKSTART.md

boardgame-digital/docs/architecture.md
boardgame-digital/docs/decisions.md
boardgame-digital/docs/roadmap.md
boardgame-digital/docs/terminology.md
boardgame-digital/docs/references.md

boardgame-digital/specs/000-spec-index.md
boardgame-digital/specs/001-version-1-scope.md
boardgame-digital/specs/002-board-rendering-input.md
boardgame-digital/specs/003-commanders-units-king-banner.md
boardgame-digital/specs/004-movement-holding-actions.md
boardgame-digital/specs/005-combat-and-dice-resolution.md
boardgame-digital/specs/006-combat-examples.md
boardgame-digital/specs/099-later-expansions-and-open-points.md

boardgame-digital/.github/pull_request_template.md
```

Die vorbereiteten Dateien bilden die fachliche Grundlage des Projekts.

Sie sind keine Implementierung, sondern Projekt-, Architektur- und Regel-Specs.

---

## 4. Ersten Git-Commit erstellen

```bash
git add .
git commit -m "Add initial boardgame specs"
```

Dieser Commit enthält die manuell vorbereitete Spec-Grundlage.

---

## 5. Spec Kit initialisieren

Führe Spec Kit erst aus, nachdem die vorbereiteten Dateien im Repository liegen.

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init --here
```

Während der Initialisierung wählst du die Agent-/Tool-Integration, die du verwenden willst.

Beispiele:

- GitHub Copilot
- Claude Code
- Gemini CLI

Empfehlung bei GitHub-/VS-Code-Workflow:

```txt
copilot
```

---

## 6. Spec-Kit-Dateien committen

Nach der Initialisierung:

```bash
git add .
git commit -m "Initialize Spec Kit"
```

Damit bleibt die Historie sauber getrennt:

```txt
Commit 1: vorbereitete Boardgame-Specs
Commit 2: Spec-Kit-Initialisierung
```

---

## 7. GitHub-Repository verbinden

Erstelle auf GitHub ein neues Repository, zum Beispiel:

```txt
boardgame-digital
```

Dann lokal verbinden:

```bash
git branch -M main
git remote add origin <DEIN_GITHUB_REPO_URL>
git push -u origin main
```

Beispiel:

```bash
git remote add origin https://github.com/<USERNAME>/boardgame-digital.git
git push -u origin main
```

---

## 8. Nach Spec Kit nicht sofort alles implementieren

Nach der Spec-Kit-Initialisierung sollte nicht direkt das komplette Spiel implementiert werden.

Arbeite in kleinen Feature-Schnitten.

Empfohlene Reihenfolge:

```txt
1. Initial board prototype
2. GameState type definitions
3. Demo start state
4. Commander and banner rendering
5. Drag-and-drop
6. Movement validation
7. Holding / Zone of Control
8. Combat and dice resolution
9. Victory conditions
10. Debug tooling
```

---

## 9. Erste sinnvolle Spec-Kit-Feature-Spec

Die erste `/specify`-Anweisung sollte klein und klar begrenzt sein.

Empfohlener Start:

```txt
Create the initial local PixiJS board prototype for the boardgame-digital project.

It must render a 24x24 grass board with 128x128 px tiles, visible grid lines, camera panning, zoom, and a debug toggle.

Use the existing README.md, docs/, and specs/ files as source of truth.

Do not implement commanders, units, king, banner, movement validation, holding, combat, dice resolution, multiplayer, server, login, database, or ranking yet.
```

Ziel dieses ersten Schnitts:

- Projekt technisch lauffähig machen
- Board rendern
- Kamera und Zoom vorbereiten
- Debug-Grundlage schaffen
- noch keine Spielregeln implementieren

---

## 10. Danach typischer Spec-Kit-Ablauf

Nach einer `/specify`-Anweisung folgt typischerweise:

```txt
/specify   -> Feature beschreiben
/clarify   -> offene Fragen klären
/plan      -> technischen Plan erstellen
/tasks     -> umsetzbare Tasks erzeugen
```

Erst danach sollte implementiert werden.

---

## 11. Wichtige Projektregeln

Für dieses Projekt gelten besonders:

```txt
PixiJS zeigt.
game-core entscheidet.
GameState ist die Wahrheit.
Specs beschreiben.
Tests kontrollieren.
GitHub organisiert.
```

Zusätzlich:

- Version 1 ist ein lokaler Browser-Prototyp.
- Kein Server in Version 1.
- Kein Login in Version 1.
- Keine Datenbank in Version 1.
- Kein Ranking in Version 1.
- `GameState` enthält regelrelevante Wahrheit.
- `PrototypeUiState` enthält UI-Zustände.
- PixiJS rendert, entscheidet aber nicht dauerhaft über Regeln.
- `game-core` soll später regelrelevante Logik kapseln.
- Spätere Erweiterungen dürfen den Version-1-Scope nicht verdeckt erweitern.

---

## 12. Empfohlene erste Implementierungsstruktur

Nach der ersten Spec-Kit-Feature-Spec kann die technische Struktur so wachsen:

```txt
boardgame-digital/
├─ apps/
│  └─ prototype/
│     ├─ package.json
│     ├─ index.html
│     └─ src/
│        ├─ main.ts
│        ├─ app/
│        ├─ rendering/
│        ├─ input/
│        └─ state/
├─ packages/
│  └─ game-core/
│     └─ src/
│        ├─ types.ts
│        ├─ createInitialGameState.ts
│        └─ index.ts
```

Diese Struktur sollte erst entstehen, wenn Spec Kit dafür einen Plan und Tasks erzeugt hat.

---

## 13. Empfohlene erste GitHub-Issues

Falls du vorab Issues anlegen möchtest:

```txt
1. Initialize local PixiJS prototype
2. Render 24x24 grass board with visible grid
3. Add camera panning and zoom
4. Add debug toggle and debug overlay
5. Add GameState and core type definitions
6. Add deterministic demo start state
7. Render commanders, units, king marker and banners
8. Add drag-and-drop with snap-to-grid
9. Add movement validation
10. Add combat and dice resolution
```

---

## 14. Merksatz

```txt
Erst Grundlagen einsortieren.
Dann Spec Kit initialisieren.
Dann kleine Feature-Specs erzeugen.
Dann planen.
Dann Tasks erstellen.
Dann implementieren.
```

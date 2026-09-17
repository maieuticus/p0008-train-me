# Tasks: [FEATURE]

**Input**: `specs/[###-feature-name]/`
**Prerequisites**: spec.md und plan.md; weitere Artefakte nach Bedarf.

## Format: `[ID] [P?] [Story] Beschreibung`

- Konkrete Pfade und Abhängigkeiten angeben.
- [P] nur für unabhängig ausführbare Aufgaben verwenden.
- Für relevante Akzeptanzkriterien passende Tests vorsehen.

## Phase 1: Setup

- [ ] T001 [Konkrete Vorbereitung entsprechend dem Plan.]

## Phase 2: Foundational

- [ ] T002 [Gemeinsame Voraussetzungen; nur wenn benötigt.]

## Phase 3: User Story 1 (Priority: P1)

**Goal**: [Unabhängig überprüfbares Ergebnis.]
**Independent Test**: [Konkrete Abnahme.]

- [ ] T003 [US1] [Relevanten Testfall mit Dateipfad ergänzen.]
- [ ] T004 [US1] [Implementierung mit Dateipfad.]

## Phase 4: Prüfung und Abschluss

- [ ] T005 `python scripts/check.py` und zusätzliche Prüfungen aus plan.md ausführen.
- [ ] T006 Betroffene Abschnitte in `docs/DV_KONZEPT.md` aktualisieren.
- [ ] T007 Akzeptanzkriterien gegen Ergebnisse abgleichen und offene Lücken erfassen.

## Dependencies & Execution Order

[Abhängigkeiten und begründete Reihenfolge.]

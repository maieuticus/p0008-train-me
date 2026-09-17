# Feature: Wiederverwendbares Projektgrundgerüst

## Ziel

Aus einem technologieoffenen Template Projekte mit konsistenter Entwicklung,
Dokumentation und begrenztem Zugriff auf Referenz-Repositories erzeugen.

## Akzeptanzkriterien

- **FR-001:** Projektziel, Architektur, Entwicklung und Betrieb stehen pro
  Projekt in genau einem `docs/DV_KONZEPT.md`.
- **FR-002:** Neutrale, Python-, TypeScript- und Maven-Projekte sind auswählbar.
  PostgreSQL, Keycloak und Observability sind optionale Bausteine.
- **FR-003:** Das API-Rezept nutzt Python und PostgreSQL und enthält einen
  automatisiert geprüften API-Vertrag.
- **FR-004:** Die Erzeugung überschreibt keine bestehenden Dateien und übernimmt
  weder Secrets noch projektspezifische Rohmaterialien.
- **FR-005:** Referenz-Repositories werden lokal ausschließlich lesbar gemountet.
  Codespaces fordert keine pauschalen Inhalts-Schreibrechte auf fremde Repos.
- **FR-006:** Spec-Kit-Constitution, eigene Vorlagen und Workflow sind vorbereitet;
  Integrationsmanifeste werden durch die echte CLI erzeugt.
- **FR-007:** Relevante Prüfungen sind lokal und in CI ausführbar. Fehlende
  Ausführungsmöglichkeiten werden ausdrücklich benannt.

## Nicht-Ziele

Keine Sport-/Boardgame-Implementierung, kein produktives Deployment und keine
automatische Veröffentlichung von Issues, Branches oder Pull Requests.

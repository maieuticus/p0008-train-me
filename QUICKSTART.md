# Quickstart: p0008-train-me

Die verbindlichen Voraussetzungen und Schritte stehen im
[DV-Konzept – Einrichtung](docs/DV_KONZEPT.md#einrichtung).

1. Das bestehende Repository öffnen und Python ab 3.11 bereitstellen.
2. `python -m pip install -r scripts/requirements.txt` ausführen.
3. Mit `python scripts/check.py` den vorhandenen Stand prüfen.
4. [Projektziel](docs/DV_KONZEPT.md#projektziel),
   [ersten Funktionsumfang](docs/DV_KONZEPT.md#erster-funktionsumfang) und
   [offene Entscheidungen](docs/DV_KONZEPT.md#offene-entscheidungen) lesen.
5. Für das bereits spezifizierte und [geplante Backend-Grundgerüst](specs/002-backend-foundation/plan.md)
   mit `speckit-tasks` Aufgaben ableiten und anschließend auf Konsistenz prüfen.
   Neue Features beginnen mit `speckit-specify`.

Spec Kit ist bereits für Codex mit PowerShell eingerichtet. Details und
Hinweise zum optionalen Devcontainer stehen im DV-Konzept.
Der [Feature-Ablauf](docs/DV_KONZEPT.md#ablauf-je-feature) führt von der
Spezifikation über Tests bis zur Abnahme.

Ein Startbefehl für die Sport-App wird mit dem ersten lauffähigen Feature
ergänzt. Der vorhandene Generator und seine Beispielprojekte sind
übernommenes Template-Material.

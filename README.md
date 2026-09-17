# p0008-train-me

Der verbindliche Einstieg in die Sport-App ist das
[DV-Konzept](docs/DV_KONZEPT.md). Es beschreibt Projektziel, fachlichen Umfang,
Zielarchitektur, Entwicklung und Betrieb.

**Stand:** Die Projektgrundlage ist beschrieben. Das Repository enthält
bislang das übernommene Template und seine Prüfwerkzeuge; die Anwendung
wird in abgegrenzten Features aufgebaut.

## Einstieg

1. [Quickstart](QUICKSTART.md) und [aktuellen Projektstand](docs/DV_KONZEPT.md#aktueller-projektstand) lesen.
2. Den [ersten Funktionsumfang](docs/DV_KONZEPT.md#erster-funktionsumfang), seine Spezifikation und offenen Entscheidungen prüfen.
3. Ein Feature mit den vorhandenen Spec-Kit-Skills spezifizieren und planen.

## Orientierung

| Thema | Einstieg |
| --- | --- |
| Einrichtung und täglicher Start | [Quickstart](QUICKSTART.md) |
| Verbindliche Projektbeschreibung | [DV-Konzept](docs/DV_KONZEPT.md) |
| Entwicklungsmethodik | [Constitution](.specify/memory/constitution.md) |
| Feature-Spezifikationen | [Feature-Übersicht](specs/README.md) |
| Übernommene Technologiebausteine | [Bausteinkatalog](templates/README.md) |
| Arbeitsregeln für Agenten | [AGENTS.md](AGENTS.md) |
| Referenz-Repositories und Beiträge | [DV-Konzept: Wissensaustausch](docs/DV_KONZEPT.md#wissensaustausch) |

## Prüfen

```powershell
python -m pip install -r scripts/requirements.txt
python scripts/check.py
```

Dies prüft derzeit Dokumentlinks, Dateisyntax und die Template-Tests.
Anwendungstests und Startbefehle werden mit den jeweiligen Features ergänzt.
Ausgeführte und noch offene Prüfungen stehen im
[Prüfstatus](docs/DV_KONZEPT.md#prüfstatus).

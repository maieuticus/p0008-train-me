# template-spec-kit

Technologieoffenes Projektgrundgerüst für Spec-Driven Development. Ein gemeinsamer
Kern wird mit einem Technologieprofil und den benötigten Diensten kombiniert.

**Projektziel, Architektur, Entwicklung und Betrieb stehen zusammen im
[DV-Konzept](docs/DV_KONZEPT.md).**

## Einstieg

Voraussetzung für die Projekterzeugung: Python ab 3.11.

```sh
python -m pip install -r scripts/requirements.txt
python scripts/create_project.py --name mein-projekt --stack python --output ../mein-projekt
```

Ein API-Projekt einschließlich PostgreSQL:

```sh
python scripts/create_project.py --name meine-api --recipe api-service --output ../meine-api
```

Das Ziel muss leer sein oder noch nicht existieren. `--dry-run` zeigt die
vorgesehenen Dateien, ohne ein Projekt anzulegen. Rohmaterialien dieses
Repositories, der Bausteinkatalog, lokale Einstellungen und Secrets werden
nicht in neue Projekte übernommen.

## Orientierung

| Thema | Einstieg |
| --- | --- |
| Einrichtung und täglicher Start | [Quickstart](QUICKSTART.md) |
| Verbindliche Projektbeschreibung | [DV-Konzept](docs/DV_KONZEPT.md) |
| Entwicklungsmethodik | [Constitution](.specify/memory/constitution.md) |
| Feature-Spezifikationen | [Feature-Übersicht](specs/README.md) |
| Technologien, Dienste und API-Rezept | [Bausteinkatalog](templates/README.md) |
| Arbeitsregeln für Agenten | [AGENTS.md](AGENTS.md) |
| Referenz-Repositories und Beiträge | [DV-Konzept: Wissensaustausch](docs/DV_KONZEPT.md#wissensaustausch) |

## Prüfen

```sh
python scripts/check.py
```

Dies prüft Dokumentlinks, Dateisyntax und die Template-Tests. Die
[CI](.github/workflows/ci.yml) prüft zusätzlich erzeugte Projekte und Compose.

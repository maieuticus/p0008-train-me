# Bausteinkatalog

Der [Generator](../scripts/create_project.py) kombiniert den gemeinsamen Kern
mit genau einem Technologieprofil und den ausgewählten Diensten. Einrichtung,
Architektur und Betrieb sind im [DV-Konzept](../docs/DV_KONZEPT.md) beschrieben.

| Auswahl | Inhalt |
| --- | --- |
| `--stack none` | Methodik und Dokumentation; noch kein Anwendungscode |
| `--stack python` | Python-Paket, unittest und CI |
| `--stack typescript` | TypeScript, Typprüfung, Node-Tests und CI |
| `--stack java-maven` | JDK/Maven, JUnit und CI |
| `--service postgres` | Lokale PostgreSQL-Datenbank mit Healthcheck |
| `--service keycloak` | Entwicklungs-Realm und lokaler Authentifizierungsdienst |
| `--service observability` | Prometheus, Grafana und erstes Dashboard |
| `--recipe api-service` | [FastAPI, PostgreSQL und Vertragsprüfungen](recipes/api-service/README.md) |

`base/files/` enthält die generischen Projekt-Dokumente. Ein Baustein besteht
aus `module.yaml`, optional `compose.yaml` und einem `files/`-Verzeichnis, dessen
Inhalt in das Projekt kopiert wird. Dateinamen mit `.template` verlieren diese
Endung bei der Erzeugung.

Die API-Ergänzungen außerhalb von `files/` sind bewusst manuell auszuwählende
Hilfen. Sie werden nicht ungeprüft in jedes API-Projekt übernommen.

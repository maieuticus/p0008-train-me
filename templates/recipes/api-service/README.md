# API-Service-Rezept

Das Rezept kombiniert das Python-Profil mit FastAPI, PostgreSQL,
einem versionierten OpenAPI-Vertrag und lokalen/CI-Prüfungen.

```sh
python scripts/create_project.py --name meine-api --recipe api-service --output ../meine-api
```

Einrichtung, Architektur, Entwicklung und Betrieb werden ausschließlich im
[DV-Konzept](../../../docs/DV_KONZEPT.md) beziehungsweise im DV-Konzept des
erzeugten Projekts beschrieben.

## Automatisch übernommen

`files/` enthält die API-Anwendung, Gesundheitstest, Vertragsprüfung,
optionalen Datenbanktest, `.env.test.example`, CI und den Anwendungs-Dockerfile.
Der Generator ergänzt die [API-Prinzipien](constitution/api-service-principles.md)
zur Projekt-Constitution. Alle Projekte verwenden dieselbe
[DV-Konzept-Vorlage](../../base/files/docs/DV_KONZEPT.md.template).

## Erhaltene Erfahrungen

| Frühere Schwierigkeit | Umgesetzte Konsequenz |
| --- | --- |
| Abweichung zwischen Routen und OpenAPI | Vertrag gegen generierte Operationen und Schemas prüfen |
| Verschiedene Datenbankwerte in CI und Tests | CI-Datenbank und Tests lesen dieselbe `.env.test.example` |
| Fehleranfälliges Docker-Healthcheck-Quoting | Separater, begrenzter Bereitschaftstest in CI |
| Widersprüchliche Architektur- und Betriebsanleitungen | Ein verbindliches DV-Konzept |
| Testinitialisierung in produktivem Kontext | Migration und Testinitialisierung klar trennen |
| Dokumentation eines falschen Tunnelmodus | Startverhalten prüfen; Named-Tunnel-Beispiel erhalten |
| Fehlende Validierung von PATCH-Grenzfällen | Anpassbare Schema-Testvorlage erhalten |

Die Erfahrungen stammen aus `p0003-alfred-api`. Die vormals separaten
Makefile-/CI-/Docker-/Betriebsdokumentvorlagen wurden durch die gemeinsamen
Bausteine beziehungsweise den neuen Rezeptinhalt ersetzt.

## Optional auszuwählende Ergänzungen

- [API-Planungscheckliste](docs/api-feature-planning.template.md):
  in den jeweiligen Feature-Plan integrieren.
- [Schema-Validierungstests](tests/test_schema_validation.py.template):
  nur für tatsächliche PATCH-Modelle anpassen.
- [SQL-Migrationsskript](scripts/run_migrations.sh.template):
  optionaler Ansatz für idempotente SQL-Dateien; Betrieb im DV-Konzept beschreiben.
- [Named-Tunnel-Beispiel](docker-compose.cloudflared-snippet.yml):
  bei konkretem Cloudflare-Bedarf in die Deployment-Konfiguration übernehmen.
- [Audit-Agent](.github/agents/speckit.audit.agent.md) und
  [Prompt](.github/prompts/speckit.audit.prompt.md):
  für die passende Copilot-Integration nach der Initialisierung installieren.
- [Copilot-Kontextvorlage](.github/copilot-instructions.md.template):
  bei Bedarf anpassen; maßgebliche Regeln bleiben Constitution und DV-Konzept.

Diese Ergänzungen werden nicht automatisch aktiviert.

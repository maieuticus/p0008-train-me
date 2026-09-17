# API-Feature-Plan: <Feature-Name>

> Diese Checkliste ergänzt das von Spec Kit erzeugte `plan.md`. Sie wird nach
> `/specify` und während `/plan` ausgefüllt. Sie verhindert, dass API-, Schema-,
> Betriebs- oder externe Integrationsauswirkungen erst während der Umsetzung
> auffallen.

## 1. Ziel, Scope und Ausschlüsse

- **Nutzerwert:** <Welches überprüfbare Ergebnis liefert das Feature?>
- **Im Scope:** <Funktionen und betroffene Komponenten>
- **Nicht im Scope:** <Explizit ausgeschlossene Funktionen und spätere Arbeit>
- **Abnahmeszenario:** <Schritte und erwartetes Ergebnis, unabhängig testbar>

## 2. Vertrags- und Kompatibilitätsauswirkungen

- **API-Vertrag:** <Neue/geänderte/entfallende Pfade, Methoden, Schemas,
  Fehlercodes und Authentifizierung; oder „keine“>
- **Kompatibilität:** <Auswirkung auf bestehende Clients und Migrationspfad;
  oder „rückwärtskompatibel“>
- **Externe Verbraucher:** <Custom GPT, Webhook, CLI, SDK o. ä. und die dort
  nötigen Aktualisierungen; oder „keine“>

Bei jeder Vertragsänderung müssen Implementierung, OpenAPI-Datei und
Vertragstest im selben Feature geplant werden.

## 3. Datenmodell und Migration

- **Betroffene Entitäten und Validierungsregeln:** <...>
- **Migration:** <Neue idempotente Datei unter `db/migrations/`; oder „keine“>
- **Datenkorrektur/Backfill:** <Ablauf, Begrenzung, Wiederholbarkeit; oder
  „nicht erforderlich“>
- **Rollback:** <Wie wird bei fehlgeschlagenem Release sicher zurückgerollt?>

`db/init.sql` ist kein Produktionsmigrationsweg. Falls das Feature das Schema
ändert, gehören Backup, Migration und Prüfschritte in den Release-Plan.

## 4. Umsetzung und Verantwortlichkeiten

| Bereich | Geplante Änderung | Maßgebliche Datei(en) |
| --- | --- | --- |
| API/Routing | <...> | <...> |
| Schema/Validierung | <...> | <...> |
| Persistenz | <...> | <...> |
| Vertrag | <...> | <...> |
| Konfiguration/Infrastruktur | <...> | <...> |
| Dokumentation | <...> | <...> |

Neue Abhängigkeiten, Komponenten oder Architekturabweichungen sind im
Constitution Check zu begründen.

## 5. Test- und Betriebsplan

- **Unit-/Schema-Tests:** <Validierung, Null-/Leerwerte, Zustandswechsel>
- **Integrations-/API-Tests:** <Erfolgs-, Fehler- und Berechtigungsfälle>
- **Vertragstest:** <Routenparität und `$ref`-Konsistenz, falls ein Vertrag
  existiert>
- **Lokale Validierung:** <z. B. `python scripts/check.py` und ein konkreter End-to-End-
  Ablauf>
- **Release:** <Backup, Migration, Deployment, Healthcheck>
- **Beobachtung/Rollback:** <Logs/Metriken, Abbruchkriterium und Rückweg>

## 6. Plan-Gate vor `/tasks`

Der Plan ist erst umsetzungsreif, wenn:

- [ ] Scope, Ausschlüsse und ein unabhängiges Abnahmeszenario feststehen.
- [ ] API-Vertrag und externe Verbraucher bewertet sind.
- [ ] Datenmodell, Migration, Backfill und Rollback bewertet sind.
- [ ] Test-, Release- und Betriebsprüfungen konkrete Befehle oder Szenarien
      enthalten.
- [ ] Betroffene Konfiguration und das DV-Konzept als Aktualisierungsaufgaben
      erfasst sind.

## Prompt für `/plan`

```text
Create the implementation plan for <Feature-Name>.

Use the feature specification and constitution as binding inputs. Apply
this feature-local API-service planning checklist: state
scope and exclusions, contract and client compatibility, data-model and
idempotent migration implications, validation and test coverage, operational
release/rollback steps, and every documentation or configuration update.

Do not begin implementation. Mark genuinely unresolved decisions as NEEDS
CLARIFICATION and resolve them during the research phase before creating
tasks.
```

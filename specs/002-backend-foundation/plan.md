# Implementation Plan: Backend-Grundgerüst

**Branch**: `main` (kein eigener Feature-Branch) | **Date**: 2026-09-18 | **Spec**: [spec.md](spec.md)

**Feature-Kontext:** `002-backend-foundation` | **Status:** Technischer Plan erstellt;
Aufgaben, Implementierung und Laufzeitabnahme stehen aus.

## Summary

Feature 002 stellt ein lokal startbares FastAPI-Backend mit unabhängigem
Health-Endpunkt, echter PostgreSQL-Verbindungsprüfung und Alembic-Baseline
bereit. Entwicklung und Tests verwenden getrennte Datenbanken in Linux-
Containern. Die Gesamtprüfung wird um Backend-, Datenbank- und Migrationstests
erweitert. Bestehende Generatorfunktionen bleiben durch eine begrenzte
Entkopplung ihrer Container-Vorlagen erhalten.

Die Architekturvorgaben bleiben im [DV-Konzept](../../docs/DV_KONZEPT.md).
[Recherche](research.md), [Datenmodell](data-model.md),
[HTTP-Vertrag](contracts/health.openapi.yaml),
[Konfigurations-/CLI-Vertrag](contracts/runtime.md) und
[Validierungsszenarien](quickstart.md) konkretisieren dieses Feature.
Mobile App, fachliche Tabellen, Anmeldung und NAS-Deployment sind Folgefeatures.

## Technical Context

**Language/Version**: Python 3.13, Python-Profil mit setuptools und src-Layout.
**Primary Dependencies**: FastAPI/Uvicorn; SQLAlchemy 2 Core, psycopg 3 binary,
Alembic; pytest/httpx für Tests, pip-tools für reproduzierbare Locks.
**Storage**: PostgreSQL 17; persistentes Entwicklungsvolume und separater
flüchtiger Testbestand; zunächst nur Alembic-Revisionsmetadaten.
**Testing**: `python scripts/check.py` im eingerichteten `dev`-Container;
vorhandene unittest-Suite plus `python -m pytest -c backend/pyproject.toml backend/tests --require-full-suite`.
**Target Platform**: Linux-Container auf Docker Desktop mit Compose v2,
vom Windows-PowerShell-Host gesteuert; identische Container für Linux-CI.
**Project Type**: API mit interner administrativer CLI für lokale Entwicklung.
**Performance Goals**: Keine Last-/Durchsatzvorgabe in der Spec. DB-Prüfung:
10 Sekunden Gesamtbudget, maximal 15 Sekunden einschließlich Prozessaufwand
im Akzeptanztest. Migration/Revisionsabfrage: 30 Sekunden Gesamtbudget.
**Constraints**: Keine automatischen Migrationen beim API-Start; keine
Produktivdaten, keine Secrets in Git/Ausgaben, kein Host-Docker-Socket,
Referenzen nur lesbar; tatsächliche Tests von Planungsnachweisen unterscheiden.
**Scale/Scope**: Eine API, ein Health-Endpunkt, eine Baselinerevision, zwei
getrennte lokale DB-Dienste; FR-001 bis FR-014, SC-001 bis SC-005.

Versionierung: vollständige Paket-Locks mit Hashes, gleicher PostgreSQL-
Image-Digest für beide Dienste, gebundener Python-Image-Digest. Exakte
Patchstände werden bei Implementierung aufgelöst und tatsächlich geprüft;
der Plan behauptet keine bereits erzeugten Locks oder installierten Pakete.

## Constitution Check

Vor der Recherche und nach dem Vertragsentwurf wurden alle Prinzipien geprüft.
„Erfüllt im Entwurf“ bezeichnet die Planung, nicht den Nachweis einer Umsetzung.

| Prinzip | Prüfung vor / nach Entwurf und Umsetzungspflicht |
| --- | --- |
| I – Anforderungen | Erfüllt / erfüllt: abgegrenzte Spec, FR-/SC-Zuordnung in der Prüfmatrix; Tasks folgen separat. |
| II – DV-Konzept | Erfüllt / erfüllt: Entscheidungen und Status im DV-Konzept; Feature-Artefakte verfeinern den Umfang. |
| III – Technologiebedarf | Erfüllt / erfüllt: vorhandenes Python-Profil; SQLAlchemy/Alembic begründen reproduzierbare Migrationen, pip-tools bindet Abhängigkeiten. |
| IV – Verträge/Daten | Erfüllt / erfüllt: HTTP-/CLI-Verträge, echte Baseline, getrennte Datenbanken, Wiederholungs- und Fehlerprüfung. |
| V – Änderungsdisziplin | Erfüllt / erfüllt: fokussiertes Backend; nur nötige Entkopplung des Generators, kein allgemeiner Umbau. |
| VI – Tests | Erfüllt / erfüllt: bestehende Tests erhalten; zusätzliche echte DB-/Migrationstests und manuelle Abnahme geplant. |
| VII – Secrets | Erfüllt / erfüllt: lokale Zufallswerte, begrenzte Rollen, ausgewählte Env-Weitergabe und redigierte Fehler. |
| VIII – Reproduzierbarkeit | Erfüllt / erfüllt: Locks/Digests, identische Laufzeit in Entwicklung/CI, Referenzschutz. |
| IX – Wissen | Erfüllt / erfüllt: allgemeine Generatorentkopplung als möglicher späterer Template-Beitrag; keine Veröffentlichung im Planungsauftrag. |
| X – SDD | Erfüllt / erfüllt: Spec → Recherche/Plan/Verträge → Tasks → Analyse → Implementierung → Verifikation. |
| XI – Bestandsprojekt | Erfüllt / erfüllt: vorhandene Skripte/Tests/CI analysiert; Generator bleibt funktionsfähig. |
| XII – Agentenverhalten | Erfüllt / erfüllt: Annahmen benannt, keine fachliche Erweiterung, kein vorgetäuschter Laufzeitnachweis. |

**Gate vor Recherche:** bestanden; offene technische Entscheidungen O-01/O-03
wurden als Rechercheaufträge behandelt. **Gate nach Entwurf:** bestanden;
keine ungelöste fachliche Klärung und keine begründungspflichtige
Constitution-Ausnahme. Implementierungs- und Abnahmegates bleiben offen.

## Project Structure

Geplante Pfade; außer den Feature-Dokumenten werden sie erst implementiert:

```text
backend/
  pyproject.toml
  requirements.lock
  requirements-dev.lock
  alembic.ini
  src/train_me_backend/
    __init__.py
    main.py                  # App-Factory, Health, keine Startmigration
    settings.py              # explizite Konfigurationsauswahl/Validierung
    database.py              # Engine, begrenzte Verbindung, SELECT 1
    db.py                    # check / upgrade / current; Prozessbudget
  migrations/
    env.py
    script.py.mako
    versions/0001_baseline.py
  tests/
    conftest.py              # Zielschutz, DB-Fixtures, --require-full-suite
    test_health.py
    test_settings.py
    test_database.py
    test_migrations.py
    test_cli.py
scripts/
  backend_init.py            # Anwendungskonfiguration, vorhandene Werte erhalten
  check.py                  # explizite Teilprüfmeldung; bleibt generisch
  create_project.py         # generische Containerbasis verwenden
.devcontainer/
  Dockerfile                # gebundene Backend-Testabhängigkeiten
  compose.yaml              # dev, postgres, postgres-test
  devcontainer.json         # Projektname, Dienste, Initialisierung
  postgres/init-app.sh       # begrenzte DB-Rollen, nur leere Instanzen
templates/base/files/.devcontainer/
  Dockerfile                # bisherige generische Basis
  compose.yaml
  devcontainer.json
tests/
  test_template.py           # bestehende Generatornachweise + Entkopplung
  test_backend_setup.py      # Konfiguration erhalten, Fehler/Secrets prüfen
config/project.yaml         # Projektmetadaten und vollständige Checks
.env.example                # ausschließlich Platzhalter, getrennte Präfixe
.github/workflows/ci.yml    # Templatejobs erhalten, eigener Backendjob
docs/DV_KONZEPT.md           # verbindliche Einrichtung/Entwicklung/Prüfstatus
```

`backend_init.py` verwendet den vorhandenen Container-Helfer, wird aber nicht
als Anwendungsabhängigkeit in generierte Template-Projekte kopiert. Für die
Anwendung muss er auch vorhandene `.env`-Dateien um fehlende Schlüssel ergänzen;
die bisherige Erstellung nur bei nicht vorhandener Datei reicht nicht.
Auch handbearbeitete lokale Compose-Overrides dürfen nicht unkontrolliert
überschrieben werden; bestehende Zusatzfelder und lesbare Referenzmounts bleiben
erhalten. Ein Konflikt wird gemeldet, nicht durch Neuinitialisierung beseitigt.

Die Anwendung verwendet `kind: project`, `name: p0008-train-me`, `stack: python`,
`services: [postgres]`, `recipe: null`. `services` bezeichnet den ausgewählten
Baustein, nicht die Anzahl seiner Entwicklungs-/Testinstanzen. Template-Herkunft
bleibt nachvollziehbar. Kein leeres Mobile-Verzeichnis und kein Generatorlauf
über das befüllte Repository.

## Verträge, Daten und externe Verbraucher

- HTTP: `GET /health` → HTTP 200, JSON `{"status":"ok"}`, ohne DB- oder
  Versionsangaben. Der Prozess startet auch ohne verfügbare DB; ungültige
  DB-Konfiguration wird erst bei einem ausdrücklichen DB-Befehl benötigt.
- DB-CLI: `python -m train_me_backend.db check|upgrade|current --target
  development|test`; Ziel ist Pflicht. Exits und Fehlerkategorien stehen im
  [Laufzeitvertrag](contracts/runtime.md). `upgrade` entspricht Alembic
  `upgrade head`; keine freie destruktive Ziel-/SQL-Eingabe.
- Baseline: genau eine Revision `0001_baseline`, kein fachliches DDL. Upgrades
  sind transaktional; Wiederholung erhält Revision und vorhandene Daten.
  Kein `create_all`, kein `stamp head`, keine Startmigration.
- Zugriff: Bootstrap-Zugangsdaten nur im zugehörigen Datenbankcontainer;
  `dev` erhält nur die Entwicklungs-/Testrollen. Diese dürfen weder Datenbanken
  noch Rollen erstellen und sind keine Superuser.
- Datenbestand: Keine Anwendungsdatenmigration oder Backfills, keine externen
  Verbraucher und keine Breaking Changes. Lokale `.env`-Werte/Volumes bleiben
  bei Wiederholung erhalten. NAS-/Produktivmigration ist nicht betroffen.

## Prüfung und Betrieb

### Automatische Prüfmatrix

| Anforderungen / Erfolg | Nachweis in der Umsetzung |
| --- | --- |
| FR-001, FR-011; SC-001 | Container aus gebundenen Images/Locks aufbauen, Uvicorn starten, stoppen und erneut starten; Portkonflikt sichtbar; keine Quellcodeänderung nötig. |
| FR-002; US1.3, EC-02 | Exakter HTTP-Vertrag im TestClient und im laufenden Prozess; bei gestoppter DB weiterhin 200; Health öffnet keine DB-Verbindung. |
| FR-003–004; SC-002 | Echtes `SELECT 1`; falsches Passwort, fehlender Pflichtwert, fehlende DB und gestoppter Dienst ergeben Fehler. Kontrolliert hängender TCP-Peer prüft das Gesamtbudget; rein lesend und ohne Zielreset. |
| FR-005; EC-07 | Falscher Host/Port/DB/Benutzer, fehlende Wegwerfmarkierung und Alias zum Entwicklungsziel werden vor Bereinigung abgelehnt; Identität serverseitig bestätigen; keine Entwicklungswerte als Testfallback. |
| FR-006–007; SC-003 | Zwei seriell unabhängig vorbereitete leere Testbestände erreichen `0001_baseline`; Wiederholung mit synthetischer Probe erhält Tabellen/Zeilen/Inhalt. |
| FR-008; EC-06 | Nicht erreichbare DB und kontrolliert fehlschlagende Testmigration: Exit != 0, kein fälschlich fortgeschriebener Stand, transaktionale Rücknahme; anschließender Wiederanlauf über `current`/`upgrade`. |
| FR-009–010; SC-004 | Vollständiger Check führt Template-, Backend-, echte DB- und Migrationstests aus; fehlende DB oder übersprungene Pflichtgruppe verhindert Erfolg. `--static-only` meldet ausgelassene Gruppen. |
| FR-012; SC-005 | Manueller Nachweis gemäß Feature-Quickstart, mit Umgebung, Versionen, Schritten, Soll/Ist und Einschränkungen im DV-Konzept. |
| FR-013; US4.5 | Linux-CI verwendet echte getrennte DB und denselben vollständigen Aufruf; bisherige generierte Projekte bleiben prüfbar. |
| FR-014; EC-03–04 | Wiederholte Initialisierung erhält Werte, Kommentare und lokale Overrides; Pflichtwertfehler verständlich; synthetische Geheimwerte erscheinen weder in stdout/stderr noch API-Antworten. |

Die Fehler-Migration gehört ausschließlich zum Testfixture in einem temporären
Migrationsverzeichnis; sie wird nie Teil der auslieferbaren Revisionskette.
Keine Parallelisierung der Tests, die denselben Testbestand zurücksetzen.
Direkte SQL-Testoperationen haben ebenfalls Connect-/Statement-Budgets.

### Laufzeit und CI

Compose erhält einen festen Projektnamen `train-me` für den dokumentierten
Host-Ablauf. Der `dev`-Container bleibt unabhängig von laufenden Datenbanken
startbar; dessen Prozess-Liveness darf kein DB-Health-Gate haben. PostgreSQL-
Healthchecks steuern nur die ausdrückliche Datenbankbereitstellung. Alle
Compose-Aufrufe erfolgen auf dem Host, Python-Befehle im Container-Arbeitsordner
`/workspaces/project`. Dazu legt Compose für `dev` ausdrücklich
`working_dir: /workspaces/project` und `user: vscode` fest.
Backend-Abhängigkeiten liegen in `/opt/train-me-venv`; diese Umgebung gehört
`vscode` und steht im Image-PATH vor den anderen Python-Umgebungen. Dadurch
verwenden auch direkte `compose exec`-Befehle dieselbe Python-/pip-Installation
mit passenden Schreibrechten. Das lokale Paket wird nach dem Mount installiert.
`remoteUser` allein ersetzt diese Compose-Einstellungen nicht.

Die Prüfkommandos in `config/project.yaml` bleiben Listen von Argumenten:
zuerst `python -m unittest discover -s tests -v`, dann
`python -m pytest -c backend/pyproject.toml backend/tests --require-full-suite`.
Der vollständige Backendlauf muss auch die Sammlung/Ausführung aller
Pflichtgruppen bestätigen; Umgebungsflags wie `RUN_DATABASE_TESTS=0`, leere
Sammlung oder Skips dürfen diesen Lauf nicht stillschweigend grün machen.
Der Backend-Testhook aktiviert diese Kontrolle über die projektspezifische
pytest-Option `--require-full-suite`, die im gemeinsamen Prüfaufruf immer gesetzt
ist. Er prüft auch durch Filter abgewählte Pflichtgruppen und übersprungene
Pflicht-Tests. Direkte pytest-Aufrufe ohne diese Option werden ausdrücklich
als Teilprüfung ausgewiesen.

Der neue Linux-Backendjob baut dieselben Container, initialisiert lokale
ephemere Zugangsdaten und führt `python scripts/check.py` im `dev`-Container aus.
Anschließend erfolgt ein echter HTTP-Smoke-Test mit Uvicorn. Compose-Ressourcen
werden im job-eigenen Projekt entfernt; Entwicklung und produktive Daten
sind für den Job nicht erreichbar. Ein `timeout-minutes` begrenzt den Job.
Bestehende Templatejobs prüfen weiterhin Dokumente und unittest separat;
die Generator-/Rezeptjobs bleiben erhalten.

### Fehlerdiagnose, Wiederanlauf und Rückweg

Ein DB-Fehler wird anhand Kategorie/Ziel behandelt: Pflichtschlüssel ergänzen,
Dienst starten oder Zugangsdaten bewusst korrigieren. Bestehende Werte werden
nicht automatisch rotiert. Nach einem Migrationsabbruch erst `current`, dann
erneut `upgrade`; bei unbekannter Revision anhalten. PostgreSQL führt die
Baseline transaktional aus. Kein automatisches `stamp`, Downgrade oder Reset.

`stop` und `down` ohne Volumenlöschung erhalten das Entwicklungsvolume.
Ein Code-Rückweg auf den vorherigen Stand benötigt wegen der leeren Baseline
keine Löschung von Daten oder Revisionsmetadaten. Testfixtures bereinigen nur
ihre bekannten Testobjekte. Dieses Feature liefert keinen Produktionsrelease,
kein NAS-Backupverfahren und keine produktive Rollback-Automatik. Vor einer
späteren datenverändernden Migration sind Backup/Wiederherstellung gesondert
zu planen. Lokale Beobachtung erfolgt über Health, CLI-Status und redigierte Logs.

## Dokumentation

O-01 ist für Backend/Container/Generator entschieden; Mobile-Struktur bleibt
beim Mobile-Feature. O-03 ist durch Laufzeiten, Locks, Treiber, Migration und
Fehlerbudgets entschieden. Im DV-Konzept werden aktueller Projektstand,
Architektur, Einrichtung, Entwicklung, Entscheidungen und Prüfstatus angepasst.
Die ausführbare Betriebsanleitung folgt mit der tatsächlichen Implementierung;
der Feature-Quickstart ist vorerst ein erwarteter Validierungsablauf.
README, Root-Quickstart und Feature-Übersicht verweisen auf den erreichten Stand.

Nächste Phase: `speckit-tasks`, danach Konsistenzanalyse und Implementierung.
Dieser Plan erzeugt noch keine Aufgabenliste und keine Anwendung. Für den
späteren Implementierungsauftrag werden Umgebung, dann verfügbares Modell,
Begründung, Ergebnis und automatische/manuelle Checks festgehalten; die
Modellwahl ist keine dauerhafte Architekturentscheidung.

## Complexity Tracking

Keine Constitution-Ausnahmen. Die zusätzlichen Mittel haben einen konkreten Zweck:

| Mittel | Bedarf | Einfachere geprüfte Alternative |
| --- | --- | --- |
| SQLAlchemy + Alembic | Ein Datenzugriff, versionierter Migrationsstand | Eigener SQL-Runner müsste Revisions-/Transaktionslogik nachbauen. |
| Zwei PostgreSQL-Dienste | Destruktive Tests vom Entwicklungsbestand trennen | Gemeinsame Datenbank verletzt die geforderte Datenisolation. |
| Prozessbudget der CLI | Endliches Fehlerverhalten auch bei hängender Verbindung | Connect-/Statement-Timeout allein deckt nicht den ganzen Ablauf. |
| Drei generische Container-Vorlagen | Bestehenden Generator beim App-Ausbau erhalten | Root-Konfiguration weiterzuverwenden erzeugt doppelte Dienste/falsche Pfade. |
| pip-tools | Exakte transitive Abhängigkeiten mit Hashes | Offene Ranges oder manuelles Freeze allein bieten keinen gepflegten Auflösungsweg. |

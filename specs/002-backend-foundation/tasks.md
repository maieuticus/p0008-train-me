# Tasks: Backend-Grundgerüst

**Input**: Design-Artefakte aus `specs/002-backend-foundation/`

**Voraussetzungen**: `spec.md`, `plan.md`, `research.md`, `data-model.md`,
`contracts/`, `quickstart.md`

**Status**: Aufgabenliste erstellt am 2026-09-18. Die Aufgaben sind noch nicht
ausgeführt.

## Phase 1: Setup (gemeinsame Infrastruktur)

**Zweck**: Anwendungsstruktur, reproduzierbare Abhängigkeiten und lokale
Entwicklungsparameter vorbereiten.

- [ ] T001 [P] Erzeuge das Python-Backend mit `backend/pyproject.toml`, dem src-Layout `backend/src/train_me_backend/` und den Testpfaden `backend/tests/` gemäß `specs/002-backend-foundation/plan.md`.
- [ ] T002 [P] Ergänze `backend/pyproject.toml` mit Python 3.13, FastAPI, Uvicorn, SQLAlchemy 2, `psycopg[binary]` 3, Alembic, pytest und httpx sowie der pytest-Option `--require-full-suite` in `backend/tests/conftest.py`.
- [ ] T003 [P] Erzeuge `backend/requirements.lock` und `backend/requirements-dev.lock` mit pip-tools, exakten Versionen und Hashes; prüfe die Installation unter Python 3.13/Linux mit `--require-hashes`.
- [ ] T004 [P] Ergänze `.env.example` und `scripts/backend_init.py` mit getrennten Entwicklungs-/Testschlüsseln; erhalte vorhandene Werte, Kommentare und lokale Overrides und gib bei fehlenden/ungültigen Pflichtschlüsseln nur Schlüsselnamen aus.
- [ ] T005 [P] Lege die generische Containerbasis in `templates/base/files/.devcontainer/Dockerfile`, `templates/base/files/.devcontainer/compose.yaml` und `templates/base/files/.devcontainer/devcontainer.json` ab, ohne Backend- oder PostgreSQL-Anwendungsabhängigkeiten einzubauen.

## Phase 2: Foundational (blockierende Voraussetzungen)

**Zweck**: Gemeinsame Container-, Konfigurations-, Datenbank- und
Migrationsgrundlage fertigstellen. Diese Phase blockiert alle User Stories.

- [ ] T006 Stelle den Generator in `scripts/create_project.py` auf die generische Containerbasis unter `templates/base/files/.devcontainer/` um und entferne die direkte Verwendung der später projektspezifischen Root-Containerdateien.
- [ ] T007 [P] Aktualisiere `.devcontainer/Dockerfile`, `.devcontainer/compose.yaml` und `.devcontainer/devcontainer.json` für `dev`, `postgres` und `postgres-test`, `working_dir: /workspaces/project`, `user: vscode`, `/opt/train-me-venv` im PATH, PostgreSQL 17 und keine veröffentlichten DB-Ports.
- [ ] T008 [P] Ergänze `backend/alembic.ini`, `backend/migrations/env.py`, `backend/migrations/script.py.mako` und `backend/migrations/versions/0001_baseline.py` mit einer leeren Alembic-Baseline `revision=0001_baseline`, `down_revision=None` und ohne fachliche Tabellen.
- [ ] T009 [P] Implementiere `backend/src/train_me_backend/settings.py` mit den Zielwerten `development`/`test`, Pflichtfeld- und Wegwerfzielsvalidierung sowie ohne Fallback zwischen den Präfixen.
- [ ] T010 Implementiere `backend/src/train_me_backend/database.py` mit SQLAlchemy-Engine, Dialekt `postgresql+psycopg`, `connect_timeout=3`, sitzungsbezogenem `statement_timeout=3000` und redigierter Fehlerklassifikation (abhängig von T009).
- [ ] T011 Implementiere `backend/src/train_me_backend/db.py` mit `check`, `upgrade` und `current`, verpflichtendem `--target`, Exitcodes 0–3, Prozessbudget sowie den Vertragsausgaben aus `specs/002-backend-foundation/contracts/runtime.md` (abhängig von T008–T010).
- [ ] T012 [P] Ergänze `templates/services/postgres/compose.yaml` und die projektspezifische Compose-Konfiguration um getrennte PostgreSQL-17-Volumes, Healthchecks, Bootstrap-Skripte und eingeschränkte Anwendungsrollen; ändere die generische Vorlage nicht semantisch.
- [ ] T013 [P] Erweitere `tests/test_template.py` und ergänze `tests/test_backend_setup.py`, um Generatorisolierung, erhaltene lokale Werte, getrennte Rollen/Hosts, keine Secrets in Ausgaben und vorhandene Template-Funktionalität zu prüfen.
- [ ] T014 [P] Aktualisiere `config/project.yaml`, `.github/workflows/ci.yml` und `scripts/check.py`, sodass der vollständige Projektcheck Backend-/DB-/Migrationstests ausführt, der Linux-CI-Job echte `postgres-test`-Dienste verwendet und `--static-only` Teilprüfung/Auslassungen ausdrücklich meldet.

**Checkpoint**: Container, Konfiguration, Python-Umgebung, Migrationsrahmen,
Generatorregressionen und der vollständige Prüfaufruf sind vorhanden; noch kein
User-Story-Nachweis gilt als abgeschlossen.

## Phase 3: User Story 1 – Backend nachvollziehbar starten (Priority: P1, MVP)

**Ziel**: Backend reproduzierbar starten, stoppen und erneut starten; `/health`
bestätigt ausschließlich den laufenden Prozess.

**Unabhängiger Test**: In der Compose-Umgebung Uvicorn starten, `GET /health`
prüfen, den Prozess wiederholen und bei gestoppter Entwicklungsdatenbank erneut
HTTP 200 mit `{"status":"ok"}` nachweisen.

- [ ] T015 [P] [US1] Schreibe den Vertragstest für `GET /health` in `backend/tests/test_health.py` gemäß `specs/002-backend-foundation/contracts/health.openapi.yaml`; prüfe HTTP 200, exakt `{"status":"ok"}` und keine Datenbankverbindung.
- [ ] T016 [US1] Implementiere `backend/src/train_me_backend/main.py` mit App-Factory `create_app`, der Route `GET /health` und ohne automatische Migration oder Datenbankprüfung beim Import/Start (abhängig von T015).
- [ ] T017 [P] [US1] Ergänze `backend/tests/test_settings.py` um App-Start ohne DB-Konfiguration, Port-/Konfigurationsfehler und Erhalt der getrennten Zielauswahl.
- [ ] T018 [US1] Aktualisiere `specs/002-backend-foundation/quickstart.md` und den Abschnitt Einrichtung in `docs/DV_KONZEPT.md` mit dem tatsächlich implementierten Start-/Stopp-/Neustartbefehl und dem Uvicorn-Health-Nachweis (abhängig von T016).

**Checkpoint**: US1 ist unabhängig über Compose, Uvicorn und `/health`
prüfbar; ein DB-Ausfall darf den Liveness-Nachweis nicht verändern.

## Phase 4: User Story 2 – Datenbankzugriff eindeutig nachweisen (Priority: P1)

**Ziel**: Eine echte PostgreSQL-Operation bestätigt Zugriff; falsche,
fehlende oder nicht erreichbare Konfiguration schlägt mit redigiertem Fehler
innerhalb des Zeitbudgets fehl.

**Unabhängiger Test**: `check --target test` gegen `postgres-test` erfolgreich
ausführen und anschließend falsches Passwort, fehlenden Wert, fehlende DB und
gestoppten Dienst jeweils als Fehler nachweisen.

- [ ] T019 [P] [US2] Schreibe `backend/tests/test_database.py` für eine echte `SELECT 1`-Operation gegen `postgres-test`, getrennte Entwicklung/Testziele, Identitätsprüfung mit `current_database()`/`current_user` und fehlende DB-Konfiguration.
- [ ] T020 [P] [US2] Schreibe `backend/tests/test_cli.py` für Exitcodes 1–3, falsches Passwort, nicht erreichbaren Host, fehlende Pflichtwerte, redigierte Fehler und das 10-Sekunden-Gesamtbudget einschließlich kontrolliert hängendem TCP-Ziel.
- [ ] T021 [US2] Ergänze die Bootstrap-SQL-/Compose-Initialisierung unter `.devcontainer/postgres/` für eingeschränkte `train_me_dev`-/`train_me_test`-Rollen; verhindere Superuser- oder automatische Passwortrotation für Anwendungsprozesse.
- [ ] T022 [US2] Vervollständige `backend/src/train_me_backend/db.py` für `check --target development|test` mit echter SQL-Operation, Timeoutüberwachung, festen Fehlerkategorien und ohne DSN-/Secret-Ausgabe (abhängig von T019–T021).
- [ ] T023 [US2] Dokumentiere die vier Verbindungsfälle, Zielschutzregeln und den Wiederanlauf in `specs/002-backend-foundation/quickstart.md` und `specs/002-backend-foundation/contracts/runtime.md` anhand der tatsächlich verfügbaren Befehle.

**Checkpoint**: US2 unterscheidet Liveness, Datenbankbereitschaft,
Authentifizierungsfehler, fehlende Konfiguration und Zeitüberschreitung.

## Phase 5: User Story 3 – Datenbankbasis reproduzierbar herstellen (Priority: P1)

**Ziel**: Die leere Testdatenbank erreicht per echtem Alembic-Upgrade eine
prüfbare Baseline; Wiederholung erhält Revision und synthetische Daten.

**Unabhängiger Test**: Zwei seriell vorbereitete leere Testbestände auf
`0001_baseline` bringen, einen Sentinel einfügen, Upgrade wiederholen und
Revision/Inhalt/Tabellenbestand vergleichen.

- [ ] T024 [P] [US3] Schreibe `backend/tests/test_migrations.py` für `upgrade head`, genau eine Revisionszeile `0001_baseline`, idempotente Wiederholung, Sentinel-Erhalt und zwei unabhängig geleerte Testbestände.
- [ ] T025 [P] [US3] Ergänze in `backend/tests/test_migrations.py` Negativtests für unbekannte Objekte/Revisionen, falsches Testziel, unterbrochene Verbindung und eine fehlschlagende temporäre Migration; prüfe Rollback und keinen vorgetäuschten Erfolg.
- [ ] T026 [US3] Implementiere Alembic-Konfigurationsübergabe und `upgrade --target` in `backend/src/train_me_backend/db.py` so dass nur `upgrade head` zählt, kein `stamp`, kein `create_all`, kein Start-Upgrade und keine pauschale Schema-/Datenbanklöschung verwendet wird (abhängig von T008, T011, T024).
- [ ] T027 [US3] Implementiere die geschützte Testfixture in `backend/tests/conftest.py`: akzeptiere nur `postgres-test:5432/train_me_test/train_me_test` mit `DISPOSABLE=1`, bestätige Serveridentität und entferne ausschließlich bekannte eigene Probeobjekte.
- [ ] T028 [US3] Aktualisiere `specs/002-backend-foundation/data-model.md` und `specs/002-backend-foundation/quickstart.md` mit dem tatsächlich beobachteten Baseline-/Wiederholungs-/Rollback-Nachweis (abhängig von T024–T027).

**Checkpoint**: US3 weist eine reale, wiederholbare und geschützte Migration
nach; Entwicklungsdaten bleiben von Testvorbereitung und Fehlerfällen getrennt.

## Phase 6: User Story 4 – Prüfstand verlässlich prüfen (Priority: P2)

**Ziel**: Vollständiger und statischer Prüfpfad unterscheiden Erfolg, Fehler
und ausgelassene Pflichtprüfungen; manueller Nachweis ist nachvollziehbar.

**Unabhängiger Test**: Vollständigen Check, statische Teilprüfung und Check bei
gestopptem `postgres-test` ausführen; Ergebnisse und Auslassungen unterscheiden.

- [ ] T029 [P] [US4] Ergänze `backend/tests/test_full_suite.py` oder `backend/tests/conftest.py` um die Sammlungspflicht für Backend-, DB- und Migrationsgruppen, `--require-full-suite`, nicht erlaubte Pflicht-Skips und Fehler bei leerer/abgewählter Pflichtgruppe.
- [ ] T030 [P] [US4] Ergänze `tests/test_check_integration.py` für `scripts/check.py`, `--static-only`, Exitcode bei fehlender Testdatenbank und die ausdrückliche Meldung „Teilprüfung“ ohne vollständigen Abnahmenachweis.
- [ ] T031 [US4] Führe die vollständige Prüfmatrix in `.github/workflows/ci.yml` aus: Container starten, getrennte Testdatenbank abwarten, `python scripts/check.py` im `dev`-Container ausführen, HTTP-Smoke-Test durchführen und Compose-Ressourcen im Job aufräumen.
- [ ] T032 [US4] Aktualisiere `config/project.yaml`, `scripts/check.py` und die bestehende Template-CI so, dass generierte Beispielprojekte keine Backend-Pfade übernehmen und Templatejobs statische Prüfung/Unittests weiterhin getrennt ausführen.
- [ ] T033 [US4] Ergänze den manuellen Nachweis im Prüfstatus von `docs/DV_KONZEPT.md` mit Git-/Umgebungsstand, Schritten, Soll/Ist, Exit-/HTTP-Codes, Einschränkungen und dem tatsächlich ausgeführten CI-Ergebnis.

**Checkpoint**: US4 unterscheidet vollständige Abnahme, statische Teilprüfung,
fehlende DB und nicht ausgeführte Prüfungen; alle vier Stories sind gemeinsam
über den Root-Check nachvollziehbar.

## Phase 7: Polish und querschnittliche Abschlussarbeiten

- [ ] T034 [P] Aktualisiere `README.md`, `QUICKSTART.md` und `specs/README.md` auf den implementierten Backend-Start, die Task-/Analyse-/Implementierungsreihenfolge und die tatsächlichen Einschränkungen.
- [ ] T035 [P] Prüfe `docs/DV_KONZEPT.md`, `specs/002-backend-foundation/plan.md`, `research.md`, `data-model.md`, `contracts/` und `quickstart.md` auf Abweichungen vom Code, insbesondere Versionen, Pfade, Health-Vertrag, Zeitbudgets und Secret-Regeln.
- [ ] T036 Führe `python scripts/check.py`, den vollständigen Backend-Check im Compose-Netz, den Quickstart und `git diff --check` aus; dokumentiere tatsächlich ausgeführte und nicht ausgeführte Container-, DB-, CI- und manuellen Prüfungen.
- [ ] T037 [P] Prüfe, dass keine realen Secrets, erweiterten Referenzrechte, Docker-Sockets, generierten Volumes oder Laufzeitlogs in Git aufgenommen wurden; kontrolliere `.gitignore`, Compose-Dateien und die Ausgabeerfassung.

## Abhängigkeiten und Ausführungsreihenfolge

### Phasenabhängigkeiten

- Phase 1 hat keine Abhängigkeit.
- Phase 2 hängt von Phase 1 ab und blockiert alle User Stories.
- US1 und US2 hängen von Phase 2 ab; US2 benötigt zusätzlich T009–T011.
- US3 hängt von Phase 2 sowie T009–T011 ab und verwendet die DB-Konfiguration aus US2.
- US4 hängt von US1–US3 ab, weil sie deren Prüfgruppen und Fehlerverhalten integriert.
- Polish hängt von allen gewünschten User Stories ab.

### User-Story-Abhängigkeiten

- US1 ist das MVP und kann nach Phase 2 unabhängig geprüft werden.
- US2 kann nach Phase 2 parallel zu US1 implementiert werden, benötigt aber die gemeinsame Settings-/DB-Grundlage.
- US3 kann nach Phase 2 beginnen, wird für die echte Migration aber nach US2s Zielschutz-/Verbindungslogik ausgeführt.
- US4 folgt nach den drei P1-Stories, damit der vollständige Root-Check reale Gruppen ausführen kann.

### Parallelisierbare Arbeiten

- T001–T005 betreffen getrennte Setup-Dateien und können parallel vorbereitet werden.
- T008–T009, T012–T014 können parallel vorbereitet werden, sobald die betroffenen Setup-Pfade feststehen.
- T015 und T017 sowie T019–T020 und T024–T025 sind getrennte Testdateien und können parallel erstellt werden; sie bleiben bis zur jeweiligen Implementierung rot.
- T029–T030 können parallel vorbereitet werden.
- T034–T035 und T037 sind nach der Umsetzung unabhängig voneinander prüfbar.

## Implementierungsstrategie

1. Phase 1 und Phase 2 abschließen und die Generatorregressionen prüfen.
2. US1 als MVP implementieren und den Health-/Neustartnachweis führen.
3. US2 ergänzen und echte DB-Verbindungsfehler nachweisen.
4. US3 mit Baseline, Sentinel und Rollback abschließen.
5. US4 in Root-Check und CI integrieren.
6. Quickstart, DV-Konzept, Locks, Image-Digests und Prüfstatus aktualisieren.
7. Erst nach dem vollständigen automatischen und manuellen Nachweis das Feature zur Abnahme vorlegen.

## Abschlusskriterien

- Jede Aufgabe folgt dem Format `- [ ] Txxx [P?] [US?] Beschreibung mit Pfad`.
- Jede User Story besitzt ein unabhängiges Testkriterium.
- Pflichtprüfungen, echte Datenbankzugriffe und nicht ausgeführte Prüfungen sind unterscheidbar.
- `tasks.md` ist eine Aufgabenliste, kein Nachweis bereits ausgeführter Implementierung.

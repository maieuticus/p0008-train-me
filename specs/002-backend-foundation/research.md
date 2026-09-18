# Recherche und Entscheidungen: Backend-Grundgerüst

**Datum:** 2026-09-18 | **Grundlage:** [Spec](spec.md),
[DV-Konzept](../../docs/DV_KONZEPT.md), Constitution 1.1.0

Die Entscheidungen gelten für Feature 002. Sie sind Planungsentscheidungen;
Installation, Paketauflösung und Laufzeitvalidierung erfolgen in der Umsetzung.
Offene technische Fragen dieses Features sind damit entschieden. Fachliche
Folgefeatures und die produktive NAS-Bereitstellung bleiben ausgeklammert.

## R-01: Entwicklungsweg und Repository-Struktur (O-01)

**Entscheidung:** Python-Backend unter `backend/` mit `src/train_me_backend/`.
Der verbindliche Abnahmeweg verwendet Linux-Container über Docker Compose,
auf Windows vom PowerShell-Host aus gesteuert. Der bestehende Service `dev`
führt Python, Uvicorn und Prüfungen aus. Hinzu kommen `postgres` und
`postgres-test`; die Datenbanken haben getrennte Zugangsdaten und Speicher.
Nur der API-Port wird an `127.0.0.1:8000` veröffentlicht. Spec Kit bleibt mit
seinen vorhandenen PowerShell-Skills auf dem Host.

**Begründung:** Nutzt die vorhandene Python-Containerbasis, hält Datenbanktests
plattformgleich zur Linux-CI und benötigt keinen Docker-Socket im Container.
Der Entwickler startet Uvicorn ausdrücklich im `dev`-Service; ein separates
Produktionsimage ist für dieses Feature nicht erforderlich.

**Alternativen:** Native Windows-Installation erzeugt einen zweiten
Abhängigkeits-/Testpfad. Vollständige Umstellung von Spec Kit auf Bash ist für
das Backend unnötig. Codespaces und VS Code „Reopen in Container“ sind mögliche
weitere Umgebungen, aber kein behaupteter Abnahmenachweis; abweichende Compose-
Projektnamen können eigene Volumes erzeugen. „Attach to Running Container“ kann
den bereits gestarteten Container verwenden. Mobile-Verzeichnisse werden erst
mit dem Mobile-Feature bestimmt.

**Quelle:** [Compose-Projektname](https://docs.docker.com/compose/how-tos/project-name/).

## R-02: Generator vom Anwendungscontainer entkoppeln (O-01)

**Entscheidung:** Vor den Anwendungsänderungen werden die heutigen generischen
Dateien `.devcontainer/Dockerfile`, `compose.yaml` und `devcontainer.json` als
Generatorvorlagen unter `templates/base/files/.devcontainer/` übernommen.
`scripts/create_project.py` liest diese Basis statt der später projektspezifischen
Root-Konfiguration. Der Dockerfile-Eintrag in `CORE_FILES` wird entsprechend
entfernt. Die vorhandenen Generatorfunktionen und neun Tests bleiben erhalten.

**Begründung:** Der aktuelle Generator liest Root-Compose direkt und ergänzt
Dienste. Ein dort bereits ergänztes `postgres` würde beim Generieren des
API-Rezepts eine doppelte Compose-Komponente auslösen; Backend-Pfade würden
außerdem in fremde Beispielprojekte gelangen.

**Alternativen:** Generator entfernen verletzt A-06. Eine Kopie des gesamten
Repositories als neue Template-Engine wäre unnötig. Die begrenzte Entkopplung
erhält den bestehenden Vertrag; zusätzliche Regressionen prüfen fehlende
Anwendungsabhängigkeiten in generierten Projekten.

**Belege:** `scripts/create_project.py` (`CORE_FILES`, `render_files`),
`tests/test_template.py`, `templates/stacks/python/`.

## R-03: Laufzeiten und reproduzierbare Abhängigkeiten (O-03)

**Entscheidung:** Python 3.13 auf der vorhandenen Bookworm-Containerlinie;
PostgreSQL 17 für die beiden neuen Anwendungsdatenbanken. Python-Pakete werden
mit pip-tools unter Linux/Python 3.13 aufgelöst. `backend/requirements.lock`
enthält die Laufzeitabhängigkeiten; `backend/requirements-dev.lock` ergänzt
Tests und Build-Werkzeuge unter den Constraints des Runtime-Locks. Beide
enthalten exakte Versionen und Hashes. Installation erfolgt mit
`pip install --require-hashes`; das eigene lokale Paket anschließend mit
`--no-deps --no-build-isolation -e backend`.

**Begründung:** Python 3.13 ist bereits in Container und CI vorgesehen.
PostgreSQL 17 bietet für eine neue Datenbank eine längere verbleibende
Unterstützung als die generische PostgreSQL-16-Vorlage. Die Vorlage selbst
bleibt bei ihrer bisherigen Version. pip/setuptools/wheel und pip-tools werden
ebenfalls versioniert; PyYAML bleibt mit den gemeinsamen Werkzeugen kompatibel.
Die tatsächlichen Paketpatchstände sowie Image-Tags und Digests werden bei der
ersten erfolgreichen Auflösung festgehalten, nicht aus Dokumentationstiteln
geschätzt. Beide PostgreSQL-Services verwenden denselben geprüften Image-Digest.
Auch der Python-Basisimage-Digest wird im Dockerfile gebunden. Updates erfolgen
bewusst mit erneuter Prüfung, nicht beim normalen Start.

**Alternativen:** Offene Versionsbereiche oder `latest` allein sind kein
reproduzierbarer Installationsvertrag. uv/Poetry würden hier zusätzliche
Werkzeugkonventionen einführen. Python 3.14/PostgreSQL 18 bringen für die
Baseline keinen benötigten Funktionsvorteil.

**Quellen:** [Python-Versionen](https://devguide.python.org/versions/),
[PostgreSQL-Unterstützung](https://www.postgresql.org/support/versioning/),
[pip-tools](https://pip-tools.readthedocs.io/en/stable/),
[FastAPI-Versionierung](https://fastapi.tiangolo.com/deployment/versions/).

## R-04: Datenzugriff und Migration (O-03)

**Entscheidung:** FastAPI und Uvicorn; synchrones SQLAlchemy 2 mit
`psycopg[binary]` 3 und dem Dialekt `postgresql+psycopg`; Alembic für versionierte
Migrationen. SQLAlchemy Core reicht aus. `0001_baseline` hat keinen Vorgänger
und keine fachlichen Tabellen. Ein echtes `upgrade head` erzeugt den
nachweisbaren Eintrag in `alembic_version`. `stamp` ersetzt diesen Ablauf nicht.

**Begründung:** Ein gemeinsamer Datenzugriff für Prüfung und Alembic vermeidet
parallele Verbindungslogik. Die Baseline baut das Migrationsverfahren auf, ohne
Profil-/Trainingstabellen vorwegzunehmen. Verbindungen und Migrationen werden
nur in ausdrücklichen Datenbankbefehlen geöffnet bzw. ausgeführt.

**Alternativen:** Nur psycopg plus eigener SQL-Migrationsrunner spart eine
Bibliothek, verlangt aber eigene Revisions-/Transaktionslogik. Async-Engine,
asyncpg, zusätzlicher Pool und Repository-Schichten sind für eine Baseline
nicht nötig. Das Initialisierungsrezept des Templates ist kein Ersatz für
versionierte Anwendungsmigrationen.

**Quellen:** [SQLAlchemy-Psycopg-Dialekt](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg),
[Psycopg-Installation](https://www.psycopg.org/psycopg3/docs/basic/install.html),
[Alembic-Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html).

## R-05: Liveness, Datenbankprüfung und Fehlerbudget (O-03)

**Entscheidung:** `GET /health` liefert ausschließlich `{"status":"ok"}`.
Die separate CLI prüft die gewählte Datenbank mittels `SELECT 1`.
Verbindungsaufbau: 3 Sekunden; SQL-Statement: 3 Sekunden; ein überwachender
Prozess begrenzt den gesamten DB-Prüfvorgang auf 10 Sekunden zuzüglich
Prozessstart/-beendigung. Der Akzeptanztest erlaubt maximal 15 Sekunden auf
der unterstützten Umgebung. Es gibt keine automatischen Wiederholungen.
Der Migrations-/Revisionsaufruf erhält ein separates Gesamtbudget von 30 Sekunden.

**Begründung:** `connect_timeout` begrenzt nicht den gesamten DNS-/SQL-/Netzablauf.
Ein abgebrochener Befehl meldet Fehler, niemals einen angenommenen Erfolg.
Ausgaben enthalten feste Fehlerkategorien und gegebenenfalls Variablennamen,
keine DSNs, Passwörter oder ungefilterten Treiber-/Validierungsfehler.

**Alternativen:** Datenbankzugriff in `/health` verletzt FR-002. Ein zusätzliches
HTTP-Readiness-API ist nicht nötig. `pg_isready` dient nur als Container-
Startsignal; es ersetzt keine erfolgreich authentifizierte SQL-Operation.

**Quellen:** [libpq-Verbindungsparameter](https://www.postgresql.org/docs/17/libpq-connect.html#LIBPQ-PARAMKEYWORDS),
[PostgreSQL-Timeouts](https://www.postgresql.org/docs/17/runtime-config-client.html),
[Python-Subprozess-Timeout](https://docs.python.org/3/library/subprocess.html),
[pg_isready](https://www.postgresql.org/docs/17/app-pg-isready.html).

## R-06: Testisolation, Initialisierung und Wiederholung

**Entscheidung:** `postgres` hat ein benanntes Entwicklungsvolume;
`postgres-test` verwendet flüchtigen Speicher. Die Testkonfiguration muss
ausdrücklich `postgres-test:5432`, Datenbank und Rolle `train_me_test` sowie
`TRAIN_ME_TEST_DB_DISPOSABLE=1` benennen. Vor Bereinigung werden zusätzlich
`current_database()` und `current_user` geprüft. Es gibt keinen Fallback auf
Entwicklungswerte. Tests entfernen nur bekannte eigene Objekte; unbekannte
Objekte oder Revisionen führen zum Abbruch.

Die PostgreSQL-Bootstrap-Rolle bleibt im jeweiligen Datenbankcontainer.
Backend und Tests erhalten eigene Rollen ohne Superuser-, Datenbankerstellungs-
oder Rollenverwaltungsrechte. Initialisierung gewährt ihnen Rechte nur auf
ihre jeweilige Datenbank und deren Anwendungsschema. Keine Datenbankports
werden auf dem Host veröffentlicht.

`scripts/backend_init.py` ergänzt fehlende Projektschlüssel in `.env` und
erzeugt fehlende lokale Passwörter. Bestehende Werte werden erhalten; ungültige,
leere oder doppelte Pflichtschlüssel werden anhand ihres Namens gemeldet.
`scripts/container_init.py` bleibt als generischer Helfer erhalten.

**Begründung:** Zwei physisch getrennte PostgreSQL-Instanzen, beschränkte Rollen
und Zielprüfung schützen Entwicklungsdaten bei Migrations-/Resettests.
Zwei nacheinander unabhängig geleerte Testbestände weisen SC-003 nach. Eine
synthetische Probe-Tabelle zeigt zusätzlich, dass Wiederholung Daten erhält.
Vorhandene PostgreSQL-Volumes werden durch geänderte Env-Werte nicht neu
initialisiert; ein Kennwortproblem rechtfertigt keinen automatischen Reset.

**Alternativen:** SQLite/Mocks allein erfüllen den echten Datenbanknachweis
nicht. Gemeinsame Entwicklungs-/Testdatenbank und pauschales `DROP ... CASCADE`
werden vermieden. Anwendungstabellen sind für den Wiederholungstest unnötig.

**Quellen:** [PostgreSQL-Rollen](https://www.postgresql.org/docs/17/sql-createrole.html),
[PostgreSQL-Rechte](https://www.postgresql.org/docs/17/ddl-priv.html),
[offizielles PostgreSQL-Image](https://hub.docker.com/_/postgres).

## R-07: Prüfaufruf und CI

**Entscheidung:** Die bestehenden unittest-Prüfungen bleiben in
`config/project.yaml`; hinzu kommt `python -m pytest -c backend/pyproject.toml
backend/tests --require-full-suite`. Fehlende Testdatenbank ist im vollständigen Lauf ein Fehler,
kein Skip. `--static-only` kennzeichnet ausdrücklich eine Teilprüfung.
Die bisherigen Generatorjobs bleiben erhalten; ein eigener Linux-Backendjob
führt den vollständigen Check im selben Compose-Container aus.

**Begründung:** Der unveränderte Einstieg `python scripts/check.py` erhält
FR-009. Windows-/Linux-Templatejobs führen die statische Prüfung und die
Generator-unittests ausdrücklich separat aus und behaupten keine Backendabnahme.
FastAPI-TestClient/httpx prüfen den HTTP-Vertrag; echte PostgreSQL-Tests prüfen
Verbindung und Migration. Ein Laufzeitfehler und ein absichtlich nicht
ausgeführter Pflicht-Test müssen im vollständigen Prüflauf erfolglos enden.

**Alternativen:** Der bisherige Rezeptschalter `RUN_DATABASE_TESTS` mit
automatischem Skip widerspricht FR-009. Nur API-Mocks oder nur Template-CI
weisen die neue Anwendung nicht nach.

**Quellen:** [FastAPI-Tests](https://fastapi.tiangolo.com/tutorial/testing/),
[Compose-Startreihenfolge](https://docs.docker.com/compose/how-tos/startup-order/).

## Recherche- und Setup-Nachweis

Repository, Spezifikation, Constitution, Profil und Generator wurden gelesen.
Zwei Rechercheagenten untersuchten Datenzugriff/Migration sowie Container/CI;
die Entscheidungen oben wurden zusammengeführt. Externe Quellen wurden am
2026-09-18 geprüft. Es wurden keine Abhängigkeiten installiert oder Dienste gestartet.

`.specify/extensions.yml` war vor und nach der Planung nicht vorhanden;
es waren keine Vor-/Nach-Hooks auszuführen.
`setup-plan.ps1 -Json` wurde versucht, aber vor der Ausführung durch die lokale
PowerShell-Ausführungsrichtlinie blockiert (`PSSecurityException`). Deshalb
wurde die Struktur aus `.specify/templates/overrides/plan-template.md` direkt
übernommen. Es wurde keine Ausführungsrichtlinie geändert. Der Feature-Pfad
stammt aus `.specify/feature.json`; der tatsächliche Git-Branch ist `main`.

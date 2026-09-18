# Vertrag: Konfiguration, Datenbank-CLI und Prüfung

**Status:** Geplanter Implementierungsvertrag für [Feature 002](../spec.md).
Alle Python-Befehle gelten im eingerichteten Container vom Repository-Root aus.
Die CLI ist ein lokales Entwicklungswerkzeug, keine externe Administrations-API.

## Konfiguration

| Variablen | Entwicklung | Tests |
| --- | --- | --- |
| Präfix | `TRAIN_ME_DEV_DB_` | `TRAIN_ME_TEST_DB_` |
| `HOST` | `postgres` | `postgres-test` |
| `PORT` | `5432` | `5432` |
| `NAME` | `train_me_dev` | `train_me_test` |
| `USER` | `train_me_dev` | `train_me_test` |
| `PASSWORD` | Eigener lokal erzeugter Wert | Anderer lokal erzeugter Wert |
| `DISPOSABLE` | Nicht verwendet | `1`, nur für den ausgewiesenen Testbestand |

Hinzu kommen `TRAIN_ME_DEV_DB_ADMIN_PASSWORD` und
`TRAIN_ME_TEST_DB_ADMIN_PASSWORD` für die Erstinitialisierung der jeweiligen
PostgreSQL-Instanz. Diese werden nur an den passenden Datenbankdienst
weitergegeben, nicht an `dev`. Die Adminrolle heißt intern `postgres`.
Die DB-Images erhalten die Standardvariablen ausdrücklich aus den jeweiligen
projektspezifischen Werten; kein gemeinsames ungefiltertes `env_file` für alle Dienste.

Alle Verbindungsfelder des gewählten Ziels sind Pflicht. Fehlende/leere Werte,
Platzhalter wie `__GENERATE__`, ungültige Ports und doppelte `.env`-Schlüssel
werden zurückgewiesen. Die Fehlermeldung darf den Variablennamen enthalten,
aber nie dessen sensitiven Inhalt. Keine automatische `.env`-Suche in der
Anwendung: Compose injiziert die ausgewählten Werte. Host-Umgebungsvariablen
können gemäß Compose-Regeln `.env` übersteuern; die Anleitung benennt diese
Priorität und vermeidet Dumps der expandierten Konfiguration.

`python scripts/backend_init.py` richtet den lokalen Konfigurationsbestand
ein. Fehlt `.env`, wird sie aus der Beispielkonfiguration erzeugt; fehlen
einzelne Schlüssel, werden nur diese ergänzt. Vorhandene Bytes/Werte/Kommentare
bleiben erhalten. Ungültige vorhandene Werte werden gemeldet und nicht ersetzt.
Passwörter werden unabhängig zufällig erzeugt, nicht zwischen Diensten kopiert.
Wiederholung darf kein bereits initialisiertes DB-Passwort ändern.

Der generische Container-Helfer darf beim ersten Anlegen der lokalen Dateien
verwendet werden. Bestehende `compose.local.yaml`/`local.json` werden vorab
gelesen; unbekannte Benutzerfelder bleiben erhalten. Das bisherige unbedingte
Neuschreiben des Overrides darf der neue Initialisierer für solche Dateien
nicht aufrufen. Fehlende notwendige Felder werden gezielt ergänzt oder
Konflikte verständlich gemeldet. Referenzmounts bleiben ausschließlich lesbar.

## Datenbankbefehle

```text
python -m train_me_backend.db check --target development
python -m train_me_backend.db check --target test
python -m train_me_backend.db upgrade --target development
python -m train_me_backend.db upgrade --target test
python -m train_me_backend.db current --target development
python -m train_me_backend.db current --target test
```

`--target` ist immer erforderlich; zulässige Werte sind ausschließlich
`development` und `test`. Es gibt weder einen Standard für Schreiboperationen
noch einen Fallback auf die jeweils andere Umgebung.

| Befehl | Operation | Erfolgsnachweis auf stdout |
| --- | --- | --- |
| `check` | Neue echte Verbindung, `SELECT 1`, Ergebnis prüfen, Verbindung schließen | `DB_OK target=development` bzw. `DB_OK target=test` |
| `upgrade` | Alembic `upgrade head` mit gewählter Verbindung, danach Revision prüfen | `MIGRATION_OK target=<target> revision=0001_baseline` |
| `current` | Revision aus einer tatsächlich erreichten DB lesen | `REVISION target=<target> revision=0001_baseline` oder `revision=none` bei erreichbarem uninitialisiertem Bestand |

`revision=none` ist kein Nachweis angewendeter Migration. Eine unbekannte
Revision ist in Feature 002 ein Fehler. Die Konfigurationsdatei
`backend/alembic.ini` enthält nur Pfade/Logging, keine Verbindungsgeheimnisse.
Die CLI setzt die Verbindung programmgesteuert. Keine Migration bei
API-Import, API-Start oder `GET /health`.

| Exitcode | Bedeutung |
| --- | --- |
| 0 | Gewählter Befehl wurde erfolgreich ausgeführt. |
| 1 | Verbindung, Authentifizierung, SQL oder Migration fehlgeschlagen. |
| 2 | Ungültiges Argument, fehlende/ungültige Konfiguration oder verweigertes Testziel. |
| 3 | Gesamtbudget des Vorgangs überschritten. |

Fehlerausgabe auf stderr beginnt mit einer festen Kategorie, beispielsweise
`CONFIG_ERROR`, `TARGET_REFUSED`, `DB_ERROR`, `MIGRATION_ERROR` oder `DB_TIMEOUT`,
und nennt höchstens Zielbezeichnung und geprüfte Pflichtschlüsselnamen.
Keine Erfolgszeile bei Fehlern; keine Roh-Exceptions, DSNs, Kennwörter,
Tracebacks mit Konfigurationswerten oder vollständigen Env-/Compose-Dumps.

## Zeitgrenzen und Zielschutz

`check`: Connect-Timeout 3 Sekunden, Statement-Timeout 3000 Millisekunden,
Gesamtbudget des überwachten DB-Prozesses 10 Sekunden. Prozessstart/-beendigung
benötigen zusätzlich Zeit; der Laufzeittest verlangt Abschluss innerhalb
15 Sekunden. `upgrade`/`current`: höchstens 30 Sekunden für den DB-Prozess,
35 Sekunden im Laufzeittest. Keine automatische Retry-Schleife.

Bei Timeout beendet der überwachende Prozess den Worker und wartet auf dessen
Ende; Secrets stehen nicht in Prozessargumenten. Bei abgebrochenem Upgrade ist
der tatsächliche Stand anschließend mit `current` festzustellen. Ein Timeout
beweist weder Erfolg noch Misserfolg eines bereits abgeschlossenen Commits.

Vor Migrationen gegen `test` und jeder Testbereinigung muss die Konfiguration
Host `postgres-test`, Port 5432, DB/Rolle `train_me_test` und Wegwerfindikator `1`
erfüllen. Nach Verbindung wird die DB-/Benutzeridentität bestätigt.
Entwicklungsziel, Administratorrolle oder unbekannter Zielbestand führen zur
Ablehnung. Keine Datenbanklöschung und kein pauschales Schema-Reset.
Der Befehl `check` bleibt rein lesend; kontrollierte falsche/hängende Ziele
dürfen ausschließlich für dessen Negativtests injiziert werden.

## Gemeinsamer Prüflauf

`python scripts/check.py` prüft Dokumente/Syntax und alle Einträge aus
`config/project.yaml`. Im implementierten Feature sind dies die bestehenden
unittests sowie Backend-, echte PostgreSQL- und Migrationstests. Fehlende
Backend-Abhängigkeiten, Testkonfiguration oder Datenbank führen zu Exit != 0.

Der gemeinsame Check ruft pytest mit der projektspezifischen Option
`--require-full-suite` auf. Der Backend-Testhook kontrolliert damit, dass die
Pflichtgruppen gesammelt und tatsächlich ausgeführt wurden. Ein übersprungener
Pflicht-Test, eine leere Gruppe oder das Abwählen einer Pflichtgruppe verhindert
Erfolg; `RUN_DATABASE_TESTS` ist kein Freigabeschalter. Direkte pytest-Aufrufe
ohne diese Option weisen sich als Teilprüfung aus. Der CI-/Abnahmeaufruf
verwendet immer die vollständige Suite und dokumentiert ihre Gruppen.

`python scripts/check.py --static-only` führt nur Dokument-/Syntaxprüfungen
aus. Bei Erfolg darf Exit 0 zurückgegeben werden, die Ausgabe muss aber
„Teilprüfung“ und die nicht ausgeführten konfigurierten Prüfkommandos nennen.
Im Anwendungsprojekt umfasst dies Template-, Backend-, DB- und Migrationstests;
die generische Umsetzung darf keine Backend-Pfade in andere Projekte einbauen.

Der manuelle Nachweis ist zusätzlich im Prüfstatus des DV-Konzepts zu führen.
Kein einzelner Exitcode oder Planungsbericht ersetzt die Feature-Abnahme.

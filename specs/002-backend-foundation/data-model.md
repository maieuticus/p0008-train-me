# Datenmodell: Backend-Grundgerüst

**Status:** Entwurf für die Umsetzung von [Feature 002](spec.md).
Es werden keine Benutzer-, Profil-, Übungs- oder Trainingsmodelle eingeführt.

## 1. Umgebungskonfiguration

Konfiguration wird aus ausdrücklich ausgewählten Umgebungsvariablen gelesen,
nicht in der Datenbank gespeichert. `development` und `test` haben eigene
Werte. Der vollständige Variablenvertrag steht in
[contracts/runtime.md](contracts/runtime.md#konfiguration).

| Feld | Typ / Regel | Verwendung |
| --- | --- | --- |
| target | Enum `development`, `test`; Pflichtargument | Wählt ausschließlich das zugehörige Variablenpräfix. |
| host | Nicht leer; keine Mehrfachhostliste | PostgreSQL-Ziel; Tests zum Schreiben nur `postgres-test`. |
| port | Ganzzahl 1–65535 | Im unterstützten Compose-Weg 5432. |
| database | Nicht leer | Entwicklung `train_me_dev`, Tests `train_me_test`. |
| username | Nicht leer | Eigene eingeschränkte Rolle je DB. |
| password | Nicht leer, kein Platzhalter; nie in Repr/Logs | Lokaler sensitiver Wert, nur über Env übergeben. |
| disposable | Für Testvorbereitung exakt `1` | Zusätzliche ausdrückliche Kennzeichnung des wegwerfbaren Ziels. |

Es gibt keinen impliziten Wechsel auf andere Präfixe, localhost oder SQLite.
SQLAlchemy erhält die Verbindung über strukturierte Parameter/`URL.create`,
ohne Passwortverkettung in einer selbstgebauten URL. Connection- und
Statement-Timeouts werden intern festgesetzt; freie DSN-Optionen dürfen die
Budgets nicht aushebeln. Anwendungsimport und Health-Route lesen keine
verpflichtende DB-Konfiguration.

Bootstrap-Konfiguration ist davon getrennt: Jede PostgreSQL-Instanz erhält ein
eigenes lokales Administratorpasswort nur zur Erstinitialisierung. Der
Backendprozess erhält diese Administratorwerte nicht. Das Initialisierungsskript
erzeugt die jeweilige Anwendungsrolle mit `LOGIN`, ohne Superuser-,
`CREATEDB`-, `CREATEROLE`-, Replikations- oder RLS-Bypass-Rechte und ohne
privilegierte Rollenmitgliedschaften. Die Bootstrap-Rolle bleibt DB-Eigentümer;
die Anwendungsrolle darf sich verbinden, im eigenen Bestand Schema-/Tabellen-
Objekte erstellen und eigene Objekte migrieren. Das sind technische
DB-Berechtigungen, keine vorweggenommene fachliche Rollenmatrix.

## 2. Migrationsstand

| Objekt | Inhalt / Regel |
| --- | --- |
| Revisionsdatei | `backend/migrations/versions/0001_baseline.py` |
| revision | `0001_baseline` |
| down_revision | `None` |
| upgrade / downgrade | Keine fachlichen Tabellen oder Datenoperationen. |
| Revisionsspeicher | Alembic-Tabelle `public.alembic_version` mit `version_num`; nach Upgrade genau eine Zeile `0001_baseline`. |

Der Alembic-Revisionsspeicher wird durch das tatsächliche Upgrade verwaltet.
Er ist keine fachliche Tabelle. Eine fehlende Versionstabelle wird nur bei
erfolgreicher Verbindung als „noch nicht migriert“ ausgewiesen; ein
Verbindungsfehler ist kein leerer Revisionsstand.

```text
Erreichbarer leerer Bestand --upgrade--> 0001_baseline
0001_baseline              --upgrade--> 0001_baseline (unverändert)
Beliebiger Bestand         --Fehler---> kein behaupteter neuer Stand
Unbekannte Revision        --upgrade--> Fehler, manuelle Diagnose
```

Upgrades verwenden Transaktionen. Eine erzwungene Testmigration, die nach DDL
fehlschlägt, prüft Rollback und unveränderte Versionsmetadaten. Sie liegt nur
in einem temporären Testverzeichnis. Historische Revisionen werden nach ihrer
Übernahme nicht nachträglich geändert. Fachliche Migrationen/Backfills folgen
mit ihren jeweiligen Features.

## 3. Synthetischer Testbestand

Nur in der geprüften wegwerfbaren Testdatenbank existiert während der Tests
das Schema `feature002_probe` mit einer Tabelle `sentinel`:

| Feld | Typ / Zweck |
| --- | --- |
| id | Integer-Primärschlüssel; feste synthetische ID |
| value | Text; fester synthetischer Prüfinhalt ohne Personenbezug |

Nach der ersten Baseline-Anwendung wird die Probe angelegt. Ein erneutes
Upgrade muss Inhalt, Anzahl, Tabellenbestand und Revision erhalten.
Die Fixture entfernt anschließend nur diese bekannten eigenen Objekte und
den bekannten Baseline-Revisionsspeicher. Unerwartete Benutzerobjekte oder
Revisionen führen zum Abbruch. Systemschemas und Extension-Objekte werden
nicht als Anwendungsobjekte behandelt und niemals bereinigt.

Vor jeder schreibenden Testvorbereitung gelten zwei Schranken:

1. Konfiguration muss dem ausdrücklich erlaubten Testziel entsprechen und vom
   Entwicklungsziel verschieden sein. Der Wegwerfindikator muss gesetzt sein.
2. Eine Verbindung bestätigt `current_database() = 'train_me_test'` und
   `current_user = 'train_me_test'`; erst danach darf Vorbereitung schreiben.

Zwei seriell unabhängig geleerte Testbestände erreichen denselben
Baselinestand. Keine pauschale Datenbank-/Schema-Löschung, keine parallelen
Fixture-Resets und keine Bereinigung der Entwicklungsdatenbank.

## 4. Prüfergebnis und manueller Nachweis

Dies sind Nachweisformate in Ausgabe/Dokumentation, keine neuen Datenbanktabellen.

| Feld | Bedeutung |
| --- | --- |
| scope | `static`, `template`, `backend`, `database`, `migration`, `manual` |
| environment | Host/Container, Laufzeit-/Imageversionen, DB-Zielbezeichnung ohne Secrets |
| revision | Geprüfter Git-Stand einschließlich Hinweis auf lokale Änderungen |
| command / steps | Tatsächlich ausgeführter Befehl bzw. Bedienfolge |
| expected / actual | Soll- und Ist-Ergebnis, einschließlich Exitcode/HTTP-Status |
| result | Erfolgreich, fehlgeschlagen oder nicht ausgeführt |
| limitations | Ausgelassene Umgebungen/Prüfungen, Fehler und Restrisiken |

Vollständiger automatischer Erfolg verlangt tatsächlich ausgeführte erfolgreiche
Pflichtgruppen. Ein dokumentierter statischer Erfolg ist nur eine Teilprüfung.
Manueller Start-/Health-/DB-Nachweis und automatisierte Tests sind getrennt
aufzuführen. Der verbindliche Nachweis wird im Prüfstatus des DV-Konzepts gepflegt.

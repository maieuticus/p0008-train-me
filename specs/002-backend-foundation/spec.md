# Feature: Backend-Grundgerüst

**Branch**: Kein eigener Feature-Branch angelegt | **Datum**: 2026-09-17 | **Status**: Entwurf, Anforderungen geprüft

**Feature-Verzeichnis**: `specs/002-backend-foundation/`

**Eingabe**: Das Backend lässt sich lokal starten, stellt einen Health-Endpunkt
bereit und erreicht eine PostgreSQL-Testdatenbank. Datenbankmigrationen sind
reproduzierbar ausführbar. Automatisierte Tests und eine verständliche
Startanleitung machen den erfolgreichen Aufbau überprüfbar. Grundlage sind
der erste Funktionsumfang und seine Abnahmekriterien im DV-Konzept.

## Ziel und Umfang

Das Entwicklungsteam benötigt eine nachprüfbar startbare Anwendungsbasis,
auf der anschließend die Profilverwaltung aufgebaut werden kann. Bisher
enthält das Repository Template-Werkzeuge und Beispielprojekte. Ein Erfolg
dieser Template-Prüfungen weist noch keinen funktionierenden Projektbetrieb nach.

Dieses Feature liefert einen dokumentierten Entwicklungsweg, einen
beobachtbaren Backend-Status, einen unabhängigen Nachweis der Datenbankverbindung
und eine wiederholbar anwendbare Migrationsbaseline. Automatisierte Prüfungen
und ein manueller Startnachweis zeigen, welche Teile tatsächlich funktionieren.

### Im Umfang

- Backend und Entwicklungsdatenbank in einer frischen, unterstützten
  Entwicklungsumgebung einrichten, starten, stoppen und erneut starten.
- Den vereinbarten Health-Endpunkt bereitstellen und die Datenbankverbindung
  unabhängig davon überprüfen.
- Eine Migrationsbaseline für eine leere Testdatenbank anwenden und
  den erreichten Stand bei einem erneuten Lauf erhalten.
- Entwicklungs- und Testkonfiguration trennen, verständliche Fehler melden
  und lokale Zugangsdaten vor Veröffentlichung schützen.
- Die vorhandene gemeinsame Prüfung um relevante Anwendungsprüfungen ergänzen.
- Projektmetadaten, benötigte Anwendungsverzeichnisse, Entwicklungsumgebung,
  CI-Prüfungen und Startdokumentation auf den realisierten Umfang abstimmen.

### Außerhalb des Umfangs

Mobile App, Benutzeranmeldung, Rollen und Profilverwaltung, fachliche
Trainingsdatenmodelle, Übungskatalog, Trainingsplanung, Player, Sprache,
KI-Export und -Import sowie produktives NAS-Deployment sind Folgefeatures.
Dieses Paket stellt keine produktiv freigegebene oder öffentlich zugängliche
Anwendung bereit. Es entwickelt kein allgemeines Template-Updateverfahren.

### Festgelegte Randbedingungen und Annahmen

- **A-01**: FastAPI/Python, PostgreSQL und `GET /health` sind bereits im
  [DV-Konzept](../../docs/DV_KONZEPT.md#erster-funktionsumfang) vorgegeben.
  Diese Spec übernimmt die Vorgaben. Bibliotheken, Paketstruktur, Versionen,
  Datenbanktreiber und Migrationswerkzeug werden im technischen Plan entschieden.
- **A-02**: Für die Abnahme genügt ein vollständig dokumentierter,
  reproduzierbarer Entwicklungsweg. Der Plan legt dessen Voraussetzungen
  und Zielumgebung fest; zusätzliche Betriebssystemvarianten sind keine
  eigenständige Anforderung dieses Features.
- **A-03**: Einrichtung kann Werkzeuge und Pakete herunterladen.
  Der eingerichtete Backend-Betrieb benötigt keine KI-Dienste.
- **A-04**: Die Baseline benötigt keine fachlichen Benutzer-, Profil- oder
  Übungstabellen. Tests verwenden eine ausdrücklich ausgewiesene, wegwerfbare
  Testdatenbank und synthetische Daten.
- **A-05**: Ein vollständiger Abnahmenachweis benötigt ausgeführte
  Datenbankprüfungen. Eine Teilprüfung bleibt als Teilprüfung erkennbar.
- **A-06**: Vorhandene Benutzeränderungen und funktionierende Template-Werkzeuge
  bleiben erhalten. Die Anwendungsintegration wird gezielt geplant.

## User Scenarios & Testing

### User Story 1 - Backend nachvollziehbar starten (Priority: P1)

Als Entwickler möchte ich das projektspezifische Backend anhand einer
Anleitung starten und seinen laufenden Zustand feststellen, damit ich
eine verlässliche Grundlage für die nächsten Features habe.

**Independent Test**: In einer frischen unterstützten Entwicklungsumgebung
die dokumentierten Voraussetzungen herstellen, den Startablauf ausführen
und den Backend-Status prüfen. Dazu sind keine Profile oder Trainingsdaten nötig.

**Acceptance Scenarios**:

1. **Given** eine frische Umgebung mit den dokumentierten Voraussetzungen,
   **When** der Entwickler Einrichtung und Startanleitung ausführt,
   **Then** startet das Backend ohne manuelle Quellcodeänderung und der
   dokumentierte Health-Aufruf liefert HTTP 200 sowie den vereinbarten Status.
2. **Given** eine bereits eingerichtete Entwicklungsumgebung,
   **When** das Backend dokumentiert gestoppt und erneut gestartet wird,
   **Then** ist derselbe Statusnachweis wieder möglich, ohne Daten zu löschen.
3. **Given** ein laufendes Backend, dessen Datenbank nicht erreichbar ist,
   **When** der Health-Endpunkt abgefragt wird,
   **Then** liefert er weiterhin HTTP 200 für den laufenden Backend-Prozess,
   behauptet aber keine erfolgreiche Datenbankverbindung.

### User Story 2 - Datenbankzugriff eindeutig nachweisen (Priority: P1)

Als Entwickler möchte ich unabhängig vom Backend-Status erkennen,
ob die konfigurierte Datenbank tatsächlich erreichbar ist, damit ich
Konfigurations- und Verbindungsfehler früh bemerke.

**Independent Test**: Die dokumentierte Verbindungsprüfung gegen eine
echte Testdatenbank ausführen und anschließend mit falschen Zugangsdaten
sowie ohne erreichbare Datenbank wiederholen.

**Acceptance Scenarios**:

1. **Given** eine erreichbare, korrekt konfigurierte Testdatenbank,
   **When** die separate Verbindungsprüfung ausgeführt wird,
   **Then** bestätigt eine tatsächlich ausgeführte Datenbankoperation den Zugriff.
2. **Given** eine nicht erreichbare Datenbank oder falsche Zugangsdaten,
   **When** die Verbindungsprüfung ausgeführt wird,
   **Then** endet sie innerhalb ihrer dokumentierten endlichen Wartezeit mit
   erkennbarem Fehler und meldet keinen erfolgreichen Zugriff.
3. **Given** eine fehlende oder unvollständige Datenbankkonfiguration,
   **When** die Einrichtung oder Verbindungsprüfung diese benötigt,
   **Then** benennt sie die fehlende Konfiguration verständlich, ohne
   Zugangsdaten auszugeben oder stillschweigend ein anderes Datenziel zu verwenden.
4. **Given** getrennte Entwicklungs- und Testkonfigurationen,
   **When** die Datenbanktests ausgeführt werden,
   **Then** betreffen ihre Änderungen ausschließlich die Testdatenbank.

### User Story 3 - Datenbankbasis reproduzierbar herstellen (Priority: P1)

Als Entwickler möchte ich eine leere Testdatenbank auf einen eindeutig
erkennbaren Ausgangsstand bringen und den Ablauf wiederholen können,
damit spätere Datenänderungen kontrolliert darauf aufbauen.

**Independent Test**: Die Baseline auf eine leere Testdatenbank anwenden,
den erreichten Stand feststellen und den Vorgang auf demselben Stand
wiederholen. Der Test benötigt keine fachlichen Anwendungsdaten.

**Acceptance Scenarios**:

1. **Given** eine leere, erreichbare Testdatenbank,
   **When** der dokumentierte Migrationsablauf ausgeführt wird,
   **Then** ist die Baseline angewendet und ihr Stand nachvollziehbar erkennbar.
2. **Given** eine Datenbank auf dem Baselinestand mit synthetischen Prüfdaten,
   **When** derselbe Migrationsablauf erneut ausgeführt wird,
   **Then** bleiben Stand und vorhandene Daten erhalten und es entstehen
   keine doppelten Einträge durch die Wiederholung.
3. **Given** eine Datenbank, auf die nicht zugegriffen werden kann,
   **When** der Migrationsablauf ausgeführt wird,
   **Then** wird ein Fehler gemeldet und die Baseline nicht als erfolgreich
   angewendet ausgewiesen.

### User Story 4 - Den erreichten Stand verlässlich prüfen (Priority: P2)

Als Entwickler oder Reviewer möchte ich einen gemeinsamen Prüfaufruf und
einen nachvollziehbaren manuellen Nachweis verwenden, damit ich Erfolg,
Fehler und nicht ausgeführte Prüfungen unterscheiden kann.

**Independent Test**: Die dokumentierte Gesamtprüfung ausführen, einen
Datenbankfehler gezielt nachstellen und die Ergebnisdarstellung sowie
das manuelle Prüfprotokoll kontrollieren.

**Acceptance Scenarios**:

1. **Given** eine eingerichtete Testumgebung,
   **When** `python scripts/check.py` ausgeführt wird,
   **Then** laufen die bestehenden relevanten Prüfungen sowie die neuen
   Backend-, Verbindungs- und Migrationstests mit nachvollziehbarem Ergebnis.
2. **Given** ein fehlschlagender Anwendungs- oder Datenbanktest,
   **When** die Gesamtprüfung ausgeführt wird,
   **Then** meldet sie den Fehler und endet erfolglos.
3. **Given** eine ausdrücklich angeforderte Teilprüfung ohne Datenbanktests,
   **When** ihr Ergebnis dokumentiert wird,
   **Then** sind Umfang und fehlende Datenbankprüfung sichtbar; das Ergebnis
   wird nicht als vollständiger Feature-Abnahmenachweis ausgewiesen.
4. **Given** ein lokal startbarer Stand,
   **When** der manuelle Abnahmetest durchgeführt wird,
   **Then** dokumentiert das Prüfprotokoll Umgebung, ausgeführte Schritte,
   erwartete und tatsächliche Ergebnisse sowie verbleibende Einschränkungen.
5. **Given** eine frische CI-Umgebung mit den dokumentierten Voraussetzungen,
   **When** die konfigurierte Projektprüfung ausgeführt wird,
   **Then** prüft sie das tatsächliche Backend einschließlich einer getrennten
   Testdatenbank und der Migrationen; alleinige Template-Prüfungen genügen nicht.

### Edge Cases

- **EC-01**: Fehlende Konfiguration oder ein belegter Startport darf nicht
  zu einer irreführenden Erfolgsmeldung führen; der betroffene Startschritt
  muss mit einem verständlichen Fehler enden.
- **EC-02**: Erreichbares Backend bei ausgefallener Datenbank liefert zwei
  unterscheidbare Ergebnisse: Backend läuft, Datenbankprüfung fehlgeschlagen.
- **EC-03**: Falsches Kennwort, fehlende Datenbank oder unterbrochene Verbindung
  führt bei der Datenbankprüfung zu einem sichtbaren Fehler innerhalb der
  dokumentierten Wartezeit. Meldungen enthalten keine Secrets.
- **EC-04**: Wiederholter Start und wiederholte Baseline-Anwendung dürfen
  bestehende lokale Einstellungen und Daten nicht ungefragt zurücksetzen.
- **EC-05**: Ein Testlauf ohne verfügbare Testdatenbank kann die vollständige
  Abnahme nicht bestehen; eine bewusst gewählte Teilprüfung bleibt kenntlich.
- **EC-06**: Ein fehlgeschlagener Migrationslauf darf keinen erfolgreichen
  Baselinestand vortäuschen. Diagnose und sicherer Wiederanlauf werden
  mit dem gewählten Migrationsverfahren dokumentiert.
- **EC-07**: Destruktive Testvorbereitung darf keine Entwicklungsdatenbank
  oder produktive Daten als Ziel verwenden.

## Requirements

### Functional Requirements

- **FR-001**: Das Projekt MUSS einen reproduzierbaren Weg zur Einrichtung,
  zum Start, Stopp und erneuten Start von Backend und Entwicklungsdatenbank
  mit dokumentierten Voraussetzungen bereitstellen. Einrichtung erfordert
  keine Änderung von Anwendungsquellcode. (US1; EC-01, EC-04)
- **FR-002**: Ein laufendes Backend MUSS `GET /health` mit HTTP 200 und
  einem dokumentierten Status beantworten, auch bei nicht erreichbarer
  Datenbank. Dieser Nachweis beschreibt den laufenden Backend-Prozess und
  bestätigt keine Datenbankbereitschaft.
  (US1.1, US1.3; EC-02)
- **FR-003**: Das Projekt MUSS den Zugriff auf eine echte PostgreSQL-Testdatenbank
  mit einer getrennten, tatsächlich ausgeführten Datenbankoperation nachweisen.
  Eine simulierte Verbindung reicht dafür nicht aus. (US2.1)
- **FR-004**: Fehlende Konfiguration, Verbindungs- und Anmeldefehler MÜSSEN
  verständlich erkennbar sein. Verbindungsprüfungen MÜSSEN nach einer
  dokumentierten endlichen Wartezeit fehlschlagen können und dürfen dabei
  keine Secrets offenlegen. (US2.2–3; EC-03)
- **FR-005**: Entwicklungs- und Testdaten MÜSSEN getrennt konfiguriert sein.
  Datenbanktests und deren Vorbereitung DÜRFEN nur die ausdrücklich
  ausgewiesene Testdatenbank verändern. (US2.4; EC-07)
- **FR-006**: Eine leere Testdatenbank MUSS über einen dokumentierten
  Migrationsablauf einen eindeutig nachvollziehbaren Baselinestand erreichen.
  (US3.1)
- **FR-007**: Ein erneuter Migrationslauf auf dem Baselinestand MUSS diesen
  Stand und vorhandene Daten erhalten, ohne migrationsbedingte Duplikate
  zu erzeugen. (US3.2; EC-04)
- **FR-008**: Fehlgeschlagene Migrationen MÜSSEN als Fehler erkennbar sein.
  Die Dokumentation MUSS Diagnose und sicheren Wiederanlauf beschreiben;
  ein Fehlschlag DARF nicht als erfolgreiche Anwendung gelten.
  (US3.3; EC-06)
- **FR-009**: `python scripts/check.py` MUSS die relevanten bestehenden
  Prüfungen sowie automatisierte Backend-, echte Datenbank- und Migrationstests
  ausführen. Ein erforderlicher fehlgeschlagener oder nicht ausgeführter
  Test verhindert einen vollständig erfolgreichen Gesamtprüflauf. (US4.1–2; EC-05)
- **FR-010**: Bewusst gewählte Teilprüfungen MÜSSEN ihren Umfang und
  nicht ausgeführte Bestandteile erkennen lassen. Sie ersetzen die
  vollständige Prüfung zur Feature-Abnahme nicht. (US4.3; EC-05)
- **FR-011**: Die Entwicklungsanleitung im DV-Konzept MUSS Voraussetzungen,
  Konfiguration, Einrichtung, Start/Stopp, Health-Aufruf, Datenbankprüfung,
  Migrationen und Fehlerdiagnose für den unterstützten Entwicklungsweg
  enthalten. README und Quickstart verweisen auf diese Anleitung. (US1–4)
- **FR-012**: Ein manueller Start-, Health- und Datenbanknachweis MUSS vor
  Abschluss des Features mit Umgebung, Schritten, Soll-/Ist-Ergebnissen
  und Einschränkungen dokumentiert werden. (US4.4)
- **FR-013**: Metadaten, neu benötigte Verzeichnisse, Entwicklungs- und
  CI-Konfiguration MÜSSEN dem implementierten Projektstand entsprechen.
  Die CI MUSS die neuen automatisierten Prüfungen mit einer getrennten
  Testdatenbank ausführen können. Ein nicht ausgeführter CI-Lauf bleibt
  als solcher dokumentiert. (US4; A-04)
- **FR-014**: Bestehende lokale Konfigurationen und Benutzeränderungen
  MÜSSEN bei Einrichtung und Wiederholung erhalten bleiben. Reale
  Zugangsdaten DÜRFEN weder in Git noch in Prüfausgaben gelangen.
  (US1.2, US2.3; EC-03, EC-04)

### Key Entities

- **Entwicklungs-/Testkonfiguration**: Benennt die jeweilige Umgebung und
  ihre Verbindungsparameter. Sensible Werte bleiben außerhalb versionierter
  Projektdateien.
- **Migrationsstand**: Kennzeichnet nachvollziehbar die angewendete Baseline;
  wiederholte Anwendung verändert einen bereits erreichten Stand nicht.
- **Prüfergebnis**: Ordnet einem konkreten Prüfablauf Umgebung und Ergebnis
  erfolgreich, fehlgeschlagen oder nicht ausgeführt zu.
- **Manueller Abnahmenachweis**: Hält den tatsächlich gestarteten Stand,
  die ausgeführten Schritte, Soll-/Ist-Ergebnisse und Einschränkungen fest.

Fachliche Benutzer-, Profil- und Trainingsentitäten werden erst in den
zugehörigen Folgefeatures modelliert.

## Success Criteria

- **SC-001**: Ein Entwickler kann in einer frischen unterstützten Umgebung
  anhand der dokumentierten Schritte den laufenden Dienst nachweisen
  und den Nachweis nach einem Stopp/Neustart wiederholen, ohne Quellcode
  oder bestehende Daten manuell anzupassen. (US1; FR-001–002, FR-011)
- **SC-002**: Alle vier dokumentierten Verbindungsfälle — korrekt eingerichtet,
  falsche Zugangsdaten, fehlende Konfiguration, Ziel nicht erreichbar —
  liefern das erwartete eindeutige Ergebnis; kein Fehlerfall wird als
  erfolgreicher Zugriff ausgewiesen. (US2; FR-003–005)
- **SC-003**: Der dokumentierte Initialisierungslauf bringt zwei unabhängig
  vorbereitete leere Testbestände auf denselben erkennbaren Ausgangsstand.
  Eine Wiederholung auf einem bestehenden Stand verändert weder diesen
  noch vorhandene Prüfdaten. (US3; FR-006–008)
- **SC-004**: Der vollständige Prüflauf weist für alle Pflichtprüfungen
  tatsächlich erfolgreiche Ausführungen nach. Ein gezielt herbeigeführter
  Verbindungsfehler führt zu einem erfolglosen Gesamtprüflauf; eine
  Teilprüfung bleibt als unvollständiger Nachweis erkennbar.
  (US4; FR-009–010, FR-013)
- **SC-005**: Ein Reviewer kann aus Anleitung und Prüfprotokoll alle sechs
  Abnahmekriterien des ersten Arbeitspakets im DV-Konzept nachvollziehen,
  einschließlich manueller Ergebnisse und nicht ausgeführter Prüfungen.
  (US1–4; FR-011–014)

## Quellen und Dokumentation

- [DV-Konzept: erster Funktionsumfang](../../docs/DV_KONZEPT.md#erster-funktionsumfang):
  Umfang und sechs vorgeschlagene Abnahmekriterien, die dieses Feature konkretisiert.
- [DV-Konzept: Zielarchitektur](../../docs/DV_KONZEPT.md#architektur) und
  [Teststrategie](../../docs/DV_KONZEPT.md#teststrategie-und-gemeinsame-prüfungen):
  bestehende Projektvorgaben.
- [Sport-App-Rohkonzept](../../docs/raw-materials/sport_app_gesamtkonzept_implementierungsleitfaden.md),
  Abschnitte 23–26: kleine Arbeitspakete, Phasen 0/1 und Prüfungen.
- [Constitution](../../.specify/memory/constitution.md):
  Konsistenz, reale Prüfnachweise und Schutz bestehender Daten.
- **Offene fachliche Fragen**: Keine für den abgegrenzten Umfang.
  Annahmen A-01 bis A-06 gelten als Ausgangspunkt.
- **Technische Entscheidungen**: O-01 für den Backend-Umfang und O-03 aus dem
  [DV-Konzept](../../docs/DV_KONZEPT.md#offene-entscheidungen) sind seit 2026-09-18
  im [technischen Plan](plan.md) und seinen Verträgen entschieden. Dazu gehören
  Zielumgebung, Struktur, Versionsbindung, Migrationswerkzeug, genaue
  Statusantwort sowie Diagnose- und Wartezeitkonfiguration.
  Die Trennung zwischen Backend-Status und Datenbanknachweis ist durch diese
  Spec vorgegeben. O-02 und die späteren fachlichen Entscheidungen bleiben
  den Folgefeatures zugeordnet.

### Zuordnung der übernommenen Abnahmekriterien

| Kriterium im DV-Konzept | Konkretisierung in dieser Spec |
| --- | --- |
| 1 – Frische Umgebung startet Backend und Datenbank | US1, US2; FR-001, FR-003–005, FR-011; SC-001–002 |
| 2 – Health liefert HTTP 200; separater Datenbanknachweis | US1.1, US1.3, US2.1; FR-002–003; SC-001–002 |
| 3 – Echte Testdatenbank und erkennbarer Verbindungsfehler | US2; FR-003–005; SC-002 |
| 4 – Baseline auf leerer Datenbank und unschädliche Wiederholung | US3; FR-006–008; SC-003 |
| 5 – Gemeinsame Prüfung und sichtbare Auslassungen | US4.1–3; FR-009–010, FR-013; SC-004 |
| 6 – Manueller Start-/Health-Test dokumentiert | US4.4; FR-011–012; SC-005 |

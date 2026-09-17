# Projekt-Constitution

Version: 1.0.0 | Beschlossen: 2026-09-16

## I. Anforderungen und überprüfbare Ergebnisse

Verhaltensänderungen beginnen mit einem abgegrenzten Feature unter `specs/`.
Spezifikation, Plan und Aufgaben beschreiben denselben Umfang. Akzeptanzkriterien
sind überprüfbar; relevante Tests und der tatsächliche Prüfstatus gehören zum
Abschluss. Kleine Korrekturen werden ihrem Risiko angemessen behandelt.

## II. Ein verbindliches DV-Konzept

`docs/DV_KONZEPT.md` enthält Projektziel, Architektur, Entwicklung und Betrieb.
README und Quickstart dienen dem Einstieg und verlinken die maßgeblichen
Abschnitte. Feature-Artefakte und Entscheidungsprotokolle dürfen auf das Konzept
verweisen, ersetzen es aber nicht. Verhaltensänderungen aktualisieren betroffene
Konzeptabschnitte gemeinsam mit dem Code.

## III. Technologie nach Bedarf

Die Struktur folgt dem gewählten Ökosystem. Dienste und Abhängigkeiten werden
nur für einen begründeten Bedarf aufgenommen. Entwicklungsdienste und
Produktionsbetrieb besitzen getrennte Konfigurationen.

## IV. Verträge und Daten

Öffentliche Verträge, Implementierung und relevante Vertragstests bleiben
konsistent. Datenänderungen berücksichtigen Migration, Prüfung, Backup und
Rückweg. Testinitialisierung ist kein Produktionsmigrationsverfahren.

## V. Reproduzierbare und begrenzte Zugriffe

Werkzeug- und Modulversionen werden festgehalten. Fremde Referenz-Repositories
sind nur lesbar; Beiträge entstehen in separaten Arbeitsklonen. Secrets,
Laufprotokolle und persistente Dienstdaten gehören nicht in Git.

## VI. Wiederverwendbares Wissen

Projektspezifische Informationen bleiben im DV-Konzept. Allgemeines Wissen
geht als geprüfter Änderungsvorschlag an die Knowledge Base; wiederverwendbare
Dateien und Abläufe an das Template.

## Änderungen

Änderungen dieser Prinzipien werden begründet und versioniert. Abhängige
Vorlagen und das DV-Konzept werden auf Widersprüche geprüft. Eine generierte
Checkliste oder ein grüner Agentenbericht ersetzt keine ausgeführten Tests.

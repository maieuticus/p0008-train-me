# Ergänzende Prinzipien für API-Service-Projekte

Diese Prinzipien ergänzt der Generator zur Projekt-Constitution.

## API-Vertrag und Implementierung

Öffentliche Operationen, Schemas und ihre Implementierung werden gemeinsam
geändert und automatisiert verglichen. Interne Referenzen im Vertrag müssen
auflösbar sein. Ein reiner YAML- oder JSON-Syntaxtest genügt nicht.

## Daten und externe Verbraucher

Vor der Umsetzung werden Kompatibilität, Datenmigration, Validierung,
Testfälle, externe Verbraucher, Release und Rückweg geplant.
Testinitialisierung ist kein Verfahren zur Aktualisierung produktiver Daten.

## Eine verbindliche Projektbeschreibung

Projektziel, Architektur, Entwicklung und Betrieb stehen zusammen in
`docs/DV_KONZEPT.md`. Bei Änderungen an Schnittstellen, Daten oder Infrastruktur
werden die betroffenen Abschnitte mit aktualisiert.

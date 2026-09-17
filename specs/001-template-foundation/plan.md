# Plan

Der gemeinsame Kern bleibt im Repository-Root. Profile und Dienste liefern
explizit ausgewählte Dateien und Konfigurationsfragmente. Ein Python-Generator
verwendet PyYAML und erstellt ausschließlich neue oder leere Zielverzeichnisse.

Die bisherige API-Sammlung wird als Rezept integriert. Das Boardgame-Beispiel
und die vorhandene Sport-App-Unterlage bleiben als Rohmaterialien erhalten und
werden nicht weitervererbt. Das DV-Konzept enthält die gesamte Projektbeschreibung.

Hostlokale Pfade liegen in ignorierten Dateien. Ein Read-only-Bind-Mount trennt
Referenzen vom schreibbaren aktuellen Projekt. Beiträge benötigen eigene Klone.
Ein Host-Docker-Socket wird nicht eingebunden.

Prüfung: Generator- und Zugriffstests, Dokumentlinks, Python-/YAML-/JSON-Syntax,
erzeugte Python-/API-Tests, TypeScript-/Maven-CI sowie Compose-Validierung und
Containerbau in einer Umgebung mit Docker.

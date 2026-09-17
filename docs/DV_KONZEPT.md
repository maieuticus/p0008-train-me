# DV-Konzept: template-spec-kit

**Stand:** 16.09.2026
**Status:** Projektgrundgerüst mit optionalen Technologie- und Dienstbausteinen

Dieses Dokument ist die verbindliche Beschreibung von Projektziel, Architektur,
Entwicklung und Betrieb. README, Quickstart und Verzeichnisübersichten verlinken
hierher. Getrennte Dateien für Vision, Architektur, Entwicklung oder Betrieb
werden nicht gepflegt.

## Inhalt

- [Projektziel](#projektziel)
- [Architektur](#architektur)
- [Einrichtung](#einrichtung)
- [Entwicklung](#entwicklung)
- [Betrieb](#betrieb)
- [Wissensaustausch](#wissensaustausch)
- [Weiterentwicklung und Versionen](#weiterentwicklung-und-versionen)
- [Prüfstatus](#prüfstatus)
- [Quellen](#quellen)

## Projektziel

Das Repository liefert einen wiederverwendbaren Grundaufbau für unterschiedliche
Softwareprojekte. Der gemeinsame Kern umfasst Spec-Driven Development,
Dokumentation, Arbeitsregeln, einen Devcontainer und Prüfungen. Technologien
und Infrastruktur werden nach Bedarf ergänzt.

Zielgruppe sind Entwickler und Coding-Agenten, die Projekte nachvollziehbar von
der Anforderung bis zur geprüften Implementierung bearbeiten und Erfahrungen
anschließend an Template und Knowledge Base zurückgeben.

Der Generator unterstützt einen neutralen Kern, Python, TypeScript und
Java/Maven. PostgreSQL, Keycloak und Observability sind unabhängig auswählbar.
Das API-Rezept kombiniert Python, FastAPI und PostgreSQL. Fachliche Funktionen,
produktive Zugangsdaten und ein fertiges Produktionsdeployment sind nicht Teil
des Grundgerüsts.

Mobile Frameworks können als weitere Profile ergänzt werden. Native
Plattformwerkzeuge bleiben eine zusätzliche Voraussetzung; iOS benötigt
insbesondere die Apple-Entwicklungsumgebung.

## Architektur

```text
.devcontainer/   Entwicklungsumgebung und lokale Dienstzusammenschaltung
.github/         GitHub Actions, Issue-/PR-Vorlagen und gewählte Integration
.specify/        Constitution, Vorlagenanpassungen und Entwicklungsworkflow
.vscode/         Gemeinsame Editor-Einstellungen und Prüfaufgabe
config/          Projektmetadaten, Referenz-Repos und Dienstkonfiguration
docs/            DV-Konzept, ursprüngliche Unterlagen und Entscheidungen
specs/           Spezifikation, Plan und Aufgaben je Feature
scripts/         Erzeugung, Einrichtung, Prüfungen und Beitragsvorbereitung
templates/       Technologieprofile, Dienste und zusammengesetzte Rezepte
tests/           Tests des Template-Generators und seiner Zugriffsregeln
```

### Zuständigkeiten und maßgebliche Dateien

| Inhalt | Ablage |
| --- | --- |
| Gemeinsame Prinzipien | `.specify/memory/constitution.md` |
| Projektbeschreibung | Dieses Dokument |
| Konkrete Feature-Anforderung | `specs/<nummer>-<name>/spec.md` |
| Technischer Feature-Plan und Aufgaben | `plan.md` und `tasks.md` im Feature |
| Rohmaterialien | `docs/raw-materials/` |
| Aktive Konfiguration | `config/` und die ausgewählten Werkzeugdateien |
| Lokale Secrets | Ignorierte `.env`, niemals Git |
| Versions- und Profilnachweis | `config/project.yaml` |

`config/project.yaml` und `config/repositories.yaml` sind Konventionen dieses
Templates. Spec Kit wertet sie nicht selbst aus. Die Integrationsmetadaten
unter `.specify/integration.json` und `.specify/integrations/` erzeugt dagegen
die Specify CLI bei der Initialisierung. Sie werden nicht von Hand erfunden.

### Bausteine

Der Generator kopiert einen ausdrücklich festgelegten Kern und ausgewählte
`files/`-Verzeichnisse. `module.yaml` ergänzt Prüfkommandos, Laufzeiten,
Umgebungsvariablen und Ports. Dienstbausteine liefern Compose-Fragmente.
`.template`-Dateien werden beim Kopieren umbenannt und Platzhalter ersetzt.

Das Ziel muss leer sein. Der Generator überschreibt keine bestehenden
Projektdateien und führt weder Installation noch Git-Initialisierung, Push,
Issue-Erstellung oder Spec-Kit-Initialisierung aus.

Der Anwendungscode folgt dem Profil: Python `src/app/` und `tests/`,
TypeScript `src/` und `tests/`, Maven `src/main/java/` und `src/test/java/`.
`.mvn/` und Maven Wrapper werden erst bei Bedarf im Java-Projekt ergänzt.
Ein Monorepo kann stattdessen `apps/` und `packages/` verwenden.

### Devcontainer und Dienste

Der Container startet über `.devcontainer/compose.yaml`. Das Python-Basisimage
stellt die gemeinsamen Werkzeuge bereit; Features ergänzen Node oder Java nur
im gewählten Profil. Die Specify CLI ist auf 1.0.7 festgelegt.

PostgreSQL, Keycloak, Prometheus und Grafana laufen bei Auswahl als separate
Container. Die ausgewählten Services stehen ausdrücklich in `runServices`.
Persistente Daten liegen in benannten Volumes. Entwicklungsdienste veröffentlichen
keine Host-Ports; benötigte Oberflächen werden über VS Code weitergeleitet.

Keycloak verwendet ausschließlich den Entwicklungsmodus. Das mitgelieferte
Realm enthält noch keine Anwendungsclients oder Benutzer. Das Grafana-Dashboard
zeigt zunächst die Erreichbarkeit der Prometheus-Ziele; Anwendungsmetriken
werden bei einem entsprechenden Feature ergänzt.

Grafana-Dashboards und Provisionierung liegen im erzeugten Projekt unter
`config/observability/`. Anwendungsmigrationen gehören nach `db/migrations/`,
Produktionsartefakte nach `deploy/`.

## Einrichtung

### Voraussetzungen

- Python ab 3.11 für Generator und gemeinsame Prüfungen.
- Git; für GitHub-Aktionen zusätzlich die GitHub CLI und eine Anmeldung.
- Für Container: Docker mit Compose und eine Dev-Containers-fähige Umgebung.
- Für lokale Referenzen: ein vorhandenes Verzeichnis mit den anderen Repositories.

Im Template-Verzeichnis:

```sh
python -m pip install -r scripts/requirements.txt
python scripts/create_project.py --help
```

### Neues Projekt erzeugen

```sh
python scripts/create_project.py --name mein-projekt --stack python --output ../mein-projekt
python scripts/create_project.py --name meine-api --recipe api-service --service observability --output ../meine-api
```

Weitere Profile: `--stack typescript`, `--stack java-maven` oder `--stack none`.
Dienste werden mit wiederholtem `--service postgres`, `--service keycloak` und
`--service observability` ausgewählt. `--dry-run` zeigt die geplanten Dateien.

Das erzeugte Projekt enthält seinen eigenen Einstieg und sein DV-Konzept.
Template-Katalog, Generator-Tests und hiesige Rohmaterialien werden nicht
übernommen. So fließt das Sport-App-Konzept nicht in fachfremde Projekte ein.

Bei Verwendung von GitHubs „Use this template“ zunächst die neue Kopie als
Generator öffnen und das ausgewählte Projekt in ein leeres Ziel ausgeben.
Ein Umbau eines bereits gefüllten Arbeitsverzeichnisses wird bewusst nicht
automatisch durchgeführt.

### Lokaler Container und Referenz-Repositories

Im zu öffnenden Projekt unter Windows:

```powershell
python scripts/container_init.py --references-root C:\Git
```

Unter Linux/macOS entsprechend:

```sh
python scripts/container_init.py --references-root /pfad/zu/repos
```

Danach „Reopen in Container“ in VS Code ausführen. Das Startskript erstellt
`.env` nur, wenn sie fehlt, und ersetzt `__GENERATE__` durch zufällige lokale
Passwörter. Bestehende Werte werden erhalten.

`.devcontainer/local.json` merkt sich den Hostpfad; das ignorierte
`compose.local.yaml` bindet ihn unter `/references/repos` mit `read_only: true`
ein. Alternativ setzt der Host `REFERENCE_REPOS_ROOT`. Keine Zugangsdaten in
diese Pfadkonfiguration schreiben.

Das aktuelle Projekt ist separat unter `/workspaces/project` schreibbar.
Der Referenz-Mount schützt die anderen Hostdateien vor Änderungen. Er erlaubt
weiterhin Lesen: Für einen bereinigten Kontext kann statt des gesamten
Arbeitsverzeichnisses eine Sammlung von Referenzklonen ohne lokale Secrets
eingebunden werden.

Der Container erhält keinen Host-Docker-Socket. Compose-Start und Verwaltung
der Nachbardienste erfolgen auf dem Host.

### Codespaces

Codespaces kann `C:\Git` nicht mounten. Dort keinen lokalen Referenzpfad setzen.
Die Konfiguration fordert für `maieuticus/*` nur `contents: read` und
`issues: write` an. Das aktuelle Arbeitsrepository hat seine eigenen Rechte.
Beim Wechsel des GitHub-Owners sowohl `config/repositories.yaml` als auch
`customizations.codespaces.repositories` anpassen.

Andere Repositories können im Codespace über `gh repo view OWNER/REPO` gelesen
oder in ein separates Referenzverzeichnis geklont werden. Der Token beschränkt
Schreibzugriffe auf die Remotes; solche lokalen Klone sind dadurch noch kein
schreibgeschützter Dateisystem-Mount. Für lokale Devcontainer müssen GitHub-
Zugangsdaten separat mit entsprechend begrenztem Umfang eingerichtet werden;
die Codespaces-Einstellungen beschränken keine weitergereichten Host-Tokens.

### Spec Kit initialisieren

Im Container ist die festgelegte CLI installiert. Außerhalb kann `uvx` verwendet
oder `python -m pip install specify-cli==1.0.7` ausgeführt werden.

```sh
python scripts/init_speckit.py --integration copilot
```

Das Skript initialisiert die gewählte Integration, lässt die Constitution
unverändert und verwendet die Bash-Skripte für die Arbeit im Linux-Container.
Andere unterstützte Integrationen können über `--integration` ausgewählt werden.
Die konkreten Agent-Dateien und Manifeste erzeugt Spec Kit.

Die lokalen Vorlagenanpassungen bleiben unter `.specify/templates/overrides/`.
Bei bereits initialisierten Projekten das Updateverfahren verwenden, nicht
erneut blind initialisieren.

## Entwicklung

### Ablauf je Feature

1. Rohmaterial und relevantes Wissen lesen; Projektziel im DV-Konzept klären.
2. Ein abgegrenztes Feature mit Akzeptanzkriterien spezifizieren.
3. Unklare Anforderungen klären und die technische Umsetzung planen.
4. Aufgaben aus Plan und Spec ableiten; Konsistenz prüfen.
5. Implementieren und relevante Tests ausführen.
6. Ergebnis gegen die Akzeptanzkriterien prüfen; Lücken nacharbeiten.
7. Betroffene Abschnitte dieses Konzepts aktualisieren und den Diff prüfen.

Der lokale Workflow liegt unter
`.specify/workflows/project-sdd/workflow.yml`:

```sh
specify workflow run .specify/workflows/project-sdd/workflow.yml -i spec="Ein abgegrenztes Feature"
```

Vor dem automatisierten Lauf müssen fachliche Unklarheiten geklärt sein.
`converge` kann weitere Aufgaben erzeugen. Der abschließende Review prüft diese
Aufgaben; ein durchgelaufener Workflow allein bedeutet keine fachliche Abnahme.
Bei Lücken Implementierung, Prüfungen und Abgleich wiederholen.

### Gemeinsame Prüfungen

```sh
python scripts/check.py
python scripts/check.py --static-only
```

Das Skript prüft lokale Dokumentlinks, Anker, Python-/JSON-/YAML-Syntax und
unzulässige parallele Konzeptdokumente. Danach führt es die Argumentlisten aus
`config/project.yaml` ohne Shell aus. Im Template sind das die Generator-Tests,
im erzeugten Projekt die jeweiligen Anwendungstests.

Die CI prüft zusätzlich generierte Python-, TypeScript-, Maven- und API-Projekte,
Compose-Konfigurationen sowie den Bau der Entwicklungsimages. API-CI verwendet
eine wegwerfbare PostgreSQL-Datenbank und übernimmt ihre Werte aus genau einer
`.env.test.example`. Ein nicht ausgeführter Containerstart darf nicht als
erfolgreich geprüft dokumentiert werden.

### API-Rezept

Das Rezept enthält eine minimale `/health`-Route, einen eingecheckten OpenAPI-
Vertrag und Tests für Vertrag/Implementierung und interne Referenzen.
`/health` ist ein Liveness-Check, kein Nachweis der Datenbankbereitschaft.
Ein eigener Datenbanktest läuft mit `RUN_DATABASE_TESTS=1`; sonst wird er
sichtbar übersprungen.

API-Änderungen planen Vertrag, Verbraucher, Validierung und Fehlerfälle.
Datenänderungen planen Migration, Backup und Rückweg. Nach dem ersten
Abhängigkeitsabgleich einen geeigneten Lock-/Constraint-Stand festhalten.

## Betrieb

### Lokale Entwicklungsdienste

Nach `python scripts/container_init.py` auf dem Docker-Host:

```sh
docker compose -f .devcontainer/compose.yaml -f .devcontainer/compose.local.yaml config --quiet
docker compose -f .devcontainer/compose.yaml -f .devcontainer/compose.local.yaml ps
docker compose -f .devcontainer/compose.yaml -f .devcontainer/compose.local.yaml logs --tail 100
docker compose -f .devcontainer/compose.yaml -f .devcontainer/compose.local.yaml down
```

`down` erhält die benannten Volumes. `down --volumes` löscht Dienstdaten und
gehört nicht zum normalen Arbeitsablauf.

### Deployment und Datenänderungen

Das Template selbst wird nicht produktiv betrieben. Erzeugte Anwendungen
ergänzen hier ihre konkreten Bereitstellungsschritte, Umgebungen,
Verantwortlichkeiten, Backups und Wiederherstellungsverfahren.

Das API-Rezept enthält einen Anwendungs-Dockerfile unter `deploy/`.
Entwicklungs-Keycloak, Testpasswörter und lokale Compose-Dienste sind keine
Produktionskonfiguration.

Vor einer Schemaänderung werden Datenmodell, Migration, Tests und Rückweg
gemeinsam geplant. Das ergänzende SQL-Skript des API-Katalogs setzt idempotente
Migrationen voraus; alternativ ein passendes Migrationswerkzeug wählen.
`db/init.sql` darf nur eine frische Testdatenbank initialisieren und ist kein
Produktionsmigrationsverfahren. Ein Backup liegt außerhalb des Git-Verzeichnisses.

### Störungen

| Symptom | Prüfung |
| --- | --- |
| Containerstart meldet fehlendes Override | `python scripts/container_init.py` auf dem Host ausführen |
| Referenzordner fehlt | Hostpfad, `local.json` und `REFERENCE_REPOS_ROOT` prüfen |
| PostgreSQL lehnt Anmeldung ab | Vorhandene Volume-Daten und tatsächliche `.env` vergleichen; neue Env-Werte ändern vorhandene DB-Benutzer nicht automatisch |
| API-Vertragstest schlägt fehl | Beabsichtigte Vertragsänderung prüfen; Implementierung und Vertrag gemeinsam aktualisieren |
| Agent-Aufruf fehlt | Installierte Integration und deren Aufrufsyntax prüfen |

## Wissensaustausch

| Ergebnis | Ziel |
| --- | --- |
| Projektarchitektur und Betrieb | Dieses DV-Konzept |
| Allgemeines Technologiewissen | `tech-knowledge-base` |
| Gemeinsame Infrastrukturkenntnisse | Infrastrukturartikel der Knowledge Base |
| Wiederverwendbare Dateien und Abläufe | `template-spec-kit` |

Die Knowledge Base verwendet `tNNNN-…` für Technologien und `iNNNN-…` für
Infrastruktur. Zuerst bestehende Artikel und ihre `AGENTS.md` lesen. Wissen
bevorzugt verlinken; relevante Versionen bei Architekturentscheidungen festhalten.

Ein Verbesserungs-Issue kann bei vorhandenem Auftrag über die GitHub CLI im
ausdrücklich genannten Repository erstellt werden. Dafür ist kein
`contents: write` erforderlich.

Für eine konkrete Dateiänderung:

```sh
python scripts/prepare_contribution.py knowledge --output .artifacts/contributions/knowledge --branch improve/postgres-notes
```

Das Skript klont ausschließlich das konfigurierte Ziel und erstellt einen
Arbeitsbranch. Es veröffentlicht nichts. Nach Prüfung kann der Branch mit
gezielten Rechten in das Ziel oder einen geeigneten Fork gepusht und ein PR
erstellt werden. `pull_requests: write` allein erlaubt keinen Branch-Push.
Die Referenzkopie bleibt unverändert.

## Weiterentwicklung und Versionen

Template-Version und verwendete Spec-Kit-Version stehen in `config/project.yaml`.
Neue Projekte erhalten zusätzlich den Ausgangscommit; `+working-tree` kennzeichnet
eine Erzeugung aus noch nicht vollständig eingecheckten Änderungen.

Template-Updates werden als gezielte Änderungen geprüft. Der Generator ist kein
Synchronisationswerkzeug für bestehende Anwendungen. Spec-Kit-Updates zunächst
an einem Testprojekt prüfen; bei bestehenden Integrationen den
manifestgestützten `specify integration upgrade`-Weg verwenden.

Neu ausgewählte Dienste erst nach Konfigurations- und Startprüfung in den
Katalog aufnehmen. Projektanforderungen, aktive Konfiguration und dieses
Dokument bei Änderungen zusammenführen.

## Prüfstatus

Stand der lokalen Überprüfung am 16.09.2026:

| Prüfung | Ergebnis |
| --- | --- |
| Dokumentlinks, Anker und Python-/JSON-/YAML-Syntax | Erfolgreich |
| Neun Generator- und Containerkonfigurationstests | Erfolgreich |
| Erzeugtes Python-Projekt: Paketbau, Installation und Importtest | Erfolgreich |
| Erzeugtes TypeScript-Projekt: Installation, Typprüfung und Node-Test | Erfolgreich |
| Erzeugtes API-Projekt: Paketbau und API-/Vertragstests | Vier Tests erfolgreich |
| API-Datenbanktest | Übersprungen; keine laufende PostgreSQL-Testinstanz |
| Maven-Build | Lokal nicht ausgeführt; JDK/Maven fehlen |
| Compose-Schema, Image-Bau und Dienststart | Lokal nicht ausgeführt; Docker fehlt |
| Spec-Kit-Initialisierung und Workflow-Validierung | CLI-Start durch Windows-Anwendungssteuerung blockiert |
| GitHub Actions | Konfiguriert, in dieser Sitzung nicht ausgeführt |

Die noch offenen Laufzeitprüfungen sind in der CI hinterlegt. Syntaxprüfungen
und Konfigurationstests ersetzen keinen erfolgreichen Containerstart.

## Quellen

- [Spec-Kit-Anpassungen](https://github.github.io/spec-kit/guides/customization.html)
- [Spec-Kit-Workflows](https://github.github.io/spec-kit/reference/workflows.html)
- [Spec-Kit-Integrationen](https://github.github.io/spec-kit/reference/integrations.html)
- [Spec Kit 1.0.7](https://github.com/github/spec-kit/releases/tag/v1.0.7)
- [Docker-Bind-Mounts](https://docs.docker.com/engine/storage/bind-mounts/)
- [Devcontainer-Mounts und Codespaces](https://code.visualstudio.com/remote/advancedcontainers/add-local-file-mount)
- [Codespaces-Repository-Rechte](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-repository-access-for-your-codespaces)
- [Maven-Projektstruktur](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html)
- [TypeScript in Node.js](https://nodejs.org/api/typescript.html)
- [Keycloak-Container](https://www.keycloak.org/server/containers)
- [Grafana in Docker](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/)

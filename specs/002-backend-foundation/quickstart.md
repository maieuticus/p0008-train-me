# Validierungsleitfaden: Backend-Grundgerüst

**Status:** Geplante Abnahmeszenarien, noch nicht ausführbar umgesetzt.
Die folgenden Befehle bezeichnen das erwartete Ergebnis der Implementierung.
Die verbindliche Projektanleitung bleibt im
[DV-Konzept](../../docs/DV_KONZEPT.md#einrichtung); dieser Leitfaden ordnet
die Nachweise den Anforderungen aus [spec.md](spec.md) zu.

## Voraussetzungen und Einrichtung

Unterstützter Weg: Windows mit PowerShell, Git, Python ab 3.11 für die
Host-Hilfsskripte und laufendem Docker Desktop mit Linux-Containern sowie
Compose v2 mit `up --wait`. Die Anwendung und alle vollständigen Prüfungen
laufen unter Python 3.13 im `dev`-Container. Port 8000 auf localhost ist frei.
Alle Hostbefehle werden im Repository-Root ausgeführt.

Für den späteren Nachweis werden Git-Stand, Host-/Docker-/Compose-Version,
Python-Version im Container und verwendete Image-Digests festgehalten.
Downloads sind bei Einrichtung erlaubt. Keine Produktionsdaten oder externen
Secrets verwenden. Vorhandene lokale `.env`-Werte und Overrides zuerst erhalten.

```powershell
python scripts/backend_init.py
$trainMeComposeArgs = @('--project-name', 'train-me', '--env-file', '.env', '-f', '.devcontainer/compose.yaml', '-f', '.devcontainer/compose.local.yaml')
docker compose @trainMeComposeArgs config --quiet
docker compose @trainMeComposeArgs build dev
docker compose @trainMeComposeArgs up -d --wait
docker compose @trainMeComposeArgs exec -T dev python -m pip install --no-deps --no-build-isolation -e backend
```

Nach jedem Befehl ist der Exitcode zu prüfen; bei Fehlern wird der folgende
Schritt nicht als erfolgreich ausgeführt protokolliert. Erwartet: drei gestartete
Dienste, gesunde DB-Dienste, korrekt installiertes lokales Backend-Paket. Der
Image-Build installiert die gebundenen Runtime-/Test-/Build-Abhängigkeiten.
Eine Wiederholung verändert keine vorhandenen Passwörter/Overrides und löscht
keine Entwicklungsdaten. `config --quiet` zeigt keine expandierten Secrets.

## V-01: Start, Health und Neustart (US1, SC-001)

In einem eigenen Host-Terminal Uvicorn starten (Compose-Argumente wie oben):

```powershell
docker compose @trainMeComposeArgs exec dev python -m uvicorn train_me_backend.main:create_app --factory --host 0.0.0.0 --port 8000
```

In einem zweiten PowerShell-Terminal, ebenfalls vom Repository-Root:

```powershell
$trainMeHealth = Invoke-WebRequest http://127.0.0.1:8000/health -UseBasicParsing
$trainMeHealth.StatusCode
$trainMeHealth.Content
```

Erwartet: HTTP 200 und exakt das JSON-Objekt `{"status":"ok"}` gemäß
[HTTP-Vertrag](contracts/health.openapi.yaml). Die Uvicorn-Konsole beenden,
denselben Start wiederholen und erneut Health prüfen. Optionaler Portkonflikt
führt zu einem fehlgeschlagenen Start mit verständlicher Meldung.

## V-02: Datenbanknachweis und Baseline (US2–3, SC-002–003)

```powershell
docker compose @trainMeComposeArgs exec -T dev python -m train_me_backend.db check --target development
docker compose @trainMeComposeArgs exec -T dev python -m train_me_backend.db current --target development
docker compose @trainMeComposeArgs exec -T dev python -m train_me_backend.db upgrade --target development
docker compose @trainMeComposeArgs exec -T dev python -m train_me_backend.db current --target development
docker compose @trainMeComposeArgs exec -T dev python -m train_me_backend.db upgrade --target development
docker compose @trainMeComposeArgs exec -T dev python -m train_me_backend.db check --target test
```

Erwartet: tatsächlicher Zugriff, `revision=none` vor der ersten Migration,
anschließend `revision=0001_baseline`; Wiederholung ändert den Stand nicht.
Die Zwei-Leerbestände-/Sentinel-/Rollback-Nachweise finden ausschließlich in
der automatisierten Testdatenbank statt. Vorhandene Entwicklungsdaten werden
nicht für diesen Test bereinigt.

## V-03: Datenbankausfall bei laufendem Backend (US1.3, EC-02)

Uvicorn läuft weiterhin. Aus einem Host-Terminal:

```powershell
docker compose @trainMeComposeArgs stop postgres
Invoke-WebRequest http://127.0.0.1:8000/health -UseBasicParsing
docker compose @trainMeComposeArgs exec -T dev python -m train_me_backend.db check --target development
docker compose @trainMeComposeArgs up -d --wait postgres
docker compose @trainMeComposeArgs exec -T dev python -m train_me_backend.db check --target development
```

Erwartet: Health bleibt 200. Die erste DB-Prüfung schlägt innerhalb des
dokumentierten Budgets fehl; nach Wiederherstellung gelingt sie. In diesem
Szenario ist der erste Fehler beabsichtigt und ausdrücklich zu protokollieren.
Die Dienstunterbrechung darf keine Volume-Löschung auslösen.

## V-04: Vollständige und unvollständige Prüfung (US4, SC-004)

```powershell
docker compose @trainMeComposeArgs exec -T dev python scripts/check.py
docker compose @trainMeComposeArgs exec -T dev python scripts/check.py --static-only
docker compose @trainMeComposeArgs stop postgres-test
docker compose @trainMeComposeArgs exec -T dev python scripts/check.py
docker compose @trainMeComposeArgs up -d --wait postgres-test
docker compose @trainMeComposeArgs exec -T dev python scripts/check.py
```

Erwartet: erster und letzter vollständiger Lauf führen alle Pflichtgruppen
erfolgreich aus. Der statische Lauf nennt Teilumfang und Auslassungen. Der
Lauf ohne Testdatenbank endet erfolglos; kein Skip darf ihn zu einem vollständigen
Erfolg machen. Die Testinstanz ist flüchtig und darf beim Neustart wieder leer
sein. Das Entwicklungsvolume bleibt erhalten.

Die automatisierten Tests decken zusätzlich ab: falsches Kennwort, fehlende
Pflichtwerte, fehlende DB, hängende Verbindung, verweigertes falsches Reset-Ziel,
zwei leere Baseline-Bestände, unveränderte Sentinel-Daten, fehlschlagende
Testmigration und Geheimwertfreiheit sämtlicher erfasster Ausgaben.
Gezielte Testauswahl ersetzt den vollständigen Aufruf nicht.

## V-05: Aufräumen und Nachweis (FR-012–014, SC-005)

Uvicorn mit Strg+C beenden. Danach auf dem Host:

```powershell
docker compose @trainMeComposeArgs stop
```

`stop` oder später `down` ohne Volumenlöschung erhält die Entwicklungsdaten.
Fehlerdiagnose und Migrationswiederanlauf erfolgen gemäß
[Laufzeitvertrag](contracts/runtime.md); Kennwortkonflikte mit bestehenden
Volumes werden bewusst korrigiert, nicht durch automatisches Löschen.

Im [DV-Prüfstatus](../../docs/DV_KONZEPT.md#prüfstatus) je Szenario festhalten:
Datum, Git-/Umgebungsstand, tatsächlich ausgeführte Schritte, erwartetes und
tatsächliches Ergebnis, Exit-/HTTP-Code, gegebenenfalls Laufzeit und Einschränkung.
CI-Ausführung separat nennen. Codespaces, alternative native Laufzeiten,
NAS-Deployment und mobile Geräte sind durch diese lokale Abnahme nicht geprüft.

Vollständige Abnahme verlangt V-01 bis V-05 und die tatsächlichen automatischen
Pflichtnachweise; dieser Planungsleitfaden allein ist kein Testergebnis.

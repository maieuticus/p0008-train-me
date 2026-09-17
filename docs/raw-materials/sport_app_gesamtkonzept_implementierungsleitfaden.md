# Sport-App – Gesamtkonzept und Implementierungsleitfaden

**Status:** Konzeptstand nach gemeinsamer Abstimmung  
**Ziel:** Master-Konzept und Entwicklungsfahrplan für eine KI-gestützt entwickelte Sport-App  
**Prinzip:** Die App funktioniert im Betrieb ohne KI-Aufrufe. KI wird primär zur Entwicklung, Planung, Pflege und Weiterentwicklung von Übungen und Trainingsplänen eingesetzt.

---

## 1. Zielbild

Die Anwendung ist eine mobile Sport-App für Android und iOS, die mehrere Personenprofile verwalten kann und jeden Nutzer durch individuell geplante Trainingseinheiten führt.

Die App soll:

- mehrere getrennte Personenprofile unterstützen,
- Ziele, Einschränkungen, verfügbares Equipment und Präferenzen je Profil speichern,
- einen strukturierten Übungskatalog verwalten,
- Wochen- und Monatspläne darstellen,
- die jeweils heutige Trainingseinheit anzeigen,
- Übungen mit Animation, Timer, Pausen und Sprachhinweisen begleiten,
- Trainings automatisch und flüssig durchlaufen lassen,
- Trainingsergebnisse und Feedback speichern,
- aus Historie und Feedback später neue Planvorschläge ableiten lassen,
- Trainingsdaten strukturiert für Codex, ChatGPT oder andere Coding-/Planungs-KI exportieren können,
- im MVP selbst keine laufenden KI-Token für den normalen Trainingsbetrieb benötigen.

### Grundprinzip

Die KI ist **nicht Bestandteil des Trainingsplayers zur Laufzeit**.

Stattdessen wird sie verwendet für:

- Entwicklung der App,
- Erstellung neuer Übungen,
- Anpassung vorhandener Übungen,
- Erstellung von Trainingsplänen,
- Analyse von Trainingshistorie und Feedback,
- Vorschläge für die nächste Woche oder den nächsten Monat,
- progressive Anpassung der Belastung,
- Verbesserung der App und des Übungskatalogs.

Die produktive App bleibt auch ohne KI-Verbindung vollständig nutzbar.

---

## 2. Technische Zielarchitektur

### Mobile App

- **React Native**
- **Expo**
- **TypeScript**
- gemeinsame Codebasis für Android und iOS

### Backend

- **Python**
- **FastAPI**
- Betrieb als Docker-Container auf der NAS

### Datenbank

- **PostgreSQL**
- eigener Docker-Container auf der NAS
- Zugriff ausschließlich über FastAPI
- die Mobile App greift niemals direkt auf PostgreSQL zu

### Netzwerkzugriff

Für die private Nutzung wird zunächst **Tailscale** eingesetzt.

Zielbild:

```text
Smartphone / Tablet
        |
        | Tailscale
        v
FastAPI auf der NAS
        |
        v
PostgreSQL
```

Vorteile:

- keine öffentliche Datenbank,
- keine direkte Portfreigabe zum Internet,
- API nur für autorisierte Geräte bzw. Nutzer erreichbar,
- später kann die Zugriffsschicht durch eine öffentliche Lösung ersetzt werden, ohne das Backend grundsätzlich neu zu bauen.

### Medien

- Standardformat für Übungsanimationen: **Lottie / dotLottie**
- MP4 nur als spätere Fallback-Option für Inhalte, die mit Vektoranimationen nicht sinnvoll darstellbar sind
- Medien werden nicht als GIF gespeichert

---

## 3. Benutzer- und Profilmodell

Die App soll mehrere Personen unterstützen.

### Benutzer

Ein Benutzer ist die technische Anmeldung an der App.

Beispiel:

```text
User
- id
- name
- login
- role
- active
```

### Profil

Ein Benutzer kann mindestens ein Trainingsprofil besitzen.

Ein Administrator kann mehrere Profile verwalten.

Beispiel:

```text
Profile
- id
- user_id
- display_name
- age_optional
- training_level
- preferred_training_days
- preferred_training_time
- active
```

### Profilbezogene Informationen

Je Profil werden getrennt gespeichert:

- Trainingsziele
- Einschränkungen
- vorhandenes Equipment
- bevorzugte Trainingszeiten
- bevorzugte Trainingsdauer
- Trainingshistorie
- persönliches Feedback
- aktive Trainingspläne
- vergangene Trainingspläne

Es darf keine Vermischung zwischen verschiedenen Personenprofilen geben.

---

## 4. Ziele, Einschränkungen und Equipment

Diese Informationen dienen als Grundlage für die spätere Trainingsplanung.

### Ziele

Beispiele:

- allgemeine Fitness
- Beweglichkeit
- Muskelaufbau
- Ausdauer
- Rumpfstabilität
- Balance
- bestimmte Muskelgruppen
- Trainingsroutine aufbauen

### Einschränkungen

Einschränkungen werden strukturiert gespeichert.

Beispiele:

- Übung vermeiden
- Körperregion nicht belasten
- Bewegungsrichtung vermeiden
- maximale Belastung
- bestimmte Hilfsmittel erforderlich
- zeitlich begrenzte Einschränkung

Einschränkungen sollen beim AI-Context-Export automatisch mit ausgegeben werden.

### Equipment

Beispiele:

- Trainingsmatte
- Hanteln
- Theraband
- Stuhl
- Fitnessband
- keine Geräte

Der Trainingsplan soll möglichst nur Übungen enthalten, die mit dem für das jeweilige Profil verfügbaren Equipment durchgeführt werden können.

---

## 5. Übungskatalog

Der Übungskatalog ist ein zentraler Bestandteil der Anwendung.

Jede Übung erhält eine eindeutige ID und strukturierte Metadaten.

### Beispielstruktur

```json
{
  "id": "exercise_001",
  "name": "Beispielübung",
  "category": "strength",
  "muscle_groups": ["core"],
  "difficulty": "easy",
  "equipment": ["chair"],
  "execution_type": "duration",
  "default_duration_seconds": 40,
  "default_repetitions": null,
  "default_pause_seconds": 20,
  "animation": {
    "type": "dotlottie",
    "asset": "exercise_001.lottie",
    "loop": true
  },
  "voice_cues": [],
  "instructions": [],
  "common_errors": [],
  "alternatives": [],
  "active": true
}
```

### Zu jeder Übung gehören mindestens

- eindeutige ID,
- Name,
- Kategorie,
- Zielmuskulatur,
- Schwierigkeitsgrad,
- Equipment,
- Dauer oder Wiederholungen,
- Standardpause,
- Animation,
- Sprachhinweise,
- Durchführung,
- typische Fehler,
- Alternativen,
- Aktiv/Inaktiv-Status.

### Neue Übungen

Neue Übungen können später auf zwei Wegen angelegt werden:

1. manuell über eine Verwaltungsfunktion,
2. über einen KI-gestützten Workflow mit festem JSON-Schema.

Die KI soll neue Übungen zunächst immer als **Entwurf** erstellen.

---

## 6. Animationen

Für den MVP wird **Lottie / dotLottie** als Standard festgelegt.

### Anforderungen

- kurze wiederholbare Bewegungsanimation,
- möglichst klarer Bewegungsablauf,
- geringer Speicherbedarf,
- ohne Ton,
- unabhängig von der Sprachausgabe,
- sauber skalierbar auf verschiedene Bildschirmgrößen.

### Dateiorganisation

Beispiel:

```text
media/
└── exercises/
    ├── exercise_001.lottie
    ├── exercise_002.lottie
    └── exercise_003.lottie
```

### KI-Unterstützung

Für neue Übungen kann die KI:

- eine Bewegungsbeschreibung erzeugen,
- ein Storyboard beschreiben,
- Lottie-kompatible Animationsvorgaben vorbereiten,
- vorhandene Animationen anpassen,
- notwendige Assets und Metadaten erzeugen.

Die endgültige Animation sollte vor Freigabe visuell geprüft werden.

---

## 7. Sprachhinweise während des Trainings

Sprachhinweise sind im MVP eine Kernfunktion.

Die Hinweise werden **nicht primär als Text eingeblendet**, sondern gesprochen.

Eine spätere Option zur zusätzlichen Textanzeige kann ergänzt werden, ist aber nicht Bestandteil des MVP.

### Umsetzung

Die Datenbank speichert:

- Übungs-ID,
- Zeitpunkt,
- Text,
- Priorität,
- optionalen Typ.

Beispiel:

```json
{
  "exercise_id": "exercise_001",
  "voice_cues": [
    {
      "at_second": 3,
      "text": "Rücken gerade halten."
    },
    {
      "at_second": 15,
      "text": "Beim Strecken ausatmen."
    },
    {
      "at_second": 30,
      "text": "Noch zehn Sekunden."
    }
  ]
}
```

### Ausgabe

Für den MVP wird die systemeigene **Text-to-Speech-Funktion des Smartphones** genutzt.

Vorteile:

- keine separaten Audiodateien erforderlich,
- keine laufenden KI-Kosten,
- Texte können jederzeit geändert werden,
- Sprachhinweise bleiben mit der Übung synchronisierbar.

---

## 8. Trainingspläne

Die App soll mehrere Wochen- und Monatspläne unterstützen.

Ein Trainingsplan gehört immer zu genau einem Profil.

### Planstruktur

```text
Plan
└── Zeitraum
    └── Woche
        └── Tag
            └── Trainingseinheit
                ├── Übung
                ├── Pause
                ├── Übung
                └── ...
```

### Status

Ein Plan kann beispielsweise folgende Status besitzen:

```text
DRAFT
APPROVED
ACTIVE
ARCHIVED
```

Ein von KI erstellter Plan darf niemals sofort produktiv werden.

Workflow:

```text
KI erstellt Vorschlag
        |
        v
DRAFT
        |
        v
Prüfung
        |
        v
APPROVED
        |
        v
ACTIVE
```

### Planungshorizont

Unterstützt werden sollen mindestens:

- einzelne Tage,
- Wochen,
- mehrere Wochen,
- Monatsplanung.

---

## 9. Trainingsplayer

Der Trainingsplayer ist die zentrale Funktion während einer Trainingseinheit.

### Ziel

Der Nutzer soll nach dem Start möglichst wenig mit dem Smartphone interagieren müssen.

### Ablauf

```text
Training starten
      |
      v
Vorbereitung
      |
      v
Übung
      |
      +--> Animation
      +--> Timer
      +--> Sprachhinweise
      |
      v
Übung abgeschlossen
      |
      v
Pause
      |
      v
Nächste Übung
      |
      v
...
      |
      v
Training abgeschlossen
```

### Standardverhalten

Der Ablauf erfolgt automatisch.

Der Nutzer soll nicht nach jeder Übung bestätigen müssen.

### Bedienelemente

Mindestens:

- Pause / Fortsetzen
- Übung überspringen
- Training abbrechen
- Feedback
- optional Wiederholen

### Anforderungen an den Zustand

Der Player soll seinen Zustand speichern können.

Beispiel:

```text
current_session
current_exercise
remaining_time
paused
completed_exercises
```

Damit kann später entschieden werden, ob eine unterbrochene Session fortgesetzt werden kann.

---

## 10. Feedbacksystem

Das Feedbacksystem wird bewusst in zwei getrennte Bereiche aufgeteilt.

### A. Individuelles Trainingsfeedback

Zweck:

- Anpassung des persönlichen Trainingsplans,
- Erkennung zu leichter oder zu schwerer Übungen,
- Erkennung ungeeigneter Übungen,
- schrittweise Progression.

Mögliche strukturierte Angaben:

- zu leicht
- passend
- zu schwer
- unangenehm
- Beschwerden
- Pause zu kurz
- Pause zu lang
- Training zu kurz
- Training zu lang

Zusätzlich:

- optionaler Freitext
- optionales gesprochenes Feedback

### B. Qualitätsfeedback zur App oder Übung

Zweck:

- Verbesserung der App,
- Verbesserung einer Übung,
- Verbesserung einer Animation,
- Fehlerhinweise,
- Verbesserung der Sprachhinweise.

Dieses Feedback darf nicht automatisch den persönlichen Trainingsplan verändern.

### Bedienung

Der Trainingsfluss soll nicht unterbrochen werden.

Es gibt lediglich einen **Feedback-Button**.

Ohne Betätigung läuft das Training automatisch weiter.

### Spracheingabe

Feedback soll gesprochen werden können.

Workflow:

```text
Feedback-Button
     |
     v
Aufnahme
     |
     v
Speech-to-Text
     |
     v
Text speichern
     |
     v
Training fortsetzen
```

Die Audioaufnahme muss standardmäßig nicht dauerhaft gespeichert werden.

Gespeichert werden soll vorzugsweise die Transkription.

---

## 11. Trainingshistorie und Progression

Nach jeder Trainingseinheit wird gespeichert, was tatsächlich durchgeführt wurde.

### Zu speichern

- Profil
- Trainingsplan
- Session
- Datum/Zeit
- durchgeführte Übungen
- Dauer
- übersprungene Übungen
- Unterbrechungen
- individuelles Feedback
- optionales Freitextfeedback

### Ziel

Die Historie wird später beim Erstellen neuer Trainingspläne berücksichtigt.

Die KI soll erkennen können:

- welche Übungen regelmäßig durchgeführt wurden,
- welche Übungen übersprungen wurden,
- welche Übungen zu schwer waren,
- welche Übungen zu leicht waren,
- ob die Trainingsdauer häufig gekürzt wurde,
- ob bestimmte Übungen wiederholt negatives Feedback erhalten haben.

### Progressive Belastungssteigerung

Wenn ein Training wiederholt gut funktioniert oder zu leicht wird, sollen neue Planvorschläge eine **schrittweise Progression** vorsehen.

Mögliche Progressionsparameter:

- mehr Wiederholungen,
- längere Belastungsdauer,
- leicht kürzere Pausen,
- zusätzliche Sätze,
- schwierigere Übungsvariante,
- moderat höheres Trainingsvolumen.

Wichtig:

- keine großen Sprünge,
- Änderungen sollen nachvollziehbar sein,
- Einschränkungen haben Vorrang,
- negative Rückmeldungen führen eher zu Reduktion oder Alternativen.

---

## 12. AI-Context-Export

Für Codex, ChatGPT, OpenCode oder andere KI-Werkzeuge wird ein standardisiertes Datenpaket erzeugt.

Beispiel:

```text
ai-context/
├── README.md
├── profile.json
├── goals.json
├── constraints.json
├── equipment.json
├── exercises.json
├── current-plan.json
├── training-history.json
└── feedback.json
```

### Ziel

Die KI soll den relevanten Kontext vollständig lesen können, ohne direkten Zugriff auf die Produktionsdatenbank zu benötigen.

### Grundregel

Die KI arbeitet zunächst mit **Exportdaten und Vorschlägen**.

Produktive Daten werden nicht direkt verändert.

---

## 13. KI-Workflow für Trainingsplanung

Beispielworkflow:

```text
Produktive Daten
      |
      v
AI-Context Export
      |
      v
Codex / ChatGPT / OpenCode
      |
      v
Planvorschlag
      |
      v
proposals/
      |
      v
Validierung
      |
      v
Review
      |
      v
Import als DRAFT
      |
      v
Freigabe
      |
      v
ACTIVE
```

### Vorschläge aus Historie und Feedback

Die KI soll auf Wunsch Vorschläge erstellen für:

- nächste Woche,
- mehrere Wochen,
- nächsten Monat.

Dabei werden berücksichtigt:

- Ziele,
- Einschränkungen,
- Equipment,
- Trainingshistorie,
- individuelles Feedback,
- aktuelle Belastung,
- gewünschte Trainingsdauer,
- gewünschte Trainingstage.

### Beispielauftrag an Codex

```text
Lies den Ordner ai-context/.

Erstelle auf Grundlage des aktuellen Profils, der Einschränkungen,
der Trainingshistorie und des Feedbacks einen Vorschlag für die
nächsten vier Wochen.

Regeln:
- nur freigegebene Übungen verwenden,
- Einschränkungen niemals ignorieren,
- Belastung schrittweise steigern,
- mehrfach zu schwere Übungen reduzieren oder ersetzen,
- mehrfach zu leichte Übungen moderat steigern,
- keine produktiven Dateien verändern.

Schreibe den Vorschlag nach:

proposals/plan_next_4_weeks.json
```

---

## 14. Allgemeines Feedback zur Weiterentwicklung

Zusätzlich zum Trainingsfeedback soll es möglich sein, allgemein Feedback zur Anwendung zu sammeln.

Beispiele:

- Navigation unpraktisch,
- Animation missverständlich,
- Sprachhinweis zu früh,
- Übung nicht verständlich,
- Timer schlecht sichtbar,
- fehlende Funktion,
- Fehler in der App.

Dieses Feedback soll separat von den personenbezogenen Trainingsdaten ausgewertet werden können.

---

## 15. API-Grundstruktur

Die genaue API wird erst in der Implementierungsphase finalisiert.

Eine mögliche Ausgangsstruktur:

```text
GET    /health

POST   /auth/login

GET    /profiles
GET    /profiles/{id}
POST   /profiles
PATCH  /profiles/{id}

GET    /exercises
GET    /exercises/{id}
POST   /exercises
PATCH  /exercises/{id}

GET    /plans
GET    /plans/{id}
POST   /plans
PATCH  /plans/{id}

GET    /training/today
POST   /training/{session_id}/start
POST   /training/{session_id}/pause
POST   /training/{session_id}/complete

POST   /feedback/training
POST   /feedback/product

GET    /history
GET    /history/{profile_id}

POST   /ai-context/export
POST   /imports/plan
```

---

## 16. Sicherheits- und Rechtekonzept

### Netzwerkebene

Tailscale schützt den Zugriff auf die private Infrastruktur.

### Anwendungsebene

FastAPI prüft zusätzlich:

- Anmeldung,
- Benutzer,
- Rolle,
- Profilzugriff,
- Berechtigungen.

### Grundsatz

Tailscale allein ersetzt keine Benutzerrechte in der App.

### Beispielrollen

```text
ADMIN
USER
```

**ADMIN**

- Profile verwalten
- Übungen verwalten
- Pläne importieren
- Pläne freigeben
- allgemeines Feedback betrachten

**USER**

- eigenes Profil sehen
- eigenes Training ausführen
- eigenes Feedback geben
- eigene Historie ansehen

---

## 17. Speicherung und Backups

### PostgreSQL

Regelmäßige Datenbanksicherung.

Mindestens:

- automatisches tägliches Backup,
- mehrere Generationen behalten,
- Wiederherstellung testbar machen.

### Medien

Animationsdateien werden auf der NAS gespeichert.

Die Datenbank enthält nur:

- Asset-ID,
- Dateipfad bzw. URL,
- Metadaten.

---

## 18. Datenschutz und Entwicklungsdaten

Persönliche Trainingsinformationen sollen nicht unnötig in Git-Repositories landen.

Für Entwicklung und Tests:

- synthetische Profile,
- Beispieldaten,
- anonymisierte Historien,
- keine realen Zugangsdaten,
- keine API-Keys im Repository.

Secrets werden über Umgebungsvariablen verwaltet.

Beispiel:

```text
.env
.env.local
secrets/
```

Diese Dateien gehören in `.gitignore`.

---

## 19. Repository-Struktur

Vorschlag:

```text
sport-app/
├── README.md
├── AGENTS.md
├── docker-compose.yml
├── .devcontainer/
│   └── devcontainer.json
│
├── app/
│   ├── src/
│   ├── assets/
│   ├── tests/
│   └── package.json
│
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── tests/
│   └── pyproject.toml
│
├── schemas/
│   ├── exercise.schema.json
│   ├── training-plan.schema.json
│   └── ai-context.schema.json
│
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   ├── training-player.md
│   └── ai-workflow.md
│
├── ai-context/
│   └── README.md
│
├── proposals/
│   └── .gitkeep
│
└── examples/
    ├── exercises/
    ├── plans/
    └── profiles/
```

---

## 20. AGENTS.md – Regeln für Coding-Agenten

Im Repository soll eine zentrale `AGENTS.md` hinterlegt werden.

Darin stehen mindestens:

- Architekturprinzipien,
- Coding-Standards,
- Testpflicht,
- Migrationsregeln,
- Sicherheitsregeln,
- Umgang mit Produktivdaten,
- erlaubte Verzeichnisse,
- Regeln für generierte Übungen,
- Regeln für Trainingsplanvorschläge.

Beispielregeln:

```text
1. Bestehende produktive Migrationen niemals verändern.
2. Schemaänderungen benötigen eine neue Migration.
3. KI-generierte Trainingspläne werden immer als DRAFT gespeichert.
4. Einschränkungen eines Profils dürfen nicht automatisch entfernt werden.
5. Keine Secrets oder echten personenbezogenen Trainingsdaten ins Repository schreiben.
6. Nach jedem Implementierungsschritt Tests ausführen.
7. Einen Schritt erst als abgeschlossen markieren, wenn die Abnahmekriterien erfüllt sind.
```

---

## 21. Screens der App

Für den MVP werden mindestens folgende Screens vorgesehen.

### Start / Heute

Anzeige:

- heutiges Training,
- Dauer,
- Anzahl Übungen,
- Start-Button.

### Trainingsplayer

Anzeige:

- aktuelle Übung,
- Animation,
- Timer,
- Fortschritt,
- Pause/Fortsetzen,
- Feedback-Button.

### Trainingsplan

Anzeige:

- Woche,
- Monat,
- geplante Trainingstage,
- Status.

### Übungskatalog

Anzeige:

- Übungen,
- Kategorien,
- Vorschau,
- Animation.

### Profil

Anzeige:

- Ziele,
- Einschränkungen,
- Equipment,
- Präferenzen.

### Historie

Anzeige:

- vergangene Trainings,
- Dauer,
- Abschlussstatus,
- Feedback.

### Admin / Verwaltung

Später bzw. nur für Administrator:

- Übungen verwalten,
- Planentwürfe prüfen,
- Import,
- Freigabe.

---

## 22. MVP-Abgrenzung

### Bestandteil des MVP

- React-Native-App
- Android und iOS grundsätzlich unterstützt
- mehrere Profile
- Benutzerrechte
- FastAPI
- PostgreSQL
- Tailscale
- Übungskatalog
- Lottie/dotLottie
- Sprachhinweise per TTS
- Wochen- und Monatspläne
- Trainingsplayer
- Timer
- Pausen
- automatische Weiterführung
- Trainingshistorie
- Sprachfeedback
- individuelles Feedback
- Qualitätsfeedback
- AI-Context-Export
- Planimport als DRAFT
- Review und Freigabe

### Nicht Bestandteil des MVP

- direkte KI-Abfragen aus der mobilen App
- laufende OpenAI-API-Nutzung im Trainingsplayer
- MCP-Direktzugriff auf die Produktionsdaten
- vollautomatische Planfreigabe
- öffentliche Bereitstellung für beliebige Nutzer
- komplexes Social-/Community-System
- automatische medizinische Bewertung
- vollständige Gamification

---

## 23. Entwicklungsprinzip: kleine Schritte mit Abnahme

Die Implementierung wird nicht als großer Gesamtauftrag durchgeführt.

Jede Phase folgt diesem Muster:

```text
1. Aufgabe definieren
2. Umsetzung
3. automatisierte Tests
4. lokal starten
5. Funktion ansehen
6. manuell prüfen
7. Feedback / Nachjustierung
8. Abnahme
9. Commit
10. nächster Schritt
```

Es gibt nach jedem größeren Arbeitspaket einen bewussten **Abnahmestopp**.

Der nächste Schritt beginnt erst, wenn der vorherige Stand akzeptiert wurde.

---

## 24. Entwicklungsphasen

### Phase 0 – Repository und Entwicklungsumgebung

Ziel:

- Repository anlegen,
- Codespace vorbereiten,
- Devcontainer,
- Grundstruktur,
- README,
- AGENTS.md,
- Docker Compose.

**Abnahme:** Projekt lässt sich in einer frischen Umgebung starten.

---

### Phase 1 – Backend-Grundgerüst

Ziel:

- FastAPI starten,
- Health Endpoint,
- PostgreSQL-Verbindung,
- Migrationen,
- Basistests.

**Abnahme:**

```text
GET /health
```

liefert erfolgreich einen Health-Status und Backend erreicht PostgreSQL.

---

### Phase 2 – Datenmodell

Ziel:

- Benutzer,
- Profile,
- Ziele,
- Einschränkungen,
- Equipment,
- Übungen,
- Sprachhinweise.

**Abnahme:** Beispieldaten können angelegt, gelesen und geändert werden.

---

### Phase 3 – Übungskatalog

Ziel:

- Übungs-API,
- JSON-Schema,
- erste 3–5 Beispielübungen,
- Lottie-Assets.

**Abnahme:** Übungen werden korrekt über API geliefert und validiert.

---

### Phase 4 – App-Grundgerüst

Ziel:

- React Native + Expo,
- Navigation,
- API-Client,
- Verbindung zum Backend.

**Abnahme:** App kann Profile und Beispielübungen anzeigen.

---

### Phase 5 – Trainingsplan

Ziel:

- Plan-Datenmodell,
- Wochenansicht,
- Monatsansicht,
- Planstatus.

**Abnahme:** Beispielplan erscheint korrekt in der App.

---

### Phase 6 – Trainingsplayer

Ziel:

- Training starten,
- Animation,
- Timer,
- automatischer Wechsel,
- Pause,
- Abschluss.

**Abnahme:** Eine komplette Beispielsession läuft ohne manuelle Zwischenschritte durch.

---

### Phase 7 – Sprachhinweise

Ziel:

- TTS,
- zeitgesteuerte Hinweise,
- Countdown-Hinweise.

**Abnahme:** Sprachhinweise werden an den vorgesehenen Zeitpunkten abgespielt.

---

### Phase 8 – Feedback

Ziel:

- Feedback-Button,
- individuelles Feedback,
- Qualitätsfeedback,
- Spracheingabe,
- Transkription.

**Abnahme:** gesprochenes Feedback wird dem richtigen Profil, der richtigen Session oder Übung zugeordnet.

---

### Phase 9 – Historie

Ziel:

- absolvierte Sessions speichern,
- Historienansicht,
- Trainingsdaten für spätere KI-Auswertung vorbereiten.

**Abnahme:** absolvierte Trainings sind vollständig nachvollziehbar.

---

### Phase 10 – AI-Context-Export

Ziel:

- standardisierter Export,
- JSON-Dateien,
- README,
- Validierung.

**Abnahme:** Ein Coding-Agent kann den Export ohne Datenbankzugriff verstehen.

---

### Phase 11 – KI-Planvorschläge

Ziel:

- Codex / ChatGPT / OpenCode liest AI-Context,
- erstellt DRAFT-Plan,
- Vorschlag wird validiert und importiert.

**Abnahme:** Ein vierwöchiger Testplan kann als Entwurf erzeugt und in der App angezeigt werden.

---

### Phase 12 – Progression und Anpassung

Ziel:

- Historie und Feedback in neue Planvorschläge einbeziehen,
- schrittweise Belastungssteigerung,
- Reduktion bei negativem Feedback.

**Abnahme:** Beispielhistorien erzeugen nachvollziehbar unterschiedliche Folgepläne.

---

## 25. Empfehlung für KI-Modell und Entwicklungsumgebung je Phase

Die konkrete Modellverfügbarkeit kann sich ändern. Vor Beginn einer Phase sollte daher geprüft werden, welche Modelle in der jeweiligen Umgebung tatsächlich verfügbar sind.

### Entscheidungsprinzip

**Codex / ChatGPT in VS Code**

Bevorzugt für:

- Architektur,
- Datenmodell,
- komplexe Refactorings,
- mehrere zusammenhängende Dateien,
- API-Design,
- Debugging,
- Review,
- Teststrategie.

**OpenCode + Kimi**

Bevorzugt für:

- klar abgegrenzte Implementierungsaufgaben,
- Boilerplate,
- einzelne Komponenten,
- repetitive Änderungen,
- Tests,
- Dokumentation,
- alternative Lösungsvorschläge.

**GitHub Codespaces**

Bevorzugte Lauf- und Testumgebung für:

- reproduzierbaren Projektstart,
- End-to-End-Tests,
- Docker,
- Backend + Frontend gemeinsam,
- saubere Neuinstallation,
- Überprüfung, ob das Projekt unabhängig vom lokalen Rechner funktioniert.

### Phasenempfehlung

| Phase | Hauptumgebung | KI-Empfehlung | Begründung |
|---|---|---|---|
| 0 Repository/Devcontainer | Codespaces + VS Code | Codex | Architektur und reproduzierbare Umgebung |
| 1 Backend-Grundgerüst | Codespaces | Codex oder OpenCode/Kimi | klar abgegrenztes Backend-Paket |
| 2 Datenmodell | VS Code | Codex | hohe Bedeutung für Gesamtarchitektur |
| 3 Übungskatalog | VS Code/Codespaces | Codex + optional Kimi | Schema zuerst sauber definieren, Inhalte danach skalieren |
| 4 App-Grundgerüst | Codespaces/VS Code | Codex | Navigation, API-Client und Projektstruktur |
| 5 Trainingsplan | VS Code | Codex | Datenmodell und UI müssen zusammenpassen |
| 6 Trainingsplayer | VS Code | Codex | Zustandslogik und Timer sind zentral |
| 7 Sprachhinweise | VS Code | Codex/OpenCode | gut isolierbares Modul |
| 8 Feedback | VS Code | Codex | Datenzuordnung und UX müssen korrekt sein |
| 9 Historie | Codespaces | Codex/OpenCode | API, DB und UI gemeinsam testen |
| 10 AI-Context | VS Code | Codex | Schema und Agentenregeln |
| 11 Planvorschläge | VS Code + Codespaces | Codex, alternativ OpenCode/Kimi | KI-Workflow und Import testen |
| 12 Progression | VS Code | leistungsfähiges Reasoning-Modell | Regeln und Historienauswertung sorgfältig prüfen |

### Praktische Regel

Vor jedem Implementierungsschritt soll im Arbeitsauftrag ein Block stehen:

```text
Empfohlene Umgebung:
Empfohlenes Modell:
Warum:
Erwartetes Ergebnis:
Automatische Tests:
Manueller Abnahmetest:
```

Damit wird die Wahl von Modell und Umgebung nicht einmalig, sondern pro Arbeitspaket bewusst entschieden.

---

## 26. Teststrategie

### Backend

- Unit Tests
- API Tests
- Datenbanktests
- Validierungstests
- Berechtigungstests

### Mobile App

- Komponenten-Tests
- Navigationstests
- Trainingsplayer-Logik
- Timerzustände
- Pause/Fortsetzen
- API-Fehler

### End-to-End

Mindestens ein kompletter Testfluss:

```text
Profil öffnen
→ heutiges Training laden
→ Training starten
→ Übung durchführen
→ Sprachhinweis
→ Pause
→ nächste Übung
→ Feedback sprechen
→ Training abschließen
→ Historie prüfen
```

---

## 27. Beispiel-Akzeptanzkriterien

Ein Feature ist nicht allein deshalb fertig, weil Code geschrieben wurde.

Beispiel Trainingsplayer:

```text
[ ] Training startet korrekt.
[ ] Erste Animation wird angezeigt.
[ ] Timer startet.
[ ] Sprachhinweis wird zum richtigen Zeitpunkt ausgegeben.
[ ] Nach Ende erfolgt automatisch die Pause.
[ ] Danach startet die nächste Übung.
[ ] Pause/Fortsetzen funktioniert.
[ ] Feedback-Button unterbricht den Ablauf kontrolliert.
[ ] Training wird korrekt abgeschlossen.
[ ] Historie enthält die Session.
[ ] automatisierte Tests sind erfolgreich.
[ ] manueller Test wurde durchgeführt.
```

---

## 28. Später mögliche Erweiterungen

Nicht für das MVP, aber architektonisch berücksichtigen:

- MCP-Anbindung,
- kontrollierter KI-Zugriff auf Trainingsdaten,
- direkte KI-Planung in der App,
- automatische Planvorschläge,
- optionale Textanzeige der Sprachhinweise,
- öffentliche Benutzerregistrierung,
- öffentliche Cloud-Bereitstellung,
- Push-Benachrichtigungen,
- Kalenderintegration,
- Wearables,
- Herzfrequenzdaten,
- Statistiken,
- Fortschrittsdiagramme,
- Gamification,
- Offline-Synchronisation,
- gemeinsames Training,
- Coach-/Trainer-Rolle.

---

## 29. Noch zu konkretisierende Detaildokumente

Aus diesem Master-Konzept sollen später separate Implementierungsdokumente entstehen.

Empfohlene Reihenfolge:

```text
01_repository_setup.md
02_data_model.md
03_backend_api.md
04_exercise_schema.md
05_training_plan_schema.md
06_mobile_app_structure.md
07_training_player.md
08_voice_cues.md
09_feedback.md
10_history.md
11_ai_context.md
12_ai_plan_workflow.md
13_security.md
14_test_strategy.md
```

Diese Dokumente werden jeweils erst dann detailliert ausgearbeitet, wenn die entsprechende Phase ansteht.

---

## 30. Definition of Done pro Phase

Eine Phase ist abgeschlossen, wenn:

1. die vereinbarten Funktionen implementiert sind,
2. der Code verständlich strukturiert ist,
3. automatisierte Tests erfolgreich sind,
4. die Anwendung in Codespaces bzw. der Zielumgebung startet,
5. ein manueller Abnahmetest durchgeführt wurde,
6. Abweichungen dokumentiert wurden,
7. der Nutzer den Stand geprüft hat,
8. notwendige Nachjustierungen abgeschlossen sind,
9. Dokumentation aktualisiert wurde,
10. ein sauberer Git-Commit vorhanden ist.

---

## 31. Grundsatz für die weitere Umsetzung

Das Projekt wird **nicht in einem einzigen großen KI-Auftrag implementiert**.

Stattdessen:

```text
Master-Konzept
      |
      v
Detailplan für Phase
      |
      v
kleines Arbeitspaket
      |
      v
KI-gestützte Implementierung
      |
      v
Tests
      |
      v
manuelle Sichtprüfung
      |
      v
Nachjustierung
      |
      v
Abnahme
      |
      v
nächstes Arbeitspaket
```

Dadurch bleibt die Entwicklung jederzeit nachvollziehbar und korrigierbar.

---

# Zusammenfassung

Das Zielsystem besteht aus einer React-Native-/Expo-App, einem FastAPI-Backend und PostgreSQL auf der NAS. Der private Zugriff erfolgt zunächst über Tailscale.

Die App führt Nutzer mit Lottie-Animationen, Timer, Pausen und gesprochenen Hinweisen durch strukturierte Trainingseinheiten. Trainingspläne und Übungen können mithilfe von Codex, ChatGPT oder OpenCode erstellt und angepasst werden, ohne dass die App im normalen Betrieb selbst KI-Token benötigt.

Feedback wird sowohl personenbezogen zur Trainingsanpassung als auch allgemein zur Verbesserung der App erfasst. Spracheingabe reduziert die notwendige Bedienung während des Trainings.

Trainingshistorie und Feedback bilden die Grundlage für zukünftige Planvorschläge und eine schrittweise Progression.

Die Implementierung erfolgt konsequent in kleinen, testbaren und jeweils abgenommenen Phasen. Für jede Phase wird bewusst entschieden, welche Entwicklungsumgebung und welches verfügbare KI-Modell am besten geeignet ist.

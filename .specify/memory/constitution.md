# Projekt-Constitution

**Version:** 1.1.0
**Beschlossen:** 2026-09-16
**Geändert:** 2026-09-17

## I. Anforderungen und überprüfbare Ergebnisse

Verhaltensänderungen beginnen grundsätzlich mit einem abgegrenzten Feature unter `specs/`.

Spezifikation, technischer Plan, Aufgaben und Implementierung müssen denselben fachlichen Umfang beschreiben.

Die Spezifikation beschreibt primär:

* welches Problem gelöst werden soll,
* welches Verhalten erwartet wird,
* welche Nutzer- oder Systemanforderungen bestehen,
* welche Akzeptanzkriterien erfüllt sein müssen.

Technische Implementierungsentscheidungen gehören grundsätzlich in den Plan und nicht in die fachliche Spezifikation.

Akzeptanzkriterien müssen eindeutig und überprüfbar formuliert sein.

Vor Abschluss eines Features muss nachvollziehbar sein:

* welche Anforderungen umgesetzt wurden,
* welche Tests dafür relevant sind,
* welche Tests tatsächlich ausgeführt wurden,
* welche Tests erfolgreich oder fehlerhaft waren,
* welche bekannten Einschränkungen bestehen.

Ein generierter Bericht oder eine Agentenaussage ersetzt keine tatsächlich ausgeführten Tests.

Kleine Fehlerkorrekturen und technische Änderungen dürfen mit einem ihrem Risiko angemessenen reduzierten Verfahren durchgeführt werden. Umfangreiche Verhaltensänderungen benötigen weiterhin Spezifikation, Plan und Aufgaben.

---

## II. Ein verbindliches DV-Konzept

`docs/DV_KONZEPT.md` ist die zentrale technische und organisatorische Projektdokumentation.

Das DV-Konzept beschreibt mindestens:

* Projektziel,
* Systemkontext,
* Architektur,
* wesentliche Komponenten,
* Schnittstellen,
* Datenhaltung,
* Entwicklungsumgebung,
* Teststrategie,
* Deployment,
* Betrieb,
* Sicherheitsaspekte,
* relevante technische Entscheidungen.

README und Quickstart dienen dem schnellen Einstieg in das Projekt und verweisen auf die maßgeblichen Abschnitte des DV-Konzepts.

Feature-Artefakte unter `specs/`, Architecture Decision Records oder andere Entscheidungsprotokolle dürfen auf das DV-Konzept verweisen, ersetzen es jedoch nicht.

Ändert eine Implementierung Architektur, Betrieb, Schnittstellen, Datenhaltung oder andere im DV-Konzept beschriebene Sachverhalte, muss der betroffene Abschnitt des DV-Konzepts gemeinsam mit der Implementierung aktualisiert werden.

Dokumentation und tatsächlicher Systemzustand dürfen nicht bewusst voneinander abweichen.

---

## III. Bestehende Architektur und Technologie nach Bedarf

Die vorhandene Architektur und Verzeichnisstruktur des Projekts gelten als Ausgangspunkt für neue Entwicklungen.

Bestehende Konventionen, Frameworks und technische Muster sollen beibehalten werden, sofern kein nachvollziehbarer technischer Grund für eine Änderung besteht.

Neue Frameworks, Laufzeitdienste, Infrastrukturkomponenten oder größere Abhängigkeiten dürfen nur aufgenommen werden, wenn sie einen konkreten fachlichen oder technischen Bedarf erfüllen.

Vor Einführung einer wesentlichen neuen Technologie sind mindestens zu berücksichtigen:

* Nutzen,
* Komplexität,
* Wartbarkeit,
* bestehende Alternativen im Projekt,
* Sicherheitsauswirkungen,
* Betriebsaufwand,
* langfristige Abhängigkeiten.

Unnötige Abstraktion und technische Komplexität sind zu vermeiden.

Bevorzugt werden einfache, robuste und wartbare Lösungen.

Entwicklungs-, Test- und Produktionsumgebungen besitzen getrennte und nachvollziehbare Konfigurationen.

Produktionskonfigurationen dürfen nicht implizit von Entwicklungsannahmen abhängen.

---

## IV. Verträge, Schnittstellen und Daten

Öffentliche und interne Verträge müssen zwischen Spezifikation, Dokumentation, Implementierung und relevanten Tests konsistent bleiben.

Dazu gehören insbesondere:

* APIs,
* Datenmodelle,
* Nachrichtenformate,
* Konfigurationsformate,
* Datenbankstrukturen,
* externe Schnittstellen.

Änderungen an bestehenden Verträgen sollen soweit praktikabel rückwärtskompatibel erfolgen.

Breaking Changes müssen ausdrücklich erkennbar, begründet und dokumentiert sein.

Datenänderungen berücksichtigen abhängig vom Risiko:

* Migration,
* Validierung,
* bestehende Datenbestände,
* Backup,
* Wiederherstellung,
* Rollback oder einen anderen geeigneten Rückweg.

Produktive Daten dürfen nicht durch Testinitialisierung oder Entwicklungsmechanismen verändert werden.

Testinitialisierung ist kein Ersatz für ein Produktionsmigrationsverfahren.

Migrationen müssen reproduzierbar und nachvollziehbar sein.

---

## V. Codequalität und Änderungsdisziplin

Code muss nachvollziehbar, modular und wartbar sein.

Bestehende Projektkonventionen haben Vorrang vor neu eingeführten persönlichen oder agentenspezifischen Präferenzen.

Es gelten insbesondere folgende Grundsätze:

* Änderungen sollen möglichst klein und fachlich fokussiert bleiben.
* Nicht betroffene Projektbereiche sollen nicht ohne begründeten Bedarf refaktoriert werden.
* Duplizierung soll vermieden werden, ohne unnötige Abstraktionsschichten einzuführen.
* Bestehende öffentliche Schnittstellen sollen erhalten bleiben, sofern die Spezifikation keine Änderung verlangt.
* Tote oder überholte Implementierungen dürfen entfernt werden, wenn ihre Nichtverwendung ausreichend geprüft wurde.
* Temporäre Workarounds müssen als solche erkennbar sein und dürfen nicht unbemerkt zu dauerhaften Architekturentscheidungen werden.

Codex und andere Entwicklungsagenten dürfen keine umfangreichen Architektur-, Technologie- oder Strukturänderungen allein aufgrund einer vermeintlichen Verbesserung durchführen.

Solche Änderungen müssen aus einer Anforderung, einem technischen Plan oder einer dokumentierten Entscheidung hervorgehen.

---

## VI. Tests und Verifikation

Bestehende Tests müssen nach Änderungen weiterhin erfolgreich ausgeführt werden, soweit sie von der Änderung betroffen sein können.

Neue Funktionalität erhält geeignete Tests entsprechend ihrem Risiko und ihrer Bedeutung.

Bei Fehlerkorrekturen soll nach Möglichkeit ein Regressionstest erstellt werden, der den ursprünglichen Fehler reproduziert und dessen erneutes Auftreten verhindert.

Tests dürfen nicht entfernt, deaktiviert oder abgeschwächt werden, nur damit eine Implementierung erfolgreich erscheint.

Relevante Prüfungen können unter anderem umfassen:

* Unit-Tests,
* Integrationstests,
* API- oder Vertragstests,
* Migrationstests,
* End-to-End-Tests,
* statische Analyse,
* Linting,
* Typprüfung,
* Build,
* Security-Prüfungen.

Welche Prüfungen erforderlich sind, richtet sich nach Art und Risiko der Änderung.

Ein Feature gilt nicht allein deshalb als abgeschlossen, weil die Implementierung syntaktisch vollständig ist.

---

## VII. Sicherheit und Secrets

Externe und vom Benutzer kontrollierte Eingaben müssen an geeigneten Systemgrenzen validiert werden.

Secrets dürfen niemals im Quellcode oder Repository gespeichert werden.

Dazu gehören insbesondere:

* Passwörter,
* API-Keys,
* Tokens,
* private Schlüssel,
* Zugangsdaten,
* produktive Verbindungsinformationen.

Secrets werden über dafür vorgesehene Mechanismen wie Umgebungsvariablen oder Secret Stores bereitgestellt.

Beispielkonfigurationen dürfen ausschließlich ungefährliche Platzhalter enthalten.

Logs dürfen keine unnötigen sensitiven Informationen enthalten.

Neue Abhängigkeiten und technische Lösungen sollen keine bekannten vermeidbaren Sicherheitsrisiken einführen.

Sicherheitsrelevante bestehende Mechanismen dürfen nicht ohne dokumentierte Begründung abgeschwächt oder umgangen werden.

---

## VIII. Reproduzierbare und begrenzte Zugriffe

Werkzeug-, Laufzeit- und relevante Modulversionen werden so festgehalten, dass Entwicklungs-, Test- und Build-Prozesse reproduzierbar bleiben.

Abhängigkeiten sollen über die für das jeweilige Ökosystem vorgesehenen Mechanismen versioniert oder gelockt werden.

Fremde Referenz-Repositories sind grundsätzlich nur lesbar.

Beiträge oder Experimente auf Basis solcher Repositories erfolgen in separaten Arbeitskopien oder ausdrücklich dafür vorgesehenen Forks.

Secrets, Laufzeitprotokolle, temporäre Dateien, Build-Artefakte und persistente Dienstdaten gehören nicht in Git, sofern sie nicht ausdrücklich als versionierte Projektressource vorgesehen sind.

Automatisierte Werkzeuge und Agenten erhalten nur die für ihre Aufgabe erforderlichen Zugriffsrechte.

---

## IX. Wiederverwendbares Wissen

Projektspezifische fachliche und technische Informationen verbleiben im Projekt und insbesondere im DV-Konzept.

Allgemein wiederverwendbares Wissen soll nicht unnötig projektspezifisch dupliziert werden.

Geeignete allgemeine Erkenntnisse können als geprüfter Änderungsvorschlag in eine zentrale Knowledge Base übernommen werden.

Wiederverwendbare:

* Projektstrukturen,
* Vorlagen,
* Automatisierungen,
* Entwicklungsabläufe,
* Agentenregeln,
* Konfigurationen

sollen nach Prüfung in das dafür vorgesehene Projekt-Template übernommen werden.

Projekt und Template dürfen sich nicht unkontrolliert gegenseitig überschreiben.

Änderungen am Template werden bewusst übernommen und nicht automatisch in bestehende Projekte eingespielt.

---

## X. Spec-Driven Development

Größere Features werden grundsätzlich über einen nachvollziehbaren Spec-Driven-Development-Prozess umgesetzt.

Der bevorzugte Ablauf ist:

1. Constitution
2. Specification
3. Clarification
4. Technical Plan
5. Tasks
6. Consistency Analysis
7. Implementation
8. Verification

Die Constitution definiert langfristige Projektprinzipien.

Eine Feature-Spezifikation definiert das gewünschte Verhalten.

Der Plan beschreibt die technische Umsetzung.

Tasks zerlegen den Plan in ausführbare Arbeitsschritte.

Die Implementierung folgt der freigegebenen Spezifikation und dem technischen Plan.

Erkennt Codex während der Implementierung einen Widerspruch zwischen:

* Constitution,
* Spezifikation,
* Plan,
* bestehenden Verträgen,
* bestehender Architektur

darf dieser Widerspruch nicht stillschweigend durch eine eigenständige Architekturentscheidung aufgelöst werden.

Der Konflikt muss sichtbar gemacht und in der dafür vorgesehenen Ebene korrigiert werden.

---

## XI. Änderungen an bestehenden Projekten

Dieses Projekt ist als bestehendes System zu behandeln.

Vor größeren Änderungen müssen Codex und andere Entwicklungsagenten zunächst die relevanten vorhandenen Projektbestandteile analysieren.

Dazu können insbesondere gehören:

* `README`,
* `docs/DV_KONZEPT.md`,
* bestehende Specs,
* Quellcode,
* Tests,
* Build-Konfiguration,
* Deployment-Konfiguration,
* CI/CD,
* Datenmodelle,
* APIs,
* vorhandene Entwicklungsrichtlinien.

Vorhandene funktionierende Strukturen sollen nicht allein deshalb ersetzt werden, weil eine alternative Implementierung moderner oder subjektiv eleganter erscheint.

Neue Features sollen möglichst in die bestehende Architektur integriert werden.

Architekturänderungen sind zulässig, wenn bestehende Strukturen eine Anforderung nicht sinnvoll erfüllen können und die Änderung nachvollziehbar geplant und dokumentiert wurde.

---

## XII. Agentenverhalten

Codex und andere KI-Agenten dienen der Umsetzung der festgelegten Anforderungen und technischen Entscheidungen.

Agenten sollen:

* vorhandenen Kontext zuerst analysieren,
* bestehende Konventionen respektieren,
* Änderungen auf den erforderlichen Umfang begrenzen,
* Annahmen sichtbar machen,
* tatsächlich ausgeführte Prüfungen von lediglich vorgeschlagenen Prüfungen unterscheiden,
* keine Testergebnisse behaupten, die nicht ausgeführt wurden,
* keine Anforderungen eigenständig erweitern,
* keine verdeckten Breaking Changes durchführen.

Ein Agent darf technische Verbesserungsvorschläge machen.

Ein Vorschlag ist jedoch keine automatisch genehmigte Änderung des Projekts.

---

# Änderungen der Constitution

Änderungen dieser Constitution müssen begründet und versioniert werden.

Bei Änderungen sind mindestens auf Widersprüche zu prüfen:

* `docs/DV_KONZEPT.md`,
* Spec-Kit-Vorlagen,
* Agentenregeln,
* Projekt-Templates,
* Entwicklungsdokumentation,
* bestehende Spezifikationen.

Versionsänderungen folgen grundsätzlich semantischer Versionierung:

* **PATCH:** Klarstellungen ohne Änderung der zugrunde liegenden Regeln.
* **MINOR:** Neue oder wesentlich erweiterte Prinzipien.
* **MAJOR:** Grundlegende Änderung oder Entfernung bestehender verbindlicher Prinzipien.

Eine generierte Checkliste, ein erfolgreicher Agentenlauf oder ein grüner Agentenbericht ersetzt keine tatsächlich ausgeführten technischen Prüfungen.

Die Constitution ist gegenüber einzelnen Feature-Plänen übergeordnet. Wenn ein Plan der Constitution widerspricht, muss entweder der Plan korrigiert oder die Constitution bewusst und versioniert geändert werden.

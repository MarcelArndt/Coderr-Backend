# Coderr - Backend

## Projektbeschreibung

**Coderr** ist eine webbasierte Vermittlungsplattform, die Business-Kunden und Dienstleister miteinander verbindet – ähnlich wie Fiverr. Unternehmen können gezielt Aufträge für verschiedene Services einstellen, während registrierte Nutzer passende Angebote einreichen und Aufträge annehmen können. Mit individuellen Nutzerprofilen, Upload-Möglichkeiten für Avatare und Projektbilder sowie einem integrierten Bewertungssystem sorgt Coderr für Transparenz und Vertrauen. Dank der leistungsstarken Backendsuche finden Kunden schnell den passenden Anbieter – einfach, effizient und direkt.

> **Hinweis:** Um dieses Backend zu verwenden, wird auch das zugehörige Frontend benötigt. <a href="https://github.com/MarcelArndt/Coderr-Frontend" target="_blank">Link zum Frontend-Repository</a>

## Installation

### 1. Projekt klonen
Zuerst solltest du das Projekt von GitHub klonen:

```
git clone https://github.com/MarcelArndt/Coderr-Backend
```

### Manuelle Installation mit Python

### 2. Virtuelle Umgebung erstellen.
Erstelle eine virtuelle Umgebung für das Projekt und aktiviere diese
```
python -m venv env
```

```
env\Scripts\activate
```

### 3. Requirements installieren.
Als Nächstes müssen alle Requirements und Abhängigkeiten installiert werden.
```
pip install -r requirements.txt
```

### 4. Anlegen von Migrationen
Um die migrationen auzuführen, die für die Erstellung der Datenbank benötigt werden

```
Coderr spaltet sich in zwei dafür nötige Apps auf
    1. auth-app für die Authentication und regestrieren der Benutzer/User
    2. Der eigentlichen market-app, wo sich die logic für den generellen Marktplatz von Coderr zu finden ist.
```

```
python manage.py makemigrations
```

```
python manage.py migrate
```

### 4. Anlegen von Testdaten
Falls man möchte, kann man optional für einpflegen von Testdaten die utils.py ausführen
```
python utils.py
```

### 5. Server starten
Nun sollte der Server starten können. Wichtig ist, dass ihr beim nächsten Mal starten wieder in die virtuelle Umgebung geht, bevor ihr den Server starten versucht.
```
python manage.py runserver
```

### 6. Nutzung
Sobald der Server läuft, kannst du das Frontend verwenden und Coderr in seiner vollen Funktionalität genießen.
Damit ist alles vollständig! Wenn noch etwas fehlt oder angepasst werden soll, lass es mich wissen.

### Installation mit Bat-Datei

### 2. Installation und Datenbank einrichten
Führe die beiliegende install.bat-Datei aus, um alle benötigten Abhängigkeiten zu installieren, die Datenbank zu füllen und einen Gast-Account zu erstellen:
Das Fenster kann geschlossen werden, sobalt die passende Meldung dazu in der Konsole erscheint.

### 3. Server starten
Nach der Installation kannst du den Server starten, indem du die start-server.bat-Datei ausführst. Dadurch wird der Backend-Server hochgefahren und du kannst das Frontend nutzen:

### 4. Nutzung
Sobald der Server läuft, kannst du das Frontend verwenden und Coderr in seiner vollen Funktionalität genießen.

Damit ist alles vollständig! Wenn noch etwas fehlt oder angepasst werden soll, lass es mich wissen.
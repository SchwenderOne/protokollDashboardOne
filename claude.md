# Transaktionsanalyse Dashboard - Projekt Dokumentation

## Projektübersicht

Ein interaktives, selbstständiges Dashboard zur Analyse von Unternehmenstransaktionen. Das Dashboard ist vollständig in deutscher Sprache und wurde für Meeting-Präsentationen optimiert.

## Technische Architektur

### Kernkomponenten

1. **dashboard.html / index.html** (138KB)
   - Vollständig selbstständige HTML-Datei
   - Alle Transaktionsdaten sind direkt als JSON eingebettet
   - Verwendet Chart.js für Visualisierungen
   - Keine externen Abhängigkeiten zur Laufzeit
   - Funktioniert komplett offline

2. **generate_dashboard.py**
   - Python-Skript zur Dashboard-Generierung
   - Liest `transactions_cleaned.csv`
   - Generiert `dashboard.html` mit eingebetteten Daten
   - Vermeidet CORS-Probleme durch Einbettung

3. **analyze_transactions.py**
   - Datenanalyse und Bereinigung
   - Erstellt `transactions_cleaned.csv` aus `bo Kopie.csv`
   - Generiert PNG-Visualisierungen für Reports

### Datenfluss

```
bo Kopie.csv (Rohdaten)
    ↓
analyze_transactions.py
    ↓
transactions_cleaned.csv
    ↓
generate_dashboard.py
    ↓
dashboard.html (mit eingebetteten Daten)
```

## CSV-Datenformat

### Rohdaten Format (`bo Kopie.csv`)
- Ungerade/Gerade Spaltenstruktur (odd/even)
- Enthält HTML-Links und Icons
- Ursprung: Backend-Scraping

### Bereinigtes Format (`transactions_cleaned.csv`)
Spalten:
- `timestamp` - ISO 8601 Format (2025-10-01 06:41:59.295)
- `transaction_id` - UUID
- `status` - CREATED, CANCELLED, APPROVED, CAPTURED
- `customer_name` - Kundenname
- `amount_str` - Originaler String mit "EUR"
- `reference` - Transaktionsreferenz (UC000000000000001XXX)
- `amount` - Float-Wert
- `date` - Datum (YYYY-MM-DD)
- `hour` - Stunde (0-23)
- `day_of_week` - Wochentag (Monday, Tuesday, etc.)
- `week` - Kalenderwoche
- `amount_range` - Kategorie (€0-1k, €1k-2k, etc.)

## Dashboard-Features

### 1. Metrikkarten (6 Stück)
- Gesamttransaktionen + eindeutige Kunden
- Gesamtwert + Zeitraum
- Durchschnitt + Median
- Erfolgsquote + stornierte Anzahl
- Erstellt (Status) + Prozent
- Größte + Kleinste Transaktion

### 2. Interaktive Diagramme (Chart.js)
- **Tägliches Transaktionsvolumen**: Line Chart
- **Transaktionsstatus Verteilung**: Doughnut Chart
- **Stündliches Aktivitätsmuster**: Bar Chart
- **Betragsverteilung**: Bar Chart

### 3. Filterfunktionen
- **Statusfilter**: Dropdown (Alle, CREATED, CANCELLED, etc.)
- **Datumsbereich**: Von/Bis Datum
- **Kundensuche**: Text-Eingabe mit Live-Filter
- **Duplikatfilter**:
  - Nur nach Namen (erste Vorkommen behalten)
  - Nach Name + Betrag (erste Vorkommen behalten)

### 4. Interaktive Kundenselektion
**Wichtiges Feature:**
- Klick auf Kunde in "Top 15 Kunden" Tabelle
- Top 15 Tabelle bleibt IMMER vollständig (wird nicht gefiltert)
- Nur die "Alle Transaktionen" Tabelle wird gefiltert
- Kunde wird blau markiert (`.customer-row.selected`)
- Transaktionen werden gelb hervorgehoben (`.highlighted-transaction`)
- Erneuter Klick = Toggle (Filter entfernen)
- Variable `selectedCustomer` trackt aktuelle Auswahl

## Wichtige Implementierungsdetails

### CORS-Lösung
**Problem**: Browser blockieren lokales Laden von CSV-Dateien
**Lösung**: Daten direkt als JSON in HTML einbetten
```javascript
const TRANSACTIONS_DATA = [/* JSON Array */];
```

### Netlify-Kompatibilität
- `index.html` als Kopie von `dashboard.html`
- `netlify.toml` für Konfiguration
- Publish directory: "." (Root)
- Redirects konfiguriert

### Filterlogik-Separation
**Kritisch für nächste Session:**
```javascript
// Top 15 basiert auf filteredData (Status, Datum, Duplikate)
const topCustomers = calculateFromFiltered(filteredData);

// Transaktionsliste zusätzlich nach selectedCustomer gefiltert
let displayTransactions = [...filteredData];
if (selectedCustomer) {
    displayTransactions = displayTransactions.filter(t =>
        t.customer_name === selectedCustomer
    );
}
```

## Styling-Details

### Farbschema
- Primär: `#667eea` (Lila/Blau für Charts)
- Erfolg: `#2ecc71` (Grün)
- Warnung: `#f39c12` (Orange)
- Fehler: `#e74c3c` (Rot)
- Info: `#3498db` (Blau)

### Status-Badges
```css
.status-created { background: #d4edda; color: #155724; }
.status-cancelled { background: #f8d7da; color: #721c24; }
.status-approved { background: #d1ecf1; color: #0c5460; }
.status-captured { background: #d4edda; color: #155724; }
```

### Interaktive Elemente
```css
.customer-row { cursor: pointer; }
.customer-row.selected { background: #2196f3; color: white; }
.highlighted-transaction { background: #fff9c4; animation: highlight-fade 2s; }
```

## Geplantes Feature: CSV-Upload-System

### Ziel für nächste Session
Ein System erstellen, das es dem Benutzer ermöglicht:
1. Eine neue CSV-Datei im Browser hochzuladen
2. Automatisch das Dashboard mit den neuen Daten zu generieren
3. Das neue Dashboard herunterzuladen oder direkt anzuzeigen

### Technische Überlegungen

#### Option 1: Client-Side Processing (Empfohlen)
**Vorteile:**
- Keine Server-Infrastruktur nötig
- Sofortige Verarbeitung im Browser
- Privatsphäre (Daten bleiben lokal)

**Implementierung:**
- File API für CSV-Upload
- Papa Parse oder ähnliche Library für CSV-Parsing
- JavaScript-Logik zur Datentransformation
- Blob-Download für neues Dashboard

**Workflow:**
```
1. User lädt CSV hoch (input type="file")
2. JavaScript liest Datei (FileReader API)
3. CSV wird geparst und transformiert
4. Neues dashboard.html wird generiert (Template + Daten)
5. Download als neue HTML-Datei angeboten
```

#### Option 2: Server-Side Processing
**Vorteile:**
- Leistungsfähiger bei großen Dateien
- Kann komplexere Validierung durchführen

**Nachteile:**
- Benötigt Backend (Python Flask/FastAPI)
- Hosting-Kosten
- Komplexere Architektur

### Benötigte Komponenten

1. **Upload-Interface**
   - Drag & Drop Zone
   - Dateivalidierung (CSV, Größe)
   - Fortschrittsanzeige

2. **CSV-Parser**
   - Erkennung des "odd/even" Formats
   - Transformation zu bereinigtem Format
   - Fehlerbehandlung

3. **Dashboard-Generator (JavaScript)**
   - Template-System für HTML
   - Einbettung der Daten als JSON
   - Generierung der vollständigen HTML-Datei

4. **Download-Mechanismus**
   - Blob-Erstellung
   - Automatischer Download
   - Dateinamen-Generierung (z.B. "dashboard_2025-11-10.html")

### CSV-Format-Anforderungen

**Erwartetes Format (wie aktuell):**
```csv
"sorting_1","odd","odd 2","odd 3","odd 4","odd 5","odd 6","odd href","odd src","even","even 2","even 3","even 4","even 5","even 6","even href","even src"
"0","2025-10-01 06:41:59.295","7b47aa65-cdc8-43d0-ab22-0c58f7342c5d","CREATED","ULRIKE CLAUDIA PICHLER","3558.0 EUR","UC000000000000001190",...
```

**Kritische Felder:**
- Spalte "odd" / "even": Timestamp
- Spalte "odd 2" / "even 2": Transaction ID
- Spalte "odd 3" / "even 3": Status
- Spalte "odd 4" / "even 4": Customer Name
- Spalte "odd 5" / "even 5": Amount (mit "EUR")
- Spalte "odd 6" / "even 6": Reference

### Validierungsregeln

1. **Pflichtfelder prüfen**: Timestamp, Status, Customer, Amount
2. **Datumsformat validieren**: ISO 8601 kompatibel
3. **Betrag extrahieren**: "3558.0 EUR" → 3558.0
4. **Status-Werte**: Nur CREATED, CANCELLED, APPROVED, CAPTURED
5. **Duplikate erkennen**: Warnung anzeigen

### UI-Mockup für Upload-Seite

```
┌─────────────────────────────────────────┐
│   📊 Dashboard Generator                │
│                                         │
│   ┌─────────────────────────────────┐  │
│   │  🗂️  CSV-Datei hier ablegen    │  │
│   │     oder klicken zum Auswählen  │  │
│   └─────────────────────────────────┘  │
│                                         │
│   Dateiformat: bo_Kopie.csv Format     │
│   Max. Größe: 10 MB                    │
│                                         │
│   ✅ Datei: transactions.csv           │
│   📊 288 Transaktionen erkannt         │
│   💶 €903,824.56 Gesamtwert            │
│                                         │
│   [Dashboard Generieren]  [Abbrechen] │
└─────────────────────────────────────────┘
```

## Entwicklungsrichtlinien

### Code-Stil
- Deutsche Kommentare und Variablennamen für UI
- Englische Variablennamen im JavaScript-Code
- Konsistente Einrückung (4 Spaces)
- JSDoc-Kommentare für Funktionen

### Testen
- Manuelles Testen im Browser (Chrome, Firefox, Safari)
- Verschiedene CSV-Größen testen
- Edge Cases: Leere Felder, Sonderzeichen, ungültige Daten

### Performance
- Dashboard sollte auch mit 1000+ Transaktionen flüssig laufen
- Chart.js mit `maintainAspectRatio: false` für responsive Charts
- Debouncing für Suchfilter (bereits implementiert durch `input` Event)

## Bekannte Einschränkungen

1. **Dateneinbettung**: Sehr große Dateien (>5MB CSV) können zu großen HTML-Dateien führen
2. **Browser-Speicher**: Eingebettete Daten erhöhen Speicherbedarf
3. **Keine Echtzeit-Updates**: Dashboard ist statisch, benötigt Neugenerierung

## Dependencies

### Python (für Generierung)
```
pandas==2.3.3
matplotlib==3.10.7
seaborn==0.13.2
numpy==2.3.4
```

### JavaScript (CDN, keine Installation)
```
Chart.js via CDN: https://cdn.jsdelivr.net/npm/chart.js
```

### Zukünftige Dependencies (für Upload-Feature)
```
PapaParse (CSV parsing): https://www.papaparse.com/
oder
CSV.js: https://github.com/knrz/CSV.js/
```

## Repository-Struktur

```
protokollDashboardOne/
├── .gitignore              # Python venv, cache, OS files
├── README.md               # Projekt-Dokumentation
├── claude.md              # Diese Datei - Projekt-Kontext
├── netlify.toml           # Netlify-Konfiguration
├── index.html             # Netlify Entry Point
├── dashboard.html         # Haupt-Dashboard (identisch mit index.html)
├── generate_dashboard.py  # Dashboard-Generator
├── analyze_transactions.py # Datenanalyse
├── bo Kopie.csv          # Original-Rohdaten
├── transactions_cleaned.csv # Bereinigte Daten
├── transaction_analysis_overview.png
├── customer_analysis.png
└── time_series_analysis.png
```

## Git Workflow

```bash
# Änderungen committen
git add .
git commit -m "Description

🤖 Generiert mit Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Zu GitHub pushen
git push origin main
```

## Deployment

### Netlify
- Automatisches Deployment bei Push zu main
- URL: [Wird von Netlify generiert]
- Konfiguration in `netlify.toml`

### Lokal
- Einfach `index.html` oder `dashboard.html` im Browser öffnen
- Keine Installation oder Server benötigt

## Nächste Session - Aufgaben

### Priorität 1: Upload-System
1. Neue HTML-Seite erstellen: `upload.html` oder `generator.html`
2. File Upload UI implementieren
3. CSV-Parser integrieren (Client-Side)
4. Datentransformation (odd/even → cleaned format)
5. Dashboard-Template-System
6. HTML-Generierung mit eingebetteten Daten
7. Download-Funktion

### Priorität 2: Validierung & UX
1. CSV-Format-Validierung
2. Fehlerbehandlung und User-Feedback
3. Fortschrittsanzeige
4. Vorschau der Daten vor Generierung

### Priorität 3: Dokumentation
1. Benutzerhandbuch für Upload-Funktion
2. CSV-Format-Spezifikation
3. Troubleshooting-Guide

## Wichtige Hinweise für nächste Session

1. **Dateiformat beibehalten**: Das odd/even Format muss unterstützt werden
2. **Template-Ansatz**: `dashboard.html` als Template nutzen, nur Daten ersetzen
3. **Client-Side bevorzugen**: Keine Server-Abhängigkeiten wenn möglich
4. **Progressive Enhancement**: Erst Basis-Upload, dann erweiterte Features
5. **Testing**: Mit verschiedenen CSV-Größen testen (klein, mittel, groß)

## Kontaktinformationen

- **GitHub**: https://github.com/SchwenderOne/protokollDashboardOne
- **Deployment**: Netlify
- **Generiert mit**: Claude Code (Sonnet 4.5)

---

**Letzte Aktualisierung**: 2025-11-11
**Version**: 1.0.0
**Status**: Production Ready - Erweiterung in Planung

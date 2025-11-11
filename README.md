# Transaktionsanalyse Dashboard

Ein interaktives Dashboard zur Analyse von Unternehmenstransaktionen.

## Funktionen

- 📊 **Umfassende Statistiken**: Gesamttransaktionen, Gesamtwert, Durchschnitt, Erfolgsquote
- 📈 **Interaktive Diagramme**: Tägliches Volumen, Statusverteilung, stündliche Aktivität, Betragsverteilung
- 🔍 **Flexible Filter**: Nach Status, Datum, Kunde filtern
- 🎯 **Duplikaterkennung**: Ausschluss von doppelten Namen oder Name+Betrag Kombinationen
- 👆 **Klickbare Top-Kunden**: Klick auf Kunde filtert Transaktionsliste automatisch
- 💡 **Toggle-Funktion**: Erneuter Klick entfernt Filter
- ✨ **Visuelle Hervorhebungen**: Ausgewählte Kunden und Transaktionen werden farblich markiert

## Dateien

- `dashboard.html` - Das vollständige, selbstständige Dashboard (einfach im Browser öffnen)
- `generate_dashboard.py` - Python-Skript zur Generierung des Dashboards
- `analyze_transactions.py` - Datenanalyse und Visualisierungen
- `bo Kopie.csv` - Original-Rohdaten
- `transactions_cleaned.csv` - Bereinigte Transaktionsdaten

## Verwendung

### Dashboard öffnen
Einfach die Datei `dashboard.html` im Browser öffnen - keine Installation erforderlich!

### Dashboard neu generieren
Falls Sie die Daten aktualisieren möchten:

```bash
# Virtuelle Umgebung erstellen (einmalig)
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install pandas matplotlib seaborn

# Dashboard neu generieren
python generate_dashboard.py
```

## Dashboard-Funktionen

### Filter
- **Statusfilter**: Nur bestimmte Status anzeigen (Erstellt, Storniert, etc.)
- **Datumsbereich**: Von/Bis Datum festlegen
- **Kundensuche**: Nach Kundenname suchen
- **Duplikate ausschließen**:
  - Nach Namen (erste Vorkommen behalten)
  - Nach Name + Betrag (erste Vorkommen behalten)

### Interaktive Kundenauswahl
1. Klick auf Kunde in Top 15 → Filtert Transaktionsliste
2. Kunde wird **blau** markiert
3. Transaktionen werden **gelb** hervorgehoben
4. Erneuter Klick → Filter wird entfernt

## Technische Details

- **Framework**: Reines HTML/JavaScript mit Chart.js
- **Datenformat**: Alle Transaktionsdaten sind direkt im HTML eingebettet
- **Offline-fähig**: Funktioniert komplett ohne Server
- **Responsive**: Passt sich an verschiedene Bildschirmgrößen an

## Datenübersicht

- **Zeitraum**: 1. Oktober - 7. November 2025 (37 Tage)
- **Transaktionen**: 288 Transaktionen
- **Gesamtwert**: €903,824.56
- **Durchschnitt**: €3,138.28 pro Transaktion
- **Erfolgsquote**: ~96.5%

## Generiert mit

🤖 Claude Code - AI-gestützte Entwicklung

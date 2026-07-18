# Protein Samurai – unabhängiger Produktvergleich für MORE Nutrition

Interaktive Vergleichsseite für Produkte der Marke **MORE Nutrition**: alle Kategorien mit
Preisen, Nährwerten, Bewertungen, einem transparenten Score, **Live-Verfügbarkeit je Variante**,
Kauf-Tipps und Bezugsquellen. Reine statische HTML-Seite (Vanilla JS) mit einem kleinen
Python-Generator für die Verfügbarkeits-Updates.

> Unabhängiger, informativer Vergleich ohne Verbindung zu MORE Nutrition. Preise/Verfügbarkeit
> ändern sich laufend; verbindlich ist immer der Shop. Angaben ohne Gewähr.

## Was ist drin
| Datei | Zweck |
|---|---|
| `index.html` / `more-nutrition-vergleich.html` | Die fertige Seite (identisch). Einfach im Browser öffnen. |
| `template.html` | Seiten-Vorlage mit Platzhaltern `__AVAIL_DATE__`, `__LIVE__`, `__NEWPRODUCTS__`. |
| `generate.py` | Erzeugt die Seite aus Vorlage + `live.json`. |
| `refresh.py` | Holt die Live-Verfügbarkeit (inkl. Varianten/Preisen) von morenutrition.de, schreibt `live.json` + `history.json` (Verfügbarkeits- und Preis-Snapshots je Variante) und regeneriert die Seite. |
| `img/` | Lokal gecachte Produktbilder (640 px, von Shopify). |
| `manifest.json` / `sw.js` / `favicon.svg` | PWA-Grundausstattung (installierbar, Offline-Cache über http). |
| `.github/workflows/refresh.yml` | Wöchentlicher Auto-Refresh via GitHub Actions inkl. Pages-Deploy (nach Push auf GitHub aktiv). |
| `.github/workflows/pages.yml` | GitHub-Pages-Deploy bei jedem Push auf `main`. |
| `fonts/` | Inter als lokale woff2 (latin-Subset). |
| `impressum.html` / `datenschutz.html` | Rechtsseiten (bis zur Veröffentlichung mit markierten Platzhaltern statt echter Personendaten). |
| `404.html` | Fehlerseite für GitHub Pages (base-Pfad wird zur Laufzeit berechnet). |
| `og-image.png` | Social-Media-Vorschaubild (og:image, 1200×630, eigenes Branding). |
| `robots.txt` / `sitemap.xml` | SEO-Grundausstattung (URLs zeigen auf die geplante Domain proteinsamurai.de). |
| `live.json` | Aktuelle Live-Daten (Verfügbarkeit je Variante, neue Produkte, Datum). |
| `CLAUDE.md` | Projekt-Brief & Konventionen (für Claude Code / Entwickler:innen). |
| `ROADMAP.md` | Nächste Ausbaustufen mit Akzeptanzkriterien. |

## Schnellstart
```bash
# Seite ansehen: index.html im Browser öffnen
# Seite neu erzeugen (nach Änderung an template/live.json):
python3 generate.py template.html live.json index.html
```

## Weiterbauen mit Claude Code

### Installation & Start
Nativer Installer (empfohlen, Auto-Update):
```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash
# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```
Oder via npm (Node.js 22+): `npm install -g @anthropic-ai/claude-code`

Im Projektordner starten:
```bash
cd more-nutrition-app
git init && git add -A && git commit -m "Initial handoff"   # empfohlen: erst in git
claude
```

### CLAUDE.md
Claude Code liest `CLAUDE.md` automatisch beim Start — dort stehen Aufbau, Datenmodell, Scoring,
die Verfügbarkeits-Pipeline und die **Constraints** (u. a. kein Checkout-Bot). `/init` würde eine
neue CLAUDE.md erzeugen — hier ist schon eine gepflegte vorhanden, also lieber ergänzen.

### Empfohlener Ablauf
1. **Plan-Modus** (Ctrl+G): Claude liest den Code und schlägt einen Umsetzungsplan vor, ohne zu ändern.
2. Plan bestätigen → Claude codet, testet (Headless-Browser-Check), fixt.
3. `/goal` setzen (z. B. „Seite lädt ohne JS-Fehler"), damit Claude nach jedem Schritt gegenprüft.
4. Für externe Dienste (GitHub, DB, Mail) via `claude mcp add` MCP-Server anbinden.

Nützliche Slash-Befehle: `/init`, `/goal`, `/clear`, `/rewind`, `/permissions`.

### Verifikation
Es gibt kein Test-Framework; prüfe mit einem Headless-Browser (Playwright/Chromium): `index.html`
laden, auf `pageerror` prüfen, Screenshots machen. Bild-Ladefehler externer CDN sind normal und
keine JS-Fehler.

Siehe `ROADMAP.md` für die nächsten Schritte (1-Klick-Warenkorb, Restock-Alerts, Affiliate, Deployment).

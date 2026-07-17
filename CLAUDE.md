# CLAUDE.md — MORE Nutrition Produktvergleich

Kontext & Konventionen für Claude Code. Bitte vor Änderungen lesen.

## Was das Projekt ist
Ein **Produktvergleich für MORE Nutrition** (deutsche Supplement-Marke, morenutrition.de).
Zeigt alle Kategorien mit Preisen, Nährwerten, Bewertungen, einem transparenten Score
(Proteine/Riegel/Snacks), Live-Verfügbarkeit je Variante, Kauf-Tipps und Bezugsquellen.
Ziel: die Seite zu einem echten kleinen Produkt ausbauen (1-Klick-Warenkorb, Restock-Alerts,
Affiliate) — siehe `ROADMAP.md`.

## Stack / Aufbau
- **Eine einzelne, self-contained HTML-Datei** (`index.html` = `more-nutrition-vergleich.html`):
  Vanilla JS, kein Framework, kein Build-Tool, keine externen JS-Deps. CSS inline, hell/dunkel.
  Produktdaten stecken als JS-Arrays direkt in der Datei. Läuft ohne Server (Datei im Browser öffnen).
- **Regeneration:** `template.html` + `live.json` → `generate.py` erzeugt die HTML neu.
  `template.html` ist identisch zur Seite, aber mit Platzhaltern `__AVAIL_DATE__`, `__LIVE__`,
  `__NEWPRODUCTS__`. Nur die **Live-Verfügbarkeit** wird so aktualisiert; kuratierte Inhalte
  (Preise, Nährwerte, Scores, Notizen, Bilder) bleiben in der Vorlage stabil.

### Build / Run
```bash
python3 refresh.py                                        # Live-Verfügbarkeit holen + Seite neu erzeugen
python3 generate.py template.html live.json index.html    # nur Seite neu erzeugen (ohne Netz)
# oder Datei einfach direkt im Browser öffnen
```
`refresh.py` aktualisiert NUR `availDate` + `live` + `variants` (mit Retry/Backoff gegen
Shopify-503), hängt einen Tages-Snapshot an `history.json` an und schlägt neue Katalog-Produkte
lediglich als Kandidaten vor — `newProducts` bleibt kuratiert.

Seit dem Feature-Paket vom 17.07.2026 außerdem: `variants` in `live.json` ([variantId, Sorte,
kaufbar, Preis]) speist die **Sorten-Anzeige** und den **Merkzettel mit 1-Klick-Warenkorb**
(`/cart/<variantId>:<qty>`-Permalink, localStorage-State, KEIN Checkout-Bot); Vergleichsmodus
(max. 3), Deep-Links im Hash (`#riegel?q=&f=avs&sort=&view=table`), Score-Popover, Tablist mit
Pfeiltasten, PWA (manifest.json/sw.js/favicon.svg, SW nur über http), JSON-LD zur Laufzeit,
Produktbilder lokal unter `img/` (IMG-Map zeigt auf lokale Pfade, `imgURL()` hängt nur an
http-URLs einen width-Parameter an). Wöchentlicher CI-Refresh: `.github/workflows/refresh.yml`.
Kein Test-Framework vorhanden. **Verifikation via Headless-Browser** (empfohlen):
Playwright/Chromium laden `index.html`, auf `pageerror`/console-errors prüfen und Screenshots
machen. `net::ERR_...`/„Failed to load resource" von Bild-URLs sind KEINE JS-Fehler (externe CDN).

## Datenmodell (in der HTML, `const PRODUCTS`)
Felder je Produkt: `id, cat, name, note, price, size, servings, perServ?, protein, sugar, kcal,
rating, reviews, flavors, avail, tags[], pick?, pickTxt?, url, img, varAvail?, varTotal?`.
Kategorien: `proteine, riegel, snacks` (bekommen Score) · `supplements, chunky, kochen`
(bekommen nur einen Preis-Leistungs-Balken). `IMG`-Map hält die Produktbild-URLs (Shopify-CDN),
werden zu `p.img` gemerged; `onerror` → farbiger Platzhalter.

## Scoring (nur proteine/riegel/snacks)
Min-Max-Normalisierung **innerhalb der Kategorie**. Teil-Scores:
- **Nährwerte** = 0.6·norm(Proteindichte g/100kcal) + 0.4·(1−norm(Zucker))
- **Preis-Leistung** = 1 − norm(€ pro g Protein)
- **Geschmack** = 0.7·norm(Rating) + 0.3·norm(log10(Reviews))
- **Gesamt** = 0.35·Nährwerte + 0.30·Preis-Leistung + 0.35·Geschmack; fehlende Teile werden
  ausgelassen und die Gewichte anteilig neu normiert. Werte 0–100.

## Live-Verfügbarkeit (WICHTIG)
- `const LIVE = {id:[verfügbar, gesamt]}` = Anzahl kaufbarer Varianten / Gesamt (aus Shopify).
- Status wird abgeleitet: `0 → ausverkauft`, `alle → auf Lager`, `teils → limitiert`.
- Quelle: `https://morenutrition.de/products/<handle>.js` (pro Produkt `available` + Varianten)
  und `https://morenutrition.de/products.json?limit=250` (Katalog / neue Produkte).
- **NIEMALS** den `.js`-Preis übernehmen: der günstigste Varianten-Preis ist oft nur eine
  2,99-€-Probiergröße. Preise sind kuratierte Standardgrößen und bleiben fix.
- Wöchentliche Auto-Aktualisierung läuft aktuell als Cowork-Scheduled-Task (Runbook liegt im
  claude.ai-Projekt „moore vergelicher"). Für die App-Version besser durch einen Cron/CI-Job
  ersetzen, der `generate.py` mit frischer `live.json` ausführt (siehe ROADMAP).

## Affiliate
`const AFF = { enabled, moreParam, amazonTag, moreCode, disclosure }`. `affLink(url)` hängt bei
`enabled:true` den Tracking-Parameter an MORE-/Amazon-Links; Werbehinweis-Bar + Vorteilscode
werden dann eingeblendet. Standard `enabled:false` (Links bleiben sauber). Aktivieren = Werte
setzen. In DE ist der Werbehinweis Pflicht — nicht entfernen.

## Constraints / Non-Goals (bitte einhalten)
- **KEIN automatischer Checkout-Bot.** Nicht im Namen der Kunden im MORE-Shop bestellen und
  keine Zahlungsdaten speichern/verarbeiten (ToS-Verstoß, DSGVO/PCI-Haftung). Stattdessen die
  legale Variante bauen: **vorbefüllter Shopify-Warenkorb-Link** (`/cart/<variantId>:<qty>,…`)
  + optionale **Restock-Benachrichtigung**. Siehe ROADMAP.
- Preise/Nährwerte/Scores sind kuratiert und dürfen nicht automatisch überschrieben werden.
- Keine externen JS-Frameworks in `index.html` ohne guten Grund (self-contained soll bleiben,
  solange es eine statische Seite ist). Ein späteres Backend darf natürlich moderner sein.

## Stil
Deutsch in der UI. Klar, wenig Formatierung. Barrierearme, in hell/dunkel validierte Farben
(Kategorien = feste Farbslots; Status good/warn/crit nur für Verfügbarkeit).

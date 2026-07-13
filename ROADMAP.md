# ROADMAP — MORE Nutrition Vergleich

Priorisierte Ausbaustufen mit Akzeptanzkriterien. Reihenfolge ist ein Vorschlag.

## 1. 1-Klick-Warenkorb (vorbefüllter Shopify-Link) — *statisch, kein Backend*
Kunden stellen auf der Seite einen Warenkorb zusammen und landen per Klick im MORE-Shop mit
allem schon im Korb (Checkout macht der Kunde selbst — **kein** automatischer Kauf).
- Shopify-Cart-Permalink: `https://morenutrition.de/cart/<variantId>:<qty>,<variantId>:<qty>`
  (optional `?discount=<code>` und Affiliate-Parameter anhängen).
- **Varianten-IDs holen** aus `https://morenutrition.de/products/<handle>.js` (`variants[].id`)
  bzw. `products.json`. Pro Produkt Sorte/Größe wählbar machen (nur kaufbare Varianten anbieten).
- „Merkzettel"/Warenkorb-State clientseitig (kein `localStorage` in Cowork-Artefakten; als echte
  App ist `localStorage` ok).
- **Akzeptanz:** Nutzer wählt N Produkte+Varianten → „Zum Warenkorb"-Button öffnet MORE mit exakt
  diesen Positionen; ausverkaufte Varianten sind nicht wählbar; Affiliate-Parameter ist dran.

## 2. Restock-Alerts — *braucht kleines Backend*
„Sag mir Bescheid, wenn X wieder da ist."
- Backend speichert Abos (E-Mail + gewünschte Variante). Ein Cron prüft regelmäßig die
  Variant-`available`-Flags (gleiche Quelle wie die Verfügbarkeits-Pipeline) und mailt bei
  Wechsel auf verfügbar — mit dem 1-Klick-Warenkorb-Link aus (1).
- Optionen: Serverless (Cloudflare Workers/Vercel/Supabase) + Mailversand (Resend/Postmark).
  DSGVO: Double-Opt-In, Abmeldelink, Datensparsamkeit.
- **Akzeptanz:** Anmeldung funktioniert (Double-Opt-In), Cron erkennt Restock, Mail kommt an
  und der Link führt in den vorbefüllten Warenkorb.

## 3. Affiliate scharf schalten
- Bei MORE bewerben: morenutrition.de/pages/join-us. Parallel **Amazon PartnerNet** für die
  Amazon-Links (niedrige Hürde) und ggf. Netzwerk (Sovrn/Awin).
- In `index.html`: `AFF.enabled=true` + `moreParam`, `amazonTag`, `moreCode` setzen.
- Amazon-Links je Produkt ergänzen (Suchlink oder ASIN-Deeplink) über `affLink()`.
- **Akzeptanz:** Links tragen die Referral-Parameter, Werbehinweis + Vorteilscode sichtbar,
  DSGVO-konform (Impressum/Datenschutz vorhanden).

## 4. Deployment & automatischer Rebuild
- Statisches Hosting: Netlify / Vercel / Cloudflare Pages / GitHub Pages.
- Wöchentlichen Verfügbarkeits-Refresh von der Cowork-Scheduled-Task auf **CI** umziehen
  (z. B. GitHub Actions: Handles abrufen → `live.json` schreiben → `generate.py` → deploy).
  Achtung: die Abfrage muss die Shopify-`.js`/`.json`-Endpunkte serverseitig lesen.
- **Akzeptanz:** Push deployt automatisch; wöchentlicher Job aktualisiert die Verfügbarkeit ohne
  manuelles Zutun.

## 5. Datenqualität / Vervollständigung
- Neue Produkte (Protein Tortilla Chips, FIZI, Essentials O3-D3-K2, DAILY100, Skin Structure
  Formula, More Breakfast Cup) mit Nährwerten/Preis/Score voll aufnehmen.
- Bewertungen/Reviews periodisch aktualisieren (aus den Produktseiten).

## 6. Recht / Betrieb (DE)
- Impressum + Datenschutzerklärung, Affiliate-/Werbekennzeichnung (bereits im Code als Hinweis),
  Cookie-/Consent-Banner nur falls Tracking/Analytics dazukommt.
- Kein Checkout-Bot, keine Speicherung fremder Zahlungsdaten (siehe CLAUDE.md → Constraints).

## Bekannte Nuancen
- `.js`-Preis = oft nur Probengröße → Preise bleiben kuratiert.
- Externe Produktbilder (Shopify-CDN) laden je nach Umgebung; `onerror`-Fallback vorhanden.
- „verfügbar" im Shop heißt: mind. eine Variante kaufbar — deshalb zeigt die Seite `X/Y Varianten`.

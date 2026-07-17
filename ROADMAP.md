# ROADMAP — MORE Nutrition Vergleich

Priorisierte Ausbaustufen mit Akzeptanzkriterien. Reihenfolge ist ein Vorschlag.

> **Stand 17.07.2026:** Punkt 1 (Merkzettel + 1-Klick-Warenkorb) ist umgesetzt, ebenso
> Vergleichsmodus, Deep-Links, Sorten-Anzeige, Score-Popover, PWA/SEO-Grundausstattung,
> lokale Produktbilder. Punkt 5 ist für 8 Neuprodukte erledigt (Breakfast Cup entpuppte
> sich als Zubehör-Lunchpot und bleibt draußen).
> **Veröffentlichung:** Repo ist gepusht → https://github.com/Biyan2744/more-nutrition-vergleich
> (public, nötig für kostenloses Pages). Der wöchentliche CI-Refresh (`refresh.yml`, Mo 06:00 UTC)
> ist damit **aktiv**; sein Deploy-Job schlägt fehl, bis Pages aktiviert ist — erwartet.
> `pages.yml` (Deploy je Push) ist **manuell deaktiviert** (`gh workflow enable pages` zum
> Reaktivieren). **Launch-Checkliste, erst NACH gekauftem Impressum:** (a) Platzhalter in
> impressum.html/datenschutz.html füllen + Entwurfsboxen raus, (b) solange keine
> Bildfreigabe von MORE vorliegt: `SHOW_PRODUCT_IMGS=false` in template.html + regenerieren
> (Schalter existiert, beide Modi verifiziert), (c) Settings → Pages → Source
> „GitHub Actions", (d) `gh workflow enable pages`, (e) 404-Seite live nachtesten.
> Impressum: Biyan will die Privatadresse nicht veröffentlichen und kauft **ganz am Ende**
> einen Impressum-Service (ladungsfähige Anschrift); bis dahin bleibt Pages aus
> (Impressumspflicht). Offen: 2 (Restock-Alerts, braucht Backend), 3 (Affiliate).
> **Modern-Refresh (17.07.):** Hero als Verlaufs-Panel (Markengrün→Card + dezenter Gold-Glow,
> 22px-Radius) mit größerer Display-Typo und integrierten Trust-Pills; Design-Tokens moderner
> (Radius 14→16px, weichere/gestufte Schatten + neues --shadow-lg); Kennzahlen-Kacheln größer
> mit Hover-Lift; Abschnitts-Überschriften mit grünem Akzent-Tick; Kategorie-Chips + Karten
> mit lebendigerem Hover. Hero-H1 auf „Alle MORE-Nutrition-Produkte im ehrlichen Vergleich"
> (Suppwert-konsistent, ohne das beim bildlosen Launch unzutreffende „echte Produktbilder").
> Beide Themes AA-kontraststark geprüft.
> **Empfehlungen-Tab + schlanke Übersicht (17.07.):** Übersicht auf eine ruhige Landeseite
> reduziert (Hero, KPIs, Trust, Restock-Radar, Kategorie-Sprung); die Best-of-Inhalte
> (Bestenlisten, Top-Empfehlungen, Neu im Shop) in einen neuen Reiter „Empfehlungen"
> ausgelagert, damit nicht alles auf einmal erschlägt.
> **Bestenlisten (17.07.):** 4 Rekord-Kacheln, live aus den Produktdaten berechnet:
> Meiste Protein fürs Geld (g Eiweiß/€), Meiste Protein/Portion, Höchste Proteindichte
> (g/100 kcal), Meistbewertet – je Kachel der Rekordhalter + Deep-Link.
> **Sets-Reiter (17.07.):** neuer Tab „Sets" mit 7 redaktionell kuratierten Bundles
> (Protein-Fasten / Muskelaufbau / Bestseller-Mix / Beauty / Frühstück & Snacks / Schlank
> kochen / Gute Nacht). Das Protein-Fasten-Set verweist BESCHREIBEND auf die WPF-Methode von
> MORE-Gründer Christian Wolf (öffentlich dokumentiert, Buch + offizielle MPF-Box) und ist
> bewusst NICHT „WPF Starter Paket" genannt (keine Anmutung des offiziellen Wolf-/MORE-Produkts;
> Produkte auf der echt dokumentierten Methode grundiert; Hinweis auf die offizielle MPF-Box im Text).
> Preise+Verfügbarkeit live aus bestBuyable(), 1-Klick legt alle lieferbaren Posten in den
> Merkzettel. Ehrlich als „unsere Empfehlung, keine Kaufdaten" gelabelt (kein „andere kauften
> auch" — dafür fehlen uns als Nicht-Shop die Daten; keine echten Influencer-Namen wegen
> Persönlichkeitsrecht).
> **Vor-Launch-Politur erledigt (17.07.):** Kategorie-Icon-Platzhalter (Launch ohne
> Produktfotos sieht gewollt aus), og:image + summary_large_image, robots.txt/sitemap.xml
> (Domain-abhängig, s. o.), Grundpreise €/kg bzw. €/l auf Karten + als sortierbare
> Tabellenspalte. **Nach-Launch-Ideen:** Verfügbarkeits-Historie aus history.json
> (wächst wöchentlich), Review-Refresh von den Produktseiten, Search Console,
> ggf. Produkt-Unterseiten für SEO, Restock-Alerts (Backend).

## 1. 1-Klick-Warenkorb (vorbefüllter Shopify-Link) — *statisch, kein Backend* ✅
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
- Wöchentlichen Verfügbarkeits-Refresh von der Cowork-Scheduled-Task auf **CI** umziehen —
  `refresh.py` erledigt bereits Abruf + `live.json` + Regeneration in einem Lauf
  (GitHub Actions muss es nur wöchentlich ausführen und deployen).
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

> **Kopf-an-Kopf-Duell im Vergleich (17.07., Vorbild UserBenchmark):** Die Vergleichsseite
> zeigt die ersten beiden gewählten Produkte als großes Duell — zwei Karten mit Bild/Platzhalter,
> Name, Preis und großem Score, „VS" in der Mitte, leere Slots als gestrichelte Einladung.
> Darunter 10 Metrik-Zeilen (Preis, Grundpreis, €/Portion, Portionen, Protein, Zucker,
> Proteindichte, Score, Bewertung, Beliebtheit): Gewinner grün + „+X %"-Vorteil + Richtungs-
> balken; identische Werte ehrlich „gleich"; Zeilen ohne Daten entfallen. Detail-Tabelle
> („Alle Details") bleibt darunter und deckt auch Produkt 3–4 ab.
> **Produkte-Reiter statt 6 Kategorie-Reitern (17.07.):** Die Tab-Leiste schrumpft von 13 auf
> 8 Reiter. Ein Reiter „Produkte" bündelt alles: Kategorie-Chips („Alle" + 6 Kategorien mit
> Zählern) als Filter, Standard „Alle" zeigt alle 56 gruppiert in Kategorie-Sektionen mit
> farbigen Überschriften; Suche/Filter/Sortierung wirken über alle Kategorien; Tabellen-Ansicht
> bekommt im Alle-Modus eine sortierbare Kategorie-Spalte. Alte Deep-Links (#proteine?q=…)
> bleiben die Wahrheit und routen auf den Produkte-Reiter mit gesetztem Chip.
> **Katalog-Vollständigkeit (17.07.):** kompletten Live-Katalog (104 Einträge) gegen unsere
> Produkte abgeglichen. Ergebnis: nur 2 echte Einzelprodukte fehlten → hinzugefügt
> (**Zerup Zero Sirup** 65 ml/48 Sorten; **Every Workout 3.0**, die günstigere Altversion,
> bestehendes umbenannt in „4.0"). Jetzt 56 Produkte. Die restlichen ~48 Katalog-Einträge sind
> bewusst ausgeschlossen (15 Bücher, 12 Bundles/Multipacks, ~11 Tasterboxen/Sets/Starterkits,
> 5 Zubehör, Gutschein/Pfand/Kühlpack) — keine vergleichbaren Einzelprodukte. Falls Bundles
> doch gewünscht: eigene Entscheidung (verzerren den €/Portion-Vergleich, rotieren stark).
> **Vergleich-Reiter + Portionen (17.07.):** Neuer Tab „Vergleich" – Produkte per Suche
> hinzufügen und bis zu 4 direkt gegenüberstellen (inline-Tabelle, gleiche cmp-Auswahl wie die
> Karten-Häkchen, beide Wege synchron; Kapazität von 3 auf 4 erhöht). Vergleichstabelle +
> Produktkarten zeigen jetzt „Portionen gesamt" bzw. „Größe · N Portionen", wo die Daten es
> hergeben (servings-Feld; bei 1-Portion-/servingslosen Produkten weggelassen).
> **Shop-Fenster (17.07.):** Der „+ andere Anbieter"-Modus zeigt statt einer Dauer-Zeile auf
> jeder Karte einen kompakten Button „Auch bei anderen Shops", der ein kleines Modal öffnet:
> pro Produkt die Anbieter als große Link-Zeilen (Amazon = kuratierter Direktlink → später der
> Affiliate-Link via affLink; Drogerien/Fitmart = Produktsuche). Schließt per x / Scrim / Escape.

## Rechtliche Leitplanken (Recherche 17.07.2026 — Einschätzung, keine Rechtsberatung)
- **Seitentyp ist legitim:** unabhängige, redaktionelle Produktvergleiche über eine Marke sind
  zulässig; die Markennennung im Text ist erlaubt (beschreibende Nutzung, § 23 MarkenG).
- **Marke nicht im Eigennamen:** Domain/Repo/Wortmarke ohne „MORE" (BGH I ZR 236/16; Fall
  IKEAhackers). → Erledigt durch Umbenennung in **Suppwert** (17.07.); Domain-Kandidat
  suppwert.de war zum Recherchezeitpunkt frei (DENIC-RDAP 404) — Registrierung macht Biyan.
- **Produktbilder = offenes Risiko:** die 54 Fotos von morenutrition.de sind ohne Lizenz
  abmahnbar (Unterlassung + Schadensersatz je Bild). Vor dem Live-Gang: Farb-Platzhalter
  (onerror-Fallback existiert) ODER Freigabe von MORE (in Partner-Bewerbung mit anfragen).
  Biyan hat entschieden, das Repo trotz der Bilder vorerst public zu lassen (17.07.).
- **Beim Aktivieren von Affiliate:** Kennzeichnungspflicht (§ 5a UWG/§ 6 DDG) — Werbehinweis-Bar
  ist verkabelt; Datenschutz-Abschnitt 5 VORHER aktualisieren.
- **Ranking-Transparenz** (P2B/UWG): Hauptparameter offenlegen — durch die öffentliche
  Score-Methodik bereits erfüllt.

## Bekannte Nuancen
- `.js`-Preis = oft nur Probengröße → Preise bleiben kuratiert.
- Externe Produktbilder (Shopify-CDN) laden je nach Umgebung; `onerror`-Fallback vorhanden.
- „verfügbar" im Shop heißt: mind. eine Variante kaufbar — deshalb zeigt die Seite `X/Y Varianten`.

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
> „GitHub Actions", (d) `gh workflow enable pages`, (e) 404-Seite live nachtesten,
> (f) `FEEDBACK_MAIL` in template.html auf die Impressums-Kontaktadresse setzen — dann
> bekommen die Community-Wünsche ihren „Per E-Mail senden"-Knopf (bis dahin nur lokal).
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
> ggf. Produkt-Unterseiten für SEO, Restock-Alerts (Backend). **Set-Zähler (18.07. geklärt):**
> „so oft bestellt" geht NIE zuverlässig (Bestellung passiert bei MORE, wir sehen sie nicht;
> erfundene Kaufzahlen sind tabu). Ehrlich möglich: (a) nach Partner-Freischaltung echte
> „über unseren Link bestellt"-Zahlen aus dem Partner-Dashboard, falls das Programm Sub-IDs
> je Set erlaubt; (b) globaler anonymer Klick-Zähler „X-mal in den MORE-Warenkorb gelegt"
> via Serverless (Cloudflare Worker, ohne Cookies, Datenschutz-§-Ergänzung) — sinnvoll
> zusammen mit dem Restock-Alerts-Backend umzusetzen.

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

> **Community-Ausbau: produktgebundene Wünsche & Kritik (18.07.):** Das Wunsch-Formular
> bindet Wünsche jetzt an ein KONKRETES Produkt: Auswahl über die (dafür zu `openGallery`
> generalisierte) Duell-Produkt-Galerie (62 Kacheln, Live-Suche, Gewähltes markiert/gesperrt)
> statt des Freitext-„Betrifft"-Felds; neue Wunsch-Art **„Produkt-Kritik"**. Produktbezug ist
> bei „Neue Sorte" + „Produkt-Kritik" Pflicht (Validierung: roter Rahmen + Hinweis), bei
> „Sonstiges" optional, bei „Neues Produkt"/„Verbesserung der Seite" ausgeblendet — der
> Wechsel dorthin verwirft die Auswahl, damit nichts unsichtbar mitgespeichert wird. Bei
> Sorten-Wünschen zeigt ein Hinweis die ECHTEN vorhandenen Sorten aus den Live-Varianten
> (parseVariants, max. 8 + „und N weitere", „Standard" gefiltert; Fallback: kuratierte
> flavors-Angabe) — so wünscht sich niemand, was es schon gibt. Wünsche speichern
> `prodId` + Namens-Snapshot; Liste und Auswahl-Chip zeigen den 28px-Thumb
> (SHOW_PRODUCT_IMGS-launch-sicher via thumbHTML), der mailto-Betreff nennt das Produkt.
> Alt-Wünsche mit Freitext-prod bleiben lesbar (ohne Thumb). Intro ehrlich ergänzt:
> Feedback landet bei Suppwert, nicht direkt bei MORE. Dynamische Textarea-Platzhalter
> je Wunsch-Art.
> **Anbieter-Ansicht II (18.07.):** Im „+ andere Anbieter"-Modus zeigen jetzt ALLE Set-Posten
> (auch lieferbare) ihre Anbieter-Links — man bekommt jedes Produkt theoretisch auch woanders.
> Recherche-Ergebnis zur Bestands-Frage: KEIN Fremd-Shop ist offen abfragbar (Fitmart live
> getestet: kein offenes Shopify-JSON; dm/Rossmann/Müller ohne offene APIs; Amazon nur via
> PartnerNet-Product-Advertising-API nach Freischaltung → als Nach-Launch-Option notiert).
> Live-Bestand bleibt ehrlich MORE-exklusiv.
> **Reiter-Umbau IV: Sets vereint + Rabatte + Community-Wünsche + Angebots-Filter (18.07.):**
> (a) Sets & Community-Sets sind wieder EIN Reiter mit prominentem Umschalter „Unsere Sets /
> Community & Creator" (Segment-Buttons); Legacy-/Share-Hash `#community` routet auf die
> Community-Ansicht, der Umschalter schreibt `#sets`/`#community`. (b) Neuer Reiter
> **„Rabatte"**: kuratierte bekannte Codes (ehrlich datiert, ohne Gewähr, Sonntags-Hinweis)
> + „Deine Creator-Codes": lokale Liste, Kopieren, und EIN Code als aktiv setzbar → wandert
> als `?discount=` in den 1-Klick-Warenkorb-Link (bewusste Nutzer-Wahl; unser Partner-Code
> via AFF bleibt nachrangig und aus, bis die Bewerbung durch ist). (c) Neuer Reiter
> **„Community"** (Wünsche & Vorschläge): Formular (Neue Sorte/Neues Produkt/Verbesserung/
> Sonstiges + Text) → lokal gespeicherte Wunschliste; `FEEDBACK_MAIL`-Konstante ist Launch-
> Platzhalter, danach mailto-Absende-Knopf je Wunsch (Checkliste (f)). (d) Filter
> **„im Angebot"** im Produkte-Reiter (Hash `f=o`): refresh.py liefert jetzt den Shopify-
> Streichpreis (compare_at, 5. VARIANTS-Feld) — echte Shop-Daten statt geratener Rabatte;
> beim Bau live 3 Treffer (Every Workout 3.0, Zerup Zero, Muffinform). Tab-Leiste jetzt 10
> Reiter: Übersicht · Produkte · Vergleich · Empfehlungen · Sets · Rabatte · Community ·
> Ratgeber · Wo kaufen · Info.
> **Zubehör-Kategorie + Set-Reichweite + Galerie-Builder (18.07.):** (a) Neue 7. Kategorie
> **„Zubehör"** (Teal) mit den 6 echten Einzel-Accessoires aus dem Katalog: Premium Shaker
> (3 Farben, live 2/3), Aqua Bottle, Breakfast Cup, Backform, Muffinform, Cosmetic Bag —
> „Wo sind die Shaker?"-Lücke geschlossen; ohne Nährwerte/Score/Grundpreis (size bewusst
> nicht g/ml-parsebar), Bilder nach img/, refresh.py nimmt die Handles automatisch mit
> (62 Produkte im Abgleich). Bücher/Tasterboxen/Bundles bleiben ausgeschlossen. (b) Set-Karten
> + Generator nennen die **Reichweite**: „bei 1 Portion pro Tag reicht das Set ca. X Tage
> (dann ist das erste Produkt leer)" — min(servings) der lieferbaren Posten, nur wo servings
> kuratiert sind, Singular/Plural sauber. (c) **„Eigenes Set erstellen" ist jetzt ein
> Galerie-Builder**: Live-Suche + alle Kategorien als Bild-Kachel-Sektionen (pickov-Muster),
> Kachel-Klick legt Produkt in Standardgröße ins Set, nochmal klicken erhöht die Menge
> (Badge „✓ n× im Set"), je Posten größen-fester Sorten-Select + ✕ + Live-Summe;
> „Merkzettel übernehmen" als optionaler Startpunkt; Teilen/Speichern wie gehabt.
> **Beeren-Akzent + Set-Themen-Icons (18.07.):** Suppwert-Identitätsfarbe `--brand`
> (Himbeer #c13a6b hell / #d95f8f dunkel) ersetzt das Grün an den IDENTITÄTS-Stellen (Hero-
> Tint, sub-h-Ticks, Trust-Dots, „Alle Produkte"-hbar, Anpassen-Checkboxen, Restock-Chip jetzt
> dunkles Beere statt Dunkelgrün, weiß darauf ≈9,4:1) — bewusst EIGENSTÄNDIGER Ton, kein
> MORE-Magenta (Look-alike = Herkunftstäuschung); Score-Metrik-Grün, Kategorie- und
> Status-Farben unangetastet (Datenfarben). Dazu 7 Line-Art-Themen-Icons auf den Set-Karten
> (Uhr/Hantel/Stern/Funkeln/Bowl/Pfanne/Mond auf Set-Akzent, PH_ICONS-Formsprache) — die
> leichte Alternative zur verworfenen KI-Bild-Idee.
> **Motion-Paket (18.07., recherchebasiert):** Nach Best-Practice-Recherche (nur
> transform/opacity, ease-out, ≤300 ms, kleine Wege, IntersectionObserver, reduced-motion
> Pflicht): Scroll-Reveal für Karten/Sektionen (einmalig beim ersten Sichtbarwerden, leichter
> Stagger; Re-Renders beim Tippen animieren bewusst NICHT), Panel-Wechsel-Fade, Overlay- und
> Merkzettel-Leisten-Entrance, Button-Press-Feedback (scale .97), globaler
> :focus-visible-Ring (nicht animiert), Header-Schatten ab Scroll. WICHTIGE Leitplanke aus
> der Verifikation: In versteckten Dokumenten (Hintergrund-Tab/Prerender — auch die
> Browser-Pane rendert so!) feuert IntersectionObserver nie → Reveal initialisiert erst beim
> Sichtbarwerden + Sicherheitsnetz nach 1,6 s; Content darf NIE davon abhängen, dass ein
> Observer ihn einblendet.
> **Sets-Anpassen (18.07.):** *(Nachtrag: Sorten-Wechsel nur innerhalb derselben GRÖSSE —
> 600 g bleibt 600 g, keine Probier-/XL-Größen im Select; Referenz ist die Set-Variante
> (bei Community-Sets fest gepinnt, inkl. ehrlichem „in der Set-Größe zzt. ausverkauft"-
> Hinweis), bei kuratierten Sets die Standardgröße via bestBuyable.)*
> „Anpassen – Sorte & Auswahl"-Button unter jeder Set-Karte
> (kuratiert + Community): Dialog mit Häkchen je Posten (rein/raus) und Sorten-/Größen-Select
> (nur kaufbare Varianten, Preis je Option), Live-Summe + Zähler, Übernahme in den Merkzettel
> mit exakt den gewählten Varianten; ausverkaufte Posten erscheinen mit Anbieter-Links.
> Tipp-Note verweist auf den Weiterteilen-Weg (Merkzettel → Eigenes Set erstellen).
> **Sets-Ausbau III: WPF-Name + Warenkorb-Split + Community-Reiter + Code-Plumbing (18.07.):**
> (a) „Protein-Fasten-Set" heißt jetzt **„WPF-Paket"** (Biyan: darunter kennt es jeder) — mit
> SICHTBARER Inoffiziell-Zeile unterm Titel („nicht die offizielle MPF-Box"), weil die
> WPF-Anmutungs-Vorsicht bewusste Rechts-Linie bleibt und der why-Disclaimer eingeklappt ist.
> (b) **Warenkorb-Split:** Führt der Merkzettel Posten, die MORE gerade nicht liefern kann,
> fängt „Zum MORE-Warenkorb" den Klick ab und zeigt einen Aufteil-Dialog: „Bei MORE holen (n)"
> mit 1-Klick-Permalink nur der lieferbaren + „Woanders holen (n)" je Posten mit den besten
> bekannten Alternativen (Amazon-Direktlink zuerst, sonst Suche) — ehrlich ohne
> „Günstigst"-Garantie (keine Live-Preise anderer Shops). Voll lieferbar = Direktlink wie immer.
> (c) **Eigener Reiter „Community-Sets"** (9. Tab, Hash `#community`): Creator-Chips („Alle" +
> je Creator + „Ohne Creator", erscheinen erst ab einem benannten Creator), eigener
> Erstellen-Button; Sets-Tab behält kuratierte Sets + Generator, seine Such-/Filter-Optionen
> wirken nur noch dort; Set-Import landet jetzt im Community-Reiter. (d) **Auto-Rabattcode:**
> Shopify-Cart-Permalink unterstützt `?discount=CODE` — verkabelt in cartURL, aktiv erst mit
> eigenem Partner-Code (AFF.enabled + moreCode); fremde Codes werden nicht auto-eingetragen.
> **Sets-Ausbau II: Bestands-Generator + Anbieter-Wahl (18.07.):** *(Nachträge: Generator-Box
> ist zuklappbar — natives details/summary, startet zu; ein generierter Vorschlag überlebt
> das Zuklappen. Sets-Suchfeld in der Optionsleiste filtert kuratierte + Community-Sets live
> über Titel/Beschreibung/Produktnamen/Creator, mit ehrlichen Kein-Treffer-Hinweisen.
> Produktbilder in Sets: überlappender Bild-Stapel am Karten-Kopf (Hover fächert auf,
> Ausverkauftes grayscale, „+N" bei >5) + 28px-Thumbs an allen Posten-Zeilen inkl. Generator,
> Builder, Import-Dialog und Ratgeber-Smart-Warenkorb — mit Kategorie-Icon-Fallback, also
> SHOW_PRODUCT_IMGS-launch-sicher. Karten visueller: Reihenfolge Titel→Bilder→Posten/Preise,
> Beschreibung eingeklappt hinter „Warum dieses Set?", Hover-Lift auf der Karte. Offen/geparkt:
> eigene Creator-Features für Creator-Sets — Biyan will das separat klären.)* (a) „Set aus dem aktuellen
> Bestand generieren": Themen-Chips (die 6 kuratierten GOALS-Pools aus dem Ratgeber) + Budget
> → deterministisches Set NUR aus gerade lieferbaren Produkten via smartCart (Score-Rangfolge,
> Versandschwellen-Logik) — „sinnvoll statt Kram", weil nur thematisch kuratierte Pools in
> Frage kommen, kein Verfügbarkeits-Zusammenwürfeln. Ergebnis: „In den Merkzettel" +
> „Als Set speichern & teilen" (läuft in die Community-Sektion + `#set=`-Link). (b) Anbieter-
> Wahl „Nur MORE-Shop / + andere Anbieter" als Chip-Paar: im Alt-Modus zeigen AUSVERKAUFTE
> Posten in kuratierten + Community-Sets die Anbieter-Links aus shopLinks() (Amazon-Direktlink
> wo kuratiert, sonst Produktsuche) — so verteilt man die Bestellung auf mehrere Shops, wenn
> MORE nicht alles hat. Ehrlichkeits-Note bleibt: 1-Klick-Warenkorb kann nur MORE befüllen,
> andere Anbieter separat bestellen, dort keine Live-Preise/-Verfügbarkeit.
> **Sets-Ausbau: Verfügbarkeits-Filter + Creator-/Community-Sets (18.07.):** (a) Anklick-Option
> „Nur komplett lieferbare Sets" über dem Set-Grid – blendet Sets aus, in denen gerade mindestens
> ein Artikel ausverkauft ist, und nennt die Zahl ehrlich. (b) Neue Sektion „Creator- &
> Community-Sets" OHNE Backend (gleiches Prinzip wie das Merkzettel-Teilen): „Eigenes Set
> erstellen & teilen" macht aus dem aktuellen Merkzettel (dort wählt man die Sorten) ein
> benanntes Set (+ optionaler Creator-Name) und erzeugt einen `#set=vid:qty,…~Name~Creator`-Link
> (navigator.share/Clipboard); das eigene Set landet zusätzlich lokal in der Sektion. Wer den
> Link öffnet, bekommt einen Bestätigungs-Dialog (Posten, Live-Preise, Verfügbarkeit, Summe) und
> kann speichern (localStorage `mn-comsets`, max. 20, Dedupe) oder lieferbare Posten direkt in
> den Merkzettel legen – NIE stille Übernahme, unbekannte Varianten-IDs werden übersprungen.
> WICHTIG (Ehrlichkeit): keine erfundenen Creator/Sets – die Sektion startet leer und erklärt,
> wie sie sich per Link füllt; gespeichert wird nur im Browser, wir sehen die Sets nicht.
> Verifikations-Ritual ergänzt: `node --check` aufs extrahierte Inline-Script (fing einen
> String-Breaker durch ein ASCII- statt deutsches Anführungszeichen).
> **Kategorie-Kombis + Plus erschafft Slots (18.07.):** (a) Die Kategorie-Chips im
> Produkte-Reiter sind jetzt **Mehrfachauswahl**: Antippen kombiniert (z. B. Proteinpulver +
> Snacks nebeneinander als Sektionen), nochmal antippen wählt ab, „Alle" leert; alle 6 an
> normalisiert auf „Alle". Einzelauswahl bleibt die flache Ansicht + alte `#proteine`-Links,
> Kombis teilen sich als `#produkte?cats=a,b` (Reihenfolge stabil = CATORDER, unbekannte Keys
> fallen beim Parsen raus); Tabelle zeigt die Kategorie-Spalte bei allem außer Einzelauswahl.
> (b) Das **Plus im Vergleich erschafft jetzt ein weiteres leeres Feld** (statt die Galerie
> für Slot 1/2 zu öffnen — Biyan-Wunsch): `duelExtra` zählt die per Plus erschaffenen leeren
> Slots, jedes Produkt-Hinzufügen (Galerie-Push, Vergleich-Suche, Karten-Häkchen) verbraucht
> eines, leere Extra-Slots (ab dem 3.) haben ein eigenes ✕ und sind als div[role=button]
> gebaut (kein Button-in-Button-HTML). Produkt-Entfernen lässt erschaffene Leerfelder stehen,
> kollabiert sonst wie bisher auf min. 2.
> **Restock-Countdown im Header (18.07.):** Recherche bestätigte: der große MORE-Wochen-Restock
> + die Sonntags-Aktionen starten üblicherweise **sonntags 11:00 Uhr** (Community-dokumentiert:
> Vorpacklink-Seiten, MORE-App-Push „Sonntag 11 Uhr"; das offizielle Helpcenter nennt bewusst
> KEINE Termine — deshalb überall „ohne Gewähr"). Neuer prominenter Countdown-Chip mittig im
> Header (dunkles Markengrün, Gold-Pulspunkt, weißer Text ≥5:1 in beiden Themes): „MORE-Restock
> · So 11:00 · in X" — tickt sekündlich, unter 24 h als HH:MM:SS; sonntags 11–13 Uhr wechselt er
> auf Gold „Zeitfenster läuft". Zielzeit DST-sicher in Europe/Berlin (Intl-basiert, stimmt auch
> bei fremder Gerätezeitzone; Browser ohne IANA-Zonen zeigen den Chip gar nicht statt falsch).
> Tooltip erklärt Quelle + Merkzettel-Tipp; Radar-Note ergänzt den Sonntags-Hinweis ehrlich.
> Layout: <992 px eigene volle Header-Zeile (Spacer raus, margin-auto statt Flex-Spacer),
> <420 px Theme-Button icon-only (Label bleibt via Clip-Pattern für Screenreader), Daten-Update-
> Chip erst ab 1180 px + kürzeres „⟳ Update in …" (Worst-Case-Countdowntexte eingerechnet).
> Nebenbei gefixt: `.top-in{padding:11px 0}` hatte das seitliche `.wrap`-Padding überschrieben —
> der Header klebte an der Viewport-Kante und war breiter als alle Content-Sektionen.
> **Header-Timer + Creator-Merkzettel-Sharing (18.07.):** (a) Der Header zeigt jetzt dauerhaft
> den ehrlichen Countdown „⟳ Daten-Update in X Tagen Y Std." (nächster Montags-Abgleich,
> gleiche Quelle wie der Radar-Countdown; unter 960 px ausgeblendet). Bewusst KEIN
> Produkt-Release-Timer — MORE nennt keine Termine, wir erfinden keine. (b) „Merkzettel
> teilen" im Merkzettel-Panel erzeugt einen Link (#warenkorb=vid:qty,…), über den andere die
> Zusammenstellung übernehmen können (navigator.share, sonst Clipboard) — die Creator-Idee
> ohne Backend: Empfänger sehen einen Bestätigungs-Dialog mit Posten + Summe (nichts wird
> still überschrieben), unbekannte Varianten-IDs werden übersprungen, Übernahme ersetzt den
> eigenen Merkzettel und führt in den normalen 1-Klick-Warenkorb-Flow.
> **Duell-Slots klickbar + Produkt-Galerie + Plus (17.07.):** Jedes Vergleichsfeld ist
> anklickbar und öffnet eine Galerie aller Produkte (Bilder bzw. Icon-Platzhalter, nach
> Kategorien gruppiert, live durchsuchbar; bereits gewählte gesperrt mit „✓ im Vergleich");
> Klick auf ein gefülltes Feld wechselt das Produkt. Ein „+" rechts erschafft weitere
> Vergleichsfelder (bis 4; Duell-Prozentzeilen nur bei exakt 2, ab 3 übernimmt die Tabelle).
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

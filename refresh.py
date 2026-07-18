#!/usr/bin/env python3
# Holt die aktuelle Verfuegbarkeit je Variante von morenutrition.de und schreibt live.json neu,
# anschliessend wird index.html regeneriert (generate.py). Kuratierte Inhalte (Preise, Naehrwerte,
# Scores, newProducts) werden NICHT automatisch veraendert — neue Katalog-Produkte werden nur als
# Vorschlag ausgegeben (Kuration von Hand, weil der Katalog voller Bundles/Buecher/Zubehoer steckt).
#
# Schreibt zusaetzlich:
#   - live.json "variants": je Produkt [[variantId, Sortenname, 1|0 kaufbar, Preis-EUR], ...]
#     (Basis fuer die Sorten-Anzeige und die 1-Klick-Warenkorb-Permalinks /cart/<id>:<qty>;
#     der Varianten-Preis ist der ECHTE Preis genau dieser Variante und dient nur der
#     Merkzettel-Zwischensumme — die kuratierten Karten-Preise bleiben unberuehrt)
#   - history.json: ein Verfuegbarkeits-Snapshot {datum: {id: [kaufbar, gesamt]}} pro Tag
#
# Nutzung: python3 refresh.py [--no-generate]
import json, re, sys, subprocess, time, urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
MONATE = ["Januar","Februar","Maerz","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]
MONATE[2] = "März"
# Handles, die im Katalog auftauchen, aber keine kuratierbaren Einzelprodukte sind.
# Zubehoer-Begriffe (shaker/bottle/...) stehen seit der Zubehoer-Kategorie (18.07.) NICHT mehr
# drin — neue Accessoires sollen wieder als Kandidaten vorgeschlagen werden.
JUNK = re.compile(r"bundle|tasterbox|multipack|starterkit|refill|kochbuch|box|pfand|gutschein|kuhlpack", re.I)

def fetch(url, tries=4):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r)
        except Exception:
            if attempt == tries - 1:
                raise
            time.sleep(3 * (attempt + 1))  # Shopify drosselt gern mit 502/503

def main():
    tpl = (ROOT / "template.html").read_text(encoding="utf-8")
    pairs = re.findall(r'\{id:"([a-z0-9]+)",cat:"[a-z]+".*?url:"https://morenutrition\.de/products/([a-z0-9-]+)"', tpl)
    data = json.loads((ROOT / "live.json").read_text(encoding="utf-8"))

    live, variants, fails = {}, {}, []
    for pid, handle in pairs:
        try:
            vs = fetch(f"https://morenutrition.de/products/{handle}.js").get("variants", [])
            live[pid] = [sum(1 for v in vs if v.get("available")), len(vs)]
            # 5. Feld: Streichpreis (compare_at_price) fuer die ehrliche "im Angebot"-Erkennung —
            # 0 wenn keiner gesetzt ist; die UI wertet nur compare_at > Preis als Angebot
            variants[pid] = [[v["id"], v.get("title") or "Standard", 1 if v.get("available") else 0, round(v.get("price", 0) / 100, 2), round((v.get("compare_at_price") or 0) / 100, 2)] for v in vs]
        except Exception as e:
            fails.append(f"{pid} ({handle}): {e}")
            if pid in data.get("live", {}):
                live[pid] = data["live"][pid]  # alter Stand statt Luecke
                if pid in data.get("variants", {}):
                    variants[pid] = data["variants"][pid]
        time.sleep(0.4)

    heute = date.today()

    # Tages-Snapshot + Restock-Radar: ehrlich beobachtete Zustandswechsel zwischen den letzten
    # beiden Abgleichen (MORE nennt keine Restock-Termine — wir erfinden auch keine)
    hist_path = ROOT / "history.json"
    hist = json.loads(hist_path.read_text(encoding="utf-8")) if hist_path.exists() else {}
    hist[heute.isoformat()] = live
    hist = dict(sorted(hist.items()))
    hist_path.write_text(json.dumps(hist, ensure_ascii=False), encoding="utf-8")
    dates = sorted(hist.keys())
    data["restocks"] = {}
    if len(dates) >= 2:
        prev = hist[dates[-2]]
        pd = date.fromisoformat(dates[-2])
        data["restocks"] = {
            "since": f"{pd.day}. {MONATE[pd.month - 1]} {pd.year}",
            "back": [k for k, v in live.items() if k in prev and prev[k][0] == 0 and v[0] > 0],
            "gone": [k for k, v in live.items() if k in prev and prev[k][0] > 0 and v[0] == 0],
        }
    print(f"history.json: {len(hist)} Snapshot(s), Radar: +{len(data['restocks'].get('back', []))}/-{len(data['restocks'].get('gone', []))}")

    data["availDate"] = f"{heute.day}. {MONATE[heute.month - 1]} {heute.year}"
    data["live"] = live
    data["variants"] = variants
    (ROOT / "live.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"live.json: {len(live)} Produkte, Stand {data['availDate']}" + (f", {len(fails)} Fallbacks: {fails}" if fails else ""))

    # Katalog: neue Produkte VORSCHLAGEN (newProducts bleibt kuratiert) + Sortiment-Radar
    try:
        catalog, page = [], 1
        while True:
            batch = fetch(f"https://morenutrition.de/products.json?limit=250&page={page}").get("products", [])
            catalog.extend(batch)
            if len(batch) < 250:
                break
            page += 1
            time.sleep(1)

        # Sortiment-Radar ("Neu im Sortiment" vs. nur Restock): wir merken uns je Handle das
        # Datum der ERSTEN Sichtung (catalogSeen). Der allererste Lauf setzt nur die Baseline —
        # sonst waere am Tag 1 das komplette Sortiment "neu". Danach gilt: Handle noch nie
        # gesehen -> neu, 28 Tage sichtbar. Keine Drop-Vorhersage, nur ehrliche Beobachtung.
        heute_iso = heute.isoformat()
        seen = data.get("catalogSeen") or {}
        if not seen:
            data["catalogBaseline"] = heute_iso
        baseline = data.get("catalogBaseline", "")
        for p in catalog:
            seen.setdefault(p["handle"], heute_iso)
        data["catalogSeen"] = seen
        cutoff = (heute - timedelta(days=28)).isoformat()
        in_cmp = {h for _, h in pairs}
        neu = [p for p in catalog
               if seen[p["handle"]] > baseline and seen[p["handle"]] >= cutoff
               and p.get("product_type") not in ("Deposit", "Geschenkgutscheine", "Systemartikel")]
        data["catalogNew"] = sorted(
            [{"title": p["title"], "handle": re.sub(r"[^a-z0-9-]", "", p["handle"]),
              "type": p.get("product_type") or "", "seen": seen[p["handle"]],
              "avail": any(v.get("available") for v in p.get("variants", [])),
              "known": p["handle"] in in_cmp} for p in neu],
            key=lambda x: x["seen"], reverse=True)
        (ROOT / "live.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        print(f"Sortiment-Radar: {len(data['catalogNew'])} neu seit Baseline {baseline} ({len(seen)} Handles beobachtet)")

        known = {h for _, h in pairs} | {n["handle"] for n in data.get("newProducts", [])}
        cands = [p for p in catalog if p["handle"] not in known
                 and p.get("product_type") not in ("Bundle", "Book", "Systemartikel", "Deposit", "Geschenkgutscheine")
                 and not JUNK.search(p["handle"])]
        if cands:
            print("Kandidaten fuer newProducts (von Hand kuratieren):")
            for p in sorted(cands, key=lambda x: x.get("published_at") or "", reverse=True):
                print(f'  {{"name":"{p["title"]}","type":"{p.get("product_type") or "?"}","handle":"{p["handle"]}"}}  # {str(p.get("published_at"))[:10]}')
        else:
            print("Keine neuen Katalog-Kandidaten.")
    except Exception as e:
        print(f"Katalog-Check uebersprungen ({e}) — catalogNew bleibt auf dem alten Stand")

    if "--no-generate" not in sys.argv:
        subprocess.run([sys.executable, str(ROOT / "generate.py"), str(ROOT / "template.html"), str(ROOT / "live.json"), str(ROOT / "index.html")], check=True)

if __name__ == "__main__":
    main()

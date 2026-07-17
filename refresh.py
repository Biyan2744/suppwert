#!/usr/bin/env python3
# Holt die aktuelle Verfuegbarkeit je Variante von morenutrition.de und schreibt live.json neu,
# anschliessend wird index.html regeneriert (generate.py). Kuratierte Inhalte (Preise, Naehrwerte,
# Scores, newProducts) werden NICHT automatisch veraendert — neue Katalog-Produkte werden nur als
# Vorschlag ausgegeben (Kuration von Hand, weil der Katalog voller Bundles/Buecher/Zubehoer steckt).
#
# Nutzung: python3 refresh.py [--no-generate]
import json, re, sys, subprocess, time, urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
MONATE = ["Januar","Februar","Maerz","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]
MONATE[2] = "März"
# Handles, die im Katalog auftauchen, aber keine kuratierbaren Einzelprodukte sind
JUNK = re.compile(r"bundle|tasterbox|multipack|starterkit|refill|kochbuch|box|pfand|gutschein|shaker|bottle|muffinform|backform|kosmetiktasche|kuhlpack", re.I)

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

    live, fails = {}, []
    for pid, handle in pairs:
        try:
            variants = fetch(f"https://morenutrition.de/products/{handle}.js").get("variants", [])
            live[pid] = [sum(1 for v in variants if v.get("available")), len(variants)]
        except Exception as e:
            fails.append(f"{pid} ({handle}): {e}")
            if pid in data.get("live", {}):
                live[pid] = data["live"][pid]  # alter Stand statt Luecke
        time.sleep(0.4)

    heute = date.today()
    data["availDate"] = f"{heute.day}. {MONATE[heute.month - 1]} {heute.year}"
    data["live"] = live
    (ROOT / "live.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"live.json: {len(live)} Produkte, Stand {data['availDate']}" + (f", {len(fails)} Fallbacks: {fails}" if fails else ""))

    # Neue Katalog-Produkte nur VORSCHLAGEN (newProducts bleibt kuratiert)
    try:
        catalog, page = [], 1
        while True:
            batch = fetch(f"https://morenutrition.de/products.json?limit=250&page={page}").get("products", [])
            catalog.extend(batch)
            if len(batch) < 250:
                break
            page += 1
            time.sleep(1)
        known = {h for _, h in pairs} | {n["handle"] for n in data.get("newProducts", [])}
        cands = [p for p in catalog if p["handle"] not in known
                 and p.get("product_type") not in ("Bundle", "Book", "Accessoire", "Systemartikel", "Deposit", "Geschenkgutscheine")
                 and not JUNK.search(p["handle"])]
        if cands:
            print("Kandidaten fuer newProducts (von Hand kuratieren):")
            for p in sorted(cands, key=lambda x: x.get("published_at") or "", reverse=True):
                print(f'  {{"name":"{p["title"]}","type":"{p.get("product_type") or "?"}","handle":"{p["handle"]}"}}  # {str(p.get("published_at"))[:10]}')
        else:
            print("Keine neuen Katalog-Kandidaten.")
    except Exception as e:
        print(f"Katalog-Check uebersprungen ({e})")

    if "--no-generate" not in sys.argv:
        subprocess.run([sys.executable, str(ROOT / "generate.py"), str(ROOT / "template.html"), str(ROOT / "live.json"), str(ROOT / "index.html")], check=True)

if __name__ == "__main__":
    main()

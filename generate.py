#!/usr/bin/env python3
# Erzeugt die MORE-Nutrition-Vergleichsseite aus Vorlage + live.json.
# Nur die Live-Verfuegbarkeit wird ersetzt; kuratierte Inhalte (Preise, Naehrwerte,
# Scores, Notizen) bleiben unveraendert in der Vorlage.
#
# Nutzung: python3 generate.py [template.html] [live.json] [out.html]
import json, re, sys

tpl_path  = sys.argv[1] if len(sys.argv) > 1 else 'template.html'
live_path = sys.argv[2] if len(sys.argv) > 2 else 'live.json'
dest      = sys.argv[3] if len(sys.argv) > 3 else 'more-nutrition-vergleich.html'

live = json.load(open(live_path, encoding='utf-8'))
tpl  = open(tpl_path, encoding='utf-8').read()

def js(o):
    # JSON fuer den <script>-Kontext: "<" wird zu \\u003c, damit ein "</script>" in
    # Shopify-Titeln (Fremddaten aus dem woechentlichen Abgleich!) nicht den
    # Script-Block der Seite beendet und die komplette Seite killt (Bug-Jagd 18.07.).
    return json.dumps(o, ensure_ascii=False).replace('<', '\\u003c')

# EIN Durchgang statt Replace-Kette (Bug-Jagd 18.07.): bei der Kette haette ein
# Platzhalter-String INNERHALB frueher eingesetzter Shopify-Daten (z. B. "__RESTOCKS__"
# in einem Produkt-Titel) vom naechsten Replace mitten im JSON ersetzt werden koennen.
# re.sub scannt nur die Vorlage; Ersetzungs-Text wird nie erneut gescannt.
repl = {
    '__AVAIL_DATE__': live['availDate'],
    '__LIVE__': js(live['live']),
    '__VARIANTS__': js(live.get('variants', {})),
    '__RESTOCKS__': js(live.get('restocks', {})),
    '__CATALOGNEW__': js(live.get('catalogNew', [])),
    '__NEWPRODUCTS__': js(live['newProducts']),
}
out = re.sub(r'__[A-Z_]+__', lambda m: repl.get(m.group(0), m.group(0)), tpl)

# newline='\n': ohne das schreibt Windows CRLF, der Ubuntu-CI-Refresh LF — jeder Wechsel
# waere ein Ganzdatei-Diff im Auto-Commit
open(dest, 'w', encoding='utf-8', newline='\n').write(out)
print('generated ->', dest, '| availDate', live['availDate'],
      '| live', len(live['live']), '| new', len(live['newProducts']))

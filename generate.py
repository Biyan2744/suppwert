#!/usr/bin/env python3
# Erzeugt die MORE-Nutrition-Vergleichsseite aus Vorlage + live.json.
# Nur die Live-Verfuegbarkeit wird ersetzt; kuratierte Inhalte (Preise, Naehrwerte,
# Scores, Notizen) bleiben unveraendert in der Vorlage.
#
# Nutzung: python3 generate.py [template.html] [live.json] [out.html]
import json, sys

tpl_path  = sys.argv[1] if len(sys.argv) > 1 else 'template.html'
live_path = sys.argv[2] if len(sys.argv) > 2 else 'live.json'
dest      = sys.argv[3] if len(sys.argv) > 3 else 'more-nutrition-vergleich.html'

live = json.load(open(live_path, encoding='utf-8'))
tpl  = open(tpl_path, encoding='utf-8').read()

out = (tpl
       .replace('__AVAIL_DATE__', live['availDate'])
       .replace('__LIVE__', json.dumps(live['live'], ensure_ascii=False))
       .replace('__NEWPRODUCTS__', json.dumps(live['newProducts'], ensure_ascii=False)))

open(dest, 'w', encoding='utf-8').write(out)
print('generated ->', dest, '| availDate', live['availDate'],
      '| live', len(live['live']), '| new', len(live['newProducts']))

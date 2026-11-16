"""Buduje index.html: aplikacja Biblia v5 + talia mitologiczna z v3 (dane bez zmian).
Uruchomienie: python tools/build_multizestaw.py  (z katalogu repo)"""
import json, re, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
bib = (root/'apps/kalambury_biblia_v5.html').read_text(encoding='utf-8')
myt = (root/'apps/kalambury_mitologia_v3.html').read_text(encoding='utf-8')
myth = json.loads(re.search(r'const CARDS = (\[.*?\]);', myt).group(1))
m = re.search(r'const DATASETS = (\{.*?\});\n', bib)
ds = json.loads(m.group(1))
assert ds['myth'] == [], 'v5 ma juz dane myth'
ds['myth'] = myth
out = bib[:m.start(1)] + json.dumps(ds, ensure_ascii=False, separators=(',', ':')) + bib[m.end(1):]
btn_b = '<button class="deck-tab" type="button" data-deck="bible"'
btn_m = ('<button class="deck-tab" type="button" data-deck="myth" aria-pressed="false">'
         f'<span class="deck-symbol">μ</span> Mitologizmy <small>{len(myth)}</small></button>\n  ')
assert out.count(btn_b) == 1
out = out.replace(btn_b, btn_m + btn_b)
out = out.replace('<title>Kalambury αω — bibliczne / wersja kanoniczna', '<title>Kalambury αω — biblizmy i mitologizmy', 1)
# logo: .brand ma text-transform:uppercase, przez co α ω wyswietla sie jako 'AΩ'
out = out.replace('</style>', '.brandmark{text-transform:none}</style>', 1)
(root/'index.html').write_text(out, encoding='utf-8')
print('index.html:', len(ds['bible']), 'biblizmow,', len(myth), 'mitologizmow')

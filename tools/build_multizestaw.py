"""Buduje index.html: interfejs Biblia v5 + talia biblijna z kanonicznej bazy JSON
+ talia mitologiczna z v3 (dane bez zmian).
Uruchomienie: python tools/build_multizestaw.py  (z katalogu repo)

Źródło prawdy dla biblizmów: data/biblia_baza_kanoniczna.json (status "gra" = karta w talii).
Dane biblijne osadzone w apps/kalambury_biblia_v5.html są ignorowane."""
import json, re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
bib = (root/'apps/kalambury_biblia_v5.html').read_text(encoding='utf-8')
myt = (root/'apps/kalambury_mitologia_v3.html').read_text(encoding='utf-8')
myth = json.loads(re.search(r'const CARDS = (\[.*?\]);', myt).group(1))
base = json.loads((root/'data/biblia_baza_kanoniczna.json').read_text(encoding='utf-8'))
records = base['records']
bible = [{'id': r['id'], 'haslo': r['haslo'], 'karta': r['haslo'], 'znaczenie': r['znaczenie'], 'poziom': r['poziom'],
          'raw': r['warianty'][0], 'numery_zrodlowe': r['numery_uczniowskie'],
          'uwaga': 'Kanoniczny zapis dydaktyczny; źródło: Jan Godyń.'}
         for r in sorted(records, key=lambda r: r['id']) if r['status'] == 'gra']
names = [c['karta'].lower() for c in bible]
assert len(names) == len(set(names)), 'duplikaty hasel w talii biblijnej'
assert all(c['poziom'] in (1, 2, 3, 4, 5) for c in bible)

m = re.search(r'const DATASETS = (\{.*?\});\n', bib)
ds = json.loads(m.group(1))
assert ds['myth'] == [], 'v5 ma juz dane myth'
ds['myth'] = myth
ds['bible'] = bible
out = bib[:m.start(1)] + json.dumps(ds, ensure_ascii=False, separators=(',', ':')) + bib[m.end(1):]

def sub(a, b):
    global out
    assert out.count(a) == 1, a
    out = out.replace(a, b)

btn_b = '<button class="deck-tab" type="button" data-deck="bible"'
sub(btn_b, '<button class="deck-tab" type="button" data-deck="myth" aria-pressed="false">'
           f'<span class="deck-symbol">μ</span> Mitologizmy <small>{len(myth)}</small></button>\n  ' + btn_b)
sub('Biblizmy <small>235</small>', f'Biblizmy <small>{len(bible)}</small>')
sub('347 haseł w wersji czystej; 235 zakwalifikowano do kalamburów. Oryginał i numery źródłowe pozostają w Google Docs.',
    f'{len(records)} haseł w bazie kanonicznej (wersja {base["version"]}); {len(bible)} zakwalifikowano do kalamburów. '
    'Oryginał i numery źródłowe pozostają w Google Docs.')
sub('<title>Kalambury αω — bibliczne / wersja kanoniczna', '<title>Kalambury αω — biblizmy i mitologizmy')
# logo: .brand ma text-transform:uppercase, przez co α ω wyswietla sie jako 'AΩ'
out = out.replace('</style>', '.brandmark{text-transform:none}</style>', 1)
(root/'index.html').write_text(out, encoding='utf-8')
print('index.html:', len(bible), 'biblizmow,', len(myth), 'mitologizmow')

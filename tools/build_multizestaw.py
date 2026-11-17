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
bible = [{'id': r['id'], 'haslo': r['haslo'], 'karta': r.get('karta', r['haslo']), 'znaczenie': r['znaczenie'], 'poziom': r['poziom'],
          'raw': r['warianty'][0], 'numery_zrodlowe': r['numery_uczniowskie'],
          'uwaga': 'Kanoniczny zapis dydaktyczny; źródło: Jan Godyń.'}
         for r in sorted(records, key=lambda r: r['id']) if r['status'] == 'gra']
names = [c['karta'].lower() for c in bible]
assert len(names) == len(set(names)), 'duplikaty hasel w talii biblijnej'
assert all(c['poziom'] in (1, 2, 3, 4, 5) for c in bible)

# Pole "Skad to?" (data/skad.json): [odnosnik, nota] dla id karty w talii
skad = json.loads((root/'data/skad.json').read_text(encoding='utf-8'))
for talia, karty in (('biblia', bible), ('mitologia', myth)):
    for c in karty:
        w = skad[talia].get(str(c['id']))
        if w:
            c['skad'] = {'ref': w[0], 'nota': w[1]}

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
sub('<title>Kalambury αω — bibliczne / wersja kanoniczna', '<title>Kalambury ΑΩ — biblizmy i mitologizmy')
# Alfa i Omega wielkimi literami greckimi (U+0391, U+03A9), nie łacińskim "A"
sub('<span>α</span><span>ω</span>', '<span>Α</span><span>Ω</span>')
sub('<span class="deck-symbol">αω</span>', '<span class="deck-symbol">ΑΩ</span>')
# motywy talii (osobne tlo i kolory dla Biblii i mitologii)
css = (root/'tools/motywy_talii.css').read_text(encoding='utf-8')
out = out.replace('</style>', css + '\n</style>', 1)
sub('function render(){', 'function render(){document.body.dataset.deck=activeDeck;')
# rewers: blok "Skad to?" pod znaczeniem
sub('<p class="def" id="definition"></p></div>',
    '<p class="def" id="definition"></p></div>\n     <div class="origin" id="origin" hidden><div class="label">Skąd to?</div>'
    '<p><span class="origin-ref" id="originref"></span> <span class="origin-note" id="originnote"></span></p></div>')
sub("ui.def.className='def'", "(()=>{const o=document.getElementById('origin'),s=item.skad;o.hidden=!s;if(s){document.getElementById('originref').textContent=s.ref;document.getElementById('originnote').textContent=s.nota?'— '+s.nota:''}})();ui.def.className='def'")
(root/'index.html').write_text(out, encoding='utf-8')
print('index.html:', len(bible), 'biblizmow,', len(myth), 'mitologizmow')

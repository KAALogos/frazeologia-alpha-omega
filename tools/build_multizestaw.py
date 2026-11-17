"""Buduje index.html: interfejs Biblia v5 + talia biblijna z kanonicznej bazy JSON
+ talia mitologiczna z v3 (dane bez zmian).
Uruchomienie: python tools/build_multizestaw.py  (z katalogu repo)
Motyw domyślny: „księga” (tools/motyw_ksiega.css + fonts/eb-garamond).
Poprzedni ciemny motyw: python tools/build_multizestaw.py --motyw talie --podglad  -> preview.html

Źródło prawdy dla biblizmów: data/biblia_baza_kanoniczna.json (status "gra" = karta w talii).
Dane biblijne osadzone w apps/kalambury_biblia_v5.html są ignorowane."""
import json, re, pathlib, sys
MOTYW = sys.argv[sys.argv.index('--motyw') + 1] if '--motyw' in sys.argv else 'ksiega'
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
if MOTYW == 'ksiega':
    # EB Garamond (SIL OFL 1.1, fonts/eb-garamond/OFL.txt), podzbiory jak w @fontsource
    R = {'latin': 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD',
         'latin-ext': 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF',
         'greek': 'U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF'}
    faces = []
    for f in sorted((root/'fonts/eb-garamond').glob('*.woff2')):
        m = re.match(r'eb-garamond-(latin-ext|latin|greek)-(\d+)-(normal|italic)\.woff2', f.name)
        faces.append(f"@font-face{{font-family:'EB Garamond';font-style:{m[3]};font-weight:{m[2]};font-display:swap;"
                     f"src:url(fonts/eb-garamond/{f.name}) format('woff2');unicode-range:{R[m[1]]}}}")
    css = '\n'.join(faces) + '\n' + (root/'tools/motyw_ksiega.css').read_text(encoding='utf-8')
else:
    css = (root/'tools/motywy_talii.css').read_text(encoding='utf-8')
out = out.replace('</style>', css + '\n</style>', 1)
sub('function render(){', 'function render(){document.body.dataset.deck=activeDeck;')
# rewers: blok "Skad to?" pod znaczeniem
sub('<p class="def" id="definition"></p></div>',
    '<p class="def" id="definition"></p></div>\n     <div class="origin" id="origin" hidden><div class="label">Skąd to?</div>'
    '<p><span class="origin-ref" id="originref"></span> <span class="origin-note" id="originnote"></span></p></div>')
# rewers: hasło nad znaczeniem (do nauki — widać, czego dotyczy znaczenie)
sub('<div><div class="label">Znaczenie frazeologizmu</div>',
    '<div><div class="back-phrase" id="backphrase"></div><div class="label">Znaczenie frazeologizmu</div>')
sub("ui.def.className='def'", "(()=>{document.getElementById('backphrase').textContent=item.karta;const o=document.getElementById('origin'),s=item.skad;o.hidden=!s;if(s){document.getElementById('originref').textContent=s.ref;document.getElementById('originnote').textContent=s.nota?'— '+s.nota:''}})();ui.def.className='def'")
# UX: poziom "Wszystkie" zaznaczony od razu (takze po zmianie talii), zeby mozna bylo losowac bez dodatkowego klikniecia
out = out.replace('</body>', """<script>(()=>{const pick=()=>{if(!document.querySelector('.level-tile[aria-pressed="true"]')){const t=document.querySelector('.level-tile[data-pick-level="all"]');if(t&&!t.disabled)t.click()}};
pick();document.querySelectorAll('.deck-tab').forEach(b=>b.addEventListener('click',()=>setTimeout(pick,0)));})();</script>
</body>""", 1)
cel = 'preview.html' if '--podglad' in sys.argv else 'index.html'
(root/cel).write_text(out, encoding='utf-8')
print('zapisano', cel)
print('index.html:', len(bible), 'biblizmow,', len(myth), 'mitologizmow')

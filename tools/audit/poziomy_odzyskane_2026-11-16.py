"""Decyzja Adama (16.11.2026): poziomy i statusy 9 haseł odzyskanych przy korekcie przesunięcia.
Uruchamiać PO fix_przesuniecie_2026-11-16.py (tamten skrypt odtwarza bazę od zera).
Skrypt jest idempotentny: zmienia data/biblia_baza_kanoniczna.json i dopisuje wpisy do dziennika."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
base_p = ROOT / 'data/biblia_baza_kanoniczna.json'
log_p = ROOT / 'docs/audyt/korekta_2026-11-16.json'
base = json.loads(base_p.read_text(encoding='utf-8'))
log = json.loads(log_p.read_text(encoding='utf-8'))

# hasło -> (poziom, status, karta lub None, powód)
D = {
    'Ziemia obiecana': (2, 'gra', None, 'powszechnie znane, łatwe do pokazania'),
    'Ważyć słowa': (2, 'gra', None, 'częste w użyciu'),
    'Zamknąć się w wieży z kości słoniowej': (3, 'gra', None, 'język literacki'),
    'Zaprzeć się kogoś, czegoś, samego siebie': (3, 'gra', 'Zaprzeć się kogoś', 'znane z historii Piotra; na karcie jedna naturalna postać'),
    'Rozpędzić kogoś na cztery wiatry': (3, 'gra', None, 'poziom jak pozostałe hasła z „wiatrem”'),
    'Bodaj cię święta ziemia nie nosiła!': (5, 'gra', None, 'archaiczne przekleństwo'),
    'Wybiła godzina': (None, 'poza grą', None, 'za bliskie „Wybiła czyjaś ostatnia godzina” — myli się w kalamburach (BIB-005)'),
    'Dobry uczynek': (None, 'poza grą', None, 'zwykłe połączenie wyrazowe, nie obrazowy frazeologizm'),
    'Nie wszyscy mają jednakie talenty': (None, 'poza grą', None, 'archaiczne przysłowie; w talii jest już „talent”'),
}
found = set()
for r in base['records']:
    if r['haslo'] in D:
        poziom, status, karta, why = D[r['haslo']]
        found.add(r['haslo'])
        if (r['poziom'], r['status'], r.get('karta')) == (poziom, status, karta):
            continue
        before = (r['poziom'], r['status'])
        r.update(poziom=poziom, status=status, powod_decyzji=why)
        if karta:
            r['karta'] = karta
        log.append({'id': r['id'], 'akcja': 'decyzja Adama: poziom/status', 'przed': before,
                    'po': (poziom, status, karta or r['haslo']), 'powod': why})
assert found == set(D), set(D) - found
base_p.write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding='utf-8')
log_p.write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding='utf-8')
st = {}
for r in base['records']:
    st[r['status']] = st.get(r['status'], 0) + 1
print(st)

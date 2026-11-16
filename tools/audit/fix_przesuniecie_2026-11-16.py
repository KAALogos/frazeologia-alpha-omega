"""Naprawa przesunięcia hasło/znaczenie w bazie biblizmów (16.11.2026).

Diagnoza: w zakresie numerów uczniowskich 311-377 część rekordów dostała tytuł
(hasło, poziom, status) z poprzedniej pozycji źródłowej, a znaczenie i warianty
z właściwej. Znaczenia i warianty są więc poprawne względem numerów; błędne są
tytuły. Naprawa przenosi tytuły do numerów, pod którymi te hasła naprawdę stoją
w zapisie uczniowskim (zweryfikowane próbnie ze skanem Godynia: ZĄB, ZIARNO,
ZAMEK/ZAMKNĄĆ, WŁOS, WIATR, ZIEMIA).

Pozycje źródłowe, które zostały bez tytułu, dostają nowy rekord ze statusem
"do weryfikacji" i bez poziomu (poziom wymaga decyzji redakcyjnej).

Wejście:  data/archiwum_biblia_baza_ROBOCZA_2026-11-10.json (wersja 2026-11-10)
Wyjście:  data/biblia_baza_kanoniczna.json + docs/audyt/korekta_2026-11-16.json
"""
import json, re, sys, copy, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from load import ROOT, student

S = student()
src = json.loads((ROOT / 'data/archiwum_biblia_baza_ROBOCZA_2026-11-10.json').read_text(encoding='utf-8'))
R = {r['id']: copy.deepcopy(r) for r in src['records']}
old = {r['id']: r for r in src['records']}
log = []

def clean_def(n):
    return re.sub(r'^[‘“’”\']+|[‘“’”\'.]+$', '', S[n][1]).strip()

def defn(n):
    """Znaczenie pozycji n: z rekordu, który miał ją jako jedyny numer, inaczej z zapisu uczniowskiego."""
    for r in old.values():
        if r['numery_uczniowskie'] == [n]:
            return r['znaczenie']
    return clean_def(n)

def set_nums(rid, nums, znaczenie=None, why=''):
    r = R[rid]
    before = (r['haslo'], r['numery_uczniowskie'], r['znaczenie'])
    r['numery_uczniowskie'] = nums
    r['warianty'] = [S[n][2] for n in nums]
    r['liczba_wariantow'] = len(nums)
    if znaczenie is not None:
        r['znaczenie'] = znaczenie
    log.append({'id': rid, 'akcja': 'zmiana', 'przed': before,
                'po': (r['haslo'], r['numery_uczniowskie'], r['znaczenie']), 'powod': why})

def retitle(rid, haslo, poziom, status, why):
    r = R[rid]
    before = (r['haslo'], r['poziom'], r['status'])
    r.update(haslo=haslo, poziom=poziom, status=status)
    log.append({'id': rid, 'akcja': 'nowy tytuł', 'przed': before, 'po': (haslo, poziom, status), 'powod': why})

def move_title(dst, src_id, why):
    s = old[src_id]
    retitle(dst, s['haslo'], s['poziom'], s['status'], why + f' (tytuł z dawnego #{src_id})')

def delete(rid, into, why):
    log.append({'id': rid, 'akcja': 'usunięty', 'przed': (R[rid]['haslo'], R[rid]['numery_uczniowskie'], R[rid]['status']),
                'scalony_do': into, 'powod': why})
    del R[rid]

next_id = max(R) + 1
def new(n, haslo, why):
    global next_id
    rid = next_id; next_id += 1
    R[rid] = {'id': rid, 'numery_uczniowskie': [n], 'haslo': haslo, 'znaczenie': defn(n), 'poziom': None,
              'status': 'do weryfikacji', 'warianty': [S[n][2]], 'liczba_wariantow': 1}
    log.append({'id': rid, 'akcja': 'nowy rekord', 'po': (haslo, [n], R[rid]['znaczenie']), 'powod': why})

SHIFT = 'przesunięcie tytułu o jedną pozycję'
LOST = 'pozycja źródłowa bez własnego rekordu (zgubiona przy przesunięciu)'

# 310/311: "A słowo stało się ciałem" to ten sam frazeologizm co #41; 311 to inne hasło.
set_nums(41, [41, 310], why='311 (ważyć słowa) dołączony błędnie; 310 to wariant tego samego hasła')
delete(309, 41, 'semantyczny duplikat #41 w talii')
new(311, 'Ważyć słowa', LOST)

# 335/336: "Tak, tak — nie, nie" dwa razy w talii; 336 to inne hasło.
set_nums(200, [200, 335], why='336 (talenta) dołączony błędnie; 335 to wariant tego samego hasła')
delete(334, 200, 'semantyczny duplikat #200 w talii')
new(336, 'Nie wszyscy mają jednakie talenty', LOST)

# 345: rekord "Uczony w Piśmie" stoi na pozycji "dobry uczynek".
retitle(344, 'Dobry uczynek', None, 'do weryfikacji', SHIFT + '; duplikat #343 usunięty z talii')

# 351-354: wiara / wiatr.
move_title(350, 351, SHIFT)
move_title(351, 352, SHIFT)
move_title(352, 353, SHIFT)
retitle(353, 'Rozpędzić kogoś na cztery wiatry', None, 'do weryfikacji', SHIFT + '; ' + LOST)

# 356-359: ewangelia / wieża Babel / wieża z kości słoniowej.
set_nums(23, [23, 356], why='357 (istna wieża Babel) dołączony błędnie; 356 to ten sam frazeologizm')
delete(355, 23, SHIFT + '; tytuł był duplikatem #354, pozycja 356 = #23')
set_nums(18, [18, 357, 358], why='357 i 358 to warianty tego samego hasła (BIB-006)')
delete(357, 18, 'duplikat #18 w talii; 359 (wieża z kości słoniowej) był dołączony błędnie')
new(359, 'Zamknąć się w wieży z kości słoniowej', LOST)

# 361-364: włosy / godzina.
move_title(360, 361, SHIFT)
move_title(361, 362, SHIFT)
move_title(362, 363, SHIFT)
retitle(363, 'Wybiła godzina', None, 'do weryfikacji', SHIFT + '; ' + LOST)

# 368-370: zamki / siedem spustów / zaprzeć się.
set_nums(366, [367, 368], why='368 (zamki na lodzie/piasku) to wariant tego samego hasła')
delete(367, 366, 'duplikat #366 w talii')
set_nums(369, [369], znaczenie=defn(369), why=SHIFT)
new(370, 'Zaprzeć się kogoś, czegoś, samego siebie', LOST)

# 372-375: zęby / ziarno / ziemia.
set_nums(24, [24], why='372 (zgrzytać zębami) dołączony błędnie')
set_nums(372, [372], znaczenie=defn(372), why=SHIFT)
set_nums(373, [373], znaczenie=defn(373), why=SHIFT)
set_nums(374, [374], znaczenie=defn(374), why=SHIFT)
new(375, 'Bodaj cię święta ziemia nie nosiła!', LOST)

# 377: "Niech mnie ziemia pochłonie!" drugi raz, na pozycji "ziemia obiecana".
retitle(376, 'Ziemia obiecana', None, 'do weryfikacji', SHIFT + '; duplikat #375 usunięty z talii')

# --- kontrole ---
recs = sorted(R.values(), key=lambda r: min(r['numery_uczniowskie']))
cover = {}
for r in recs:
    for n in r['numery_uczniowskie']:
        cover.setdefault(n, []).append(r['id'])
assert sorted(cover) == list(range(1, 383)), 'brakujące numery'
assert all(len(v) == 1 for v in cover.values()), {n: v for n, v in cover.items() if len(v) > 1}
game = [r for r in recs if r['status'] == 'gra']
names = [r['haslo'].lower() for r in game]
import collections; dd=[(r['id'],r['haslo'],r['numery_uczniowskie']) for r in game if names.count(r['haslo'].lower())>1]
assert not dd, dd
assert all(r['poziom'] in (1, 2, 3, 4, 5) for r in game)

out = {'version': '2026-11-16', 'source': src['source'],
       'poprzednia_wersja': src['version'],
       'korekta': 'docs/audyt/korekta_2026-11-16.json', 'records': recs}
(ROOT / 'data/biblia_baza_kanoniczna.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
(ROOT / 'docs/audyt').mkdir(parents=True, exist_ok=True)
(ROOT / 'docs/audyt/korekta_2026-11-16.json').write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding='utf-8')
st = {}
for r in recs:
    st[r['status']] = st.get(r['status'], 0) + 1
print('rekordy', len(recs), st, 'zmian w logu', len(log))

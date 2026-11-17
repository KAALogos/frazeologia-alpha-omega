"""Dodaje kandydatow z przegladu slownika frazeologicznego (LingLogos, 17.11.2026).

Decyzja Adama (17.11.2026): wprowadzic nowe biblizmy i mitologizmy z przegladu.
Wszystkie karty dostaja status "do weryfikacji" i poziom null, wiec NIE trafiaja
do talii, dopoki Adam nie nada poziomu i statusu "gra".

Znaczenia sa sformulowane samodzielnie (nie sa cytatem ze slownika).
Skrypt jest idempotentny: drugi przebieg nic nie zmienia.

Uruchom:  python -I tools/audit/dodaj_kandydatow_linglogos_2026-11-17.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIB = ROOT / "data" / "biblia_baza_kanoniczna.json"
MIT = ROOT / "data" / "mitologia_kandydaci.json"
ZRODLO = "przeglad LingLogos 2026-11-17 (slownik frazeologiczny); znaczenie opracowane samodzielnie"

BIBLIA = [
    ("W stroju Ewy", "żart. ‘nago’ (o kobiecie)", "Rdz 2, 25; para do karty „W stroju Adama”"),
    ("Niewola egipska", "‘ciężkie zniewolenie, uciążliwa i długotrwała zależność od kogoś’", "Wj 1–14"),
    ("Po nas choćby potop", "‘nie obchodzi nas, co będzie potem; liczy się tylko dziś’",
     "nawiązanie do potopu (Rdz 6–8); samo powiedzenie przypisywane dworowi Ludwika XV — do decyzji, czy to biblizm"),
    ("Judaszowe srebrniki", "‘zapłata za zdradę; pieniądze zdobyte nieuczciwie, kosztem kogoś’",
     "Mt 26, 15; 27, 3–5; bliskie karcie #320, ale inne wyrażenie"),
    ("Tron Piotrowy", "książk. ‘urząd papieża, papiestwo’", "Mt 16, 18–19"),
]
MITOLOGIA = [
    ("miecz Damoklesa / Damoklesowy", "miecz Damoklesa",
     "stale wiszące nad kimś zagrożenie, które może spaść w każdej chwili",
     "anegdota antyczna (Cyceron, Rozmowy tuskulańskie V), nie mit — do decyzji"),
    ("pyrrusowe zwycięstwo", "pyrrusowe zwycięstwo",
     "zwycięstwo okupione tak wielkimi stratami, że niewiele różni się od klęski",
     "historia (Pyrrus, król Epiru; Plutarch), nie mit — do decyzji"),
    ("węzeł gordyjski || przeciąć / rozciąć węzeł gordyjski", "węzeł gordyjski",
     "bardzo zawiła sprawa; przeciąć go — rozwiązać ją jednym zdecydowanym ruchem",
     "legenda o Aleksandrze Wielkim, nie mit — do decyzji"),
]


def main():
    base = json.loads(BIB.read_text(encoding="utf-8"))
    rec = base["records"]
    istniejace = {r["haslo"].lower() for r in rec}
    nid = max(r["id"] for r in rec) + 1
    dodane_b = 0
    for haslo, znacz, powod in BIBLIA:
        if haslo.lower() in istniejace:
            continue
        rec.append({
            "id": nid, "numery_uczniowskie": [], "haslo": haslo, "znaczenie": znacz,
            "poziom": None, "status": "do weryfikacji", "warianty": [f"{haslo} — {znacz}"],
            "liczba_wariantow": 1, "zrodlo": ZRODLO, "powod_decyzji": powod,
        })
        nid += 1
        dodane_b += 1
    if dodane_b:
        BIB.write_text(json.dumps(base, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    mit = json.loads(MIT.read_text(encoding="utf-8")) if MIT.exists() else {
        "opis": "Kandydaci do talii mitologicznej spoza listy Pudy-Blokesz. Build ich NIE czyta; "
                "przeniesienie do apps/kalambury_mitologia_v3.html dopiero po decyzji Adama.",
        "records": []}
    juz = {r["haslo"].lower() for r in mit["records"]}
    dodane_m = 0
    for haslo, karta, znacz, powod in MITOLOGIA:
        if haslo.lower() in juz:
            continue
        mit["records"].append({
            "id": f"K{len(mit['records']) + 1}", "haslo": haslo, "karta": karta, "znaczenie": znacz,
            "poziom": None, "status": "do weryfikacji", "zrodlo": ZRODLO, "powod_decyzji": powod,
        })
        dodane_m += 1
    if dodane_m:
        MIT.write_text(json.dumps(mit, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"dodano: {dodane_b} biblizmow, {dodane_m} mitologizmow (status: do weryfikacji)")


if __name__ == "__main__":
    main()

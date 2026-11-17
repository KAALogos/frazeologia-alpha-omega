"""Test kandydatow z przegladu LingLogos (17.11.2026).

Sprawdza: talia w grze bez zmian, kandydaci poza gra, brak tekstu definicji PWN w repo.
Uruchom:  python -I tools/audit/test_kandydaci_linglogos.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
# Lokalny (niepubliczny) plik z jednostkami PWN; jesli go brak, test licencyjny jest pomijany.
PWN = pathlib.Path("C:/codeLogos-bootstrap/linglogos-rebuild/PRACE/frazeologia_aw/wyniki/kandydaci_fraz_pwn_2006.jsonl")
bledy = []


def ok(cond, msg):
    if not cond:
        bledy.append(msg)


base = json.loads((ROOT / "data/biblia_baza_kanoniczna.json").read_text(encoding="utf-8"))["records"]
mit = json.loads((ROOT / "data/mitologia_kandydaci.json").read_text(encoding="utf-8"))["records"]
kand_b = [r for r in base if "LingLogos" in r.get("zrodlo", "")]

ok(sum(r["status"] == "gra" for r in base) == 233, "talia biblijna w grze != 233")
ok(len({r["id"] for r in base}) == len(base), "zdublowane id w bazie biblijnej")
ok(len(kand_b) == 5 and len(mit) == 3, f"oczekiwano 5+3 kandydatow, jest {len(kand_b)}+{len(mit)}")
for r in kand_b + mit:
    ok(r["status"] == "do weryfikacji" and r["poziom"] is None, f"kandydat w grze lub z poziomem: {r['haslo']}")
    ok(r["znaczenie"].strip() != "", f"puste znaczenie: {r['haslo']}")

idx = (ROOT / "index.html").read_text(encoding="utf-8")
ds = json.loads(re.search(r"const DATASETS = (\{.*?\});\n", idx).group(1))
ok(len(ds["bible"]) == 233, "index.html: talia biblijna != 233")
ok(not any(c["haslo"] in {r["haslo"] for r in kand_b} for c in ds["bible"]), "kandydat trafil do index.html")

if PWN.exists():
    pwn = [json.loads(l)["znaczenie_pwn"] for l in PWN.open(encoding="utf-8")]
    pwn = [z for z in pwn if len(z) >= 30]
    # Twardo: nasi kandydaci nie moga zawierac tekstu PWN.
    kand_txt = json.dumps(kand_b + mit, ensure_ascii=False)
    for z in pwn:
        ok(z not in kand_txt, f"tekst definicji PWN u kandydata: {z[:40]}")
    # Informacyjnie: zbieznosci w kartach sprzed 17.11 (dane Godynia / transkrypcji uczniowskiej).
    stare = [r for r in base if r not in kand_b and any(z in r["znaczenie"] or any(z in w for w in r["warianty"]) for z in pwn)]
    if stare:
        print(f"INFO: {len(stare)} starszych kart ma znaczenie identyczne z PWN (do audytu): "
              + ", ".join(f"#{r['id']}" for r in stare))
else:
    print("UWAGA: brak lokalnego pliku PWN - test licencyjny pominiety")

print("TESTY:", "PASS" if not bledy else "FAIL")
for b in bledy:
    print(" -", b)
sys.exit(1 if bledy else 0)

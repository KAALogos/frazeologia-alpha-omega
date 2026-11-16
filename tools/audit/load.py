import json,re,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
def student():
    """orig nr (1..382) -> (fraza, definicja, linia). Plik ma 381 akapitow: 306 = orig 306/307."""
    out={}
    for line in (ROOT/'data/biblia_zapis_po_pierwszych_korektach.txt').read_text(encoding='utf-8-sig').splitlines():
        m=re.match(r'^(\d+)\.\s*(.*)$',line.strip())
        if not m: continue
        n=int(m.group(1)); t=m.group(2)
        nums=[n] if n<306 else ([306,307] if n==306 else [n+1])
        parts=re.split(r'\s*[-–—]\s+|\s+[-–—]\s*|(?<=\))\s*(?=[‘“])|\s(?=‘)',t,1)
        for o in nums: out[o]=(parts[0].strip(), parts[1].strip() if len(parts)>1 else '', t)
    return out
def html_cards():
    s=(ROOT/'apps/kalambury_biblia_v5.html').read_text(encoding='utf-8')
    m=re.search(r'const DATASETS = (\{.*?\});\n',s); return json.loads(m.group(1))['bible']
def canon():
    return json.loads((ROOT/'data/archiwum_biblia_baza_ROBOCZA_2026-11-10.json').read_text(encoding='utf-8'))
STOP={'się','kto','jak','nie','ani','czy','ten','tak','kogo','coś','czegoś','kogoś','komuś','kimś','czymś','czym','być','swój','swoje','jest'}
def toks(s):
    s=re.sub(r'\(.*?\)','',s.lower())
    return {w[:4] for w in re.findall(r'[a-ząćęłńóśźż]+',s) if len(w)>2 and w not in STOP}

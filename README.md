# Kalambury αω: frazeologia biblijna i mitologiczna

Multizestaw do kalamburów na lekcji i do samodzielnej nauki frazeologizmów. Jedna aplikacja HTML działa offline na telefonie i komputerze, ma dwie talie (Biblizmy i Mitologizmy), a każda talia ma osobną historię i postęp.

> **Stan: prototyp roboczy.** 16.11.2026 naprawiono przesunięcie haseł i znaczeń w talii biblijnej oraz usunięto duplikaty (patrz `docs/RAPORT_SCALENIA_2026-11-16.md`). Poziomy i selekcja kart są nadal robocze; pełnej kolacji ze słownikiem nie wykonano.

## Uruchomienie
Otwórz `index.html` w przeglądarce. Nie trzeba niczego instalować. Postęp zapisuje się w `localStorage` danej przeglądarki.

## Struktura
| Ścieżka | Zawartość |
|---|---|
| `index.html` | scalona aplikacja (generowana, nie edytować ręcznie) |
| `apps/kalambury_biblia_v5.html` | źródło interfejsu (jego osadzone dane biblijne są nieaktualne i ignorowane) |
| `apps/kalambury_mitologia_v3.html` | źródło: talia mitologiczna (202 karty), działa też samodzielnie |
| `tools/build_multizestaw.py` | buduje `index.html` z dwóch plików w `apps/` |
| `data/biblia_baza_kanoniczna.json` | **jedyne źródło danych biblijnych**: 347 rekordów, status `gra` = karta w talii |
| `data/` (pozostałe) | transkrypcje uczniowskie, archiwum bazy z 10.11.2026 |
| `tools/audit/` | skrypty audytu i korekty bazy; dziennik zmian w `docs/audyt/` |
| `docs/handoff/` | paczka przekazania z 16.11.2026 (polecenie, stan, manifest) |
| `docs/qa/` | raport QA z paczki, lista błędów krytycznych, zrzuty |
| `archive/apps/` | wcześniejsze wersje mitologii; nie używać jako bazy |

## Przebudowa po zmianie danych
```
python tools/build_multizestaw.py
```

## Źródła
- Jan Godyń, *Od Adama i Ewy zaczynać. Mały słownik biblizmów języka polskiego*.
- Magdalena Puda-Blokesz, *Po nitce do kłębka. Mały słownik mitologizmów frazeologicznych języka polskiego*.

Skany słowników **nie są** częścią repozytorium (materiał wyłącznie do wewnętrznej weryfikacji).

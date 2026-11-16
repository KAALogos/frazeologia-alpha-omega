# Kalambury αω: frazeologia biblijna i mitologiczna

Multizestaw do kalamburów na lekcji i do samodzielnej nauki frazeologizmów. Jedna aplikacja HTML działa offline na telefonie i komputerze, ma dwie talie (Biblizmy i Mitologizmy), a każda talia ma osobną historię i postęp.

> **Stan: prototyp roboczy, NIE zatwierdzony dydaktycznie.** Talia biblijna zawiera karty z cudzą definicją (patrz `docs/RAPORT_SCALENIA_2026-11-16.md`). Nie używać z uczniami, dopóki nie zostanie wykonany Etap A z `docs/handoff/POLECENIE_DLA_CLAUDE.md`.

## Uruchomienie
Otwórz `index.html` w przeglądarce. Nie trzeba niczego instalować. Postęp zapisuje się w `localStorage` danej przeglądarki.

## Struktura
| Ścieżka | Zawartość |
|---|---|
| `index.html` | scalona aplikacja (generowana, nie edytować ręcznie) |
| `apps/kalambury_biblia_v5.html` | źródło: aplikacja i talia biblijna (235 kart) |
| `apps/kalambury_mitologia_v3.html` | źródło: talia mitologiczna (202 karty), działa też samodzielnie |
| `tools/build_multizestaw.py` | buduje `index.html` z dwóch plików w `apps/` |
| `data/` | robocza baza biblizmów (JSON, 347 rekordów) i transkrypcje uczniowskie |
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

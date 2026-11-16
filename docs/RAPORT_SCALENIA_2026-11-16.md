# Raport scalenia i przeglądu (16.11.2026)

## Co scalono
- Paczka `PACZKA_CLAUDE_FRAZEOLOGIA_ALPHA_OMEGA_2026-11-16.zip`: 28 plików z manifestu, wszystkie sumy SHA-256 zgodne.
- `Kalambury_mitologiczne_losowanie_202_v2.html` z Pobranych jest bajt w bajt identyczny z `archive/apps/mitologia_v2.html` (ta sama suma SHA-256). Nie wnosi nic nowego; nie dodano go drugi raz.
- `index.html` = aplikacja Biblia v5 (miała już przełącznik talii, ale pustą talię `myth`) + 202 karty z Mitologii v3, bez zmian w danych. Dodano przycisk talii „Mitologizmy”. Zmieniono tytuł strony.
- Poprawka: logo pokazywało „AΩ” (CSS `text-transform:uppercase`), więc α wyglądała jak łacińskie A. Teraz widać α ω.
- Do repozytorium nie trafiły: skany PDF słowników (`03_ZRODLA`), eksport DOCX z Google Docs i jego TXT (`04_DOKUMENT_GOOGLE`), niezatwierdzone karty i scenariusze (`06_ARCHIWUM_NIEZATWIERDZONE`). Zostają w ZIP-ie w Pobranych.

## Testy (wykonane, localhost:8771, wbudowana przeglądarka)
| Test | Wynik |
|---|---|
| Pełne losowanie Mitologizmów: 202/202, 0 powtórek | PASS |
| Pełne losowanie Biblizmów: 235/235, 0 powtórek | PASS |
| Filtr poziomu (V SP ×5 w mitologii, PRO ×3 w Biblii) | PASS |
| Rewers pokazuje znaczenie | PASS |
| Przeładowanie strony: obie talie zachowują postęp, poziom i aktywną talię | PASS |
| Reset jednej talii nie rusza drugiej | PASS |
| Telefon 375 px: brak przewijania w poziomie, kafelki nad kartą | PASS |
| Błędy JS w konsoli | brak |

Nie testowano: Safari/iOS, prawdziwego telefonu, przeniesienia postępu ze starej mitologii v3 (kod migracji istnieje, nie sprawdzony).

## Co NIE działa: dane
Interfejs działa, ale **talia biblijna uczy błędnych znaczeń**.

1. **Przesunięcie hasło/znaczenie jest większe niż w `KRYTYCZNE_BLEDY.json`.** Raport z paczki podaje 5 kart (BIB-001 do 005). W rzeczywistości w zakresie mniej więcej #343 do #376 hasło pochodzi z jednej pozycji uczniowskiej, a znaczenie z następnej. Przykłady widoczne w grze:
   - #344 „Uczony w Piśmie” → „czyn zgodny z zasadami moralnymi…” (to „dobry uczynek”)
   - #351 „Wiara góry przenosi” → przysłowie o konsekwencjach złych działań (to „kto sieje wiatr…”)
   - #352 „Kto sieje wiatr, zbiera burzę” → „mówić, obiecywać nieodpowiedzialnie” (to „rzucać słowa na wiatr”)
   - #353 „Rzucać słowa na wiatr” → „rozpędzić, wypędzić…”
   - #355 „Wiedzieć, skąd wieje wiatr” → „wierzyć w coś bardzo”
   - #360 „Rwać włosy z głowy” → „nie grozi żadne niebezpieczeństwo”
   - #361 „Włos z głowy nie spadnie” → „ogarnia strach”
   - #362 „Włosy stają dęba” → „nadeszła chwila śmierci”
   - #363 „Wybiła czyjaś ostatnia godzina” → „nadszedł czas”
   - #369, #372, #373, #374 (jak w BIB-001 do 004)
   - #376 „Niech mnie ziemia pochłonie!” → „miejsce najbardziej pożądane, raj”
2. **Błąd jest już w `data/biblia_baza_kanoniczna_ROBOCZA.json`**, a nie tylko w HTML. Pole `warianty` w JSON-ie zawiera prawdziwy wpis źródłowy, który zgadza się ze znaczeniem, ale nie z hasłem. Dlatego JSON nie może być „kanonicznym źródłem” bez naprawy.
3. **Błędne scalenia rekordów:** #23 „Wierzyć jak w Ewangelię” ma w wariantach „wieżę Babel”; #24 „Błędna owca” ma „zgrzytać zębami”; #200 „Tak, tak, nie, nie” ma „nie wszyscy mają jednakie talenta”.
4. **Duplikaty w talii** (BIB-006 potwierdzone): wieża Babel, uczony w Piśmie, rwać włosy z głowy, budować zamki na piasku.
5. **Mitologia:** 202 karty, brak duplikatów haseł, jedna karta bez znaczenia (#196, aplikacja pokazuje wtedy komunikat „wymaga weryfikacji”). Kolacji ze skanem Pudy-Blokesz nie robiono.
6. Biblia: 75 kart ma `numery_zrodlowe` różne od `id`. Nie zawsze jest to błąd (numeracja uczniowska jest przesunięta od #309), ale bez kolacji ze skanem Godynia nie da się tego rozstrzygnąć automatycznie.

## Następny krok
Etap A z polecenia: rekolacja zakresu biblijnego #300 do #382 ze skanem Godynia i oryginałem uczniowskim, naprawa JSON-u, przebudowa talii, usunięcie duplikatów.

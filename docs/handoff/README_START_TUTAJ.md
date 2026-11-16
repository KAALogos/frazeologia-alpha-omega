# αω — PACZKA DLA CLAUDE | START TUTAJ

**Zlecenie:** rozwój multizestawu do nauki frazeologii: najpierw biblizmy, następnie mitologizmy według tej samej metodologii, na końcu połączenie serwisów i rozbudowa do pełnej aplikacji frazeologicznej.

**Stan na 16.11.2026:** dwa oddzielne działające prototypy HTML (mitologia v3 / Biblia v5), dwa słowniki źródłowe (skany PDF), dokument Google z dwoma kartami, oraz robocza baza biblizmów. **Nie jest to zatwierdzona wersja dydaktyczna:** lista błędów wysokiej wagi jest w `05_QA/KRYTYCZNE_BLEDY.json`.

## Co otworzyć w pierwszej kolejności
1. `00_CLAUDE/POLECENIE_DLA_CLAUDE.md` — kompletna dyspozycja dalszej pracy, granice zakresu.
2. `05_QA/KRYTYCZNE_BLEDY.json` — błędy, które mogą nauczyć uczniów nieprawdy.
3. `04_DOKUMENT_GOOGLE/Wersja_czysta_snapshot_z_Docs.txt` oraz `02_DANE/biblia_baza_kanoniczna_ROBOCZA.json` — **dwa nierównoznaczne stany**, bez automatycznego nadpisywania jednego drugim.
4. `01_APLIKACJE/AKTUALNE/kalambury_biblia_v5.html` i `.../kalambury_mitologia_v3.html` — aktualne osobne aplikacje.
5. `03_ZRODLA/` — pełne oryginalne skany słowników (materiał źródłowy, nie publikować).

## Drzewo katalogów
- `00_CLAUDE/`: zadanie, decyzje i ograniczenia.
- `01_APLIKACJE/AKTUALNE/`: samodzielne działające HTML do przeglądarki (offline).
- `01_APLIKACJE/ARCHIWUM/`: wcześniejsze iteracje; **nie wybierać jako bazowych**.
- `02_DANE/`: eksport bazy i różne lokalne wersje danych.
- `03_ZRODLA/`: dwa skany słowników.
- `04_DOKUMENT_GOOGLE/`: DOCX z dwiema kartami + ekstrakty TXT.
- `05_QA/`: test UI, raporty różnic, błędy krytyczne.
- `06_ARCHIWUM_NIEZATWIERDZONE/`: stare materiały do druku i scenariusze; **nie są zaakceptowanym formatem gry**.
- `META_STAN.json`: stan, źródła, liczby, ograniczenia.
- `MANIFEST_SHA256.json`: integralność plików w archiwum.

## Uruchomienie
Wystarczy dwukrotnie kliknąć odpowiedni plik HTML z folderu `01_APLIKACJE/AKTUALNE/`. Nie ma kroku instalacji ani serwera. Gry zapisują postęp w localStorage (nie jest on współdzielony między plikami i przeglądarkami).

## Co zostało zrobione teraz
Zebrałem i sprawdziłem pliki z dostępnego środowiska, odczytałem dwie karty Google Docs przez eksport, przeliczyłem bazę i wykonałem testy interfejsu na dwóch szerokościach ekranu. Nie publikowałem i nie modyfikowałem Google Docs ani aplikacji.

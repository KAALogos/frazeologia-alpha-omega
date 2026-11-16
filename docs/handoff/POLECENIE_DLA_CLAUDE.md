# POLECENIE DLA CLAUDE — FRAZEOLOGIA αω

Jesteś agentem przejmującym istniejący projekt edukacyjny. **Najpierw wykonaj audyt i naprawę niespójności, dopiero potem rozwój.** Nie zaczynaj od pisania nowej gry ani od przebudowy UI, jeśli nie jest to potrzebne. Pracuj na dołączonych plikach i rzeczywiście czytaj zawartość, nie wnioskuj z nazw.

## Produkt końcowy
Multizestaw edukacyjny do nauki i gry obejmujący rozdzielne zasoby frazeologizmów biblijnych i mitologicznych, docelowo wspólny serwis z możliwością dalszego rozszerzania o inne zasoby. Na lekcjach **wyłącznie kalambury**; materiał do samodzielnej nauki w domu. Projekt ma działać bezpośrednio na telefonach i komputerach.

## ZAMROŻONE DECYZJE — nie zmieniaj ich samowolnie
- Gra: **awers = wyrażenie, typ prezentacji (rysowany/pokazywany) i poziom**; rewers = znaczenie (oraz ewentualna osobna sekcja kontekstowa na przyszłość).
- Wybór poziomu **jednym kliknięciem kafelka obok karty (mobile: nad kartą)**; poziomy: **V SP, E8, LO P, LO R, PRO** + Wszystkie.
- Losowanie **bez powtórek**, bez utraty historii; można podejrzeć poprzednio wylosowane karty. Zachować zachowanie pamięci postępu.
- Do odgadnięcia jedna jednoznaczna, naturalna postać hasła; alternatywy tylko tam, gdzie są rzeczywiście uprawnionymi wariantami.
- Logo wykorzystuje prawdziwe greckie znaki **α i ω**, nie łacińskie literki zastępcze.
- Oryginał transkrypcji uczniów ma pozostać nienaruszony; pracujemy na osobnej **„Wersji czystej”** dokumentu Google.
- Źródła muszą być cytowane i możliwe do zweryfikowania, nie zastępować prawdziwych cytatów zdaniami autorskimi.
- Nie robić drukowanych kart, PDF-ów z ćwiczeniami, scenariuszy, komunikacji mailowej, ani publikacji bez zlecenia.
- Po korekcie zmieniaj tylko wskazaną część, nie przepisuj innych zaakceptowanych elementów.

## ZADANIA — wykonuj po kolei

### ETAP A — bezpieczeństwo danych i spójność (najpierw)
1. Zobacz `05_QA/KRYTYCZNE_BLEDY.json`. W obecnej grze biblijnej są **przesunięte hasła i znaczenia**. Nie wolno jej kwalifikować jako bezbłędnej.
2. Przyjmij skan Godynia za główne źródło leksykograficzne, a źródłową numerację uczniowską za klucz referencyjny.
3. Porównaj `04_DOKUMENT_GOOGLE/Wersja_czysta_snapshot_z_Docs.txt` z `02_DANE/biblia_baza_kanoniczna_ROBOCZA.json` i z danymi osadzonymi w HTML v5. Nie ma gwarancji, że są identyczne.
4. Wyjaśnij każdą kolizję: źródło (numery), poprawna forma, poprawne znaczenie, status wariantu/duplikatu/oddzielnego znaczenia. Zapisuj nierozstrzygnięte przypadki, nie zgaduj.
5. Ustal **jedno kanoniczne źródło danych**, na którym będą budowane Google Docs, HTML i przyszłe moduły. Zachowaj pełny audit trail numerów źródłowych. Zastąp błędne rozbieżności tylko po sprawdzeniu.

### ETAP B — biblizmy: redakcja i selekcja
1. Wszystkie 381 uczniowskich akapitów (pierwotnie zakres 1–382 z połączonym 306/307) zachowaj w „Oryginale”.
2. Obecne 347 rekordów kanonicznych i podział `235 gra / 83 poza grą / 29 do weryfikacji` to **stan roboczy**, nie zatwierdzony. Rewiduj scalania; różnica postaci nie zawsze oznacza duplikat, a różnica sensu może wymagać rozdzielenia.
3. Oddziel `hasło kanoniczne`, `dopuszczalne warianty`, `jednoznaczną definicję`, `pochodzenie`, `numer/y źródłowe`, `poziom trudności`, `status gry`, `powód decyzji`.
4. Oznacz przysłowia, biblizmy leksykalne, związki wyrazowe, odsyłacze i przypadki niepewnej genezy (nie wszystko jest frazeologizmem wielowyrazowym).
5. Dopiero po weryfikacji wygeneruj ponownie talię kalamburów oraz zsynchronizuj kartę „Wersja czysta”.

### ETAP C — mitologizmy
1. Zachowaj źródłowe 202 pozycje, porównaj ze skanem Pudy-Blokesz.
2. Zastosuj identyczny model danych i metodę rozpoznawania wariantów, duplikatów, definicji i poziomów.
3. Nie ruszaj UI w działającej wersji mitologicznej v3 poza zmianami koniecznymi dla wspólnej bazy i dopiero gdy etap B zostanie ustabilizowany.

### ETAP D — multizestaw + konteksty użycia
1. Po pozytywnej weryfikacji obu talii zbuduj wspólny interfejs z wyborem Biblia / Mitologia, osobnymi historiami i poziomami oraz możliwością rozszerzania o inne zbiory.
2. Dodaj **prawdziwe, weryfikowalne przykłady użycia w literaturze, publicystyce, kulturze**. Każda referencja: frazeologizm, krótki cytat w dozwolonym zakresie, autor, utwór/tytuł, wydanie/rok, strona lub URL, status weryfikacji i komentarz znaczeniowy.
3. Oddziel cytat dosłowny od parafrazy; w ogóle nie wstawiaj nieweryfikowanych cytatów.
4. Stosuj krótkie fragmenty i linki do źródeł; nie wklejaj długich chronionych fragmentów.

## WARUNKI ODBIORU
- Wszystkie źródłowe pozycje zachowane w warstwie oryginalnej, bez znikających numerów.
- Każdy kanoniczny rekord ma poprawne odesłanie do uczniowskiego numeru i definicję zgodną z oryginalnym słownikiem albo uczciwą flagę `NIEPOTWIERDZONE`.
- W grze nie ma kart z cudzą definicją; brak powtórek semantycznych.
- Testy: desktop+mobile, front/back, tryb kalamburu na awersie, poziomy, historia, restart, brak powtórek, trwałość stanu po przeładowaniu na prawdziwym origin.
- Raport zmian z rzeczywistymi testami, ścieżkami i listą ryzyk. Nie deklaruj QA, którego nie wykonałeś.
- Nie dokonuj publikacji lub zewnętrznych modyfikacji bez jednoznacznego zlecenia; najpierw wersje lokalne do zatwierdzenia.

## UŻYTECZNE PLIKI
- `README_START_TUTAJ.md`
- `META_STAN.json`
- `05_QA/KRYTYCZNE_BLEDY.json`
- `05_QA/ROZNICE_GOOGLE_DOCS_VS_JSON_AUDYT.json`
- `01_APLIKACJE/AKTUALNE/`
- `02_DANE/`, `03_ZRODLA/`, `04_DOKUMENT_GOOGLE/`

## UWAGA
Archiwum zawiera także starsze prototypy i materiały wcześniej niezaakceptowane. Nie przywracaj ich funkcjonalności ani formatu „bo są w paczce”.

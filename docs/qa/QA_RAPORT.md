# KONTROLA PACZKI (2026-11-16)

1. Zweryfikowano istnienie wszystkich plików przekazanych do paczki, przepisano je bez edycji.
2. `Frazeologizmy biblijne.docx` wyeksportowano z istniejącego dokumentu Google zawierającego dwie karty. Odczyt z DOCX wykazał 381 akapitów numerowanych uczniowskiej transkrypcji i 347 numerowanych rekordów „Wersji czystej”. Oba teksty zostały także wyeksportowane do plików TXT.
3. JSON: 347 rekordów, 235 `gra`, 83 `poza grą`, 29 `do weryfikacji`. HTML Biblia: 235 kart, pięć poziomów (V SP 35, E8 61, LO P 67, LO R 52, PRO 20). HTML Biblia **nie zawiera kart mitologicznych** (`myth=[]`).
4. Chrome/Playwright (systemowy `/usr/bin/chromium`): otwarto obie gry na viewportach 1280×800 i 390×844 z treści HTML (`page.set_content`), kliknięto poziom V SP, losowanie, rewers, historię. **4/4 przypadki PASS**, bez JS pageerrors i bez poziomego overflow; szczegóły `testy_interfejsu_2026-11-16.json`.
5. Nie sprawdzono w tej sesji pełnego losowania 202/235, działania zapisu localStorage po realnym odświeżeniu strony ani synchronizacji oryginału z Google Docs po stworzeniu archiwum. Weryfikacje leksykograficzne tylko punktowe; patrz `KRYTYCZNE_BLEDY.json`.
6. Stwierdzono co najmniej 4 duplikaty nazw kart w talii Biblia, ignorując wielkość liter. To nie jest dopuszczalny stan finalny.
7. Wszystkie pliki w ZIP otrzymują SHA-256 w `MANIFEST_SHA256.json`.

**Zastrzeżenie:** test funkcjonalności interfejsu nie jest testem poprawności danych. Gra może działać perfekcyjnie i równocześnie pokazywać uczniowi błędną definicję — obecna wersja ma właśnie taki problem.

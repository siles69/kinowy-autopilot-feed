# Założenia przyjęte przy tworzeniu materiałów

Polecenie brzmiało: nie zadawać pytań, przyjąć rozsądne założenia i je spisać. Oto one.

## Ogólne
1. **Miasto = Katowice.** Wszędzie, gdzie w zadaniu było `[MIASTO]`, wpisałem Katowice; w ogłoszeniach dopisałem „i okolice / Śląsk”, bo zdalna obsługa nie ma granic.
2. **Termin „48 h”** na pierwszy film — przyjęty jako obietnica sprzedażowa (produkcja AI jest szybka). Jeśli to za ostro, zmień w `index.html`, `cennik.html`, `wiadomosci.md`, `ogloszenia.md` (wyszukaj „48”).
3. **Jedna runda poprawek w cenie** (także w darmowym filmie) — przyjęte, żeby ograniczyć niekończące się poprawki; nie było tego w briefie.
4. **Płatność:** przelew, pakiet płatny z góry, rozliczenie miesięczne, bez okresu wypowiedzenia. Darmowy film — bez żadnej płatności.
5. **Publikacja w pakiecie Pro** odbywa się bez przekazywania haseł — przez dostęp współpracownika w Meta Business lub akceptację filmów przez klienta. To zapis w FAQ; jeśli wolisz inaczej, zmień.
6. **Lektor „AI”** nazywam wprost na stronie i w ogłoszeniach (uczciwość wobec klienta), ale zaznaczam, że scenariusz piszesz sam, a materiał wideo jest prawdziwy.
7. Nazwy firm z demo oznaczone na stronie jako „przykładowa firma”; brak opinii i referencji — zgodnie z zasadami.
8. **Folder `demo/`** utworzony z pustym `.gitkeep`, żeby ścieżki `../demo/*.mp4` były gotowe. Strona pokazuje komunikat o brakującym pliku zamiast czarnego pola do czasu uploadu.

## Strona i PDF
9. Brak zewnętrznych bibliotek poza Google Fonts (Inter). Ikony w przyciskach kontaktu to inline SVG.
10. Linki portfolio wskazują na `https://siles69.github.io/kinowy-autopilot-feed/oferta/` — zakładam, że GitHub Pages serwuje z gałęzi `main`, więc pliki muszą trafić na `main`, żeby adres działał.
11. PDF wygenerowano headless Chromium z `cennik.html`; A4, ciemne tło. Zawiera placeholdery `TODO_*` — po ich uzupełnieniu wygeneruj ponownie (instrukcja w `README.md`).

## Leady (`leady.csv`)
12. Dane pochodzą wyłącznie z publicznych źródeł (katalogi: ZnanyLekarz, kliniki.pl, Booksy, Otodom, sonarhome, crossfit.com, In Your Pocket, intravel, rankingpro) znalezionych przez wyszukiwarkę. **Nie miałem możliwości przeglądania Instagrama/Facebooka ani Google Maps na żywo**, więc:
    - kolumny *profil Instagram*, *profil Facebook*, *strona www* (tam gdzie nie znalazłem) mają wartość `do sprawdzenia` — nie zgadywałem adresów, żeby nie wpisać cudzego profilu;
    - *liczba obserwujących IG* i *ostatni post* mają `nie sprawdzono`;
    - *ocena Google* wpisana tylko tam, gdzie źródło ją podawało (z nazwą źródła); inaczej `brak danych`;
    - *telefon publiczny* tylko dla Basiliany (jedyny znaleziony w wynikach) — reszta `brak danych`.
    Uzupełnienie tych kolumn to ok. 2–3 minuty na firmę w Google Maps + Instagram — wpisane w punkt 1 dziennego rytuału.
13. Kolumna *co kuleje* to hipoteza na podstawie tego, co widać w katalogach (obecność tylko przez Booksy/ZnanyLekarz, brak wzmianek o wideo). Przed wysłaniem wiadomości zweryfikuj ją na profilu — spersonalizowane zdanie w DM musi być prawdziwe.
14. Priorytet: 1 = wysoka marża + silny produkt + widoczny brak wideo; 2 = dobry produkt, mniej danych; 3 = sieciówka lub silna marka (trudniej dotrzeć do decydenta).
15. Rozkład branż (min. 2 z każdej z 6 pierwszych): stomatologia/medycyna estetyczna 5, fryzjerzy 4, siłownie 3, nieruchomości 2, detailing 2, gastronomia 4 — razem 20.
16. Adresy ulic w nazwach dopisane tam, gdzie je znalazłem, żeby łatwiej odnaleźć wizytówkę w Google Maps.

## Git
17. Zadanie mówi „push na main”, a konfiguracja sesji wymaga pracy na gałęzi `claude/tender-noether-7uvx9x`. Wypchnąłem obie: najpierw gałąź roboczą, potem `main` (zgodnie z wyraźnym poleceniem, bo GitHub Pages serwuje z `main`). Jeśli push na `main` się nie powiódł, informacja jest w podsumowaniu w czacie — wtedy wystarczy zmergować gałąź roboczą do `main` na GitHubie.

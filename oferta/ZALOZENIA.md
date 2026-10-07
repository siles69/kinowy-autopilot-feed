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

## Założenia — etap SEO / technika (2026-10-07)

18. **Godziny kontaktu** w JSON-LD (`openingHoursSpecification`): pn–pt 9:00–18:00 — przyjęte, bo nie było ich w briefie. Zmień w `index.html` (sekcja `<script type="application/ld+json">`), jeśli odpowiadasz w innych porach.
19. **Typ w danych strukturalnych:** `ProfessionalService` (podtyp `LocalBusiness`) zamiast gołego `LocalBusiness` — lepiej opisuje usługę bez lokalu. Adres tylko na poziomie miasta/województwa (`Katowice`, `śląskie`, `PL`), bez ulicy, bo działasz bez lokalu i działalność jest nierejestrowana. Nie dodawałem `aggregateRating` — nie ma prawdziwych opinii.
20. **Nazwa w JSON-LD i manifeście:** „Rolki reklamowe dla firm — Mateusz, Katowice” (bez nazwiska, bo nie było w briefie; w `sameAs` są Twoje profile IG/FB).
21. **Obraz OG** (`oferta/og.png`, 1200×630, 152 KB) wyrenderowany headless Chromium z pomocniczego HTML w stylu strony; HTML źródłowy nie jest w repo (jednorazowy). Ten sam obraz używany dla strony głównej i cennika.
22. **Favicon:** prosty kadr 9:16 z trójkątem „play” w bursztynie na ciemnym tle. ICO 32×32 i PNG 180/512 zrasteryzowane z SVG (Chromium + PIL, bo ImageMagick w tym środowisku nie ma delegata SVG). Manifest ma `display: "browser"` — to strona, nie aplikacja.
23. **Filmy:** `preload="none"` + poster, więc przy wejściu na stronę pobierają się tylko postery (~230 KB łącznie), a MP4 dopiero gdy karta jest w kadrze (autoodtwarzanie bez dźwięku) lub po kliknięciu. Przy `prefers-reduced-motion: reduce` autoodtwarzanie jest wyłączone — film startuje tylko po kliknięciu. Komunikat fallbacku zmieniony z „wrzuć plik” na „nie udało się załadować + link do MP4”, bo pliki już są.
24. **Test odtwarzania:** Chromium z Playwright w tym środowisku nie ma kodeka H.264 (`canPlayType` zwraca pusty ciąg), więc w audycie MP4 raportują `MEDIA_ERR_SRC_NOT_SUPPORTED`. To ograniczenie przeglądarki testowej, nie plików — w Chrome/Safari/Firefox H.264+AAC gra. Nie zweryfikowałem odtwarzania w prawdziwej przeglądarce; zrób to raz na telefonie po deployu.
25. **Cennik HTML** jest jednocześnie źródłem PDF — okruszki i link powrotny są ukryte w `@media print`, dlatego PDF nie zmienił układu. Dla ekranów < 700 px dodałem układ jednokolumnowy (wcześniej strona A4 na telefonie wymagała przewijania w bok).
26. **`robots.txt`, `sitemap.xml`, `404.html`, `llms.txt`** leżą w katalogu głównym repo (wymóg GitHub Pages), obok plików starego projektu — nic z nich nie ruszałem. Sitemap obejmuje tylko dwie strony oferty; starych stron `en-*/pl-*` celowo nie dodałem, bo nie są częścią oferty.
27. **Pliku `CNAME` nie tworzyłem** (brak domeny) — instrukcja w `README.md`, sekcja „Własna domena”.
28. **Ostrzeżenia konsoli:** `fonts.googleapis.com` to jedyny zewnętrzny zasób (CSS, nie skrypt). W środowisku testowym bez dostępu do Google Fonts ładowanie czcionki kończy się cicho (bez błędu w konsoli) i strona używa czcionki systemowej — tak samo zachowa się u użytkownika z blokadą.

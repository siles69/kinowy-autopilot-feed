# Arkusz pracy — sprzedaż rolek reklamowych (Katowice)

Strona portfolio: **https://siles69.github.io/kinowy-autopilot-feed/oferta/**
Cennik PDF: https://siles69.github.io/kinowy-autopilot-feed/oferta/cennik.pdf

Pliki w tym folderze:

| Plik | Do czego |
|---|---|
| `index.html` | strona portfolio (GitHub Pages) |
| `cennik.html` / `cennik.pdf` | cennik jednostronicowy — PDF do wysyłania klientom |
| `wiadomosci.md` | szablony DM / Messenger / e-mail, obiekcje, follow-up, oferta po darmowym filmie |
| `ogloszenia.md` | teksty na Useme, OLX, Fixly, grupy FB, bio IG i FB |
| `leady.csv` | lista 30 firm z Katowic do kontaktu (kolumna `email` — automat odpowiedzi działa po mailu) |
| `dzien1.md` | 8 gotowych, spersonalizowanych wiadomości na pierwszy dzień (priorytet 1) |
| `instagram-posty.md` | opisy i hashtagi do 6 rolek demo, bio i przypięty post dla @matilemek |
| `regulamin.html`, `polityka-prywatnosci.html`, `dostepnosc.html` | strony prawne i deklaracja dostępności (wersje robocze do weryfikacji) |
| `fonts/` | czcionka Inter hostowana lokalnie (licencja OFL w `fonts/LICENSE.txt`) |
| `ZALOZENIA.md` | założenia, które przyjąłem przy tworzeniu plików |

---

## Dzienny rytuał (ok. 90 minut)

1. **Zbuduj listę na dziś (15 min).** Dzień 1: wyślij osiem wiadomości z `dzien1.md`. Potem otwórz `leady.csv`. Wybierz 20 firm ze statusem pustym — zaczynaj od priorytetu 1. Gdy lista się kończy, dopisz nowe firmy: Google Maps → fraza branżowa + „Katowice” → filtruj 4,5+ → otwórz profil IG/FB → jeśli nie ma rolek z ostatnich 2 miesięcy, to lead. Min. 2 nowe branże dziennie, żeby nie wypalić jednej.

2. **Wyślij 20 wiadomości (45 min).** Dla każdej firmy: 2 minuty na profil, jedno spersonalizowane zdanie (to, co kuleje), szablon z `wiadomosci.md`. Kanał: IG DM jeśli profil żyje, Messenger jeśli FB jest głównym kanałem, e-mail do gabinetów i biur (tam częściej czyta właściciel). Po wysłaniu wpisz w kolumnę `status`: `wysłano DD.MM kanał` (np. `wysłano 07.10 IG`).

3. **Follow-upy (10 min).** Przefiltruj `status` = `wysłano` sprzed 3 dni bez odpowiedzi → wyślij follow-up (`wiadomosci.md`, sekcja 5) → status `follow-up DD.MM`. Jeśli po follow-upie nadal cisza przez 3 dni → status `brak odpowiedzi` i wracasz za 2 miesiące.

4. **Odpisz na wszystko (15 min).** Zasady:
   - „ok / tak / chętnie” → podziękuj, poproś o 3–4 zdania o ofercie i kontakt do filmu, ustal termin 48 h. Status `w produkcji`.
   - obiekcja → odpowiedź z sekcji 4 `wiadomosci.md`, zawsze zakończona pytaniem.
   - „nie, dziękuję” → jedno zdanie: „Rozumiem, dziękuję za odpowiedź. Jeśli zmieni się sytuacja, jestem pod tym numerem.” Status `odmowa`.
   - film wysłany → wiadomość z sekcji 6 (oferta pakietu). Status `film wysłany DD.MM`.
   - klient płaci → status `KLIENT Start` / `KLIENT Pro`.

5. **Policz (5 min).** Na końcu dnia dopisz w notatniku: wysłane / odpowiedzi / zgody na darmowy film / filmy wysłane / sprzedane pakiety. Cele na pierwszy miesiąc: 20 wiadomości dziennie = ~400/mies.; przy typowych 10–15% odpowiedzi to 40–60 rozmów, 15–25 darmowych filmów, 3–6 pakietów — czyli limit działalności nierejestrowanej (~3500 zł) jest w zasięgu. Jeśli odpowiedzi < 8% przez tydzień — zmień wariant wiadomości, nie branżę.

---

## Statusy w `leady.csv` (kolumna `status`)

`wysłano DD.MM kanał` → `follow-up DD.MM` → `brak odpowiedzi` / `odmowa` / `w produkcji` → `film wysłany DD.MM` → `KLIENT Start` / `KLIENT Pro` / `odmowa po filmie`

---

## Dane kontaktowe

Uzupełnione we wszystkich plikach: Instagram `instagram.com/matilemek`, Messenger `facebook.com/messages/t/MateuszLemek`, e-mail `mateuszlekem@gmail.com` (na ten adres patrzy automat przygotowujący szkice odpowiedzi — nie zmieniaj go bez aktualizacji automatu), tel. `797 224 220`, usługodawca `Mateusz Lekem`. Jeśli coś się zmieni, wyszukaj starą wartość w folderze `oferta/` i podmień, a potem wygeneruj PDF ponownie (sekcja niżej).

---

## Jak wrzucić filmy demo do `demo/`

Strona oczekuje 6 plików MP4 w folderze `demo/` w głównym katalogu repozytorium (poziom wyżej niż `oferta/`):

```
demo/demo-pizzeria.mp4
demo/demo-fryzjer.mp4
demo/demo-nieruchomosci.mp4
demo/demo-silownia.mp4
demo/demo-detailing.mp4
demo/demo-dentysta.mp4
```

Zalecenia: H.264 + AAC, 1080×1920, do ~15 MB każdy (GitHub ostrzega powyżej 50 MB, Pages ładuje się wolno przy dużych plikach). Jeśli pliki są większe, skompresuj:
```bash
ffmpeg -i wejscie.mp4 -vf scale=1080:1920 -c:v libx264 -crf 26 -preset slow -c:a aac -b:a 96k demo/demo-pizzeria.mp4
```

Wrzucenie:
```bash
git add demo/*.mp4
git commit -m "Dodaj filmy demo"
git push
```
Albo przez przeglądarkę: GitHub → folder `demo/` → „Add file” → „Upload files”.

Do momentu wrzucenia pliku każda karta na stronie pokazuje komunikat z nazwą brakującego pliku — strona działa od razu po uploadzie, bez zmian w kodzie.

---

## Jak odświeżyć `cennik.pdf`

Po edycji `cennik.html` (ceny, kontakt):
```bash
# Chrome/Chromium (Linux); na macOS zamień na /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
chromium --headless=new --no-pdf-header-footer --print-to-pdf=cennik.pdf --virtual-time-budget=4000 "file://$PWD/cennik.html"
```
Albo: otwórz `cennik.html` w Chrome → Drukuj → „Zapisz jako PDF”, marginesy „Brak”, włącz „Grafika tła”.

---

## Co dodano (SEO / technika)

**W `oferta/index.html` i `oferta/cennik.html`:**
- unikalne `<title>` (≤ 60 zn.) i `<meta name="description">` (≤ 155 zn.) z frazą „rolki reklamowe Katowice”, `<link rel="canonical">`, `theme-color`, `lang="pl"`;
- Open Graph + Twitter Card (`og:image` = `oferta/og.png`, 1200×630, generowany z `scratch` HTML w stylu strony — źródło w ZALOZENIA.md);
- dane strukturalne JSON-LD: `ProfessionalService` (nazwa, opis, obszar: Katowice/Górny Śląsk, telefon, e-mail, godziny kontaktu pn–pt 9–18) + `OfferCatalog` z trzema pakietami w PLN + `FAQPage` (5 pytań) na stronie głównej; `BreadcrumbList` + `WebPage` na cenniku;
- dokładnie jeden `<h1>` na stronę, poprawna hierarchia H1 → H2 → H3;
- favicon (`favicon.svg`, `favicon.ico` 32×32, `apple-touch-icon.png` 180×180, `icon-512.png`) + `site.webmanifest`;
- filmy: `poster` (klatki z ffmpeg, `demo/poster-*.jpg`, < 80 KB), `preload="none"`, `aria-label`, obsługa klawiatury (Enter/spacja włącza dźwięk), brak autoodtwarzania z dźwiękiem, brak autoodtwarzania przy `prefers-reduced-motion`;
- dostępność: link „Przejdź do treści”, widoczny `:focus-visible` na linkach/przyciskach/wideo, kontrasty tekstu ≥ 7:1 (sprawdzone wzorem WCAG), `<main>`, `<nav aria-label>`;
- linkowanie: nav i stopka → cennik HTML/PDF, cennik → okruszki „Oferta › Cennik” i link powrotny (ukryte w druku, więc PDF bez zmian).

**W katalogu głównym repo (GitHub Pages czyta je z roota):**
- `robots.txt` (allow all + sitemap), `sitemap.xml` (oferta + cennik, `lastmod`), `llms.txt` (opis oferty dla modeli językowych), `404.html` w stylu strony z powrotem do `/kinowy-autopilot-feed/oferta/`.

**Jak to sprawdzałem:** strony uruchomione w headless Chromium (Playwright) przez lokalny serwer HTTP z tym samym prefiksem ścieżki co Pages — zero błędów i ostrzeżeń w konsoli, zero odpowiedzi HTTP ≥ 400 dla zasobów, JSON-LD parsuje się, brak przewijania poziomego przy 390 px. Możesz powtórzyć po każdej zmianie: https://validator.schema.org/ (wklej URL strony), https://search.google.com/test/rich-results, https://developers.facebook.com/tools/debug/ (podgląd OG).

**Po zmianie treści pamiętaj:** zaktualizuj `lastmod` w `sitemap.xml`, a jeśli zmieniasz ceny — także w JSON-LD w `index.html` (sekcja `hasOfferCatalog`) i w `llms.txt`.

---

## Własna domena (gdy ją kupisz)

1. W katalogu głównym repo utwórz plik `CNAME` z samą nazwą domeny, np. `rolkikatowice.pl` (bez `https://`). Na GitHubie: Settings → Pages → Custom domain → wpisz tę samą domenę i włącz „Enforce HTTPS” (certyfikat pojawia się do ~24 h).
2. U rejestratora domeny ustaw DNS:
   - dla domeny głównej (`rolkikatowice.pl`) — cztery rekordy **A**: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (opcjonalnie AAAA: `2606:50c0:8000::153`, `8001::153`, `8002::153`, `8003::153`);
   - dla subdomeny `www` — rekord **CNAME** → `siles69.github.io`.
3. Po przepięciu zamień we wszystkich plikach `https://siles69.github.io/kinowy-autopilot-feed/` na nowy adres (`index.html`, `cennik.html`, `sitemap.xml`, `robots.txt`, `llms.txt`, `404.html`, `site.webmanifest`, `wiadomosci.md`, `ogloszenia.md`) — przy własnej domenie ścieżka `/kinowy-autopilot-feed/` znika, strona będzie pod `/oferta/`. Wygeneruj PDF ponownie.
4. Dodaj domenę w Google Search Console i wyślij `sitemap.xml`.

---

## Strony prawne i placeholdery do uzupełnienia

Dodane: `regulamin.html`, `polityka-prywatnosci.html`, `dostepnosc.html` (podlinkowane w stopkach `index.html` i `cennik.html`, dodane do `sitemap.xml`). Każdy dokument ma na górze komentarz HTML z datą i notatką „wersja robocza do weryfikacji”.

Dane usługodawcy (`Mateusz Lekem`, Katowice, `mateuszlekem@gmail.com`, `797 224 220`) są już wpisane we wszystkich dokumentach i stopkach — nie ma placeholderów `TODO_*` do uzupełnienia. Jeśli zechcesz podać adres korespondencyjny, dopisz go po „Katowice” w `regulamin.html` § 1 i `polityka-prywatnosci.html` pkt 1 (nie jest wymagany, dopóki reklamacje obsługujesz e-mailem). Gdyby nazwisko wymagało poprawki, z katalogu `oferta/`:
```bash
sed -i 's/Mateusz Lekem/Imię Nazwisko/g' index.html cennik.html regulamin.html polityka-prywatnosci.html dostepnosc.html
```
Po każdej zmianie w `cennik.html` wygeneruj PDF ponownie.

**Dwie zasady, które chronią Cię najbardziej:**
1. **Regulamin wysyłaj klientowi przed zapłatą** — link do `regulamin.html` i `polityka-prywatnosci.html` wklej do każdego maila z wyceną (szablon w `wiadomosci.md`, sekcja 6 ma już to zdanie). Bez tego klient-konsument może twierdzić, że nie znał warunków, a termin odstąpienia wydłuża się do 12 miesięcy.
2. **Przed pierwszą płatną umową daj dokumenty do przejrzenia prawnikowi** — jednorazowa weryfikacja regulaminu i polityki przez radcę prawnego kosztuje zwykle 200–400 zł i zdejmuje z Ciebie ryzyko klauzul niedozwolonych. Dokumenty są napisane prostym językiem, więc prawnik zrobi to szybko.

**Co sprawdzono pod kątem ryzyka (i co zmieniono):** usunięte sformułowania sugerujące gwarancję wyników („lepiej konwertuje”, „kilka razy większy zasięg”, „jeśli nie będzie efektu”); brak jakichkolwiek opinii i referencji — w `index.html` jest pusta, ukryta sekcja `#opinie` z komentarzem, jak ją włączyć, gdy pojawią się prawdziwe opinie za zgodą klientów; nazwy firm z demo opisane jako fikcyjne w sekcji demo, stopce, cenniku i `llms.txt`; słowo „agencja” występuje tylko w zaprzeczeniu („nie jestem agencją”); brak porównań do konkurencji; jawność AI w stopce obu stron.

**Google Fonts usunięte** — czcionka Inter jest w `oferta/fonts/` (8 plików woff2, 240 KB, ładowane tylko potrzebne zakresy znaków). Dzięki temu wejście na stronę nie wysyła adresu IP odwiedzającego do Google, a polityka prywatności może zgodnie z prawdą mówić „bez zewnętrznych skryptów i transferów”.

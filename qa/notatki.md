# QA — notatki z rund

Zrzuty: `qa/round-N/` (390×844, 768×1024, 1440×900; `*-fold.png` = widok bez przewijania, `*.png` = cała strona). Stan sprzed redesignu: `qa/before/`. Skrypt: `node qa/shoot.js qa/round-N` (wymaga lokalnego serwera z katalogu nadrzędnego repo, żeby ścieżka `/kinowy-autopilot-feed/` działała jak na Pages).

## Runda 1 (2026-10-07) — pierwszy build nowego systemu

**Własny przegląd zrzutów**
- 1440: hero zgodnie z zamierzeniem — serif 3 wiersze, trzy telefony w wachlarzu, jeden akcent. OK.
- 768: pojedynczy telefon przyklejony do prawej krawędzi, duże puste pole po lewej — **poprawka:** na 700–900 px pokazuję wachlarz trzech telefonów pod tekstem, jeden telefon tylko < 700 px.
- 390: telefon wystaje poza dolną krawędź hero (celowo, jako zachęta do przewinięcia) — zostawiam, do oceny sędziów.
- PDF cennika (z `cennik.html` + `@media print`): etykieta „Najczęściej wybierany” zawijała się na nazwę pakietu, strona miała białe marginesy — **poprawka:** `@page{margin:0}`, padding w `main`, etykieta `white-space:nowrap`. Po poprawce 1 strona A4, czcionki osadzone.
- html-validate: id sekcji zaczynały się cyfrą (`1-kto-swiadczy-usluge`) i miały zgubione „ł” — **poprawka:** prefiks `s-` + transliteracja polskich znaków; numer telefonu z twardymi spacjami (`797&nbsp;224&nbsp;220`). Reguła `aria-label-misuse` wyłączona świadomie: `aria-label` na `<video>` jest wymagany przez brief i dozwolony przez WAI-ARIA.

**Walidacje techniczne (runda 1)**
- Konsola: 0 błędów / 0 ostrzeżeń na 6 stronach. Zasoby HTTP ≥ 400: 0. Zasoby zewnętrzne: 0 (`performance.getEntriesByType('resource')` — wszystko z własnej domeny).
- JSON-LD: parsuje się na 5 stronach (404 bez JSON-LD — celowo).
- Waga bez wideo i posterów: index 32 KB HTML + 23 KB CSS + 10 plików czcionek (≈ 125 KB łącznie z HTML) — limit 300 KB.
- Lighthouse (index): desktop 100 / 100 / 100 / 100 (LCP 0,6 s, CLS 0); mobile 96 / 100 / 100 / 100 (LCP 2,6 s przy symulowanym wolnym 4G — CSS blokujący render; zostawiam czytelny CSS, próg ≥ 95 spełniony).
- html-validate (preset recommended): 0 błędów po poprawkach.
- Najmniejszy przycisk: 48 px.

**Panel sędziów rundy 1 (workflow, 8 agentów: po jednym na stronę + krytyk „premium/zakazane elementy” + sędzia spójności)** — 38 znalezisk, w tym 3 „high”:
- [high] Blok statystyk: „48” renderowało się jako 10-pikselowa miniatura, czytało się „h / 1 / 0”. Przyczyna: selektor `.stat span` łapał też licznik. → `.stat > span`.
- [high] Polityka prywatności, tabela „Cele i podstawy prawne”: `dl` z `grid-template-columns:max-content 1fr` → kolumna podstawy prawnej ściśnięta do ~110 px. → `minmax(0,5fr) minmax(0,7fr)` + linie 1 px między wierszami.
- [med] Hero 768: pojedynczy telefon przy prawej krawędzi, ucięty. → wachlarz trzech telefonów od 700 px.
- [med] Stopka: kolumna linków ~80 px, „Polityka prywatności” łamała się na dwa wiersze; kolumny poza siatką. → `.footer-grid{grid-template-columns:minmax(0,1.4fr) max-content minmax(0,1fr)}`, linki `white-space:nowrap`.
- [med] Miara wiersza w dokumentach 80–88 znaków (68ch w Inter Tight to za dużo). → `.doc{max-width:56ch}` (≈ 65–70 znaków), FAQ 54ch, lead 46ch, listy „Co dostajesz” 56ch, drobny druk 72ch.
- [med] Poświata w sekcji Kontakt przecinała linię 1 px nad sekcją. → `overflow:hidden` i poświata zaczynająca się od górnej krawędzi sekcji.
- [med] Spis treści na mobile stał przed streszczeniem i zajmował 480 px. → `<details>` zwijany poniżej 900 px (3-linijkowy skrypt), na 640–900 px dwie kolumny.
- [med] Cennik mobile: przyciski „Wróć / Pobierz PDF” zawijały się nierówno. → `.cta-row`.
- [low] Za dużo bursztynu (punktory list, plusy FAQ, myślniki). → punktory i plusy wyciszone, bursztyn tylko: CTA, numery 01–03, statystyki, obramowanie Pro, kreska eyebrow, otwarte pytanie FAQ.
- [low] Pływająca pigułka „Najczęściej wybierany” jako klisza SaaS. → etykieta jako wiersz tekstu w akcencie nad nazwą pakietu (brief wymaga etykiety i Pro w środku — zostaje w środku).
- [low] Chipy „Dla kogo” ucięte na krawędzi bez wygaszenia. → maska 56 px.
- [low] Mobilna nawigacja bez żadnego linku poza CTA. → „Cennik” zostaje widoczny, na < 480 px skrócona marka „Mateusz”.
- [low] Literówka „2026 r.. Aktualna” w regulaminie; na stronie widoczna notka „wersja robocza do weryfikacji” i data ISO. → poprawione; notka zostaje tylko w komentarzu HTML, data słownie.
- [low] Etykiety statystyk łamały się na 1440. → `.stats` od 7. kolumny, `white-space:nowrap`.
- [med] Drugi akcent: zielone wyróżnienia słów w napisach filmów (w posterach i klipach hero). → postery wycięte z klatki 0,4 s (karty tytułowe bez zielonych słów); klipów nie da się zmienić bez ponownego renderu filmów — **decyzja dla Mateusza** (patrz raport).
- Odrzucone świadomie: „kolejność cen 149 → 449 → 799” (brief: Pro w środku), „2 kolumny demo na mobile” (brief: 1 kolumna), „sticky zamiast fixed” (artefakt zrzutu — naprawiony w skrypcie: `scroll-behavior:auto` przed przewinięciem).

## Runda 2 (2026-10-07) — po poprawkach z rundy 1

Zrzuty: `qa/round-2/`. Własny przegląd: hero 1440/768/390 zgodne z zamierzeniem (postery-karty tytułowe w telefonach), polityka z proporcjonalną tabelą, stopka na siatce, html-validate 0 błędów.

**Panel sędziów rundy 2** (8 agentów; krytyk premium: „TAK z zastrzeżeniem”, sędzia spójności: „PASS z dwiema poprawkami”):
- [high] **Środek strony czarny na zrzutach całej strony** — `.reveal{opacity:0}` zdejmował tylko IntersectionObserver; po wyłączeniu płynnego przewijania w skrypcie zrzutów sekcje nie dostawały `.in`. To także realne ryzyko dla użytkownika bez JS / z błędem skryptu. → `.js .reveal` (klasa `js` dodawana pierwszym skryptem w `<head>`, bez JS wszystko widoczne), bezpiecznik `setTimeout(…,1500)` odsłaniający wszystko, a w `qa/shoot.js` odsłonięcie `.reveal` przed zrzutem całej strony.
- [med] Hero 1440: telefony nachodziły na siebie tak, że napisy w bocznych filmach były obcięte. → węższe boczne telefony (13 vw), środkowy większy, mniejsze nakładanie.
- [med] Hero 768/390: telefony ucięte dolną krawędzią hero. → telefony w przepływie dokumentu (flex), bez cięcia; na mobile jeden pełny telefon.
- [med] Cennik 768: jedna wąska kolumna kart z pustką po prawej. → 700–900 px: Pro na całą szerokość u góry, dwie karty poniżej.
- [med] Cennik: za długie wiersze w notach (87–90 zn.). → `max-width:52ch` / `60ch`.
- [med] Cennik mobile: drobny druk nad stopką powtarzał stopkę. → na ekranie jedno zdanie o cenach; pełna nota zostaje tylko w druku (PDF) jako `.print-fine`.
- [med] Dostępność: H1 i pierwsze H2 identyczne. → H2 „Zobowiązanie”.
- [med] (z rundy 1, krytyk premium) karta „149 zł” kontra „darmowy film” na tej samej karcie. → karta „Pojedynczy film — 149 zł / film”, opis „pierwszy dla nowej firmy gratis, 149 zł za kolejny”, przycisk „Zacznij od darmowego”.
- [low] potrójne linie 1 px pod nagłówkiem dokumentów na mobile → linia tylko pod zwiniętym spisem treści; linie tabeli RODO przerywane w gutterze → ciągłe; maska chipów tylko gdy mogą się nie zmieścić (< 1100 px); poświata w Kontakcie słabsza (5 %); 404: nawigacyjny CTA obrysowy (jeden bursztynowy przycisk), większa liczba, podtytuł skalowany; stopka: linki „Jak to działa”, „FAQ”, akapity 62ch; `tel:` bez łamania.
- Odrzucone: „cztery jednakowe karty kontaktu z ikonami” — brief wymaga czterech przycisków z inline SVG; „kolejność cen”, „2 kolumny demo na mobile” — jak w rundzie 1.
- PDF: reguła tabletowa (700–900 px) łapała szerokość A4 i rozbijała cennik na 2 strony → nadpisana w `@media print`.

## Runda 3 (2026-10-07) — po poprawkach z rundy 2

Zrzuty: `qa/round-3/`. Własny przegląd: pełne strony pokazują wszystkie sekcje; hero 768 z trzema telefonami w przepływie; 390 z jednym pełnym telefonem; PDF 1 strona. Walidacje: konsola 0/0 na 6 stronach, HTTP ≥ 400: 0, zasoby zewnętrzne: 0, html-validate 0, JSON-LD ok, waga bez wideo ≈ 127 KB (index), przyciski ≥ 48 px.

**Panel sędziów rundy 3** (krytyk premium: „TAK — w ~90% robota drogiego studia”; sędzia spójności: „gotowe do wypuszczenia po trzech poprawkach CSS”; 5 z 6 stron bez znalezisk „high/med”):
- [high] index 390: rząd statystyk z `white-space:nowrap` dotykał prawej krawędzi, a zdanie obok było ściśnięte do 6 kolumn (reguła `.after-steps p{grid-column:1/7}` wygrywała specyficznością z `.after-steps>*`). → statystyki zawijane (`flex-wrap`), etykiety bez `nowrap` < 480 px, zdanie na pełną szerokość.
- [med] polityka: kolumny tabeli RODO stykały się — `padding-left` nadpisany przez skrót `padding`. → kolejność reguł.
- [med] hero 1440/768: środkowy telefon zasłaniał napis w lewym. → boczne telefony dalej od środka (−6 %), środkowy węższy, na tablecie odstęp 26 px.
- [med] licznik pokazywał „0 h”, gdy animacja nie odpaliła (zrzut całej strony, brak JS). → w HTML od razu „48”, JS animuje 0 → 48 tylko gdy obserwator zadziała.
- [low] poszarpany stos `.cta-row` na mobile → przyciski na pełną szerokość < 480 px; linia bazowa cen w cenniku 1440 (etykieta Pro w przepływie) → karty bez etykiety dostają równy odstęp górny; ghostowy CTA w nawigacji 404 — zostawiony celowo (jeden bursztynowy przycisk na stronie błędu).

## Runda 4 (2026-10-07) — weryfikacja końcowa

Zrzuty: `qa/round-4/` (po poprawkach z rundy 3) i `qa/final/` (po ostatnich szlifach). Sprawdzone ręcznie: statystyki na 390 mieszczą się w marginesach 16–374 px (`scrollWidth` = 390), tabela RODO z odstępem 24 px, telefony w hero bez zasłaniania napisów, licznik „48”. Konsola 0/0 na 6 stronach, HTTP ≥ 400: 0, zasoby zewnętrzne: 0, html-validate 0, PDF 1 strona, JS w `index.html`: 41 linii.

**Wydajność po rundzie 3 (index, Lighthouse 13.5):** desktop 100 / 100 / 100 / 100 (LCP 0,6 s, CLS 0, TBT 0). Mobile początkowo 93 (LCP 3,2 s — H1 czekał na czcionki, bo 6 posterów kart demo ładowało się od razu przez atrybut `poster` i konkurowało o symulowane łącze). Zmiany: CSS inline tylko w `index.html` (podstrony: `style.css`), preload 4 plików czcionek (latin + latin-ext, serif i tekst), postery 405×720 (25–38 KB), postery kart demo jako `<img loading="lazy">` nad `<video>` (atrybut `poster` ustawiany z `data-poster` przy odtworzeniu). Wynik: **mobile 97 / 100 / 100 / 100** (LCP 2,6 s, FCP 1,5 s), dwa przebiegi zgodne. Waga index bez wideo i posterów ≈ 101 KB (HTML z inline CSS 58 KB + czcionki).

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
| `leady.csv` | lista 20 firm z Katowic do kontaktu |
| `ZALOZENIA.md` | założenia, które przyjąłem przy tworzeniu plików |

---

## Dzienny rytuał (ok. 90 minut)

1. **Zbuduj listę na dziś (15 min).** Otwórz `leady.csv`. Wybierz 20 firm ze statusem pustym — zaczynaj od priorytetu 1. Gdy lista się kończy, dopisz nowe firmy: Google Maps → fraza branżowa + „Katowice” → filtruj 4,5+ → otwórz profil IG/FB → jeśli nie ma rolek z ostatnich 2 miesięcy, to lead. Min. 2 nowe branże dziennie, żeby nie wypalić jednej.

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

Uzupełnione we wszystkich plikach: Instagram `instagram.com/matilemek`, Messenger `facebook.com/messages/t/MateuszLemek`, e-mail `odpowiedzi.opinie@gmail.com`, tel. `797 224 220`. Jeśli coś się zmieni, wyszukaj starą wartość w folderze `oferta/` i podmień, a potem wygeneruj PDF ponownie (sekcja niżej).

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

# tools/ — produkcja rolek przez Revid API

`revid_make.py` zamienia plik ze scenariuszem w gotowy MP4 9:16 (lektor AI, napisy, stock video) bez klikania w przeglądarce.

## Status: NIEPRZETESTOWANE na żywo

Skrypt powstał na podstawie publicznie opisanych pól Revid Public API v2 (`POST /api/public/v2/render`, `GET /api/public/v2/status?pid=…`, `POST /api/public/v2/calculate-credits`, nagłówek `key`). W sesji, w której powstał, domena `www.revid.ai` była zablokowana przez politykę sieciową, więc nie wykonałem ani jednego prawdziwego wywołania. Pierwsze uruchomienie zrób w kolejności: `--dry-run` → `--estimate` → render; jeśli API zwróci błąd o nieznanym polu, popraw `build_payload()` według aktualnej dokumentacji (revid.ai/docs lub kolekcja Postman „Revid Public API v3”).

## Wymagania

- Python 3.10+, biblioteka `requests` (`pip install requests`)
- Klucz API Revid **wyłącznie** w zmiennej środowiskowej:

```bash
export REVID_API_KEY="twój-klucz"        # Linux/macOS, tylko w bieżącej sesji terminala
# Windows PowerShell: $env:REVID_API_KEY="twój-klucz"
```

Nigdy nie wpisuj klucza do plików w repo. `out/` jest w `.gitignore`, więc MP4 też nie trafią do repo.

## Użycie

```bash
# 1. scenariusz = sam tekst lektora, 40–90 słów na 20–35 s
cat > scenariusz.txt <<'EOF'
Boisz się dentysty? W Klinice Dentica w Katowicach leczymy bez stresu: znieczulenie komputerowe, sedacja i spokojna atmosfera. Umów pierwszą wizytę — numer i adres na ekranie.
EOF

# 2. podgląd payloadu bez wysyłki
python3 tools/revid_make.py scenariusz.txt --dry-run

# 3. koszt w kredytach + pytanie o zgodę, potem render i pobranie do out/
python3 tools/revid_make.py scenariusz.txt --estimate

# 4. wersja angielska z głosem Brian
python3 tools/revid_make.py script_en.txt --voice Brian --name demo-en
```

Opcje: `--voice` (nazwa z `voices.json` lub ID), `--voice-id`, `--captions` (Basic, Revid, Hormozi, Ali, Wrap 1, Wrap 2, Faceless), `--media` (stockVideo, movingImage, aiVideo), `--ratio` (domyślnie `9 / 16`), `--resolution` (1080p/720p), `--webhook`, `--out`, `--name`, `--interval`, `--max-minutes`.

## Głosy

`tools/voices.json` mapuje nazwy na ID głosów (ElevenLabs). „Brian” ma wpisane publiczne ID głosu premade ElevenLabs; „Ian — Polish Narrator” to głos z biblioteki — jego ID skopiuj z panelu Revid (wybór głosu → ID) i wklej do pliku. Bez tego skrypt zatrzyma się z czytelnym komunikatem.

## Po pobraniu

- Obejrzyj film na telefonie, sprawdź lektora (polskie nazwy własne bywają czytane dziwnie — czasem pomaga zapis fonetyczny w scenariuszu).
- Filmy dla klientów trzymaj poza repo (dysk, GitHub Release `demo-videos`, Drive). Do `demo/` trafiają tylko filmy demo o fikcyjnych firmach.
- Scenariusze warto wersjonować w `tools/scenariusze/` (tekst), bo tekst jest mały i da się do niego wrócić.

## Koszty i decyzje

Każdy render zużywa kredyty z planu Revid — `--estimate` pokazuje ile przed wysłaniem. Jeśli API odpowie, że plan nie obejmuje API lub kredyty się skończyły, to decyzja do podjęcia w panelu Revid, nie w skrypcie.

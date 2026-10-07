#!/usr/bin/env python3
"""
revid_make.py — produkcja krótkiej rolki 9:16 przez Revid Public API (v2) z pliku ze scenariuszem.

Użycie (minimalne):
    export REVID_API_KEY="..."            # klucz TYLKO w zmiennej środowiskowej, nigdy w repo
    python3 tools/revid_make.py scenariusz.txt

Opcje: python3 tools/revid_make.py --help

Co robi:
  1. czyta scenariusz (tekst lektora) z pliku,
  2. (opcjonalnie) pyta API o szacunkowy koszt w kredytach (--estimate),
  3. wysyła zlecenie renderu: lektor AI + napisy + stock video + format 9:16,
  4. odpytuje status co N sekund aż pojawi się link do MP4,
  5. pobiera MP4 do katalogu out/ (katalog jest w .gitignore).

Uwaga: skrypt powstał na podstawie publicznie opisanych pól API v2 (POST /api/public/v2/render,
GET /api/public/v2/status?pid=..., POST /api/public/v2/calculate-credits, nagłówek "key").
Nazwy pól odpowiedzi statusu (np. videoUrl) mogą się różnić — skrypt szuka kilku wariantów
i w razie wątpliwości wypisuje surową odpowiedź. Pierwsze uruchomienie zrób z --dry-run, potem
z --estimate, dopiero potem render.
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("Brak biblioteki requests: pip install requests")

BASE_URL = os.environ.get("REVID_BASE_URL", "https://www.revid.ai")
RENDER = "/api/public/v2/render"
STATUS = "/api/public/v2/status"
CREDITS = "/api/public/v2/calculate-credits"

HERE = Path(__file__).resolve().parent
VOICES_FILE = HERE / "voices.json"

# Presety napisów znane z dokumentacji v2
CAPTION_PRESETS = ["Basic", "Revid", "Hormozi", "Ali", "Wrap 1", "Wrap 2", "Faceless"]


def load_voices() -> dict:
    """Mapa nazwa głosu -> ID (ElevenLabs). Edytuj tools/voices.json."""
    if VOICES_FILE.exists():
        with open(VOICES_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def resolve_voice(name_or_id: str, voices: dict) -> str:
    if not name_or_id:
        return ""
    # ID ElevenLabs: 20 znaków alfanumerycznych
    if re.fullmatch(r"[A-Za-z0-9]{20}", name_or_id):
        return name_or_id
    key = name_or_id.strip().lower()
    for name, vid in voices.items():
        if name.lower() == key or key in name.lower():
            if vid:
                return vid
            sys.exit(f"Głos „{name}” jest w voices.json, ale bez ID — uzupełnij ID z panelu Revid/ElevenLabs.")
    sys.exit(f"Nie znam głosu „{name_or_id}”. Podaj ID (--voice-id) albo dopisz do {VOICES_FILE}.")


def headers() -> dict:
    key = os.environ.get("REVID_API_KEY")
    if not key:
        sys.exit("Ustaw zmienną środowiskową REVID_API_KEY (klucz nie może być w repo).")
    return {"key": key, "Content-Type": "application/json", "Accept": "application/json"}


def build_payload(script_text: str, voice_id: str, caption_preset: str, ratio: str,
                  media_type: str, resolution: str, webhook: str | None) -> dict:
    creation = {
        "inputText": script_text,
        "hasToGenerateVoice": True,
        "selectedVoice": voice_id,
        "hasToSearchMedia": True,
        "mediaType": media_type,          # stockVideo | movingImage | aiVideo
        "captionPresetName": caption_preset,
        "ratio": ratio,                   # "9 / 16" wg dokumentacji v2
    }
    payload = {"creationParams": creation, "resolution": resolution}
    if webhook:
        payload["webhook"] = webhook
    return payload


def api_post(path: str, body: dict, timeout: int = 60) -> dict:
    r = requests.post(BASE_URL + path, headers=headers(), json=body, timeout=timeout)
    if r.status_code >= 400:
        sys.exit(f"HTTP {r.status_code} dla {path}:\n{r.text[:2000]}")
    try:
        return r.json()
    except ValueError:
        sys.exit(f"Odpowiedź {path} nie jest JSON-em:\n{r.text[:2000]}")


def api_get(path: str, params: dict, timeout: int = 60) -> dict:
    r = requests.get(BASE_URL + path, headers=headers(), params=params, timeout=timeout)
    if r.status_code >= 400:
        sys.exit(f"HTTP {r.status_code} dla {path}:\n{r.text[:2000]}")
    try:
        return r.json()
    except ValueError:
        sys.exit(f"Odpowiedź {path} nie jest JSON-em:\n{r.text[:2000]}")


def find_first(d, keys):
    """Zwraca pierwszą znalezioną wartość spośród kluczy (także zagnieżdżone 1 poziom)."""
    if not isinstance(d, dict):
        return None
    for k in keys:
        if k in d and d[k]:
            return d[k]
    for v in d.values():
        if isinstance(v, dict):
            for k in keys:
                if k in v and v[k]:
                    return v[k]
    return None


def wait_for_video(pid: str, interval: int, max_minutes: int) -> str:
    deadline = time.time() + max_minutes * 60
    last_status = None
    while time.time() < deadline:
        data = api_get(STATUS, {"pid": pid})
        url = find_first(data, ["videoUrl", "video_url", "url", "downloadUrl", "outputUrl", "mp4Url"])
        status = find_first(data, ["status", "state", "progress"])
        if status != last_status:
            print(f"  status: {status}")
            last_status = status
        if isinstance(status, str) and status.lower() in {"error", "failed", "failure"}:
            sys.exit(f"Render zakończył się błędem. Surowa odpowiedź:\n{json.dumps(data, ensure_ascii=False, indent=1)}")
        if url and isinstance(url, str) and url.startswith("http"):
            return url
        time.sleep(interval)
    sys.exit(f"Przekroczono {max_minutes} min oczekiwania. Sprawdź pid={pid} w panelu Revid.")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                f.write(chunk)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[ąćęłńóśźż]", lambda m: "acelnoszz"["ąćęłńóśźż".index(m.group(0))], text)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:40] or "rolka"


def main() -> None:
    p = argparse.ArgumentParser(description="Rolka 9:16 z pliku scenariusza przez Revid API v2")
    p.add_argument("script", help="plik tekstowy ze scenariuszem (tekst lektora)")
    p.add_argument("--voice", default="Ian — Polish Narrator",
                   help='nazwa głosu z tools/voices.json (domyślnie "Ian — Polish Narrator"; EN: "Brian") albo ID ElevenLabs')
    p.add_argument("--voice-id", default="", help="bezpośrednio ID głosu (nadpisuje --voice)")
    p.add_argument("--captions", default="Wrap 1", choices=CAPTION_PRESETS, help="preset napisów")
    p.add_argument("--media", default="stockVideo", choices=["stockVideo", "movingImage", "aiVideo"])
    p.add_argument("--ratio", default="9 / 16", help='format, domyślnie "9 / 16"')
    p.add_argument("--resolution", default="1080p", choices=["1080p", "720p"])
    p.add_argument("--webhook", default=None, help="opcjonalny URL webhooka (zamiast odpytywania)")
    p.add_argument("--out", default=str(HERE.parent / "out"), help="katalog wyjściowy (domyślnie out/)")
    p.add_argument("--name", default="", help="nazwa pliku wynikowego bez rozszerzenia")
    p.add_argument("--interval", type=int, default=15, help="co ile sekund pytać o status")
    p.add_argument("--max-minutes", type=int, default=30, help="maksymalny czas oczekiwania")
    p.add_argument("--estimate", action="store_true", help="najpierw policz koszt w kredytach i zapytaj o zgodę")
    p.add_argument("--dry-run", action="store_true", help="tylko wypisz payload, nic nie wysyłaj")
    args = p.parse_args()

    script_text = Path(args.script).read_text(encoding="utf-8").strip()
    if not script_text:
        sys.exit("Plik scenariusza jest pusty.")
    words = len(script_text.split())
    print(f"Scenariusz: {words} słów (~{round(words / 2.5)} s lektora)")

    voices = load_voices()
    voice_id = args.voice_id or resolve_voice(args.voice, voices)
    payload = build_payload(script_text, voice_id, args.captions, args.ratio, args.media,
                            args.resolution, args.webhook)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=1))
        return

    if args.estimate:
        est = api_post(CREDITS, {"creationParams": payload["creationParams"]})
        print("Szacunek kosztu:", json.dumps(est, ensure_ascii=False))
        if input("Renderować? [t/N] ").strip().lower() not in {"t", "tak", "y", "yes"}:
            print("Przerwano.")
            return

    print("Wysyłam zlecenie renderu…")
    res = api_post(RENDER, payload)
    pid = find_first(res, ["pid", "projectId", "id"])
    if not pid:
        sys.exit(f"Brak pid w odpowiedzi:\n{json.dumps(res, ensure_ascii=False, indent=1)}")
    print(f"  pid: {pid}")

    if args.webhook:
        print("Podano webhook — wynik przyjdzie na webhook. Koniec.")
        return

    url = wait_for_video(str(pid), args.interval, args.max_minutes)
    name = args.name or f"{time.strftime('%Y%m%d-%H%M')}-{slugify(script_text[:60])}"
    dest = Path(args.out) / f"{name}.mp4"
    print(f"Pobieram: {url}\n  -> {dest}")
    download(url, dest)
    print(f"Gotowe: {dest} ({dest.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

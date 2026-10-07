#!/usr/bin/env python3
"""
Builder stron oferty. Składa index.html, cennik.html, strony prawne i 404.html
z jednego systemu (oferta/style.css), zachowując meta, JSON-LD i treści prawne
ze „starych” wersji w qa/old/. Uruchamiaj z katalogu głównego repo:

    python3 qa/build_pages.py

Treści prawne edytuj w qa/old/*.html (sekcja po <p class="meta">), potem przebuduj.
"""
import json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD = ROOT / "qa" / "old"
OUT = ROOT / "oferta"
BASE = "https://siles69.github.io/kinowy-autopilot-feed/oferta/"
YEAR = "2026"
DATE = "2026-10-07"

ICONS = {
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.4 5.4a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM21.9 7.9c-.1-1.6-.4-3-1.6-4.2S17.7 2.2 16.1 2.1C14.4 2 9.6 2 7.9 2.1 6.3 2.2 4.9 2.5 3.7 3.7S2.2 6.3 2.1 7.9C2 9.6 2 14.4 2.1 16.1c.1 1.6.4 3 1.6 4.2s2.6 1.5 4.2 1.6c1.7.1 6.5.1 8.2 0 1.6-.1 3-.4 4.2-1.6s1.5-2.6 1.6-4.2c.1-1.7.1-6.5 0-8.2zm-2.2 10c-.3.9-1 1.5-1.9 1.9-1.3.5-4.4.4-5.8.4s-4.5.1-5.8-.4c-.9-.3-1.5-1-1.9-1.9-.5-1.3-.4-4.4-.4-5.8s-.1-4.5.4-5.8c.3-.9 1-1.5 1.9-1.9 1.3-.5 4.4-.4 5.8-.4s4.5-.1 5.8.4c.9.3 1.5 1 1.9 1.9.5 1.3.4 4.4.4 5.8s.1 4.5-.4 5.8z"/></svg>',
    "msg": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C6.4 2 2 6.1 2 11.3c0 2.9 1.4 5.5 3.6 7.2V22l3.4-1.9c.9.3 1.9.4 3 .4 5.6 0 10-4.1 10-9.3S17.6 2 12 2zm1 12.5l-2.6-2.7-5 2.7 5.5-5.8 2.6 2.7 4.9-2.7-5.4 5.8z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"/></svg>',
    "tel": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>',
    "play": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>',
}

FAQ = [
    ("Ile to trwa?", "Pierwszy film dostajesz w ciągu 48 godzin od momentu, gdy prześlesz mi opis firmy. W pakietach filmy przychodzą regularnie: w Start — jeden tygodniowo, w Pro — dwa tygodniowo. Poprawki robię zwykle tego samego lub następnego dnia."),
    ("Czy potrzebuję własnych zdjęć albo nagrań?", "Nie. Standardowo pracuję na materiale stockowym dobranym do branży i scenariusza. Jeśli masz własne zdjęcia lub filmy (wnętrze lokalu, efekty zabiegów, gotowe auto), zmontuję z nich — to dopłata 100 zł za film; prawdziwe wnętrze lub efekty zwykle wyglądają bardziej wiarygodnie niż stock."),
    ("Czy publikujecie filmy za mnie?", "W pakiecie Pro tak — wrzucam filmy na Twój TikTok, Instagram i Facebook razem z opisem i hashtagami, według ustalonego harmonogramu. W pakiecie Start i filmie testowym dostajesz gotowe pliki i publikujesz sam. Nie potrzebuję hasła do Twoich kont — wystarczy dostęp jako współpracownik w Meta Business lub przesłanie filmów do akceptacji."),
    ("Jak płacę?", "Przelewem na konto, z góry za miesiąc pakietu; zaczynam po zaksięgowaniu. Wystawiam rachunek — prowadzę działalność nierejestrowaną, więc nie ma faktury VAT, ale rachunek możesz wrzucić w koszty. Darmowy film to naprawdę darmowy film: zero płatności, zero zobowiązań."),
    ("Czy mogę zrezygnować?", "Tak, w każdym momencie — pakiet rozliczam co miesiąc, bez umowy na czas określony i bez okresu wypowiedzenia. Jeśli po pierwszym miesiącu uznasz, że to nie dla Ciebie, po prostu nie przedłużasz. Wszystkie filmy, które dostałeś, zostają Twoje."),
    ("Czy film będzie wyglądał jak AI?", "Lektor jest generowany przez AI i nie udaję, że to aktor — ale materiał wideo jest prawdziwy (stock albo Twoje nagrania), scenariusz piszę sam pod Twoją ofertę, a napisy i montaż robię ręcznie. Najprościej ocenić to na własnym przykładzie: jeśli po obejrzeniu darmowego filmu uznasz, że brzmi sztucznie, nie płacisz nic i nie musisz go używać."),
    ("Czy mogę zamówić jeden film bez pakietu?", "Tak — pojedynczy film kosztuje 149 zł. Pierwszy film dla nowej firmy jest gratis, więc płacisz dopiero za drugi. Pakiety opłacają się, gdy chcesz publikować regularnie: w Start jeden film wychodzi po 112 zł, w Pro — po 100 zł z publikacją."),
]

DEMOS = [
    ("pizzeria", "Gastronomia", "Pizzeria — wyjątkowa pizza z pieca, zamówienie na dziś z dowozem.", "Przykładowa firma „Da Marco”", "Film demo dla pizzerii — przykładowa firma Da Marco"),
    ("fryzjer", "Beauty", "Salon fryzjerski — nowa fryzura, nowa energia, rezerwacja terminu online.", "Przykładowa firma „Studio Nova”", "Film demo dla salonu fryzjerskiego — przykładowa firma Studio Nova"),
    ("nieruchomosci", "Nieruchomości", "Oferta mieszkania — metraż, układ, cena i kontakt do agenta w 30 sekund.", "Przykładowa oferta agenta", "Film demo z ofertą mieszkania — przykładowa oferta agenta nieruchomości"),
    ("silownia", "Fitness", "Siłownia — plan, który przetrwa poniedziałek: pierwszy trening i karnet.", "Przykładowa firma „FitZone”", "Film demo dla siłowni — przykładowa firma FitZone"),
    ("detailing", "Motoryzacja", "Detailing — przywróć blask swojemu autu: powłoka, przed i po, cena.", "Przykładowa firma „AutoGlanz”", "Film demo dla studia detailingu — przykładowa firma AutoGlanz"),
    ("dentysta", "Stomatologia", "Gabinet — dentysta bez stresu: pierwsza wizyta i jak się umówić.", "Przykładowa firma „Klinika Dentica”", "Film demo dla gabinetu stomatologicznego — przykładowa firma Klinika Dentica"),
]


PL = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")


def slug(text):
    t = unicodedata.normalize("NFKD", text.translate(PL)).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return "s-" + t[:46]


def head_meta(old_html, drop_ld=False):
    """Zbiera <title>, <meta>, <link canonical/icon/manifest> i JSON-LD ze starego pliku."""
    head = re.search(r"<head>(.*?)</head>", old_html, re.S).group(1)
    keep = []
    for line in head.splitlines():
        s = line.strip()
        if s.startswith("<title") or s.startswith("<meta") or re.match(r'<link rel="(canonical|icon|apple-touch-icon|manifest)"', s):
            keep.append(s)
    ld = re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', head, re.S)
    ld_obj = json.loads(ld.group(1)) if ld else None
    return keep, ld_obj


def shell(meta_lines, ld_obj, body, css="style.css", nav_prefix="", extra_head="", body_class="", inline_css=False):
    ld = f'<script type="application/ld+json">\n{json.dumps(ld_obj, ensure_ascii=False, indent=1)}\n</script>\n' if ld_obj else ""
    # Strona główna: CSS inline (jedno żądanie mniej na ścieżce LCP). Podstrony: wspólny plik style.css.
    if inline_css:
        css_src = (OUT / "style.css").read_text(encoding="utf-8").replace("url(fonts/", "url(fonts/")
        css_tag = "<style>\n" + css_src + "\n</style>"
    else:
        css_tag = f'<link rel="stylesheet" href="{css}">'
    nav = f"""<a class="skip" href="#main">Przejdź do treści</a>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="{nav_prefix}./">Mateusz <span>· rolki reklamowe</span></a>
    <nav aria-label="Główna">
      <a href="{nav_prefix}./#demo">Przykłady</a>
      <a href="{nav_prefix}./#jak">Jak to działa</a>
      <a class="keep" href="{nav_prefix}cennik.html">Cennik</a>
      <a href="{nav_prefix}./#faq">FAQ</a>
      <a class="btn primary" href="{nav_prefix}./#kontakt">Pierwszy film gratis</a>
    </nav>
  </div>
</header>
"""
    footer = f"""<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <p><strong style="color:var(--text)">Mateusz Lekem</strong> · Katowice<br>działalność nierejestrowana (art. 5 ustawy Prawo przedsiębiorców) — wystawiam rachunek, nie fakturę VAT</p>
        <p><a href="mailto:mateuszlekem@gmail.com">mateuszlekem@gmail.com</a> · <a href="tel:+48797224220">797 224 220</a></p>
      </div>
      <div>
        <nav aria-label="Stopka">
          <a href="{nav_prefix}./#demo">Przykłady</a>
          <a href="{nav_prefix}./#jak">Jak to działa</a>
          <a href="{nav_prefix}./#faq">FAQ</a>
          <a href="{nav_prefix}cennik.html">Cennik</a>
          <a href="{nav_prefix}branze/">Branże</a>
          <a href="{nav_prefix}dla-agencji.html">Dla agencji</a>
          <a href="{nav_prefix}cennik.pdf">Cennik PDF</a>
          <a href="{nav_prefix}regulamin.html">Regulamin</a>
          <a href="{nav_prefix}polityka-prywatnosci.html">Polityka prywatności</a>
          <a href="{nav_prefix}dostepnosc.html">Dostępność</a>
        </nav>
      </div>
      <div>
        <p>Filmy powstają z użyciem narzędzi AI (lektor, montaż). Materiał wideo pochodzi z licencjonowanych bibliotek lub od klienta.</p>
        <p>Ceny na stronie są cenami końcowymi w PLN.</p>
      </div>
    </div>
    <div class="copy">
      <span>© {YEAR} Mateusz Lekem · Katowice</span>
      <span>Nazwy firm w filmach demo są fikcyjne — to przykłady formatu, nie klienci.</span>
    </div>
  </div>
</footer>
"""
    html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
{chr(10).join(meta_lines)}
<script>document.documentElement.classList.add("js")</script>
{css_tag}
{extra_head}{ld}</head>
<body{(' class="' + body_class + '"') if body_class else ''}>
{nav}{body}
{footer}</body>
</html>
"""
    return html.replace("797 224 220", "797&nbsp;224&nbsp;220")


# ------------------------------------------------------------------ INDEX
def build_index():
    old = (OLD / "index.html").read_text(encoding="utf-8")
    meta, ld = head_meta(old)
    # FAQ w JSON-LD = FAQ na stronie
    for node in ld["@graph"]:
        if node.get("@type") == "FAQPage":
            node["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]
    # dodatkowo: preload krytycznych czcionek
    extra = ('<link rel="preload" href="fonts/instrument-serif-latin-400.woff2" as="font" type="font/woff2" crossorigin>\n'
             '<link rel="preload" href="fonts/instrument-serif-latin-ext-400.woff2" as="font" type="font/woff2" crossorigin>\n'
             '<link rel="preload" href="fonts/inter-tight-latin-400.woff2" as="font" type="font/woff2" crossorigin>\n'
             '<link rel="preload" href="fonts/inter-tight-latin-ext-400.woff2" as="font" type="font/woff2" crossorigin>\n')

    demos = "\n".join(f"""      <article class="demo reveal">
        <div class="frame">
          <img class="poster" src="../demo/poster-{k}.jpg" alt="" width="405" height="720" loading="lazy" decoding="async">
          <video src="../demo/demo-{k}.mp4" data-poster="../demo/poster-{k}.jpg" preload="none" playsinline aria-label="{aria}">Twoja przeglądarka nie obsługuje wideo. <a href="../demo/demo-{k}.mp4">Pobierz film</a>.</video>
          <button class="play" type="button" aria-label="Odtwórz: {branza.lower()}"><span>{ICONS['play']}</span></button>
        </div>
        <div class="cap">
          <h3>{branza}</h3>
          <p>{sells}</p>
          <small>{note} · materiał stockowy, lektor AI</small>
        </div>
      </article>""" for k, branza, sells, note, aria in DEMOS)

    faq = "\n".join(f"""      <details{' open' if i == 0 else ''}>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>""" for i, (q, a) in enumerate(FAQ))

    body = f"""<main id="main">

<!-- 1. HERO -->
<section class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div class="hero-copy">
        <p class="eyebrow">Rolki reklamowe · Katowice i Śląsk</p>
        <h1>Twoja firma zasługuje na film, który ktoś obejrzy do końca.</h1>
        <p class="lead">Pionowe filmy 9:16, 20–35 sekund, z polskim lektorem i napisami — gotowe na Instagram, TikTok i Facebook. Pierwszy robię w 48 godzin i nic za niego nie płacisz.</p>
        <div class="cta-row">
          <a class="btn primary" href="#kontakt">Zrób mi darmowy film</a>
          <a class="btn" href="#demo">Zobacz 6 przykładów</a>
        </div>
        <p class="trust"><span>Katowice i Śląsk</span><span>produkcja w 48 h</span><span>bez umowy na rok</span></p>
      </div>
      <div class="hero-visual" aria-hidden="true">
        <div class="phones">
          <div class="phone a"><div class="screen"><video src="../demo/hero-fryzjer.mp4" poster="../demo/poster-fryzjer.jpg" muted loop playsinline preload="metadata" tabindex="-1"></video></div></div>
          <div class="phone b"><div class="screen"><video src="../demo/hero-pizzeria.mp4" poster="../demo/poster-pizzeria.jpg" muted loop playsinline preload="metadata" tabindex="-1"></video></div></div>
          <div class="phone c"><div class="screen"><video src="../demo/hero-detailing.mp4" poster="../demo/poster-detailing.jpg" muted loop playsinline preload="metadata" tabindex="-1"></video></div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- 2. DLA KOGO -->
<section class="industries" aria-label="Dla kogo">
  <div class="wrap">
    <span class="label">Dla kogo</span>
    <div class="chips">
      <a class="chip" href="branze/stomatologia.html">stomatologia</a><a class="chip" href="branze/medycyna-estetyczna.html">medycyna estetyczna</a><a class="chip" href="branze/salony-fryzjerskie-beauty.html">beauty i fryzjerzy</a><a class="chip" href="branze/silownie-trenerzy.html">siłownie i trenerzy</a><a class="chip" href="branze/nieruchomosci.html">nieruchomości</a><a class="chip" href="branze/detailing-warsztaty.html">detailing i warsztaty</a><a class="chip" href="branze/gastronomia.html">gastronomia</a><a class="chip" href="branze/szkoly-jazdy.html">szkoły jazdy</a><a class="chip" href="branze/fotowoltaika-pompy-ciepla.html">fotowoltaika i OZE</a><a class="chip" href="branze/biura-rachunkowe-kancelarie.html">biura rachunkowe</a><a class="chip" href="dla-agencji.html">dla agencji</a>
    </div>
  </div>
</section>

<!-- 3. DEMO -->
<section id="demo">
  <div class="wrap">
    <div class="section-head reveal">
      <h2><span class="eyebrow">Przykłady</span>Sześć przykładów, sześć branż.</h2>
      <p class="lead">Każdy z tych filmów powstał dla wymyślonej firmy — tak samo powstanie Twój, tylko z Twoją nazwą, ofertą i kontaktem. Kliknij, żeby obejrzeć z dźwiękiem.</p>
    </div>
    <div class="demo-grid">
{demos}
    </div>
  </div>
</section>

<!-- 4. JAK TO DZIAŁA -->
<section id="jak">
  <div class="wrap">
    <div class="section-head reveal">
      <h2><span class="eyebrow">Proces</span>Jak to działa.</h2>
      <p class="lead">Trzy kroki, z których Ty robisz jeden. Resztą zajmuję się ja.</p>
    </div>
    <ol class="steps reveal" style="list-style:none;margin:0;padding-left:0">
      <li class="step"><div class="n">01</div><h3>Piszesz 3 zdania o ofercie</h3><p>Nazwa firmy, co oferujesz i dla kogo, co Cię wyróżnia, kontakt. Wystarczy wiadomość — resztę dopytam.</p></li>
      <li class="step"><div class="n">02</div><h3>W 48 h dostajesz film do akceptacji</h3><p>Scenariusz, polski lektor, napisy, muzyka i materiał dobrany do branży. Jedna runda poprawek w cenie.</p></li>
      <li class="step"><div class="n">03</div><h3>Publikujesz albo publikuję za Ciebie</h3><p>Plik MP4 w pionie, gotowy na Instagram, TikTok i Facebook. W pakiecie Pro dodaję opisy, hashtagi i wrzucam na Twoje profile.</p></li>
    </ol>
    <div class="after-steps reveal">
      <p>Nie potrzebujesz nagrań, aktorów ani studia.</p>
      <div class="stats">
        <div class="stat"><b><span data-count="48">48</span> h</b><span>od opisu do filmu</span></div>
        <div class="stat"><b>1</b><span>runda poprawek w cenie</span></div>
        <div class="stat"><b>0</b><span>nagrań od Ciebie</span></div>
      </div>
    </div>
  </div>
</section>

<!-- 5. DLACZEGO -->
<section id="dlaczego">
  <div class="wrap">
    <div class="section-head reveal">
      <h2><span class="eyebrow">Uczciwie</span>Co dostajesz — i czego nie obiecuję.</h2>
      <p class="lead">Wolę powiedzieć wprost, co jest w cenie, niż obiecywać rzeczy, na które nie mam wpływu.</p>
    </div>
    <div class="two reveal">
      <div>
        <h3>Co dostajesz</h3>
        <ul class="plain">
          <li>Scenariusz napisany pod Twoją ofertę <span>— nie szablon z podmienioną nazwą.</span></li>
          <li>Polski lektor, napisy i muzyka z licencją <span>— plik gotowy do publikacji bez dalszej obróbki.</span></li>
          <li>Materiał wideo dobrany do branży <span>— albo zmontowany z Twoich zdjęć i nagrań.</span></li>
          <li>MP4 1080×1920 <span>— działa na Instagramie, TikToku, Facebooku i na ekranie w lokalu.</span></li>
          <li>Jedną rundę poprawek w cenie i rachunek <span>— bez umowy na czas określony.</span></li>
        </ul>
      </div>
      <div>
        <h3>Czego nie robię</h3>
        <ul class="plain no">
          <li>Nie obiecuję viralu ani liczby wyświetleń <span>— tego nie da się uczciwie obiecać.</span></li>
          <li>Nie robię długich filmów, spotów ani nagrań na miejscu <span>— tylko krótkie rolki pionowe.</span></li>
          <li>Nie prowadzę płatnych kampanii <span>— dostarczam film, który możesz w nich użyć.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- 6. CENNIK -->
<section id="cennik">
  <div class="wrap">
    <div class="section-head reveal">
      <h2><span class="eyebrow">Cennik</span>Proste ceny, bez niespodzianek.</h2>
      <p class="lead">Rozliczenie miesięczne, rezygnacja w dowolnym momencie. <a href="cennik.html">Cennik na osobnej stronie</a> albo <a href="cennik.pdf">w PDF</a>.</p>
    </div>
    <div class="plans reveal">
      <div class="plan">
        <div class="name">Pojedynczy film</div>
        <div class="price">149 zł<small>/ film</small></div>
        <p class="sub">Jeden film bez pakietu. Pierwszy dla nowej firmy jest gratis — 149 zł płacisz dopiero za kolejny.</p>
        <ul><li>1 rolka 9:16, 20–35 s</li><li>polski lektor AI i napisy</li><li>materiał stockowy</li><li>1 runda poprawek</li></ul>
        <a class="btn" href="#kontakt">Zacznij od darmowego</a>
      </div>
      <div class="plan featured">
        <span class="tag">Najczęściej wybierany</span>
        <div class="name">Pakiet Pro</div>
        <div class="price">799 zł<small>/ miesiąc</small></div>
        <p class="sub">Dwa filmy tygodniowo i publikacja na Twoich profilach.</p>
        <ul><li>8 rolek miesięcznie</li><li>publikacja na TikTok, Instagram i Facebook</li><li>opisy postów i hashtagi</li><li>lektor, napisy, muzyka</li><li>1 runda poprawek na film</li></ul>
        <a class="btn primary" href="#kontakt">Wybieram Pro</a>
      </div>
      <div class="plan">
        <div class="name">Pakiet Start</div>
        <div class="price">449 zł<small>/ miesiąc</small></div>
        <p class="sub">Jeden nowy film tygodniowo. Ty publikujesz.</p>
        <ul><li>4 rolki miesięcznie</li><li>lektor, napisy, muzyka</li><li>materiał stockowy</li><li>1 runda poprawek na film</li><li>pliki gotowe do publikacji</li></ul>
        <a class="btn" href="#kontakt">Wybieram Start</a>
      </div>
    </div>
    <div class="price-notes reveal">
      <p>Pierwszy film zawsze gratis — niezależnie od pakietu.</p>
      <p>Ceny końcowe w PLN, rachunek, bez VAT, bez zobowiązań na rok. Montaż z Twoich zdjęć lub nagrań: +100 zł za film.</p>
    </div>
  </div>
</section>

<!-- 7. FAQ -->
<section id="faq">
  <div class="wrap">
    <div class="section-head reveal">
      <h2><span class="eyebrow">FAQ</span>Najczęstsze pytania.</h2>
    </div>
    <div class="faq reveal">
{faq}
    </div>
  </div>
</section>

<!-- 8. KONTAKT -->
<section id="kontakt" class="contact">
  <div class="wrap">
    <p class="eyebrow">Kontakt</p>
    <h2>Napisz, a za 48 h masz pierwszy film.</h2>
    <p class="lead">Najszybciej przez Instagram albo Messenger. Odpowiadam w dni robocze, zwykle w kilka godzin. Jestem z Katowic — mogę też wpaść osobiście.</p>
    <div class="contact-grid">
      <a class="btn primary" href="https://www.instagram.com/matilemek/" target="_blank" rel="noopener">{ICONS['ig']}Instagram DM<small>@matilemek</small></a>
      <a class="btn" href="https://www.facebook.com/messages/t/MateuszLemek" target="_blank" rel="noopener">{ICONS['msg']}Messenger<small>Mateusz Lemek</small></a>
      <a class="btn" href="mailto:mateuszlekem@gmail.com">{ICONS['mail']}E-mail<small>mateuszlekem@gmail.com</small></a>
      <a class="btn" href="tel:+48797224220">{ICONS['tel']}Telefon<small>797 224 220</small></a>
    </div>
    <p class="consent">Wysyłając wiadomość, zgadzasz się na kontakt w sprawie oferty. Szczegóły w <a href="polityka-prywatnosci.html">polityce prywatności</a>. Zasady współpracy opisuje <a href="regulamin.html">regulamin</a>.</p>
  </div>
</section>

<!--
  OPINIE KLIENTÓW — sekcja celowo PUSTA i UKRYTA (hidden).
  Włącz dopiero, gdy masz prawdziwe opinie od klientów, którzy wyrazili zgodę na publikację
  (imię/nazwa firmy + treść + data). Nie wstawiaj opinii wymyślonych ani „przykładowych”.
  Żeby włączyć: usuń atrybut hidden i wypełnij <blockquote>.
-->
<section id="opinie" hidden aria-hidden="true">
  <div class="wrap">
    <div class="section-head"><h2><span class="eyebrow">Opinie</span>Co mówią klienci.</h2></div>
    <div class="two">
      <!-- <figure style="margin:0"><blockquote class="serif" style="font-size:28px;margin:0 0 12px">„…”</blockquote><figcaption class="muted">Imię, nazwa firmy, miesiąc rok</figcaption></figure> -->
    </div>
  </div>
</section>

</main>
""" + r"""<script>
(function(){
  var rm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;
  // 1. Pojawianie się sekcji — raz, 8 px + opacity (patrz .reveal w style.css)
  var els = document.querySelectorAll('.reveal');
  if (rm || !hasIO) { els.forEach(function(e){ e.classList.add('in'); }); }
  else {
    var io = new IntersectionObserver(function(en){ en.forEach(function(x){ if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { threshold: .12 });
    els.forEach(function(e){ io.observe(e); });
    setTimeout(function(){ els.forEach(function(e){ e.classList.add('in'); }); }, 1500); // bezpiecznik: nic nie zostaje ukryte
  }
  // 2. Telefony w hero: autoodtwarzanie bez dźwięku tylko gdy widoczne (nie przy reduced motion)
  var hv = document.querySelectorAll('.phone video');
  if (!rm && hasIO) {
    var ho = new IntersectionObserver(function(en){ en.forEach(function(x){ x.isIntersecting ? x.target.play().catch(function(){}) : x.target.pause(); }); }, { threshold: .3 });
    hv.forEach(function(v){ ho.observe(v); });
  }
  // 3. Demo: odtwarzanie po kliknięciu, z dźwiękiem, jeden film naraz
  var current = null;
  document.querySelectorAll('.demo').forEach(function(card){
    var v = card.querySelector('video'), btn = card.querySelector('.play');
    btn.addEventListener('click', function(){
      if (current && current !== v) { current.pause(); current.controls = false; current.closest('.demo').classList.remove('playing'); }
      if (!v.poster) v.poster = v.getAttribute('data-poster');
      card.classList.add('playing'); v.controls = true; v.muted = false; current = v; v.play().catch(function(){});
    });
    v.addEventListener('ended', function(){ card.classList.remove('playing'); v.controls = false; v.currentTime = 0; });
  });
  // 4. Licznik 0 → 48 w sekcji „jak to działa”
  var c = document.querySelector('[data-count]');
  if (c) {
    var target = +c.getAttribute('data-count');
    if (!(rm || !hasIO)) { // bez JS/IO zostaje statyczne „48”
      var co = new IntersectionObserver(function(en){
        if (!en[0].isIntersecting) return; co.disconnect();
        var t0 = performance.now();
        (function tick(now){ var p = Math.min(1, (now - t0) / 900); c.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(tick); })(t0);
      }, { threshold: .5 });
      co.observe(c);
    }
  }
})();
</script>"""
    (OUT / "index.html").write_text(shell(meta, ld, body, extra_head=extra, inline_css=True), encoding="utf-8")
    print("index.html")


# ------------------------------------------------------------------ DOKUMENTY
def build_doc(fname, crumb):
    old = (OLD / fname).read_text(encoding="utf-8")
    meta, ld = head_meta(old)
    h1 = re.search(r"<h1>(.*?)</h1>", old, re.S).group(1).strip()
    body = re.search(r'<p class="meta">.*?</p>\n(.*?)\n  </div>\n</main>', old, re.S).group(1)
    # id-ki na h2 + spis treści
    toc = []
    def add_id(m):
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        i = slug(title)
        toc.append((i, title))
        return f'<h2 id="{i}">{m.group(1)}</h2>'
    body = re.sub(r"<h2>(.*?)</h2>", add_id, body)
    toc_html = ""
    if len(toc) >= 3:
        toc_html = '<aside class="toc" aria-label="Spis treści"><details open><summary>Spis treści</summary><ol>' + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc) + "</ol></details></aside>"
    page = f"""<main id="main" class="page">
  <div class="wrap">
    <nav class="crumbs" aria-label="Okruszki"><a href="./">Oferta</a><span class="sep" aria-hidden="true">›</span><span aria-current="page">{crumb}</span></nav>
    <div class="doc-head">
      <h1>{h1}</h1>
      <p class="meta">Wersja z 7 października 2026 r.<br>Usługodawca: Mateusz Lekem, Katowice.</p>
    </div>
    <div class="doc-layout">
      <article class="doc">
{body}
      </article>
      {toc_html}
    </div>
  </div>
</main>
<script>if (window.innerWidth < 900) {{ var d = document.querySelector('.toc details'); if (d) d.open = false; }}</script>"""
    comment = f"<!-- {DATE} — wersja robocza do weryfikacji przez prawnika. Nie stanowi porady prawnej. -->\n"
    html = shell(meta, ld, page)
    html = html.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + comment, 1)
    (OUT / fname).write_text(html, encoding="utf-8")
    print(fname, "TOC:", len(toc))


# ------------------------------------------------------------------ CENNIK
def build_cennik():
    old = (OLD / "cennik.html").read_text(encoding="utf-8")
    meta, ld = head_meta(old)
    body = f"""<main id="main" class="page cennik-page">
  <div class="wrap">
    <nav class="crumbs" aria-label="Okruszki"><a href="./">Oferta</a><span class="sep" aria-hidden="true">›</span><span aria-current="page">Cennik</span></nav>
    <div class="doc-head">
      <h1>Cennik rolek reklamowych.</h1>
      <p class="meta">Ceny końcowe w PLN. Rozliczenie miesięczne, rezygnacja w dowolnym momencie, bez umowy na czas określony. Wystawiam rachunek — bez VAT.</p>
    </div>

    <div class="plans">
      <div class="plan">
        <div class="name">Pojedynczy film</div>
        <div class="price">149 zł<small>/ film</small></div>
        <p class="sub">Jeden film bez pakietu. Pierwszy dla nowej firmy jest gratis — 149 zł płacisz dopiero za kolejny.</p>
        <ul><li>1 rolka 9:16, 20–35 s</li><li>polski lektor AI i napisy</li><li>materiał stockowy</li><li>1 runda poprawek</li></ul>
        <a class="btn" href="./#kontakt">Zacznij od darmowego</a>
      </div>
      <div class="plan featured">
        <span class="tag">Najczęściej wybierany</span>
        <div class="name">Pakiet Pro</div>
        <div class="price">799 zł<small>/ miesiąc</small></div>
        <p class="sub">Dwa filmy tygodniowo i publikacja na Twoich profilach.</p>
        <ul><li>8 rolek miesięcznie</li><li>publikacja na TikTok, Instagram i Facebook</li><li>opisy postów i hashtagi</li><li>lektor, napisy, muzyka</li><li>1 runda poprawek na film</li></ul>
        <a class="btn primary" href="./#kontakt">Wybieram Pro</a>
      </div>
      <div class="plan">
        <div class="name">Pakiet Start</div>
        <div class="price">449 zł<small>/ miesiąc</small></div>
        <p class="sub">Jeden nowy film tygodniowo. Ty publikujesz.</p>
        <ul><li>4 rolki miesięcznie</li><li>lektor, napisy, muzyka</li><li>materiał stockowy</li><li>1 runda poprawek na film</li><li>pliki gotowe do publikacji</li></ul>
        <a class="btn" href="./#kontakt">Wybieram Start</a>
      </div>
    </div>

    <div class="price-notes">
      <p>Pierwszy film zawsze gratis — niezależnie od pakietu.</p>
      <p>Montaż z Twoich własnych zdjęć lub nagrań: +100 zł za film. Prawdziwe wnętrze, efekty i produkty zwykle wyglądają bardziej wiarygodnie niż materiał stockowy.</p>
    </div>

    <div class="cennik-steps">
      <div><div class="n">01</div><b>Opisujesz firmę</b><p>Nazwa, oferta, dla kogo, co Cię wyróżnia, kontakt — kilka zdań w wiadomości.</p></div>
      <div><div class="n">02</div><b>W 48 h masz film</b><p>Scenariusz, lektor, napisy, muzyka. Jedna runda poprawek w cenie.</p></div>
      <div><div class="n">03</div><b>Publikacja</b><p>Ty — albo ja za Ciebie (Pro), razem z opisami i hashtagami.</p></div>
    </div>

    <p class="print-contact">Mateusz Lekem · Katowice · <a href="mailto:mateuszlekem@gmail.com">mateuszlekem@gmail.com</a> · tel. 797 224 220 · Instagram: <a href="https://www.instagram.com/matilemek/">instagram.com/matilemek</a> · portfolio i demo: <a href="{BASE}">siles69.github.io/kinowy-autopilot-feed/oferta/</a></p>

    <p class="fine">Ceny końcowe w PLN, bez VAT (działalność nierejestrowana — wystawiam rachunek). Rozliczenie miesięczne, rezygnacja w dowolnym momencie. Zasady współpracy: <a href="regulamin.html">regulamin</a> i <a href="polityka-prywatnosci.html">polityka prywatności</a>.</p>
    <p class="print-fine">Ceny końcowe w PLN (brutto, bez VAT — działalność nierejestrowana, wystawiam rachunek). Rozliczenie miesięczne, rezygnacja w dowolnym momencie, bez umowy na czas określony. Filmy powstają z użyciem narzędzi AI (lektor, montaż); materiał wideo pochodzi z licencjonowanych bibliotek lub od klienta. Nazwy firm w filmach demo są fikcyjne. Usługodawca: Mateusz Lekem, Katowice · mateuszlekem@gmail.com · 797 224 220. Regulamin i polityka prywatności: siles69.github.io/kinowy-autopilot-feed/oferta/</p>

    <div class="cta-row no-print"><a class="btn" href="./">← Wróć do oferty i filmów demo</a><a class="btn" href="cennik.pdf">Pobierz PDF</a></div>
  </div>
</main>"""
    (OUT / "cennik.html").write_text(shell(meta, ld, body), encoding="utf-8")
    print("cennik.html")


# ------------------------------------------------------------------ 404
def build_404():
    old = (OLD / "404.html").read_text(encoding="utf-8")
    meta, ld = head_meta(old)
    body = """<main id="main" class="notfound">
  <div class="wrap">
    <div class="grid">
      <div class="c7">
        <div class="code" aria-hidden="true">404</div>
        <h1 style="font-size:clamp(32px,5.5vw,56px);margin:16px 0 20px">Tej strony tu nie ma.</h1>
        <p class="lead">Adres jest nieprawidłowy albo strona została przeniesiona. Oferta rolek reklamowych dla firm z Katowic jest pod adresem poniżej.</p>
        <div class="cta-row">
          <a class="btn primary" href="/kinowy-autopilot-feed/oferta/">Przejdź do oferty</a>
          <a class="btn" href="/kinowy-autopilot-feed/oferta/cennik.html">Cennik</a>
        </div>
      </div>
    </div>
  </div>
</main>"""
    html = shell(meta, ld, body, css="/kinowy-autopilot-feed/oferta/style.css", nav_prefix="/kinowy-autopilot-feed/oferta/", body_class="notfound-page")
    (ROOT / "404.html").write_text(html, encoding="utf-8")
    print("404.html")


if __name__ == "__main__":
    build_index()
    build_doc("regulamin.html", "Regulamin")
    build_doc("polityka-prywatnosci.html", "Polityka prywatności")
    build_doc("dostepnosc.html", "Dostępność")
    build_cennik()
    build_404()

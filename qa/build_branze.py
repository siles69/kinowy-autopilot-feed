#!/usr/bin/env python3
"""
Strony branżowe (SEO): oferta/branze/<slug>.html + oferta/dla-agencji.html.
Używa tego samego szkieletu co qa/build_pages.py (nav, stopka, style.css).

    python3 qa/build_branze.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_pages import shell, BASE, OUT  # noqa: E402

DATE = "2026-10-07"

BRANZE = [
    {
        "slug": "stomatologia", "nazwa": "gabinetów stomatologicznych", "krotko": "Stomatologia",
        "title": "Rolki reklamowe dla gabinetów stomatologicznych — Katowice",
        "desc": "Rolki 9:16 dla gabinetów stomatologicznych z Katowic: lektor, napisy, treść informacyjna zgodna z zasadami reklamy podmiotów leczniczych. Pierwszy gratis.",
        "h1": "Rolki dla gabinetów stomatologicznych, które spokojnie tłumaczą, jak wygląda wizyta.",
        "lead": "Pacjent, który boi się dentysty, nie przeczyta cennika. Obejrzy 30 sekund o tym, jak wygląda pierwsza wizyta, znieczulenie czy higienizacja — i zapamięta nazwę gabinetu.",
        "demo": "dentysta",
        "tematy": [
            ("Jak wygląda pierwsza wizyta", "Rejestracja, przegląd, plan leczenia — krok po kroku, bez straszenia."),
            ("Znieczulenie bez stresu", "Czym jest znieczulenie komputerowe albo sedacja i dla kogo — jeśli je stosujecie."),
            ("Higienizacja w 30 sekund", "Co się dzieje na fotelu, ile trwa, jak często warto przychodzić."),
        ],
        "uwaga": "Reklama podmiotu leczniczego może mieć wyłącznie charakter informacyjny (art. 14 ustawy o działalności leczniczej) — dlatego w scenariuszach nie ma obietnic efektów, „promocji” na zabiegi ani zdjęć przed/po. Ostateczną decyzję o publikacji podejmuje gabinet.",
        "faq": [("Czy taki film jest zgodny z przepisami o reklamie usług medycznych?", "Scenariusz piszę informacyjnie: co robicie, jak wygląda wizyta, jak się umówić — bez zachęt do skorzystania ze świadczeń i bez obietnic efektów. Treść akceptuje gabinet przed publikacją."),
                ("Czy potrzebuję nagrań z gabinetu?", "Nie — standardowo pracuję na materiale stockowym. Ujęcia z Waszego gabinetu (bez wizerunku pacjentów) zwykle wyglądają bardziej wiarygodnie; montaż z nich to +100 zł za film.")],
    },
    {
        "slug": "medycyna-estetyczna", "nazwa": "gabinetów medycyny estetycznej", "krotko": "Medycyna estetyczna",
        "title": "Rolki reklamowe dla medycyny estetycznej — Katowice",
        "desc": "Rolki dla gabinetów medycyny estetycznej w Katowicach: zabieg wyjaśniony w 30 sekund, lektor, napisy, treść informacyjna. Pierwszy film gratis.",
        "h1": "Rolki dla medycyny estetycznej: zabieg wyjaśniony, zanim pacjentka zapyta.",
        "lead": "Większość pytań w DM-ach to te same pięć: czy boli, ile trwa, kiedy widać efekt, ile kosztuje, czy można od razu wrócić do pracy. Krótki film odpowiada na nie raz, a ogląda go każdy, kto trafi na profil.",
        "demo": None,
        "tematy": [
            ("Zabieg w 30 sekund", "Na czym polega, ile trwa, jak się przygotować — informacyjnie, bez obietnic efektu."),
            ("Kim jesteśmy", "Lekarz, kwalifikacje, gabinet — film, który buduje zaufanie przed pierwszą konsultacją."),
            ("Pytania z DM-ów", "Najczęstsze pytania pacjentek jako seria krótkich odpowiedzi."),
        ],
        "uwaga": "Jeśli gabinet jest podmiotem leczniczym, reklama może być wyłącznie informacyjna (art. 14 ustawy o działalności leczniczej). Scenariusze nie zawierają zdjęć przed/po, obietnic efektu ani promocji cenowych na zabiegi.",
        "faq": [("Czy pokazujecie efekty przed i po?", "Nie — w reklamie podmiotu leczniczego to ryzykowne. Pokazuję gabinet, proces i odpowiedzi na pytania; o publikacji decyduje gabinet."),
                ("Czy lektor może być kobiecy?", "Tak, do wyboru głos męski lub żeński.")],
    },
    {
        "slug": "salony-fryzjerskie-beauty", "nazwa": "salonów fryzjerskich i beauty", "krotko": "Fryzjerzy i beauty",
        "title": "Rolki reklamowe dla salonów fryzjerskich i beauty — Katowice",
        "desc": "Krótkie filmy dla salonów fryzjerskich, kosmetycznych i barberów z Katowic: metamorfozy, nowe usługi, wolne terminy. Lektor i napisy, pierwszy film gratis.",
        "h1": "Rolki dla salonów, które mają co pokazać — a nie mają czasu montować.",
        "lead": "Metamorfoza koloru, nowa stylistka, wolne terminy w czwartek — to najwdzięczniejszy materiał na rolki. Ty robisz zdjęcia i krótkie nagrania telefonem, ja składam z nich film z lektorem i napisami.",
        "demo": "fryzjer",
        "tematy": [
            ("Metamorfoza tygodnia", "Przed i po z Twoich zdjęć, z opisem techniki i ceną od."),
            ("Wolne terminy", "Szybka rolka „mamy jeszcze miejsca w czwartek” — publikowana w dniu, w którym jest luka."),
            ("Poznaj zespół", "Kto, w czym się specjalizuje, jak się umówić."),
        ],
        "uwaga": "Zdjęcia klientek publikujemy tylko za ich zgodą — o zgodę prosi salon.",
        "faq": [("Czy mogę wysłać zdjęcia z telefonu?", "Tak — montaż z Twoich zdjęć i nagrań to +100 zł za film; zwykle to najlepiej działający materiał w beauty."),
                ("Jak często publikować?", "Raz–dwa razy w tygodniu wystarczy, żeby profil żył — stąd pakiety 4 i 8 filmów.")],
    },
    {
        "slug": "silownie-trenerzy", "nazwa": "siłowni i trenerów personalnych", "krotko": "Siłownie i trenerzy",
        "title": "Rolki reklamowe dla siłowni i trenerów — Katowice",
        "desc": "Rolki dla siłowni, boxów crossfit, studiów EMS i trenerów z Katowic: pierwszy trening, karnet, nabór. Lektor, napisy, pierwszy film gratis.",
        "h1": "Rolki dla siłowni i trenerów: pierwszy trening pokazany, zanim ktoś się zapisze.",
        "lead": "Najtrudniejsze jest przyjść pierwszy raz. Film, który w 30 sekund pokazuje, jak wygląda pierwszy trening, kto prowadzi i ile to kosztuje, robi więcej niż kolejna grafika z promocją na karnet.",
        "demo": "silownia",
        "tematy": [
            ("Pierwszy trening", "Jak wygląda, co zabrać, kto Cię przywita."),
            ("Nabór / nowy grafik", "Rolka pod konkretny termin — zajęcia, wyzwanie, nowa grupa."),
            ("Trener w 30 sekund", "Kim jestem, z kim pracuję, jak się umówić na konsultację."),
        ],
        "uwaga": "Nie obiecujemy w filmach konkretnych efektów sylwetkowych ani zdrowotnych.",
        "faq": [("Czy nagracie zajęcia u nas?", "Nie nagrywam na miejscu — montuję z Twoich nagrań z telefonu (+100 zł) albo ze stocku."),
                ("Czy to działa dla jednego trenera?", "Tak — pakiet Start (4 filmy) zwykle wystarcza na regularny profil trenera.")],
    },
    {
        "slug": "nieruchomosci", "nazwa": "agentów nieruchomości", "krotko": "Nieruchomości",
        "title": "Filmy do ogłoszeń nieruchomości dla agentów — Katowice",
        "desc": "Film do każdego ogłoszenia: mieszkanie w 30 sekund ze zdjęć z oferty, lektor, napisy, cena i kontakt. Dla agentów z Katowic. Pierwszy gratis.",
        "h1": "Film do każdego ogłoszenia — ze zdjęć, które już masz.",
        "lead": "Wysyłasz link do oferty, ja robię z jej zdjęć 30-sekundową rolkę: metraż, układ, najważniejsze atuty, cena i Twój telefon. Gotowe na Instagram, Facebook, TikTok i do wysłania klientowi.",
        "demo": "nieruchomosci",
        "tematy": [
            ("Mieszkanie w 30 sekund", "Ze zdjęć z ogłoszenia: metraż, pokoje, piętro, okolica, cena."),
            ("Agent w 30 sekund", "Kim jesteś, w jakich dzielnicach działasz, ile transakcji — film wizerunkowy."),
            ("Dzielnica", "Krótki przewodnik po okolicy: szkoły, komunikacja, zieleń — przyciąga kupujących z innych miast."),
        ],
        "uwaga": "Dane w filmie (metraż, cena) pochodzą z ogłoszenia — sprawdza je agent przed publikacją.",
        "faq": [("Ile kosztuje film do jednej oferty?", "149 zł za pojedynczy film albo w pakiecie: 4 filmy za 449 zł, 8 filmów z publikacją za 799 zł. Montaż ze zdjęć z ogłoszenia to standard w tej branży — dopłata +100 zł nie dotyczy zdjęć z oferty."),
                ("Jak szybko?", "48 godzin od wysłania linku do ogłoszenia.")],
    },
    {
        "slug": "detailing-warsztaty", "nazwa": "detailingu i warsztatów", "krotko": "Detailing i warsztaty",
        "title": "Rolki reklamowe dla detailingu i warsztatów — Katowice",
        "desc": "Rolki dla detailingu, oklejania i warsztatów z Katowic: lakier przed i po, powłoki, cena. Montaż z Twoich nagrań, lektor, napisy. Pierwszy gratis.",
        "h1": "Detailing sprzedaje się obrazem. Ja zrobię z niego film, który ktoś obejrzy do końca.",
        "lead": "Masz w telefonie dziesiątki nagrań lakieru przed i po. Brakuje im tylko lektora, który powie, co widać, ile to kosztuje i jak się umówić. To robię ja.",
        "demo": "detailing",
        "tematy": [
            ("Przed i po", "Z Twoich nagrań: co było, co zrobione, jakim produktem, cena od."),
            ("Co to jest powłoka ceramiczna / PPF", "Edukacyjna rolka, która odpowiada na pytania, zanim klient zadzwoni."),
            ("Pakiet sezonowy", "Rolka pod konkretną usługę na jesień i zimę."),
        ],
        "uwaga": "Tablice rejestracyjne klientów zamazujemy w montażu.",
        "faq": [("Czy montujecie z moich nagrań?", "Tak — w detailingu to najlepiej działający materiał (+100 zł za film)."),
                ("Czy dodacie cenę na ekranie?", "Tak, jeśli ją podasz — cena „od” na końcu filmu.")],
    },
    {
        "slug": "gastronomia", "nazwa": "restauracji, pizzerii i kawiarni", "krotko": "Gastronomia",
        "title": "Rolki reklamowe dla restauracji i kawiarni — Katowice",
        "desc": "Rolki dla restauracji, pizzerii i kawiarni z Katowic: danie dnia, nowe menu, dowóz. Lektor, napisy, montaż z Twoich ujęć lub stocku. Pierwszy gratis.",
        "h1": "Rolki dla gastronomii: nowe menu pokazane tak, że chce się zamówić.",
        "lead": "Zdjęcie dania przewija się w sekundę. Dwadzieścia sekund z pieca, z lektorem, który mówi, co to jest i do której dowozicie, zostaje w głowie do kolacji.",
        "demo": "pizzeria",
        "tematy": [
            ("Nowe menu / danie sezonu", "Z Twoich ujęć z kuchni albo ze stocku, z ceną i godzinami."),
            ("Lunch dnia", "Krótka, powtarzalna rolka na każdy tydzień."),
            ("Dowóz i odbiór", "Gdzie zamówić, jak szybko, jaki zasięg dowozu."),
        ],
        "uwaga": "Nie robię reklam napojów alkoholowych (ograniczenia ustawy o wychowaniu w trzeźwości) — film może pokazać lokal i jedzenie.",
        "faq": [("Czy wystarczą nagrania z telefonu?", "Tak — 4–6 ujęć po 3–5 sekund z kuchni wystarczy na jeden film (+100 zł za montaż z materiałów)."),
                ("Czy możecie publikować za nas?", "Tak, w pakiecie Pro — 8 filmów miesięcznie z publikacją, opisami i hashtagami.")],
    },
    {
        "slug": "szkoly-jazdy", "nazwa": "szkół jazdy", "krotko": "Szkoły jazdy",
        "title": "Rolki reklamowe dla szkół jazdy — Katowice",
        "desc": "Filmy 9:16 dla ośrodków szkolenia kierowców z Katowic: nowy kurs, jak wygląda egzamin, plac manewrowy. Lektor, napisy, tam gdzie są kursanci — na TikToku.",
        "h1": "Rolki dla szkół jazdy — tam, gdzie są przyszli kursanci.",
        "lead": "Osoby, które za pół roku zapiszą się na kurs, są dziś na TikToku i Instagramie. Krótki film o tym, jak wygląda pierwsza jazda albo egzamin na placu, trafia do nich lepiej niż ulotka w szkole.",
        "demo": None,
        "tematy": [
            ("Nowy kurs od…", "Termin, cena, co w pakiecie — rolka pod każdy nabór."),
            ("Jak wygląda egzamin", "Plac, miasto, najczęstsze błędy — edukacyjnie."),
            ("Instruktor w 30 sekund", "Kto uczy, jakim autem, gdzie startujecie."),
        ],
        "uwaga": "Nie obiecujemy zdawalności ani wyników egzaminu.",
        "faq": [("Czy filmy są dla młodszych odbiorców?", "Tak — dobieram tempo, muzykę i napisy pod TikTok i Reels."),
                ("Czy mogę zamówić jeden film pod nabór?", "Tak, 149 zł za pojedynczy film; pierwszy gratis.")],
    },
    {
        "slug": "fotowoltaika-pompy-ciepla", "nazwa": "firm fotowoltaicznych i pomp ciepła", "krotko": "Fotowoltaika i OZE",
        "title": "Rolki reklamowe dla fotowoltaiki i pomp ciepła — Śląsk",
        "desc": "Rolki dla instalatorów fotowoltaiki i pomp ciepła ze Śląska: realizacja, dotacje, przebieg montażu. Lektor, napisy, montaż z Twoich zdjęć.",
        "h1": "Rolki dla OZE: realizacja i dotacja wyjaśnione w 30 sekund.",
        "lead": "Klient na fotowoltaikę albo pompę ciepła ma dużo pytań i mało zaufania. Film z prawdziwej realizacji pod Katowicami i jasne wyjaśnienie, jak wygląda montaż i dofinansowanie, robi więcej niż kolejna obietnica oszczędności.",
        "demo": None,
        "tematy": [
            ("Realizacja tygodnia", "Z Twoich zdjęć z montażu: gdzie, jaka moc, ile trwało."),
            ("Jak wygląda montaż", "Od audytu do odbioru — krok po kroku."),
            ("Dofinansowanie", "Jaki program, dla kogo, jakie dokumenty — informacyjnie, z odesłaniem do źródła."),
        ],
        "uwaga": "W filmach nie podajemy gwarantowanych oszczędności ani zwrotu inwestycji — tylko fakty z realizacji i aktualne zasady programów.",
        "faq": [("Czy możecie użyć zdjęć z realizacji?", "Tak, montaż z Twoich zdjęć i nagrań (+100 zł za film)."),
                ("Czy treść o dotacjach będzie aktualna?", "Opieram się na tym, co przekażesz i na oficjalnych stronach programów; datę i źródło weryfikujesz przed publikacją.")],
    },
    {
        "slug": "biura-rachunkowe-kancelarie", "nazwa": "biur rachunkowych i kancelarii", "krotko": "Biura rachunkowe",
        "title": "Rolki dla biur rachunkowych i kancelarii — Katowice",
        "desc": "Rolki edukacyjne dla biur rachunkowych i kancelarii z Katowic: zmiana w przepisach w 30 sekund, lektor, napisy. Pierwszy film gratis.",
        "h1": "Rolki dla biur rachunkowych: jedna zmiana w przepisach, 30 sekund, Twoje logo.",
        "lead": "Przedsiębiorcy szukają księgowej, której ufają. Seria krótkich filmów „co zmienia się od stycznia” albo „jak założyć JDG” pokazuje kompetencje lepiej niż strona z cennikiem.",
        "demo": None,
        "tematy": [
            ("Zmiana w przepisach", "Jedna zmiana, kogo dotyczy, co zrobić — z datą i źródłem."),
            ("Pytanie od klienta", "Najczęstsze pytania przedsiębiorców w 30 sekund."),
            ("Kim jesteśmy", "Zespół, specjalizacja, jak wygląda współpraca."),
        ],
        "uwaga": "Treści merytoryczne (podatki, prawo) pisze lub zatwierdza biuro — ja odpowiadam za formę, nie za poradę.",
        "faq": [("Kto odpowiada za treść merytoryczną?", "Biuro: przysyłasz 3–4 zdania albo akceptujesz mój szkic; ja nie udzielam porad podatkowych."),
                ("Jak często publikować?", "Raz w tygodniu wystarczy — pakiet Start, 4 filmy miesięcznie.")],
    },
]

FAQ_WSPOLNE = [
    ("Ile kosztuje?", "Pierwszy film dla nowej firmy jest gratis. Potem: pojedynczy film 149 zł, pakiet Start (4 filmy/mies.) 449 zł, pakiet Pro (8 filmów/mies. z publikacją, opisami i hashtagami) 799 zł. Ceny końcowe, rachunek, bez umowy na rok."),
    ("Ile trwa?", "Pierwszy film w 48 godzin od otrzymania opisu. Jedna runda poprawek w cenie."),
]


def plan_cards(prefix=""):
    return f"""    <div class="plans">
      <div class="plan">
        <div class="name">Pojedynczy film</div>
        <div class="price">149 zł<small>/ film</small></div>
        <p class="sub">Pierwszy dla nowej firmy jest gratis — 149 zł płacisz dopiero za kolejny.</p>
        <a class="btn" href="{prefix}./#kontakt">Zacznij od darmowego</a>
      </div>
      <div class="plan featured">
        <span class="tag">Najczęściej wybierany</span>
        <div class="name">Pakiet Pro</div>
        <div class="price">799 zł<small>/ miesiąc</small></div>
        <p class="sub">8 filmów miesięcznie z publikacją, opisami i hashtagami.</p>
        <a class="btn primary" href="{prefix}./#kontakt">Wybieram Pro</a>
      </div>
      <div class="plan">
        <div class="name">Pakiet Start</div>
        <div class="price">449 zł<small>/ miesiąc</small></div>
        <p class="sub">4 filmy miesięcznie, publikujesz sam.</p>
        <a class="btn" href="{prefix}./#kontakt">Wybieram Start</a>
      </div>
    </div>"""


def meta_lines(title, desc, url):
    assert len(title) <= 60, (title, len(title))
    assert len(desc) <= 155, (desc, len(desc))
    img = BASE + "og.png"
    return [
        '<meta charset="UTF-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{title}</title>", f'<meta name="description" content="{desc}">',
        '<meta name="author" content="Mateusz">', '<meta name="robots" content="index, follow">',
        '<meta name="theme-color" content="#0B0B0E">', f'<link rel="canonical" href="{url}">',
        '<link rel="icon" href="../favicon.svg" type="image/svg+xml">', '<link rel="icon" href="../favicon.ico" sizes="32x32">',
        '<link rel="apple-touch-icon" href="../apple-touch-icon.png">', '<link rel="manifest" href="../site.webmanifest">',
        '<meta property="og:type" content="website">', '<meta property="og:site_name" content="Rolki reklamowe dla firm — Katowice">',
        f'<meta property="og:title" content="{title}">', f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{url}">', f'<meta property="og:image" content="{img}">',
        '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
        '<meta property="og:locale" content="pl_PL">', '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">', f'<meta name="twitter:description" content="{desc}">',
        f'<meta name="twitter:image" content="{img}">',
    ]


def build_branza(b):
    url = f"{BASE}branze/{b['slug']}.html"
    faq = b["faq"] + FAQ_WSPOLNE
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Oferta", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Branże", "item": BASE + "branze/"},
            {"@type": "ListItem", "position": 3, "name": b["krotko"], "item": url}]},
        {"@type": "Service", "@id": url + "#usluga", "name": f"Rolki reklamowe dla {b['nazwa']}",
         "serviceType": "Produkcja krótkich filmów reklamowych 9:16", "provider": {"@id": BASE + "#business"},
         "areaServed": [{"@type": "City", "name": "Katowice"}, {"@type": "AdministrativeArea", "name": "Górny Śląsk"}],
         "offers": {"@type": "Offer", "price": "149", "priceCurrency": "PLN", "url": BASE + "cennik.html"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    demo = ""
    if b["demo"]:
        d = b["demo"]
        demo = f"""
    <div class="two" style="margin-top:56px;align-items:center">
      <div>
        <article class="demo" style="max-width:300px">
          <div class="frame">
            <img class="poster" src="../../demo/poster-{d}.jpg" alt="" width="405" height="720" loading="lazy" decoding="async">
            <video src="../../demo/demo-{d}.mp4" data-poster="../../demo/poster-{d}.jpg" preload="none" playsinline controls aria-label="Film demo — przykładowa firma, branża: {b['krotko'].lower()}"></video>
          </div>
          <div class="cap"><small>Przykładowa firma (fikcyjna) · materiał stockowy, lektor AI</small></div>
        </article>
      </div>
      <div><h3>Tak wygląda format.</h3><p class="muted">To film demo dla wymyślonej firmy z tej branży. Twój będzie z Twoją nazwą, ofertą i kontaktem. Pozostałe przykłady: <a href="../#demo">sześć branż na stronie głównej</a>.</p></div>
    </div>"""
    tematy = "\n".join(f'<li class="step"><div class="n">0{i}</div><h3>{t}</h3><p>{o}</p></li>' for i, (t, o) in enumerate(b["tematy"], 1))
    faqh = "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)
    body = f"""<main id="main" class="page">
  <div class="wrap">
    <nav class="crumbs" aria-label="Okruszki"><a href="../">Oferta</a><span class="sep" aria-hidden="true">›</span><a href="./">Branże</a><span class="sep" aria-hidden="true">›</span><span aria-current="page">{b['krotko']}</span></nav>
    <p class="eyebrow">Rolki reklamowe Katowice · {b['krotko']}</p>
    <h1 style="max-width:18ch">{b['h1']}</h1>
    <p class="lead" style="margin-top:24px">{b['lead']}</p>
    <div class="cta-row"><a class="btn primary" href="../#kontakt">Zrób mi darmowy film</a><a class="btn" href="../cennik.html">Cennik</a></div>
{demo}
    <section style="padding:96px 0 0;border:0">
      <h2 style="margin-bottom:40px">Trzy pomysły na pierwsze filmy.</h2>
      <ol class="steps" style="list-style:none;margin:0;padding-left:0">
{tematy}
      </ol>
      <p class="muted small" style="margin-top:32px;max-width:62ch">{b['uwaga']}</p>
    </section>
    <section style="padding:96px 0 0;border:0">
      <h2 style="margin-bottom:40px">Ceny — takie same dla każdej branży.</h2>
{plan_cards('../')}
    </section>
    <section style="padding:96px 0 0;border:0">
      <h2 style="margin-bottom:24px">Pytania.</h2>
      <div class="faq">
{faqh}
      </div>
    </section>
    <section style="padding:96px 0 0;border:0">
      <h2 style="max-width:16ch">Napisz trzy zdania o swojej ofercie — film masz za 48 h.</h2>
      <div class="cta-row"><a class="btn primary" href="../#kontakt">Kontakt</a><a class="btn" href="mailto:mateuszlekem@gmail.com?subject=Darmowy%20film%20%E2%80%94%20{b['slug']}">mateuszlekem@gmail.com</a></div>
      <p class="consent">Wysyłając wiadomość, zgadzasz się na kontakt w sprawie oferty. Szczegóły w <a href="../polityka-prywatnosci.html">polityce prywatności</a>.</p>
    </section>
  </div>
</main>
<script>document.querySelectorAll('.demo video').forEach(function(v){{v.addEventListener('play',function(){{var p=v.parentNode.querySelector('.poster');if(p)p.style.display='none';}});}});</script>"""
    html = shell(meta_lines(b["title"], b["desc"], url), ld, body, css="../style.css", nav_prefix="../")
    (OUT / "branze").mkdir(exist_ok=True)
    (OUT / "branze" / f"{b['slug']}.html").write_text(html, encoding="utf-8")
    return url


def build_index_branz():
    url = BASE + "branze/"
    title, desc = "Rolki reklamowe dla firm w Katowicach — branże", "Krótkie filmy reklamowe 9:16 dla stomatologii, beauty, siłowni, nieruchomości, detailingu, gastronomii, szkół jazdy, OZE i biur rachunkowych w Katowicach."
    items = "\n".join(f'<li><a href="{b["slug"]}.html"><span class="serif" style="font-size:26px">{b["krotko"]}</span><br><span class="muted small">{b["lead"][:110].rsplit(" ",1)[0]}…</span></a></li>' for b in BRANZE)
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Oferta", "item": BASE}, {"@type": "ListItem", "position": 2, "name": "Branże", "item": url}]},
        {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": f"{url}{b['slug']}.html", "name": b["krotko"]} for i, b in enumerate(BRANZE, 1)]}]}
    body = f"""<main id="main" class="page">
  <div class="wrap">
    <nav class="crumbs" aria-label="Okruszki"><a href="../">Oferta</a><span class="sep" aria-hidden="true">›</span><span aria-current="page">Branże</span></nav>
    <h1 style="max-width:16ch">Rolki reklamowe dla Twojej branży.</h1>
    <p class="lead" style="margin-top:24px">Ten sam format i te same ceny — inne tematy, inne zasady. Wybierz swoją branżę: znajdziesz pomysły na pierwsze filmy i to, na co uważam przy treści.</p>
    <ul class="plain branze-lista" style="margin-top:48px">
{items}
      <li><a href="../dla-agencji.html"><span class="serif" style="font-size:26px">Agencje i social media managerowie</span><br><span class="muted small">Filmy white-label w hurcie — 99 zł za film, bez mojej marki.</span></a></li>
    </ul>
  </div>
</main>"""
    html = shell(meta_lines(title, desc, url), ld, body, css="../style.css", nav_prefix="../")
    (OUT / "branze" / "index.html").write_text(html, encoding="utf-8")
    return url


def build_agencje():
    url = BASE + "dla-agencji.html"
    title = "Rolki white-label dla agencji social media — 99 zł/film"
    desc = "Rolki 9:16 z lektorem i napisami dla agencji i social media managerów: bez mojej marki, prawo do odsprzedaży, 48 h, od 99 zł za film."
    faq = [("Czy mogę sprzedawać filmy jako swoje?", "Tak — film nie ma mojej marki, a licencja obejmuje przekazanie go Twojemu klientowi."),
           ("Jaki jest minimalny wolumen?", "Brak minimum. Stawka 99 zł obowiązuje od 5 filmów w miesiącu; pojedyncze filmy po 129 zł."),
           ("Jak przekazujecie brief?", "Arkusz albo e-mail: firma, oferta, 3–4 zdania, dane do ekranu końcowego, styl. Odsyłam MP4 w 48 h."),
           ("Kto odpowiada za treść?", "Ty i Twój klient akceptujecie scenariusz przed produkcją; ja pilnuję formy i zgodności z briefem.")]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Oferta", "item": BASE}, {"@type": "ListItem", "position": 2, "name": "Dla agencji", "item": url}]},
        {"@type": "Service", "name": "Rolki white-label dla agencji", "serviceType": "Produkcja krótkich filmów 9:16 w modelu white-label", "provider": {"@id": BASE + "#business"},
         "areaServed": {"@type": "Country", "name": "Polska"},
         "offers": [{"@type": "Offer", "name": "Film white-label (od 5/mies.)", "price": "99", "priceCurrency": "PLN"}, {"@type": "Offer", "name": "Film white-label pojedynczy", "price": "129", "priceCurrency": "PLN"}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    faqh = "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)
    body = f"""<main id="main" class="page">
  <div class="wrap">
    <nav class="crumbs" aria-label="Okruszki"><a href="./">Oferta</a><span class="sep" aria-hidden="true">›</span><span aria-current="page">Dla agencji</span></nav>
    <p class="eyebrow">White-label · dla agencji i social media managerów</p>
    <h1 style="max-width:17ch">Twoi klienci chcą rolek. Ty nie masz czasu ich montować.</h1>
    <p class="lead" style="margin-top:24px">Wysyłasz brief, ja w 48 godzin oddaję pionowy film 20–35 s z polskim lektorem, napisami i muzyką — bez mojej marki, gotowy do wysłania klientowi pod Twoim szyldem.</p>
    <div class="cta-row"><a class="btn primary" href="mailto:mateuszlekem@gmail.com?subject=White-label%20%E2%80%94%20brief">Wyślij brief</a><a class="btn" href="./#demo">Zobacz przykłady</a></div>
    <section style="padding:96px 0 0;border:0">
      <h2 style="margin-bottom:40px">Hurt, nie abonament.</h2>
      <div class="plans">
        <div class="plan"><div class="name">Pojedynczy film</div><div class="price">129 zł<small>/ film</small></div><p class="sub">Bez minimum, bez umowy.</p><a class="btn" href="mailto:mateuszlekem@gmail.com?subject=White-label%20%E2%80%94%20pojedynczy%20film">Zamów</a></div>
        <div class="plan featured"><span class="tag">Dla stałych partnerów</span><div class="name">Od 5 filmów / mies.</div><div class="price">99 zł<small>/ film</small></div><p class="sub">Rozliczenie raz w miesiącu za faktycznie oddane filmy.</p><a class="btn primary" href="mailto:mateuszlekem@gmail.com?subject=White-label%20%E2%80%94%20sta%C5%82a%20wsp%C3%B3%C5%82praca">Porozmawiajmy</a></div>
        <div class="plan"><div class="name">Montaż z materiałów klienta</div><div class="price">+50 zł<small>/ film</small></div><p class="sub">Gdy dosyłasz zdjęcia i nagrania od klienta.</p><a class="btn" href="mailto:mateuszlekem@gmail.com?subject=White-label%20%E2%80%94%20monta%C5%BC">Zapytaj</a></div>
      </div>
      <p class="muted small" style="margin-top:24px">Ceny końcowe w PLN, rachunek. Pierwszy film testowy dla agencji — gratis, na briefie Twojego prawdziwego klienta.</p>
    </section>
    <section style="padding:96px 0 0;border:0">
      <h2 style="margin-bottom:24px">Pytania.</h2>
      <div class="faq">
{faqh}
      </div>
    </section>
  </div>
</main>"""
    html = shell(meta_lines(title, desc, url), ld, body)
    html = html.replace('href="../favicon', 'href="favicon').replace('href="../apple-touch', 'href="apple-touch').replace('href="../site.webmanifest', 'href="site.webmanifest')
    (OUT / "dla-agencji.html").write_text(html, encoding="utf-8")
    return url


if __name__ == "__main__":
    urls = [build_branza(b) for b in BRANZE] + [build_index_branz(), build_agencje()]
    for u in urls:
        print(u)

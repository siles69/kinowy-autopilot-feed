// Zrzuty ekranu każdej strony w 3 rozmiarach. Użycie: node qa/shoot.js <katalog_wyjściowy> [baseUrl]
// Wymaga lokalnego serwera: (cd /ścieżka/nad/repo && python3 -m http.server 8765)
const path = require('path');
const { chromium } = require(process.env.PW_PATH || 'playwright');
const out = process.argv[2] || 'qa/round-1';
const base = process.argv[3] || 'http://127.0.0.1:8765/kinowy-autopilot-feed/';
const pages = ['oferta/', 'oferta/cennik.html', 'oferta/regulamin.html', 'oferta/polityka-prywatnosci.html', 'oferta/dostepnosc.html', '404.html'];
const sizes = [[390, 844], [768, 1024], [1440, 900]];
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined });
  const fs = require('fs'); fs.mkdirSync(out, { recursive: true });
  for (const pg of pages) for (const [w, h] of sizes) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await p.goto(base + pg, { waitUntil: 'networkidle' });
    await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
    await p.evaluate(() => new Promise(r => { window.scrollTo(0, document.body.scrollHeight); setTimeout(() => { window.scrollTo(0, 0); setTimeout(r, 600); }, 600); }));
    // sekcje .reveal odsłania IntersectionObserver; przed zrzutem całej strony odsłoń wszystkie (tak jak zrobi to bezpiecznik po 1,5 s)
    await p.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('in')));
    await p.waitForTimeout(500);
    const name = (pg.replace(/[\/.]+/g, '_').replace(/^_|_$/g, '') || 'index') + `-${w}`;
    await p.screenshot({ path: path.join(out, name + '.png'), fullPage: true });
    await p.screenshot({ path: path.join(out, name + '-fold.png'), fullPage: false });
    await p.close();
  }
  await b.close();
  console.log('zrzuty w', out);
})();

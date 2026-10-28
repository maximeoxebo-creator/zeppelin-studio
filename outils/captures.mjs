// Captures des sections d'Opaline pour la documentation.
// A lancer depuis le depot du theme (playwright y est installe), serveur
// de developpement `shopify theme dev` actif sur le port 9393 :
//   node --input-type=module - <cibles.json> <dossier> [types...] < captures.mjs
import { chromium } from 'playwright';
import fs from 'fs';
const [cheminCibles, sortie, ...filtre] = process.argv.slice(2);
const cibles = JSON.parse(fs.readFileSync(cheminCibles, 'utf8'));
const B = 'http://127.0.0.1:9393';
const browser = await chromium.launch({ executablePath: '/Users/maxime/Library/Caches/ms-playwright/chromium-1234/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing' });
const formats = [
  { nom: 'desktop', viewport: { width: 1440, height: 900 }, dpr: 1, max: 1700 },
  { nom: 'mobile', viewport: { width: 390, height: 844 }, dpr: 2, max: 1500 },
];
for (const f of formats) {
  const ctx = await browser.newContext({ viewport: f.viewport, deviceScaleFactor: f.dpr, reducedMotion: 'reduce', isMobile: f.nom === 'mobile', hasTouch: f.nom === 'mobile' });
  // Les sections qui se construisent au defilement (parallaxe, piste
  // horizontale, image epinglee) se photographient animations actives, a
  // l'ecran, au moment ou elles sont en place.
  const ctxScene = await browser.newContext({ viewport: f.viewport, deviceScaleFactor: f.dpr, isMobile: f.nom === 'mobile', hasTouch: f.nom === 'mobile' });
  for (const [type, c] of Object.entries(cibles)) {
    if (filtre.length && !filtre.includes(type)) continue;
    if (c.scene !== undefined) {
      const p = await ctxScene.newPage();
      await p.addInitScript(() => { new MutationObserver(() => document.querySelectorAll('[data-lf-popup]').forEach(e => e.remove())).observe(document, { childList: true, subtree: true }); });
      try {
        await p.goto(B + c.url, { waitUntil: 'load', timeout: 45000 }); await p.waitForTimeout(1200);
        await p.addStyleTag({ content: '#lf-back-to-top{display:none!important}' });
        const vh = f.viewport.height;
        const box = await p.evaluate(k => { const e = document.querySelector(`.shopify-section[id$="__${k}"]`); const r = e.getBoundingClientRect(); return { top: r.top + scrollY, h: r.height }; }, c.cle);
        const cible = box.top + c.scene * Math.max(0, box.h - vh) - (box.h <= vh ? (vh - box.h) / 2 : 0);
        for (let y = Math.max(0, cible - 1600); y <= cible; y += 200) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(60); }
        await p.evaluate(v => scrollTo(0, v), cible); await p.waitForTimeout(1800);
        await p.screenshot({ path: `${sortie}/${type}-${f.nom}.png` });
        console.log('ok', type, f.nom, 'scene');
      } catch (e) { console.log('ERR', type, f.nom, e.message.split('\n')[0]); }
      await p.close();
      continue;
    }
    const p = await ctx.newPage();
    if (type !== 'lf-popup') await p.addInitScript(() => { new MutationObserver(() => document.querySelectorAll('[data-lf-popup]').forEach(e => e.remove())).observe(document, { childList: true, subtree: true }); });
    if (type === 'lf-popup') await p.addInitScript(() => { try { document.cookie.split(';').forEach(c => { if (c.trim().startsWith('lf_popup')) document.cookie = c.split('=')[0] + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'; }); } catch (e) {} });
    try {
      if (c.panier) {
        // Un panier vide ne montre rien de la section : deux articles d'abord.
        await p.goto(B + '/', { waitUntil: 'domcontentloaded' });
        await p.evaluate(async () => { for (const h of ['alma22', 'asilah']) { const v = (await (await fetch('/products/' + h + '.js')).json()).variants[0].id; await fetch('/cart/add.js', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: v, quantity: 1 }) }); } });
      }
      await p.goto(B + c.url, { waitUntil: 'load', timeout: 45000 });
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
      await p.waitForTimeout(1200);
      let el;
      // L'en-tete fixe et le bouton de retour en haut se poseraient sur
      // chaque section : on les retire, sauf pour photographier l'en-tete
      // et pour les fenetres, montrees sur la page entiere.
      if (!['header', 'lf-announcement'].includes(type) && !c.modal) {
        await p.addStyleTag({ content: '.shopify-section-group-header-group, .lf-hdr, #lf-back-to-top, .lf-floating-cart, .lf-fcart { display: none !important; }' });
        await p.waitForTimeout(300);
      }
      if (type === 'header' || type === 'lf-announcement') {
        await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(600);
        const h = await p.evaluate(() => { const e = document.querySelector('.lf-hdr'); return e ? Math.ceil(e.getBoundingClientRect().bottom) + 8 : 140; });
        await p.screenshot({ path: `${sortie}/${type}-${f.nom}.png`, clip: { x: 0, y: 0, width: f.viewport.width, height: Math.max(h, 80) } });
        console.log('ok', type, f.nom); await p.close(); continue;
      }
      if (c.modal) {
        await p.waitForTimeout(type === 'lf-popup' ? 6000 : 1500);
        el = null; // ecran entier pour une fenetre
        await p.screenshot({ path: `${sortie}/${type}-${f.nom}.png` });
      } else {
        el = p.locator(`.shopify-section[id$="__${c.cle}"]`).first();
        if (!(await el.count())) { console.log('ABSENT', type, f.nom); await p.close(); continue; }
        await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(900);
        if (c.survol && f.nom === 'desktop') { await p.locator(c.survol).first().hover(); await p.waitForTimeout(900); }
        const b = await el.boundingBox();
        if (!b || b.height < 10) { console.log('VIDE', type, f.nom); await p.close(); continue; }
        const scrollY = await p.evaluate(() => scrollY);
        // Marge propre a certaines sections : leur contenu deborde du cadre
        // (parallaxe du collage, bandeau tres bas). Sinon la capture vise
        // l'element lui-meme : une mesure prise avant coup se decalait des
        // que des images chargees au defilement poussaient la page. Une
        // section trop haute est rognee a la conversion.
        const m = c.marge || 0;
        if (m && b.height + 2 * m <= f.viewport.height) {
          // Section basse : centree a l'ecran et photographiee la, sans
          // passer par la page entiere dont la mesure se decalait.
          await p.evaluate(dy => scrollBy(0, dy), b.y + b.height / 2 - f.viewport.height / 2); await p.waitForTimeout(700);
          const b2 = await el.boundingBox();
          await p.screenshot({ path: `${sortie}/${type}-${f.nom}.png`, clip: { x: 0, y: Math.max(0, b2.y - m), width: f.viewport.width, height: b2.height + 2 * m } });
        } else if (m) {
          const h = Math.min(b.height + 2 * m, f.max);
          await p.screenshot({ path: `${sortie}/${type}-${f.nom}.png`, fullPage: true, clip: { x: 0, y: Math.max(0, b.y + scrollY - m), width: f.viewport.width, height: h } });
        } else {
          await p.waitForTimeout(600);
          await el.screenshot({ path: `${sortie}/${type}-${f.nom}.png` });
        }
      }
      console.log('ok', type, f.nom);
    } catch (e) { console.log('ERR', type, f.nom, e.message.split('\n')[0]); }
    await p.close();
  }
  await ctx.close();
  await ctxScene.close();
}
await browser.close();

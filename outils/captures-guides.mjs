// Captures des guides : apercu rapide, galerie produit, pastilles, mega menu.
//   node --input-type=module - <dossier> < captures-guides.mjs   (depuis le depot du theme)
import { chromium } from 'playwright';
const sortie = process.argv[2];
const B = 'http://127.0.0.1:9393';
const browser = await chromium.launch({ executablePath: '/Users/maxime/Library/Caches/ms-playwright/chromium-1234/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing' });
const page = async (vp, mobile) => {
  const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: mobile ? 2 : 1, isMobile: !!mobile, hasTouch: !!mobile });
  const p = await ctx.newPage();
  await p.addInitScript(() => { new MutationObserver(() => document.querySelectorAll('[data-lf-popup]').forEach(e => e.remove())).observe(document, { childList: true, subtree: true }); });
  return p;
};
const D = { width: 1440, height: 900 }, M = { width: 390, height: 844 };
const ok = n => console.log('ok', n);

// Carte au survol
{ const p = await page(D);
  await p.goto(B + '/collections/all', { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const c = p.locator('.lf-card').nth(1); await c.scrollIntoViewIfNeeded(); await c.hover(); await p.waitForTimeout(500);
  await c.locator('.lf-card__act').nth(1).hover(); await p.waitForTimeout(700);
  const b = await c.boundingBox();
  await p.screenshot({ path: `${sortie}/guide-card-actions-desktop.png`, clip: { x: Math.max(0, b.x - 380), y: Math.max(0, b.y - 20), width: Math.min(1440, b.width + 760), height: b.height + 40 } });
  ok('card-actions'); await p.close(); }

// Apercu rapide
for (const [vp, nom, mob] of [[D, 'desktop', false], [M, 'mobile', true]]) {
  const p = await page(vp, mob);
  await p.goto(B + '/collections/all', { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const c = p.locator('.lf-card').first(); await c.scrollIntoViewIfNeeded(); if (!mob) await c.hover();
  await c.locator('.lf-card__act').first().click();
  await p.waitForSelector('.lf-qvp.is-open .lf-qv'); await p.waitForTimeout(1400);
  await p.screenshot({ path: `${sortie}/guide-quick-view-${nom}.png` });
  ok('quick-view ' + nom); await p.close();
}

// Galerie en carrousel avec vignettes
for (const [vp, nom, mob] of [[D, 'desktop', false], [M, 'mobile', true]]) {
  const p = await page(vp, mob);
  await p.goto(B + '/products/alma22?view=zzcar', { waitUntil: 'load' }); await p.waitForTimeout(1800);
  await p.screenshot({ path: `${sortie}/guide-product-carousel-${nom}.png` });
  ok('carousel ' + nom); await p.close();
}

// Galerie empilee avec vignettes
{ const p = await page(D);
  await p.goto(B + '/products/alma22?view=zzthumb', { waitUntil: 'load' }); await p.waitForTimeout(1500);
  await p.mouse.wheel(0, 700); await p.waitForTimeout(1200);
  await p.screenshot({ path: `${sortie}/guide-product-thumbs-desktop.png` });
  ok('thumbs'); await p.close(); }

// Pastilles
{ const p = await page(D);
  await p.goto(B + '/products/alma22', { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const info = p.locator('.lf-product__info').first();
  const v = p.locator('.lf-product__variants').first(); await v.scrollIntoViewIfNeeded(); await p.waitForTimeout(500);
  const bi = await info.boundingBox(); const bv = await v.boundingBox();
  await p.screenshot({ path: `${sortie}/guide-swatches-desktop.png`, clip: { x: bi.x, y: Math.max(0, bv.y - 220), width: bi.width, height: 420 } });
  ok('swatches'); await p.close(); }

// Mega menu
{ const p = await page(D);
  await p.goto(B + '/collections/all', { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const item = p.locator('.lf-hdr__item:has(.lf-hdr__mega)').first();
  await item.hover(); await p.waitForTimeout(1600);
  await p.screenshot({ path: `${sortie}/guide-mega-menu-desktop.png`, clip: { x: 0, y: 0, width: 1440, height: 640 } });
  ok('mega'); await p.close(); }

await browser.close();

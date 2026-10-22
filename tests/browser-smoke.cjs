/* Optional browser QA. Uses an already installed Playwright; no project packages. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const prefix = '/nonfunzionacosi/';
const pages = ['pagine/home.html', 'pagine/chi_siamo.html',
    'articoli/petrolio_wti/index_petrolio.html', 'articoli/superbonus_110/index_superbonus.html'];
const mime = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.woff2': 'font/woff2' };
const fontVariants = [
    '500 16px Cinzel', '700 16px Cinzel',
    '400 16px "Playfair Display"', '700 16px "Playfair Display"', 'italic 400 16px "Playfair Display"',
    '400 16px Inter', '500 16px Inter', '600 16px Inter', '700 16px Inter'
];
const server = http.createServer((req, res) => {
    let file;
    try {
        const url = new URL(req.url, 'http://localhost');
        if (!url.pathname.startsWith(prefix)) throw new Error('Invalid path');
        file = path.resolve(root, decodeURIComponent(url.pathname.slice(prefix.length)) || 'index.html');
        if (!file.startsWith(root + path.sep) || !fs.statSync(file).isFile()) throw new Error('Not found');
    } catch {
        res.writeHead(404).end(); return;
    }
    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
});

(async () => {
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}${prefix}`;
    const browser = await chromium.launch({ headless: true,
        ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) });
    const output = process.env.QA_OUTPUT;
    if (output) fs.mkdirSync(output, { recursive: true });
    let checks = 0;
    try {
        for (const width of [320, 390, 768, 1440]) {
            for (const route of pages) {
                const page = await browser.newPage({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
                const errors = [];
                page.on('pageerror', error => errors.push(error.message));
                page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
                page.on('response', response => { if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
                page.on('request', request => { if (!request.url().startsWith(base)) errors.push(`External request: ${request.url()}`); });
                await page.goto(base + route);
                const fontsLoaded = await page.evaluate(async variants => {
                    const faces = await Promise.all(variants.map(font => document.fonts.load(font, 'È già così — 123 € Āă')));
                    await document.fonts.ready;
                    return faces.every(group => group.length > 0 && group.every(face => face.status === 'loaded'));
                }, fontVariants);
                assert.equal(fontsLoaded, true, `${route} at ${width}: local font variants failed to load`);
                assert.deepEqual(errors, [], `${route} at ${width}: browser errors`);
                assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), true,
                    `${route} at ${width}: horizontal overflow`);
                assert.equal(await page.locator('img').evaluateAll(images => images.every(img => img.complete && img.naturalWidth > 0)), true, 'Broken image');
                assert.equal(await page.locator('main').count(), 1);
                assert.equal(await page.locator('main').isVisible(), true);
                if (route.startsWith('articoli/')) {
                    assert.equal(await page.getByRole('complementary', { name: 'Nota di archivio' }).isVisible(), true);
                    assert.equal(await page.locator('main .archive-notice').count(), 0, 'Archive notice must not alter original article text');
                }
                if (route.includes('petrolio_wti')) {
                    const heroFits = await page.locator('.dossier-hero').evaluate(hero => {
                        const bounds = hero.getBoundingClientRect();
                        return [...hero.querySelectorAll('.badge-dossier, h1, .subtitle')].every(element => {
                            const rect = element.getBoundingClientRect();
                            return rect.top >= bounds.top - 1 && rect.bottom <= bounds.bottom + 1 &&
                                rect.left >= bounds.left - 1 && rect.right <= bounds.right + 1;
                        });
                    });
                    assert.equal(heroFits, true, `Oil dossier at ${width}: clipped title, badge or subtitle`);
                }
                if (output && [390, 1440].includes(width)) {
                    await page.screenshot({ path: path.join(output, `${path.basename(route, '.html')}-${width}.png`), fullPage: true });
                }
                await page.close(); checks++;
            }
        }
        const page = await browser.newPage();
        await page.goto(base);
        await page.waitForURL(base + 'pagine/home.html');
        await page.locator('[data-slide="1"]').click();
        assert.equal(await page.locator('.banner-slide:not([hidden]) h2').textContent(), 'Giornalismo Senza Filtri');
        await page.locator('[data-slide="1"]').press('ArrowRight');
        assert.equal(await page.locator('.banner-slide:not([hidden]) h2').textContent(), 'Radici Italiane, Valori Eterni');
        assert.equal(await page.locator('[data-slide="2"]').getAttribute('aria-pressed'), 'true');
        await page.locator('[data-slide="2"]').press('Home');
        assert.equal(await page.locator('.banner-slide:not([hidden])').count(), 1);
        assert.equal(await page.locator('form,input[type="email"]').count(), 0);
        assert.equal(await page.getByRole('heading', { name: 'Resta Libero. Newsletter in arrivo.' }).isVisible(), true);
        assert.equal(await page.locator('.newsletter button, .newsletter a').count(), 0);
        await page.evaluate(() => {
            window.cspViolations = [];
            document.addEventListener('securitypolicyviolation', e => window.cspViolations.push(e.effectiveDirective));
            const injected = document.createElement('script');
            injected.textContent = 'window.inlineCodeExecuted = true';
            document.body.append(injected);
            const button = document.createElement('button');
            button.setAttribute('onclick', 'window.inlineHandlerExecuted = true');
            document.body.append(button); button.click(); button.remove();
        });
        await page.waitForFunction(() => window.cspViolations.length >= 2);
        assert.equal(await page.evaluate(() => !!window.inlineCodeExecuted || !!window.inlineHandlerExecuted), false);
        assert.ok((await page.evaluate(() => window.cspViolations)).includes('script-src-elem'));
        assert.ok((await page.evaluate(() => window.cspViolations)).includes('script-src-attr'));
        let externalFontRequest = false;
        await page.route('https://example.invalid/**', route => {
            externalFontRequest = true;
            return route.abort();
        });
        const externalFontBlocked = await page.evaluate(async () => {
            const font = new FontFace('BlockedExternalFont', 'url("https://example.invalid/font.woff2")');
            try { await font.load(); return false; } catch { return true; }
        });
        await page.waitForFunction(() => window.cspViolations.includes('font-src'));
        assert.equal(externalFontBlocked, true, 'CSP must block external fonts');
        assert.equal(externalFontRequest, false, 'External font must be blocked before the network');
        await page.close();
        const noJS = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 900 } });
        const staticPage = await noJS.newPage();
        await staticPage.goto(base);
        await staticPage.waitForURL(base + 'pagine/home.html');
        assert.equal(await staticPage.locator('.banner-slide:visible').count(), 3);
        assert.equal(await staticPage.locator('.banner-dots:visible').count(), 0);
        assert.equal(await staticPage.locator('main a[href*="index_petrolio"]').count(), 3);
        await noJS.close();
        console.log(`PASS: ${checks} page/viewport combinations; 9 local font variants, redirect, keyboard carousel, no-JS fallback, newsletter and browser CSP enforcement.`);
    } finally {
        await browser.close();
        await new Promise(resolve => server.close(resolve));
    }
})().catch(error => { console.error(error); server.close(); process.exitCode = 1; });

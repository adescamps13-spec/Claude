// Screenshot each #id of a local cards page to <outDir>/<id>.png (transparent corners).
// node tools/cardshot.mjs cards.html outDir id1 id2 ...
import { chromium } from "/opt/node22/lib/node_modules/playwright/index.mjs";
const [page, outDir, ...ids] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 840, height: 1000 }, deviceScaleFactor: 1 });
await p.goto("file://" + page);
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(300);
for (const id of ids) await (await p.$("#" + id)).screenshot({ path: `${outDir}/${id}.png`, omitBackground: true });
await b.close();

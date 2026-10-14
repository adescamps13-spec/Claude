// Rend card.html image par image (fond transparent) puis encode les vidéos.
// Usage : node render.js [outDir] [fps] [scale]
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const outDir = path.resolve(process.argv[2] || path.join(__dirname, "..", "exports"));
const FPS = parseInt(process.argv[3] || "30", 10);
const SCALE = parseFloat(process.argv[4] || "3");
const page = "file://" + path.join(__dirname, "card.html");

async function renderSeq(browser, query, dir) {
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });
  const ctx = await browser.newContext({ viewport: { width: 420, height: 420 }, deviceScaleFactor: SCALE });
  const p = await ctx.newPage();
  await p.goto(page + "?t=0" + query);
  await p.evaluate(() => document.fonts.ready);
  const duration = await p.evaluate(() => window.DURATION);
  const n = Math.round(duration * FPS);
  for (let i = 0; i <= n; i++) {
    await p.evaluate(t => window.render(t), i / FPS);
    await p.screenshot({ path: path.join(dir, `f_${String(i).padStart(4, "0")}.png`), omitBackground: true });
  }
  await ctx.close();
  return n;
}

(async () => {
  const browser = await chromium.launch();
  fs.mkdirSync(outDir, { recursive: true });
  const seq = path.join(outDir, "_seq");
  const matte = path.join(outDir, "_matte");
  await renderSeq(browser, "", seq);
  await renderSeq(browser, "&matte", matte);

  // Image fixe (état complet)
  const ctx = await browser.newContext({ viewport: { width: 420, height: 420 }, deviceScaleFactor: SCALE });
  const p = await ctx.newPage();
  await p.goto(page + "?t=4.8");
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(outDir, "carte_paiement_finale.png"), omitBackground: true });
  await browser.close();

  const ff = (...args) => execFileSync("ffmpeg", ["-v", "error", "-y", "-framerate", String(FPS), ...args], { stdio: "inherit" });
  ff("-i", path.join(seq, "f_%04d.png"), "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
     "-alpha_bits", "8", "-vendor", "apl0", "-qscale:v", "16", path.join(outDir, "carte_paiement_alpha_prores4444.mov"));
  ff("-i", path.join(seq, "f_%04d.png"), "-c:v", "png", "-pix_fmt", "rgba",
     path.join(outDir, "carte_paiement_alpha_sans_perte.mov"));
  ff("-i", path.join(seq, "f_%04d.png"), "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "22",
     "-row-mt", "1", path.join(outDir, "carte_paiement_alpha.webm"));
  ff("-i", path.join(matte, "f_%04d.png"), "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
     "-alpha_bits", "16", "-vendor", "apl0", path.join(outDir, "carte_paiement_masque_flou.mov"));
  console.log("OK →", outDir);
})();

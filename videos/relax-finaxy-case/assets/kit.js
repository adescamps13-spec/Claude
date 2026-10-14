/* Motion kit for the Relax × Finaxy case (v2).
 * Loaded once by index.html; scenes call window.KIT. Deterministic and seek-safe:
 * seeded random only, every derived state is a pure function of a tweened proxy.
 */
(function () {
  function rng(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // wrap each character in an inline-block span; returns the spans
  function letters(el, text) {
    el.innerHTML = [...text].map((c) => `<span style="display:inline-block">${c === " " ? "&nbsp;" : c}</span>`).join("");
    return [...el.children];
  }

  /* Curved iridescent film strip (after Jerry's carousel).
   * Cards (pre-rendered PNGs) sit on a flat strip that bends onto a cylinder past ±FLAT,
   * the bent part flushes iridescent and smears. Drive it with place(v), v = scroll px.
   * Card k is centred when v = k * STEP. */
  function film(o) {
    const CW = o.CW || 840, CH = o.CH || 480, GAP = o.GAP || 220, SW = o.SW || 42;
    const FLAT = o.FLAT || 470, R = o.R || 360, CX = o.CX || 960;
    const STEP = CW + GAP, imgs = o.imgs, slices = [];
    const TOTAL = imgs.length * STEP + 1000;
    for (let x = -1200; x < TOTAL; x += SW) {
      const k = Math.floor((x + GAP / 2) / STEP), local = x - k * STEP;
      const inCard = k >= 0 && k < imgs.length && local >= 0 && local < CW;
      const sl = document.createElement("div");
      sl.style.cssText = `position:absolute;top:0;height:${CH}px;width:${SW + 1}px;overflow:hidden;transform-origin:50% 50%;display:none`;
      sl.innerHTML = (inCard
        ? `<div style="position:absolute;top:0;left:${-local}px;width:${CW}px;height:${CH}px;background:url(${imgs[k]}) 0 0/${CW}px ${CH}px"></div>`
        : `<div style="position:absolute;left:0;right:0;top:${CH * 0.07}px;bottom:${CH * 0.07}px;opacity:0;background:linear-gradient(180deg,#7FE3F0 0%,#B3C3F7 55%,#8FDDF6 100%)"></div>`)
        + `<div style="position:absolute;inset:0;opacity:0;background:linear-gradient(180deg,#8EEBF7 0%,#B9A8F0 38%,#F0A9E2 70%,#8FDDF6 100%)"></div>`;
      o.el.appendChild(sl);
      slices.push({ el: sl, x, irid: sl.lastChild, band: inCard ? null : sl.firstChild });
    }
    const mirrors = [];
    if (o.mirror) {
      o.mirror.innerHTML = imgs.map((u) => `<div style="position:absolute;top:0;left:0;width:${CW}px;height:${CH * 0.42}px;border-radius:26px;background:url(${u}) 0 100%/${CW}px ${CH}px"></div>`).join("");
      mirrors.push(...o.mirror.children);
    }
    function place(v) {
      for (const s of slices) {
        const xs = s.x + SW / 2 - v - CW / 2, ax = Math.abs(xs), sg = Math.sign(xs) || 1;
        let X = xs, Z = 0, rot = 0, bend = 0;
        if (ax > FLAT) {
          const th = Math.min((ax - FLAT) / R, 1.9);
          X = sg * (FLAT + R * Math.sin(th));
          Z = -R * (1 - Math.cos(th));
          rot = -sg * th * 57.2958;
          bend = Math.min(1, th / 1.05);
        }
        const on = ax < FLAT + R * 1.85;
        s.el.style.display = on ? "block" : "none";
        if (!on) continue;
        s.el.style.transform = `translate3d(${(CX + X - SW / 2).toFixed(1)}px,0,${Z.toFixed(1)}px) rotateY(${rot.toFixed(2)}deg) scaleX(${(1 + bend * 0.3).toFixed(3)})`;
        s.irid.style.opacity = (bend * 0.9).toFixed(3);
        if (s.band) s.band.style.opacity = (bend * 0.95).toFixed(3);
      }
      mirrors.forEach((m, k) => {
        const off = k * STEP - v;
        m.style.transform = `translateX(${(CX - CW / 2 + off).toFixed(1)}px) scaleY(-1)`;
        m.style.opacity = Math.max(0, 1 - Math.abs(off) / 520).toFixed(3);
      });
      return Math.abs(v / STEP - Math.round(v / STEP)) < 0.004 ? Math.round(v / STEP) : -1; // card at rest, or -1
    }
    return { place, STEP, CW, CH };
  }

  // bracket title slot: { word } that slides one word at a time; words laid on a strip of width W
  function slot(strip, words, W) {
    strip.innerHTML = words.map((w) => `<span style="display:inline-block;width:${W}px;text-align:center">${w}</span>`).join("");
    return (i) => -i * W;
  }

  window.KIT = { rng, letters, film, slot };
})();

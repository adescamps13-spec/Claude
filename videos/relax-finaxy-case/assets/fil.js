/* Shared helpers for the Relax × Finaxy case.
 * Loaded once by index.html; every scene calls window.FIL.
 * Everything here is deterministic: seeded random, geometry measured at build time,
 * state driven only by timeline position (seek-safe).
 */
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const C = {
    white: "#FFFFFF", ink: "#212C34", ink2: "#6B7278", lav: "#D4CCEE", purple: "#6955AA",
    pink: "#FF0055", cyan: "#56A0AA", yellow: "#ABA256", red: "#AA5655", grey: "#A7AEB4",
    navy: "#191853", fblue: "#5A80D9", slate: "#4A5892", cream: "#F4F1EB", burg: "#9C0A3F",
  };

  // mulberry32 — seeded PRNG
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

  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  // The Relax ribbon gradient, defined once per svg.
  function defs(svg, id) {
    const d = el("defs", {}, svg);
    const g = el("linearGradient", { id: `rib-${id}`, x1: "0", x2: "1", y1: "0", y2: "0", gradientUnits: "objectBoundingBox" }, d);
    el("stop", { offset: "0", "stop-color": C.lav }, g);
    el("stop", { offset: ".55", "stop-color": C.purple }, g);
    el("stop", { offset: "1", "stop-color": "#C77DDB" }, g);
    return d;
  }

  /**
   * A thread: soft lavender halo + gradient core + optional pink head dot.
   * Drawn by a progress proxy p ∈ [0,1]; the head rides the path tip.
   * Returns { draw(tl, from, to, at, dur, ease), pointAt(p), len, nodes }.
   */
  function thread(svg, id, d, opts) {
    const o = Object.assign({ w: 6, head: true, halo: true }, opts || {});
    const g = el("g", { class: "fil" }, svg);
    const halo = o.halo ? el("path", { d, fill: "none", stroke: C.lav, "stroke-width": o.w * 4, "stroke-linecap": "round", opacity: ".55" }, g) : null;
    const core = el("path", { d, fill: "none", stroke: `url(#rib-${id})`, "stroke-width": o.w, "stroke-linecap": "round" }, g);
    const head = o.head ? el("circle", { r: o.w * 2.1, fill: C.pink, cx: -100, cy: -100 }, g) : null;
    const len = core.getTotalLength();
    [halo, core].forEach((p) => p && (p.style.strokeDasharray = `${len} ${len + 10}`));
    const proxy = { p: 0 };
    const apply = () => {
      const off = len * (1 - proxy.p);
      if (halo) halo.style.strokeDashoffset = off;
      core.style.strokeDashoffset = off;
      if (head) {
        const pt = core.getPointAtLength(len * proxy.p);
        head.setAttribute("cx", pt.x);
        head.setAttribute("cy", pt.y);
        head.setAttribute("opacity", proxy.p > 0.001 ? 1 : 0);
      }
    };
    apply();
    let first = true;
    return {
      len, core, head, group: g,
      pointAt: (p) => core.getPointAtLength(len * p),
      draw(tl, from, to, at, dur, ease) {
        tl.fromTo(proxy, { p: from }, { p: to, duration: dur, ease: ease || "expo.inOut", onUpdate: apply, immediateRender: first }, at);
        first = false;
        return this;
      },
      set(p) { proxy.p = p; apply(); },
    };
  }

  /** Progress along a path where it passes closest to (x,y) — for "head reaches node" timing. */
  function progressNear(th, x, y) {
    let best = 0, bd = 1e9;
    for (let i = 0; i <= 400; i++) {
      const pt = th.pointAt(i / 400);
      const dd = (pt.x - x) ** 2 + (pt.y - y) ** 2;
      if (dd < bd) { bd = dd; best = i / 400; }
    }
    return best;
  }

  /** Finite yoyo jitter on an element (seek-safe: fromTo, finite repeat). */
  function jitter(tl, target, r, ampX, ampY, start, end) {
    const dur = 0.28 + r() * 0.3;
    const reps = Math.max(0, Math.floor((end - start) / dur) - 1);
    tl.fromTo(target, { x: -ampX * r(), y: -ampY * r() }, { x: ampX * (0.4 + r()), y: ampY * (0.4 + r()), duration: dur, ease: "sine.inOut", yoyo: true, repeat: reps }, start);
  }

  window.FIL = { C, rng, el, defs, thread, progressNear, jitter };
})();

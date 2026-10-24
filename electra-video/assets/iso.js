// Tiny isometric SVG engine shared by every scene.
// World units: x runs to the lower right, y to the lower left, z up.
// Every scene calls its own render(t) from a GSAP proxy tween, so each frame
// is a pure function of scene time.
(function () {
  const C = Math.cos(Math.PI / 6);
  const S = 0.5;

  function clamp(v, a, b) {
    return v < a ? a : v > b ? b : v;
  }
  // 0..1 progress of t inside [a, b]
  function seg(t, a, b) {
    return clamp((t - a) / (b - a), 0, 1);
  }
  function lerp(a, b, k) {
    return a + (b - a) * k;
  }
  const easeCache = {};
  function ease(name, k) {
    if (!easeCache[name]) easeCache[name] = gsap.parseEase(name);
    return easeCache[name](clamp(k, 0, 1));
  }
  // closed-form spring, damping ratio z, settles around k = 1
  function spring(k, z = 0.5, w = 14) {
    if (k <= 0) return 0;
    if (k >= 1) return 1;
    const t = k * 1.4;
    const wd = w * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + ((z * w) / wd) * Math.sin(wd * t));
  }
  // seeded PRNG
  function rng(seed) {
    let a = seed >>> 0;
    return function () {
      a |= 0;
      a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function hex2rgb(h) {
    const n = parseInt(h.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function rgb2hex(r, g, b) {
    return "#" + [r, g, b].map((v) => clamp(Math.round(v), 0, 255).toString(16).padStart(2, "0")).join("");
  }
  // k > 0 lightens toward white, k < 0 darkens toward black
  function shade(h, k) {
    const [r, g, b] = hex2rgb(h);
    if (k >= 0) return rgb2hex(r + (255 - r) * k, g + (255 - g) * k, b + (255 - b) * k);
    return rgb2hex(r * (1 + k), g * (1 + k), b * (1 + k));
  }
  function mix(h1, h2, k) {
    const a = hex2rgb(h1);
    const b = hex2rgb(h2);
    return rgb2hex(lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k));
  }

  function cam(ox, oy, s) {
    return { ox, oy, s };
  }
  // camera whose world point (x,y,z) lands on screen point (sx,sy)
  function camAt(x, y, z, sx, sy, s) {
    return { ox: sx - (x - y) * C * s, oy: sy - (x + y) * S * s + z * s, s };
  }
  function p(c, x, y, z) {
    return [c.ox + (x - y) * C * c.s, c.oy + (x + y) * S * c.s - z * c.s];
  }
  function pts(c, list) {
    return list
      .map((q) => {
        const r = p(c, q[0], q[1], q[2]);
        return r[0].toFixed(1) + "," + r[1].toFixed(1);
      })
      .join(" ");
  }
  function attrs(o) {
    let s = "";
    for (const k in o) if (o[k] !== undefined && o[k] !== null) s += " " + k + '="' + o[k] + '"';
    return s;
  }
  function poly(c, list, fill, extra) {
    return "<polygon points=\"" + pts(c, list) + '" fill="' + fill + '"' + attrs(extra || {}) + "/>";
  }

  // A box: three visible faces. o = {x,y,z,w,d,h, color | top/left/right, stroke, sw, op}
  function box(c, o) {
    const { x, y, w, d } = o;
    const z = o.z || 0;
    const h = Math.max(o.h, 0.0001);
    const top = o.top || shade(o.color, 0.18);
    const left = o.left || o.color;
    const right = o.right || shade(o.color, -0.22);
    const ex = { stroke: o.stroke, "stroke-width": o.sw, "stroke-linejoin": o.stroke ? "round" : undefined };
    const g = o.op !== undefined && o.op < 1 ? '<g opacity="' + o.op.toFixed(3) + '">' : "<g>";
    return (
      g +
      poly(c, [[x, y + d, z], [x + w, y + d, z], [x + w, y + d, z + h], [x, y + d, z + h]], left, ex) +
      poly(c, [[x + w, y, z], [x + w, y + d, z], [x + w, y + d, z + h], [x + w, y, z + h]], right, ex) +
      poly(c, [[x, y, z + h], [x + w, y, z + h], [x + w, y + d, z + h], [x, y + d, z + h]], top, ex) +
      "</g>"
    );
  }

  // A flat quad on a horizontal plane at height z
  function tile(c, x, y, z, w, d, fill, extra) {
    return poly(c, [[x, y, z], [x + w, y, z], [x + w, y + d, z], [x, y + d, z]], fill, extra);
  }

  // A vertical cylinder (coins, pillars, poles). o = {x,y,z,r,h,top,side,rim}
  function cyl(c, o) {
    const rx = Math.SQRT2 * C * o.r * c.s;
    const ry = Math.SQRT2 * S * o.r * c.s;
    const b = p(c, o.x, o.y, o.z || 0);
    const t = p(c, o.x, o.y, (o.z || 0) + o.h);
    const side = o.side;
    const ex = o.rim ? ' stroke="' + o.rim + '" stroke-width="' + (o.rimw || 3) + '"' : "";
    let s = "<g" + (o.op !== undefined ? ' opacity="' + o.op.toFixed(3) + '"' : "") + ">";
    s +=
      '<path d="M' + (b[0] - rx).toFixed(1) + "," + b[1].toFixed(1) +
      " A" + rx.toFixed(1) + "," + ry.toFixed(1) + " 0 0 0 " + (b[0] + rx).toFixed(1) + "," + b[1].toFixed(1) +
      " L" + (t[0] + rx).toFixed(1) + "," + t[1].toFixed(1) +
      " L" + (t[0] - rx).toFixed(1) + "," + t[1].toFixed(1) + ' Z" fill="' + side + '"' + ex + "/>";
    s +=
      '<ellipse cx="' + t[0].toFixed(1) + '" cy="' + t[1].toFixed(1) + '" rx="' + rx.toFixed(1) + '" ry="' +
      ry.toFixed(1) + '" fill="' + o.top + '"' + ex + "/>";
    if (o.inner) {
      s +=
        '<ellipse cx="' + t[0].toFixed(1) + '" cy="' + t[1].toFixed(1) + '" rx="' + (rx * 0.66).toFixed(1) +
        '" ry="' + (ry * 0.66).toFixed(1) + '" fill="none" stroke="' + o.inner + '" stroke-width="' + (o.innerw || 4) + '"/>';
    }
    return s + "</g>";
  }

  // Flat circle on the ground (shadows, rings)
  function disc(c, x, y, z, r, fill, extra) {
    const q = p(c, x, y, z);
    return (
      '<ellipse cx="' + q[0].toFixed(1) + '" cy="' + q[1].toFixed(1) + '" rx="' + (Math.SQRT2 * C * r * c.s).toFixed(1) +
      '" ry="' + (Math.SQRT2 * S * r * c.s).toFixed(1) + '" fill="' + fill + '"' + attrs(extra || {}) + "/>"
    );
  }

  // SVG transform that maps 1 local unit onto a face; local y runs down the face.
  // face: "left" (plane y = const, reads along +x), "right" (plane x = const, reads along -y), "top"
  function faceMatrix(c, face, x, y, z) {
    const q = p(c, x, y, z);
    const s = c.s;
    let m;
    if (face === "left") m = [C * s, S * s, 0, s];
    else if (face === "right") m = [C * s, -S * s, 0, s];
    else m = [C * s, S * s, -C * s, S * s];
    return "matrix(" + m.map((v) => v.toFixed(4)).join(",") + "," + q[0].toFixed(1) + "," + q[1].toFixed(1) + ")";
  }

  // Polyline through world points, as an SVG path "d"
  function pathD(c, list) {
    return list
      .map((q, i) => {
        const r = p(c, q[0], q[1], q[2] || 0);
        return (i ? "L" : "M") + r[0].toFixed(1) + "," + r[1].toFixed(1);
      })
      .join(" ");
  }

  // point at fraction k along a world polyline, plus the segment heading
  function along(list, k) {
    const lens = [];
    let total = 0;
    for (let i = 1; i < list.length; i++) {
      const l = Math.hypot(list[i][0] - list[i - 1][0], list[i][1] - list[i - 1][1]);
      lens.push(l);
      total += l;
    }
    let dist = clamp(k, 0, 1) * total;
    for (let i = 0; i < lens.length; i++) {
      if (dist <= lens[i] || i === lens.length - 1) {
        const f = lens[i] ? dist / lens[i] : 0;
        const a = list[i];
        const b = list[i + 1];
        return { x: lerp(a[0], b[0], f), y: lerp(a[1], b[1], f), dx: b[0] - a[0], dy: b[1] - a[1], total };
      }
      dist -= lens[i];
    }
    return { x: list[0][0], y: list[0][1], dx: 1, dy: 0, total };
  }

  // A small car. Faces +x when dir = "x", +y when dir = "y". o = {x,y,z,dir,body,glass}
  function car(c, o) {
    const body = o.body || "#173847";
    const glass = o.glass || "#BFF6EA";
    const z = o.z || 0;
    let s = "";
    if (o.dir === "y") {
      s += box(c, { x: o.x + 0.05, y: o.y + 0.25, z, w: 1.0, d: 0.42, h: 0.28, color: "#0B1F28" });
      s += box(c, { x: o.x + 0.05, y: o.y + 1.45, z, w: 1.0, d: 0.42, h: 0.28, color: "#0B1F28" });
      s += box(c, { x: o.x, y: o.y, z: z + 0.16, w: 1.1, d: 2.2, h: 0.46, color: body });
      s += box(c, { x: o.x + 0.08, y: o.y + 0.55, z: z + 0.62, w: 0.94, d: 1.15, h: 0.38, color: glass, top: shade(body, 0.12) });
      s += box(c, { x: o.x + 0.12, y: o.y + 2.18, z: z + 0.36, w: 0.22, d: 0.04, h: 0.12, color: "#F7FFF9" });
      s += box(c, { x: o.x + 0.76, y: o.y + 2.18, z: z + 0.36, w: 0.22, d: 0.04, h: 0.12, color: "#F7FFF9" });
    } else {
      s += box(c, { x: o.x + 0.25, y: o.y + 0.05, z, w: 0.42, d: 1.0, h: 0.28, color: "#0B1F28" });
      s += box(c, { x: o.x + 1.45, y: o.y + 0.05, z, w: 0.42, d: 1.0, h: 0.28, color: "#0B1F28" });
      s += box(c, { x: o.x, y: o.y, z: z + 0.16, w: 2.2, d: 1.1, h: 0.46, color: body });
      s += box(c, { x: o.x + 0.55, y: o.y + 0.08, z: z + 0.62, w: 1.15, d: 0.94, h: 0.38, color: glass, top: shade(body, 0.12) });
      s += box(c, { x: o.x + 2.18, y: o.y + 0.12, z: z + 0.36, w: 0.04, d: 0.22, h: 0.12, color: "#F7FFF9" });
      s += box(c, { x: o.x + 2.18, y: o.y + 0.76, z: z + 0.36, w: 0.04, d: 0.22, h: 0.12, color: "#F7FFF9" });
    }
    return s;
  }

  // ---- camera energy -------------------------------------------------
  // eased push that holds: 0 before t0, a after t0 + dur
  function push(t, t0, dur, a, e = "expo.out") {
    return a * ease(e, seg(t, t0, t0 + dur));
  }
  // quick bump that decays back to 0
  function bump(t, t0, a, decay = 9) {
    if (t < t0) return 0;
    const k = t - t0;
    return a * Math.min(1, k / 0.05) * Math.exp(-k * decay);
  }
  // seeded decaying shake from a list of hit times -> [dx, dy]
  function shake(t, hits, amp, decay = 10) {
    let dx = 0;
    let dy = 0;
    hits.forEach((h, i) => {
      if (t < h) return;
      const k = t - h;
      const e = amp * Math.exp(-k * decay);
      dx += e * Math.sin(k * 61 + i * 1.7);
      dy += e * Math.cos(k * 53 + i * 2.3);
    });
    return [dx, dy];
  }
  // wrap a painted world in a 2D camera: zoom k about (cx, cy), offset, roll in degrees
  function camFx(svgStr, o) {
    const k = o.k || 1;
    const cx = o.cx === undefined ? 540 : o.cx;
    const cy = o.cy === undefined ? 960 : o.cy;
    return (
      '<g transform="translate(' + ((o.dx || 0) + cx).toFixed(1) + "," + ((o.dy || 0) + cy).toFixed(1) + ") rotate(" + (o.rot || 0).toFixed(2) + ") scale(" + k.toFixed(4) + ") translate(" + (-cx) + "," + (-cy) + ')">' +
      svgStr + "</g>"
    );
  }
  // screen-space speed streaks along the iso y axis (down-left), pure function of t
  function streaks(t, n, speed, seed, color = "#FFFFFF", op = 0.55) {
    const r = rng(seed);
    let s = "";
    for (let i = 0; i < n; i++) {
      const x0 = r() * 1700 - 100;
      const y0 = r() * 1400 + 300;
      const len = 120 + r() * 220;
      const span = 2600;
      const d = ((t * speed * (0.7 + r() * 0.6) + r() * span) % span) - 600;
      const x = x0 - d * C;
      const y = y0 + d * S;
      s += '<line x1="' + x.toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + (x + len * C).toFixed(1) + '" y2="' + (y - len * S).toFixed(1) + '" stroke="' + color + '" stroke-width="5" stroke-linecap="round" opacity="' + op + '"/>';
    }
    return s;
  }

  // Sort drawables {k, s} back to front and join them
  function paint(list) {
    return list
      .sort((a, b) => a.k - b.k)
      .map((d) => d.s)
      .join("");
  }

  window.ISO = { C, S, clamp, seg, lerp, ease, spring, rng, shade, mix, cam, camAt, p, pts, poly, box, tile, cyl, disc, faceMatrix, pathD, along, car, paint, push, bump, shake, camFx, streaks };
})();

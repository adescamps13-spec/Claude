// The open road shared by the promise and the claim scenes: a band of land
// along the y axis with a road, dashes and trees, followed by the camera.
(function () {
  const I = window.ISO;
  const R = I.rng(41);
  const trees = [];
  for (let i = 0; i < 160; i++) {
    const side = R() < 0.5 ? -1 : 1;
    trees.push({ x: side * (1.6 + R() * 2.6), y: -30 + R() * 140, r: 0.2 + R() * 0.18, h: 0.5 + R() * 0.6 });
  }
  const poles = [];
  for (let y = -30; y < 110; y += 3.2) poles.push(y);

  // D: drawables list; c: camera; yc: the y the camera follows
  function drawRoad(c, D, yc) {
    const y0 = yc - 26;
    const y1 = yc + 26;
    D.push({ k: -1000, s: I.box(c, { x: -4.6, y: y0, z: -0.45, w: 9.2, d: y1 - y0, h: 0.45, top: "#CFF0E4", left: "#9BD3C3", right: "#7DC1B0" }) });
    D.push({ k: -999, s: I.tile(c, -0.95, y0, 0.002, 1.9, y1 - y0, "#1B3442") });
    const first = Math.floor(y0 / 1.6) * 1.6;
    for (let y = first; y < y1; y += 1.6) D.push({ k: -998, s: I.tile(c, -0.06, y, 0.004, 0.12, 0.7, "#45F5B9") });
    poles.forEach((py) => {
      if (py < y0 || py > y1) return;
      D.push({ k: 1.25 + py, s: I.box(c, { x: 1.2, y: py, z: 0, w: 0.08, d: 0.08, h: 0.5, color: "#F4FFFC" }) });
    });
    trees.forEach((tr) => {
      if (Math.abs(tr.y - yc) > 24) return;
      D.push({
        k: tr.x + tr.y,
        s:
          I.cyl(c, { x: tr.x, y: tr.y, z: 0, r: 0.06, h: 0.25, top: "#7A5A3A", side: "#5E452C" }) +
          I.cyl(c, { x: tr.x, y: tr.y, z: 0.22, r: tr.r, h: tr.h, top: "#5BD3A3", side: "#2DAE7F" }),
      });
    });
  }

  window.ROAD = { drawRoad };
})();

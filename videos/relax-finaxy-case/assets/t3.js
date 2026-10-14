/* 3D kit for the Relax × Finaxy case (v3) — soft glossy pastel objects in the Relax style.
 * A scene renders only when its GSAP timeline asks (render(t) from an onUpdate proxy), never from rAF,
 * so every frame is a pure function of time. Requires three.global.js + three-addons.js.
 */
(function () {
  const P = {
    lav: 0xd4ccee, peri: 0xa99cf0, pink: 0xf4c6e6, hot: 0xff0055, cyan: 0xcceaee, teal: 0x56a0aa,
    sand: 0xe0dec3, rose: 0xe1c3c3, ink: 0x212c34, white: 0xffffff, purple: 0x6955aa,
  };

  // a canvas-backed stage: renderer, scene, camera, studio environment and lights
  function stage(canvas, o = {}) {
    const W = o.w || canvas.width, H = o.h || canvas.height;
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(1);
    renderer.setSize(W, H, false);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = o.exposure || 1.05;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.setClearColor(0x000000, 0);
    const scene = new THREE.Scene();
    const pm = new THREE.PMREMGenerator(renderer);
    scene.environment = pm.fromScene(new THREE.RoomEnvironment(), 0.04).texture;
    const camera = new THREE.PerspectiveCamera(o.fov || 30, W / H, 0.1, 200);
    camera.position.set(0, o.camY || 0, o.camZ || 10);
    camera.lookAt(0, 0, 0);
    scene.add(new THREE.HemisphereLight(0xffffff, 0xd4ccee, 0.9));
    const key = new THREE.DirectionalLight(0xffffff, 1.6);
    key.position.set(-4, 6, 6);
    scene.add(key);
    const rim = new THREE.DirectionalLight(0xbfe9f0, 0.9);
    rim.position.set(5, -2, -4);
    scene.add(rim);
    return { renderer, scene, camera, W, H, render: () => renderer.render(scene, camera) };
  }

  // materials: glossy pastel "pearl-glass" and soft matte clay
  const glossy = (color, o = {}) => new THREE.MeshPhysicalMaterial({
    color, roughness: o.roughness ?? 0.16, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.08,
    iridescence: o.irid ?? 0.7, iridescenceIOR: 1.35, iridescenceThicknessRange: [180, 620],
    sheen: 0.4, sheenColor: new THREE.Color(0xffffff), transparent: !!o.opacity, opacity: o.opacity ?? 1,
  });
  const clay = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: o.roughness ?? 0.55, metalness: 0 });
  const glass = (color) => new THREE.MeshPhysicalMaterial({ color, roughness: 0.05, transmission: 0.9, thickness: 0.6, ior: 1.4, clearcoat: 1, iridescence: 0.5 });

  // soft contact shadow under an object (radial texture on a plane)
  function shadow(r = 1.4, o = 0.28) {
    const c = document.createElement("canvas");
    c.width = c.height = 128;
    const g = c.getContext("2d"), grd = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    grd.addColorStop(0, `rgba(42,34,68,${o})`);
    grd.addColorStop(1, "rgba(42,34,68,0)");
    g.fillStyle = grd;
    g.fillRect(0, 0, 128, 128);
    const m = new THREE.Mesh(new THREE.PlaneGeometry(r * 2, r * 2), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false }));
    m.rotation.x = -Math.PI / 2;
    return m;
  }

  const rbox = (w, h, d, r = 0.12, seg = 4) => new THREE.RoundedBoxGeometry(w, h, d, seg, r);
  const ease = { out: (x) => 1 - Math.pow(1 - x, 3), inOut: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2), clamp: (x) => Math.max(0, Math.min(1, x)) };

  window.T3 = { P, stage, glossy, clay, glass, shadow, rbox, ease };
})();

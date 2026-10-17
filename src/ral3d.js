/* JomaPaint · placa RAL en 3D (three.js).
   Placa de muestra taladrada, colgada de un gancho que pasa por el agujero.
   Acabados con material físico: mate (rugosa), satinado (reflejo difuso),
   brillante (barniz con reflejo nítido) y texturado (relieve real con mapa de normales).
   Se carga solo al acercarse a la sección de colores; si falla, se queda la placa SVG.
   Compilar: npm run build:3d  →  assets/ral3d.js */
import {
  WebGLRenderer, Scene, PerspectiveCamera, Group, Mesh, Shape, Path, ExtrudeGeometry,
  MeshPhysicalMaterial, MeshStandardMaterial, PlaneGeometry, CanvasTexture, DataTexture,
  RepeatWrapping, LinearMipmapLinearFilter, LinearFilter, NoColorSpace, SRGBColorSpace,
  NoToneMapping, PMREMGenerator, Vector2, Vector3, CatmullRomCurve3, TubeGeometry,
  DirectionalLight, Color, MathUtils, RGBAFormat, UnsignedByteType, SphereGeometry, MeshBasicMaterial,
  BackSide, Float32BufferAttribute
} from 'three';

/* ---------- mapas de normales procedurales (repetibles) ---------- */
function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function blur(src, N, r) {
  const out = new Float32Array(N * N), tmp = new Float32Array(N * N), w = 2 * r + 1;
  for (let pass = 0; pass < 2; pass++) {
    const a = pass ? out : src;
    for (let y = 0; y < N; y++) { let s = 0; for (let k = -r; k <= r; k++) s += a[y * N + ((k + N) % N)]; for (let x = 0; x < N; x++) { tmp[y * N + x] = s / w; s += a[y * N + ((x + r + 1) % N)] - a[y * N + ((x - r + N) % N)]; } }
    for (let x = 0; x < N; x++) { let s = 0; for (let k = -r; k <= r; k++) s += tmp[((k + N) % N) * N + x]; for (let y = 0; y < N; y++) { out[y * N + x] = s / w; s += tmp[((y + r + 1) % N) * N + x] - tmp[((y - r + N) % N) * N + x]; } }
  }
  return out;
}
function heightMap(N, octaves, seed) {
  const R = rng(seed), h = new Float32Array(N * N);
  for (const [r, wgt] of octaves) {
    const n = new Float32Array(N * N); for (let i = 0; i < n.length; i++) n[i] = R();
    const b = blur(n, N, r); let mn = 1e9, mx = -1e9; for (const v of b) { if (v < mn) mn = v; if (v > mx) mx = v; }
    for (let i = 0; i < h.length; i++) h[i] += ((b[i] - mn) / (mx - mn) - 0.5) * wgt;
  }
  return h;
}
function normalTex(N, octaves, seed, strength, maxAniso) {
  const h = heightMap(N, octaves, seed), d = new Uint8Array(N * N * 4), v = new Vector3();
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const dx = h[y * N + (x + 1) % N] - h[y * N + (x - 1 + N) % N];
    const dy = h[((y + 1) % N) * N + x] - h[((y - 1 + N) % N) * N + x];
    v.set(-dx * strength, -dy * strength, 1).normalize();
    const i = (y * N + x) * 4; d[i] = (v.x * 0.5 + 0.5) * 255; d[i + 1] = (v.y * 0.5 + 0.5) * 255; d[i + 2] = (v.z * 0.5 + 0.5) * 255; d[i + 3] = 255;
  }
  const t = new DataTexture(d, N, N, RGBAFormat, UnsignedByteType);
  t.wrapS = t.wrapT = RepeatWrapping; t.colorSpace = NoColorSpace; t.generateMipmaps = true;
  t.minFilter = LinearMipmapLinearFilter; t.magFilter = LinearFilter; t.anisotropy = maxAniso; t.needsUpdate = true;
  return t;
}

/* ---------- estudio para los reflejos ----------
   Sala gris con degradado y tres ventanas de luz. La principal, alta y estrecha,
   queda donde la placa la refleja hacia la cámara: con el vaivén, su reflejo cruza
   la placa (nítido en brillante, ancho y suave en satinado, ausente en mate). */
function studio() {
  const env = new Scene();
  const sg = new SphereGeometry(20, 48, 24), pos = sg.attributes.position, col = [];
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i) / 20, v = y > 0 ? 0.42 + 0.33 * y : 0.42 + 0.34 * y; // techo claro, suelo oscuro
    col.push(v, v, v * 1.01);
  }
  sg.setAttribute('color', new Float32BufferAttribute(col, 3));
  env.add(new Mesh(sg, new MeshBasicMaterial({ side: BackSide, vertexColors: true })));
  function panel(az, el, w, h, k, r) {
    const m = new Mesh(new PlaneGeometry(w, h), new MeshBasicMaterial({ color: new Color(k, k, k * 0.98), side: 2 }));
    r = r || 14;
    const a = az * Math.PI / 180, e = el * Math.PI / 180;
    m.position.set(Math.sin(a) * Math.cos(e) * r, Math.sin(e) * r, Math.cos(a) * Math.cos(e) * r);
    m.lookAt(0, 0, 0); env.add(m);
  }
  panel(36, 6, 1.25, 13, 5.5); // ventana principal, frente-derecha, partida en dos hojas
  panel(43.5, 6, 0.6, 13, 5.5);
  panel(-22, 10, 3.2, 9, 2.6); // relleno, frente-izquierda
  panel(10, 62, 9, 5, 3.2);    // cenital
  return env;
}

/* ---------- acabados ---------- */
// roughness: rugosidad de la capa; cc: barniz (clearcoat) y su rugosidad; spec: intensidad especular.
const GLOSS = {
  mate: { roughness: 0.9, cc: 0, ccr: 0.6, spec: 0.55, peel: 0.0 },
  satinado: { roughness: 0.5, cc: 0.05, ccr: 0.32, spec: 0.6, peel: 0 },
  brillante: { roughness: 0.45, cc: 1, ccr: 0.045, spec: 0.5, peel: 0 }
};
const TEXTURED = {
  mate: { roughness: 0.95, cc: 0, ccr: 0.6, spec: 0.5 },
  satinado: { roughness: 0.62, cc: 0.15, ccr: 0.45, spec: 0.8 },
  brillante: { roughness: 0.42, cc: 0.5, ccr: 0.16, spec: 0.9 }
};

export function init(host, opts) {
  opts = opts || {};
  const reduce = !!opts.reduce;
  let dirty = true;
  const canvas = document.createElement('canvas');
  canvas.className = 'ral-3d';
  canvas.setAttribute('role', 'img');
  host.appendChild(canvas);

  const renderer = new WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'low-power', preserveDrawingBuffer: !!opts.capture });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.toneMapping = NoToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.setClearColor(0x000000, 0);
  const aniso = renderer.capabilities.getMaxAnisotropy();

  const scene = new Scene();
  const pmrem = new PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(studio(), 0).texture;
  scene.environmentIntensity = 1;
  pmrem.dispose();

  const key = new DirectionalLight(0xffffff, 0.7);
  key.position.set(-2.5, 3, 4);
  scene.add(key);

  const camera = new PerspectiveCamera(28, 440 / 470, 0.1, 50);
  camera.position.set(0, 0.3, 3.95);
  camera.lookAt(0, 0.12, 0);

  /* ---------- placa taladrada ---------- */
  const W = 1.0, H = 1.62, T = 0.026, RC = 0.022, HR = 0.046, HY = H / 2 - 0.115;
  const sh = new Shape();
  const x0 = -W / 2, x1 = W / 2, y0 = -H / 2, y1 = H / 2;
  sh.moveTo(x0 + RC, y0); sh.lineTo(x1 - RC, y0); sh.quadraticCurveTo(x1, y0, x1, y0 + RC);
  sh.lineTo(x1, y1 - RC); sh.quadraticCurveTo(x1, y1, x1 - RC, y1); sh.lineTo(x0 + RC, y1);
  sh.quadraticCurveTo(x0, y1, x0, y1 - RC); sh.lineTo(x0, y0 + RC); sh.quadraticCurveTo(x0, y0, x0 + RC, y0);
  const hole = new Path(); hole.absarc(0, HY, HR, 0, Math.PI * 2, true); sh.holes.push(hole);
  const geo = new ExtrudeGeometry(sh, { depth: T - 0.008, bevelEnabled: true, bevelThickness: 0.004, bevelSize: 0.004, bevelSegments: 3, curveSegments: 48 });
  geo.translate(0, 0, -(T - 0.008) / 2);

  const peelTex = normalTex(256, [[22, 1], [9, 0.3]], 7, 22, aniso);
  const sandTex = normalTex(256, [[1, 1], [3, 0.55]], 11, 7, aniso);
  peelTex.repeat.set(2.2, 2.2); sandTex.repeat.set(2.6, 2.6);

  const mat = new MeshPhysicalMaterial({ color: 0xf7b500, roughness: 0.46, metalness: 0, clearcoat: 0, ior: 1.5 });
  const plate = new Mesh(geo, mat);

  /* pivote = punto donde el canto superior del agujero apoya en el alambre */
  const pivot = new Group();
  pivot.position.set(0, 0.86, 0);
  plate.position.y = -(HY + HR);
  pivot.add(plate);
  scene.add(pivot);

  /* ---------- gancho: baja por delante, entra en el agujero y sale por detrás ---------- */
  const WR = 0.0105, D = 0.052, CY = -WR + D;
  const pts = [new Vector3(0, 3.2, 0), new Vector3(0, 1.1, 0), new Vector3(0, 0.5, 0.004), new Vector3(0, 0.32, 0.02), new Vector3(0, 0.18, D * 0.92), new Vector3(0, CY + 0.04, D)];
  for (let i = 0; i <= 16; i++) { const a = (i / 16) * Math.PI; pts.push(new Vector3(0, CY - D * Math.sin(a), D * Math.cos(a))); }
  pts.push(new Vector3(0, CY + 0.05, -D), new Vector3(0, CY + 0.075, -D * 0.9));
  const hookGeo = new TubeGeometry(new CatmullRomCurve3(pts, false, 'centripetal'), 360, WR, 14, false);
  const hook = new Mesh(hookGeo, new MeshStandardMaterial({ color: 0xc4c1c8, metalness: 1, roughness: 0.3 }));
  pivot.add(hook);

  /* ---------- etiqueta ---------- */
  const lab = document.createElement('canvas'); const lctx = lab.getContext('2d');
  const labTex = new CanvasTexture(lab); labTex.colorSpace = SRGBColorSpace; labTex.anisotropy = aniso;
  const labMat = new MeshStandardMaterial({ map: labTex, roughness: 0.75, metalness: 0, polygonOffset: true, polygonOffsetFactor: -2 });
  const label = new Mesh(new PlaneGeometry(1, 1), labMat);
  plate.add(label);
  let lastText = '';
  /* Lienzo de tamaño fijo: la textura no cambia de tamaño (WebGL2 reserva su memoria una vez). */
  const LW = 1024, LH = 84, LHW = 0.062;
  lab.width = LW; lab.height = LH;
  labMat.transparent = true;
  label.scale.set(LHW * LW / LH, LHW, 1);
  label.position.set(x0 + 0.08 + (LHW * LW / LH) / 2, y0 + 0.2, T / 2 + 0.0012);
  function drawLabel(text) {
    if (text === lastText) return; lastText = text;
    const padX = 24; let fs = 44;
    const setFont = function () { lctx.font = '600 ' + fs + 'px Archivo, "Helvetica Neue", Arial, sans-serif'; if ('letterSpacing' in lctx) lctx.letterSpacing = '3px'; };
    setFont();
    let tw = lctx.measureText(text).width;
    const maxW = Math.min(LW, (W - 0.16) / LHW * LH) - padX * 2;
    if (tw > maxW) { fs = Math.floor(fs * maxW / tw); setFont(); tw = lctx.measureText(text).width; }
    lctx.clearRect(0, 0, LW, LH);
    lctx.fillStyle = '#FFFFFF'; lctx.fillRect(0, 0, Math.ceil(tw) + padX * 2, LH);
    lctx.fillStyle = '#1A1A1A'; lctx.textBaseline = 'middle'; lctx.fillText(text, padX, LH / 2 + 2);
    labTex.needsUpdate = true;
  }

  /* ---------- estado ---------- */
  const cur = { hex: '#F7B500', tex: 'lisa', gloss: 'satinado', pearl: false, lum: false };
  function apply() {
    const tx = cur.tex === 'texturada';
    const g = (tx ? TEXTURED : GLOSS)[cur.gloss] || GLOSS.satinado;
    mat.color.set(cur.hex);
    mat.roughness = g.roughness * (cur.pearl ? 0.8 : 1);
    mat.metalness = cur.pearl ? 0.45 : 0;
    mat.specularIntensity = g.spec;
    mat.clearcoat = g.cc; mat.clearcoatRoughness = g.ccr;
    mat.iridescence = cur.pearl ? 0.35 : 0; mat.iridescenceIOR = 1.45; mat.iridescenceThicknessRange = [180, 420];
    mat.emissive.set(cur.lum ? cur.hex : '#000000'); mat.emissiveIntensity = cur.lum ? 0.22 : 0;
    if (tx) {
      mat.normalMap = sandTex; mat.normalScale.set(1.1, 1.1);
      mat.clearcoatNormalMap = g.cc ? sandTex : null; mat.clearcoatNormalScale.set(0.55, 0.55);
    } else {
      const pe = GLOSS[cur.gloss].peel;
      mat.normalMap = pe ? peelTex : null; mat.normalScale.set(pe, pe);
      mat.clearcoatNormalMap = g.cc && pe ? peelTex : null; mat.clearcoatNormalScale.set(pe * 0.7, pe * 0.7);
    }
    mat.needsUpdate = true;
    dirty = true;
  }

  /* ---------- tamaño ---------- */
  function resize() {
    const w = host.clientWidth || 400, h = Math.round(w * 470 / 440);
    renderer.setSize(w, h, false);
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    camera.aspect = w / h; camera.updateProjectionMatrix();
    dirty = true;
  }
  let ro = null;
  if (window.ResizeObserver) { ro = new ResizeObserver(resize); ro.observe(host); } else window.addEventListener('resize', resize);
  resize();

  /* ---------- movimiento: vaivén lento y respuesta al puntero ---------- */
  const BASE = opts.yaw != null ? opts.yaw : 0.34, AMP = 0.2, PERIOD = 9;
  let yaw = BASE, target = BASE, pointer = null, visible = true, raf = 0;
  const t0 = performance.now();
  canvas.addEventListener('pointermove', function (e) {
    const r = canvas.getBoundingClientRect();
    pointer = MathUtils.clamp((e.clientX - r.left) / r.width, 0, 1);
    if (reduce) { target = BASE + (pointer - 0.5) * 1.1; kick(); }
  });
  canvas.addEventListener('pointerleave', function () { pointer = null; if (reduce) { target = BASE; kick(); } });

  function frame(now) {
    raf = 0;
    const t = (now - t0) / 1000;
    if (!reduce) target = pointer == null ? BASE + AMP * Math.sin(t * 2 * Math.PI / PERIOD) : BASE + (pointer - 0.5) * 1.1;
    const prev = yaw;
    yaw += (target - yaw) * (pointer == null ? 0.06 : 0.12);
    pivot.rotation.y = yaw;
    pivot.rotation.z = reduce ? 0 : Math.sin(t * 2 * Math.PI / (PERIOD * 1.37)) * 0.012;
    if (dirty || Math.abs(yaw - prev) > 1e-5 || !reduce) { renderer.render(scene, camera); dirty = false; }
    if (visible && !document.hidden && (!reduce || Math.abs(target - yaw) > 1e-4)) raf = requestAnimationFrame(frame);
  }
  function kick() { if (!raf) raf = requestAnimationFrame(frame); }

  if (window.IntersectionObserver) {
    new IntersectionObserver(function (es) { visible = es.some(function (e) { return e.isIntersecting; }); if (visible) kick(); }, { rootMargin: '120px 0px' }).observe(host);
  }
  document.addEventListener('visibilitychange', function () { if (!document.hidden) kick(); });

  apply();
  kick();

  return {
    canvas,
    update(p) {
      Object.assign(cur, p || {});
      if (p && p.label) canvas.setAttribute('aria-label', p.label);
      if (p && p.sticker) {
        const run = function () { drawLabel(p.sticker); dirty = true; kick(); };
        if (document.fonts && document.fonts.load) document.fonts.load('600 44px Archivo').then(run, run); else run();
      }
      apply(); kick();
    },
    render() { renderer.render(scene, camera); }
  };
}

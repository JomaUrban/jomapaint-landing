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
  BackSide, Float32BufferAttribute, SpotLight, EquirectangularReflectionMapping
} from 'three';
import { HDRLoader } from 'three/examples/jsm/loaders/HDRLoader.js';

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
   Nave real (HDRI) o sala gris, una fila de regletas LED inclinadas (como un túnel
   de inspección de pintura) y dos rellenos. Al moverse la placa y la luz, las regletas
   cruzan la placa en diagonal: líneas nítidas en brillo, brillo difuso en satinado,
   nada en mate. */
function studio(hdr, hdrScale) {
  const env = new Scene();
  if (hdr) {
    // Nave real (HDRI de Poly Haven, CC0), casi en gris para no teñir el color RAL.
    const k = hdrScale || 1;
    env.add(new Mesh(new SphereGeometry(20, 64, 32), new MeshBasicMaterial({ map: hdr, color: new Color(k, k, k), side: BackSide })));
  }
  const sg = new SphereGeometry(20, 48, 24), pos = sg.attributes.position, col = [];
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i) / 20, v = y > 0 ? 0.42 + 0.33 * y : 0.42 + 0.34 * y; // techo claro, suelo oscuro
    col.push(v, v, v * 1.01);
  }
  sg.setAttribute('color', new Float32BufferAttribute(col, 3));
  if (!hdr) env.add(new Mesh(sg, new MeshBasicMaterial({ side: BackSide, vertexColors: true })));
  function place(m, az, el, r, roll) {
    const a = az * Math.PI / 180, e = el * Math.PI / 180;
    m.position.set(Math.sin(a) * Math.cos(e) * r, Math.sin(e) * r, Math.cos(a) * Math.cos(e) * r);
    m.lookAt(0, 0, 0); if (roll) m.rotateZ(roll * Math.PI / 180); env.add(m);
  }
  /* Luz industrial: tres regletas LED largas e inclinadas, como las de una cabina de
     inspección de pintura. En brillo se ven como líneas nítidas que cruzan la placa. */
  const stripCanvas = document.createElement('canvas'); stripCanvas.width = 64; stripCanvas.height = 8;
  const sg2 = stripCanvas.getContext('2d'), grd = sg2.createLinearGradient(0, 0, 64, 0);
  grd.addColorStop(0, 'rgba(255,255,255,0)'); grd.addColorStop(0.3, 'rgba(255,255,255,0.9)'); grd.addColorStop(0.5, 'rgba(255,255,255,1)');
  grd.addColorStop(0.7, 'rgba(255,255,255,0.9)'); grd.addColorStop(1, 'rgba(255,255,255,0)');
  sg2.fillStyle = grd; sg2.fillRect(0, 0, 64, 8);
  const stripTex = new CanvasTexture(stripCanvas); stripTex.colorSpace = SRGBColorSpace;
  // [azimut, ancho, intensidad]: separación irregular para que no parezca una cebra
  [[-2, 0.32, 0.8], [9, 0.22, 0.65], [21, 0.36, 1], [33, 0.26, 0.85], [42, 0.2, 0.6], [53, 0.34, 0.95], [66, 0.24, 0.7], [78, 0.3, 0.8]].forEach(function (a) {
    const k = 5.2 * a[2];
    const m = new Mesh(new PlaneGeometry(a[1], 13), new MeshBasicMaterial({ map: stripTex, color: new Color(k, k * 0.985, k * 0.96), transparent: true, depthWrite: false, side: 2 }));
    place(m, a[0], 8, 14, -20);
  });
  const fill = new Mesh(new PlaneGeometry(3.2, 9), new MeshBasicMaterial({ color: new Color(2.4, 2.4, 2.45), side: 2 }));
  place(fill, -24, 10, 14); // relleno, frente-izquierda
  const top = new Mesh(new PlaneGeometry(9, 5), new MeshBasicMaterial({ color: new Color(3, 3, 3), side: 2 }));
  place(top, 10, 62, 14);  // cenital
  return env;
}

/* ---------- acabados ---------- */
// roughness: rugosidad de la capa; cc: barniz (clearcoat) y su rugosidad; spec: intensidad especular.
const GLOSS = {
  mate: { roughness: 0.93, cc: 0, ccr: 0.6, spec: 0.4, peel: 0.0 },
  satinado: { roughness: 0.12, cc: 0, ccr: 0.3, spec: 0.6, peel: 0 },
  brillante: { roughness: 0.5, cc: 1, ccr: 0.03, spec: 0.3, peel: 0 }
};
const TEXTURED = {
  mate: { roughness: 0.95, cc: 0, ccr: 0.6, spec: 0.5 },
  satinado: { roughness: 0.62, cc: 0.15, ccr: 0.45, spec: 0.8 },
  brillante: { roughness: 0.45, cc: 0.4, ccr: 0.2, spec: 0.6 }
};

export function init(host, opts) {
  opts = opts || {};
  const reduce = !!opts.reduce;
  let dirty = true;
  const field = host.closest ? host.closest('.ral-field') : null;
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
  renderer.shadowMap.enabled = true;
  const aniso = renderer.capabilities.getMaxAnisotropy();

  const scene = new Scene();
  const pmrem = new PMREMGenerator(renderer);
  /* Reflejos: el estudio provisional a 256; el definitivo (con la nave) a 512, para que las
     regletas se reflejen nítidas en el brillo sin escalones. */
  let envRT = pmrem.fromScene(studio(), 0, 0.1, 100, { size: 256 });
  scene.environment = envRT.texture;
  scene.environmentIntensity = 1;
  /* Entorno real: HDRI de estudio (Poly Haven, CC0). Mientras carga, el estudio procedural. */
  let envBase = -0.32, envSweep = 0.36;
  if (opts.env) {
    pmrem.compileEquirectangularShader();
    new HDRLoader().load(opts.env, function (tex) {
      const rt = pmrem.fromScene(studio(tex, opts.envScale), 0, 0.1, 100, { size: 512 });
      scene.environment = rt.texture; envRT.dispose(); envRT = rt;
      tex.dispose(); pmrem.dispose();
      if (opts.envIntensity != null) scene.environmentIntensity = opts.envIntensity;
      if (opts.envYaw != null) envBase = opts.envYaw;
      if (opts.envSweep != null) envSweep = opts.envSweep;
      setSun(lastSun); dirty = true; kick();
    }, undefined, function () { pmrem.dispose(); });
  } else pmrem.dispose();

  const key = new DirectionalLight(0xffffff, 0.45);
  key.position.set(-2.5, 3, 4);
  scene.add(key);

  /* Haz de luz: foco cálido y suave con una máscara (cookie) en banda diagonal, como
     la luz que entra por un lucernario de nave. Cruza la placa despacio; el gancho deja
     su sombra. La banda se dibuja con un degradado (sin filtro de desenfoque: el blur
     del canvas deja dientes de sierra en algunos navegadores). Para usar la máscara
     (.map) el foco tiene que proyectar sombras. */
  const cookie = new CanvasTexture((function () {
    const c = document.createElement('canvas'); c.width = c.height = 512;
    const g = c.getContext('2d');
    const a = -24 * Math.PI / 180, dx = Math.cos(a) * 256, dy = Math.sin(a) * 256;
    const gr = g.createLinearGradient(256 - dx, 256 - dy, 256 + dx, 256 + dy);
    gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(0.36, 'rgba(255,255,255,0)');
    gr.addColorStop(0.46, 'rgba(255,255,255,0.85)'); gr.addColorStop(0.5, 'rgba(255,255,255,1)');
    gr.addColorStop(0.56, 'rgba(255,255,255,0.85)'); gr.addColorStop(0.68, 'rgba(255,255,255,0)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 512, 512);
    return c;
  })());
  cookie.colorSpace = SRGBColorSpace;
  const sun = new SpotLight(0xfff0e0, 0.65, 0, 0.16, 0.4, 0);
  sun.position.set(-3.6, 3.1, 4.4);
  sun.map = cookie;
  sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024);
  sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.01;
  sun.shadow.camera.near = 2; sun.shadow.camera.far = 14;
  scene.add(sun, sun.target);

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
  plate.receiveShadow = true; // solo el gancho proyecta sombra (la placa sobre sí misma daría dientes de sierra)

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
  hook.castShadow = true;
  pivot.add(hook);

  /* ---------- etiqueta ---------- */
  const lab = document.createElement('canvas'); const lctx = lab.getContext('2d');
  const labTex = new CanvasTexture(lab); labTex.colorSpace = SRGBColorSpace; labTex.anisotropy = aniso;
  const labMat = new MeshStandardMaterial({ map: labTex, roughness: 0.75, metalness: 0, polygonOffset: true, polygonOffsetFactor: -2 });
  const label = new Mesh(new PlaneGeometry(1, 1), labMat);
  label.receiveShadow = true;
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
      mat.clearcoatNormalMap = g.cc ? sandTex : null; mat.clearcoatNormalScale.set(0.35, 0.35);
    } else {
      const pe = GLOSS[cur.gloss].peel;
      mat.normalMap = pe ? peelTex : null; mat.normalScale.set(pe, pe);
      mat.clearcoatNormalMap = g.cc && pe ? peelTex : null; mat.clearcoatNormalScale.set(pe * 0.7, pe * 0.7);
    }
    /* El sol de ventana (foco y haces del fondo) solo en brillo: ahí es donde se ve. */
    const shine = cur.gloss === 'brillante';
    sun.visible = shine; key.intensity = shine ? 0.68 : 0.8;
    if (field) field.classList.toggle('ral-sunlit', shine);
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
  const BASE = opts.yaw != null ? opts.yaw : 0.34, AMP = 0.14, PERIOD = 9, SUN = 13;
  let beam = null;
  if (field) { beam = document.createElement('div'); beam.className = 'ral-sun'; beam.setAttribute('aria-hidden', 'true'); field.insertBefore(beam, field.firstChild); }
  let lastSun = 0.42;
  function setSun(p) {
    lastSun = p;
    sun.target.position.set(-1.05 + 2.1 * p, 0.12, 0);
    scene.environmentRotation.y = envBase + envSweep * (p - 0.5);
    if (field) field.style.setProperty('--sun', p.toFixed(4));
  }
  setSun(opts.sun != null ? opts.sun : 0.42);
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
    if (!reduce && opts.sun == null) setSun(0.5 - 0.5 * Math.cos(t * 2 * Math.PI / SUN));
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
    render() { renderer.render(scene, camera); },
    sun(p) { setSun(p); dirty = true; kick(); },
    env(base, sweep, intensity) { if (base != null) envBase = base; if (sweep != null) envSweep = sweep; if (intensity != null) scene.environmentIntensity = intensity; setSun(lastSun); dirty = true; kick(); },
    light(k, s) { if (k != null) key.intensity = k; if (s != null) sun.intensity = s; dirty = true; kick(); }
  };
}

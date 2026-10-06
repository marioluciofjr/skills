/*!
 * motion-core.js — palco, linha do tempo mestre e primitivas de animação.
 * Depende de: gsap (global). Lê: window.MOTION_CONFIG.
 * Exporta: window.Motion  (outros módulos se plugam em Motion.chrome, Motion.brand, Motion.recipes)
 * Contrato com o renderizador: window.__tl = linha do tempo mestre (uma iteração = T.duration()).
 */
(function (global) {
  'use strict';
  var gsap = global.gsap;
  var cfg = global.MOTION_CONFIG || {};
  var W = cfg.width || 1920;
  var H = cfg.height || 1080;
  var stage = document.getElementById('stage');
  var composers = [];

  /* ---------- utilitários de DOM ---------- */
  function $(q, root) { return (root || document).querySelector(q); }
  function $$(q, root) { return Array.prototype.slice.call((root || document).querySelectorAll(q)); }
  function el(x) { return typeof x === 'string' ? $(x) : x; }
  function make(tag, cls, parent) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    (parent || stage).appendChild(n);
    return n;
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fmt(v, d) {
    d = d || 0;
    return Number(v).toLocaleString(cfg.locale || 'pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
  }

  /* posição de layout no palco (ignora transforms — seguro para calcular alvos antes das animações) */
  function layoutPos(node) {
    var x = 0, y = 0, n = node;
    while (n && n !== stage) { x += n.offsetLeft; y += n.offsetTop; n = n.offsetParent; }
    return { x: x, y: y, w: node.offsetWidth, h: node.offsetHeight, cx: x + node.offsetWidth / 2, cy: y + node.offsetHeight / 2 };
  }
  /* retângulo visual no palco (inclui transforms — usar em tempo de execução) */
  function rectInStage(node) {
    var sr = stage.getBoundingClientRect(), s = sr.width / W, r = node.getBoundingClientRect();
    return { x: (r.left - sr.left) / s, y: (r.top - sr.top) / s, w: r.width / s, h: r.height / s };
  }

  function fit() {
    var s = Math.min(global.innerWidth / W, global.innerHeight / H);
    stage.style.transform = 'translate(-50%,-50%) scale(' + s + ')';
  }

  /* data-split: "|" quebra linha; data-dim-first="N" esmaece as N primeiras palavras */
  function splitWords(root) {
    $$('[data-split]', root).forEach(function (node) {
      if (node.dataset.splitDone) return;
      var dim = parseInt(node.dataset.dimFirst || '0', 10), i = 0;
      node.innerHTML = node.textContent.trim().split('|').map(function (line) {
        return line.trim().split(/\s+/).map(function (w) {
          return '<span class="w' + (i++ < dim ? ' dim' : '') + '"><span>' + esc(w) + '</span></span>';
        }).join(' ');
      }).join('<br>');
      node.dataset.splitDone = '1';
    });
  }

  /* ---------- linha do tempo mestre ---------- */
  var T = gsap.timeline({ repeat: cfg.loop === false ? 0 : -1, paused: true });

  /* ---------- sobreposições globais ---------- */
  var sweeps = [0, 1, 2, 3].map(function () { return make('div', 'sweep'); });
  var ripple = make('div', 'ripple');
  var cursor = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  cursor.setAttribute('class', 'cursor');
  cursor.setAttribute('viewBox', '0 0 40 40');
  cursor.innerHTML = '<path d="M6 3l26 14-11.5 3L15 31z" fill="#fff" stroke="#000" stroke-width="2" stroke-linejoin="round"/>';
  stage.appendChild(cursor);

  /* ---------- echo trail ---------- */
  var ECHO_KEYS = ['x', 'y', 'scale', 'rotation', 'xPercent', 'yPercent', 'filter', 'duration', 'ease'];
  var ECHO_ALPHA = [0.55, 0.34, 0.2, 0.1];
  function echo(node, vars, n) {
    n = n || 4;
    var op = parseFloat(global.getComputedStyle(node).opacity) || 1;
    for (var i = 1; i <= n; i++) {
      var c = node.cloneNode(true);
      c.removeAttribute('id');
      $$('[id]', c).forEach(function (x) { x.removeAttribute('id'); });
      c.classList.add('echo-ghost');
      node.parentNode.insertBefore(c, node);
      gsap.set(c, { opacity: op * ECHO_ALPHA[i - 1] });
      var v = {};  /* copia só chaves seguras: o gsap anexa estado interno ao objeto vars original */
      ECHO_KEYS.forEach(function (k) { if (k in vars) v[k] = vars[k]; });
      v.opacity = 0;
      v.delay = i * 0.05;
      v.onComplete = (function (ghost) { return function () { ghost.remove(); }; })(c);
      gsap.to(c, v);
    }
  }
  function echoTo(target, vars, t) {
    var node = el(target);
    T.call(function () { echo(node, vars); }, null, t);
    T.to(node, Object.assign({}, vars), t);
    return t + (vars.duration || 0);
  }

  /* ---------- transições ---------- */
  function sweep(t, dir) {
    dir = dir || 1;
    T.fromTo(sweeps, { x: dir > 0 ? -60 : W + 60, opacity: function (i) { return [0.9, 0.45, 0.22, 0.1][i]; } },
      { x: dir > 0 ? W + 60 : -60, duration: 0.55, ease: 'power2.inOut', stagger: 0.035 }, t);
    T.set(sweeps, { opacity: 0 }, t + 0.7);
  }
  function sceneIn(sel, t) {
    T.fromTo(sel, { autoAlpha: 0, x: 180, filter: 'blur(18px)' },
      { autoAlpha: 1, x: 0, filter: 'blur(0px)', duration: 0.65, ease: 'expo.out' }, t);
    sweep(t - 0.12);
    return t + 0.65;
  }
  function outVars() { return { x: -220, autoAlpha: 0, filter: 'blur(16px)', duration: 0.45, ease: 'power3.in' }; }
  function sceneOut(sel, t) { return echoTo(el(sel), outVars(), t); }

  /* ---------- texto ---------- */
  function words(sel, t, stagger) {
    var spans = $$(sel + ' .w>span');
    if (!spans.length) return t;
    T.fromTo(spans, { yPercent: 115, rotate: 5 },
      { yPercent: 0, rotate: 0, duration: 0.85, ease: 'expo.out', stagger: stagger || 0.07 }, t);
    return t + 0.85 + (spans.length - 1) * (stagger || 0.07);
  }
  function eyebrowIn(scope, t) {
    T.fromTo(scope + ' .eyebrow', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.6, ease: 'power3.out' }, t);
    T.fromTo(scope + ' .eyebrow i', { scaleX: 0 }, { scaleX: 1, transformOrigin: 'left', duration: 0.6, ease: 'power3.out' }, t + 0.1);
  }
  function subIn(scope, t) {
    T.fromTo(scope + ' .sub', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, t);
  }
  /* bloco padrão de cabeçalho: eyebrow + headline palavra por palavra + subtítulo */
  function headIn(scope, t) {
    if ($(scope + ' .eyebrow')) eyebrowIn(scope, t + 0.1);
    words(scope + ' .h', t + 0.15);
    if ($(scope + ' .sub')) subIn(scope, t + 0.7);
  }

  /* ---------- números e digitação ---------- */
  function count(target, to, t, dur, dec) {
    var node = el(target), o = { v: 0 };
    dec = dec || 0;
    T.call(function () { node.textContent = fmt(0, dec); }, null, Math.max(0, t - 0.01));
    T.to(o, { v: to, duration: dur || 1.4, ease: 'power3.out',
      onStart: function () { o.v = 0; },
      onUpdate: function () { node.textContent = fmt(o.v, dec); } }, t);
  }
  /* conta todos os [data-n] (decimais em data-dec) dentro do escopo */
  function countAll(scope, t, dur, stagger) {
    $$(scope + ' [data-n]').forEach(function (n, i) {
      count(n, parseFloat(n.dataset.n), t + i * (stagger || 0), dur, parseInt(n.dataset.dec || '0', 10));
    });
  }
  function type(target, text, t, dur) {
    var node = el(target);
    T.call(function () { node.textContent = ''; }, null, Math.max(0, t - 0.01));
    T.to({}, { duration: dur || 0.6, ease: 'none', onUpdate: function () {
      node.textContent = text.slice(0, Math.round(this.progress() * text.length));
    } }, t);
    return t + (dur || 0.6);
  }

  /* ---------- cursor ---------- */
  function cursorPath(points, t) {
    T.set(cursor, { autoAlpha: 1, scale: 1, x: points[0][0], y: points[0][1] }, t);
    var tt = t;
    for (var i = 1; i < points.length; i++) {
      T.to(cursor, { x: points[i][0], y: points[i][1], duration: 0.55, ease: 'power3.inOut' }, tt);
      tt += 0.55;
    }
    return tt;
  }
  function click(x, y, t) {
    T.to(cursor, { scale: 0.82, duration: 0.08, yoyo: true, repeat: 1, transformOrigin: '15% 10%' }, t);
    T.fromTo(ripple, { left: x, top: y, scale: 0.2, opacity: 0.9 }, { scale: 1.4, opacity: 0, duration: 0.5, ease: 'power2.out' }, t);
    return t + 0.2;
  }
  function cursorOut(t) {
    T.to(cursor, { x: W - 20, y: H * 0.62, autoAlpha: 0, duration: 0.5, ease: 'power2.in' }, t);
  }
  /* move o cursor até o centro de um elemento, clica e devolve o instante do clique */
  function clickOn(target, t, from) {
    var p = layoutPos(el(target));
    var tc = cursorPath([from || [W - 220, H - 80], [p.cx, p.cy]], t);
    click(p.cx + 6, p.cy + 6, tc);
    return tc;
  }

  /* ---------- ciclo de vida ---------- */
  function compose(fn) { composers.push(fn); }
  function ready() {
    var imgs = $$('img', stage).map(function (i) { return i.decode ? i.decode().catch(function () {}) : null; });
    var fonts = document.fonts ? document.fonts.ready : Promise.resolve();
    return Promise.all(imgs.concat([fonts]));
  }
  function start() {
    fit();
    global.addEventListener('resize', fit);
    splitWords();
    ready().then(function () {
      composers.forEach(function (fn) { fn(api); });
      T.play(0);
    });
    global.addEventListener('keydown', function (e) {
      if (e.code === 'Space') { e.preventDefault(); T.paused(!T.paused()); }
    });
  }

  var api = {
    T: T, W: W, H: H, cfg: cfg, stage: stage, gsap: gsap,
    $: $, $$: $$, el: el, make: make, fmt: fmt, layoutPos: layoutPos, rectInStage: rectInStage, splitWords: splitWords,
    echo: echo, echoTo: echoTo, sweep: sweep, sceneIn: sceneIn, sceneOut: sceneOut, outVars: outVars,
    words: words, eyebrowIn: eyebrowIn, subIn: subIn, headIn: headIn,
    count: count, countAll: countAll, type: type,
    cursor: cursor, cursorPath: cursorPath, click: click, clickOn: clickOn, cursorOut: cursorOut,
    compose: compose, start: start
  };
  global.Motion = api;
  global.__tl = T;
})(window);

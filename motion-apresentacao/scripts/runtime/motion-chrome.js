/*!
 * motion-chrome.js — moldura de "app": cabeçalho (marca + título) e barra de progresso por seção.
 * Depende de: Motion (motion-core.js). Lê: MOTION_CONFIG.chrome e MOTION_CONFIG.brand (ícone).
 * Exporta: Motion.chrome = { in(t), out(t), progress(i, tStart, tEnd) }
 * Sem config.chrome, exporta funções vazias (as cenas continuam funcionando).
 */
(function (global) {
  'use strict';
  var M = global.Motion, cfg = M.cfg, c = cfg.chrome, b = cfg.brand || {};
  var noop = function () {};
  if (!c) { M.chrome = { in: noop, out: noop, progress: noop }; return; }

  var root = M.make('div', 'chrome');
  var top = M.make('div', 'chrome-top', root);
  var brand = M.make('div', 'chrome-brand', top);
  if (b.logo) {
    /* recorta só o símbolo do logo (0 .. mark_end) */
    var aspect = b.aspect || 4, markEnd = b.mark_end || 1, h = 26;
    var icon = M.make('div', 'chrome-icon', brand);
    icon.style.width = (h * aspect * markEnd) + 'px';
    var img = M.make('img', '', icon);
    img.src = b.logo; img.alt = '';
    img.style.width = (h * aspect) + 'px';
  }
  M.make('span', '', brand).textContent = c.left || b.name || '';
  M.make('div', '', top).textContent = c.right || '';

  var sections = c.sections || [];
  var prog = M.make('div', 'chrome-prog', root);
  prog.style.gridTemplateColumns = 'repeat(' + Math.max(1, sections.length) + ',1fr)';
  var fills = [], labels = [];
  sections.forEach(function (name) {
    var seg = M.make('div', 'chrome-seg', prog);
    var tr = M.make('div', 'tr', seg);
    fills.push(M.make('i', '', tr));
    var lb = M.make('span', '', seg);
    lb.textContent = name;
    labels.push(lb);
  });

  var T = M.T, OFF = '#4a4a4a', ON = getComputedStyle(document.documentElement).getPropertyValue('--fg').trim() || '#fff';
  T.set(root, { autoAlpha: 0 }, 0);
  if (fills.length) { T.set(fills, { scaleX: 0 }, 0); T.set(labels, { color: OFF }, 0); }

  M.chrome = {
    in: function (t) { T.fromTo(root, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.6 }, t); },
    out: function (t) { T.to(root, { autoAlpha: 0, duration: 0.4 }, t); },
    progress: function (i, a, z) {
      if (!fills[i]) return;
      T.fromTo(fills[i], { scaleX: 0 }, { scaleX: 1, duration: z - a, ease: 'none' }, a);
      T.to(labels[i], { color: ON, duration: 0.3 }, a);
      T.to(labels[i], { color: OFF, duration: 0.3 }, z);
    }
  };
})(window);

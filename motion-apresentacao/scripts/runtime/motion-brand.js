/*!
 * motion-brand.js — abertura com logo e encerramento "elementos formam o logo" + tagline.
 * Depende de: Motion (motion-core.js), MotionParticles (motion-particles.js).
 * Lê: MOTION_CONFIG.brand = { logo, aspect, mark_end, word_start, tagline, tagline_dim, url, intro:{kicker,title,meta}, lockup_width }
 * Exporta: Motion.brand = { intro(t) -> instante em que a 1ª cena deve entrar,
 *                           outro(t, { sources, hide, hold }) -> instante final do filme }
 *
 * Geometria: o logo inteiro (símbolo + nome) fica centrado em (W/2, 43,5% de H).
 * O símbolo é a faixa 0..mark_end da imagem; o nome é a faixa word_start..1.
 */
(function (global) {
  'use strict';
  var M = global.Motion, P = global.MotionParticles, T = M.T, W = M.W, H = M.H;
  var b = M.cfg.brand || {};
  var noop = function (t) { return t; };
  if (!b.logo) { M.brand = { intro: noop, outro: noop }; return; }

  var aspect = b.aspect || 4;
  var markEnd = b.mark_end == null ? 1 : b.mark_end;
  var wordStart = b.word_start == null ? 1 : b.word_start;
  var hasWord = wordStart < 1;
  var lockW = b.lockup_width || Math.min(W * 0.52, 1000);
  var lockH = lockW / aspect;
  var left = (W - lockW) / 2, top = H * 0.435 - lockH / 2;
  var origin = (markEnd / 2 * 100) + '% 50%';
  /* estado "grande": símbolo centrado no palco com 52% da altura */
  var bigScale = (H * 0.52) / lockH;
  var bigX = W / 2 - (left + markEnd / 2 * lockW);
  var bigY = H / 2 - (top + lockH / 2);
  var CLIP_MARK = 'inset(0% ' + ((1 - markEnd) * 100) + '% 0% 0%)';
  var CLIP_WORD_HIDDEN = 'inset(0% ' + ((1 - wordStart) * 100) + '% 0% ' + (wordStart * 100) + '%)';
  var CLIP_WORD_SHOWN = 'inset(0% 0% 0% ' + (wordStart * 100) + '%)';

  /* ---------- DOM ---------- */
  var canvas = M.make('canvas', 'fx-canvas');
  canvas.width = W; canvas.height = H;

  var lock = M.make('div', 'lock');
  Object.assign(lock.style, { left: left + 'px', top: top + 'px', width: lockW + 'px', height: lockH + 'px' });
  var mark = M.make('img', 'lock-mark', lock);
  mark.src = b.logo; mark.alt = b.name || '';
  mark.style.clipPath = CLIP_MARK; mark.style.transformOrigin = origin;
  var word = null;
  if (hasWord) {
    word = M.make('img', 'lock-word', lock);
    word.src = b.logo; word.alt = '';
    word.style.clipPath = CLIP_WORD_HIDDEN;
  }

  var intro = M.make('div', 'scene brand-intro');
  var line = M.make('div', 'brand-line', intro);
  line.style.top = (top + lockH / 2 - 1) + 'px';
  var cap = null;
  if (b.intro) {
    cap = M.make('div', 'brand-cap', intro);
    cap.style.top = (top + lockH + 70) + 'px';
    if (b.intro.kicker) M.make('div', 'k', cap).textContent = b.intro.kicker;
    if (b.intro.title) { var tt = M.make('div', 't', cap); tt.textContent = b.intro.title; tt.setAttribute('data-split', ''); }
    if (b.intro.meta) M.make('div', 'm', cap).textContent = b.intro.meta;
  }

  var tag = M.make('div', 'tagline');
  tag.style.top = (top + lockH + 70) + 'px';
  if (b.tagline) {
    var tl = M.make('div', 'tl', tag);
    tl.textContent = b.tagline; tl.setAttribute('data-split', '');
    if (b.tagline_dim) tl.setAttribute('data-dim-first', String(b.tagline_dim));
  }
  if (b.url) M.make('div', 'url', tag).textContent = b.url;

  var field = P.create({
    canvas: canvas, image: mark, src: { fx: 0, fy: 0, fw: markEnd, fh: 1 },
    dest: { x: W / 2 - markEnd * lockW * bigScale / 2, y: H / 2 - lockH * bigScale / 2, w: markEnd * lockW * bigScale, h: lockH * bigScale },
    step: b.particle_step || 6
  });

  /* ---------- estados iniciais (início de cada volta do loop) ---------- */
  T.set(canvas, { opacity: 0 }, 0);
  T.call(field.clear, null, 0.02);
  T.set(tag, { autoAlpha: 0, filter: 'blur(0px)' }, 0);

  /* ---------- abertura ---------- */
  function introSeq(t0) {
    T.set(intro, { autoAlpha: 1, x: 0, filter: 'blur(0px)' }, t0);
    T.set(lock, { autoAlpha: 1, x: 0, y: 0, filter: 'blur(0px)' }, t0);
    if (word) T.set(word, { clipPath: CLIP_WORD_HIDDEN }, t0);
    T.fromTo(line, { scaleX: 0, transformOrigin: 'left center' }, { scaleX: 1, duration: 0.55, ease: 'power3.inOut' }, t0 + 0.05);
    T.fromTo(line, { scaleX: 1, transformOrigin: 'right center' }, { scaleX: 0, duration: 0.45, ease: 'power3.in' }, t0 + 0.6);
    T.fromTo(mark, { opacity: 0, scale: 0.25, rotation: -140, x: 0, y: 0, filter: 'blur(20px)' },
      { opacity: 1, scale: 1, rotation: 0, filter: 'blur(0px)', duration: 1.1, ease: 'expo.out' }, t0 + 0.85);
    if (word) T.fromTo(word, { clipPath: CLIP_WORD_HIDDEN }, { clipPath: CLIP_WORD_SHOWN, duration: 0.85, ease: 'expo.inOut' }, t0 + 1.15);
    if (cap) {
      T.fromTo(M.$$('.k, .m', cap), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.6, stagger: 0.35, ease: 'power3.out' }, t0 + 1.55);
      T.fromTo(M.$$('.t .w>span', cap), { yPercent: 115, rotate: 5 },
        { yPercent: 0, rotate: 0, duration: 0.85, ease: 'expo.out', stagger: 0.05 }, t0 + 1.7);
    }
    M.echoTo(lock, { y: -160, autoAlpha: 0, filter: 'blur(14px)', duration: 0.45, ease: 'power3.in' }, t0 + 2.7);
    M.echoTo(intro, M.outVars(), t0 + 2.72);
    return t0 + 2.95;
  }

  /* ---------- encerramento ----------
     opts.sources: função que devolve os elementos de onde as partículas nascem (ex.: barras da última cena)
     opts.hide:    seletor escondido no instante em que as partículas assumem
     opts.hold:    segundos extras com logo + tagline antes do fade (padrão 0)
     opts.fade:    false para terminar congelado no logo (sem fade para preto) */
  function outroSeq(t0, opts) {
    opts = opts || {};
    T.set(canvas, { opacity: 1 }, t0 - 0.02);
    T.call(function () {
      var els = opts.sources ? opts.sources() : [];
      field.prepare(els.map(M.rectInStage));
      if (opts.hide) M.gsap.set(opts.hide, { autoAlpha: 0 });
    }, null, t0);
    var po = { p: 0 };
    T.fromTo(po, { p: 0 }, { p: 1, duration: 2.2, ease: 'none', onUpdate: function () { field.draw(po.p); } }, t0 + 0.02);

    T.set(lock, { autoAlpha: 1, x: 0, y: 0, filter: 'blur(0px)' }, t0);
    T.set(mark, { opacity: 0, scale: bigScale, x: bigX, y: bigY, rotation: 0, filter: 'blur(0px)' }, t0);
    if (word) T.set(word, { clipPath: CLIP_WORD_HIDDEN }, t0);
    T.to(mark, { opacity: 1, duration: 0.4, ease: 'power2.out' }, t0 + 2.15);
    T.to(canvas, { opacity: 0, duration: 0.5 }, t0 + 2.25);
    M.echoTo(mark, { scale: 1, x: 0, y: 0, duration: 0.95, ease: 'expo.inOut' }, t0 + 2.65);
    if (word) T.to(word, { clipPath: CLIP_WORD_SHOWN, duration: 0.85, ease: 'expo.inOut' }, t0 + 3.2);
    T.set(tag, { autoAlpha: 1 }, t0 + 3.5);
    var tw = M.$$('.tl .w>span', tag);
    if (tw.length) T.fromTo(tw, { yPercent: 115, rotate: 5 }, { yPercent: 0, rotate: 0, duration: 0.85, ease: 'expo.out', stagger: 0.08 }, t0 + 3.6);
    var url = M.$('.url', tag);
    if (url) T.fromTo(url, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }, t0 + 4.3);
    var end = t0 + 5.2 + (opts.hold || 0);
    if (opts.fade === false) { T.to({}, { duration: 0.4 }, end); return end + 0.4; }
    T.to([lock, tag], { autoAlpha: 0, filter: 'blur(10px)', duration: 0.4, ease: 'power2.in' }, end);
    T.set([lock, tag], { filter: 'blur(0px)' }, end + 0.4);
    return end + 0.4;
  }

  M.brand = { intro: introSeq, outro: outroSeq, lock: lock, mark: mark, word: word };
})(window);

/*!
 * motion-recipes.js — coreografias prontas para cada componente de scripts/components/.
 * Depende de: Motion (motion-core.js). Cada receita recebe um seletor de escopo e o instante t,
 * lê os dados do próprio HTML (data-n, data-dec, data-s, data-a, data-b, data-type) e devolve
 * o instante em que a sua animação principal termina.
 * Exporta: Motion.recipes
 */
(function (global) {
  'use strict';
  var M = global.Motion, T = M.T, $ = M.$, $$ = M.$$;

  function q(scope, sel) { return scope + ' ' + sel; }
  function exists(sel) { return !!$(sel); }

  /* janela/celular/card subindo no lugar */
  function rise(sel, t, opts) {
    opts = opts || {};
    T.fromTo(sel, { y: opts.y == null ? 90 : opts.y, opacity: 0, rotation: opts.rotation || 0 },
      { y: 0, opacity: 1, rotation: 0, duration: opts.duration || 0.9, ease: 'expo.out' }, t);
    return t + (opts.duration || 0.9);
  }

  /* barras horizontais .fill com escala em data-s (0..1) */
  function bars(scope, t, stagger, attr) {
    $$(q(scope, '.fill')).forEach(function (f, i) {
      var v = parseFloat(f.dataset[attr || 's'] || '1');
      T.fromTo(f, { scaleX: 0 }, { scaleX: v, duration: 1, ease: 'expo.out' }, t + i * (stagger || 0.07));
    });
  }

  /* ---------- celular com KPIs (phone-stats.html) ---------- */
  function phone(scope, t) {
    var ph = q(scope, '.phone');
    rise(ph, t + 0.2, { y: 140, rotation: 3, duration: 1 });
    T.fromTo($$(q(ph, '.card')), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: 'power3.out', stagger: 0.1 }, t + 0.55);
    M.countAll(ph, t + 0.7, 1.5, 0.12);
    if (exists(q(ph, '.vb .bar'))) {
      T.fromTo(q(ph, '.vb .bar'), { scaleY: 0 }, { scaleY: 1, duration: 0.9, ease: 'expo.out', stagger: 0.14 }, t + 1.25);
      T.fromTo(q(ph, '.vb .v'), { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.14 }, t + 1.5);
    }
    return t + 2.1;
  }

  /* ---------- card flutuante / notificação (notif-card.html) ---------- */
  function floatCard(sel, t, from) {
    var v = from === 'bottom' ? { y: 80, rotation: -2 } : { x: 120, scale: 0.94 };
    T.fromTo(sel, Object.assign({ opacity: 0 }, v), { x: 0, y: 0, scale: 1, rotation: 0, opacity: 1, duration: 0.8, ease: 'expo.out' }, t);
    M.countAll(sel, t + 0.1, 1.2);
    return t + 0.8;
  }

  /* ---------- busca + lista ranqueada (search-list.html) ---------- */
  function searchList(scope, t, opts) {
    opts = opts || {};
    var win = q(scope, '.win');
    rise(win, t + 0.2);
    var tt = t + 0.35, typed = $(q(scope, '[data-type]'));
    if (typed && exists(q(scope, '.search'))) {
      tt = M.clickOn(q(scope, '.search'), t + 0.35);
      M.type(typed, typed.dataset.type, tt + 0.1, 0.5);
      M.cursorOut(tt + 0.35);
    }
    T.fromTo(q(scope, '.trow'), { x: 40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: 'power3.out', stagger: 0.07 }, tt + 0.35);
    bars(scope, tt + 0.45, 0.07);
    M.countAll(q(scope, '.rows'), tt + 0.45, 1.1, 0.07);
    if (opts.highlightFirst !== false && exists(q(scope, '.trow'))) {
      T.fromTo(q(scope, '.trow:first-child'), { backgroundColor: 'rgba(255,255,255,0)' }, { backgroundColor: 'rgba(255,255,255,.07)', duration: 0.4 }, tt + 1.4);
    }
    if (exists(q(scope, '.flag'))) {
      T.fromTo(q(scope, '.flag'), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }, tt + 1.6);
      T.fromTo(q(scope, '.flag .tag'), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(2)' }, tt + 1.85);
    }
    return tt + 2.2;
  }

  /* ---------- ranking de pessoas (leaderboard.html) ---------- */
  function leaderboard(scope, t) {
    rise(q(scope, '.win'), t + 0.2);
    T.fromTo(q(scope, '.lrow'), { x: 50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: 'power3.out', stagger: 0.09 }, t + 0.55);
    T.fromTo(q(scope, '.av'), { scale: 0 }, { scale: 1, duration: 0.5, ease: 'back.out(2)', stagger: 0.09 }, t + 0.6);
    $$(q(scope, '.lbar')).forEach(function (b, i) {
      T.fromTo(b, { scaleX: 0 }, { scaleX: parseFloat(b.dataset.s || '1'), duration: 1.1, ease: 'expo.out' }, t + 0.75 + i * 0.09);
    });
    M.countAll(q(scope, '.win'), t + 0.7, 1.4, 0.09);
    return t + 2;
  }

  /* ---------- pipeline de etapas (pipeline.html) ---------- */
  function pipeline(scope, t) {
    var rail = $(q(scope, '.rail')), pulse = $(q(scope, '.pulse'));
    if (rail) T.fromTo(rail, { scaleX: 0 }, { scaleX: 1, duration: 1.2, ease: 'expo.inOut' }, t + 0.45);
    T.fromTo(q(scope, '.node'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: 'expo.out', stagger: 0.14 }, t + 0.55);
    T.fromTo(q(scope, '.node svg'), { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(2)', stagger: 0.14 }, t + 0.75);
    if (rail && pulse) {
      T.fromTo(pulse, { x: 0, opacity: 0 }, { x: rail.offsetWidth - 14, opacity: 1, duration: 1.6, ease: 'power2.inOut' }, t + 1.2);
      T.to(pulse, { opacity: 0, duration: 0.3 }, t + 2.8);
    }
    T.fromTo(q(scope, '.node'), { borderColor: '#262626' }, { borderColor: '#ffffff', duration: 0.2, stagger: 0.38, yoyo: true, repeat: 1 }, t + 1.25);
    return t + 2.8;
  }

  /* ---------- terminal com digitação (terminal.html) ---------- */
  function terminal(sel, t, dur) {
    T.fromTo(sel, { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: 'expo.out' }, t);
    var typed = $(sel + ' [data-type]');
    if (typed) return M.type(typed, typed.dataset.type, t + 0.3, dur || 1.3);
    return t + 0.7;
  }

  /* ---------- controle segmentado + barras que trocam de série (segmented-bars.html) ----------
     opts.switchAfter: segundos após t para o cursor clicar na 2ª aba (padrão 1.45) */
  function segmentedBars(scope, t, opts) {
    opts = opts || {};
    var win = q(scope, '.win');
    rise(win, t + 0.2);
    T.set(q(scope, '.segc .pl'), { x: 0 }, t);
    T.set(q(scope, '.flip .a'), { yPercent: 0, opacity: 1 }, t);
    T.set(q(scope, '.flip .b'), { yPercent: 100, opacity: 0 }, t);
    T.fromTo(q(scope, '.srow'), { x: 40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: 'power3.out', stagger: 0.08 }, t + 0.55);
    bars(scope, t + 0.7, 0.08, 'a');
    var tabs = $$(q(scope, '.segc span')), segc = $(q(scope, '.segc'));
    if (tabs.length < 2) return t + 1.8;
    var tc = M.clickOn(tabs[1], t + (opts.switchAfter || 1.45));
    T.to(q(scope, '.segc .pl'), { x: segc.clientWidth / 2 - 6, duration: 0.55, ease: 'expo.inOut' }, tc + 0.05);
    T.to(q(scope, '.flip .a'), { yPercent: -100, opacity: 0, duration: 0.4, ease: 'power3.in', stagger: 0.05 }, tc + 0.1);
    T.to(q(scope, '.flip .b'), { yPercent: 0, opacity: 1, duration: 0.5, ease: 'expo.out', stagger: 0.05 }, tc + 0.3);
    $$(q(scope, '.fill')).forEach(function (f, i) {
      T.to(f, { scaleX: parseFloat(f.dataset.b || f.dataset.a || '1'), duration: 0.9, ease: 'expo.inOut' }, tc + 0.15 + i * 0.05);
    });
    M.cursorOut(tc + 0.45);
    return tc + 1.2;
  }

  /* ---------- dissolve a moldura de uma janela deixando só as barras (ponte para o encerramento) ---------- */
  function dissolveToBars(scope, t, fadeSel) {
    var win = $(q(scope, '.win'));
    var fade = fadeSel || '.win-bar, .segc, .rowtop, .trow .r, .trow .t, .trow .c, .flag, .search, .lbl';
    var targets = $$(q(scope, fade.split(',').join(', ' + scope + ' ')));
    if (targets.length) T.to(targets, { autoAlpha: 0, duration: 0.35, stagger: 0.03 }, t + 0.1);
    if (win) T.to(win, { backgroundColor: 'rgba(10,10,10,0)', borderColor: 'rgba(38,38,38,0)', boxShadow: '0 0 0 rgba(0,0,0,0)', duration: 0.4 }, t + 0.15);
    T.to(q(scope, '.track'), { backgroundColor: 'rgba(28,28,28,0)', duration: 0.4 }, t + 0.15);
    /* restaura para a próxima volta do loop */
    if (targets.length) T.set(targets, { autoAlpha: 1 }, 0);
    if (win) T.set(win, { backgroundColor: '', borderColor: '', boxShadow: '' }, 0);
    T.set(q(scope, '.track'), { backgroundColor: '' }, 0);
    return t + 0.6;
  }

  M.recipes = {
    rise: rise, bars: bars, phone: phone, floatCard: floatCard, searchList: searchList,
    leaderboard: leaderboard, pipeline: pipeline, terminal: terminal,
    segmentedBars: segmentedBars, dissolveToBars: dissolveToBars
  };
})(window);

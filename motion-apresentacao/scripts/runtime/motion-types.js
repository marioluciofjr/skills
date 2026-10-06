/*!
 * motion-types.js — tipos de movimento reutilizáveis em qualquer cena (references/tipos-de-motion.md).
 * Depende de: Motion (motion-core.js). Não conhece componentes: recebe um seletor e anima o que achar nele.
 * Diferença para motion-recipes.js: receita = coreografia de UM componente; tipo = UMA forma de movimento
 * que serve a vários componentes (alta coesão em cada módulo, nenhum depende do outro).
 * Assinatura de todos: (seletor, t, opções) -> instante em que o movimento principal termina.
 * Exporta: Motion.types
 */
(function (global) {
  'use strict';
  var M = global.Motion, T = M.T, $ = M.$, $$ = M.$$;

  /* lê uma cor do tema (tokens --bg, --fg... injetados pelo build_motion.py) */
  function token(name) {
    return global.getComputedStyle(document.documentElement).getPropertyValue('--' + name).trim();
  }
  /* devolve o próprio elemento (se casar com o filtro) ou os descendentes que casam */
  function targets(sel, filter) {
    var self = $(sel);
    if (!self) return [];
    if (self.matches && self.matches(filter)) return $$(sel);
    return $$(sel + ' ' + filter.split(',').join(', ' + sel + ' '));
  }

  /* ---------- revelação por máscara: o conteúdo aparece "descoberto" por uma janela que abre ----------
     opts.dir: 'left' (padrão, abre da esquerda para a direita) | 'right' | 'up' | 'down'
     opts.duration (0.9) | opts.settle: true faz o conteúdo assentar de 1.06 para 1 durante a abertura */
  var MASKS = {
    left: 'inset(0% 100% 0% 0%)', right: 'inset(0% 0% 0% 100%)',
    up: 'inset(100% 0% 0% 0%)', down: 'inset(0% 0% 100% 0%)'
  };
  function maskReveal(sel, t, opts) {
    opts = opts || {};
    var dur = opts.duration || 0.9;
    T.fromTo(sel, { clipPath: MASKS[opts.dir] || MASKS.left, autoAlpha: 1 },
      { clipPath: 'inset(0% 0% 0% 0%)', duration: dur, ease: 'expo.inOut' }, t);
    if (opts.settle) T.fromTo(sel, { scale: 1.06 }, { scale: 1, duration: dur + 0.3, ease: 'expo.out' }, t);
    return t + dur;
  }

  /* ---------- transição em íris: um círculo abre (ou fecha) a partir de um ponto do quadro ----------
     Serve como entrada de cena alternativa ao sceneIn (use um OU outro na mesma cena) ou para revelar uma foto.
     opts.mode: 'open' (padrão) | 'close' | opts.at ('50% 50%', centro do círculo) | opts.duration (0.8) */
  function iris(sel, t, opts) {
    opts = opts || {};
    var at = opts.at || '50% 50%', dur = opts.duration || 0.8;
    var shut = 'circle(0% at ' + at + ')', full = 'circle(110% at ' + at + ')';
    /* power3.inOut e não expo.out: com expo o círculo cobre o quadro em 0,1 s e a forma redonda nem é percebida */
    if (opts.mode === 'close') {
      T.fromTo(sel, { clipPath: full }, { clipPath: shut, duration: dur, ease: 'power3.inOut' }, t);
    } else {
      T.fromTo(sel, { clipPath: shut, autoAlpha: 1, x: 0, filter: 'blur(0px)' },
        { clipPath: full, duration: dur, ease: 'power3.inOut' }, t);
    }
    return t + dur;
  }

  /* ---------- desenho de traço: linhas e contornos SVG são "desenhados" do início ao fim ----------
     Anima path, line, polyline, polygon, circle, rect e ellipse dentro do seletor.
     opts.duration (1.2) | opts.stagger (0.12) */
  function drawLine(sel, t, opts) {
    opts = opts || {};
    var dur = opts.duration || 1.2, st = opts.stagger == null ? 0.12 : opts.stagger;
    var shapes = targets(sel, 'path, line, polyline, polygon, circle, rect, ellipse');
    shapes.forEach(function (s, i) {
      var len = s.getTotalLength ? Math.ceil(s.getTotalLength()) : 1000;
      T.set(s, { strokeDasharray: len }, 0);
      T.fromTo(s, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur, ease: 'power2.inOut' }, t + i * st);
    });
    return t + dur + Math.max(0, shapes.length - 1) * st;
  }

  /* ---------- marcador de destaque (accent): uma barra passa por trás de um trecho e o inverte ----------
     Marcação: <mark class="mk">trecho</mark> FORA de elementos com data-split (o split reescreve o HTML).
     opts.style: 'fill' (padrão, barra cheia e texto invertido) | 'under' (sublinhado grosso)
               | 'ink' (sem barra: o trecho ganha cor de destaque; some a classe mk-serif para itálico serifado)
     opts.color (cor do 'ink'; padrão --fg) | opts.duration (0.6) | opts.stagger (0.15) */
  function prepareMark(node) {
    if (node.dataset.mkDone) return;
    node.innerHTML = '<i class="mk-bar"></i><span class="mk-t">' + node.innerHTML + '</span>';
    node.dataset.mkDone = '1';
  }
  function highlight(sel, t, opts) {
    opts = opts || {};
    var dur = opts.duration || 0.6, st = opts.stagger == null ? 0.15 : opts.stagger;
    var marks = targets(sel, '.mk');
    marks.forEach(function (node, i) {
      prepareMark(node);
      node.classList.toggle('mk-under', opts.style === 'under');
      node.classList.toggle('mk-ink', opts.style === 'ink');
      var at = t + i * st;
      if (opts.style === 'ink') {
        T.fromTo(node.querySelector('.mk-t'), { color: token('g1') }, { color: opts.color || token('fg'), duration: dur, ease: 'power2.out' }, at);
        return;
      }
      T.fromTo(node.querySelector('.mk-bar'), { scaleX: 0 }, { scaleX: 1, duration: dur, ease: 'expo.inOut' }, at);
      if (opts.style !== 'under') {
        T.fromTo(node.querySelector('.mk-t'), { color: token('fg') }, { color: token('bg'), duration: dur * 0.5, ease: 'none' }, at + dur * 0.35);
      }
    });
    return t + dur + Math.max(0, marks.length - 1) * st;
  }

  /* ---------- flutuação 3D: o objeto (celular, card, produto) paira e gira devagar no espaço ----------
     A perspectiva vem do próprio tween (transformPerspective), então não precisa de CSS no elemento pai.
     opts.duration (4, normalmente a duração da cena) | opts.tilt (10 graus de giro) | opts.lift (14 px de subida) */
  function float3d(sel, t, opts) {
    opts = opts || {};
    var dur = opts.duration || 4, tilt = opts.tilt == null ? 10 : opts.tilt, lift = opts.lift == null ? 14 : opts.lift;
    T.fromTo(sel, { transformPerspective: 1400, rotationY: -tilt, rotationX: tilt / 2, y: lift },
      { rotationY: tilt, rotationX: -tilt / 2, y: -lift, duration: dur, ease: 'sine.inOut' }, t);
    return t + dur;
  }

  /* ---------- morphing de forma: um elemento muda de forma (ponto -> card, linha -> painel) ----------
     Usa clip-path inset com cantos arredondados; o GSAP interpola os números das duas formas.
     opts.from ('dot') e opts.to ('card'): nomes de MORPHS ou strings "inset(a% b% c% d% round Npx)"
     opts.radius (28, raio do card) | opts.duration (0.9) */
  function morphShape(name, radius) {
    var shapes = {
      dot: 'inset(46% 46% 46% 46% round 999px)',
      line: 'inset(49.5% 0% 49.5% 0% round 0px)',
      column: 'inset(0% 49% 0% 49% round 0px)',
      pill: 'inset(38% 20% 38% 20% round 999px)',
      card: 'inset(0% 0% 0% 0% round ' + radius + 'px)'
    };
    return shapes[name] || name;
  }
  function morph(sel, t, opts) {
    opts = opts || {};
    var r = opts.radius == null ? 28 : opts.radius, dur = opts.duration || 0.9;
    T.fromTo(sel, { clipPath: morphShape(opts.from || 'dot', r), autoAlpha: 1 },
      { clipPath: morphShape(opts.to || 'card', r), duration: dur, ease: 'expo.inOut' }, t);
    return t + dur;
  }

  /* ---------- parallax em camadas: camadas com data-depth andam em velocidades diferentes ----------
     data-depth="0.2" (fundo, anda pouco) até "1" (frente, anda mais). Movimento contínuo e linear durante a cena.
     opts.duration (4, normalmente a duração da cena) | opts.distance (120 px na profundidade 1) | opts.axis ('x' | 'y') */
  function parallax(sel, t, opts) {
    opts = opts || {};
    var dur = opts.duration || 4, dist = opts.distance || 120, axis = opts.axis === 'y' ? 'y' : 'x';
    targets(sel, '[data-depth]').forEach(function (layer) {
      var d = parseFloat(layer.dataset.depth || '1'), from = {}, to = { duration: dur, ease: 'none' };
      from[axis] = dist * d;
      to[axis] = -dist * d;
      T.fromTo(layer, from, to, t);
    });
    return t + dur;
  }

  /* ---------- push de câmera: aproximação (ou afastamento) lenta, como uma câmera andando ----------
     Aplique num invólucro .cam dentro da cena (não na .scene, que já é animada por sceneIn/sceneOut).
     opts.from (1) | opts.to (1.08; menor que from = afastamento) | opts.duration (4) | opts.origin ('50% 50%') */
  function cameraPush(sel, t, opts) {
    opts = opts || {};
    var dur = opts.duration || 4;
    T.fromTo(sel, { scale: opts.from || 1, transformOrigin: opts.origin || '50% 50%' },
      { scale: opts.to || 1.08, duration: dur, ease: 'power1.inOut' }, t);
    return t + dur;
  }

  M.types = {
    maskReveal: maskReveal, iris: iris, drawLine: drawLine, highlight: highlight,
    float3d: float3d, morph: morph, parallax: parallax, cameraPush: cameraPush
  };
})(window);

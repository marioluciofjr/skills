/*!
 * motion-particles.js — sistema de partículas em canvas que convergem para a forma de uma imagem.
 * Não depende de gsap nem do Motion: recebe canvas, imagem e retângulos; o agendamento fica com quem chama.
 * Exporta: window.MotionParticles.create(opts) -> { prepare(rects), draw(p), clear(), count() }
 *
 * opts:
 *   canvas   HTMLCanvasElement (tamanho em px do palco)
 *   image    HTMLImageElement já decodificada (silhueta luminosa sobre transparente)
 *   src      recorte da imagem em frações { fx, fy, fw, fh } (padrão: imagem inteira)
 *   dest     retângulo de destino no palco { x, y, w, h }
 *   step     espaçamento da amostragem em px (padrão 6)
 *   trail    opacidade do preenchimento de rastro por quadro (padrão 0.22; 1 = sem rastro)
 *   max      limite de partículas (padrão 4200)
 *   color    cor das partículas (padrão '#fff')
 *   bg       cor do rastro (padrão '0,0,0')
 */
(function (global) {
  'use strict';

  function easeInOutCubic(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), k = a[i]; a[i] = a[j]; a[j] = k; }
    return a;
  }

  function create(opts) {
    var canvas = opts.canvas, ctx = canvas.getContext('2d');
    var CW = canvas.width, CH = canvas.height;
    var step = opts.step || 6, trail = opts.trail == null ? 0.22 : opts.trail;
    var color = opts.color || '#fff', bg = opts.bg || '0,0,0';
    var targets = null, parts = [];

    function sampleTargets() {
      var img = opts.image, s = opts.src || { fx: 0, fy: 0, fw: 1, fh: 1 }, d = opts.dest;
      var iw = img.naturalWidth, ih = img.naturalHeight;
      var off = document.createElement('canvas');
      off.width = CW; off.height = CH;
      var c = off.getContext('2d');
      c.drawImage(img, s.fx * iw, s.fy * ih, s.fw * iw, s.fh * ih, d.x, d.y, d.w, d.h);
      var data = c.getImageData(0, 0, CW, CH).data, out = [];
      for (var y = Math.max(0, Math.floor(d.y)); y < Math.min(CH, d.y + d.h); y += step) {
        for (var x = Math.max(0, Math.floor(d.x)); x < Math.min(CW, d.x + d.w); x += step) {
          if (data[(y * CW + x) * 4 + 3] > 140) out.push([x, y]);
        }
      }
      shuffle(out);
      return out.slice(0, opts.max || 4200);
    }

    /* rects: [{x,y,w,h}] de onde as partículas nascem (ex.: barras de um gráfico); vazio = espalhadas */
    function prepare(rects) {
      if (!targets) targets = sampleTargets();
      rects = (rects || []).filter(function (r) { return r.w > 2 && r.h > 0; });
      var total = rects.reduce(function (a, r) { return a + r.w * Math.max(r.h, 4); }, 0);
      parts = targets.map(function (t) {
        var sx, sy;
        if (rects.length && Math.random() < 0.9) {
          var k = Math.random() * total, r = rects[0];
          for (var i = 0; i < rects.length; i++) {
            var wgt = rects[i].w * Math.max(rects[i].h, 4);
            if (k < wgt) { r = rects[i]; break; }
            k -= wgt;
          }
          sx = r.x + Math.random() * r.w; sy = r.y + Math.random() * r.h;
        } else { sx = Math.random() * CW; sy = Math.random() * CH; }
        return {
          sx: sx, sy: sy, tx: t[0], ty: t[1],
          cx: (sx + t[0]) / 2 + (Math.random() - 0.5) * 700,
          cy: (sy + t[1]) / 2 + (Math.random() - 0.5) * 520,
          d: Math.min(0.3, Math.max(0, (sx - CW * 0.47) / (CW * 0.47) * 0.28)) + Math.random() * 0.08
        };
      });
      clear();
    }

    /* p: progresso global 0..1 */
    function draw(p) {
      ctx.fillStyle = 'rgba(' + bg + ',' + trail + ')';
      ctx.fillRect(0, 0, CW, CH);
      ctx.fillStyle = color;
      for (var i = 0; i < parts.length; i++) {
        var q = parts[i];
        var t = Math.min(1, Math.max(0, (p - q.d) / 0.62)), e = easeInOutCubic(t), u = 1 - e;
        var x = u * u * q.sx + 2 * u * e * q.cx + e * e * q.tx;
        var y = u * u * q.sy + 2 * u * e * q.cy + e * e * q.ty;
        var s = t >= 1 ? step * 0.6 : 2.4;
        ctx.fillRect(x, y, s, s);
      }
    }
    function clear() { ctx.clearRect(0, 0, CW, CH); }

    return { prepare: prepare, draw: draw, clear: clear, count: function () { return parts.length; } };
  }

  global.MotionParticles = { create: create };
})(window);

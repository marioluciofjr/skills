/* Coreografia do exemplo (30 s). Só usa a API pública: Motion (core), M.chrome, M.brand, M.recipes.
   Mapa de tempo: abertura 0–2,95 | 5 cenas de ~4,2 s com 0,2 s de sobreposição | encerramento 24,4–30. */
Motion.compose(function (M) {
  var R = M.recipes;

  /* abertura com logo */
  var t = M.brand.intro(0);                 // 2.95
  M.chrome.in(t);

  /* 1. O que encontramos? — celular com KPIs + notificação */
  M.sceneIn('#s2', t); M.chrome.progress(0, t, 7.45); M.headIn('#s2', t);
  R.phone('#s2', t);
  R.floatCard('#s2 .notif', t + 2.1, 'right');
  M.sceneOut('#s2', 7.4);

  /* 2. Sobre os temas — busca digitada + ranking de termos */
  t = 7.6;
  M.sceneIn('#s3', t); M.chrome.progress(1, t, 11.65); M.headIn('#s3', t);
  R.searchList('#s3', t);
  M.sceneOut('#s3', 11.6);

  /* 3. Sobre os líderes — leaderboard + card de eficiência */
  t = 11.8;
  M.sceneIn('#s4', t); M.chrome.progress(2, t, 15.95); M.headIn('#s4', t);
  R.leaderboard('#s4', t);
  R.floatCard('#s4 .notif', t + 1.9, 'bottom');
  M.sceneOut('#s4', 15.9);

  /* 4. Metodologias — pipeline + fórmula digitada */
  t = 16.1;
  M.sceneIn('#s5', t); M.chrome.progress(3, t, 20.25); M.headIn('#s5', t);
  R.pipeline('#s5', t);
  R.terminal('#s5 .term', t + 1.15, 1.3);
  M.sceneOut('#s5', 20.2);

  /* 5. Dados por setor — troca de aba; as barras viram a matéria-prima do logo */
  t = 20.4;
  M.sceneIn('#s6', t); M.chrome.progress(4, t, 24.25); M.headIn('#s6', t);
  R.segmentedBars('#s6', t, { switchAfter: 1.45 });
  M.echoTo('#s6 .left', M.outVars(), 23.75);
  M.T.set('#s6 .left', { x: 0, autoAlpha: 1, filter: 'blur(0px)' }, 24.6);
  R.dissolveToBars('#s6', 23.75);
  M.chrome.out(23.95);

  /* encerramento: barras -> partículas -> símbolo -> logo completo + tagline */
  M.brand.outro(24.4, { sources: function () { return M.$$('#s6 .fill'); }, hide: '#s6' });
});

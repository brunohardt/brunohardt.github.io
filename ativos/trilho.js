/* ============================================================================
   O AVANÇO DO TRILHO

   A única exceção à regra "zero JavaScript" da ESPEC §2.3, e ela tem nome:
   carrossel que anda sozinho num trilho de `scroll-snap` não tem versão em CSS
   que não seja gambiarra, e gambiarra em CSS é o que estoura em 320px.

   Por que existe: lâmina que não é a primeira depende de rolagem horizontal, e
   quase ninguém rola na horizontal. Publicar texto que ninguém alcança é pior
   que não destacá-lo.

   O que ele não faz: nada indispensável. Sem este arquivo as réguas continuam
   navegando o trilho por clique e por teclado, e nenhum escrito fica
   inalcançável — o site fica pior, não quebrado.

   Para sob `prefers-reduced-motion: reduce`, e para de vez assim que o leitor
   toca no trilho: periódico que puxa a página enquanto a pessoa lê é pior que
   periódico parado.
   ========================================================================= */
(function () {
  'use strict';

  var INTERVALO = 6000;
  window.__trilhoIntervalo = INTERVALO;   // o verificador lê o intervalo daqui

  var trilho = document.querySelector('.trilho');
  if (!trilho) return;

  var laminas = trilho.querySelectorAll('.lamina');
  if (laminas.length < 2) return;         // uma lâmina só não avança para lugar nenhum

  var reguas = document.querySelectorAll('.reguas a');
  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');
  var timer = null;
  var assumido = false;                   // o leitor tomou o comando

  function atual() {
    return Math.round(trilho.scrollLeft / (trilho.clientWidth || 1));
  }

  function marcar() {
    var i = atual();
    for (var k = 0; k < reguas.length; k++) {
      if (k === i) reguas[k].setAttribute('aria-current', 'true');
      else reguas[k].removeAttribute('aria-current');
    }
  }

  function avancar() {
    var proximo = (atual() + 1) % laminas.length;
    trilho.scrollTo({ left: proximo * trilho.clientWidth, behavior: 'smooth' });
  }

  function tocar() {
    if (timer) { clearInterval(timer); timer = null; }
    if (!assumido && !quieto.matches) timer = setInterval(avancar, INTERVALO);
  }

  function parar() {
    assumido = true;
    if (timer) { clearInterval(timer); timer = null; }
  }

  trilho.addEventListener('scroll', marcar, { passive: true });
  trilho.addEventListener('pointerdown', parar);
  trilho.addEventListener('wheel', parar, { passive: true });
  trilho.addEventListener('keydown', parar);
  for (var k = 0; k < reguas.length; k++) {
    reguas[k].addEventListener('click', parar);
  }
  // alguém que liga "movimento reduzido" no meio da visita é atendido na hora
  if (quieto.addEventListener) quieto.addEventListener('change', tocar);

  marcar();
  tocar();
})();

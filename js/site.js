(function () {
  'use strict';

  function normalize(text) {
    return String(text || '')
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .toLowerCase()
      .trim();
  }

  function initNav() {
    var toggle = document.querySelector('[data-nav-toggle]');
    var nav = document.getElementById('mobile-nav');
    if (!toggle || !nav) return;
    toggle.addEventListener('click', function () {
      var hidden = nav.classList.toggle('hidden');
      toggle.setAttribute('aria-expanded', hidden ? 'false' : 'true');
    });
  }

  function priceOf(card) {
    var raw = card.getAttribute('data-price');
    if (raw === null || raw === '') return null;
    var n = parseFloat(String(raw).replace(',', '.'));
    return isNaN(n) ? null : n;
  }

  function initProducts() {
    var cards = Array.prototype.slice.call(document.querySelectorAll('[data-product-card]'));
    if (!cards.length) return;
    var input = document.getElementById('product-search');
    var select = document.getElementById('product-sort');
    var empty = document.getElementById('no-results');
    var grid = cards[0].parentNode;

    var titles = cards.map(function (c) { return normalize(c.getAttribute('data-title')); });

    function sorted(mode) {
      var items = cards.map(function (c, i) { return { el: c, i: i, title: c.getAttribute('data-title') || '', price: priceOf(c) }; });
      items.sort(function (a, b) {
        if (mode === 'price-asc' || mode === 'price-desc') {
          if (a.price === null && b.price === null) return a.i - b.i;
          if (a.price === null) return 1;
          if (b.price === null) return -1;
          var d = mode === 'price-asc' ? a.price - b.price : b.price - a.price;
          return d !== 0 ? d : a.i - b.i;
        }
        return a.title.localeCompare(b.title, 'sl');
      });
      return items.map(function (x) { return x.el; });
    }

    function apply() {
      var query = normalize(input ? input.value : '');
      var visible = 0;
      cards.forEach(function (card, i) {
        var show = query === '' || titles[i].indexOf(query) !== -1;
        card.classList.toggle('hidden', !show);
        if (show) visible += 1;
      });
      if (select && grid) {
        sorted(select.value).forEach(function (el) { grid.appendChild(el); });
      }
      if (empty) empty.hidden = visible !== 0;
    }

    function syncUrl() {
      if (!input || !window.history || !history.replaceState) return;
      var params = new URLSearchParams(window.location.search);
      if (input.value) params.set('q', input.value); else params.delete('q');
      var qs = params.toString();
      history.replaceState(null, '', window.location.pathname + (qs ? '?' + qs : '') + window.location.hash);
    }

    if (input) {
      var initial = new URLSearchParams(window.location.search).get('q');
      if (initial) input.value = initial;
      input.addEventListener('input', function () { apply(); syncUrl(); });
    }
    if (select) select.addEventListener('change', apply);
    apply();
  }

  function init() {
    initNav();
    initProducts();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

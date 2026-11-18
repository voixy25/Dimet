(function () {
  'use strict';

  function normalize(text) {
    return String(text || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .trim();
  }

  function formatProductCount(n) {
    var mod100 = n % 100;
    var mod10 = n % 10;
    var word = 'izdelkov';
    if (mod100 === 1) word = 'izdelek';
    else if (mod100 === 2) word = 'izdelka';
    else if (mod100 === 3 || mod100 === 4) word = 'izdelki';
    else if (mod100 < 11 || mod100 > 14) {
      if (mod10 === 1) word = 'izdelek';
      else if (mod10 === 2) word = 'izdelka';
      else if (mod10 === 3 || mod10 === 4) word = 'izdelki';
    }
    var verb = n === 1 ? 'Prikazan ' : n === 2 ? 'Prikazana ' : 'Prikazanih ';
    if (mod100 >= 3 && mod100 <= 4) verb = 'Prikazani ';
    else if (n >= 3 && (mod100 < 11 || mod100 > 14) && (mod10 === 3 || mod10 === 4)) verb = 'Prikazani ';
    else if (n >= 1 && (mod100 < 11 || mod100 > 14) && mod10 === 1) verb = 'Prikazan ';
    else if (n >= 2 && (mod100 < 11 || mod100 > 14) && mod10 === 2) verb = 'Prikazana ';
    return verb + n + ' ' + word;
  }

  function initNav() {
    var toggle = document.querySelector('[data-nav-toggle]');
    var nav = document.getElementById('mobile-nav');
    if (toggle && nav) {
      toggle.addEventListener('click', function () {
        var hidden = nav.classList.toggle('hidden');
        toggle.setAttribute('aria-expanded', hidden ? 'false' : 'true');
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !nav.classList.contains('hidden')) {
          nav.classList.add('hidden');
          toggle.setAttribute('aria-expanded', 'false');
          toggle.focus();
        }
      });
    }

    var catWrap = document.querySelector('[data-cat-menu]');
    var catBtn = catWrap ? catWrap.querySelector('.category-box') : document.querySelector('header .category-box');
    if (!catWrap && catBtn) catWrap = catBtn.parentNode;
    var catNav = catWrap ? catWrap.querySelector('nav[aria-label="Kategorije"]') : null;
    if (catWrap && catBtn && catNav) {
      var defaultOpen = catWrap.getAttribute('data-default-open') === 'true' || catBtn.getAttribute('aria-expanded') === 'true';
      var isPinned = defaultOpen;
      var suppressedByClick = false;

      function setCatMenu(open) {
        catBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (open) {
          catNav.classList.remove('hidden');
          catNav.classList.add('block');
        } else {
          catNav.classList.remove('block');
          catNav.classList.add('hidden');
        }
      }

      catBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (defaultOpen) {
          var expanded = catBtn.getAttribute('aria-expanded') === 'true';
          setCatMenu(!expanded);
          return;
        }
        if (isPinned) {
          isPinned = false;
          suppressedByClick = true;
          setCatMenu(false);
        } else {
          isPinned = true;
          suppressedByClick = false;
          setCatMenu(true);
        }
      });

      if (!defaultOpen) {
        catWrap.addEventListener('mouseenter', function () {
          if (!suppressedByClick) {
            setCatMenu(true);
          }
        });
        catWrap.addEventListener('mouseleave', function () {
          suppressedByClick = false;
          if (!isPinned) {
            setCatMenu(false);
          }
        });
        catWrap.addEventListener('focusout', function (e) {
          if (!isPinned && (!e.relatedTarget || !catWrap.contains(e.relatedTarget))) {
            setCatMenu(false);
          }
        });
        document.addEventListener('click', function (e) {
          if (!catWrap.contains(e.target) && catBtn.getAttribute('aria-expanded') === 'true') {
            isPinned = false;
            suppressedByClick = false;
            setCatMenu(false);
          }
        });
        document.addEventListener('keydown', function (e) {
          if (e.key === 'Escape' && catBtn.getAttribute('aria-expanded') === 'true') {
            isPinned = false;
            suppressedByClick = true;
            setCatMenu(false);
            catBtn.focus();
          }
        });
      } else {
        document.addEventListener('keydown', function (e) {
          if (e.key === 'Escape' && catWrap.contains(document.activeElement) && catBtn.getAttribute('aria-expanded') === 'true') {
            setCatMenu(false);
            catBtn.focus();
          }
        });
      }
    }
  }

  function initHeroSlider() {
    var root = document.querySelector('[data-hero-carousel]');
    if (!root) return;
    var slides = Array.prototype.slice.call(root.querySelectorAll('[data-hero-slide]'));
    var dots = Array.prototype.slice.call(root.querySelectorAll('[data-hero-dot]'));
    var prevBtn = root.querySelector('[data-hero-prev]');
    var nextBtn = root.querySelector('[data-hero-next]');
    if (slides.length < 2) return;

    var current = 0;
    var timer = null;
    var isHovered = false;
    var isFocused = false;
    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function goTo(index) {
      current = (index + slides.length) % slides.length;
      slides.forEach(function (slide, i) {
        var active = i === current;
        slide.setAttribute('aria-hidden', active ? 'false' : 'true');
        slide.inert = !active;
        var focusables = slide.querySelectorAll('a, button');
        for (var j = 0; j < focusables.length; j += 1) {
          if (active) focusables[j].removeAttribute('tabindex');
          else focusables[j].setAttribute('tabindex', '-1');
        }
        if (active) {
          slide.classList.remove('pointer-events-none', 'absolute', 'inset-0', 'z-0', 'opacity-0');
          slide.classList.add('relative', 'z-10', 'opacity-100');
        } else {
          slide.classList.remove('relative', 'z-10', 'opacity-100');
          slide.classList.add('pointer-events-none', 'absolute', 'inset-0', 'z-0', 'opacity-0');
        }
      });
      dots.forEach(function (dot, i) {
        var active = i === current;
        var pill = dot.querySelector('[data-hero-dot-pill]');
        dot.setAttribute('aria-pressed', active ? 'true' : 'false');
        if (pill) {
          if (active) {
            pill.classList.remove('w-2.5', 'bg-gray-500/80', 'hover:bg-[#007BC4]/70');
            pill.classList.add('w-6', 'bg-[#007BC4]');
          } else {
            pill.classList.remove('w-6', 'bg-[#007BC4]');
            pill.classList.add('w-2.5', 'bg-gray-500/80', 'hover:bg-[#007BC4]/70');
          }
        }
      });
    }

    function stopAuto() {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    }

    function startAuto() {
      if (reducedMotion || isHovered || isFocused) return;
      stopAuto();
      timer = setInterval(function () {
        goTo(current + 1);
      }, 6000);
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        goTo(current - 1);
        startAuto();
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        goTo(current + 1);
        startAuto();
      });
    }
    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        goTo(i);
        startAuto();
      });
    });

    root.addEventListener('mouseenter', function () {
      isHovered = true;
      stopAuto();
    });
    root.addEventListener('mouseleave', function () {
      isHovered = false;
      startAuto();
    });
    root.addEventListener('focusin', function () {
      isFocused = true;
      stopAuto();
    });
    root.addEventListener('focusout', function (e) {
      if (!e.relatedTarget || !root.contains(e.relatedTarget)) {
        isFocused = false;
        startAuto();
      }
    });

    goTo(0);
    startAuto();
  }

  function initTabs() {
    var containers = Array.prototype.slice.call(document.querySelectorAll('[data-tabs-container]'));
    containers.forEach(function (container) {
      var tabs = Array.prototype.slice.call(container.querySelectorAll('[data-tab-target]'));
      var panels = Array.prototype.slice.call(container.querySelectorAll('[data-tab-panel]'));
      if (!tabs.length || !panels.length) return;

      function activate(targetId) {
        tabs.forEach(function (tab) {
          var active = tab.getAttribute('data-tab-target') === targetId;
          tab.setAttribute('aria-selected', active ? 'true' : 'false');
          tab.setAttribute('tabindex', active ? '0' : '-1');
          if (active) {
            tab.classList.remove('border-transparent', 'text-[#595959]');
            tab.classList.add('border-[#007BC4]', 'text-[#007BC4]');
          } else {
            tab.classList.remove('border-[#007BC4]', 'text-[#007BC4]');
            tab.classList.add('border-transparent', 'text-[#595959]');
          }
        });
        panels.forEach(function (panel) {
          var active = panel.getAttribute('data-tab-panel') === targetId;
          panel.classList.toggle('hidden', !active);
        });
      }

      tabs.forEach(function (tab, idx) {
        tab.addEventListener('click', function () {
          activate(tab.getAttribute('data-tab-target'));
        });
        tab.addEventListener('keydown', function (e) {
          var nextIdx = null;
          if (e.key === 'ArrowRight') nextIdx = (idx + 1) % tabs.length;
          else if (e.key === 'ArrowLeft') nextIdx = (idx - 1 + tabs.length) % tabs.length;
          else if (e.key === 'Home') nextIdx = 0;
          else if (e.key === 'End') nextIdx = tabs.length - 1;
          if (nextIdx !== null) {
            e.preventDefault();
            tabs[nextIdx].focus();
            activate(tabs[nextIdx].getAttribute('data-tab-target'));
          }
        });
      });
    });
  }

  function initNewsletter() {
    var forms = Array.prototype.slice.call(document.querySelectorAll('[data-newsletter-form]'));
    forms.forEach(function (form) {
      var email = form.querySelector('input[type="email"]');
      var status = form.parentNode.querySelector('[data-newsletter-status]');
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (email && !email.checkValidity()) {
          email.reportValidity();
          return;
        }
        var submitted = email ? email.value.trim() : '';
        if (submitted) {
          window.location.href =
            'mailto:info@dimet.si?subject=' +
            encodeURIComponent('Prijava na e-novice') +
            '&body=' +
            encodeURIComponent('Prosim za prijavo na e-novice: ' + submitted);
        }
        if (email) email.value = '';
        if (status) {
          status.textContent = submitted
            ? 'Hvala! Prijava na e-novice za naslov ' + submitted + ' je pripravljena za pošiljanje.'
            : 'Hvala za prijavo na naše e-novice!';
          status.hidden = false;
        }
      });
    });
  }

  function initContactForm() {
    var forms = Array.prototype.slice.call(document.querySelectorAll('[data-contact-form]'));
    forms.forEach(function (form) {
      var status = form.querySelector('[data-contact-status]');
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (!form.checkValidity()) {
          form.reportValidity();
          return;
        }
        var name = (form.querySelector('[name="name"]') || {}).value || '';
        var email = (form.querySelector('[name="email"]') || {}).value || '';
        var phone = (form.querySelector('[name="phone"]') || {}).value || '';
        var message = (form.querySelector('[name="message"]') || {}).value || '';
        var bodyLines = [
          'Ime in priimek: ' + name.trim(),
          'E-pošta: ' + email.trim()
        ];
        if (phone.trim()) bodyLines.push('Telefon: ' + phone.trim());
        bodyLines.push('', message.trim());
        window.location.href =
          'mailto:info@dimet.si?subject=' +
          encodeURIComponent('Spletno povpraševanje: ' + name.trim()) +
          '&body=' +
          encodeURIComponent(bodyLines.join('\n'));
        form.reset();
        if (status) {
          status.textContent = 'Hvala za vaše sporočilo! Odpiramo vaš e-poštni program za pošiljanje.';
          status.hidden = false;
        }
      });
    });
  }

  function initProductGallery() {
    var mainImg = document.querySelector('[data-product-main-img]');
    var thumbs = Array.prototype.slice.call(document.querySelectorAll('[data-gallery-thumb]'));
    if (!mainImg || !thumbs.length) return;
    thumbs.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var src = btn.getAttribute('data-img-src');
        var w = btn.getAttribute('data-img-width');
        var h = btn.getAttribute('data-img-height');
        if (src) mainImg.setAttribute('src', src);
        if (w) mainImg.setAttribute('width', w);
        if (h) mainImg.setAttribute('height', h);
        thumbs.forEach(function (other) {
          var active = other === btn;
          other.setAttribute('aria-pressed', active ? 'true' : 'false');
          other.classList.toggle('border-[#007BC4]', active);
          other.classList.toggle('border-[#E8E8E8]', !active);
        });
      });
    });
  }

  function priceOf(card) {
    var raw = card.getAttribute('data-price');
    if (raw === null || raw === '') return null;
    var n = parseFloat(String(raw).replace(',', '.'));
    return isNaN(n) ? null : n;
  }

  function initProducts() {
    var grid = document.querySelector('[data-product-grid]');
    if (!grid) return;
    var cards = Array.prototype.slice.call(grid.querySelectorAll('[data-product-card]'));
    if (!cards.length) return;

    var input = document.getElementById('product-search');
    var select = document.getElementById('product-sort');
    var empty = document.getElementById('no-results');
    var countEl = document.querySelector('[data-product-count]');
    var headingEl = document.querySelector('[data-shop-heading]');
    var resetBtn = document.querySelector('[data-filter-reset]');
    var catLinks = Array.prototype.slice.call(document.querySelectorAll('[data-cat-filter]'));

    var params = new URLSearchParams(window.location.search);
    var activeCat = params.get('cat') || '';
    var lastSortMode = null;

    var meta = cards.map(function (c) {
      var cats = String(c.getAttribute('data-categories') || '')
        .split(',')
        .map(function (s) { return s.trim(); })
        .filter(Boolean);
      var searchBlob = normalize(
        (c.getAttribute('data-title') || '') + ' ' +
        (c.getAttribute('data-category-names') || '') + ' ' +
        cats.join(' ')
      );
      return { cats: cats, searchBlob: searchBlob };
    });

    function sorted(mode) {
      var items = cards.map(function (c, i) {
        return { el: c, i: i, title: c.getAttribute('data-title') || '', price: priceOf(c) };
      });
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

    function updateCatUI() {
      var activeLabel = '';
      catLinks.forEach(function (link) {
        var slug = link.getAttribute('data-cat-filter') || '';
        var baseColor = link.getAttribute('data-base-color') || '';
        var isMatch = slug === activeCat;
        if (baseColor) {
          link.classList.toggle(baseColor, !isMatch);
        }
        link.classList.toggle('font-semibold', isMatch);
        link.classList.toggle('text-[#007BC4]', isMatch);
        link.classList.toggle('border-[#007BC4]', isMatch && link.classList.contains('chip'));
        if (isMatch) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
        if (isMatch && slug !== '' && !activeLabel) {
          var firstSpan = link.querySelector('span');
          activeLabel = (firstSpan ? firstSpan.textContent : link.textContent).trim();
        }
      });
      if (headingEl) {
        headingEl.textContent = activeCat && activeLabel ? 'Izdelki: ' + activeLabel : 'Izdelki';
      }
    }

    function syncUrl() {
      if (!window.history || !history.replaceState) return;
      var nextParams = new URLSearchParams(window.location.search);
      if (input && input.value.trim()) nextParams.set('q', input.value.trim());
      else nextParams.delete('q');
      if (activeCat) nextParams.set('cat', activeCat);
      else nextParams.delete('cat');
      var qs = nextParams.toString();
      history.replaceState(null, '', window.location.pathname + (qs ? '?' + qs : '') + window.location.hash);
    }

    function apply() {
      var query = normalize(input ? input.value : '');
      var visible = 0;
      cards.forEach(function (card, i) {
        var matchQuery = query === '' || meta[i].searchBlob.indexOf(query) !== -1;
        var matchCat = activeCat === '' || meta[i].cats.indexOf(activeCat) !== -1;
        var show = matchQuery && matchCat;
        card.classList.toggle('hidden', !show);
        if (show) visible += 1;
      });
      if (select && select.value !== lastSortMode) {
        lastSortMode = select.value;
        sorted(lastSortMode).forEach(function (el) { grid.appendChild(el); });
      }
      if (empty) empty.hidden = visible !== 0;
      if (countEl) countEl.textContent = formatProductCount(visible);
      if (resetBtn) resetBtn.classList.toggle('hidden', query === '' && activeCat === '');
      updateCatUI();
    }

    if (input) {
      var initialQ = params.get('q');
      if (initialQ) input.value = initialQ;
      input.addEventListener('input', function () {
        apply();
        syncUrl();
      });
    }
    if (select) select.addEventListener('change', apply);

    catLinks.forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        activeCat = link.getAttribute('data-cat-filter') || '';
        apply();
        syncUrl();
      });
    });

    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        activeCat = '';
        if (input) input.value = '';
        apply();
        syncUrl();
      });
    }

    apply();
  }

  function init() {
    initNav();
    initHeroSlider();
    initTabs();
    initNewsletter();
    initContactForm();
    initProductGallery();
    initProducts();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

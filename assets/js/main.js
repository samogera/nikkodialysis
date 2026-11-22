/* Nikko Dialysis Center — site behaviour. No dependencies. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.remove('no-js');
  var CFG = window.NIKKO || {};
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  /* Mobile menu */
  var mb = $('.menu-btn'), mm = $('#mobile-menu');
  if (mb && mm) {
    mb.addEventListener('click', function () {
      var open = mb.getAttribute('aria-expanded') !== 'true';
      mb.setAttribute('aria-expanded', String(open));
      mb.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      mm.classList.toggle('open', open);
      $('path', mb).setAttribute('d', open ? 'M6 6l12 12M18 6 6 18' : 'M4 7h16M4 12h16M4 17h16');
    });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && mm.classList.contains('open')) mb.click(); });
  }

  /* Reveal on scroll + split wordmark */
  var targets = $$('.reveal, .split-word');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    targets.forEach(function (t) { io.observe(t); });
  } else { targets.forEach(function (t) { t.classList.add('in'); }); }

  /* Tabs (session stages) */
  $$('[role=tablist]').forEach(function (list) {
    var tabs = $$('[role=tab]', list);
    function select(t, focus) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute('aria-selected', String(on)); x.tabIndex = on ? 0 : -1;
        var p = d.getElementById(x.getAttribute('aria-controls')); if (p) p.hidden = !on;
      });
      if (focus) t.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (n) { e.preventDefault(); select(tabs[(i + n + tabs.length) % tabs.length], true); }
      });
    });
  });

  /* First-session checklist (remembered on this device) */
  var cl = $('[data-checklist]');
  if (cl) {
    var saved = {}; try { saved = JSON.parse(store('nikko-checklist') || '{}'); } catch (e) {}
    var items = $$('.check', cl), count = $('[data-count]', cl);
    function upd() { var n = items.filter(function (b) { return b.getAttribute('aria-pressed') === 'true'; }).length; if (count) count.textContent = n + ' / ' + items.length + ' ready'; }
    items.forEach(function (b, i) {
      if (saved[i]) b.setAttribute('aria-pressed', 'true');
      b.addEventListener('click', function () {
        var on = b.getAttribute('aria-pressed') !== 'true';
        b.setAttribute('aria-pressed', String(on)); saved[i] = on; store('nikko-checklist', JSON.stringify(saved)); upd();
      });
    });
    upd();
  }

  /* Insurer search */
  var q = $('#insurer-search');
  if (q) {
    var cards = $$('[data-insurer]'), none = $('#insurer-none');
    q.addEventListener('input', function () {
      var v = q.value.trim().toLowerCase(), shown = 0;
      cards.forEach(function (c) { var m = !v || c.getAttribute('data-insurer').toLowerCase().indexOf(v) > -1; c.hidden = !m; if (m) shown++; });
      if (none) none.hidden = shown > 0;
    });
  }

  /* FAQ category filter */
  var ff = $('[data-faq-filter]');
  if (ff) {
    var btns = $$('button', ff), qs = $$('[data-cat]', d.getElementById(ff.getAttribute('data-faq-filter')));
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var c = b.getAttribute('data-value');
        btns.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        qs.forEach(function (x) { x.hidden = c !== 'All' && x.getAttribute('data-cat') !== c; if (x.hidden) x.open = false; });
      });
    });
  }

  /* Cookie consent: analytics + error tracking load only after "Accept" */
  function loadScript(src, attrs) { var s = d.createElement('script'); s.src = src; s.defer = true; for (var k in attrs || {}) s.setAttribute(k, attrs[k]); d.head.appendChild(s); }
  function startTracking() {
    if (CFG.plausibleDomain) loadScript('https://plausible.io/js/script.outbound-links.js', { 'data-domain': CFG.plausibleDomain });
    if (CFG.sentryLoader) loadScript(CFG.sentryLoader, { crossorigin: 'anonymous' });
  }
  var ck = $('#cookie'), choice = store('nikko-consent');
  if (choice === 'all') startTracking();
  if (ck && !choice) {
    ck.hidden = false;
    ck.addEventListener('click', function (e) {
      var v = e.target.getAttribute && e.target.getAttribute('data-consent'); if (!v) return;
      store('nikko-consent', v); ck.hidden = true; if (v === 'all') startTracking();
    });
  }
  $$('[data-cookie-settings]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); try { localStorage.removeItem('nikko-consent'); } catch (x) {} if (ck) ck.hidden = false; }); });
  function track(name, props) { if (window.plausible) window.plausible(name, { props: props || {} }); }
  d.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"], a[href*="wa.me"]');
    if (a) track(a.href.indexOf('tel:') === 0 ? 'Call click' : 'WhatsApp click', { page: location.pathname });
  });

  /* Shared POST helper with timeout + idempotency key */
  function uid() { return (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2); }
  function post(url, data) {
    var ctl = 'AbortController' in window ? new AbortController() : null;
    var t = setTimeout(function () { if (ctl) ctl.abort(); }, 15000);
    return fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data), signal: ctl ? ctl.signal : undefined })
      .then(function (r) { clearTimeout(t); return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok) throw new Error(j.error || 'Request failed'); return j; }); });
  }

  /* Two-step booking form */
  var form = $('#booking');
  if (form) {
    var s1 = $('#step-1', form), s2 = $('#step-2', form), done = $('#done'), err = $('#form-error', form);
    var next = $('#to-step-2', form), bar2 = $('[data-bar2]', form), label = $('[data-step-label]', form), pct = $('[data-step-pct]', form);
    var key = uid(), sending = false;
    function needs() { return $$('input[name=needs]:checked', form).map(function (i) { return i.value; }); }
    function syncNext() { var n = needs().length; next.disabled = n === 0; $('[data-selected]', form).textContent = n ? n + ' selected' : 'Select at least one option'; $('#dates-field', form).hidden = needs().indexOf('Holiday dialysis') < 0; $('#dates', form).required = !$('#dates-field', form).hidden; }
    $$('input[name=needs]', form).forEach(function (i) { i.addEventListener('change', syncNext); });
    function go(step) {
      s1.hidden = step !== 1; s2.hidden = step !== 2;
      bar2.classList.toggle('on', step === 2); label.textContent = 'Step ' + step + ' of 2 · ' + (step === 1 ? 'Your needs' : 'Your details'); pct.textContent = step === 1 ? '50%' : '100%';
      if (step === 2) { var c = $('#chosen', form); c.innerHTML = ''; needs().forEach(function (n) { var sp = d.createElement('span'); sp.className = 'chip'; sp.textContent = n; c.appendChild(sp); }); $('#name', form).focus(); track('Booking step 2'); }
      else { $('legend', s1).scrollIntoView({ block: 'nearest' }); }
    }
    next.addEventListener('click', function () { if (needs().length) go(2); });
    $$('[data-back]', form).forEach(function (b) { b.addEventListener('click', function () { go(1); }); });
    syncNext();
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (sending) return;
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var fd = new FormData(form), data = {};
      fd.forEach(function (v, k) { if (k === 'needs') (data.needs = data.needs || []).push(v); else data[k] = typeof v === 'string' ? v.trim() : v; });
      if (data.email) data.email = data.email.toLowerCase();
      data.idempotencyKey = key; data.page = location.pathname; data.tz = (Intl.DateTimeFormat().resolvedOptions().timeZone || '');
      sending = true; err.hidden = true;
      var btn = $('button[type=submit]', form); btn.disabled = true; btn.setAttribute('aria-busy', 'true'); btn.textContent = 'Sending…';
      post('/api/enquiry', data).then(function () {
        track('Booking submitted', { needs: (data.needs || []).join(', ') });
        form.hidden = true; done.hidden = false;
        $('[data-first]', done).textContent = (data.name || 'there').split(/\s+/)[0];
        $('[data-method]', done).textContent = (data.method || 'phone').toLowerCase();
        var c = $('#done-needs', done); (data.needs || []).forEach(function (n) { var sp = d.createElement('span'); sp.className = 'chip'; sp.textContent = n; c.appendChild(sp); });
        done.focus();
      }).catch(function () {
        err.hidden = false; sending = false; btn.disabled = false; btn.removeAttribute('aria-busy'); btn.textContent = 'Try again';
      });
    });
  }

  /* Footer patient-tips signup */
  $$('form[data-signup]').forEach(function (f) {
    var busy = false, k = uid();
    f.addEventListener('submit', function (e) {
      e.preventDefault(); if (busy) return;
      if (!f.checkValidity()) { f.reportValidity(); return; }
      busy = true; var m = $('.msg', f), b = $('button', f); b.disabled = true;
      post('/api/enquiry', { type: 'newsletter', email: f.email.value.trim().toLowerCase(), website: f.website.value, consent: f.consent.checked, idempotencyKey: k, page: location.pathname })
        .then(function () { m.textContent = 'Thank you. Check your inbox to confirm.'; m.hidden = false; f.reset(); track('Newsletter signup'); })
        .catch(function () { m.textContent = 'Something went wrong. Please try again.'; m.hidden = false; busy = false; b.disabled = false; });
    });
  });

  /* Year */
  $$('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();

/* Zeppelin Studio — documentation d'Opaline : recherche, menu, sommaire,
   visionneuse. Aucune dependance. */
(function () {
  'use strict';

  /* ---- Menu lateral au telephone ---- */
  var bascule = document.querySelector('[data-menu-toggle]');
  var barre = document.querySelector('.sidebar');
  if (bascule && barre) {
    bascule.addEventListener('click', function () {
      var ouvert = barre.classList.toggle('is-open');
      bascule.setAttribute('aria-expanded', String(ouvert));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && barre.classList.contains('is-open')) {
        barre.classList.remove('is-open');
        bascule.setAttribute('aria-expanded', 'false');
        bascule.focus();
      }
    });
    // La page courante a l'ecran dans la barre laterale.
    var courant = barre.querySelector('[aria-current="page"]');
    if (courant && courant.scrollIntoView) courant.scrollIntoView({ block: 'center' });
    window.scrollTo(0, 0);
  }

  /* ---- Sommaire qui suit la lecture ---- */
  var liens = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (liens.length && 'IntersectionObserver' in window) {
    var cibles = liens
      .map(function (a) {
        return document.getElementById(decodeURIComponent(a.hash.slice(1)));
      })
      .filter(Boolean);
    var actif = null;
    var obs = new IntersectionObserver(
      function (entrees) {
        entrees.forEach(function (e) {
          if (e.isIntersecting) actif = e.target.id;
        });
        liens.forEach(function (a) {
          a.classList.toggle('is-active', a.hash === '#' + actif);
        });
      },
      { rootMargin: '-15% 0px -70% 0px' },
    );
    cibles.forEach(function (c) {
      obs.observe(c);
    });
  }

  /* ---- Visionneuse des captures ---- */
  var boite = document.createElement('div');
  boite.className = 'lightbox';
  boite.hidden = true;
  boite.setAttribute('role', 'dialog');
  boite.setAttribute('aria-modal', 'true');
  boite.setAttribute('aria-label', 'Enlarged screenshot');
  var grande = document.createElement('img');
  grande.alt = '';
  boite.appendChild(grande);
  document.body.appendChild(boite);
  var retour = null;
  function fermerBoite() {
    boite.hidden = true;
    grande.removeAttribute('src');
    if (retour) retour.focus();
  }
  document.addEventListener('click', function (e) {
    var z = e.target.closest && e.target.closest('[data-zoom]');
    if (z) {
      e.preventDefault();
      retour = z;
      grande.src = z.getAttribute('data-zoom');
      grande.alt = z.getAttribute('data-alt') || '';
      boite.hidden = false;
      boite.focus();
      return;
    }
    if (!boite.hidden && e.target.closest('.lightbox')) fermerBoite();
  });
  boite.tabIndex = -1;
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !boite.hidden) fermerBoite();
  });

  /* ---- Recherche ---- */
  var fenetre = document.querySelector('[data-search]');
  var champ = fenetre && fenetre.querySelector('input');
  var liste = fenetre && fenetre.querySelector('[data-search-results]');
  var index = null;
  var choix = 0;
  var ouvreur = null;

  function charger() {
    if (index) return Promise.resolve(index);
    return fetch('/assets/search.json')
      .then(function (r) {
        return r.json();
      })
      .then(function (d) {
        index = d;
        return d;
      });
  }

  function normal(s) {
    return (s || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '');
  }

  function chercher(q) {
    var mots = normal(q).split(/\s+/).filter(Boolean);
    if (!mots.length) return index.slice(0, 8);
    return index
      .map(function (p) {
        var t = normal(p.t);
        var h = normal(p.h);
        var x = normal(p.x);
        var score = 0;
        for (var i = 0; i < mots.length; i++) {
          var m = mots[i];
          if (t.indexOf(m) > -1) score += 10;
          else if (h.indexOf(m) > -1) score += 4;
          else if (x.indexOf(m) > -1) score += 1;
          else return null;
        }
        return { p: p, s: score };
      })
      .filter(Boolean)
      .sort(function (a, b) {
        return b.s - a.s;
      })
      .slice(0, 12)
      .map(function (r) {
        return r.p;
      });
  }

  function afficher(resultats) {
    choix = 0;
    if (!resultats.length) {
      liste.innerHTML = '<li class="search__empty">No results. Try another word, or write to us from the Support page.</li>';
      return;
    }
    liste.innerHTML = resultats
      .map(function (p, i) {
        return (
          '<li><a href="' + p.u + '"' + (i === 0 ? ' class="is-active"' : '') + '><b>' + p.t + '</b><small>' + p.c + '</small></a></li>'
        );
      })
      .join('');
  }

  function ouvrir() {
    if (!fenetre) return;
    ouvreur = document.activeElement;
    fenetre.hidden = false;
    champ.value = '';
    charger().then(function () {
      afficher(chercher(''));
    });
    setTimeout(function () {
      champ.focus();
    }, 20);
  }
  function fermer() {
    fenetre.hidden = true;
    if (ouvreur && ouvreur.focus) ouvreur.focus();
  }

  if (fenetre) {
    document.querySelectorAll('[data-search-open]').forEach(function (b) {
      b.addEventListener('click', ouvrir);
    });
    fenetre.addEventListener('click', function (e) {
      if (e.target === fenetre) fermer();
    });
    champ.addEventListener('input', function () {
      charger().then(function () {
        afficher(chercher(champ.value));
      });
    });
    fenetre.addEventListener('keydown', function (e) {
      var items = liste.querySelectorAll('a');
      if (e.key === 'Escape') {
        e.preventDefault();
        fermer();
      } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (!items.length) return;
        items[choix].classList.remove('is-active');
        choix = (choix + (e.key === 'ArrowDown' ? 1 : items.length - 1)) % items.length;
        items[choix].classList.add('is-active');
        items[choix].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter' && items[choix] && document.activeElement === champ) {
        e.preventDefault();
        window.location.href = items[choix].getAttribute('href');
      }
    });
    document.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (fenetre.hidden) ouvrir();
        else fermer();
      } else if (e.key === '/' && fenetre.hidden && !/input|textarea|select/i.test(document.activeElement.tagName)) {
        e.preventDefault();
        ouvrir();
      }
    });
  }

  document.querySelectorAll('[data-year]').forEach(function (n) {
    n.textContent = new Date().getFullYear();
  });
})();

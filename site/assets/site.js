/* Zeppelin Studio — documentation d'Opaline : recherche, menu, sommaire.
   Aucune dependance. */
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
      var raccourci = (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k';
      var barre = e.key === '/' && fenetre.hidden && !/input|textarea|select/i.test(document.activeElement.tagName);
      if (!raccourci && !barre) return;
      e.preventDefault();
      // A l'accueil, la recherche est dans la page : on y place le curseur.
      if (quete && fenetre.hidden) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        quete.querySelector('input').focus();
      } else if (raccourci && !fenetre.hidden) fermer();
      else ouvrir();
    });
  }

  /* ---- Accueil : la recherche au centre de la page ---- */
  var quete = document.querySelector('[data-quete]');
  if (quete) {
    var qChamp = quete.querySelector('input');
    var qListe = quete.querySelector('[role="listbox"]');
    var qChoix = -1;

    var echappe = function (t) {
      return String(t).replace(/[&<>"]/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
      });
    };
    // Les mots cherches, soulignes dans le titre du resultat.
    var souligne = function (titre, q) {
      var t = normal(titre);
      var zones = [];
      normal(q).split(/\s+/).filter(Boolean).forEach(function (m) {
        var i = t.indexOf(m);
        if (i > -1) zones.push([i, i + m.length]);
      });
      zones.sort(function (a, b) {
        return a[0] - b[0];
      });
      var out = '';
      var pos = 0;
      zones.forEach(function (z) {
        if (z[0] < pos) return;
        out += echappe(titre.slice(pos, z[0])) + '<mark>' + echappe(titre.slice(z[0], z[1])) + '</mark>';
        pos = z[1];
      });
      return out + echappe(titre.slice(pos));
    };
    var deplier = function (ouvert) {
      qListe.hidden = !ouvert;
      qChamp.setAttribute('aria-expanded', String(ouvert));
      if (!ouvert) {
        qChoix = -1;
        qChamp.removeAttribute('aria-activedescendant');
      }
    };
    var marquer = function (i) {
      var items = qListe.querySelectorAll('[role="option"]');
      if (!items.length) return;
      qChoix = (i + items.length) % items.length;
      items.forEach(function (li, k) {
        li.setAttribute('aria-selected', String(k === qChoix));
      });
      qChamp.setAttribute('aria-activedescendant', items[qChoix].id);
      items[qChoix].scrollIntoView({ block: 'nearest' });
    };
    var rendre = function () {
      var q = qChamp.value.trim();
      if (!q) return deplier(false);
      charger().then(function () {
        if (qChamp.value.trim() !== q) return;
        var res = chercher(q);
        qChoix = -1;
        qListe.innerHTML = res.length
          ? res
              .map(function (p, i) {
                return '<li role="option" id="quete-' + i + '" aria-selected="false"><a href="' + p.u + '" tabindex="-1"><b>' +
                  souligne(p.t, q) + '</b><small>' + echappe(p.c) + '</small></a></li>';
              })
              .join('')
          : '<li class="quete__vide" role="presentation">No results for \u201c' + echappe(q) +
            '\u201d. Try another word, or <a href="/support">write to us</a>.</li>';
        deplier(true);
      });
    };

    qChamp.addEventListener('input', rendre);
    qChamp.addEventListener('focus', function () {
      charger();
      if (qChamp.value.trim()) rendre();
    });
    qChamp.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        if (qListe.hidden) return;
        e.preventDefault();
        if (qChoix === -1) marquer(e.key === 'ArrowDown' ? 0 : -1);
        else marquer(qChoix + (e.key === 'ArrowDown' ? 1 : -1));
      } else if (e.key === 'Enter') {
        var liens = qListe.querySelectorAll('[role="option"] a');
        var cible = liens[qChoix > -1 ? qChoix : 0];
        if (cible && !qListe.hidden) {
          e.preventDefault();
          window.location.href = cible.getAttribute('href');
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        if (!qListe.hidden) deplier(false);
        else qChamp.value = '';
      }
    });
    document.addEventListener('click', function (e) {
      if (!quete.contains(e.target)) deplier(false);
    });
    document.querySelectorAll('[data-requete]').forEach(function (b) {
      b.addEventListener('click', function () {
        qChamp.value = b.getAttribute('data-requete');
        qChamp.focus();
        rendre();
      });
    });
  }

  /* ---- Accueil : filtres et rail des sections ---- */
  var rail = document.querySelector('[data-rail]');
  if (rail) {
    document.querySelectorAll('[data-filtres] button').forEach(function (b) {
      b.addEventListener('click', function () {
        var cat = b.getAttribute('data-filtre');
        document.querySelectorAll('[data-filtres] button').forEach(function (x) {
          x.setAttribute('aria-pressed', String(x === b));
        });
        rail.querySelectorAll('[data-cat]').forEach(function (c) {
          c.hidden = cat !== 'all' && c.getAttribute('data-cat') !== cat;
        });
        rail.scrollTo({ left: 0, behavior: 'smooth' });
      });
    });
    var pas = function (sens) {
      var carte = rail.querySelector('.rail__card:not([hidden])');
      var largeur = carte ? carte.getBoundingClientRect().width + 16 : 360;
      rail.scrollBy({ left: sens * largeur * 2, behavior: 'smooth' });
    };
    var prec = document.querySelector('[data-rail-prev]');
    var suiv = document.querySelector('[data-rail-next]');
    if (prec) prec.addEventListener('click', function () { pas(-1); });
    if (suiv) suiv.addEventListener('click', function () { pas(1); });
  }

  document.querySelectorAll('[data-year]').forEach(function (n) {
    n.textContent = new Date().getFullYear();
  });
})();

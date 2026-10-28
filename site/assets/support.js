/* Formulaire de support : repris tel quel de la version precedente du site. */
(function () {

    

    /* Copie de l'adresse. L'API presse-papiers n'est offerte qu'en contexte
       sécurisé ; en son absence on se rabat sur une sélection classique. */
    document.querySelectorAll('[data-copy]').forEach(function (b) {
      b.addEventListener('click', function () {
        var texte = b.getAttribute('data-copy');
        var initial = b.textContent;
        var fini = function () {
          b.textContent = 'Copied';
          setTimeout(function () { b.textContent = initial; }, 1800);
        };
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(texte).then(fini, function () {});
          return;
        }
        var z = document.createElement('textarea');
        z.value = texte;
        z.style.cssText = 'position:fixed;left:-9999px';
        document.body.appendChild(z);
        z.select();
        try { document.execCommand('copy'); fini(); } catch (e) {}
        z.remove();
      });
    });

    /* Envoi du formulaire.
       Deux chemins : si un point de collecte est configuré, on envoie en
       arrière-plan et l'on reste sur la page ; sinon on compose un message
       dans le client mail du visiteur avec ce qu'il a saisi. Dans les deux
       cas il n'a pas à ressaisir quoi que ce soit. */
    (function () {
      var f = document.querySelector('[data-cform]');
      if (!f) return;
      var etat = f.querySelector('[data-cform-status]');
      var bouton = f.querySelector('button[type="submit"]');
      var configure = f.getAttribute('action').indexOf('REMPLACER_PAR_VOTRE_ID') === -1;

      function dire(texte, ok) {
        etat.textContent = texte;
        etat.className = 'cform__status cform__status--' + (ok ? 'ok' : 'ko');
        etat.hidden = false;
      }

      function manquant() {
        var vides = [];
        [['cf-name', 'your name'], ['cf-email', 'your email'], ['cf-store', 'your store URL'], ['cf-message', 'a description of the problem']].forEach(function (p) {
          if (!f.querySelector('#' + p[0]).value.trim()) vides.push(p[1]);
        });
        var mail = f.querySelector('#cf-email').value.trim();
        if (mail && mail.indexOf('@') < 1) vides.push('a valid email address');
        return vides;
      }

      f.addEventListener('submit', function (e) {
        e.preventDefault();
        if (f.querySelector('#cf-company').value) return;   // robot

        var vides = manquant();
        if (vides.length) {
          dire('Still missing: ' + vides.join(', ') + '.', false);
          return;
        }

        var d = new FormData(f);

        if (!configure) {
          var corps =
            'Name: ' + d.get('name') + '\n' +
            'Email: ' + d.get('email') + '\n' +
            'Store: ' + d.get('store') + '\n\n' +
            d.get('message');
          window.location.href =
            'mailto:' + f.getAttribute('data-mailto') +
            '?subject=' + encodeURIComponent('[Zeppelin] ' + d.get('topic')) +
            '&body=' + encodeURIComponent(corps);
          dire('Your mail app should be opening, with everything already filled in. If nothing happens, write to us at ' + f.getAttribute('data-mailto') + '.', true);
          return;
        }

        /* Objet du mail de notification : sans lui, tous les messages
           arrivent sous le même intitulé et la boîte devient illisible.
           L'adresse de réponse, elle, est déduite du champ « email ». */
        d.set('_subject', '[Zeppelin] ' + d.get('topic'));

        /* Un champ fichier vide envoie tout de meme une entree multipart, et
           tous les points de collecte n'acceptent pas les pieces jointes. La
           requete echouait alors, et le message ne partait pas — alors que le
           visiteur n'avait rien joint. On retire l'entree quand elle est vide. */
        var champFichier = f.querySelector('#cf-file');
        var aFichier = !!(champFichier && champFichier.files && champFichier.files.length);
        if (!aFichier) d.delete('attachment');

        function envoyer(charge) {
          return fetch(f.getAttribute('action'), {
            method: 'POST', body: charge, headers: { Accept: 'application/json' }
          }).then(function (r) { if (!r.ok) throw new Error(); });
        }

        /* Accusé de réception : envoyé par /api/accuse une fois le message
           accepté par Formspree. On retient les champs avant de vider le
           formulaire. Si l'envoi échoue, la demande est déjà partie : on
           n'annonce simplement pas de confirmation. */
        var accuse = {
          email: String(d.get('email') || ''),
          name: String(d.get('name') || ''),
          topic: String(d.get('topic') || ''),
          _gotcha: String(d.get('_gotcha') || '')
        };

        function reussi(message) {
          f.reset();
          dire(message, true);
          fetch('/api/accuse', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(accuse)
          })
            .then(function (r) { return r.ok; }, function () { return false; })
            .then(function (ok) {
              if (ok) dire(message + ' A confirmation is on its way to ' + accuse.email + '.', true);
            });
        }

        function echoue() {
          dire('The message could not be sent. Write to us directly at ' + f.getAttribute('data-mailto') + '.', false);
        }

        bouton.setAttribute('aria-busy', 'true');
        envoyer(d)
          .then(function () {
            reussi('Message sent. We’ll get back to you within one to two business days.');
          })
          .catch(function () {
            /* Un envoi refuse alors qu'un fichier etait joint ne doit pas
               couter son message au visiteur : on renvoie sans la piece, et on
               lui dit ou l'adresser. */
            if (!aFichier) { echoue(); return; }
            var sansPiece = new FormData(f);
            sansPiece.delete('attachment');
            sansPiece.set('_subject', '[Zeppelin] ' + d.get('topic'));
            return envoyer(sansPiece).then(function () {
              reussi('Message sent — the file could not be attached, so please email it to '
                + f.getAttribute('data-mailto') + ' if it helps.');
            }).catch(echoue);
          })
          .then(function () { bouton.removeAttribute('aria-busy'); });
      });
    })();
  
})();

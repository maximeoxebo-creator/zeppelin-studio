/*
  Serveur du site Zeppelin Studio : la documentation d'Opaline, statique,
  et le point d'envoi de l'accuse de reception du formulaire de support.

  Il reprend ce que faisait Vercel : adresses sans « .html », sans barre
  finale, et /api/accuse. Toute autre adresse en .zeppelin-apps.com que
  DOMAINE y est renvoyee. Aucune dependance hors nodemailer, utilise par
  l'accuse.

  Variables d'environnement (reglages de l'application dans Coolify) :
    PORT                port d'ecoute (3000 par defaut)
    GMAIL_USER          adresse Gmail d'envoi de l'accuse
    GMAIL_APP_PASSWORD  mot de passe d'application Google
*/
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const accuse = require('./api/accuse');

const RACINE = path.join(__dirname, 'site');
// Adresse du site. L'ancienne (zeppelin-studio.zeppelin-apps.com) y renvoie
// pour toujours : elle figure dans des versions publiees du theme.
const DOMAINE = 'opaline.zeppelin-apps.com';
const PORT = Number(process.env.PORT) || 3000;

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
};

const ENTETES = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'X-Frame-Options': 'SAMEORIGIN',
};

function cache(ext) {
  if (ext === '.woff2') return 'public, max-age=31536000, immutable';
  if (ext === '.html' || ext === '.json' || ext === '.xml') return 'public, max-age=0, s-maxage=300';
  return 'public, max-age=86400';
}

// Pendant un deploiement, l'ancien et le nouveau conteneur repondent tous
// les deux : une page neuve peut demander site.css?v=<nouvelle empreinte> a
// l'ancien, qui renvoie l'ancien fichier. Cloudflare le gardait alors un jour
// sous la nouvelle adresse. Une empreinte qui ne correspond pas au fichier
// servi n'est donc jamais mise en cache.
function servir(res, fichier, code, version) {
  const ext = path.extname(fichier);
  fs.readFile(fichier, (err, donnees) => {
    if (err) return introuvable(res);
    const perimee = version && !crypto.createHash('sha1').update(donnees).digest('hex').startsWith(version);
    res.writeHead(code || 200, Object.assign({}, ENTETES, {
      'Content-Type': TYPES[ext] || 'application/octet-stream',
      'Cache-Control': perimee ? 'no-store' : cache(ext),
    }));
    res.end(donnees);
  });
}

function introuvable(res) {
  const page = path.join(RACINE, '404.html');
  fs.readFile(page, (err, donnees) => {
    res.writeHead(404, Object.assign({}, ENTETES, { 'Content-Type': 'text/html; charset=utf-8' }));
    res.end(err ? 'Not found' : donnees);
  });
}

function rediriger(res, code, cible) {
  res.writeHead(code, { Location: cible });
  res.end();
}

function existe(f) {
  try {
    return fs.statSync(f).isFile();
  } catch (e) {
    return false;
  }
}

http
  .createServer((req, res) => {
    let url;
    try {
      url = new URL(req.url, 'http://local');
    } catch (e) {
      return introuvable(res);
    }
    let chemin;
    try {
      chemin = decodeURIComponent(url.pathname);
    } catch (e) {
      return introuvable(res);
    }

    const hote = (req.headers.host || '').split(':')[0];
    if (hote.endsWith('.zeppelin-apps.com') && hote !== DOMAINE) {
      return rediriger(res, 301, 'https://' + DOMAINE + url.pathname + url.search);
    }

    if (chemin === '/api/accuse') return accuse(req, res);
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      res.writeHead(405);
      return res.end();
    }

    // /page.html -> /page ; /page/ -> /page (comme cleanUrls et trailingSlash: false)
    if (/\.html$/.test(chemin)) {
      const propre = chemin.replace(/(index)?\.html$/, '').replace(/\/$/, '') || '/';
      return rediriger(res, 308, propre + url.search);
    }
    if (chemin.length > 1 && chemin.endsWith('/')) return rediriger(res, 308, chemin.slice(0, -1) + url.search);

    // Pas de sortie du dossier du site.
    const cible = path.normalize(path.join(RACINE, chemin));
    if (!cible.startsWith(RACINE)) return introuvable(res);

    if (chemin === '/') return servir(res, path.join(RACINE, 'index.html'));
    if (existe(cible)) return servir(res, cible, 200, url.searchParams.get('v'));
    if (existe(cible + '.html')) return servir(res, cible + '.html');
    return introuvable(res);
  })
  .listen(PORT, () => {
    console.log('Zeppelin Studio sur le port ' + PORT);
  });

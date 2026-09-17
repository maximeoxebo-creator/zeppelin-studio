/*
  Accusé de réception du formulaire de support.

  Le Theme Store exige qu'une réponse automatique parte après chaque
  demande. Formspree la réserve à ses offres payantes : ce point d'envoi la
  fait partir depuis la boîte du studio, par le SMTP de Gmail.

  Le formulaire l'appelle après que Formspree a accepté le message — la
  demande elle-même ne dépend donc jamais de cette fonction.

  Une adresse qui envoie des e-mails à la demande attire les abus. D'où :
  un texte fixe (rien de ce que tape le visiteur n'y figure, hormis un
  prénom nettoyé et un sujet pris dans une liste fermée), une origine
  vérifiée, le champ piège, et une limite par adresse et par IP.

  Variables d'environnement (réglages Vercel du projet) :
    GMAIL_USER          adresse Gmail d'envoi
    GMAIL_APP_PASSWORD  mot de passe d'application Google (16 caractères)
*/
const nodemailer = require('nodemailer');

const SUJETS = [
  'Installation',
  'A setting or a section',
  'Something looks wrong',
  'Customisation request',
  'Licence & invoicing',
  'Something else',
];

// Limites « au mieux » : la mémoire d'une instance ne survit pas à sa fin,
// mais suffit à casser une rafale.
const parAdresse = new Map(); // adresse -> horodatage du dernier envoi
const parIp = new Map();      // ip -> horodatages de la dernière heure
const DIX_MINUTES = 10 * 60 * 1000;
const UNE_HEURE = 60 * 60 * 1000;

function repondre(res, code, corps) {
  res.statusCode = code;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(corps));
}

function lireCorps(req) {
  if (req.body && typeof req.body === 'object') return Promise.resolve(req.body);
  return new Promise((ok) => {
    let brut = '';
    req.on('data', (c) => { brut += c; if (brut.length > 10000) req.destroy(); });
    req.on('end', () => { try { ok(JSON.parse(brut || '{}')); } catch (e) { ok({}); } });
    req.on('error', () => ok({}));
  });
}

function origineAutorisee(req) {
  const origine = req.headers.origin || '';
  const hote = req.headers['x-forwarded-host'] || req.headers.host || '';
  if (!origine || !hote) return false;
  if (origine === 'https://' + hote) return true;
  // En local (vercel dev), le site est servi en http.
  return /^(127\.0\.0\.1|localhost)(:\d+)?$/.test(hote) && origine === 'http://' + hote;
}

function adresseValide(a) {
  return typeof a === 'string' && a.length <= 254 && /^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[a-z]{2,}$/i.test(a);
}

function nettoyerNom(n) {
  if (typeof n !== 'string') return '';
  return n.replace(/[\r\n\t<>]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 60);
}

module.exports = async function (req, res) {
  if (req.method !== 'POST') return repondre(res, 405, { ok: false });
  if (!origineAutorisee(req)) return repondre(res, 403, { ok: false });

  const corps = await lireCorps(req);
  if (corps._gotcha) return repondre(res, 200, { ok: true }); // robot : on ne dit rien

  const adresse = typeof corps.email === 'string' ? corps.email.trim() : '';
  if (!adresseValide(adresse)) return repondre(res, 400, { ok: false });

  const utilisateur = process.env.GMAIL_USER;
  const motDePasse = process.env.GMAIL_APP_PASSWORD;
  if (!utilisateur || !motDePasse) return repondre(res, 503, { ok: false, raison: 'non-configure' });

  const maintenant = Date.now();
  const cle = adresse.toLowerCase();
  if (parAdresse.has(cle) && maintenant - parAdresse.get(cle) < DIX_MINUTES) {
    return repondre(res, 429, { ok: false });
  }
  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'inconnue';
  const recents = (parIp.get(ip) || []).filter((t) => maintenant - t < UNE_HEURE);
  if (recents.length >= 5) return repondre(res, 429, { ok: false });

  const nom = nettoyerNom(corps.name);
  const sujet = SUJETS.includes(corps.topic) ? corps.topic : 'your request';

  const texte = [
    nom ? `Hello ${nom},` : 'Hello,',
    '',
    `Thank you for contacting Zeppelin Studio. Your message about "${sujet}" has reached us, and we will reply within one to two business days, Monday to Friday.`,
    '',
    'If your store is down or checkout is affected, reply to this email with URGENT in the subject line.',
    '',
    'In the meantime, the Opaline documentation covers most settings and questions:',
    'https://zeppelin-studio.vercel.app/docs',
    '',
    'Zeppelin Studio',
    'https://zeppelin-studio.vercel.app',
    '',
    '—',
    'This is an automatic confirmation. You can reply to it directly.',
  ].join('\n');

  try {
    const transport = nodemailer.createTransport({
      host: 'smtp.gmail.com',
      port: 465,
      secure: true,
      auth: { user: utilisateur, pass: motDePasse },
    });
    await transport.sendMail({
      from: { name: 'Zeppelin Studio', address: utilisateur },
      to: adresse,
      replyTo: utilisateur,
      subject: 'We received your message — Zeppelin Studio',
      text: texte,
      headers: { 'Auto-Submitted': 'auto-replied' },
    });
    parAdresse.set(cle, maintenant);
    recents.push(maintenant);
    parIp.set(ip, recents);
    return repondre(res, 200, { ok: true });
  } catch (e) {
    console.error('accuse: envoi impossible', e && e.code);
    return repondre(res, 502, { ok: false });
  }
};

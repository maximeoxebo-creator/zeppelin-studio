#!/usr/bin/env python3
"""Fabrique le site de documentation d'Opaline dans site/.

Les tableaux de reglages viennent directement des schemas du theme : ils
disent exactement ce que l'editeur affiche, et suivent le theme a chaque
version. Les textes rediges vivent dans contenu.py et guides.py.

    python3 outils/build.py [chemin-du-theme] [dossier-des-captures]
"""

import hashlib
import glob
import html
import json
import os
import re
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import contenu  # noqa: E402
import guides  # noqa: E402
import schemas  # noqa: E402

RACINE = os.path.dirname(ICI)
SITE = os.path.join(RACINE, 'site')
THEME = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Documents/la-fonderie-v2')
CAPTURES = sys.argv[2] if len(sys.argv) > 2 else None
URL_SITE = 'https://opaline.zeppelin-apps.com'


# ── Lecture du theme ──────────────────────────────────────────────────

def charge(p):
    t = open(p, encoding='utf-8').read()
    return json.loads(re.sub(r'^\s*/\*.*?\*/', '', t, flags=re.S))


TRAD = charge(os.path.join(THEME, 'locales', 'en.default.schema.json'))


def trad(v):
    """Resout une cle `t:...` du schema en anglais."""
    if isinstance(v, str) and v.startswith('t:'):
        cur = TRAD
        for k in v[2:].split('.'):
            cur = cur.get(k, {}) if isinstance(cur, dict) else {}
        return cur if isinstance(cur, str) else v
    return v


SCHEMAS = {}
for f in sorted(glob.glob(os.path.join(THEME, 'sections', '*.liquid'))):
    m = re.search(r'{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema', open(f, encoding='utf-8').read(), re.S)
    if m:
        SCHEMAS[os.path.basename(f)[:-7]] = json.loads(m.group(1))

REGLAGES_THEME = charge(os.path.join(THEME, 'config', 'settings_schema.json'))
DONNEES = charge(os.path.join(THEME, 'config', 'settings_data.json'))
INFO = next(g for g in REGLAGES_THEME if g.get('name') == 'theme_info')
VERSION = INFO.get('theme_version', '')


def e(s):
    return html.escape(str(s), quote=True)


def slug(s):
    s = re.sub(r'[^a-z0-9]+', '-', str(s).lower().replace('&', 'and')).strip('-')
    return s


# ── Tableaux de reglages ──────────────────────────────────────────────

TYPES = {
    'checkbox': 'Toggle', 'range': 'Slider', 'select': 'Dropdown', 'radio': 'Choice',
    'text': 'Text', 'textarea': 'Text', 'richtext': 'Rich text', 'inline_richtext': 'Rich text',
    'html': 'HTML', 'liquid': 'Liquid', 'image_picker': 'Image', 'video': 'Video',
    'video_url': 'Video URL', 'url': 'Link', 'color': 'Color', 'color_background': 'Gradient',
    'color_scheme': 'Color scheme', 'color_scheme_group': 'Color schemes', 'font_picker': 'Font',
    'collection': 'Collection', 'product': 'Product', 'blog': 'Blog', 'page': 'Page',
    'article': 'Article', 'link_list': 'Menu', 'collection_list': 'Collections',
    'product_list': 'Products', 'number': 'Number', 'text_alignment': 'Alignment',
    'metaobject': 'Entry', 'metaobject_list': 'Entries',
}


def police(handle):
    nom = re.sub(r'_[nio]\d$', '', str(handle))
    return ' '.join(p.capitalize() for p in nom.split('_'))


def texte_option(s, valeur):
    for o in s.get('options', []):
        if o.get('value') == valeur:
            return trad(o.get('label'))
    return valeur


def condition(s, par_id):
    """Traduit un `visible_if` simple en phrase : « Shown when … »."""
    v = s.get('visible_if')
    if not v:
        return ''
    morceaux = []
    for clause in re.split(r'\s+and\s+', v.strip('{} ')):
        m = re.match(r"(?:section|block)\.settings\.(\w+)\s*(==|!=)\s*'([^']*)'", clause.strip())
        if m:
            cible = par_id.get(m.group(1))
            if not cible:
                return ''
            nom = trad(cible.get('label')) or m.group(1)
            val = texte_option(cible, m.group(3))
            mot = 'is' if m.group(2) == '==' else 'is not'
            morceaux.append(f'<strong>{e(nom)}</strong> {mot} {e(val)}')
            continue
        m = re.match(r'(?:section|block)\.settings\.(\w+)$', clause.strip())
        if m and par_id.get(m.group(1)):
            cible = par_id[m.group(1)]
            nom = trad(cible.get('label')) or m.group(1)
            if cible.get('type') == 'checkbox':
                morceaux.append(f'<strong>{e(nom)}</strong> is on')
            else:
                morceaux.append(f'<strong>{e(nom)}</strong> is set')
            continue
        m = re.match(r'(?:section|block)\.settings\.(\w+)\s*==\s*(true|false)$', clause.strip())
        if m and par_id.get(m.group(1)):
            nom = trad(par_id[m.group(1)].get('label'))
            morceaux.append(f'<strong>{e(nom)}</strong> is {"on" if m.group(2) == "true" else "off"}')
            continue
        return ''
    return 'Shown when ' + ' and '.join(morceaux) + '.' if morceaux else ''


def puces(s):
    """Options, plage et valeur par defaut d'un reglage."""
    t = s.get('type')
    out = []
    d = s.get('default')
    if t in ('select', 'radio'):
        opts = [trad(o.get('label')) for o in s.get('options', [])]
        if d is not None:
            out.append(('default', 'Default: ' + str(texte_option(s, d))))
        others = [o for o in opts if o != texte_option(s, d)]
        for o in others[:12]:
            out.append(('', o))
        if len(others) > 12:
            out.append(('', f'+{len(others) - 12} more'))
    elif t == 'checkbox':
        out.append(('default', 'Default: ' + ('On' if d else 'Off')))
    elif t == 'range':
        u = trad(s.get('unit') or '')
        out.append(('default', f'Default: {d}{u}'))
        out.append(('', f"From {s.get('min')} to {s.get('max')}{u}, in steps of {s.get('step', 1)}"))
    elif t == 'color' and d:
        out.append(('swatch', d))
    elif t == 'font_picker' and d:
        out.append(('default', 'Default: ' + police(d)))
    elif t == 'number' and d is not None:
        out.append(('default', f'Default: {d}'))
    elif t == 'color_scheme' and d:
        out.append(('default', 'Default: ' + nom_schema(d)))
    return out


def nom_schema(cle):
    m = re.match(r'scheme-(\d+)', str(cle))
    return f'Scheme {m.group(1)}' if m else str(cle)


# Quand le schema ne dit rien, une phrase selon le type : toujours vraie,
# quelle que soit la section, pour qu'aucune ligne ne reste muette.
PAR_DEFAUT = {
    'image_picker': 'Select an image from your Files, or upload a new one.',
    'video': 'Select a video from your Files, or upload a new one.',
    'video_url': 'Paste a YouTube or Vimeo link.',
    'url': 'Where the link leads: a product, a collection, a page, or any web address.',
    'product': 'Choose one of your products.',
    'collection': 'Choose one of your collections.',
    'collection_list': 'Choose the collections to show.',
    'product_list': 'Choose the products to show.',
    'link_list': 'Choose a menu. Menus are edited in Shopify admin > Content > Menus.',
    'page': 'Choose one of your pages.',
    'blog': 'Choose one of your blogs.',
    'article': 'Choose a blog post.',
    'text': 'The text shown in this place.',
    'textarea': 'The text shown in this place.',
    'richtext': 'Formatted text: bold, italic and links are kept.',
    'inline_richtext': 'Text on one line; bold, italic and links are kept.',
    'html': 'Your own HTML.',
    'liquid': 'Your own Liquid code.',
    'color': 'Pick a color, or type its hex code.',
    'color_background': 'A CSS background, for example a gradient.',
    'color_scheme': 'The color scheme of the section. Schemes are set under Theme settings > Colors.',
    'font_picker': 'Choose a font from the Shopify font library.',
    'checkbox': 'Turn on or off.',
    'number': 'A number.',
}


def ligne_reglage(s, par_id):
    label = trad(s.get('label')) or s.get('id')
    info = trad(s.get('info')) or PAR_DEFAUT.get(s.get('type'), '')
    typ = TYPES.get(s.get('type'), s.get('type', '').replace('_', ' ').capitalize())
    desc = f'<p>{info}</p>' if info else ''
    cond = condition(s, par_id)
    chips = []
    for genre, txt in puces(s):
        if genre == 'swatch':
            chips.append(f'<span class="chip chip--default"><span class="chip__swatch" style="background:{e(txt)}"></span>Default: {e(txt)}</span>')
        elif genre == 'default':
            chips.append(f'<span class="chip chip--default">{e(txt)}</span>')
        else:
            chips.append(f'<span class="chip">{e(txt)}</span>')
    meta = f'<div class="setting__meta">{"".join(chips)}</div>' if chips else ''
    when = f'<span class="when">{cond}</span>' if cond else ''
    if not desc and not meta and not when:
        desc = '<p>&nbsp;</p>'
    return (f'<div class="setting"><div class="setting__name">{e(label)}<br><span class="setting__type">{e(typ)}</span></div>'
            f'<div class="setting__desc">{desc}{meta}{when}</div></div>')


def tableau(reglages, titre_defaut='General'):
    """Groupes de reglages, coupes aux en-tetes du schema."""
    par_id = {s['id']: s for s in reglages if s.get('id')}
    groupes = []
    courant = [titre_defaut, []]
    for s in reglages:
        t = s.get('type')
        if t == 'header':
            if courant[1]:
                groupes.append(courant)
            courant = [trad(s.get('content')) or 'Settings', []]
            if s.get('info'):
                courant[1].append(f'<div class="setting setting--note">{trad(s.get("info"))}</div>')
            continue
        if t == 'paragraph':
            courant[1].append(f'<div class="setting setting--note">{trad(s.get("content"))}</div>')
            continue
        courant[1].append(ligne_reglage(s, par_id))
    if courant[1]:
        groupes.append(courant)
    out = []
    for titre, lignes in groupes:
        out.append(f'<div class="settings-group"><p class="settings-group__title">{e(titre)}</p>'
                   f'<div class="settings glass">{"".join(lignes)}</div></div>')
    return ''.join(out)


# ── Briques de mise en page ───────────────────────────────────────────

def note(texte, genre='note'):
    icone = 'i' if genre == 'note' else '✦'
    label = 'Good to know' if genre == 'note' else 'Tip'
    return (f'<div class="note glass note--{genre}"><span class="note__icon" aria-hidden="true">{icone}</span>'
            f'<div><span class="note__label">{label}</span><p>{texte}</p></div></div>')


def etapes(liste):
    return '<ol class="steps">' + ''.join(f'<li>{x}</li>' for x in liste) + '</ol>'


def taille(rel):
    """Largeur et hauteur d'une image du site, pour reserver sa place."""
    from PIL import Image
    with Image.open(os.path.join(SITE, rel.lstrip('/'))) as im:
        return im.size


def vignette_capture(chemin, alt, telephone=False):
    l, h = taille(chemin)
    img = f'<img src="{chemin}" alt="{e(alt)}" width="{l}" height="{h}" loading="lazy">'
    if telephone:
        cadre = f'<div class="shot__phone">{img}</div>'
    else:
        cadre = f'<div class="shot__desk"><div class="shot__chrome" aria-hidden="true"><i></i><i></i><i></i></div>{img}</div>'
    quoi = 'mobile' if telephone else 'desktop'
    return (f'<button type="button" class="shot__zoom" data-zoom="{chemin}" data-alt="{e(alt)}" '
            f'aria-label="Enlarge the {quoi} screenshot">{cadre}</button>')


def figure(nom, legende='', dossier='sections', seul=False, alt='', nue=False):
    """Capture ordinateur, et telephone a cote, chacune a son format naturel :
    ni recadrage ni zoom."""
    bureau = f'/img/{dossier}/{nom}-desktop.webp'
    tel = f'/img/{dossier}/{nom}-mobile.webp'
    a_bureau = os.path.exists(os.path.join(SITE, bureau[1:]))
    a_tel = os.path.exists(os.path.join(SITE, tel[1:])) and not seul
    if not a_bureau and not a_tel:
        return ''
    alt = alt or legende or nom
    parties = []
    if a_bureau:
        parties.append(vignette_capture(bureau, alt + ' — desktop'))
    if a_tel:
        parties.append(vignette_capture(tel, alt + ' — mobile', telephone=True))
    duo = ' shot__stage--duo' if a_bureau and a_tel else ''
    scene = f'<div class="shot__stage{duo} glass">{"".join(parties)}</div>'
    if nue:
        return scene
    cap = f'<figcaption>{legende}</figcaption>' if legende else ''
    return f'<figure class="shot">{scene}{cap}</figure>'


# Captures sans interet pour illustrer la section : le schema suffit.
SANS_CAPTURE = {'main-page', 'page', 'lf-divider', 'custom-liquid', 'apps', 'email-signup-banner'}


def anatomie(h, nom):
    """Schema au trait de la section et sa legende ; la capture de la demo,
    quand elle apporte quelque chose, dans un second onglet."""
    if h not in schemas.S:
        return figure(h, alt=f'The {nom} section on the Opaline demo store', seul=True)
    planche = (f'<div class="planche glass">{schemas.svg(h, titre=f"Diagram of the {nom} section")}'
               + '<ol class="legende">'
               + ''.join(f'<li><b>{n}</b><span>{e(t)}</span></li>' for n, t in schemas.LEGENDES.get(h, []))
               + '</ol></div>')
    capture = '' if h in SANS_CAPTURE else figure(h, alt=f'The {nom} section on the Opaline demo store', seul=True, nue=True)
    if not capture:
        return f'<figure class="anatomie">{planche}</figure>'
    return (f'<figure class="anatomie" data-vues>'
            f'<div class="vue glass" role="tablist" aria-label="Illustration">'
            f'<button type="button" role="tab" id="vue-{h}-s" aria-selected="true" aria-controls="pan-{h}-s">Diagram</button>'
            f'<button type="button" role="tab" id="vue-{h}-d" aria-selected="false" aria-controls="pan-{h}-d" tabindex="-1">Demo store</button></div>'
            f'<div role="tabpanel" id="pan-{h}-s" aria-labelledby="vue-{h}-s">{planche}</div>'
            f'<div role="tabpanel" id="pan-{h}-d" aria-labelledby="vue-{h}-d" hidden>{capture}</div></figure>')


def planche(h, legende=''):
    """Illustration au trait dans un guide."""
    cap = f'<figcaption>{legende}</figcaption>' if legende else ''
    return f'<figure class="anatomie"><div class="planche glass">{schemas.svg(h, titre=legende)}</div>{cap}</figure>'


def ecrire_schemas():
    """Vignettes au trait : sections (rail de l'accueil) et guides (mosaique)."""
    dossier = os.path.join(SITE, 'img', 'schemas')
    os.makedirs(dossier, exist_ok=True)
    for f in glob.glob(os.path.join(dossier, '*.svg')):
        os.remove(f)
    for h in schemas.S:
        encre = '#f6f5f2' if h.startswith('guide-') else '#111110'
        open(os.path.join(dossier, h + '.svg'), 'w', encoding='utf-8').write(schemas.svg(h, mini=True, encre=encre))


def image(chemin, alt, legende=''):
    if not os.path.exists(os.path.join(SITE, chemin.lstrip('/'))):
        return ''
    cap = f'<figcaption>{legende}</figcaption>' if legende else ''
    return (f'<figure class="shot"><div class="shot__stage shot__stage--single glass">'
            f'<button type="button" class="shot__zoom" data-zoom="{chemin}" data-alt="{e(alt)}" aria-label="Enlarge the screenshot">'
            f'<div class="shot__desk"><img src="{chemin}" alt="{e(alt)}" loading="lazy"></div></button></div>{cap}</figure>')


OUTILS = {'note': note, 'etapes': etapes, 'figure': figure, 'image': image, 'planche': planche, 'tableau': tableau,
          'schemas': SCHEMAS, 'trad': trad, 'e': e, 'version': VERSION, 'donnees': DONNEES}


# ── Navigation ────────────────────────────────────────────────────────

SECTIONS_DOC = []   # (handle, slug, nom, categorie)
for cle, titre, liste in contenu.CATEGORIES:
    for h in liste:
        s = SCHEMAS.get(h)
        if not s:
            continue
        SECTIONS_DOC.append((h, slug(trad(s.get('name'))), trad(s.get('name')), titre))

GROUPES_THEME = [g for g in REGLAGES_THEME if g.get('name') != 'theme_info']

NAV = [
    ('Get started', [
        ('Introduction', '/docs'),
        ('Install Opaline', '/docs/install'),
        ('Using the theme editor', '/docs/theme-editor'),
        ('Update Opaline', '/docs/update'),
        ('Before you go live', '/docs/launch-checklist'),
    ]),
    ('Guides', [(g['titre'], '/docs/guides/' + g['slug']) for g in guides.GUIDES]),
    ('Theme settings', [(g['name'], '/docs/settings/' + slug(g['name'])) for g in GROUPES_THEME]),
]
for cle, titre, liste in contenu.CATEGORIES:
    NAV.append(('Sections — ' + titre, [(n, '/docs/sections/' + sl) for h, sl, n, c in SECTIONS_DOC if c == titre]))
NAV.append(('Help', [('FAQ', '/docs/faq'), ("What's new", '/docs/changelog'), ('Contact support', '/support')]))

ORDRE = [u for _, liens in NAV for _, u in liens if u.startswith('/docs')]
TITRES = {u: t for _, liens in NAV for t, u in liens}


def barre_laterale(actuel):
    out = ['<nav class="sidebar glass" id="sidebar" aria-label="Documentation">']
    vu_sections = False
    for titre, liens in NAV:
        if titre.startswith('Sections — '):
            if not vu_sections:
                out.append('<div class="sidebar__group"><p class="sidebar__title">Sections</p>')
                vu_sections = True
            ouvert = ' open' if any(u == actuel for _, u in liens) else ''
            out.append(f'<details{ouvert}><summary>{e(titre[11:])}<small>{len(liens)}</small></summary><ul>')
            for t, u in liens:
                cur = ' aria-current="page"' if u == actuel else ''
                out.append(f'<li><a href="{u}"{cur}>{e(t)}</a></li>')
            out.append('</ul></details>')
            continue
        if vu_sections:
            out.append('</div>')
            vu_sections = False
        out.append(f'<div class="sidebar__group"><p class="sidebar__title">{e(titre)}</p><ul>')
        for t, u in liens:
            cur = ' aria-current="page"' if u == actuel else ''
            out.append(f'<li><a href="{u}"{cur}>{e(t)}</a></li>')
        out.append('</ul></div>')
    if vu_sections:
        out.append('</div>')
    out.append('</nav>')
    return ''.join(out)


def ids_titres(corps):
    """Pose un identifiant sur chaque h2/h3 et rend le sommaire."""
    vus = {}
    toc = []

    def pose(m):
        niveau, attrs, texte = m.group(1), m.group(2) or '', m.group(3)
        brut = re.sub(r'<[^>]+>', '', texte)
        if 'id="' in attrs:
            ident = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            ident = slug(brut) or 'section'
            n = vus.get(ident, 0)
            vus[ident] = n + 1
            if n:
                ident = f'{ident}-{n + 1}'
            attrs = f'{attrs} id="{ident}"'
        toc.append((niveau, ident, html.unescape(brut)))
        return f'<h{niveau}{attrs}>{texte}<a class="anchor" href="#{ident}" aria-label="Link to this heading">#</a></h{niveau}>'

    corps = re.sub(r'<h([23])((?:\s[^>]*)?)>(.*?)</h\1>', pose, corps, flags=re.S)
    return corps, toc


ICONE_LOUPE = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="6.5" stroke="currentColor" stroke-width="1.5"/><path d="M16 16l4.5 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'


def gabarit(*, titre, description, chemin, contenu_html, mise='docs', toc=None, fil=None, classe=''):
    """La page entiere : en-tete de verre, contenu, pied de page."""
    plein_titre = f'{titre} — Opaline documentation' if chemin != '/' else 'Opaline — Documentation & support by Zeppelin Studio'
    nav_actif = lambda p: ' aria-current="page"' if (chemin == p or (p != '/' and chemin.startswith(p) and p != '/docs')) else ''
    doc_actif = ' aria-current="page"' if (chemin.startswith('/docs') and '/guides' not in chemin and 'changelog' not in chemin) else ''
    entete = (
        '<a class="skip" href="#contenu">Skip to content</a>'
        '<div class="ambiance" aria-hidden="true"><span></span><span></span><span></span></div>'
        '<header class="site-header"><div class="site-header__bar glass">'
        '<a class="brand" href="/" aria-label="Zeppelin Studio — home"><img class="brand__mark" src="/assets/logo.svg" alt="" width="30" height="30">'
        '<span class="brand__name">Zeppelin Studio</span><span class="brand__theme">Opaline</span></a>'
        '<nav class="site-nav" aria-label="Main">'
        + '<a href="/docs"' + doc_actif + '>Documentation</a>'
        + '<a href="/docs/guides/product-page"' + nav_actif('/docs/guides') + '>Guides</a>'
        + '<a href="/docs/changelog"' + nav_actif('/docs/changelog') + ">What's new</a>"
        + '<a href="/support"' + nav_actif('/support') + '>Support</a></nav>'
        f'<button type="button" class="search-trigger" data-search-open aria-label="Search the documentation">{ICONE_LOUPE}<span>Search the docs</span><kbd>⌘K</kbd></button>'
        + ('<button type="button" class="menu-toggle" data-menu-toggle aria-expanded="false" aria-controls="sidebar" aria-label="Documentation menu">'
           '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 8h16M4 16h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>'
           if mise == 'docs' else '')
        + '</div></header>'
    )
    recherche = (
        '<div class="search" data-search hidden role="dialog" aria-modal="true" aria-label="Search the documentation">'
        '<div class="search__panel glass"><div class="search__field">' + ICONE_LOUPE +
        '<input type="search" placeholder="Search settings, sections, guides…" aria-label="Search" autocomplete="off"></div>'
        '<ul class="search__results" data-search-results></ul></div></div>'
    )
    pied = (
        '<footer class="pied"><div class="pied__inner glass">'
        '<div class="pied__brand"><a class="brand" href="/"><img class="brand__mark" src="/assets/logo.svg" alt="" width="30" height="30"><span class="brand__name">Zeppelin Studio</span></a>'
        '<p>Opaline is an editorial Shopify theme by Zeppelin Studio: large photography, fine serif headings and liquid glass.</p></div>'
        '<div><h3>Get started</h3><ul><li><a href="/docs">Introduction</a></li><li><a href="/docs/install">Install Opaline</a></li><li><a href="/docs/theme-editor">Theme editor</a></li><li><a href="/docs/update">Update</a></li></ul></div>'
        '<div><h3>Guides</h3><ul><li><a href="/docs/guides/product-page">Product page</a></li><li><a href="/docs/guides/quick-view">Quick view</a></li><li><a href="/docs/guides/cinematic-intro">Cinematic intro</a></li><li><a href="/docs/guides/liquid-glass">Liquid glass</a></li></ul></div>'
        '<div><h3>Help</h3><ul><li><a href="/docs/faq">FAQ</a></li><li><a href="/docs/changelog">What’s new</a></li><li><a href="/support">Contact support</a></li><li><a href="mailto:contact.zeppelin.studio@gmail.com">Email us</a></li></ul></div>'
        f'<div class="pied__bas"><span>© <span data-year>2026</span> Zeppelin Studio</span><span>Opaline {e(VERSION)} · Built for Shopify Online Store 2.0</span></div>'
        '</div></footer>'
    )
    if mise == 'docs':
        sommaire = ''
        if toc:
            items = ''.join(
                f'<li class="toc__h{n}"><a href="#{i}">{e(t)}</a></li>' for n, i, t in toc)
            sommaire = f'<aside class="toc" aria-label="On this page"><p class="toc__title">On this page</p><ul>{items}</ul></aside>'
        corps = (f'<div class="docs{"" if sommaire else " docs--wide"}">{barre_laterale(chemin)}'
                 f'<main class="content" id="contenu">{contenu_html}</main>{sommaire}</div>')
    else:
        corps = f'<main id="contenu">{contenu_html}</main>'
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{e(plein_titre)}</title>'
        f'<meta name="description" content="{e(description)}">'
        f'<link rel="canonical" href="{URL_SITE}{chemin}">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:title" content="{e(plein_titre)}">'
        f'<meta property="og:description" content="{e(description)}">'
        f'<meta property="og:image" content="{URL_SITE}/img/og.webp">'
        '<meta name="theme-color" content="#f3f3f1">'
        '<link rel="icon" href="/assets/logo.svg" type="image/svg+xml">'
        '<link rel="preload" href="/fonts/Fraunces-normal-300-latin.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="preload" href="/fonts/DMSans-normal-400-latin.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="stylesheet" href="/fonts/fonts.css">'
        '<link rel="stylesheet" href="/assets/site.css">'
        '<script src="/assets/site.js" defer></script>'
        f'</head><body class="{classe}">{entete}{corps}{pied}{recherche}</body></html>'
    )


def fil_ariane(liens):
    items = ''.join(f'<li><a href="{u}">{e(t)}</a></li>' if u else f'<li>{e(t)}</li>' for t, u in liens)
    return f'<ol class="crumbs" aria-label="Breadcrumb">{items}</ol>'


def pagination(chemin):
    if chemin not in ORDRE:
        return ''
    i = ORDRE.index(chemin)
    out = []
    if i > 0:
        p = ORDRE[i - 1]
        out.append(f'<a class="glass" href="{p}"><small>Previous</small><span>{e(TITRES[p])}</span></a>')
    if i < len(ORDRE) - 1:
        n = ORDRE[i + 1]
        out.append(f'<a class="glass pager__next" href="{n}"><small>Next</small><span>{e(TITRES[n])}</span></a>')
    return f'<nav class="pager" aria-label="Pages">{"".join(out)}</nav>'


PAGES = []   # (chemin, html, titre, categorie, texte)


def publie(chemin, titre, description, corps_html, categorie, mise='docs', avec_toc=True):
    corps_html, toc = ids_titres(corps_html)
    if mise == 'docs':
        corps_html += pagination(chemin)
    page = gabarit(titre=titre, description=description, chemin=chemin, contenu_html=corps_html,
                   mise=mise, toc=toc if (avec_toc and len(toc) > 2) else None,
                   classe='is-home' if chemin == '/' else '')
    texte = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', corps_html)))
    PAGES.append((chemin, page, titre, categorie, texte, ' · '.join(t for _, _, t in toc)))


def entete_page(titre, lead, fil, sur_titre=''):
    eyebrow = f'<p class="eyebrow">{e(sur_titre)}</p>' if sur_titre else ''
    return f'{fil_ariane(fil)}{eyebrow}<h1 class="page-title">{e(titre)}</h1><p class="lead">{lead}</p>'


# ── Pages de section ──────────────────────────────────────────────────

def disponibilite(h, s):
    on = s.get('enabled_on') or {}
    off = s.get('disabled_on') or {}
    gab = {'product': 'product', 'collection': 'collection', 'password': 'password', 'index': 'home',
           'page': 'page', 'cart': 'cart', 'search': 'search', 'blog': 'blog', 'article': 'article'}
    if on.get('templates'):
        return 'Available on the ' + ', '.join(gab.get(t, t) for t in on['templates']) + ' template only.'
    if off.get('groups'):
        return 'Available on every template. It cannot be placed in the header or footer.'
    return 'Available on every template.'


def page_section(h, sl, nom, categorie, prec_suiv=None):
    s = SCHEMAS[h]
    desc = contenu.DESCRIPTIONS.get(h, '')
    corps = [entete_page(nom, desc, [('Docs', '/docs'), ('Sections', None), (categorie, None)], categorie)]
    n_reg = len([x for x in s.get('settings', []) if x.get('id')])
    blocs_types = [b for b in s.get('blocks', []) if b.get('type') != '@app']
    n_blocs = sum(len([x for x in b.get('settings', []) if x.get('id')]) for b in blocs_types)
    coup = [f'<span><b>{n_reg}</b> section settings</span>']
    if blocs_types:
        coup.append(f'<span><b>{len(blocs_types)}</b> block type{"s" if len(blocs_types) > 1 else ""} · {n_blocs} settings</span>')
    if any(b.get('type') == '@app' for b in s.get('blocks', [])):
        coup.append('<span>Accepts <b>app blocks</b></span>')
    coup.append(f'<span>{e(disponibilite(h, s).rstrip("."))}</span>')
    corps.append(f'<div class="glance">{"".join(coup)}</div>')
    corps.append(anatomie(h, nom))
    corps.append('<div class="prose">')

    # Ajouter ou retrouver la section
    if s.get('presets'):
        corps.append('<h2>Add the section</h2>')
        corps.append(f'<p>{disponibilite(h, s)}</p>')
        corps.append(etapes([
            'From your Shopify admin, go to <strong>Online Store &gt; Themes</strong>, then click <strong>Customize</strong> next to Opaline.',
            'Use the page selector at the top of the editor to open the template you want to change.',
            'In the sidebar, click <strong>Add section</strong> where you want it to appear.',
            f'Select <strong>{e(nom)}</strong>. Click the section in the sidebar to open its settings.',
            'Click <strong>Save</strong> in the top right corner when you are done.',
        ]))
    else:
        corps.append('<h2>Find the section</h2>')
        if h in ('header', 'lf-announcement'):
            ou = 'It lives in the <strong>Header</strong> area at the top of the sidebar and appears on every page.'
        elif h == 'footer':
            ou = 'It lives in the <strong>Footer</strong> area at the bottom of the sidebar and appears on every page.'
        else:
            ou = 'It belongs to its page template and is already in place. Open that template with the page selector at the top of the editor, then click the section in the sidebar.'
        corps.append(f'<p>{ou}</p>')

    # Reglages
    if s.get('settings'):
        corps.append('<h2>Settings</h2>')
        corps.append(tableau(s['settings']))

    # Blocs
    blocs = [b for b in s.get('blocks', []) if b.get('type') != '@app']
    apps = any(b.get('type') == '@app' for b in s.get('blocks', []))
    if blocs or apps:
        corps.append('<h2>Blocks</h2>')
        if s.get('max_blocks'):
            corps.append(f'<p>Up to {s["max_blocks"]} blocks per section. Click <strong>Add block</strong> under the section in the sidebar, then drag blocks to reorder them.</p>')
        else:
            corps.append('<p>Click <strong>Add block</strong> under the section in the sidebar to add one, then drag blocks to reorder them.</p>')
        for b in blocs:
            bn = trad(b.get('name')) or b.get('type')
            lim = f'<span class="block-card__limit">Up to {b["limit"]} per section</span>' if b.get('limit') else ''
            corps.append(f'<div class="block-card"><div class="block-card__head"><h3>{e(bn)}</h3>{lim}</div>')
            if b.get('settings'):
                corps.append(tableau(b['settings']))
            else:
                corps.append('<p>This block has no settings.</p>')
            corps.append('</div>')
        if apps:
            corps.append(note('This section also accepts <strong>app blocks</strong>. Apps that offer blocks appear in the <strong>Add block</strong> menu once installed.'))

    conseils = contenu.CONSEILS.get(h)
    if conseils:
        corps.append('<h2>Good to know</h2>')
        for genre, txt in conseils:
            corps.append(note(txt, genre))
    corps.append('</div>')
    publie(f'/docs/sections/{sl}', nom, desc[:155], ''.join(corps), 'Section · ' + categorie)


# ── Pages des reglages du theme ───────────────────────────────────────

def page_reglages(g):
    nom = g['name']
    sl = slug(nom)
    extra = guides.REGLAGES_INTRO.get(nom, {})
    lead = extra.get('lead', f'The {nom} settings apply to the whole store.')
    corps = [entete_page(nom, lead, [('Docs', '/docs'), ('Theme settings', None)], 'Theme settings')]
    corps.append('<div class="prose">')
    corps.append('<h2>Open these settings</h2>')
    corps.append(etapes([
        'In the theme editor, click the <strong>Theme settings</strong> icon (the paintbrush) in the left toolbar.',
        f'Click <strong>{e(nom)}</strong> to expand the group.',
        'Changes preview instantly. Click <strong>Save</strong> to publish them.',
    ]))
    if extra.get('avant'):
        corps.append(extra['avant'](OUTILS))
    corps.append('<h2>Settings</h2>')
    reglages = g.get('settings', [])
    if len(reglages) == 1 and reglages[0].get('type') == 'color_scheme_group':
        corps.append(guides.schemas_couleurs(OUTILS, reglages[0]))
    else:
        corps.append(tableau(reglages))
    if extra.get('apres'):
        corps.append(extra['apres'](OUTILS))
    corps.append('</div>')
    publie(f'/docs/settings/{sl}', nom, lead[:155], ''.join(corps), 'Theme settings')


# ── Images ────────────────────────────────────────────────────────────

def images():
    """Convertit les captures PNG en WebP, aux tailles du site."""
    if not CAPTURES or not os.path.isdir(CAPTURES):
        return 0
    from PIL import Image
    n = 0
    for f in glob.glob(os.path.join(CAPTURES, '*.png')):
        nom = os.path.basename(f)[:-4]
        dossier = 'sections'
        if nom.startswith('guide-'):
            dossier = 'guides'
            nom = nom[6:]
        dest = os.path.join(SITE, 'img', dossier, nom + '.webp')
        if os.path.exists(dest) and os.path.getmtime(dest) > os.path.getmtime(f):
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        im = Image.open(f).convert('RGB')
        largeur = 1440 if nom.endswith('-desktop') or dossier == 'guides' else 780
        if im.width > largeur:
            im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
        # Une section tres haute est rognee : la capture montre son debut.
        plafond = 1700 if largeur == 1440 else 1600
        if im.height > plafond:
            im = im.crop((0, 0, im.width, plafond))
        im.save(dest, 'WEBP', quality=80, method=6)
        n += 1
    return n


# ── Assemblage ────────────────────────────────────────────────────────

ASSET = re.compile(r'(?<=["\'(])(/(?:assets|fonts|img)/[^"\'()?#\s]+\.(?:css|js|webp|png|jpg|svg))(?=["\')])')
_empreintes = {}


def versionne(page):
    """Ajoute l'empreinte du fichier a chaque adresse de feuille, script ou
    image : une nouvelle version a une nouvelle adresse, que ni Cloudflare
    ni le navigateur n'ont en cache (ils gardent ces fichiers un jour)."""
    def pose(m):
        rel = m.group(1)
        if rel not in _empreintes:
            f = os.path.join(SITE, rel.lstrip('/'))
            _empreintes[rel] = hashlib.sha1(open(f, 'rb').read()).hexdigest()[:10] if os.path.exists(f) else None
        return rel + ('?v=' + _empreintes[rel] if _empreintes[rel] else '')
    return ASSET.sub(pose, page)


def main():
    n = images()
    ecrire_schemas()
    shutil.copy(os.path.join(RACINE, 'logo.svg'), os.path.join(SITE, 'assets', 'logo.svg'))

    for h, sl, nom, cat in SECTIONS_DOC:
        page_section(h, sl, nom, cat)
    for g in GROUPES_THEME:
        page_reglages(g)
    for p in guides.pages(OUTILS, SECTIONS_DOC, GROUPES_THEME, slug):
        publie(p['chemin'], p['titre'], p['description'], p['corps'], p['categorie'],
               mise=p.get('mise', 'docs'), avec_toc=p.get('toc', True))

    # Ecriture : /docs/x -> site/docs/x.html (adresses sans extension)
    for f in glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True):
        os.remove(f)
    for chemin, page, *_ in PAGES:
        rel = 'index.html' if chemin == '/' else chemin.strip('/') + '.html'
        dest = os.path.join(SITE, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'w', encoding='utf-8').write(versionne(page))

    index = [{'t': titre, 'u': chemin, 'c': cat, 'h': h[:600], 'x': texte[:6000]}
             for chemin, page, titre, cat, texte, h in PAGES if chemin not in ('/', '/404')]
    json.dump(index, open(os.path.join(SITE, 'assets', 'search.json'), 'w', encoding='utf-8'), ensure_ascii=False)

    urls = ''.join(f'<url><loc>{URL_SITE}{c}</loc></url>' for c, *_ in PAGES if c != '/404')
    open(os.path.join(SITE, 'sitemap.xml'), 'w').write(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(SITE, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {URL_SITE}/sitemap.xml\n')
    print(f'{len(PAGES)} pages, {n} images converties, {len(SECTIONS_DOC)} sections documentees')


if __name__ == '__main__':
    main()

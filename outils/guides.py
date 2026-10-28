"""Pages redigees de la documentation d'Opaline : accueil, prise en main,
guides, FAQ, nouveautes et support.

Chaque nom de reglage cite ici est celui que l'editeur affiche, releve dans
les schemas du theme. Anglais americain.
"""

GUIDES = [
    {'slug': 'product-page', 'titre': 'Product page'},
    {'slug': 'quick-view', 'titre': 'Quick view & quick add'},
    {'slug': 'color-variants', 'titre': 'Color variants & swatches'},
    {'slug': 'navigation', 'titre': 'Navigation & mega menu'},
    {'slug': 'cinematic-intro', 'titre': 'Cinematic intro'},
    {'slug': 'templates', 'titre': 'Alternate templates'},
    {'slug': 'liquid-glass', 'titre': 'Liquid glass'},
    {'slug': 'mobile', 'titre': 'Mobile layouts'},
    {'slug': 'languages', 'titre': 'Languages & markets'},
    {'slug': 'accessibility', 'titre': 'Motion & accessibility'},
]


# ── Introductions des pages de reglages ───────────────────────────────

def _typo_avant(O):
    return (
        '<p>Opaline pairs a fine serif for headings with a clean sans-serif for text. Both come from the '
        'Shopify font library, so any pairing from that library can replace them.</p>'
        '<div class="table-wrap glass"><table class="simple"><thead><tr><th>Role</th><th>Default</th><th>Used for</th></tr></thead><tbody>'
        '<tr><td>Heading font</td><td><span style="font-family:var(--serif);font-size:2rem">Fraunces</span></td><td>Page titles, section headings, large statements.</td></tr>'
        '<tr><td>Body font</td><td><span style="font-family:var(--sans);font-size:1.6rem">DM Sans</span></td><td>Text, buttons, labels, prices and forms.</td></tr>'
        '<tr><td>Sans-serif heading font</td><td>Your choice</td><td>An optional sans-serif for headings, with its own weight and letter spacing. Use it store-wide or section by section.</td></tr>'
        '</tbody></table></div>'
        + O['note']('Most sections have their own <strong>Heading typeface</strong> setting. Leave it on <strong>Theme</strong> to follow this page, or switch one section to another typeface without touching the rest of the store.', 'tip')
    )


def _cartes_avant(O):
    return (
        O['planche']('guide-card-actions', 'A product card on hover: the quick view and quick add buttons in liquid glass, top right.')
        + '<p>Both buttons appear on every product card of the store: collection grids, featured collections, the scrolling product row, recommendations and search results. '
          'See the full guide: <a href="/docs/guides/quick-view">Quick view &amp; quick add</a>.</p>'
    )


REGLAGES_INTRO = {
    'Logo': {'lead': 'The logo and favicon used outside the header: on the password page, the gift card page, the age check and your search-engine listing. The header has its own logo settings.'},
    'Colors': {'lead': 'Color schemes are named sets of colors — background, text, buttons — that every section can use. Change a scheme once and every section using it follows.'},
    'Typography': {'lead': 'Choose the fonts of the store, their scale, and an optional sans-serif for headings.', 'avant': _typo_avant},
    'Layout': {'lead': 'Decide how far your content spreads on wide screens.'},
    'Product cards': {'lead': 'Turn on the quick view and quick add buttons shown on product cards.', 'avant': _cartes_avant},
    'Animations': {'lead': 'Turn the reveal of sections on scroll on or off. Visitors who ask their device to reduce motion never see the movement, whatever you choose here.'},
    'Social media': {'lead': 'Links to your social profiles, shown as icons in the footer and wherever a section offers social links.'},
}


def schemas_couleurs(O, reglage):
    """Explique chaque couleur d'un schema et montre ceux de la demo."""
    e = O['e']
    defs = reglage.get('definition', [])
    out = ['<p>Open <strong>Colors</strong>, then click a scheme to edit it or <strong>Add scheme</strong> to create one. Each scheme holds these colors:</p>']
    out.append('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Color</th><th>Where it shows</th></tr></thead><tbody>')
    usage = {
        'background': 'The section background.',
        'background_gradient': 'An optional gradient that replaces the background color.',
        'text': 'Headings and text.',
        'button': 'The fill of primary buttons.',
        'button_label': 'The text of primary buttons.',
        'secondary_button_label': 'Outline buttons and text links.',
        'shadow': 'Shadows of cards, buttons and panels.',
    }
    for d in defs:
        out.append(f'<tr><td>{e(O["trad"](d.get("label")))}</td><td>{usage.get(d.get("id"), "")}</td></tr>')
    out.append('</tbody></table></div>')
    schemas = (O['donnees'].get('current') or {}).get('color_schemes') or {}
    if schemas:
        out.append('<h3>The schemes of the demo store</h3><p>Opaline ships with these five schemes. Every section has a <strong>Color scheme</strong> setting that picks one of them.</p>')
        out.append('<div class="cards">')
        for cle, v in schemas.items():
            s = v.get('settings', {})
            bg, tx, bt, bl = s.get('background', '#fff'), s.get('text', '#000'), s.get('button', '#000'), s.get('button_label', '#fff')
            num = cle.split('-')[-1]
            out.append(
                f'<div class="card glass" style="padding:1.2rem"><div style="background:{bg};color:{tx};border-radius:1.4rem;padding:2.4rem 2rem;border:1px solid rgba(0,0,0,.08)">'
                f'<div style="font-family:var(--serif);font-size:3.2rem;line-height:1">Aa</div>'
                f'<div style="font-size:1.3rem;margin-top:.6rem;color:{tx}">Text and headings</div>'
                f'<span style="display:inline-block;margin-top:1.6rem;padding:.8rem 1.8rem;border-radius:999px;background:{bt};color:{bl};font-size:1.1rem;letter-spacing:.16em;text-transform:uppercase">Button</span></div>'
                f'<div class="card__title" style="font-size:2rem;margin:1.2rem .8rem .2rem">Scheme {e(num)}</div>'
                f'<div class="card__text" style="margin:0 .8rem .6rem">Background {e(bg)} · Text {e(tx)}</div></div>')
        out.append('</div>')
    out.append(O['note']('Text must stay readable on its background: 4.5:1 contrast for body text, 3:1 for large headings. Dark text on a light background, or the reverse, keeps every scheme legible.'))
    return ''.join(out)


# ── Pages ─────────────────────────────────────────────────────────────

POPULAIRES = [('Quick view', 'quick view'), ('Color swatches', 'swatches'), ('Mega menu', 'mega menu'), ('Cinematic intro', 'cinematic intro'), ('Product gallery', 'gallery'), ('Translations', 'languages'), ('Age verifier', 'age')]


def pages(O, SECTIONS_DOC, GROUPES, slug):
    e, note, etapes, planche = O['e'], O['note'], O['etapes'], O['planche']
    v = O['version']
    P = []

    def ajoute(chemin, titre, description, corps, categorie, **kw):
        d = {'chemin': chemin, 'titre': titre, 'description': description, 'corps': corps, 'categorie': categorie}
        d.update(kw)
        P.append(d)

    def tete(titre, lead, fil, sur=''):
        items = ''.join(f'<li><a href="{u}">{e(t)}</a></li>' if u else f'<li>{e(t)}</li>' for t, u in fil)
        ey = f'<p class="eyebrow">{e(sur)}</p>' if sur else ''
        return f'<ol class="crumbs" aria-label="Breadcrumb">{items}</ol>{ey}<h1 class="page-title">{e(titre)}</h1><p class="lead">{lead}</p>'

    def carte(url, kicker, titre, texte, vignette=''):
        th = f'<div class="card__thumb"><img src="{vignette}" alt="" loading="lazy"></div>' if vignette else ''
        return (f'<a class="card glass" href="{url}">{th}<span class="card__kicker">{e(kicker)}</span>'
                f'<span class="card__title">{e(titre)}</span><span class="card__text">{texte}</span>'
                f'<span class="card__go">Read →</span></a>')

    nb_sections = len(SECTIONS_DOC)

    # ── Accueil ──
    import contenu as C
    cle_cat = {titre: cle for cle, titre, _ in C.CATEGORIES}
    loupe = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="6.5" stroke="currentColor" stroke-width="1.5"/><path d="M16 16l4.5 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
    noms = [n for _, _, n, _ in SECTIONS_DOC]
    ruban = ''.join(f'<li>{e(n)}</li>' for n in noms + noms)
    filtres = '<button type="button" aria-pressed="true" data-filtre="all">All</button>' + ''.join(
        f'<button type="button" aria-pressed="false" data-filtre="{cle}">{e(titre)}</button>' for cle, titre, _ in C.CATEGORIES)
    # Chaque carte montre le schema au trait de sa section ; a defaut, son
    # nom en grand sur un verre.
    import os
    traits = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'img', 'schemas')
    vignette = lambda h, n: (
        f'<div class="rail__img"><img src="/img/schemas/{h}.svg" alt="" loading="lazy"></div>'
        if os.path.exists(os.path.join(traits, h + '.svg'))
        else f'<div class="rail__img rail__img--nom" aria-hidden="true"><span>{e(n)}</span></div>')
    cartes = ''.join(
        f'<a class="rail__card glass" href="/docs/sections/{sl}" data-cat="{cle_cat.get(cat, "")}">'
        f'{vignette(h, n)}'
        f'<span class="rail__cat">{e(cat)}</span><span class="rail__name">{e(n)}</span></a>'
        for h, sl, n, cat in SECTIONS_DOC)
    pastilles = ''.join(f'<button type="button" data-requete="{q}">{e(t)}</button>' for t, q in POPULAIRES)
    icone = lambda d: f'<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="{d}" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    sujets = ''.join(
        f'<a class="sujet glass" href="{u}">{icone(d)}<span class="sujet__titre">{e(t)}</span><span class="sujet__texte">{e(x)}</span><span class="sujet__plus">{e(c)}</span></a>'
        for u, d, t, x, c in (
            ('/docs/install', 'M16 5v15m-6-6 6 6 6-6M7 25h18', 'Get started', 'Install Opaline, use the theme editor, update and go live.', '5 pages'),
            ('/docs/sections/header', 'M6 6h8v8H6zM18 6h8v8h-8zM6 18h8v8H6zM18 18h8v8h-8z', 'Sections', 'Every section, drawn and explained with all its settings.', f'{nb_sections} sections'),
            ('/docs/guides/product-page', 'M7 6h13l5 5v15H7zM20 6v5h5M11 16h10M11 20h7', 'Guides', 'Step-by-step guides for the features that make Opaline.', '10 guides'),
            ('/docs/settings/logo', 'M6 10h12M22 10h4M6 22h4M14 22h12M20 7v6M12 19v6', 'Theme settings', 'Logo, colors, typography, layout, cards and motion.', f'{len(GROUPES)} groups'),
            ('/docs/faq', 'M16 27a11 11 0 1 0-11-11M12.5 12.5a3.5 3.5 0 1 1 5 3.2c-1 .5-1.5 1.2-1.5 2.3M16 22v.5', 'FAQ', 'Short answers to the questions merchants ask most.', 'Answers'),
            ('/support', 'M6 8h20v13H14l-6 5v-5H6z', 'Support', 'Write to the studio: an answer within one to two business days.', 'Contact'),
        ))
    chevron = lambda d: f'<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="{d}" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    chevron_g, chevron_d = chevron('M12.5 4.5 7 10l5.5 5.5'), chevron('M7.5 4.5 13 10l-5.5 5.5')
    accueil = f'''
<section class="cine quete">
  <div class="cine__bg" aria-hidden="true"></div>
  <div class="cine__veil"></div>
  <div class="quete__inner">
    <p class="eyebrow eyebrow--light">Opaline · Shopify theme · Version {e(v)}</p>
    <h1 class="cine__title">Every detail, <em>documented.</em></h1>
    <div class="quete__boite" data-quete>
      <label class="quete__champ">
        {loupe}
        <span class="visually-hidden">Search the documentation</span>
        <input type="search" placeholder="Search a section, a setting or a guide" autocomplete="off" spellcheck="false"
          role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="quete-resultats">
      </label>
      <ul class="quete__resultats" id="quete-resultats" role="listbox" aria-label="Results" hidden></ul>
    </div>
    <div class="quete__pop"><span>Popular</span>{pastilles}</div>
  </div>
  <div class="cine__ribbon" aria-hidden="true"><ul>{ruban}</ul></div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band__head">
      <div><p class="eyebrow">Browse</p><h2>Or start <em>from a topic.</em></h2></div>
      <p class="band__intro">Opaline is set up entirely in the Shopify theme editor. No code, and every change previews before it goes live.</p>
    </div>
    <div class="sujets">{sujets}</div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="band__head">
      <div><p class="eyebrow">Sections</p><h2>{nb_sections} sections, <em>one signature.</em></h2></div>
      <div class="filtres" data-filtres>{filtres}</div>
    </div>
    <div class="rail__cadre">
      <button type="button" class="rail__fleche rail__fleche--prec glass" data-rail-prev aria-label="Previous sections" disabled>{chevron_g}</button>
      <div class="rail" data-rail>{cartes}</div>
      <button type="button" class="rail__fleche rail__fleche--suiv glass" data-rail-next aria-label="Next sections">{chevron_d}</button>
    </div>
  </div>
</section>

<section class="sombre">
  <div class="wrap">
    <div class="band__head">
      <div><p class="eyebrow eyebrow--light">Guides</p><h2>The features <em>behind the look.</em></h2></div>
      <p class="band__intro">Step-by-step guides for what makes Opaline different, with the exact name of every setting.</p>
    </div>
    <div class="bento">
      <a class="tile tile--a glass" href="/docs/guides/quick-view"><div class="tile__img"><img src="/img/schemas/guide-quick-view.svg" alt="" loading="lazy"></div><span class="tile__kicker">Guide</span><span class="tile__title">Quick view &amp; quick add</span><p>Shop from any product card, in a panel of liquid glass.</p></a>
      <a class="tile tile--b glass" href="/docs/guides/product-page"><div class="tile__img"><img src="/img/schemas/guide-product-page.svg" alt="" loading="lazy"></div><span class="tile__kicker">Guide</span><span class="tile__title">Product page</span><p>Stacked or carousel gallery, thumbnails, swatches.</p></a>
      <a class="tile tile--c glass" href="/docs/guides/cinematic-intro"><div class="tile__img"><img src="/img/schemas/guide-cinematic-intro.svg" alt="" loading="lazy"></div><span class="tile__kicker">Guide</span><span class="tile__title">Cinematic intro</span></a>
      <a class="tile tile--c glass" href="/docs/guides/navigation"><div class="tile__img"><img src="/img/schemas/guide-mega-menu.svg" alt="" loading="lazy"></div><span class="tile__kicker">Guide</span><span class="tile__title">Mega menu</span></a>
      <a class="tile tile--c glass" href="/docs/guides/color-variants"><div class="tile__img"><img src="/img/schemas/guide-swatches.svg" alt="" loading="lazy"></div><span class="tile__kicker">Guide</span><span class="tile__title">Color swatches</span></a>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="appel">
      <div class="appel__texte">
        <p class="eyebrow eyebrow--light">Support</p>
        <h2>Need a hand?</h2>
        <p>Write to the studio. Every message is answered by the people who built Opaline.</p>
        <div class="appel__actions">
          <a class="pill pill--light" href="/support">Contact support</a>
          <a class="pill pill--ghost-light" href="/docs/faq">Read the FAQ</a>
        </div>
      </div>
      <div class="appel__delai glass">
        {icone('M6 8h20v13H14l-6 5v-5H6z')}
        <span class="appel__libelle">Reply within</span>
        <span class="appel__valeur">1–2 <em>business days</em></span>
        <span class="appel__note">Monday to Friday, by email.</span>
      </div>
    </div>
  </div>
</section>'''
    ajoute('/', 'Opaline', 'Documentation and support for Opaline, the Shopify theme by Zeppelin Studio.', accueil, 'Home', mise='plain', toc=False)

    # ── Introduction ──
    corps = tete('Welcome to Opaline', 'Opaline is an editorial Shopify theme built around large photography, fine serif headings and liquid glass. This documentation explains how to install it, set it up and use each of its sections.', [('Docs', '/docs')], 'Documentation')
    corps += '<div class="prose">'
    corps += '<h2>How this documentation is organized</h2>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Part</th><th>What you will find</th></tr></thead><tbody>'
              '<tr><td><a href="/docs/install">Get started</a></td><td>Installing Opaline, the theme editor, updates, and a checklist before you open your store.</td></tr>'
              '<tr><td><a href="/docs/guides/product-page">Guides</a></td><td>Step-by-step explanations of the features that span several sections: the product page, quick view, color swatches, the mega menu, alternate templates, liquid glass, mobile layouts and languages.</td></tr>'
              '<tr><td><a href="/docs/settings/logo">Theme settings</a></td><td>Every store-wide setting: logo, colors, typography, layout, product cards, animations and social media.</td></tr>'
              f'<tr><td><a href="/docs/sections/header">Sections</a></td><td>{nb_sections} pages, one per section, each with screenshots on desktop and mobile, how to add it, and a table of every setting and block.</td></tr>'
              '<tr><td><a href="/docs/faq">Help</a></td><td>Frequently asked questions, what changed in each version, and how to reach us.</td></tr>'
              '</tbody></table></div>')
    corps += '<h2>Find a setting quickly</h2>'
    corps += '<p>Press <kbd>⌘</kbd> <kbd>K</kbd> (or <kbd>Ctrl</kbd> <kbd>K</kbd> on Windows), or click <strong>Search the docs</strong> at the top of the page. The search covers every page, section and setting name.</p>'
    corps += '<h2>Before you start</h2>'
    corps += etapes([
        'Add your products, collections and menus in the Shopify admin first. Many sections show your real content and are easier to set up once it exists.',
        'Duplicate the theme before larger changes, from <strong>Online Store &gt; Themes</strong> &gt; <strong>…</strong> &gt; <strong>Duplicate</strong>. The copy lets you return to a working version at any time.',
        'Preview every change on mobile as well as desktop, using the device icons at the top of the theme editor.',
    ])
    corps += '<h2>Explore</h2><div class="cards">'
    corps += carte('/docs/install', 'Get started', 'Install Opaline', 'From the Theme Store to your theme library.')
    corps += carte('/docs/theme-editor', 'Get started', 'Use the theme editor', 'Sections, blocks, templates and theme settings.')
    corps += carte('/docs/guides/product-page', 'Guide', 'Product page', 'Gallery layouts, thumbnails, swatches, stock and subscriptions.')
    corps += carte('/docs/guides/quick-view', 'Guide', 'Quick view & quick add', 'Shop from any product card, in liquid glass.')
    corps += '</div></div>'
    ajoute('/docs', 'Introduction', 'How the Opaline documentation is organized, and where to start.', corps, 'Get started')

    # ── Installer ──
    corps = tete('Install Opaline', 'Add Opaline to your store from the Shopify Theme Store, try it on your own products, then publish it when you are ready.', [('Docs', '/docs'), ('Get started', None)], 'Get started')
    corps += '<div class="prose">'
    corps += '<h2>Add the theme to your store</h2>'
    corps += etapes([
        'From your Shopify admin, go to <strong>Online Store &gt; Themes</strong>.',
        'Click <strong>Visit Theme Store</strong>, then search for <strong>Opaline</strong>.',
        'On the Opaline page, click <strong>Try theme</strong>. Shopify adds a trial copy to your <strong>Theme library</strong>, where you can customize it with your own products before buying.',
        'When you are ready, click <strong>Buy theme</strong>. Your customizations are kept.',
    ])
    corps += '<h2>Work on it before publishing</h2>'
    corps += '<p>In your theme library, the <strong>…</strong> menu next to Opaline offers these actions:</p>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Action</th><th>What it does</th></tr></thead><tbody>'
              '<tr><td>Customize</td><td>Opens the theme editor, where you set up sections, blocks and theme settings.</td></tr>'
              '<tr><td>Preview</td><td>Shows the theme on your store without publishing it. Share the preview link to get feedback.</td></tr>'
              '<tr><td>Rename</td><td>Gives the copy a name you will recognize, such as “Opaline — spring”.</td></tr>'
              '<tr><td>Duplicate</td><td>Makes a full copy. Do this before large changes so you can go back.</td></tr>'
              '<tr><td>Download theme file</td><td>Saves a ZIP of the theme, as a backup.</td></tr>'
              '<tr><td>Edit code</td><td>Opens the code editor. Code changes are not carried over by theme updates.</td></tr>'
              '<tr><td>Publish</td><td>Makes Opaline the live theme of your store.</td></tr>'
              '</tbody></table></div>')
    corps += note('Opaline comes with ready-made pages and alternate templates. Until you add your own images and products, sections show placeholders so you can see their shape.')
    corps += '<h2>Next</h2><div class="cards">'
    corps += carte('/docs/theme-editor', 'Get started', 'Use the theme editor', 'Learn where everything lives.')
    corps += carte('/docs/launch-checklist', 'Get started', 'Before you go live', 'A checklist to open your store with confidence.')
    corps += '</div></div>'
    ajoute('/docs/install', 'Install Opaline', 'How to add Opaline from the Shopify Theme Store, preview it and publish it.', corps, 'Get started')

    # ── Editeur ──
    corps = tete('Using the theme editor', 'Everything in Opaline is set up in the Shopify theme editor, without code: sections, blocks, templates and theme settings.', [('Docs', '/docs'), ('Get started', None)], 'Get started')
    corps += '<div class="prose">'
    corps += '<h2>Open the editor</h2>'
    corps += etapes(['Go to <strong>Online Store &gt; Themes</strong> in your Shopify admin.', 'Click <strong>Customize</strong> next to Opaline.'])
    corps += '<h2>The three areas of a page</h2>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Area</th><th>What it holds</th></tr></thead><tbody>'
              '<tr><td>Header</td><td>The announcement bar and the header. They appear on every page.</td></tr>'
              '<tr><td>Template</td><td>The sections of the page you are editing. Each template — home, product, collection, page — has its own.</td></tr>'
              '<tr><td>Footer</td><td>The footer. It appears on every page.</td></tr>'
              '</tbody></table></div>')
    corps += '<h2>Sections and blocks</h2>'
    corps += ('<ul><li><strong>Add a section</strong>: click <strong>Add section</strong> in the sidebar and pick one from the list. Each section is documented under <a href="/docs/sections/header">Sections</a>.</li>'
              '<li><strong>Add a block</strong>: inside a section, click <strong>Add block</strong>. Blocks are the repeatable parts of a section — slides, questions, testimonials.</li>'
              '<li><strong>Reorder</strong>: drag a section or block by its handle.</li>'
              '<li><strong>Hide without deleting</strong>: click the eye icon next to it.</li>'
              '<li><strong>Apps</strong>: sections that accept app blocks list your installed apps in <strong>Add block</strong>.</li></ul>')
    corps += '<h2>Switch template</h2>'
    corps += '<p>Use the page selector at the top center of the editor to move between the home page, product pages, collections, the cart and other templates. Opaline includes alternate product and collection templates: see <a href="/docs/guides/templates">Alternate templates</a>.</p>'
    corps += '<h2>Theme settings</h2>'
    corps += '<p>Click the paintbrush icon in the left toolbar to open the store-wide settings: <a href="/docs/settings/colors">colors</a>, <a href="/docs/settings/typography">typography</a>, <a href="/docs/settings/layout">layout</a>, <a href="/docs/settings/product-cards">product cards</a> and more.</p>'
    corps += '<h2>Preview on mobile</h2>'
    corps += '<p>Use the device icons at the top of the editor to switch the preview to mobile. Many Opaline sections have separate mobile settings; see <a href="/docs/guides/mobile">Mobile layouts</a>.</p>'
    corps += note('After a theme update, close the editor and open it again (or reload with <kbd>⌘</kbd> <kbd>Shift</kbd> <kbd>R</kbd>) so new settings appear.', 'tip')
    corps += '</div>'
    ajoute('/docs/theme-editor', 'Using the theme editor', 'Where sections, blocks, templates and theme settings live in the Shopify theme editor.', corps, 'Get started')

    # ── Mise a jour ──
    corps = tete('Update Opaline', 'Shopify tells you when a new version of Opaline is available. Updating keeps your settings and content, and lets you check the new version before publishing it.', [('Docs', '/docs'), ('Get started', None)], 'Get started')
    corps += '<div class="prose">'
    corps += '<h2>Install an update</h2>'
    corps += etapes([
        'Go to <strong>Online Store &gt; Themes</strong>. When an update exists, a notice appears on Opaline in your theme library.',
        'Click <strong>View update</strong>, then <strong>Add to theme library</strong>. Shopify creates an updated copy that keeps your theme settings, sections and content.',
        'Preview the copy and check your main pages: home, a product, a collection and the cart.',
        'When everything looks right, click <strong>Publish</strong> on the updated copy.',
    ])
    corps += note('Changes you made in the code editor are not carried over to the updated copy. Note them down before updating so you can apply them again.')
    corps += f'<h2>Check your version</h2><p>In the theme editor, open <strong>Theme settings</strong> and scroll to <strong>Theme information</strong>. The current version is <strong>{e(v)}</strong>.</p>'
    corps += '</div>'
    ajoute('/docs/update', 'Update Opaline', 'How to update Opaline without losing your settings and content.', corps, 'Get started')

    # ── Liste de controle ──
    corps = tete('Before you go live', 'A short checklist to open your store with every page in order.', [('Docs', '/docs'), ('Get started', None)], 'Get started')
    corps += '<div class="prose"><h2>Content</h2><ul>'
    corps += ('<li>Replace every placeholder image with your own photographs. Product photos read best in portrait (4:5 or 3:4).</li>'
              '<li>Add alternative text to your images in the Shopify admin. Opaline uses it everywhere the image appears.</li>'
              '<li>Fill in the <strong>Logo</strong> and <strong>Favicon</strong> under <a href="/docs/settings/logo">Theme settings &gt; Logo</a>.</li>'
              '<li>Check the main menu and footer menus under <strong>Content &gt; Menus</strong>.</li></ul>')
    corps += '<h2>Shopping</h2><ul>'
    corps += ('<li>Open a product with several colors and check that the gallery follows each color (see <a href="/docs/guides/color-variants">Color variants</a>).</li>'
              '<li>Add a product to the cart from a product page, from a collection with <strong>Quick add</strong>, and from the cart page.</li>'
              '<li>Try a product with low stock: the quantity stops at what is left, with a message.</li>'
              '<li>Check the cart drawer and the checkout button.</li></ul>')
    corps += '<h2>Store-wide</h2><ul>'
    corps += ('<li>Preview every template on mobile.</li>'
              '<li>Check the text contrast of your color schemes on photographs.</li>'
              '<li>Turn on the languages you sell in under <strong>Settings &gt; Languages</strong>.</li>'
              '<li>Fill in the policies under <strong>Settings &gt; Policies</strong>; the footer links to them.</li></ul></div>')
    ajoute('/docs/launch-checklist', 'Before you go live', 'A checklist of content, shopping and store-wide checks before opening your store.', corps, 'Get started')

    # ── Guide : fiche produit ──
    corps = tete('Product page', 'Set up the gallery, the buying controls and the information blocks of your product pages.', [('Docs', '/docs'), ('Guides', None)], 'Guide')
    corps += planche('lf-product', 'The product page: the gallery on one side, the information column on the other.')
    corps += '<div class="prose">'
    corps += '<h2>Open the product page settings</h2>'
    corps += etapes(['In the theme editor, choose <strong>Products &gt; Default product</strong> in the page selector.', 'Click <strong>Product page</strong> in the sidebar.'])
    corps += '<h2>The media gallery</h2>'
    corps += '<p>Under <strong>Media</strong>, <strong>Media layout</strong> offers two presentations:</p>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Layout</th><th>How it looks</th><th>Its settings</th></tr></thead><tbody>'
              '<tr><td>Stacked</td><td>Every image one below the other, scrolling with the page, while the information column stays in view.</td><td><strong>Media aspect ratio</strong> (Original by default), <strong>Show margins around media</strong> (on by default), <strong>Show thumbnails</strong> (off by default).</td></tr>'
              '<tr><td>Carousel</td><td>One image at a time in a shared frame, with arrows and swipe.</td><td><strong>Media aspect ratio</strong> (Portrait 5:6 by default), <strong>Show margins around media</strong> (off by default), <strong>Show thumbnails</strong> (on by default).</td></tr>'
              '</tbody></table></div>')
    corps += planche('guide-product-carousel', 'The carousel layout with thumbnails: a glass strip of thumbnails and a progress bar set over the image.')
    corps += ('<ul><li><strong>Media aspect ratio</strong>: <strong>Original</strong> keeps each photo’s own proportions. The other ratios — portrait 5:6, 4:5, 3:4, square, landscape 16:9 — give every image the same frame and crop it to fill.</li>'
              '<li><strong>Show margins around media</strong>: a white border with rounded corners around the images. Off, the images run edge to edge with a thin line between them.</li>'
              '<li><strong>Show thumbnails</strong>: a small strip of thumbnails in liquid glass, with a progress bar. In the stacked layout it stays at the bottom of the screen while the gallery scrolls; clicking a thumbnail scrolls the page to that image.</li></ul>')
    corps += planche('guide-product-thumbs', 'The stacked layout with thumbnails turned on.')
    corps += note('Videos, YouTube and Vimeo videos and 3D models can sit in the gallery. Only one plays at a time: starting one pauses the others.')
    corps += '<h2>Variants and colors</h2>'
    corps += '<p>Under <strong>Variants</strong>:</p><ul><li><strong>Color swatches for variants</strong> shows round or square color chips for any option named Color, Colour, Couleur or Teinte. Choose the shape with <strong>Swatch shape</strong>.</li><li><strong>Hide photos of non-selected colors</strong> shows only the photos of the chosen color.</li></ul>'
    corps += '<p>The full set-up is in <a href="/docs/guides/color-variants">Color variants &amp; swatches</a>.</p>'
    corps += '<h2>The information column</h2>'
    corps += '<p>The right column is made of blocks. Add, remove and reorder them under <strong>Product page</strong> in the sidebar.</p>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Block</th><th>What it shows</th></tr></thead><tbody>'
              '<tr><td>Vendor</td><td>The vendor or an eyebrow line above the title.</td></tr>'
              '<tr><td>Product title</td><td>The product name.</td></tr>'
              '<tr><td>Price</td><td>The price, the compare-at price, the unit price and, when turned on, the variant SKU.</td></tr>'
              '<tr><td>Variant picker</td><td>The options: swatches for colors, buttons for the others. Unavailable values are crossed out.</td></tr>'
              '<tr><td>Subscriptions</td><td>Delivery frequencies from your subscription app, with a one-time purchase when allowed.</td></tr>'
              '<tr><td>Buy buttons</td><td>Quantity, Add to cart and the accelerated checkout buttons.</td></tr>'
              '<tr><td>Description</td><td>The product description.</td></tr>'
              '<tr><td>Accordion panel</td><td>A collapsible panel for care, dimensions, delivery or returns.</td></tr>'
              '<tr><td>Complementary products</td><td>Products that go with this one, chosen in Shopify’s Search &amp; Discovery app.</td></tr>'
              '<tr><td>Custom Liquid</td><td>Your own code.</td></tr>'
              '</tbody></table></div>')
    corps += '<h2>Buying controls</h2>'
    corps += ('<ul><li><strong>Show accelerated checkout buttons</strong> adds Shop Pay, Apple Pay and the other express checkouts under Add to cart.</li>'
              '<li><strong>Show pickup availability</strong> tells visitors whether the variant can be picked up in store.</li>'
              '<li><strong>Show tax and shipping note</strong> adds the tax mention under the price.</li>'
              '<li><strong>Show the variant SKU</strong> shows the reference of the selected variant.</li></ul>')
    corps += note('When Shopify tracks the inventory of a variant and does not allow overselling, the quantity stops at what is left — minus what is already in the cart — and a message says so before anything is added.', 'tip')
    corps += '</div>'
    ajoute('/docs/guides/product-page', 'Product page', 'Gallery layouts, thumbnails, swatches, buying controls and blocks of the Opaline product page.', corps, 'Guide')

    # ── Guide : apercu rapide ──
    corps = tete('Quick view & quick add', 'Let visitors look at a product and add it to their cart from any product card, without leaving the page.', [('Docs', '/docs'), ('Guides', None)], 'Guide')
    corps += planche('guide-card-actions', 'On hover, two glass buttons appear at the top right of the card. Hovering one reveals its label.')
    corps += '<div class="prose">'
    corps += '<h2>Turn them on or off</h2>'
    corps += etapes(['In the theme editor, open <strong>Theme settings &gt; Product cards</strong>.', 'Use <strong>Quick view</strong> and <strong>Quick add</strong>. Both are on by default.'])
    corps += '<p>The buttons appear on every product card: collection pages, featured collections, the scrolling product row, product recommendations and search results.</p>'
    corps += '<h2>What the + button does</h2>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>The product…</th><th>Clicking +</th></tr></thead><tbody>'
              '<tr><td>has a single variant</td><td>Adds it to the cart straight away. The + turns into a spinner, then a check mark, and the cart drawer opens.</td></tr>'
              '<tr><td>has options (color, size…)</td><td>Opens the quick view panel on <strong>Select options</strong>.</td></tr>'
              '<tr><td>requires a subscription, or is a gift card</td><td>Opens the quick view panel, which leads to the product page for the details these need.</td></tr>'
              '<tr><td>is sold out</td><td>No + button is shown.</td></tr>'
              '</tbody></table></div>')
    corps += '<h2>The quick view panel</h2>'
    corps += planche('guide-quick-view', 'The quick view panel slides in from the right on desktop and rises from the bottom on mobile.')
    corps += ('<p>The panel is a pane of liquid glass with the page blurred behind it. It shows a summary of the product page:</p>'
              '<ul><li>a strip of square photos to swipe;</li><li>the title, price and tax mention, and the start of the description;</li>'
              '<li>the same color swatches, quantity selector, subscription options and Add to cart button as the product page;</li>'
              '<li>a <strong>View full details</strong> link to the product page.</li></ul>'
              '<p>Choosing a color updates the price and brings that color’s photo into view. The panel respects the stock limit and shows Shopify’s messages when an item can’t be added. After a successful add, the panel closes and the cart drawer opens.</p>')
    corps += note('The panel loads only when a visitor opens it, so it adds nothing to the page’s loading time. It closes with <kbd>Esc</kbd>, keeps the keyboard inside while open, and returns focus to the card afterwards.')
    corps += '</div>'
    ajoute('/docs/guides/quick-view', 'Quick view & quick add', 'How the quick view panel and the quick add button work on Opaline product cards.', corps, 'Guide')

    # ── Guide : couleurs ──
    corps = tete('Color variants & swatches', 'Show colors as swatches, and make the gallery follow the color a visitor chooses.', [('Docs', '/docs'), ('Guides', None)], 'Guide')
    corps += planche('guide-swatches', 'Color swatches on the product page: the selected color is ringed and named next to the option.')
    corps += '<div class="prose">'
    corps += '<h2>Show swatches</h2>'
    corps += etapes([
        'In the Shopify admin, give the product an option named <strong>Color</strong> (or Colour, Couleur, Teinte) and create a variant for each color.',
        'In the theme editor, open a product page and click <strong>Product page</strong>.',
        'Under <strong>Variants</strong>, turn on <strong>Color swatches for variants</strong> and choose a <strong>Swatch shape</strong>.',
    ])
    corps += ('<h3>Where the swatch colors come from</h3><ol>'
              '<li>The swatch set on the option value in Shopify — a color or an image. This is the most precise.</li>'
              '<li>Otherwise, a built-in color for common names: noir, blanc, beige, crème, navy, bleu, rouge, bordeaux, vert, kaki, gris, anthracite, rose, jaune, orange, terracotta, marron, cognac, camel, taupe, or, argent.</li>'
              '<li>Otherwise, the option value itself read as a CSS color name, such as “navy” or “olive”.</li></ol>')
    corps += '<h2>Make the gallery follow the color</h2>'
    corps += etapes([
        'In the product’s admin page, upload all its photos in color order: the photos of the first color, then those of the second, and so on.',
        'Open each variant and set its image to the <strong>first</strong> photo of its color.',
        'In the theme editor, turn on <strong>Hide photos of non-selected colors</strong> under <strong>Variants</strong>.',
        'Preview the product and click through each color.',
    ])
    corps += '<p>Each photo belongs to the color whose variant image comes before it. Videos and 3D models belong to every color and always stay visible. If a color has no photo of its own, the full gallery stays visible rather than an empty one.</p>'
    corps += note('Unavailable values are crossed out in the picker but stay selectable, so visitors can still read why: the Add to cart button then says “Sold out” or “Unavailable”.', 'tip')
    corps += '</div>'
    ajoute('/docs/guides/color-variants', 'Color variants & swatches', 'Color swatches and per-color photo galleries in Opaline.', corps, 'Guide')

    # ── Guide : navigation ──
    corps = tete('Navigation & mega menu', 'Choose how your main menu opens, and build a mega menu from your menu’s sub-levels.', [('Docs', '/docs'), ('Guides', None)], 'Guide')
    corps += planche('guide-mega-menu', 'The mega menu: a glass panel under the header, laid out from the categories nested in your menu.')
    corps += '<div class="prose">'
    corps += '<h2>Menu types</h2><p>The header shows the menu chosen in its <strong>Menu</strong> setting — your Main menu by default. <strong>Menu type</strong> decides how it opens on desktop:</p>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Menu type</th><th>What it does</th></tr></thead><tbody>'
              '<tr><td>Dropdown</td><td>A short list of links under the menu item.</td></tr>'
              '<tr><td>Mega menu</td><td>A glass panel under the header, laid out from your menu’s sub-levels.</td></tr>'
              '<tr><td>Burger (drawer)</td><td>The whole menu slides in from the side, on desktop as on mobile.</td></tr>'
              '</tbody></table></div>')
    corps += '<h2>Build a mega menu</h2>'
    corps += etapes([
        'In the Shopify admin, go to <strong>Content &gt; Menus</strong> and open <strong>Main menu</strong>.',
        'Add a top-level item — for example <strong>Shop</strong> — and link it to a collection.',
        'Nest items under it by dragging them slightly to the right. Each one becomes a category of the panel; link it to its collection.',
        'If a category needs its own links, nest a third level under it.',
        'Save the menu, then in the theme editor set the header’s <strong>Menu type</strong> to <strong>Mega menu</strong>.',
    ])
    corps += '<h2>How the panel arranges your categories</h2><p>You don’t choose a layout: the panel adapts to what your menu contains.</p>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Your menu</th><th>What visitors see</th></tr></thead><tbody>'
              '<tr><td>Up to 6 categories</td><td>Cards with a picture — the collection image, or its first product’s image when the collection has none.</td></tr>'
              '<tr><td>7 categories or more</td><td>A compact list with thumbnails, in columns across the full width.</td></tr>'
              '<tr><td>Categories with links</td><td>Columns of links, spread evenly across the panel.</td></tr>'
              '</tbody></table></div>')
    corps += '<p>The panel also shows the menu item’s name and a <strong>View all</strong> link. Its pictures load the first time it opens, so they add nothing to the page load.</p>'
    corps += '<h2>Long menus</h2><p>When the menu no longer fits beside the logo, it moves to its own row under the logo. If it wouldn’t fit there either, the header switches to the menu button, as on mobile.</p>'
    corps += note('The mega menu works with the keyboard: <kbd>Tab</kbd> moves through the categories and links, and <kbd>Esc</kbd> closes the panel.')
    corps += '<h2>The transparent header</h2><p>On the home page, <strong>Transparent header on the home page</strong> lays the header over the opening image. With <strong>Frosted glass effect (liquid glass)</strong>, it turns into frosted glass once visitors scroll past the <strong>Scroll threshold</strong>. All header settings are listed on the <a href="/docs/sections/header">Header</a> page.</p>'
    corps += '</div>'
    ajoute('/docs/guides/navigation', 'Navigation & mega menu', 'Menu types, building a mega menu and the transparent header in Opaline.', corps, 'Guide')

    # ── Guide : intro cinematique ──
    entete = O['schemas']['header']['settings']
    debut = next(i for i, x in enumerate(entete) if x.get('type') == 'header' and 'intro' in str(O['trad'](x.get('content'))).lower())
    fin = next((i for i in range(debut + 1, len(entete)) if entete[i].get('type') == 'header'), len(entete))
    corps = tete('Cinematic intro', 'Open your store with a short logo animation: your logo appears over frosted glass, a photograph or a solid color, then gives way to the page.', [('Docs', '/docs'), ('Guides', None)], 'Guide')
    corps += planche('guide-cinematic-intro', 'The intro over frosted glass: the logo holds for a moment, then moves into the header.')
    corps += '<div class="prose">'
    corps += '<h2>Turn it on</h2>'
    corps += etapes([
        'In the theme editor, click <strong>Header</strong> in the sidebar.',
        'Scroll to <strong>Cinematic intro</strong> and turn on <strong>Enable the cinematic intro</strong>.',
        'Choose the <strong>Intro backdrop</strong>: frosted glass over the page, a photograph, or a solid color.',
        'Set the <strong>Logo size</strong>, <strong>Logo color</strong> and how long it <strong>Hold</strong>s, then decide when to <strong>Show</strong> it.',
        'Click <strong>Save</strong>.',
    ])
    corps += '<h2>Settings</h2>' + O['tableau'](entete[debut + 1:fin], 'Cinematic intro')
    corps += '<h2>Good to know</h2>'
    corps += note('The intro uses the logo of the header. Set it under <strong>Header &gt; Logo header</strong> first; a transparent PNG or SVG works best.')
    corps += note('Visitors who ask their device to reduce motion skip the intro. Showing it once per session keeps returning visitors from waiting on every page.', 'tip')
    corps += '</div>'
    ajoute('/docs/guides/cinematic-intro', 'Cinematic intro', 'How to set up the cinematic logo intro of the Opaline header.', corps, 'Guide')

    # ── Guide : gabarits ──
    corps = tete('Alternate templates', 'Give one product or one collection its own page layout without changing the others.', [('Docs', '/docs'), ('Guides', None)], 'Guide')
    corps += '<div class="prose">'
    corps += '<h2>Product templates</h2><p>The default product template drives every product. Opaline also includes alternate product templates, each fully independent:</p>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Template</th><th>What it’s for</th></tr></thead><tbody>'
              '<tr><td>technical</td><td>Dimensioned drawings and compatible uses, like a specification sheet.</td></tr>'
              '<tr><td>compare</td><td>A before/after slider, for comparisons of finishes or results.</td></tr>'
              '<tr><td>story</td><td>A narrative sequence about how the piece is made.</td></tr>'
              '<tr><td>craft</td><td>Materials and process, with a statement and workshop imagery.</td></tr>'
              '<tr><td>chapters</td><td>Full-screen chapters that stack as visitors scroll.</td></tr>'
              '<tr><td>lookbook</td><td>Floating editorial images and a colorway switcher.</td></tr>'
              '<tr><td>editorial</td><td>More room for story-driven content.</td></tr>'
              '<tr><td>launch</td><td>A promotional banner and reassurance, for a dated release.</td></tr>'
              '<tr><td>bundle</td><td>Cross-selling: a row of companion pieces and recommendations.</td></tr>'
              '<tr><td>gift</td><td>A gifting angle with promotional tiles and reassurance.</td></tr>'
              '<tr><td>trust</td><td>Reviews, press and an FAQ before the footer.</td></tr>'
              '<tr><td>minimal</td><td>A pared-back layout for simple products.</td></tr>'
              '</tbody></table></div>')
    corps += '<h2>Collection templates</h2>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Template</th><th>Grid</th></tr></thead><tbody>'
              '<tr><td>wide</td><td>3 columns, portrait cards, names aligned left.</td></tr>'
              '<tr><td>gallery</td><td>4 columns, portrait, no gap: the photography reads as one surface.</td></tr>'
              '<tr><td>compact</td><td>4 columns, square cards close together.</td></tr>'
              '<tr><td>minimal</td><td>4 columns, image and name only, prices hidden.</td></tr>'
              '<tr><td>editorial</td><td>2 columns, large cards framed like a magazine spread.</td></tr>'
              '<tr><td>showcase</td><td>2 columns with generous space, for a small range.</td></tr>'
              '<tr><td>dense</td><td>2 columns of large square cards.</td></tr>'
              '<tr><td>list</td><td>2 columns of landscape cards, 1 on mobile.</td></tr>'
              '</tbody></table></div>')
    corps += '<h2>Assign a template</h2>'
    corps += etapes([
        'In the Shopify admin, open the product (or the collection).',
        'In the right sidebar, find <strong>Theme template</strong>.',
        'Choose a template and save.',
        'In the theme editor, pick that template in the page selector to edit it. Changes apply to every product or collection using it.',
    ])
    corps += '<h2>Create your own</h2><p>In the theme editor, open the page selector, choose <strong>Products</strong> or <strong>Collections</strong>, then <strong>Create template</strong>. Base it on an existing template and give it a name.</p>'
    corps += note('A template shows nothing until a product or collection is assigned to it.')
    corps += '</div>'
    ajoute('/docs/guides/templates', 'Alternate templates', 'The alternate product and collection templates included with Opaline, and how to assign them.', corps, 'Guide')

    # ── Guide : verre ──
    corps = tete('Liquid glass', 'Liquid glass is Opaline’s signature: translucent, blurred panels with light edges, laid over photography.', [('Docs', '/docs'), ('Guides', None)], 'Guide')
    corps += planche('lf-duo', 'The round button and the captions of the Duo panel sit on liquid glass.')
    corps += '<div class="prose">'
    corps += '<h2>Where you will find it</h2><p>The header on scroll, the mega menu, the quick view panel and the card buttons, the product thumbnails, the promotional popup, the footer panel, and many sections: Colorways, Stacked chapters, Duo panel, Editorial grid, Product mosaic, Closing statement, Statement with images, Testimonials, Timeline and Scrolling text.</p>'
    corps += '<h2>Sections where you can switch it</h2>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Section</th><th>Setting</th></tr></thead><tbody>'
              '<tr><td>Header</td><td>Frosted glass effect (liquid glass)</td></tr>'
              '<tr><td>Editorial grid</td><td>Liquid glass effect (labels + chips)</td></tr>'
              '<tr><td>Product mosaic</td><td>Liquid glass effect (promo block), with Panel shape and text colors</td></tr>'
              '<tr><td>Footer</td><td>Glass tone, Glass tint and Glass blur</td></tr>'
              '<tr><td>Age verifier</td><td>Frosted glass effect</td></tr>'
              '<tr><td>Image / video banner</td><td>Background behind text: glass box, with Glass opacity and Glass blur</td></tr>'
              '</tbody></table></div>')
    corps += '<p>Elsewhere the glass is part of the design: what you control is the photograph behind it and the text color on top.</p>'
    corps += '<h2>Getting a clean effect</h2><ul><li>Glass needs something to blur. Photographs with depth and color read best; a flat, near-white image gives the effect nothing to work with.</li><li>Check the text against the photograph, not against the panel: a light photograph needs dark text, a dark one light text.</li><li>Panels that carry text use a denser glass, so prices and options stay readable on any background.</li></ul>'
    corps += note('Visitors who ask their device to reduce transparency see solid panels instead of glass, automatically.')
    corps += '</div>'
    ajoute('/docs/guides/liquid-glass', 'Liquid glass', 'Where Opaline uses liquid glass, which sections let you switch it, and how to get a clean effect.', corps, 'Guide')

    # ── Guide : mobile ──
    corps = tete('Mobile layouts', 'Many Opaline sections can be tuned for phones without touching the desktop layout.', [('Docs', '/docs'), ('Guides', None)], 'Guide')
    corps += '<div class="prose">'
    corps += '<h2>How mobile settings work</h2><p>Mobile size settings multiply the desktop size: 100% keeps the desktop size, higher enlarges, lower shrinks — on phones only. Set the desktop first, then switch the editor preview to mobile and adjust.</p>'
    corps += ('<div class="table-wrap glass"><table class="simple"><thead><tr><th>Section</th><th>Mobile settings</th></tr></thead><tbody>'
              '<tr><td>Image / video banner</td><td>Image (mobile), eyebrow, heading and text sizes, button scale.</td></tr>'
              '<tr><td>Full-screen hero</td><td>Mobile image, and whether the video plays on mobile.</td></tr>'
              '<tr><td>Statement with images</td><td>Sentence size and line spacing on mobile.</td></tr>'
              '<tr><td>Floating showcase</td><td>Position and width of each image on mobile.</td></tr>'
              '<tr><td>Multiple columns</td><td>Columns on mobile, and a swipeable row.</td></tr>'
              '<tr><td>Product grid</td><td>Columns, title sizes and breadcrumbs on mobile.</td></tr>'
              '<tr><td>Testimonials</td><td>Carousel on mobile, columns on mobile.</td></tr>'
              '<tr><td>Header</td><td>Padding on mobile.</td></tr>'
              '</tbody></table></div>')
    corps += note('On phones, product galleries become swipeable carousels, and the quick view panel rises from the bottom of the screen.', 'tip')
    corps += '</div>'
    ajoute('/docs/guides/mobile', 'Mobile layouts', 'The mobile-specific settings of Opaline sections.', corps, 'Guide')

    # ── Guide : langues ──
    corps = tete('Languages & markets', 'Sell in several languages and countries with Opaline.', [('Docs', '/docs'), ('Guides', None)], 'Guide')
    corps += '<div class="prose">'
    corps += '<h2>Storefront languages</h2><p>Every storefront text of Opaline — buttons, cart, search, forms, messages — is translated into <strong>English, French, German, Spanish and Italian</strong>. Turn languages on under <strong>Settings &gt; Languages</strong> in the Shopify admin; the theme follows automatically.</p>'
    corps += '<p>To change a wording, go to <strong>Online Store &gt; Themes</strong>, click <strong>…</strong> &gt; <strong>Edit default theme content</strong> and search for the text.</p>'
    corps += '<h2>Your own content</h2><p>Texts you type in sections — headings, buttons, slides — are translated with Shopify’s Translate &amp; Adapt app or another translation app.</p>'
    corps += '<h2>Country and language selectors</h2><p>Turn on <strong>Show country and language selectors</strong> in the footer. The country selector appears when you sell in several markets (<strong>Settings &gt; Markets</strong>).</p>'
    corps += '<h2>Right-to-left languages</h2><p>Opaline sets the reading direction from the language: Arabic, Hebrew and other right-to-left languages read from right to left.</p>'
    corps += '</div>'
    ajoute('/docs/guides/languages', 'Languages & markets', 'Storefront languages, translations, selectors and right-to-left support in Opaline.', corps, 'Guide')

    # ── Guide : accessibilite ──
    corps = tete('Motion & accessibility', 'Opaline moves with the page, never against the visitor, and stays usable with a keyboard and a screen reader.', [('Docs', '/docs'), ('Guides', None)], 'Guide')
    corps += '<div class="prose">'
    corps += '<h2>Motion</h2><p>Animation in Opaline follows the scroll rather than timers: headings rise into place, sections reveal as they enter the screen, some images drift. Turn the reveal off under <a href="/docs/settings/animations">Theme settings &gt; Animations</a>.</p>'
    corps += '<p>Visitors who ask their device to reduce motion get the same content without the movement, whatever the setting. Visitors who ask for reduced transparency get solid panels instead of glass.</p>'
    corps += '<h2>Keyboard and screen readers</h2><ul>'
    corps += ('<li>Every interactive element can be reached with <kbd>Tab</kbd> and shows a visible focus ring.</li>'
              '<li>Panels — the cart drawer, the quick view, the menu, the popup — close with <kbd>Esc</kbd> and return focus where it was.</li>'
              '<li>Sliders and carousels can be moved with the arrow keys.</li>'
              '<li>Form fields have labels, and error messages are announced.</li></ul>')
    corps += '<h2>What depends on you</h2><ul><li>Add alternative text to your images in the Shopify admin.</li><li>Keep text readable on its background: 4.5:1 contrast for text, 3:1 for large headings and icons. This matters most for text set on photographs.</li><li>Use descriptive button labels, such as “Shop the tagines” rather than “Click here”.</li></ul>'
    corps += '</div>'
    ajoute('/docs/guides/accessibility', 'Motion & accessibility', 'How Opaline handles motion, keyboard navigation, screen readers and contrast.', corps, 'Guide')

    # ── FAQ ──
    qr = [
        ('Will my content survive a theme update?', 'Yes. Your settings, texts and images are kept in the updated copy Shopify creates. Only changes made in the code editor are not carried over. See <a href="/docs/update">Update Opaline</a>.'),
        ('Why does a section look different on my phone?', 'Several sections have their own mobile settings — image, sizes, columns, positions — so phones can be tuned without changing the desktop. Switch the editor preview to mobile and check the section’s mobile settings. See <a href="/docs/guides/mobile">Mobile layouts</a>.'),
        ('The glass effect barely shows. What is wrong?', 'Probably nothing. Glass needs something to blur: photographs with depth read well, a flat near-white image gives the effect nothing to work with. Panels also turn solid on purpose when a visitor asked their device for reduced transparency.'),
        ('How do I use an alternate product or collection page?', 'Assign it in the Shopify admin, on the product or collection, under <strong>Theme template</strong>. See <a href="/docs/guides/templates">Alternate templates</a>.'),
        ('How do I create a mega menu?', 'Nest items under a top-level item of your main menu in <strong>Content &gt; Menus</strong>, then set the header’s <strong>Menu type</strong> to <strong>Mega menu</strong>. See <a href="/docs/guides/navigation">Navigation &amp; mega menu</a>.'),
        ('My content sits in a narrow column on a large screen.', 'Check <strong>Full width</strong> under <a href="/docs/settings/layout">Theme settings &gt; Layout</a>. Turned off, content is held to the <strong>Page width</strong> you set.'),
        ('Can I change the fonts?', 'Yes, under <a href="/docs/settings/typography">Theme settings &gt; Typography</a>. Any font from the Shopify font library can replace Fraunces and DM Sans.'),
        ('The gallery shows every photo when I choose a color.', 'Check that each variant has its image set, and that <strong>Hide photos of non-selected colors</strong> is on. See <a href="/docs/guides/color-variants">Color variants &amp; swatches</a>.'),
        ('How do I turn off the quick add button?', 'Under <a href="/docs/settings/product-cards">Theme settings &gt; Product cards</a>, turn off <strong>Quick add</strong>. <strong>Quick view</strong> can stay on.'),
        ('Can you customize the theme for my store?', 'We don’t write custom code for individual stores. For changes beyond the theme’s settings, we recommend hiring a <a href="https://www.shopify.com/partners/directory">Shopify Partner</a>.'),
    ]
    corps = tete('Frequently asked questions', 'Quick answers to the questions we receive most often.', [('Docs', '/docs'), ('Help', None)], 'Help')
    corps += '<div class="prose">'
    for q, r in qr:
        corps += f'<h3>{e(q)}</h3><p>{r}</p>'
    corps += note('Can’t find your answer? <a href="/support">Write to us</a> — every message is answered within one to two business days.', 'tip')
    corps += '</div>'
    ajoute('/docs/faq', 'FAQ', 'Answers to frequent questions about Opaline: updates, mobile, glass, templates, menus and fonts.', corps, 'Help')

    # ── Page introuvable ──
    introuvable = (
        '<div class="home"><section class="hero" style="min-height:60vh"><div>'
        '<p class="eyebrow">Error 404</p><h1>This page has <em>moved on.</em></h1>'
        '<p class="hero__lead">The address may have changed with a new version of the documentation. Search for what you need, or start again from the introduction.</p>'
        '<div class="hero__actions"><a class="pill pill--dark" href="/docs">Go to the documentation</a>'
        '<button type="button" class="pill pill--line" data-search-open>Search the docs</button></div></div></section></div>')
    ajoute('/404', 'Page not found', 'This page does not exist.', introuvable, 'Help', mise='plain', toc=False)

    # ── Support ──
    support = '''
<div class="support">
  <div class="support__form glass">
    <p class="eyebrow">Support</p>
    <h1 class="page-title">Tell us what you’re building.</h1>
    <p class="lead">Installation, a setting that won’t behave, a section you want to use — write to us. Every message is read by the studio and answered by the people who wrote the theme.</p>
    <form class="cform" action="https://formspree.io/f/mnpapkzp" enctype="multipart/form-data" method="POST" data-cform data-mailto="contact.zeppelin.studio@gmail.com" novalidate>
      <div class="cform__row">
        <div class="cform__field"><label for="cf-name">Your name</label><input id="cf-name" name="name" type="text" autocomplete="name" placeholder="Jane Mercier" required></div>
        <div class="cform__field"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" placeholder="jane@studio.com" required></div>
      </div>
      <div class="cform__row">
        <div class="cform__field"><label for="cf-store">Store URL</label><input id="cf-store" name="store" type="text" autocomplete="url" placeholder="yourstore.myshopify.com" aria-describedby="cf-store-help" required><span class="cform__hint" id="cf-store-help">For example: yourstore.myshopify.com</span></div>
        <div class="cform__field"><label for="cf-topic">Subject</label><select id="cf-topic" name="topic"><option>Installation</option><option>A setting or a section</option><option>Something looks wrong</option><option>Customisation request</option><option>Licence &amp; invoicing</option><option>Something else</option></select></div>
      </div>
      <div class="cform__field"><label for="cf-message">Describe the problem</label><textarea id="cf-message" name="message" required placeholder="The page or section concerned, what you expected, and what happens instead."></textarea></div>
      <div class="cform__field"><label for="cf-file">Screenshot or file (optional)</label><input id="cf-file" name="attachment" type="file" accept="image/*,.pdf,.txt,.zip" aria-describedby="cf-file-help"><span class="cform__hint" id="cf-file-help">A screenshot of the problem helps us answer faster. Up to 10 MB.</span></div>
      <input type="hidden" name="_subject" value="Opaline — support request">
      <div class="cform__trap" aria-hidden="true"><label for="cf-company">Leave this field empty</label><input id="cf-company" name="_gotcha" type="text" tabindex="-1" autocomplete="off"></div>
      <div class="cform__foot"><button type="submit" class="pill pill--dark">Send the message</button><span class="cform__hint">We answer within one to two business days.</span></div>
      <p class="cform__status" data-cform-status role="status" aria-live="polite" hidden></p>
    </form>
  </div>
  <aside class="support__aside">
    <div class="note glass"><span class="note__label">By email</span><p><a href="mailto:contact.zeppelin.studio@gmail.com">contact.zeppelin.studio@gmail.com</a></p><p><button type="button" class="pill pill--line" data-copy="contact.zeppelin.studio@gmail.com">Copy address</button></p></div>
    <div class="note glass"><span class="note__label">Response time</span><p>One to two business days, Monday to Friday. A broken live store or an unreachable checkout is handled first.</p></div>
    <div class="note glass"><span class="note__label">What we cover</span><p>Bugs in the theme, how a setting or a section works, and help with this documentation. We don’t cover custom development, third-party apps, or issues coming from Shopify itself — we’ll tell you plainly and point you to the right place.</p></div>
    <div class="note glass"><span class="note__label">Before you edit</span><p>Duplicate your theme before changing its code or reworking its settings: <strong>Online Store &gt; Themes</strong> &gt; <strong>…</strong> &gt; <strong>Duplicate</strong>.</p></div>
    <div class="note glass"><span class="note__label">Custom work</span><p>For changes beyond the theme’s settings, we recommend a <a href="https://www.shopify.com/partners/directory">Shopify Partner</a>. Support is offered in English and French.</p></div>
    <div class="note glass"><span class="note__label">Quick answers</span><p>Many questions are answered in the <a href="/docs/faq">FAQ</a> and the <a href="/docs">documentation</a>.</p></div>
  </aside>
</div>
<script src="/assets/support.js" defer></script>'''
    ajoute('/support', 'Support', 'Contact Zeppelin Studio for help with the Opaline Shopify theme. Answers within one to two business days.', support, 'Help', mise='plain', toc=False)

    return P

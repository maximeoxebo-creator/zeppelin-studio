"""Contenu redige de la documentation d'Opaline.

Les tableaux de reglages sont generes depuis les schemas du theme (voir
build.py) ; ici vivent les textes qu'un schema ne peut pas donner : a quoi
sert chaque section, comment s'en servir, et les guides des fonctions qui
traversent plusieurs sections.

Langue : anglais americain, comme l'exige le Theme Store.
"""

# ── Classement des sections ───────────────────────────────────────────
# (cle, titre, sections) — l'ordre est celui de la barre laterale.
CATEGORIES = [
    ('header-footer', 'Header, footer & overlays',
     ['header', 'lf-announcement', 'footer', 'lf-popup', 'lf-age-verification']),
    ('heroes', 'Heroes & banners',
     ['lf-hero-cinematic', 'image-banner', 'lf-duo', 'lf-split-quote', 'lf-float-showcase', 'lf-finale']),
    ('products', 'Products & collections',
     ['featured-product', 'featured-collection', 'lf-drag-rail', 'lf-mosaic', 'lf-colorways',
      'lf-blueprint', 'lf-recommendations', 'lf-index-list']),
    ('storytelling', 'Storytelling',
     ['lf-manifesto', 'lf-inlay', 'lf-sticky-story', 'lf-deck', 'lf-timeline', 'lf-collage',
      'lf-editorial-grid', 'lf-marquee', 'rich-text', 'image-with-text', 'multicolumn', 'lf-before-after']),
    ('trust', 'Reviews, press & FAQ',
     ['lf-testimonials', 'lf-press', 'lf-faq']),
    ('utilities', 'Forms & utilities',
     ['contact-form', 'email-signup-banner', 'page', 'custom-liquid', 'apps', 'lf-divider']),
    ('templates', 'Template sections',
     ['lf-product', 'main-collection-product-grid', 'main-list-collections', 'main-search',
      'main-cart-items', 'main-blog', 'main-article', 'main-page']),
]

# ── Ce que fait chaque section ────────────────────────────────────────
DESCRIPTIONS = {
    'header': "Your logo, main menu, search, account and cart. On the home page the header can sit transparent over the opening image and turn into frosted glass as visitors scroll. It can also open the site with a short cinematic logo intro.",
    'lf-announcement': "A slim bar above the header for short messages: a free-shipping threshold, a launch, opening hours. Several messages take turns, with optional arrows.",
    'footer': "Newsletter sign-up, reassurance messages, link columns, social icons, payment icons, policy links and the country and language selectors. It can sit on a photograph behind a frosted glass panel.",
    'lf-popup': "A promotional glass window that opens after a delay. It can hand over a discount code to copy or collect an email address. Visitors who close it don't see it again for the number of days you choose.",
    'lf-age-verification': "A full-screen check that asks visitors to confirm their age before they browse, for stores selling alcohol or other age-restricted products. You choose where a refusal leads.",
    'lf-hero-cinematic': "A full-height opening scene with an image or video, a large heading, buttons and an optional glass capsule that highlights a product. Several slides can follow each other.",
    'image-banner': "A full-width image or video with an eyebrow, heading, text and buttons. The text can sit on the image, on an overlay, or inside a frosted glass box, with optional parallax.",
    'lf-duo': "Two halves side by side: a large photograph on one side, a colored panel on the other with heading, text, an inset image, a round badge and a button.",
    'lf-split-quote': "A large quotation set next to a photograph, with author, role and an optional link. The panel color, quotation mark and text colors are yours to choose.",
    'lf-float-showcase': "Images placed freely around a central heading, drifting at different speeds as visitors scroll. Each image can carry a glass tag and link to a product.",
    'lf-finale': "A full-bleed closing scene before the footer: a photograph, a large heading, a button, a row of press logos and glass links.",
    'featured-product': "One product with its media, price, options, quantity and add-to-cart button, anywhere in your store. It uses the same buying controls as the product page.",
    'featured-collection': "Products from one collection in a grid or a carousel, with an optional View all button.",
    'lf-drag-rail': "A horizontal row of products that visitors scroll with a swipe or a drag. It can show collection tabs, and a custom cursor label follows the mouse.",
    'lf-mosaic': "Products from a collection laid out in a mosaic around a promotional glass panel with heading, subtitle and two links.",
    'lf-colorways': "Shows one product range in each of its finishes. Visitors click a swatch and the photograph, background wash and glass panel change together.",
    'lf-blueprint': "Technical drawings with dimensions, grouped by shape with size tabs, plus a list of compatible cooking surfaces or uses.",
    'lf-recommendations': "Related or complementary products chosen automatically by Shopify's product recommendations.",
    'lf-index-list': "A list of links set in large type. Hovering a line reveals a preview image, and each line can carry a short side note.",
    'lf-manifesto': "A statement in large type whose words light up as visitors scroll, with key figures underneath and an optional link.",
    'lf-inlay': "A sentence in large type with product photographs set between the words like oversized characters. Each photograph can link somewhere and show a caption on hover.",
    'lf-sticky-story': "A story in steps: the text scrolls while the image beside it stays in place and changes from one step to the next.",
    'lf-deck': "Full-screen chapters that stack on top of each other as visitors scroll, each with an image or video, a title, text and glass tags.",
    'lf-timeline': "Key moments of your brand on a horizontal timeline that advances as visitors scroll. Each milestone has a year, image, title, text and key figure.",
    'lf-collage': "An editorial collage of captioned images arranged around a central heading, with a gentle parallax.",
    'lf-editorial-grid': "A grid of image tiles with overlines and headings, for stories, guides or behind-the-scenes content. Labels can sit on liquid glass.",
    'lf-marquee': "A ribbon of short messages that scrolls continuously across the page, with an optional icon between messages.",
    'rich-text': "Eyebrow, heading, text and buttons in an editorial layout, for an introduction or a pause between two image-led sections.",
    'image-with-text': "An image or video next to a block of text with heading, text and buttons. The media can sit on the left or the right.",
    'multicolumn': "Columns with an image, title and text, for benefits, values or services. On mobile the columns can become a swipeable row.",
    'lf-before-after': "A slider that compares two photographs: before and after, or two finishes. Visitors drag the handle or use the arrow keys.",
    'lf-testimonials': "Customer reviews with star rating, quote, headline, name and location or product purchased. Shown as a grid or a draggable carousel.",
    'lf-press': "A row of publications that mentioned you, as logos or names, with an optional short quote under each.",
    'lf-faq': "Questions and answers in an accordion, with an eyebrow, a heading and an intro.",
    'contact-form': "A contact form with name, email, phone number and message. Messages arrive in the store's email address.",
    'email-signup-banner': "The sign-up banner of your password page, shown while your store is closed to the public.",
    'page': "The content of a page you wrote in Shopify admin > Online Store > Pages, placed anywhere on another page.",
    'custom-liquid': "A space for your own Liquid, HTML or embed code.",
    'apps': "A container for app blocks from the apps you installed.",
    'lf-divider': "A spacer between two sections, with or without a line, to give the page room to breathe.",
    'lf-product': "The product page: media gallery, title, price, options, subscriptions, quantity, add to cart, description, accordion panels and complementary products.",
    'main-collection-product-grid': "The collection page: title, description, filters and sorting, the product grid, and promotional tiles placed among the products.",
    'main-list-collections': "The page listing all your collections.",
    'main-search': "Search results, with filters and sorting.",
    'main-cart-items': "The cart page: line items, quantities, order notes, discounts and the checkout button.",
    'main-blog': "The blog page and its article cards.",
    'main-article': "An article page: cover image, title, author, date and content.",
    'main-page': "The title and content of a standard page.",
}

# Conseils propres a une section, affiches apres le tableau des reglages.
CONSEILS = {
    'header': [
        ('tip', "The transparent header only applies to the home page. Everywhere else the header uses the colors under <strong>Opaque header</strong>."),
        ('note', "The menu is chosen in the <strong>Menu</strong> setting. Nested items in that menu become a mega menu: see <a href=\"/docs/guides/navigation\">Navigation &amp; mega menu</a>."),
    ],
    'lf-popup': [
        ('note', "In the theme editor the popup opens straight away so you can style it. On the live store it waits for the delay you set."),
    ],
    'lf-age-verification': [
        ('note', "This screen is a courtesy, not a legal guarantee. Check what the law asks of you in each country you sell to."),
    ],
    'lf-inlay': [
        ('tip', "Cut-out product photos often keep a wide transparent margin. If one product looks smaller than the others, raise its <strong>Size</strong> until the drawings look the same."),
    ],
    'lf-drag-rail': [
        ('tip', "The <strong>Cursor label</strong> appears inside a glass bubble that follows the mouse over the row. Near the quick view and quick add buttons of a card, the bubble steps aside so visitors can click."),
    ],
    'lf-product': [
        ('note', "The product page has a full guide: <a href=\"/docs/guides/product-page\">Product page</a>."),
    ],
    'main-collection-product-grid': [
        ('note', "Filters come from Shopify's Search &amp; Discovery app. Add or remove filters there; the theme displays them."),
    ],
    'lf-recommendations': [
        ('note', "Recommendations are calculated by Shopify from your sales and product descriptions. A new store may show few or none at first. You can choose them yourself with Shopify's free Search &amp; Discovery app."),
    ],
}

"""Schemas au trait des sections d'Opaline.

Chaque section est dessinee en SVG, comme une planche d'architecte : cadre
de navigateur, aplats hachures pour les photos, t-shirt au trait pour les
produits (le visuel d'attente de Shopify), titres en serif, lignes grises pour le texte. Les reperes
numerotes renvoient a la legende sous le schema.

  svg(h)            -> schema complet, reperes compris (insere dans la page)
  svg(h, mini=True) -> vignette sans reperes, trait plus appuye (fichier)
  LEGENDES[h]       -> [(numero, libelle), ...]

Zone de dessin : 1160 x 676, origine en haut a gauche de la page affichee.
"""
import html

W, H = 1160, 676
SERIF = "Fraunces, Georgia, 'Times New Roman', serif"
SANS = "'DM Sans', 'Helvetica Neue', Arial, sans-serif"
REPERE = '#a9521a'


class Planche:
    """Accumule les traces d'un schema."""

    def __init__(self, encre, mini, pid):
        self.encre, self.mini, self.pid = encre, mini, pid
        self.clair = encre != '#111110'
        self.k = 1.8 if mini else 1.0
        self.out = []
        self.appels = []

    # ── Traits de base ──
    def _t(self, w=2.0, o=1.0, fill=None, dash=None):
        f = fill or 'none'
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return (f'stroke="{self.encre}" stroke-width="{w * self.k:.2f}" stroke-opacity="{o}" fill="{f}" '
                f'stroke-linecap="round" stroke-linejoin="round"{d}')

    def rect(self, x, y, w, h, r=0, o=1.0, sw=2.0, fill=None, dash=None):
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" {self._t(sw, o, fill, dash)}/>')

    def ligne(self, x1, y1, x2, y2, o=1.0, sw=2.0, dash=None):
        self.out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {self._t(sw, o, None, dash)}/>')

    def chemin(self, d, o=1.0, sw=2.0, fill=None):
        self.out.append(f'<path d="{d}" {self._t(sw, o, fill)}/>')

    def rond(self, cx, cy, r, o=1.0, sw=2.0, fill=None):
        self.out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" {self._t(sw, o, fill)}/>')

    def mot(self, x, y, texte, taille=44, ancre='start', italique=False, o=1.0, famille=SERIF, poids=300, espace=-0.02):
        st = ' font-style="italic"' if italique else ''
        self.out.append(
            f'<text x="{x}" y="{y}" font-family="{famille}" font-size="{taille}" font-weight="{poids}"{st} '
            f'letter-spacing="{espace * taille:.2f}" text-anchor="{ancre}" fill="{self.encre}" fill-opacity="{o}">'
            f'{html.escape(texte)}</text>')

    # ── Elements de page ──
    def texte(self, x, y, w, n=3, pas=16, fin=0.62, o=0.38):
        """Paragraphe : lignes grises, la derniere plus courte."""
        for i in range(n):
            lg = w * (fin if i == n - 1 else (1 if i % 3 != 1 else 0.93))
            self.ligne(x, y + i * pas, x + lg, y + i * pas, o=o, sw=2.4)

    def surtitre(self, x, y, w=90, centre=False):
        if centre:
            self.ligne(x - w / 2, y, x + w / 2, y, o=0.55, sw=2)
        else:
            self.ligne(x, y, x + 26, y, o=0.55, sw=1.6)
            self.ligne(x + 36, y, x + 36 + w, y, o=0.55, sw=2)

    def bouton(self, x, y, w=150, h=40, plein=False, o=1.0):
        r = h / 2
        if plein:
            self.rect(x, y, w, h, r, fill=self.encre, o=o)
            contraste = '#111110' if self.clair else '#ffffff'
            self.out.append(f'<line x1="{x + w * 0.28}" y1="{y + h / 2}" x2="{x + w * 0.72}" y2="{y + h / 2}" '
                            f'stroke="{contraste}" stroke-width="{2 * self.k:.2f}" stroke-linecap="round"/>')
        else:
            self.rect(x, y, w, h, r, o=o)
            self.ligne(x + w * 0.28, y + h / 2, x + w * 0.72, y + h / 2, o=0.5, sw=2)

    def lien(self, x, y, w=110):
        self.ligne(x, y, x + w, y, o=0.6, sw=2)
        self.ligne(x, y + 9, x + w, y + 9, o=0.9, sw=1.4)

    def photo(self, x, y, w, h, r=10, o=1.0):
        """Photo : cadre et hachures fines."""
        self.out.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{self.pid}-h)" stroke="none"/>')
        if o:
            self.rect(x, y, w, h, r, o=o)

    def produit(self, x, y, w, h, r=8, echelle=None, o=1.0, cadre=True):
        """Visuel produit : cadre et t-shirt au trait au centre."""
        if cadre:
            self.rect(x, y, w, h, r, o=0.55 * o)
        s = echelle or min(w, h) / 150
        self.teeshirt(x + w / 2, y + h / 2 + 2 * s, s, o=o)

    def teeshirt(self, cx, cy, s=1.0, o=1.0):
        d = ('M-14,-38 C-8,-31 8,-31 14,-38 L38,-30 L56,-6 L40,4 L34,-4 L34,40 L-34,40 L-34,-4 L-40,4 L-56,-6 L-38,-30 Z '
             'M-14,-38 C-10,-26 10,-26 14,-38 M50,-14 L36,-4 M-50,-14 L-36,-4')
        self.out.append(f'<path d="{d}" transform="translate({cx} {cy}) scale({s})" '
                        f'stroke="{self.encre}" stroke-width="{2 * self.k / s:.2f}" stroke-opacity="{o}" fill="none" '
                        f'stroke-linecap="round" stroke-linejoin="round"/>')

    def verre(self, x, y, w, h, r=18, o=1.0):
        """Panneau de verre : voile clair, contour, reflet."""
        if self.clair:
            # Sur fond sombre : un voile qui estompe ce qui passe dessous.
            self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#121a2b" fill-opacity=".55" stroke="none"/>')
        op = 0.08 if self.clair else 0.78
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#ffffff" fill-opacity="{op}" stroke="none"/>')
        if o:
            self.rect(x, y, w, h, r, o=o)
            self.ligne(x + r * 0.9, y + 7, x + min(w * 0.38, 160), y + 7, o=0.35, sw=1.6)

    def pastille(self, cx, cy, r=12, plein=False, o=1.0):
        self.rond(cx, cy, r, o=o, fill=self.encre if plein else None)

    def fleche(self, x, y, sens=1, t=14, o=1.0):
        self.chemin(f'M{x - sens * t / 2},{y - t / 2} L{x + sens * t / 2},{y} L{x - sens * t / 2},{y + t / 2}', o=o)

    def croix(self, cx, cy, t=8, o=1.0):
        self.ligne(cx - t, cy, cx + t, cy, o=o)
        self.ligne(cx, cy - t, cx, cy + t, o=o)

    def entete(self, y=0, h=64, o=0.5, transparent=False):
        """En-tete de la boutique, en filigrane (contexte)."""
        for i, lg in enumerate((40, 70, 44, 40)):
            self.ligne(40 + i * 82, y + h / 2, 40 + i * 82 + lg * 0.8, y + h / 2, o=o * 0.8, sw=2)
        self.mot(W / 2, y + h / 2 + 9, 'Logo', 26, 'middle', o=o)
        for i in range(3):
            self.rond(W - 120 + i * 36, y + h / 2, 7, o=o)
        if not transparent:
            self.ligne(0, y + h, W, y + h, o=o * 0.5, sw=1.6)

    def cote(self, x1, y1, x2, y2, texte='', o=0.7):
        """Ligne de cote d'architecte, avec ses butees."""
        self.ligne(x1, y1, x2, y2, o=o, sw=1.4)
        if x1 == x2:
            self.ligne(x1 - 7, y1, x1 + 7, y1, o=o, sw=1.4)
            self.ligne(x2 - 7, y2, x2 + 7, y2, o=o, sw=1.4)
            if texte:
                self.mot(x1 + 12, (y1 + y2) / 2 + 5, texte, 14, famille=SANS, poids=400, o=o, espace=0.04)
        else:
            self.ligne(x1, y1 - 7, x1, y1 + 7, o=o, sw=1.4)
            self.ligne(x2, y2 - 7, x2, y2 + 7, o=o, sw=1.4)
            if texte:
                self.mot((x1 + x2) / 2, y1 - 10, texte, 14, 'middle', famille=SANS, poids=400, o=o, espace=0.04)

    def voile(self, o=0.05):
        self.out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{self.encre}" fill-opacity="{o}"/>')

    def appel(self, n, x, y, cx, cy):
        """Repere numerote en (x, y), relie au point vise (cx, cy)."""
        self.appels.append((n, x, y, cx, cy))

    def rendu_appels(self):
        out = []
        for n, x, y, cx, cy in self.appels:
            if (cx, cy) != (x, y):
                out.append(f'<line x1="{x}" y1="{y}" x2="{cx}" y2="{cy}" stroke="{REPERE}" stroke-width="1.6" stroke-dasharray="3 4"/>')
                out.append(f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="{REPERE}"/>')
            out.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{REPERE}"/>'
                       f'<text x="{x}" y="{y + 5.5}" font-family="{SANS}" font-size="15" font-weight="600" '
                       f'text-anchor="middle" fill="#fff">{n}</text>')
        return ''.join(out)


# ─────────────────────────────────────────────────────────────────────────
# Les sections. Chaque fonction dessine sur la planche p et pose ses reperes.
# ─────────────────────────────────────────────────────────────────────────
S = {}
LEGENDES = {}


def section(h, *legende):
    def deco(f):
        S[h] = f
        LEGENDES[h] = list(enumerate(legende, 1))
        return f
    return deco


def fond_photo(p, y=0, h=H):
    p.photo(0, y, W, h, 0, o=0)


@section('header', 'Logo, centered or on the left', 'Main menu, with mega menu panels', 'Search, account and cart',
         'Transparent over the first section, frosted glass on scroll')
def _(p):
    fond_photo(p, 120, H - 120)
    p.verre(24, 22, W - 48, 78, 39)
    for i, lg in enumerate((50, 84, 52, 48, 60)):
        p.ligne(70 + i * 96, 61, 70 + i * 96 + lg, 61, o=0.8, sw=2.2)
    p.mot(W / 2, 72, 'Logo', 34, 'middle')
    p.rond(W - 190, 58, 9)
    p.ligne(W - 183, 65, W - 176, 72)
    p.rond(W - 132, 53, 6)
    p.chemin(f'M{W - 144},74 C{W - 144},63 {W - 120},63 {W - 120},74')
    p.chemin(f'M{W - 86},52 L{W - 64},52 L{W - 61},76 L{W - 89},76 Z M{W - 81},52 C{W - 81},43 {W - 69},43 {W - 69},52')
    p.surtitre(70, 420)
    p.mot(70, 500, 'New season', 64)
    p.texte(70, 548, 380, 2)
    p.bouton(70, 590, 170, 44)
    p.appel(1, W / 2, 160, W / 2, 84)
    p.appel(2, 200, 160, 200, 66)
    p.appel(3, W - 128, 160, W - 128, 80)
    p.appel(4, 90, 250, 60, 100)


@section('lf-announcement', 'Message: several can take turns', 'Arrows to move between messages', 'Bar color, or liquid glass')
def _(p):
    p.rect(0, 0, W, 64, 0)
    p.ligne(W / 2 - 150, 32, W / 2 + 150, 32, o=0.9, sw=2.6)
    p.fleche(60, 32, -1)
    p.fleche(W - 60, 32, 1)
    p.entete(64, 80, o=0.45)
    fond_photo(p, 144, H - 144)
    p.appel(1, W / 2 + 230, 110, W / 2 + 140, 34)
    p.appel(2, 120, 110, 62, 34)
    p.appel(3, W - 200, 110, W - 200, 50)


@section('footer', 'Newsletter in a glass panel', 'Reassurance items', 'Menus and text column',
         'Social icons and payment methods', 'Background image')
def _(p):
    fond_photo(p)
    p.verre(260, 40, 640, 150, 22)
    p.mot(W / 2, 96, 'Join our mailing list', 30, 'middle')
    p.rect(390, 122, 260, 40, 20)
    p.bouton(660, 122, 110, 40, plein=True)
    p.verre(24, 216, W - 48, 430, 22)
    for i in range(4):
        x = 24 + (W - 48) / 4 * i
        if i:
            p.ligne(x, 236, x, 326, o=0.35, sw=1.6)
        p.mot(x + (W - 48) / 8, 272, ('Free shipping', 'Easy returns', 'Warranty', 'Secure payment')[i], 22, 'middle')
        p.ligne(x + 80, 298, x + (W - 48) / 4 - 80, 298, o=0.4, sw=2.2)
    p.ligne(60, 346, W - 60, 346, o=0.3, sw=1.4)
    p.mot(70, 410, 'Logo', 30)
    p.texte(70, 440, 220, 3)
    for c in range(3):
        x = 380 + c * 250
        p.ligne(x, 390, x + 90, 390, o=0.8, sw=2)
        for k in range(5 if c < 2 else 3):
            p.ligne(x, 424 + k * 26, x + (110 if c < 2 else 200), 424 + k * 26, o=0.38, sw=2.2)
    p.ligne(60, 580, W - 60, 580, o=0.3, sw=1.4)
    for i in range(4):
        p.rond(80 + i * 34, 612, 9)
    p.ligne(W / 2 - 110, 612, W / 2 + 110, 612, o=0.38, sw=2.2)
    for i in range(4):
        p.rect(W - 260 + i * 52, 600, 40, 24, 5, o=0.6)
    p.appel(1, 200, 110, 260, 110)
    p.appel(2, 70, 330, 120, 298)
    p.appel(3, 660, 520, 630, 476)
    p.appel(4, 80, 560, 110, 604)
    p.appel(5, 1100, 160, 1060, 150)


@section('lf-popup', 'Eyebrow, heading and text', 'Discount code, copied in one tap', 'Button and the No thanks link',
         'Close button, delay and frequency')
def _(p):
    p.entete(0, 64, o=0.3)
    p.photo(0, 64, W, H - 64, 0, o=0)
    p.voile(0.05)
    p.verre(W / 2 - 230, 120, 460, 440, 26)
    p.surtitre(W / 2, 182, 80, centre=True)
    p.mot(W / 2, 236, 'Join the list', 40, 'middle')
    p.ligne(W / 2 - 150, 270, W / 2 + 150, 270, o=0.38, sw=2.2)
    p.rect(W / 2 - 170, 302, 340, 56, 12, dash='6 6')
    p.mot(W / 2, 339, 'WELCOME10', 22, 'middle', famille=SANS, poids=400, espace=0.18)
    p.bouton(W / 2 - 90, 384, 180, 44, plein=True)
    p.lien(W / 2 - 45, 466, 90)
    p.rond(W / 2 + 196, 156, 17)
    p.ligne(W / 2 + 190, 150, W / 2 + 202, 162)
    p.ligne(W / 2 + 202, 150, W / 2 + 190, 162)
    p.appel(1, W / 2 - 300, 220, W / 2 - 110, 230)
    p.appel(2, W / 2 + 300, 330, W / 2 + 170, 330)
    p.appel(3, W / 2 - 300, 420, W / 2 - 90, 406)
    p.appel(4, W / 2 + 300, 156, W / 2 + 214, 156)


@section('lf-age-verification', 'Heading and text', 'Accept button: the visitor enters the store',
         'Deny button, or a page to send them to', 'Backdrop: frosted glass, image or color')
def _(p):
    p.entete(0, 64, o=0.3)
    p.photo(0, 64, W, H - 64, 0, o=0)
    p.voile(0.05)
    p.verre(W / 2 - 220, 160, 440, 300, 26)
    p.mot(W / 2, 240, 'Age verification', 38, 'middle')
    p.ligne(W / 2 - 120, 276, W / 2 + 120, 276, o=0.38, sw=2.2)
    p.bouton(W / 2 - 160, 316, 320, 48, plein=True)
    p.bouton(W / 2 - 160, 380, 320, 44)
    p.appel(1, W / 2 - 300, 240, W / 2 - 140, 236)
    p.appel(2, W / 2 + 300, 340, W / 2 + 160, 340)
    p.appel(3, W / 2 + 300, 402, W / 2 + 160, 402)
    p.appel(4, 120, 600, 160, 560)


@section('lf-hero-cinematic', 'Background image or video', 'Eyebrow, heading and text', 'Buttons',
         'Featured product in a glass card', 'Scroll cue')
def _(p):
    fond_photo(p)
    p.entete(0, 80, o=0.55, transparent=True)
    p.surtitre(60, 360)
    p.mot(60, 450, 'Designed to last.', 68)
    p.texte(60, 494, 420, 2)
    p.bouton(60, 556, 180, 46)
    p.lien(268, 568, 120)
    p.verre(W - 380, 540, 320, 92, 20)
    p.produit(W - 366, 552, 68, 68)
    p.ligne(W - 282, 574, W - 190, 574, o=0.5, sw=2)
    p.mot(W - 282, 608, 'Product', 22)
    p.fleche(W - 90, 586, 1, 12)
    p.ligne(W / 2, 610, W / 2, 650, o=0.6, sw=1.6)
    p.appel(1, W - 120, 200, W - 200, 260)
    p.appel(2, 640, 380, 600, 420)
    p.appel(3, 120, 640, 150, 602)
    p.appel(4, W - 220, 490, W - 220, 540)
    p.appel(5, W / 2 + 60, 640, W / 2 + 6, 640)


@section('image-banner', 'Image, full width or contained', 'Heading and text, placed where you choose', 'Buttons')
def _(p):
    fond_photo(p)
    p.mot(W / 2, 320, 'Signature', 84, 'middle')
    p.texte(W / 2 - 180, 362, 360, 2, fin=0.8)
    p.bouton(W / 2 - 85, 410, 170, 46)
    p.appel(1, 120, 120, 200, 160)
    p.appel(2, W / 2 + 330, 300, W / 2 + 230, 300)
    p.appel(3, W / 2 + 200, 433, W / 2 + 85, 433)


@section('lf-duo', 'Two panels side by side', 'Heading and link on each panel', 'Round glass button')
def _(p):
    p.photo(0, 0, W / 2 - 6, H, 0, o=0)
    p.photo(W / 2 + 6, 0, W / 2 - 6, H, 0, o=0)
    p.ligne(W / 2 - 6, 0, W / 2 - 6, H, o=0.5, sw=1.6)
    p.ligne(W / 2 + 6, 0, W / 2 + 6, H, o=0.5, sw=1.6)
    p.mot(60, 140, 'The first', 54)
    p.mot(60, 200, 'collection', 54, italique=True)
    p.texte(60, 240, 300, 2)
    p.lien(60, 560, 140)
    p.mot(W / 2 + 60, 560, 'The second', 44)
    p.lien(W / 2 + 60, 600, 140)
    p.verre(W / 2 - 40, H / 2 - 40, 80, 80, 40)
    p.croix(W / 2, H / 2, 10)
    p.appel(1, W / 2 - 120, 440, W / 2 - 200, 400)
    p.appel(2, 420, 150, 360, 170)
    p.appel(3, W / 2 + 120, H / 2, W / 2 + 40, H / 2)


@section('lf-split-quote', 'Quote, set large in italics', 'Author and role', 'Image on the other half')
def _(p):
    p.photo(W / 2, 0, W / 2, H, 0, o=0)
    p.ligne(W / 2, 0, W / 2, H, o=0.5, sw=1.6)
    p.mot(140, 230, '“', 160, o=0.2)
    p.mot(W / 4, 300, 'Made with care,', 54, 'middle', italique=True)
    p.mot(W / 4, 360, 'meant to be', 54, 'middle', italique=True)
    p.mot(W / 4, 420, 'kept.', 54, 'middle', italique=True)
    p.ligne(W / 4 - 50, 480, W / 4 + 50, 480, o=0.6, sw=2)
    p.ligne(W / 4 - 70, 504, W / 4 + 70, 504, o=0.35, sw=2)
    p.appel(1, 60, 360, 130, 350)
    p.appel(2, 120, 492, W / 4 - 76, 492)
    p.appel(3, W - 120, 120, W - 200, 180)


@section('lf-float-showcase', 'Very large heading', 'Floating images, in front of or behind the heading',
         'Glass tag linking to a product', 'Each image drifts at its own speed')
def _(p):
    p.photo(140, 60, 200, 240, 12)
    p.photo(760, 40, 300, 220, 12)
    p.mot(W / 2, 330, 'NEW', 190, 'middle', espace=-0.03)
    p.mot(W / 2, 520, 'SEASON', 190, 'middle', espace=-0.03)
    p.photo(600, 380, 200, 260, 12)
    p.verre(620, 590, 160, 40, 20)
    p.ligne(650, 610, 750, 610, o=0.5, sw=2)
    p.chemin('M1110,300 L1110,420 M1100,310 L1110,300 L1120,310 M1100,410 L1110,420 L1120,410', o=0.6)
    p.appel(1, 70, 470, 120, 470)
    p.appel(2, 1090, 80, 1060, 120)
    p.appel(3, 860, 640, 780, 612)
    p.appel(4, 1110, 470, 1110, 424)


@section('lf-finale', 'Background image', 'Large heading', 'Links in glass cards')
def _(p):
    fond_photo(p)
    p.surtitre(W / 2, 200, 120, centre=True)
    p.mot(W / 2, 330, 'THE ESSENTIALS', 96, 'middle')
    for i in range(3):
        x = 150 + i * 300
        p.verre(x, 440, 260, 110, 18)
        p.mot(x + 24, 488, 'Collection', 24)
        p.ligne(x + 24, 518, x + 180, 518, o=0.4, sw=2)
        p.fleche(x + 230, 496, 1, 12)
    p.appel(1, 80, 100, 140, 140)
    p.appel(2, W / 2 + 420, 300, W / 2 + 380, 300)
    p.appel(3, 100, 600, 150, 550)


def infos_produit(p, x=640):
    """Colonne d'informations d'une fiche produit."""
    p.surtitre(x, 70)
    p.mot(x, 140, 'Product title', 48)
    p.ligne(x, 180, x + 440, 180, o=0.3, sw=1.4)
    p.mot(x, 236, '$49.00', 36)
    p.ligne(x, 262, x + 90, 262, o=0.35, sw=2)
    p.ligne(x, 306, x + 70, 306, o=0.6, sw=2)
    p.pastille(x + 14, 340, 14, plein=True)
    p.pastille(x + 52, 340, 14)
    p.rect(x, 392, 120, 48, 24)
    p.bouton(x + 136, 392, 304, 48, plein=True)
    p.bouton(x, 456, 440, 46)
    return x


def fiche_produit(p, vignettes=True):
    p.rect(40, 40, 520, 520, 14, o=0.5)
    p.produit(40, 40, 520, 520, cadre=False, echelle=2.6)
    if vignettes:
        p.verre(150, 580, 300, 64, 16)
        for i in range(5):
            p.rect(164 + i * 56, 592, 44, 40, 8, o=1 if i == 0 else 0.5)
    return infos_produit(p)


@section('featured-product', 'Product media', 'Title and price', 'Variant picker', 'Quantity and buy buttons')
def _(p):
    x = fiche_produit(p, vignettes=False)
    for i in range(4):
        p.rect(170 + i * 70, 586, 56, 56, 8, o=1 if i == 0 else 0.5)
    p.appel(1, 30, 620, 100, 560)
    p.appel(2, x - 50, 120, x - 6, 130)
    p.appel(3, x + 120, 340, x + 70, 340)
    p.appel(4, x - 50, 440, x - 6, 430)


def cartes(p, y, n=4, w=None, x0=60, h=300, prix=True):
    w = w or (W - 2 * x0 - (n - 1) * 20) / n
    for i in range(n):
        x = x0 + i * (w + 20)
        p.rect(x, y, w, h, 12, o=0.5)
        p.produit(x, y, w, h, cadre=False, echelle=min(w, h) / 120)
        p.ligne(x + w * 0.2, y + h + 30, x + w * 0.8, y + h + 30, o=0.6, sw=2)
        if prix:
            p.ligne(x + w * 0.38, y + h + 54, x + w * 0.62, y + h + 54, o=0.38, sw=2)
    return w


@section('featured-collection', 'Heading', 'Product cards from the collection', 'Button to the collection')
def _(p):
    p.mot(W / 2, 100, 'You may also like', 44, 'middle')
    cartes(p, 160, 4)
    p.bouton(W / 2 - 80, 580, 160, 44)
    p.appel(1, W / 2 + 230, 86, W / 2 + 190, 86)
    p.appel(2, 30, 140, 70, 180)
    p.appel(3, W / 2 + 130, 602, W / 2 + 80, 602)


@section('lf-drag-rail', 'Heading', 'Filter tabs', 'Cards in a rail you can drag', 'Glass cursor that invites dragging, can be turned off')
def _(p):
    p.mot(60, 110, 'Pieces designed', 46)
    p.mot(60, 162, 'for every day.', 46)
    x = 600
    for i, lg in enumerate((120, 96, 96, 110)):
        p.rect(x, 128, lg, 38, 19, fill=p.encre if i == 0 else None)
        x += lg + 12
    cartes(p, 230, 5, w=250, h=270)
    p.verre(530, 300, 96, 96, 48)
    p.fleche(560, 348, -1, 10)
    p.fleche(596, 348, 1, 10)
    p.appel(1, 480, 90, 420, 110)
    p.appel(2, 1090, 100, 1060, 128)
    p.appel(3, 1110, 620, 1110, 520)
    p.appel(4, 700, 330, 626, 340)


@section('lf-mosaic', 'Product tiles', 'Center card with heading', 'Link to the collection')
def _(p):
    for r in range(2):
        for c in range(6):
            if c in (2, 3):
                continue
            p.produit(40 + c * 183, 40 + r * 310, 170, 290, 10)
    for r in range(2):
        for c in (2, 3):
            p.rect(40 + c * 183, 40 + r * 310, 170, 290, 10, o=0.25)
    p.verre(406, 220, 348, 240, 18)
    p.mot(W / 2, 320, 'COLLECTION', 36, 'middle')
    p.ligne(W / 2 - 80, 352, W / 2 + 80, 352, o=0.38, sw=2)
    p.lien(W / 2 - 40, 400, 80)
    p.appel(1, 30, 360, 80, 300)
    p.appel(2, W / 2, 196, W / 2, 220)
    p.appel(3, W / 2 + 110, 404, W / 2 + 42, 404)


@section('lf-colorways', 'Heading and text', 'Large photo of the range', 'Glass card: color name and link',
         'Swatches switch the photo')
def _(p):
    p.mot(40, 64, 'Two shades & two characters', 40)
    p.texte(40, 100, 360, 3)
    p.photo(0, 160, W, H - 160, 0, o=0)
    p.ligne(0, 160, W, 160, o=0.5, sw=1.6)
    p.verre(40, 450, 280, 180, 18)
    p.mot(64, 500, 'Beige', 30)
    p.ligne(64, 528, 220, 528, o=0.4, sw=2)
    p.pastille(78, 566, 12)
    p.pastille(110, 566, 12, plein=True)
    p.lien(64, 598, 110)
    p.appel(1, 600, 64, 560, 60)
    p.appel(2, 900, 300, 820, 340)
    p.appel(3, 380, 500, 320, 500)
    p.appel(4, 180, 566, 126, 566)


@section('lf-blueprint', 'Heading and text', 'Product tabs', 'Size selector', 'Technical drawings with dimensions',
         'Specification table')
def _(p):
    p.surtitre(40, 50)
    p.mot(40, 110, 'Proportions studied', 42)
    p.mot(40, 160, 'with care', 42)
    p.texte(40, 196, 340, 3)
    for i in range(3):
        p.rect(700 + i * 130, 64, 118, 36, 18, fill=p.encre if i == 0 else None)
    for i in range(3):
        p.rect(700 + i * 76, 140, 64, 30, 15, fill=p.encre if i == 0 else None)
    p.teeshirt(250, 440, 2.6)
    p.cote(162, 572, 338, 572, 'width 52 cm')
    p.cote(440, 341, 440, 544, 'length 70 cm')
    p.cote(349, 300, 396, 300, 'sleeve')
    for i in range(4):
        y = 300 + i * 70
        p.ligne(720, y, 1120, y, o=0.3, sw=1.4)
        p.ligne(720, y + 30, 800, y + 30, o=0.4, sw=2)
        p.mot(1120, y + 40, ('S \u00b7 M \u00b7 L', '180 g/m\u00b2', '100% cotton', 'Regular fit')[i], 26, 'end')
    p.appel(1, 430, 110, 390, 110)
    p.appel(2, 1120, 40, 1090, 64)
    p.appel(3, 960, 155, 930, 155)
    p.appel(4, 120, 620, 162, 572)
    p.appel(5, 1120, 620, 1090, 590)


@section('lf-recommendations', 'Heading', 'Products picked by Shopify for the product shown')
def _(p):
    p.mot(W / 2, 110, 'You may also like', 44, 'middle')
    cartes(p, 180, 4, h=320)
    p.appel(1, W / 2 + 230, 96, W / 2 + 190, 96)
    p.appel(2, 30, 160, 70, 200)


@section('lf-index-list', 'Each line: large type and a link', 'Side note', 'Preview image on hover')
def _(p):
    p.ligne(40, 60, W - 40, 60, o=0.3, sw=1.4)
    for i, m in enumerate(('NEW IN', 'ESSENTIALS', 'ACCESSORIES')):
        y = 60 + (i + 1) * 170
        p.mot(40, y - 64, '0' + str(i + 1), 16, famille=SANS, poids=400, o=0.6)
        p.mot(90, y - 50, m, 92, o=1 if i != 1 else 0.35)
        p.ligne(W - 200, y - 80, W - 60, y - 80, o=0.38, sw=2)
        p.ligne(40, y, W - 40, y, o=0.3, sw=1.4)
    p.photo(700, 150, 220, 280, 14)
    p.appel(1, 40, 620, 110, 572)
    p.appel(2, W - 130, 40, W - 130, 140)
    p.appel(3, 980, 290, 920, 290)


@section('lf-manifesto', 'Statement, with words revealed as visitors scroll', 'Italic emphasis', 'Link', 'Key figures')
def _(p):
    p.surtitre(60, 80)
    p.mot(60, 190, 'We favour strong materials,', 66)
    p.mot(60, 270, 'timeless shapes and a design', 66, o=0.45)
    p.mot(60, 350, 'made to last.', 66, italique=True, o=0.45)
    p.lien(60, 410, 120)
    for i, t in enumerate(('2010', '100%', '48 h', '5 years')):
        x = 60 + i * 200
        p.ligne(x, 500, x + 150, 500, o=0.5, sw=1.6)
        p.mot(x, 556, t, 40)
        p.ligne(x, 584, x + 80, 584, o=0.38, sw=2)
    p.appel(1, 1040, 170, 980, 170)
    p.appel(2, 520, 400, 440, 350)
    p.appel(3, 240, 420, 186, 415)
    p.appel(4, 920, 540, 880, 540)


@section('lf-inlay', 'Sentence in large type', 'Images set between the words', 'Glass caption on hover')
def _(p):
    p.surtitre(W / 2, 170, 110, centre=True)
    p.mot(80, 300, 'Every detail,', 64)
    p.teeshirt(500, 280, 0.95)
    p.mot(580, 300, 'reveals the craft', 64)
    p.rond(220, 404, 36, o=0.6)
    p.teeshirt(220, 405, 0.42)
    p.mot(290, 424, 'natural', 64)
    p.rond(560, 404, 36, o=0.6)
    p.teeshirt(560, 405, 0.42)
    p.mot(630, 424, 'elegance', 64, italique=True)
    p.verre(430, 318, 150, 40, 20)
    p.ligne(460, 338, 550, 338, o=0.5, sw=2)
    p.appel(1, 1080, 230, 1040, 280)
    p.appel(2, 160, 500, 200, 440)
    p.appel(3, 640, 338, 582, 338)


@section('lf-sticky-story', 'Intro that stays in place', 'Chapter list', 'Images that scroll past')
def _(p):
    p.surtitre(60, 80)
    p.mot(60, 150, 'The making of', 48)
    p.mot(60, 206, 'a timeless piece', 48)
    p.texte(60, 244, 400, 2)
    for i in range(3):
        y = 330 + i * 72
        p.ligne(60, y, 500, y, o=0.3, sw=1.4)
        p.mot(60, y + 37, '0' + str(i + 1), 14, famille=SANS, poids=400, o=0.6)
        p.ligne(100, y + 32, 230, y + 32, o=0.8, sw=2)
        p.ligne(100, y + 54, 400, y + 54, o=0.35, sw=2)
    p.photo(640, 40, 480, 280, 14)
    p.ligne(640, 344, 760, 344, o=0.4, sw=2)
    p.photo(640, 420, 480, 280, 14)
    p.chemin('M570,250 L570,420 M560,260 L570,250 L580,260 M560,410 L570,420 L580,410', o=0.5)
    p.appel(1, 530, 150, 490, 150)
    p.appel(2, 530, 520, 500, 500)
    p.appel(3, 1110, 370, 1080, 320)


@section('lf-deck', 'Chapter card with its photo', 'Heading, text and button', 'Cards stack as visitors scroll')
def _(p):
    p.rect(120, 120, W - 240, 540, 20, o=0.35)
    p.rect(90, 80, W - 180, 560, 20, o=0.6)
    p.out.append(f'<rect x="60" y="40" width="{W - 120}" height="600" rx="20" fill="#ffffff" fill-opacity="{0.08 if p.clair else 1}" stroke="none"/>')
    p.photo(60, 40, W - 120, 600, 20)
    p.surtitre(110, 400)
    p.mot(110, 470, 'The art of slow making', 56)
    p.bouton(110, 510, 160, 44)
    p.lien(300, 522, 120)
    p.appel(1, 1020, 100, 980, 160)
    p.appel(2, 790, 460, 730, 460)
    p.appel(3, 1110, 660, 1080, 650)


@section('lf-timeline', 'Chapter: eyebrow, heading and text', 'Key figure', 'Image of the chapter',
         'Years on a line that fills as visitors scroll')
def _(p):
    p.surtitre(60, 120)
    p.mot(60, 200, 'Craft that endures', 50)
    p.texte(60, 244, 420, 3)
    p.ligne(60, 330, 500, 330, o=0.3, sw=1.4)
    p.mot(60, 404, '+200', 56)
    p.ligne(210, 396, 330, 396, o=0.38, sw=2)
    p.photo(640, 40, 480, 470, 16)
    p.ligne(60, 590, W - 60, 590, o=0.4, sw=1.4)
    p.ligne(60, 590, 520, 590, o=1, sw=2.6)
    for i, a in enumerate(('2010', '2015', '2020', '2025')):
        x = 60 + i * (W - 120) / 3
        p.pastille(x, 590, 6, plein=i < 2)
        p.mot(x, 626, a, 16, 'middle', famille=SANS, poids=400, o=0.7)
    p.appel(1, 560, 200, 520, 200)
    p.appel(2, 400, 440, 340, 400)
    p.appel(3, 1110, 560, 1080, 500)
    p.appel(4, 600, 550, 520, 590)


@section('lf-collage', 'Images at different sizes', 'Captions in glass', 'Text block', 'Each image moves at its own speed')
def _(p):
    p.photo(40, 40, 230, 300, 12)
    p.photo(300, 80, 260, 200, 12)
    p.photo(590, 30, 200, 320, 12)
    p.photo(830, 60, 290, 240, 12)
    p.photo(60, 380, 260, 260, 12)
    p.photo(880, 340, 240, 300, 12)
    for x, y in ((60, 296), (850, 256)):
        p.verre(x, y, 120, 30, 15)
        p.ligne(x + 24, y + 15, x + 96, y + 15, o=0.5, sw=2)
    p.mot(W / 2, 470, 'Stories from', 40, 'middle')
    p.mot(W / 2, 516, 'the studio', 40, 'middle', italique=True)
    p.texte(W / 2 - 140, 556, 280, 2)
    p.appel(1, 430, 330, 430, 280)
    p.appel(2, 220, 360, 180, 326)
    p.appel(3, W / 2 + 200, 480, W / 2 + 130, 480)
    p.appel(4, 1140, 330, 1120, 300)


@section('lf-editorial-grid', 'Cards with a photo each', 'Caption and link, in glass')
def _(p):
    for i, (y, h) in enumerate(((60, 560), (140, 480), (40, 600))):
        x = 40 + i * 370
        p.photo(x, y, 340, h, 16)
        p.verre(x + 20, y + h - 90, 300, 70, 16)
        p.mot(x + 40, y + h - 46, 'Chapter', 24)
        p.fleche(x + 290, y + h - 55, 1, 10)
    p.appel(1, 420, 100, 440, 160)
    p.appel(2, 770, 650, 720, 600)


@section('lf-marquee', 'Short messages', 'Cut-out images between the words', 'Direction and speed of the scroll')
def _(p):
    p.ligne(0, 230, W, 230, o=0.3, sw=1.4)
    p.ligne(0, 420, W, 420, o=0.3, sw=1.4)
    p.mot(-60, 352, 'Made to last', 84)
    p.chemin('M478,300 L486,320 L506,328 L486,336 L478,356 L470,336 L450,328 L470,320 Z', o=0.8)
    p.teeshirt(600, 326, 0.9)
    p.mot(690, 352, 'Designed with care', 84)
    p.chemin('M200,500 L960,500 M940,488 L960,500 L940,512', o=0.6)
    p.appel(1, 300, 190, 260, 290)
    p.appel(2, 600, 190, 600, 290)
    p.appel(3, 1010, 500, 968, 500)


@section('rich-text', 'Heading', 'Text', 'Button')
def _(p):
    p.surtitre(W / 2, 200, 100, centre=True)
    p.mot(W / 2, 290, 'Essentials for every day', 56, 'middle')
    p.texte(W / 2 - 260, 340, 520, 2, fin=0.8)
    p.lien(W / 2 - 55, 420, 110)
    p.appel(1, W / 2 + 400, 270, W / 2 + 350, 270)
    p.appel(2, W / 2 + 330, 350, W / 2 + 270, 350)
    p.appel(3, W / 2 + 120, 425, W / 2 + 62, 425)


@section('image-with-text', 'Image', 'Eyebrow, heading and text', 'Button')
def _(p):
    p.photo(40, 80, 560, 520, 16)
    p.surtitre(680, 240)
    p.mot(680, 310, 'Made by hand,', 46)
    p.mot(680, 362, 'finished with care', 46)
    p.texte(680, 404, 380, 3)
    p.bouton(680, 480, 200, 46, plein=True)
    p.appel(1, 320, 640, 320, 600)
    p.appel(2, 1120, 300, 1070, 330)
    p.appel(3, 930, 503, 880, 503)


@section('multicolumn', 'Heading', 'Columns: image, title and text', 'Button')
def _(p):
    p.mot(40, 80, 'Made for everyday life', 40)
    for i in range(3):
        x = 40 + i * 370
        p.photo(x, 120, 340, 300, 12)
        p.mot(x, 470, 'Column', 26)
        p.texte(x, 500, 300, 2)
    p.bouton(W / 2 - 75, 590, 150, 42)
    p.appel(1, 660, 66, 620, 66)
    p.appel(2, 380, 446, 336, 462)
    p.appel(3, W / 2 + 120, 611, W / 2 + 75, 611)


@section('lf-before-after', 'Two images, before and after', 'Handle dragged across', 'Label on each side')
def _(p):
    p.mot(40, 64, 'Beige & Navy blue', 40)
    p.photo(40, 110, 540, 520, 0, o=0)
    p.out.append(f'<rect x="580" y="110" width="540" height="520" fill="{p.encre}" fill-opacity=".1"/>')
    p.rect(40, 110, 1080, 520, 14)
    p.ligne(580, 110, 580, 630, sw=2.4)
    p.verre(552, 342, 56, 56, 28)
    p.fleche(570, 370, -1, 9)
    p.fleche(590, 370, 1, 9)
    p.verre(64, 584, 80, 30, 15)
    p.verre(1016, 584, 80, 30, 15)
    p.appel(1, 300, 90, 300, 140)
    p.appel(2, 680, 370, 608, 370)
    p.appel(3, 210, 599, 144, 599)


@section('lf-testimonials', 'Heading', 'Rating', 'Quote and author', 'Arrows between quotes')
def _(p):
    p.surtitre(W / 2, 140, 100, centre=True)
    p.mot(W / 2, 210, 'They trust us', 48, 'middle')
    for i in range(5):
        cx = W / 2 - 60 + i * 30
        p.chemin(f'M{cx},252 L{cx + 4},262 L{cx + 14},262 L{cx + 6},268 L{cx + 9},278 L{cx},272 L{cx - 9},278 '
                 f'L{cx - 6},268 L{cx - 14},262 L{cx - 4},262 Z', sw=1.4)
    p.mot(W / 2, 340, 'Simple to use, ready in no time.', 34, 'middle', italique=True)
    p.texte(W / 2 - 220, 380, 440, 2, fin=0.7)
    p.ligne(W / 2 - 60, 450, W / 2 + 60, 450, o=0.6, sw=2)
    p.rond(W / 2 - 30, 530, 20)
    p.fleche(W / 2 - 30, 530, -1, 10)
    p.rond(W / 2 + 30, 530, 20)
    p.fleche(W / 2 + 30, 530, 1, 10)
    p.appel(1, W / 2 + 250, 196, W / 2 + 170, 196)
    p.appel(2, W / 2 + 140, 265, W / 2 + 90, 265)
    p.appel(3, W / 2 + 340, 340, W / 2 + 290, 340)
    p.appel(4, W / 2 + 120, 530, W / 2 + 52, 530)


@section('lf-press', 'Eyebrow', 'Publication names, as text or logos', 'Quote for each publication')
def _(p):
    p.surtitre(W / 2, 200, 140, centre=True)
    for i, t in enumerate(('Journal', 'Magazine', 'Review', 'Weekly')):
        p.mot(170 + i * 273, 330, t, 44, 'middle', italique=True, o=1 if i != 1 else 0.4)
    p.texte(W / 2 - 230, 420, 460, 2, fin=0.6)
    p.ligne(60, 480, W - 60, 480, o=0.25, sw=1.4)
    p.ligne(60, 480, 400, 480, o=1, sw=2)
    p.appel(1, W / 2 + 140, 170, W / 2 + 80, 200)
    p.appel(2, 60, 250, 110, 300)
    p.appel(3, W / 2 + 300, 430, W / 2 + 240, 430)


@section('lf-faq', 'Eyebrow and heading', 'Question', 'Answer, open', 'Button that opens and closes')
def _(p):
    p.surtitre(W / 2, 70, 100, centre=True)
    p.mot(W / 2, 140, 'Frequently asked questions', 46, 'middle')
    y = 200
    for i in range(5):
        p.ligne(160, y, W - 160, y, o=0.3, sw=1.4)
        p.mot(170, y + 46, '0' + str(i + 1), 13, famille=SANS, poids=400, o=0.6)
        p.ligne(210, y + 41, 210 + (300, 340, 260, 300, 320)[i], y + 41, o=0.85, sw=2.2)
        p.rond(W - 190, y + 41, 16)
        p.ligne(W - 197, y + 41, W - 183, y + 41)
        if i != 1:
            p.ligne(W - 190, y + 34, W - 190, y + 48)
        if i == 1:
            p.texte(210, y + 86, 560, 3)
            y += 70
        y += 82
    p.ligne(160, y, W - 160, y, o=0.3, sw=1.4)
    p.appel(1, W / 2 + 390, 126, W / 2 + 330, 126)
    p.appel(2, 110, 241, 196, 241)
    p.appel(3, 110, 370, 200, 350)
    p.appel(4, W - 110, 241, W - 172, 241)


@section('contact-form', 'Fields: name, email, phone and message', 'Send button')
def _(p):
    x0, w = 300, 560
    for x, y, lw in ((x0, 120, 260), (x0 + 300, 120, 260), (x0, 220, 260)):
        p.ligne(x, y, x + 44, y, o=0.6, sw=1.8)
        p.ligne(x, y + 46, x + lw, y + 46, o=0.6, sw=1.6)
    p.ligne(x0, 320, x0 + 60, 320, o=0.6, sw=1.8)
    p.rect(x0, 340, w, 160, 6, o=0.5)
    p.bouton(W / 2 - 90, 550, 180, 46, plein=True)
    p.appel(1, x0 - 60, 166, x0 - 6, 166)
    p.appel(2, W / 2 + 140, 573, W / 2 + 90, 573)


@section('email-signup-banner', 'Background image', 'Heading and text', 'Email field and button')
def _(p):
    fond_photo(p)
    p.verre(W / 2 - 300, 170, 600, 330, 26)
    p.mot(W / 2, 260, 'Join our letter', 46, 'middle')
    p.texte(W / 2 - 180, 300, 360, 2, fin=0.75)
    p.rect(W / 2 - 220, 380, 300, 48, 24)
    p.bouton(W / 2 + 92, 380, 128, 48, plein=True)
    p.appel(1, 120, 100, 180, 140)
    p.appel(2, W / 2 + 360, 260, W / 2 + 300, 260)
    p.appel(3, W / 2 + 360, 404, W / 2 + 222, 404)


@section('page', 'Page title', 'Page content, written in Online Store > Pages')
def _(p):
    p.mot(W / 2, 170, 'About us', 64, 'middle')
    p.texte(W / 2 - 300, 260, 600, 4, pas=22)
    p.texte(W / 2 - 300, 380, 600, 3, pas=22, fin=0.4)
    p.appel(1, W / 2 + 240, 150, W / 2 + 150, 150)
    p.appel(2, W / 2 + 370, 300, W / 2 + 306, 300)


@section('main-page', 'Page title', 'Page content, written in Online Store > Pages')
def _(p):
    S['page'](p)


@section('custom-liquid', 'Your own Liquid, HTML or embed code')
def _(p):
    p.rect(260, 140, 640, 400, 16)
    p.ligne(260, 186, 900, 186, o=0.4, sw=1.4)
    for i in range(3):
        p.rond(290 + i * 22, 163, 6, o=0.5)
    for i, (ind, lg) in enumerate(((0, 260), (40, 320), (80, 200), (80, 280), (40, 120), (0, 180))):
        p.ligne(300 + ind, 233 + i * 46, 300 + ind + lg, 233 + i * 46, o=0.5 if i % 2 else 0.85, sw=2.4)
    p.mot(W / 2, 620, '{% … %}', 28, 'middle', famille='Menlo, monospace', poids=400, o=0.6)
    p.appel(1, 960, 300, 900, 300)


@section('apps', 'App blocks added by your apps', 'Full width, or within the page margins')
def _(p):
    for x, w in ((120, 440), (600, 440)):
        p.rect(x, 200, w, 260, 16, dash='8 8')
        p.chemin(f'M{x + w / 2 - 24},336 l0,-20 l16,0 a8,8 0 0 1 16,0 l16,0 l0,20 a8,8 0 0 0 0,16 l0,20 l-48,0 Z', o=0.7)
    p.cote(120, 520, 1040, 520, 'page width')
    p.appel(1, 580, 160, 560, 200)
    p.appel(2, 1090, 520, 1046, 520)


@section('lf-divider', 'Line: color, thickness and style', 'Space above and below', 'Full width, or within the page margins')
def _(p):
    p.photo(60, 40, 480, 200, 12, o=0.5)
    p.texte(620, 120, 400, 3, o=0.25)
    p.ligne(60, 338, W - 60, 338, sw=2.4)
    p.cote(1100, 262, 1100, 330, 'above')
    p.cote(1100, 346, 1100, 414, 'below')
    p.mot(60, 500, 'Made for everyday life', 40, o=0.3)
    p.texte(60, 540, 500, 2, o=0.2)
    p.cote(60, 300, 1040, 300)
    p.appel(1, 400, 390, 400, 340)
    p.appel(2, 1030, 236, 1092, 280)
    p.appel(3, 560, 266, 560, 300)


@section('lf-product', 'Gallery: stacked or carousel', 'Thumbnails in a glass strip', 'Title, price and text',
         'Variant picker with swatches', 'Quantity and buy buttons')
def _(p):
    x = fiche_produit(p)
    p.appel(1, 30, 30, 80, 70)
    p.appel(2, 500, 612, 452, 612)
    p.appel(3, x - 50, 120, x - 6, 130)
    p.appel(4, x + 120, 340, x + 70, 340)
    p.appel(5, x - 50, 440, x - 6, 430)


@section('main-collection-product-grid', 'Collection title', 'Links to other collections', 'Filter and sort', 'Product grid')
def _(p):
    p.mot(W / 2, 120, 'Products', 84, 'middle')
    for i in range(3):
        p.rect(W / 2 - 200 + i * 136, 160, 124, 36, 18)
    p.ligne(40, 236, W - 40, 236, o=0.3, sw=1.4)
    p.ligne(40, 262, 100, 262, o=0.7, sw=2)
    p.ligne(W - 140, 262, W - 40, 262, o=0.7, sw=2)
    p.ligne(40, 288, W - 40, 288, o=0.3, sw=1.4)
    cartes(p, 320, 4, h=260, x0=40)
    p.appel(1, W / 2 + 270, 90, W / 2 + 210, 90)
    p.appel(2, W / 2 + 270, 178, W / 2 + 212, 178)
    p.appel(3, 160, 262, 106, 262)
    p.appel(4, 20, 450, 40, 450)


@section('main-list-collections', 'Page title', 'One card per collection')
def _(p):
    p.mot(W / 2, 110, 'Collections', 64, 'middle')
    for c in range(3):
        x = 60 + c * 360
        p.produit(x, 170, 320, 360, 14, echelle=1.6)
        p.ligne(x + 100, 570, x + 220, 570, o=0.7, sw=2)
    p.appel(1, W / 2 + 240, 92, W / 2 + 180, 92)
    p.appel(2, 30, 350, 60, 350)


@section('main-search', 'Search field', 'Number of results', 'Results: products, articles and pages')
def _(p):
    p.rect(W / 2 - 300, 60, 600, 56, 28)
    p.rond(W / 2 + 250, 86, 10)
    p.ligne(W / 2 + 257, 93, W / 2 + 265, 101)
    p.ligne(W / 2 - 260, 88, W / 2 - 160, 88, o=0.4, sw=2)
    p.ligne(40, 170, 140, 170, o=0.6, sw=2)
    cartes(p, 210, 4, h=270, x0=40)
    p.appel(1, W / 2 + 360, 88, W / 2 + 302, 88)
    p.appel(2, 200, 170, 146, 170)
    p.appel(3, 20, 340, 40, 340)


@section('main-cart-items', 'Products in the cart', 'Quantity and remove', 'Summary in glass: subtotal, notes and checkout')
def _(p):
    p.mot(40, 90, 'Your cart', 64)
    for i in range(3):
        y = 150 + i * 150
        p.ligne(40, y, 700, y, o=0.3, sw=1.4)
        p.produit(40, y + 20, 110, 110, 10, echelle=0.7)
        p.ligne(180, y + 50, 380, y + 50, o=0.85, sw=2.2)
        p.ligne(180, y + 78, 260, y + 78, o=0.4, sw=2)
        p.rect(460, y + 50, 120, 40, 20)
        p.ligne(620, y + 70, 690, y + 70, o=0.7, sw=2)
    p.verre(760, 150, 360, 380, 22)
    for i in range(3):
        p.ligne(790, 210 + i * 50, 880, 210 + i * 50, o=0.5, sw=2)
        p.ligne(1010, 210 + i * 50, 1090, 210 + i * 50, o=0.8, sw=2)
    p.bouton(790, 440, 300, 50, plein=True)
    p.appel(1, 20, 240, 40, 240)
    p.appel(2, 520, 160, 520, 200)
    p.appel(3, 1140, 130, 1110, 160)


@section('main-blog', 'Blog title', 'Article cards: image, date, title and excerpt')
def _(p):
    p.mot(W / 2, 100, 'News', 64, 'middle')
    for i in range(3):
        x = 40 + i * 370
        p.photo(x, 150, 340, 260, 12)
        p.ligne(x, 440, x + 90, 440, o=0.5, sw=1.8)
        p.mot(x, 486, 'Article title', 28)
        p.texte(x, 520, 300, 3)
    p.appel(1, W / 2 + 140, 82, W / 2 + 90, 82)
    p.appel(2, 400, 610, 340, 560)


@section('main-article', 'Title, date and author', 'Article image', 'Article content')
def _(p):
    p.mot(W / 2, 90, 'Inside the studio', 54, 'middle')
    p.ligne(W / 2 - 80, 124, W / 2 + 80, 124, o=0.5, sw=1.8)
    p.photo(160, 160, W - 320, 300, 14)
    p.texte(260, 500, W - 520, 3, pas=20)
    p.mot(260, 600, 'Behind the scenes', 30)
    p.texte(260, 630, W - 520, 2, pas=20)
    p.appel(1, W / 2 + 330, 80, W / 2 + 270, 80)
    p.appel(2, W - 100, 300, W - 160, 300)
    p.appel(3, 200, 520, 254, 520)


@section('main-404', 'Message', 'Button back to the store')
def _(p):
    p.surtitre(W / 2, 230, 60, centre=True)
    p.mot(W / 2, 330, 'Page not found', 72, 'middle')
    p.bouton(W / 2 - 100, 390, 200, 46)
    p.appel(1, W / 2 + 330, 310, W / 2 + 270, 310)
    p.appel(2, W / 2 + 150, 413, W / 2 + 100, 413)


# ── Illustrations des guides (accueil), sans legende ──

def illustration(h):
    def deco(f):
        S[h] = f
        return f
    return deco


@illustration('guide-quick-view')
def _(p):
    cartes(p, 60, 3, w=180, x0=40, h=250)
    p.verre(370, 74, 44, 44, 22)
    p.croix(392, 96, 8)
    p.verre(320, 74, 44, 44, 22)
    p.rond(340, 94, 8)
    p.ligne(346, 100, 352, 106)
    p.verre(640, 20, 500, 640, 26)
    p.ligne(670, 62, 760, 62, o=0.6, sw=1.8)
    p.rond(1100, 60, 16)
    p.produit(670, 96, 300, 300, 14, echelle=1.5)
    p.rect(990, 96, 120, 300, 14, o=0.4)
    p.mot(670, 452, 'Product title', 34)
    p.mot(670, 498, '$49.00', 26)
    p.pastille(684, 548, 13, plein=True)
    p.pastille(722, 548, 13)
    p.rect(670, 590, 120, 46, 23)
    p.bouton(804, 590, 306, 46, plein=True)


@illustration('guide-product-page')
def _(p):
    fiche_produit(p)


@illustration('guide-product-carousel')
def _(p):
    p.rect(40, 40, 520, 600, 14, o=0.5)
    p.produit(40, 40, 520, 600, cadre=False, echelle=2.6)
    for cx, sens in ((84, -1), (516, 1)):
        p.verre(cx - 22, 318, 44, 44, 22)
        p.fleche(cx, 340, sens, 10)
    p.verre(150, 548, 300, 56, 16)
    for i in range(5):
        p.rect(162 + i * 56, 556, 44, 40, 8, o=1 if i == 0 else 0.5)
    p.ligne(150, 620, 450, 620, o=0.3, sw=3)
    p.ligne(150, 620, 230, 620, o=1, sw=3)
    infos_produit(p)


@illustration('guide-product-thumbs')
def _(p):
    p.verre(40, 40, 72, 340, 18)
    for i in range(5):
        p.rect(52, 52 + i * 64, 48, 52, 8, o=1 if i == 0 else 0.5)
    for y in (40, 360):
        p.rect(132, y, 428, 300, 14, o=0.5)
        p.produit(132, y, 428, 300, cadre=False, echelle=1.8)
    infos_produit(p)


@illustration('guide-card-actions')
def _(p):
    cartes(p, 70, 3, w=320, x0=60, h=420)
    p.verre(640, 92, 52, 52, 26)
    p.rond(664, 116, 9)
    p.ligne(671, 123, 679, 131)
    p.verre(470, 92, 156, 52, 26)
    p.croix(498, 118, 9)
    p.ligne(522, 118, 598, 118, o=0.6, sw=2.2)
    p.chemin('M560,150 L560,186 L569,177 L576,192 L582,189 L575,175 L588,175 Z', sw=1.6, fill='#ffffff' if not p.clair else None)


@illustration('guide-cinematic-intro')
def _(p):
    fond_photo(p)
    p.voile(0.06)
    p.entete(0, 72, o=0.35, transparent=True)
    p.mot(W / 2, H / 2 + 40, 'Logo', 150, 'middle')
    p.chemin(f'M{W / 2},{H / 2 - 80} C{W / 2 - 60},{H / 2 - 160} {W / 2 - 40},{150} {W / 2},{90}', o=0.6, sw=1.6)
    p.fleche(W / 2, 92, 1, 12)
    p.out[-1] = p.out[-1].replace('<path', f'<path transform="rotate(-90 {W / 2} 92)"')


@illustration('guide-mega-menu')
def _(p):
    p.entete(0, 76, o=0.9)
    p.ligne(110, 52, 180, 52, o=1, sw=2.2)
    p.verre(40, 92, W - 80, 330, 22)
    for k in range(5):
        p.ligne(80, 140 + k * 40, 200 + (k % 2) * 40, 140 + k * 40, o=0.85 if k == 0 else 0.45, sw=2.2)
    p.ligne(300, 120, 300, 390, o=0.3, sw=1.4)
    cartes(p, 120, 3, w=230, x0=350, h=200)
    p.photo(0, 440, W, H - 440, 0, o=0)


@illustration('guide-swatches')
def _(p):
    p.produit(40, 60, 520, 556, 16, echelle=2.6)
    p.mot(640, 150, 'Product title', 48)
    p.mot(640, 220, '$49.00', 34)
    p.ligne(640, 296, 700, 296, o=0.7, sw=2)
    p.ligne(716, 296, 800, 296, o=0.4, sw=2)
    for i in range(4):
        cx = 664 + i * 72
        if i == 0:
            p.rond(cx, 360, 31, sw=1.6)
        if i == 2:
            p.out.append(f'<circle cx="{cx}" cy="360" r="24" fill="url(#{p.pid}-h)" stroke="none"/>')
        p.pastille(cx, 360, 24, plein=i == 0)
    p.bouton(640, 450, 440, 50, plein=True)


# ─────────────────────────────────────────────────────────────────────────

def svg(h, mini=False, encre='#111110', titre=''):
    """Le schema de la section h, dans son cadre de navigateur."""
    pid = f's-{h}{"-m" if mini else ""}'
    p = Planche(encre, mini, pid)
    S[h](p)
    k = p.k
    chrome = (
        f'<rect x="20" y="20" width="1160" height="720" rx="20" fill="none" stroke="{encre}" stroke-width="{2 * k:.2f}"/>'
        f'<line x1="20" y1="64" x2="1180" y2="64" stroke="{encre}" stroke-width="{1.6 * k:.2f}" stroke-opacity=".5"/>'
        + ''.join(f'<circle cx="{46 + i * 20}" cy="42" r="5.5" fill="none" stroke="{encre}" '
                  f'stroke-width="{1.6 * k:.2f}" stroke-opacity=".6"/>' for i in range(3))
        + f'<rect x="480" y="33" width="240" height="18" rx="9" fill="none" stroke="{encre}" '
          f'stroke-width="{1.4 * k:.2f}" stroke-opacity=".4"/>'
    )
    defs = (
        f'<defs><pattern id="{pid}-h" width="13" height="13" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<line x1="0" y1="0" x2="0" y2="13" stroke="{encre}" stroke-width="{1.3 * k:.2f}" stroke-opacity=".2"/></pattern>'
        f'<clipPath id="{pid}-c"><path d="M20,64 H1180 V720 a20,20 0 0 1 -20,20 H40 a20,20 0 0 1 -20,-20 Z"/></clipPath></defs>'
    )
    corps = f'<g clip-path="url(#{pid}-c)"><g transform="translate(20 64)">{"".join(p.out)}</g></g>'
    appels = '' if mini else f'<g transform="translate(20 64)">{p.rendu_appels()}</g>'
    lab = f' role="img" aria-label="{html.escape(titre)}"' if titre else ' aria-hidden="true"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760"{lab}>'
            f'{defs}{chrome}{corps}{appels}</svg>')

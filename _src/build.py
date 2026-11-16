"""Assemble the static Bāyit site from _src/pages/*.html + shared header/footer.

Run from anywhere:  python Clients/Bayit/website/_src/build.py
Each page keeps its live-site URL (/menu/, /findus/, /cateringwholesale/, /suppliers/)
so existing Google rankings and shared links carry over.
"""
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
SITE = "https://bayithospitality.co.uk"

PAGES = [
    # (source, output, url path, nav key, title, description)
    ("home.html", "index.html", "/", "home",
     "Bāyit Bagels - Fresh bagels baked daily in Brighton's Open Market",
     "Bagels made over three days with stone-milled organic flour, filled with Sussex produce. "
     "Unit 26, Brighton Open Market. Open Tue-Sun 10-5. Catering, wholesale and pre-orders."),
    ("menu.html", "menu/index.html", "/menu/", "menu",
     "Menu - Bāyit Bagels, Brighton",
     "Salmon & schmear, salt beef, vegan Tzimmes and more. Our full bagel menu with prices, "
     "vegan options and allergen information."),
    ("catering.html", "cateringwholesale/index.html", "/cateringwholesale/", "catering",
     "Catering, wholesale & pre-orders - Bāyit Bagels, Brighton",
     "Office lunches, party platters, weddings and festive catering in Brighton. Wholesale bagels "
     "for cafés. Order with 3 days' notice."),
    ("suppliers.html", "suppliers/index.html", "/suppliers/", "suppliers",
     "Our suppliers - Bāyit Bagels, Brighton",
     "Curing Rebels, Gilchesters Organics, Hodmedod's, Shrub, Infinity Foods, Sussex Surplus, "
     "our Hollingdean allotment and weekly foraging."),
    ("findus.html", "findus/index.html", "/findus/", "findus",
     "Find us - Bāyit Bagels, Unit 26 Brighton Open Market",
     "Unit 26, The Open Market, Brighton BN1 4JU. Open Tuesday to Sunday 10am-5pm. "
     "Wheelchair accessible, dogs always welcome."),
    ("404.html", "404.html", "/404", None,
     "Page not found - Bāyit Bagels",
     "This page has gone the way of Saturday's last bagel."),
]

NAV = [("menu", "/menu/", "Menu"), ("catering", "/cateringwholesale/", "Catering & wholesale"),
       ("suppliers", "/suppliers/", "Our suppliers"), ("findus", "/findus/", "Find us")]

SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Bakery",
  "@id": "https://bayithospitality.co.uk/#bakery",
  "name": "Bāyit Bagels",
  "alternateName": "Bayit Hospitality",
  "url": "https://bayithospitality.co.uk/",
  "logo": "https://bayithospitality.co.uk/assets/img/favicon.png",
  "image": "https://bayithospitality.co.uk/assets/img/og-image.jpg",
  "description": "Bagel bakery in Brighton's Open Market. Bagels made over three days and filled with local, ethically sourced produce. Catering, wholesale and pre-orders.",
  "email": "oli.itkin@bayithospitality.co.uk",
  "servesCuisine": ["Bagels", "Jewish deli", "Bakery"],
  "priceRange": "£2-£12",
  "hasMenu": "https://bayithospitality.co.uk/menu/",
  "acceptsReservations": false,
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Unit 26, The Open Market, Marshalls Row",
    "addressLocality": "Brighton",
    "postalCode": "BN1 4JU",
    "addressCountry": "GB"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 50.8315474, "longitude": -0.1347281 },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "opens": "10:00", "closes": "17:00"
  }],
  "sameAs": ["https://www.instagram.com/bayit_bagels/"]
}
</script>"""


def header(active: str | None) -> str:
    links = "\n".join(
        f'        <a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a>'
        for key, href, label in NAV
    )
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Bāyit Bagels home">
      <img src="/assets/img/wordmark.svg" alt="Bāyit" width="128" height="72">
      <span class="brand-meta">
        <span class="open-status" data-open-status>Open 10-5pm</span><br>
        Tues-Sun
      </span>
    </a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="site-nav" aria-label="Main">
{links}
        <a class="btn btn--solid" href="/cateringwholesale/#enquire">Order catering <span class="arrow" aria-hidden="true">→</span></a>
        <p class="mobile-meta mono"><span class="open-status" data-open-status>Open 10-5pm</span><br>Unit 26, The Open Market, Brighton BN1 4JU</p>
    </nav>
  </div>
</header>
<div class="ticker" aria-hidden="true">
  <div class="ticker-track">
    {"".join("<span>" + s + "</span>" for s in TICKER * 2)}
  </div>
</div>"""


TICKER = ["Open 10-5pm", "Tues-Sun", "Fresh bagels baked daily", "Festive catering now booking",
          "Unit 26, Brighton Open Market", "Dogs always welcome"]

FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="/assets/img/wordmark.svg" alt="Bāyit" width="320" height="180" loading="lazy">
        <p class="mono" style="margin-top:20px">To us, hospitality means home.</p>
      </div>
      <div>
        <h2 class="mono">Visit</h2>
        <ul>
          <li><a href="https://www.google.com/maps/place/Bayit/@50.8315474,-0.1373084,17z/data=!3m1!4b1!4m6!3m5!1s0x48758500234355b3:0xc95901298066fd1e!8m2!3d50.8315474!4d-0.1347281!16s%2Fg%2F11m5m6hhw3" target="_blank" rel="noopener">Unit 26, The Open Market<br>Brighton, BN1 4JU</a></li>
          <li style="margin-top:8px">Tues-Sun, 10am-5pm</li>
          <li class="soft">Closed Mondays</li>
        </ul>
      </div>
      <div>
        <h2 class="mono">Explore</h2>
        <ul>
          <li><a href="/menu/">Menu</a></li>
          <li><a href="/cateringwholesale/">Catering & wholesale</a></li>
          <li><a href="/suppliers/">Our suppliers</a></li>
          <li><a href="/findus/">Find us</a></li>
        </ul>
      </div>
      <div>
        <h2 class="mono">Say hello</h2>
        <ul>
          <li><a href="mailto:oli.itkin@bayithospitality.co.uk">oli.itkin@<br>bayithospitality.co.uk</a></li>
          <li style="margin-top:8px"><a href="https://www.instagram.com/bayit_bagels/" target="_blank" rel="noopener">Instagram @bayit_bagels</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-base">
      <span>© <span data-year>2026</span> Bayit Hospitality</span>
      <span>Brand &amp; illustration by <a href="http://louisthings.com/" target="_blank" rel="noopener">louisthings</a></span>
    </div>
  </div>
  <svg class="swoop" viewBox="0 0 1600 300" preserveAspectRatio="none" aria-hidden="true">
    <path d="M-20 120 C 300 10, 640 10, 880 80 S 1380 140, 1640 20"/>
  </svg>
</footer>
<script src="/assets/js/main.js" defer></script>"""


def page(src, out, path, active, title, desc):
    body = (SRC / "pages" / src).read_text(encoding="utf-8")
    url = SITE + path
    noindex = '\n<meta name="robots" content="noindex">' if src == "404.html" else ""
    html = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">{noindex}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#FFF5F0">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bāyit Bagels">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400&family=Inter:wght@300;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/styles.css">
{SCHEMA}
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
"""
    target = OUT / out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    print("built", out)


def sitemap():
    urls = "\n".join(
        f"  <url><loc>{SITE}{p[2]}</loc></url>" for p in PAGES if p[0] != "404.html"
    )
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    for p in PAGES:
        page(*p)
    sitemap()

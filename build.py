#!/usr/bin/env python3
"""Builds the Verse Anywhere website.

i18n/<lang>.json  ->  <lang>/index.html, <lang>/privacy.html, <lang>/support.html, index.html, sitemap.xml

Run:  python3 build.py   (then `python3 -m http.server` to look at it)
The folder is the website: it can be served as is (GitHub Pages, like PawShelf). No external requests.
"""
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent

# Set these before publishing.
SITE_URL = "https://archivelab-kr.github.io/verseanywhere"  # same GitHub Pages account as PawShelf
SUPPORT_EMAIL = "archivelabapps@gmail.com"                   # the support address PawShelf's site uses
APP_STORE_URL = ""                                           # empty shows "Coming soon"

LANGS = [("en", "en"), ("ko", "ko")]  # (code for <html lang>/hreflang, folder)
PAGES = ["index.html", "privacy.html", "support.html"]

ICONS = {  # 24px line icons, drawn here (decorative, aria-hidden)
    "copy": '<rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h2"/>',
    "mark": '<path d="M4 20h6l10-10-6-6L4 14z"/><path d="M13 5l6 6"/>',
    "listen": '<path d="M4 10v4h4l5 4V6L8 10z"/><path d="M16.5 8.5a5 5 0 0 1 0 7"/><path d="M19 6a8.5 8.5 0 0 1 0 12"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "refs": '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M7 6h10M6 8l5 8M18 8l-5 8"/>',
    "theme": '<path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1-9-9z"/>',
    "keys": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 10h.01M11 10h.01M15 10h.01M7 14h10"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>')


def esc(s):
    out = html.escape(s, quote=False)
    return out.replace("{email}", f'<a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>')


def attr(s):
    return html.escape(s, quote=True)


def url(slug, page):
    return f"{SITE_URL}/{slug}/" + ("" if page == "index.html" else page)


def shot(slug, name):
    """A language's own screenshot when there is one, else the other language's."""
    for s in (slug, "ko", "en"):
        p = f"assets/shots/{name}-{s}.jpg"
        if (ROOT / p).exists():
            return "../" + p
    sys.exit(f"missing screenshot {name}")


def head(code, slug, page, title, desc, extra=""):
    alts = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{url(s, page)}">' for c, s in LANGS)
    return f"""<!doctype html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{attr(title)}</title>
<meta name="description" content="{attr(desc)}">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{url(slug, page)}">
{alts}
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Verse Anywhere">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(desc)}">
<meta property="og:url" content="{url(slug, page)}">
<meta property="og:image" content="{SITE_URL}/assets/icon-1024.png">
<link rel="icon" type="image/png" href="../assets/favicon.png">
<link rel="apple-touch-icon" href="../assets/icon-256.png">
<link rel="stylesheet" href="../assets/style.css">
<script src="../assets/site.js" defer></script>{extra}
</head>
<body>"""


def jsonld(t, code, slug):
    data = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Verse Anywhere",
            "description": t["description"], "operatingSystem": "macOS 14, iOS 17, iPadOS 17",
            "applicationCategory": "ReferenceApplication", "inLanguage": code, "url": url(slug, "index.html"),
            "image": f"{SITE_URL}/assets/icon-1024.png", "screenshot": f"{SITE_URL}/{shot(slug, 'reader')[3:]}",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "publisher": {"@type": "Organization", "name": "ArchiveLab"}}
    if APP_STORE_URL:
        data["downloadUrl"] = APP_STORE_URL
    return '\n<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def header(t, page):
    opts = "".join(f'<option value="../{s}/{page}"{" selected" if s == t["_slug"] else ""}>{esc(all_t[s]["lang_name"])}</option>'
                   for _, s in LANGS)
    home = "./" if page == "index.html" else "./index.html"
    return f"""
<header class="top">
  <div class="top-in">
    <a class="brand" href="./"><img src="../assets/icon-256.png" alt="" width="32" height="32">Verse Anywhere</a>
    <nav class="top-nav" aria-label="{attr(t["nav_home"])}">
      <a href="{home}#features">{esc(t["nav_features"])}</a>
      <a href="{home}#pricing">{esc(t["nav_pricing"])}</a>
      <a href="support.html">{esc(t["nav_support"])}</a>
      <label class="lang">{icon("globe", "ico sm")}<span class="sr">{esc(t["language"])}</span><select>{opts}</select></label>
    </nav>
  </div>
</header>"""


def footer(t, page):
    langs = "".join(f'<li><a href="../{s}/{page}" hreflang="{c}" lang="{c}">{esc(all_t[s]["lang_name"])}</a></li>' for c, s in LANGS)
    return f"""
<footer class="foot">
  <div class="foot-in">
    <p class="foot-brand"><img src="../assets/icon-256.png" alt="" width="24" height="24">Verse Anywhere</p>
    <ul class="foot-links">
      <li><a href="./">{esc(t["nav_home"])}</a></li>
      <li><a href="support.html">{esc(t["nav_support"])}</a></li>
      <li><a href="privacy.html">{esc(t["nav_privacy"])}</a></li>
    </ul>
    <ul class="foot-langs" aria-label="{attr(t["language"])}">{langs}</ul>
    <p class="foot-copy">{esc(t["foot_copy"])}</p>
  </div>
</footer>
</body>
</html>
"""


def cta(t):
    if APP_STORE_URL:
        return f'<a class="cta" href="{attr(APP_STORE_URL)}">{esc(t["cta_download"])}</a>'
    return f'<p class="cta is-soon">{esc(t["cta_soon"])}</p>'


def home(t):
    slug = t["_slug"]
    steps = "".join(f'<li><figure><img src="{shot(slug, s)}" alt="" width="1440" height="900" loading="lazy"></figure>'
                    f"<h3>{esc(h)}</h3><p>{esc(p)}</p></li>" for h, p, s in t["steps"])
    feats = "".join(f'<li>{icon(k)}<h3>{esc(h)}</h3><p>{esc(p)}</p></li>' for k, h, p in t["features"])
    free = "".join(f"<li>{icon('check', 'ico sm')}{esc(x)}</li>" for x in t["free_items"])
    pro = "".join(f"<li>{icon('check', 'ico sm')}{esc(x)}</li>" for x in t["pro_items"])
    texts = "".join(f"<li>{esc(x)}</li>" for x in t["texts"])
    return f"""
<main>
<section class="hero">
  <div class="hero-in">
    <div class="hero-copy">
      <p class="kicker">{esc(t["hero_kicker"])}</p>
      <h1>{esc(t["hero_h1"]).replace(chr(10), "<br>")}</h1>
      <p class="lead">{esc(t["hero_p"])}</p>
      {cta(t)}
      <p class="note">{esc(t["hero_note"])}</p>
      <p class="req">{esc(t["requirements"])}</p>
    </div>
    <div class="hero-art">
      <img class="mac" src="{shot(slug, 'reader-dark')}" alt="" width="1440" height="900">
      <img class="phone" src="{shot(slug, 'iphone-marks')}" alt="" width="640" height="1390">
    </div>
  </div>
</section>

<section class="how" id="how">
  <h2>{esc(t["how_h2"])}</h2>
  <ol class="steps">{steps}</ol>
</section>

<section class="features" id="features">
  <h2>{esc(t["features_h2"])}</h2>
  <ul class="feature-grid">{feats}</ul>
</section>

<section class="devices">
  <div class="devices-in">
    <div class="devices-copy">
      <h2>{esc(t["devices_h2"])}</h2>
      <p>{esc(t["devices_p"])}</p>
      <p class="note">{esc(t["devices_note"])}</p>
    </div>
    <div class="devices-art">
      <img class="pad" src="{shot(slug, 'ipad-parallel')}" alt="" width="1200" height="1600" loading="lazy">
      <img class="phone" src="{shot(slug, 'iphone-notes')}" alt="" width="640" height="1390" loading="lazy">
    </div>
  </div>
</section>

<section class="pricing" id="pricing">
  <h2>{esc(t["pricing_h2"])}</h2>
  <div class="plans">
    <div class="plan"><h3>{esc(t["free_h3"])}</h3><p class="price">{esc(t["free_price"])}</p><ul>{free}</ul></div>
    <div class="plan pro"><h3>{esc(t["pro_h3"])}</h3><p class="price">{esc(t["pro_price"])}</p><ul>{pro}</ul></div>
  </div>
  <p class="note center">{esc(t["pricing_note"])}</p>
</section>

<section class="texts">
  <h2>{esc(t["texts_h2"])}</h2>
  <ul class="text-list">{texts}</ul>
  <p class="note center">{esc(t["texts_note"])}</p>
</section>

<section class="promise">
  <div class="promise-in">
    {icon("lock", "ico lg")}
    <h2>{esc(t["promise_h2"])}</h2>
    <p>{esc(t["promise_p"])}</p>
    <p><a href="privacy.html">{esc(t["promise_link"])}</a></p>
  </div>
</section>
</main>"""


def privacy(t):
    p = t["privacy"]
    body = "".join(f"<h2>{esc(h)}</h2>" + "".join(f"<p>{esc(x)}</p>" for x in paras) for h, paras in p["sections"])
    return f"""
<main class="doc">
  <h1>{esc(p["title"])}</h1>
  <p class="updated">{esc(p["updated"])}</p>
  <p class="lead">{esc(p["intro"])}</p>
  {body}
  <p class="note">{esc(p["note"])}</p>
</main>"""


def support(t):
    s = t["support"]
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in s["faq"])
    return f"""
<main class="doc">
  <h1>{esc(s["title"])}</h1>
  <p class="lead">{esc(s["intro"])}</p>
  <h2>{esc(s["faq_h2"])}</h2>
  <div class="faq">{faq}</div>
</main>"""


def root_index():
    alts = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{url(s, "index.html")}">' for c, s in LANGS)
    links = "".join(f'<li><a href="{s}/" lang="{c}">{esc(all_t[s]["lang_name"])}</a></li>' for c, s in LANGS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verse Anywhere</title>
<meta name="description" content="{attr(all_t["en"]["description"])}">
{alts}
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
<link rel="icon" type="image/png" href="assets/favicon.png">
<script>
(function () {{
  var langs = (navigator.languages || [navigator.language || "en"]);
  for (var i = 0; i < langs.length; i++) {{ if (langs[i].toLowerCase().indexOf("ko") === 0) {{ location.replace("ko/"); return; }} }}
  location.replace("en/");
}})();
</script>
<noscript><meta http-equiv="refresh" content="0; url=en/"></noscript>
</head>
<body>
<ul>{links}</ul>
</body>
</html>
"""


def check_keys(ref, other, lang, path=""):
    """Every language must have the same keys and list lengths as English."""
    if isinstance(ref, dict):
        for k in ref:
            if k not in other:
                sys.exit(f"{lang}: missing {path}{k}")
            check_keys(ref[k], other[k], lang, f"{path}{k}.")
    elif isinstance(ref, list):
        if not isinstance(other, list) or len(ref) != len(other):
            sys.exit(f"{lang}: {path[:-1]} should have {len(ref)} entries")
        for i, (a, b) in enumerate(zip(ref, other)):
            check_keys(a, b, lang, f"{path}{i}.")


all_t = {}
for code, slug in LANGS:
    all_t[slug] = json.loads((ROOT / "i18n" / f"{slug}.json").read_text(encoding="utf-8"))
    all_t[slug]["_slug"] = slug
    if slug != "en":
        check_keys(all_t["en"], all_t[slug], slug)

for code, slug in LANGS:
    t = all_t[slug]
    out = ROOT / slug
    out.mkdir(exist_ok=True)
    pages = {
        "index.html": (t["title"], t["description"], header(t, "index.html") + home(t)),
        "privacy.html": (f'{t["privacy"]["title"]} | Verse Anywhere', t["privacy"]["intro"], header(t, "privacy.html") + privacy(t)),
        "support.html": (f'{t["support"]["title"]} | Verse Anywhere', t["support"]["intro"].replace("{email}", SUPPORT_EMAIL),
                         header(t, "support.html") + support(t)),
    }
    for page, (title, desc, body) in pages.items():
        extra = jsonld(t, code, slug) if page == "index.html" else ""
        (out / page).write_text(head(code, slug, page, title, desc, extra) + body + footer(t, page), encoding="utf-8")

(ROOT / "index.html").write_text(root_index(), encoding="utf-8")
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{url(s, p)}</loc></url>\n" for _, s in LANGS for p in PAGES) + "</urlset>\n", encoding="utf-8")
print(f"Built {len(LANGS)} languages x {len(PAGES)} pages + index.html + sitemap.xml")
if not APP_STORE_URL:
    print("note: APP_STORE_URL is empty, pages show 'coming soon'")

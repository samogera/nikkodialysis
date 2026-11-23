#!/usr/bin/env python3
"""Builds the static Nikko Dialysis Center website.

Edit CONFIG below (phone, address, domain, etc.), then run:
    python3 scripts/build.py
Every HTML page, sitemap.xml, robots.txt, llms.txt and assets/js/config.js is regenerated.
"""
import json, os, datetime, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# CONFIG — replace every [PLACEHOLDER] before launch
# ---------------------------------------------------------------------------
CONFIG = {
    "url": "https://nikkodialysis.vercel.app",   # final domain, no trailing slash
    "name": "Nikko Dialysis Center",
    "phone_display": "[+254 PHONE]",
    "phone_tel": "+254000000000",
    "whatsapp_display": "[+254 WHATSAPP]",
    "whatsapp_number": "254000000000",           # digits only, for wa.me
    "email": "info@example.com",
    "street": "[STREET ADDRESS]",
    "area": "[AREA]",
    "postcode": "[POSTCODE]",
    "lat": "", "lng": "",                          # e.g. "-1.2921", "36.8219"
    "hours_weekdays": "[06:00–20:00]",
    "hours_saturday": "[06:00–16:00]",
    "hours_sunday": "[Closed]",
    "shift_morning": "[06:00–10:00]",
    "shift_midday": "[11:00–15:00]",
    "shift_evening": "[16:00–20:00]",
    "mpesa_paybill": "[PAYBILL]",
    "airtel_till": "[TILL]",
    "price_per_session": "[KES PRICE]",
    "kmpdc_licence": "[NO.]",
    "sha_code": "[CODE]",
    "odpc_reg": "[NO.]",
    "nck_reg": "[NO.]",
    "nema_licence": "[NO.]",
    "maps_url": "",                                # Google Maps share link
    "maps_embed": "",                              # Google Maps embed src
    "facebook": "", "instagram": "", "linkedin": "", "google_business": "",
    "plausible_domain": "",                        # e.g. "nikkodialysis.co.ke" to enable analytics
    "sentry_loader": "",                           # Sentry JS loader URL to enable error tracking
    "last_updated": datetime.date.today().isoformat(),
}
C = CONFIG
WA = f"https://wa.me/{C['whatsapp_number']}?text=" + "Hello%20Nikko%20Dialysis%20Center%2C%20I%27d%20like%20to%20ask%20about%20dialysis."
ADDR = f"{C['street']}, {C['area']}, Nairobi"

INSURERS = [("SHA", "sha"), ("Jubilee Insurance", "jubilee"), ("AAR Insurance", "aar"), ("Britam", "britam"),
            ("CIC Insurance", "cic"), ("APA Insurance", "apa"), ("Madison Insurance", "madison"), ("Old Mutual", "oldmutual"),
            ("ICEA LION", "icealion"), ("Sanlam Allianz", "sanlam-allianz"), ("GA Insurance", "ga"), ("First Assurance", "first-assurance")]
IMG_SIZE = {"sha": (248, 168), "jubilee": (376, 200), "aar": (165, 200), "britam": (397, 150), "cic": (249, 200), "apa": (298, 200),
            "madison": (178, 59), "oldmutual": (440, 126), "icealion": (289, 199), "sanlam-allianz": (381, 73), "ga": (440, 144),
            "first-assurance": (352, 81), "mpesa": (440, 183), "airtel-money": (413, 200)}

# ---------------------------------------------------------------------------
# Icons (Lucide-style strokes)
# ---------------------------------------------------------------------------
P = {
    "arrow": '<path d="M7 17 17 7M8 7h9v9"/>',
    "right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "left": '<path d="M19 12H5M11 18l-6-6 6-6"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-12.6 7.3L3 21l2.3-5.2A8.4 8.4 0 1 1 21 11.5z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m22 7-10 6L2 7"/>',
    "pin": '<path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "check": '<path d="m5 12 5 5L20 7"/>',
    "drop": '<path d="M12 2.7S6 9 6 14a6 6 0 0 0 12 0c0-5-6-11.3-6-11.3z"/>',
    "swap": '<path d="M7 7h13l-4-4M17 17H4l4 4"/>',
    "home": '<path d="M3 21h18M5 21V10l7-6 7 6v11M10 21v-6h4v6"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "leaf": '<path d="M20 3C10 3 4 9 4 17c0 1.4.2 2.7.5 4 1-5 5-9.5 10.5-11-4 2.3-7 6-8 10.6C16.5 20 21 13 20 3z"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "alert": '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    "bank": '<path d="M3 10 12 4l9 6"/><path d="M4 10h16M6 10v8M10 10v8M14 10v8M18 10v8M3 20h18"/>',
    "cash": '<rect x="2" y="7" width="20" height="12" rx="2"/><circle cx="12" cy="13" r="2.5"/><path d="M6 13h.01M18 13h.01M5 4h14"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "fb": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "ig": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
    "in": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/>',
}
def ic(n, w=1.75):
    return f'<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{P[n]}</svg>'

def e(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------------------
# Page metadata
# ---------------------------------------------------------------------------
PAGES = {
    "index": ("/", "Home", "Dialysis Centre in Nairobi | Nikko Dialysis Center",
              f"Safe, on-time haemodialysis in {C['area']}, Nairobi. Morning, midday and evening shifts, holiday dialysis, SHA and major insurers accepted. Book a consultation."),
    "services": ("/services", "Services", "Haemodialysis & Holiday Dialysis in Nairobi | Nikko",
                 "Haemodialysis, holiday dialysis for visitors, vascular access care, kidney diet education and specialist reviews, all in one Nairobi unit."),
    "about": ("/about", "About", "About Us | Nikko Dialysis Center, Nairobi",
              "The team, unit and standards behind Nikko Dialysis Center: nephrologist-reviewed care, renal nurses and strict infection control in Nairobi."),
    "patients": ("/patients", "Patients & families", "Dialysis Patient Guide & FAQs | Nikko Dialysis Center",
                 "What to bring to your first dialysis session, habits for life between sessions, support for families and answers to common questions."),
    "insurance": ("/insurance", "Insurance", "Dialysis Insurance & SHA Cover in Kenya | Nikko Dialysis",
                  "We accept SHA and major insurers including Jubilee, AAR, Britam, CIC and APA. Pay balances by M-Pesa, Airtel Money, bank transfer or cash."),
    "contact": ("/contact", "Contact", "Book Dialysis in Nairobi | Contact Nikko Dialysis Center",
                f"Book a consultation, transfer or holiday dialysis in two quick steps. Call {C['phone_display']} or WhatsApp us. A nurse calls you back."),
    "privacy": ("/privacy", "Privacy & terms", "Privacy Policy & Terms | Nikko Dialysis Center",
                "How Nikko Dialysis Center protects your data under Kenya's Data Protection Act 2019, your rights, cookies and terms of use."),
    "404": ("/404", "Page not found", "Page not found | Nikko Dialysis Center", "The page you were looking for has moved or doesn't exist."),
}
NAV = [("index", "Home"), ("services", "Services"), ("about", "About"), ("patients", "Patients & families"), ("insurance", "Insurance")]
def href(k):
    return PAGES[k][0]

FAQS = [
    ("Treatment", "How often will I need dialysis?", "Most people need haemodialysis three times a week, for about four hours each time. Your nephrologist sets the exact plan based on your blood results and how you feel."),
    ("Treatment", "Does dialysis hurt?", "Inserting the needles can sting briefly. Most people feel fine during treatment; some feel tired afterwards. Tell your nurse about cramps or dizziness and they will adjust your session."),
    ("Treatment", "Can I eat during my session?", "A light snack is usually fine. Ask your nurse first, as eating can lower blood pressure for some people."),
    ("Scheduling", "Can I keep working while on dialysis?", "Many patients do. Choose the morning, midday or evening shift that fits around your job and keep the same chair and time every week."),
    ("Scheduling", "What if I miss a session?", "Call us as soon as you can. Missing treatment lets fluid and waste build up, so we will try to fit you in the same or next day."),
    ("Scheduling", "Can I dialyse with you while visiting Nairobi?", "Yes. Ask your home unit to send your prescription and recent blood results at least two weeks before you travel, and we will reserve your sessions."),
    ("Payment", "Do you accept SHA and private insurance?", "Yes. Bring your SHA number and insurance card to your consultation and we confirm your cover and handle pre-authorisation before you start."),
    ("Payment", "How can I pay a balance?", "By M-Pesa, Airtel Money, bank transfer or cash. You get a receipt for every session."),
    ("Families", "Can someone stay with me during treatment?", "One companion is welcome for your first sessions. After that it depends on space in the unit."),
    ("Families", "Can I get a kidney transplant?", "Many people on dialysis can be assessed. Your nephrologist will discuss it with you and refer you to a transplant team when appropriate."),
]

# ---------------------------------------------------------------------------
# Shared chrome
# ---------------------------------------------------------------------------
def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"

def clinic_schema():
    o = {"@context": "https://schema.org", "@type": ["MedicalClinic", "MedicalBusiness"], "@id": C["url"] + "/#clinic",
         "name": C["name"], "alternateName": "Nikko Dialysis Centre", "slogan": "Life. Hope. Better Tomorrow.",
         "description": "Outpatient haemodialysis centre in Nairobi, Kenya offering haemodialysis, holiday dialysis for visitors, vascular access care and kidney diet education. Accepts SHA and major Kenyan medical insurers.",
         "url": C["url"] + "/", "logo": C["url"] + "/logo.png", "image": C["url"] + "/og-image.jpg",
         "telephone": C["phone_tel"], "email": C["email"],
         "address": {"@type": "PostalAddress", "streetAddress": C["street"], "addressLocality": "Nairobi", "addressRegion": "Nairobi County", "postalCode": C["postcode"], "addressCountry": "KE"},
         "areaServed": [{"@type": "City", "name": "Nairobi"}, {"@type": "Country", "name": "Kenya"}],
         "medicalSpecialty": "Renal", "isAcceptingNewPatients": True,
         "availableService": [{"@type": "MedicalTherapy", "name": n} for n in ["Haemodialysis", "Holiday dialysis for visiting patients", "Vascular access care", "Kidney diet and nutrition education"]],
         "paymentAccepted": "Cash, M-Pesa, Airtel Money, Bank transfer, Health insurance", "currenciesAccepted": "KES"}
    if C["lat"] and C["lng"]:
        o["geo"] = {"@type": "GeoCoordinates", "latitude": C["lat"], "longitude": C["lng"]}
    if C["maps_url"]:
        o["hasMap"] = C["maps_url"]
    same = [C[k] for k in ("google_business", "facebook", "instagram", "linkedin") if C[k]]
    if same:
        o["sameAs"] = same
    return o

def head(key, extra=""):
    path, name, title, desc = PAGES[key]
    url = C["url"] + (path if path != "/" else "/")
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": C["url"] + "/"}]
    if key not in ("index", "404"):
        crumbs.append({"@type": "ListItem", "position": 2, "name": name, "item": url})
    robots = '<meta name="robots" content="noindex, follow">' if key == "404" else '<meta name="robots" content="index, follow, max-image-preview:large">'
    canonical = "" if key == "404" else f'<link rel="canonical" href="{url}">'
    ld = jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}) if key != "404" else ""
    if key == "index":
        ld += jsonld(clinic_schema()) + jsonld({"@context": "https://schema.org", "@type": "WebSite", "name": C["name"], "url": C["url"] + "/", "inLanguage": "en-KE"})
    return f'''<!doctype html>
<html lang="en-KE" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
{canonical}
<meta name="theme-color" content="#0B2F87">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">
<link rel="icon" href="/favicon-16x16.png" type="image/png" sizes="16x16">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{C['name']}">
<meta property="og:locale" content="en_KE">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{C['url']}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Nikko Dialysis Center: Dialysis that fits your life.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{C['url']}/og-image.jpg">
<meta name="geo.region" content="KE-110">
<meta name="geo.placename" content="Nairobi">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/styles.css?v={VERSION}">
{extra}
<script src="/assets/js/config.js?v={VERSION}" defer></script>
<script src="/assets/js/main.js?v={VERSION}" defer></script>
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(key):
    links = "".join(f'<a href="{href(k)}"{" aria-current=\"page\"" if k == key else ""}>{t}</a>' for k, t in NAV)
    mlinks = "".join(f'<a href="{href(k)}">{t}</a>' for k, t in NAV + [("contact", "Contact")])
    return f'''<div class="topbar"><div class="wrap">
<span><i class="dot" aria-hidden="true"></i>SHA &amp; major insurers accepted · Mon–Sat</span>
<span class="hide-sm">Questions? Call <a href="tel:{C['phone_tel']}">{C['phone_display']}</a></span>
</div></div>
<header class="nav">
<div class="wrap nav-inner">
<a class="brand" href="/" aria-label="{C['name']} home"><img src="/assets/img/logo.webp" alt="{C['name']}" width="141" height="44" fetchpriority="high"></a>
<nav class="nav-links" aria-label="Main">{links}</nav>
<div class="nav-actions">
<a class="btn btn-line desk" href="tel:{C['phone_tel']}">Call us</a>
<a class="btn btn-dark desk" href="/contact">Book a consultation {ic("arrow", 2)}</a>
<button class="btn btn-line menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
</div>
</div>
<nav id="mobile-menu" class="mobile-menu" aria-label="Mobile">{mlinks}<a class="btn btn-dark" href="/contact">Book a consultation</a></nav>
</header>
<main id="main">
'''

ECG = "M0 36H500l10-4 8 4h20l12-30 14 62 16-70 12 50 10-12h16l8-6 10 6H1200"
CUT = "M0 30H520l10-4 8 4h18l12-22 14 46 16-52 12 36 10-8h14l8-4 10 4H1200"

def footer():
    return f'''</main>
<footer class="footer">
<div class="wrap fwrap">
<div class="ftop">
<div class="fbrand"><img src="/assets/img/logo-white.webp" alt="{C['name']}" width="141" height="44" loading="lazy"><p>Haemodialysis &amp; holiday dialysis in {C['area']}, Nairobi.</p></div>
<div class="fcta"><p>Need dialysis in Nairobi?</p><div class="row"><a class="btn btn-white btn-sm" href="/contact">Book a consultation</a><a class="btn btn-ghost-dark btn-sm" href="tel:{C['phone_tel']}">Call us</a></div></div>
</div>
<div class="fgrid">
<nav class="fcol" aria-label="Footer"><p class="h">Explore</p><a href="/services">Services</a><a href="/about">About</a><a href="/patients">Patients &amp; families</a><a href="/insurance">Insurance</a></nav>
<div class="fcol"><p class="h">Contact</p><a href="tel:{C['phone_tel']}">{C['phone_display']}</a><a href="{WA}" rel="noopener" target="_blank">WhatsApp</a><a href="mailto:{C['email']}">{C['email']}</a></div>
<div class="fcol fvisit"><p class="h">Visit</p><address>{C['street']}, {C['area']}, Nairobi</address><span>Mon–Fri {C['hours_weekdays']} · Sat {C['hours_saturday']}</span></div>
</div>
<div class="legalbar">
<p>Licence {C['kmpdc_licence']} · SHA code {C['sha_code']} · General information only, not medical advice. In an emergency go to the nearest emergency department or call 999 / 112.</p>
<div class="row-between"><span>© <span data-year>2026</span> {C['name']}</span><span class="links"><a href="/privacy">Privacy</a><a href="/privacy#terms">Terms</a><a href="/privacy#cookies" data-cookie-settings>Cookies</a><a href="/privacy#accessibility">Accessibility</a></span></div>
</div>
</div>
<div class="fanim" aria-hidden="true">
<div class="split-word">
<span class="w top">Dialysis <b>Center</b></span>
<span class="w bot">Dialysis <b>Center</b></span>
<div class="cut"><svg viewBox="0 0 1200 60" preserveAspectRatio="none"><path d="{CUT}" pathLength="1600"/></svg></div>
</div>
</div>
</footer>
<nav class="actionbar" aria-label="Quick actions">
<a href="tel:{C['phone_tel']}">{ic("phone")}Call</a>
<a href="{WA}" rel="noopener" target="_blank">{ic("chat")}WhatsApp</a>
<a class="main" href="/contact">Book now</a>
</nav>
<div class="cookie" id="cookie" role="region" aria-label="Cookie notice" hidden>
<p>We use essential cookies to run this site and, with your consent, privacy-friendly analytics to improve it. <a href="/privacy#cookies">Cookie policy</a>.</p>
<div class="row"><button class="btn btn-dark btn-sm" type="button" data-consent="all">Accept all</button><button class="btn btn-line btn-sm" type="button" data-consent="essential">Essential only</button></div>
</div>
</body>
</html>
'''

def page(key, body, extra_head=""):
    return head(key, extra_head) + header(key) + body + footer()

def logo_img(slug, name, cls="", lazy=True):
    w, h = IMG_SIZE[slug]
    return f'<img src="/assets/img/partners/{slug}.webp" alt="{e(name)}" width="{w}" height="{h}"{" loading=\"lazy\" decoding=\"async\"" if lazy else ""}>'

def photo(n, alt, h, pos="50% 18%", eager=False, sizes="(max-width: 760px) 100vw, 50vw"):
    return (f'<img class="photo" src="/assets/img/unit-{n}-736.webp" srcset="/assets/img/unit-{n}-480.webp 480w, /assets/img/unit-{n}-736.webp 736w" '
            f'sizes="{sizes}" width="736" height="1308" alt="{e(alt)}" style="height:{h}px;object-position:{pos}"'
            + (' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"') + '>')

def faq_html(items, filter_id=None):
    out = []
    for c, q, a in items:
        out.append(f'<details data-cat="{c}"><summary>{e(q)}</summary><p>{e(a)}</p></details>')
    return f'<div class="faq"{f" id=\"{filter_id}\"" if filter_id else ""}>' + "".join(out) + "</div>"

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def home():
    tiles = "".join(f'<div class="logo-tile">{logo_img(s, n)}</div>' for n, s in INSURERS)
    services = [("01", "Haemodialysis", "Regular sessions, usually three a week, in a reclining chair with continuous monitoring.", "/services#hd"),
                ("02", "Holiday &amp; visiting dialysis", "In Nairobi for work, family or a safari? Stay on schedule, coordinated with your home unit.", "/services#holiday"),
                ("03", "Vascular access care", "Fistula and catheter checks every session, with quick referral if anything changes.", "/services#access"),
                ("04", "Kidney diet &amp; education", "Fluids, salt and potassium explained with everyday Kenyan meals, for you and your family.", "/services#diet")]
    rows = "".join(f'<a class="service-row" href="{h}"><span class="n">{n}</span><span class="t">{t}</span><span class="d">{d}</span><span class="circle">{ic("arrow", 2)}</span></a>' for n, t, d, h in services)
    feats = ["Continuous machine monitoring", "Treated water to clinical standard", "Strict infection control", "Reclining chairs, Wi-Fi and TV", "Emergency equipment on the floor"]
    steps = [("01", "Call or send a referral", "Your doctor's letter, or simply call us. We'll tell you what to bring."),
             ("02", "Consultation &amp; cover", "We review your history and labs, and confirm your SHA or insurance cover."),
             ("03", "Your fixed schedule", "Choose the shift that suits your work and family. Your chair is reserved."),
             ("04", "Ongoing care", "Routine bloods, regular specialist reviews and a team you can always ask.")]
    body = f'''<section class="hero">
<div class="wrap split center">
<div class="stack" style="gap:32px">
<span class="chip green" style="align-self:flex-start"><i class="dot" aria-hidden="true"></i>Accepting new patients &amp; visitors</span>
<h1 class="h1">Dialysis that fits <span class="accent">your life.</span></h1>
<p class="lead">Safe, on-time haemodialysis in a calm, modern unit in Nairobi, with a care team that knows you by name.</p>
<div class="row"><a class="btn btn-dark" href="/contact">Book a consultation {ic("arrow", 2)}</a><a class="btn btn-line" href="/services#holiday">Holiday dialysis</a></div>
<div class="stats"><div><strong>3 shifts</strong><span>Morning, midday, evening</span></div><div><strong>~4 hours</strong><span>Typical session</span></div><div><strong>Mon–Sat</strong><span>{C['hours_weekdays']}</span></div></div>
</div>
<div class="hero-media">
{photo(1, "Haemodialysis machine at Nikko Dialysis Center", 640, eager=True)}
<div class="hero-badge"><div class="who"><img src="/assets/img/mark.webp" alt="" width="44" height="44"><span><strong style="font-weight:600;display:block;font-size:15px">Life. Hope. Better Tomorrow.</strong><span class="small" style="font-size:13px">Care plans reviewed by a nephrologist</span></span></div><a class="link" href="/about">Inside the unit →</a></div>
</div>
</div>
</section>
<section style="padding:0 0 112px"><div class="wrap stack" style="gap:28px">
<div class="row-between"><p class="small" style="font-size:15px">Accepted by <strong style="color:var(--navy);font-weight:600">SHA</strong> and Kenya's major medical insurers</p><span class="small hide-sm">Pay by M-Pesa, Airtel Money, bank or cash</span></div>
<div class="logos">{tiles}<a class="logo-tile more" href="/insurance"><strong>+ many others</strong><span>Check your cover →</span></a></div>
</div></section>
<section class="section alt"><div class="wrap stack-lg">
<div class="split end"><div class="stack"><p class="eyebrow">Services</p><h2 class="h2">Everything around dialysis, <span class="accent">in one place.</span></h2></div><p class="lead max-sm">One team for your sessions, your access, your diet and your reviews, so you're never juggling clinics.</p></div>
<div class="service-list reveal">{rows}</div>
</div></section>
<section class="section"><div class="wrap stack-lg">
<p class="statement reveal">Four hours, three times a week. <span>So we designed every minute of it around safety first and your comfort right after.</span></p>
<div class="split" style="gap:20px">
{photo(2, "Dialyser and blood lines mounted on a machine", 460, "20% 6%")}
<div class="card deep reveal" style="justify-content:space-between;gap:28px"><p class="eyebrow">The unit</p><ul class="checks">{"".join(f"<li>{ic('check', 2.25)}{f}</li>" for f in feats)}</ul><a class="btn btn-white" href="/about" style="align-self:flex-start">Book a tour</a></div>
</div>
</div></section>
<section class="section tight-top"><div class="wrap stack-lg">
<div class="stack max-lg"><p class="eyebrow">Getting started</p><h2 class="h2">From first call to <span class="accent">first session.</span></h2></div>
<ol class="steps reveal">{"".join(f'<li><span class="n">{n}</span><strong class="h3">{t}</strong><span class="body">{d}</span></li>' for n, t, d in steps)}</ol>
<div class="banner blue reveal"><div class="stack max-md" style="gap:12px"><h2 class="h2 sm">Not sure where to start?</h2><p class="body">Tell us what you need in two quick steps. A nurse will call you back.</p></div><div class="row"><a class="btn btn-dark" href="/contact">Book a consultation {ic("arrow", 2)}</a><a class="btn btn-line" href="/patients#faq">Read the FAQs</a></div></div>
</div></section>
'''
    return page("index", body, '<link rel="preload" as="image" href="/assets/img/unit-1-736.webp" imagesrcset="/assets/img/unit-1-480.webp 480w, /assets/img/unit-1-736.webp 736w" imagesizes="(max-width: 760px) 100vw, 50vw">')

def services():
    stages = [("Arrive", "First 15 minutes", "Check-in and checks", "We weigh you, take your blood pressure and temperature, and ask how you have been since your last session."),
              ("Connect", "About 15 minutes", "Connecting to the machine", "Your nurse cleans and checks your access, then connects you while you settle into a reclining chair."),
              ("Treat", "About 4 hours", "Your blood is cleaned", "The machine filters your blood while nurses monitor you and the machine throughout. Read, rest, watch TV or work."),
              ("Home", "Last 20 minutes", "Disconnect and recover", "We disconnect you, check your access site and weigh you again, then confirm your next session.")]
    tabs = "".join(f'<button type="button" role="tab" id="tab-{i}" aria-controls="panel-{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{s[0]}</button>' for i, s in enumerate(stages))
    panels = "".join(f'<div class="panel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}"{"" if i == 0 else " hidden"}><span class="time">{s[1]}</span><strong class="h3">{s[2]}</strong><p class="body">{s[3]}</p></div>' for i, s in enumerate(stages))
    holiday = ["Referral letter and dialysis prescription from your nephrologist", "Recent blood results, including hepatitis B, C and HIV screening", "Your last three treatment records and current medicines", "Travel dates and how you will pay: insurance or self-pay"]
    others = [("access", "03 · Access care", "Your fistula is your lifeline.", "We check your fistula, graft or catheter every session, teach you how to protect it, and refer you quickly to a vascular surgeon if anything changes.", ["Fistula checks", "Catheter care", "Surgical referral"]),
              ("diet", "04 · Diet &amp; education", "Eat well, the Kenyan way.", "Fluid limits, salt, potassium and phosphate, explained with everyday meals like ugali, sukuma and githeri. Take-home guides for whoever cooks at home.", ["Fluid planning", "Meal guides", "Family sessions"]),
              ("reviews", "05 · Labs &amp; reviews", "A plan that keeps up with you.", "Routine blood tests and regular nephrologist reviews keep your prescription right. When you are ready, we coordinate transplant work-up referrals.", ["Monthly bloods", "Specialist reviews", "Transplant referral"])]
    orows = "".join(f'<div id="{i}" class="split reveal" style="padding:56px 0;border-bottom:1px solid var(--line);gap:24px 64px"><div class="stack" style="gap:14px"><p class="eyebrow">{n}</p><h2 class="h2 sm">{t}</h2></div><div class="stack"><p class="lead" style="font-size:18px">{d}</p><div class="row" style="gap:8px">{"".join(f"<span class=chip>{x}</span>" for x in tags)}</div></div></div>' for i, n, t, d, tags in others)
    body = f'''<section class="page-hero"><div class="wrap stack" style="gap:28px">
<p class="eyebrow">Services</p>
<h1 class="h1 max-lg">Kidney care, <span class="accent">all in one place.</span></h1>
<div class="row-between" style="align-items:flex-end;gap:32px"><p class="lead max-md">Your sessions, your access, your diet and your reviews, handled by one team that talks to each other.</p>
<nav class="row" style="gap:8px" aria-label="On this page"><a class="chip" href="#hd">Haemodialysis</a><a class="chip" href="#holiday">Holiday dialysis</a><a class="chip" href="#access">Access care</a><a class="chip" href="#diet">Diet</a><a class="chip" href="#reviews">Reviews</a></nav></div>
</div></section>
<section id="hd" class="section" style="padding-top:32px"><div class="wrap split">
{photo(2, "Dialyser mounted on a haemodialysis machine", 560, "50% 8%")}
<div class="stack" style="gap:28px">
<p class="eyebrow">01 · Haemodialysis</p>
<h2 class="h2">Cleaning your blood when your kidneys can't.</h2>
<p class="lead">A machine filters your blood through a dialyser, an artificial kidney, removing waste and extra fluid, then returns it to you. Most people come three times a week for about four hours.</p>
<div class="stack" style="gap:14px"><strong style="font-size:14px;font-weight:600">A session, step by step</strong><div class="seg" role="tablist" aria-label="Session stages">{tabs}</div>{panels}</div>
<div class="shifts"><div><span>Morning</span><strong>{C['shift_morning']}</strong></div><div><span>Midday</span><strong>{C['shift_midday']}</strong></div><div><span>Evening</span><strong>{C['shift_evening']}</strong></div></div>
</div>
</div></section>
<section id="holiday" class="section dark"><div class="wrap split">
<div class="stack" style="gap:24px"><p class="eyebrow">02 · Holiday &amp; visiting dialysis</p><h2 class="h2">Travel to Nairobi. <span class="accent">Don't miss a session.</span></h2><p class="lead">A family wedding, a business trip or a safari: we reserve your chairs and work directly with your home unit.</p><a class="btn btn-white" href="/contact" style="align-self:flex-start">Request holiday sessions</a></div>
<div class="stack" style="gap:0"><p class="small" style="color:var(--dark-muted);padding-bottom:16px;border-bottom:1px solid var(--dark-line)">Send us at least 2 weeks before travel</p><ul class="checks">{"".join(f"<li>{ic('check', 2.25)}{h}</li>" for h in holiday)}</ul></div>
</div></section>
<section class="section"><div class="wrap" style="border-top:1px solid var(--line)">{orows}</div></section>
<section class="section tight-top"><div class="wrap"><div class="banner green"><div class="stack max-md" style="gap:12px"><h2 class="h2 sm">Not sure which service you need?</h2><p class="body">Tell us where you are in your kidney journey and we'll guide you.</p></div><a class="btn btn-dark" href="/contact">Book a consultation {ic("arrow", 2)}</a></div></div></section>
'''
    return page("services", body)

def about():
    team = [("Nephrologists", "Kidney specialists who set and review your treatment plan."), ("Renal nurses", "With you through every session, from connection to going home."),
            ("Technicians", "Keep machines and water treatment checked and calibrated."), ("Nutrition &amp; support", "Diet guidance and practical help for families.")]
    glance = [("Type", "Outpatient haemodialysis centre"), ("Location", ADDR + ", Kenya"), ("Hours", f"Mon–Fri {C['hours_weekdays']} · Sat {C['hours_saturday']} · Sun {C['hours_sunday']}"),
              ("Services", "Haemodialysis, holiday dialysis, access care, kidney diet education"), ("Payment", "SHA, private insurance, M-Pesa, Airtel Money, bank transfer, cash"),
              ("Contact", f'<a href="tel:{C["phone_tel"]}">{C["phone_display"]}</a> · <a href="mailto:{C["email"]}">{C["email"]}</a>')]
    lic = [("KMPDC facility licence", C["kmpdc_licence"]), ("SHA facility code", C["sha_code"]), ("Nursing Council of Kenya", C["nck_reg"]), ("ODPC data controller", C["odpc_reg"]), ("NEMA medical waste licence", C["nema_licence"])]
    body = f'''<section class="page-hero"><div class="wrap stack" style="gap:28px">
<p class="eyebrow">About us</p><h1 class="h1 max-lg">Clinical precision, <span class="accent">delivered warmly.</span></h1>
<p class="lead max-md">People on dialysis spend more time with their care team than almost any other patients. We built Nikko so that time feels safe, calm and human.</p>
</div></section>
<section style="padding:0 0 128px"><div class="wrap cards" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:16px">
{photo(1, "Haemodialysis machine at the unit", 480, "50% 15%", sizes="(max-width: 760px) 100vw, 33vw")}
<div class="ph" style="height:480px"><strong>Treatment bay</strong><span>Photo coming soon</span></div>
<div class="ph" style="height:480px"><strong>Reception &amp; lounge</strong><span>Photo coming soon</span></div>
</div></section>
<section class="section alt"><div class="wrap stack-lg">
<div class="stack max-lg"><p class="eyebrow">What we stand for</p><h2 class="h2">Life. Hope. <span class="accent">Better Tomorrow.</span></h2></div>
<div class="cards reveal">
<div class="card" style="min-height:300px"><span class="n">01</span><strong class="big">Life</strong><p class="body">Safe, consistent treatment every session: trained nurses, modern machines and strict infection control.</p></div>
<div class="card" style="min-height:300px"><span class="n">02</span><strong class="big">Hope</strong><p class="body">Dialysis is part of your week, not your whole life. Flexible shifts and holiday sessions keep you living fully.</p></div>
<div class="card navy" style="min-height:300px"><span class="n">03</span><strong class="big">Better Tomorrow</strong><p class="body">Education on diet and fluids, support for families, and referral toward transplant when the time is right.</p></div>
</div></div></section>
<section class="section"><div class="wrap split">
<div class="stack"><p class="eyebrow">At a glance</p><h2 class="h2">Nikko Dialysis Center, in brief.</h2><p class="lead">The essentials, in one place.</p></div>
<dl class="kv reveal">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in glance)}</dl>
</div></section>
<section id="team" class="section tight-top"><div class="wrap split">
<div class="stack"><p class="eyebrow">Your care team</p><h2 class="h2">The people beside your chair.</h2></div>
<div class="rule-list reveal">{"".join(f'<div style="grid-template-columns:1fr 1.4fr"><strong class="h3">{t}</strong><span class="body">{d}</span></div>' for t, d in team)}</div>
</div></section>
<section id="standards" class="section dark"><div class="wrap split">
<div class="stack"><p class="eyebrow">Licences &amp; standards</p><h2 class="h2">Licensed, inspected, accountable.</h2><p class="lead">We follow national guidelines for haemodialysis and infection prevention. Licences are displayed at reception and available on request.</p></div>
<dl class="kv">{"".join(f"<div><dt>{k}</dt><dd><strong style='font-weight:600'>{v}</strong></dd></div>" for k, v in lic)}</dl>
</div></section>
<section class="section"><div class="wrap"><div class="banner green"><div class="stack max-md" style="gap:12px"><h2 class="h2 sm">See the unit before you start.</h2><p class="body">Bring a family member. Tours by appointment.</p></div><a class="btn btn-dark" href="/contact">Book a tour</a></div></div></section>
'''
    return page("about", body)

def patients():
    items = ["National ID or passport", "Referral letter from your doctor", "Recent blood results", "List of your current medicines", "SHA number or insurance card", "A warm layer, a book or headphones"]
    checks = "".join(f'<button type="button" class="check" aria-pressed="false"><span class="box">{ic("check", 3)}</span><span class="label">{t}</span></button>' for t in items)
    habits = [("01", "Watch your fluids", "Keep to the daily allowance your team gives you, including tea, soup and fruit."), ("02", "Go easy on salt", "Less salt means less thirst. Season with herbs, lemon and onion instead."),
              ("03", "Protect your access", "No BP cuffs, tight sleeves or heavy bags on your fistula arm. Check the buzz daily."), ("04", "Never skip a session", "Running late or unwell? Call us. We will find another slot rather than lose a treatment.")]
    cats = ["All", "Treatment", "Scheduling", "Payment", "Families"]
    fbtn = "".join(f'<button type="button" class="pill" data-value="{c}" aria-pressed="{"true" if c == "All" else "false"}">{c}</button>' for c in cats)
    faq_ld = jsonld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, q, a in FAQS]})
    body = f'''<section class="page-hero"><div class="wrap stack" style="gap:28px">
<p class="eyebrow">Patients &amp; families</p><h1 class="h1 max-lg">Living well <span class="accent">on dialysis.</span></h1>
<p class="lead max-md">Plain answers for patients and the people who care for them, from your first session to everyday life in between.</p>
</div></section>
<section style="padding:0 0 128px"><div class="wrap split">
<div class="stack"><p class="eyebrow">Your first session</p><h2 class="h2">What to bring.</h2><p class="lead">Arrive 20 minutes early on day one. A nurse will show you around and answer every question before you start.</p></div>
<div class="checklist" data-checklist>{checks}<div class="row-between" style="padding-top:20px"><span class="small">Tap to tick off. Saved on this device.</span><strong data-count style="font-weight:600">0 / {len(items)} ready</strong></div></div>
</div></section>
<section class="section alt"><div class="wrap stack-lg">
<div class="split end"><div class="stack"><p class="eyebrow">Between sessions</p><h2 class="h2">Small habits, <span class="accent">big difference.</span></h2></div><p class="body max-sm">General guidance only. Your care team sets your personal fluid and diet limits.</p></div>
<div class="cards reveal" style="gap:0;border-top:1px solid var(--line)">{"".join(f'<div class="stack" style="gap:12px;padding:32px 28px 32px 0;border-bottom:1px solid var(--line)"><span class="eyebrow" style="text-transform:none">{n}</span><strong class="h3">{t}</strong><span class="body">{d}</span></div>' for n, t, d in habits)}</div>
<div class="alert">{ic("alert", 2)}<p class="body" style="color:var(--navy)"><strong>Get help straight away</strong> for chest pain, severe breathlessness, bleeding from your access that won't stop, or if your fistula buzz disappears. Go to the nearest emergency department and call us on <a href="tel:{C['phone_tel']}">{C['phone_display']}</a>.</p></div>
</div></section>
<section id="families" class="section"><div class="wrap split">
<div class="stack"><p class="eyebrow">Families &amp; carers</p><h2 class="h2">You're part of the care team too.</h2><p class="lead">Sit in on a session, ask the nurses anything, and join our family talks on diet, fluids and what to watch for at home.</p></div>
<div class="rule-list reveal" style="padding:0">
<div style="grid-template-columns:1fr auto;align-items:center"><strong class="h3" style="font-size:18px">Kidney-friendly Kenyan meals guide</strong><a class="chip" href="/contact">Request a copy</a></div>
<div style="grid-template-columns:1fr auto;align-items:center"><strong class="h3" style="font-size:18px">Caring for a fistula at home</strong><a class="chip" href="/contact">Request a copy</a></div>
<div style="grid-template-columns:1fr auto;align-items:center"><strong class="h3" style="font-size:18px">Family education talks</strong><a class="chip" href="/contact">Ask for dates</a></div>
</div>
</div></section>
<section id="faq" class="section alt"><div class="wrap stack" style="max-width:1000px;gap:32px">
<div class="stack"><p class="eyebrow">Questions</p><h2 class="h2">Frequently asked.</h2></div>
<div class="row" style="gap:8px" data-faq-filter="faq-list" role="group" aria-label="Filter questions">{fbtn}</div>
{faq_html(FAQS, "faq-list")}
</div></section>
'''
    return page("patients", body, faq_ld)

def insurance():
    cards = "".join(f'<div class="ins" data-insurer="{e(n)}"><div class="logo">{logo_img(s, n + " logo")}</div><div class="meta"><span>{n}</span><span class="ok"><i class="dot" aria-hidden="true"></i>Accepted</span></div></div>' for n, s in INSURERS)
    steps = [("Share your details", "ID, SHA number and insurance card, at your consultation or by WhatsApp."), ("We verify &amp; pre-authorise", "Our billing team checks eligibility with SHA and requests approval from your insurer."),
             ("You get a written estimate", "What's covered, what isn't, and any balance per session, before treatment starts."), ("Receipt for every session", "Monthly statements to you, your insurer or your employer on request.")]
    body = f'''<section class="page-hero"><div class="wrap split end">
<div class="stack"><p class="eyebrow">Insurance &amp; payment</p><h1 class="h1">Cover sorted <span class="accent">before you start.</span></h1></div>
<p class="lead max-sm">We work with SHA and Kenya's major medical insurers. Our billing team confirms your benefit, handles pre-authorisation and explains any balance in writing, before your first session.</p>
</div></section>
<section style="padding:0 0 112px"><div class="wrap stack" style="gap:28px">
<div class="row-between"><h2 class="h3" style="font-size:26px">Insurers we work with</h2>
<label class="search"><span class="sr-only">Search insurers</span>{ic("search", 2)}<input id="insurer-search" class="input" type="search" placeholder="Search your insurer" autocomplete="off"></label></div>
<div class="ins-grid">{cards}<a class="ins more" href="/contact"><strong style="font-size:20px;font-weight:600;letter-spacing:-.02em">+ many others</strong><span class="small">Including corporate and embassy schemes. Ask us about yours →</span></a></div>
<p id="insurer-none" class="body" hidden>Don't see your insurer? <a href="/contact">Ask us</a>. We may still be able to work with them or help with a reimbursement claim.</p>
<p class="note">Logos are trademarks of their owners, shown to indicate accepted cover. Cover depends on your individual plan.</p>
</div></section>
<section class="section alt"><div class="wrap stack-lg">
<div class="stack max-lg"><p class="eyebrow">Ways to pay</p><h2 class="h2">Three routes. <span class="accent">One clear bill.</span></h2></div>
<div class="cards reveal">
<div class="card"><span class="n">01</span><h3 class="h3" style="font-size:26px">Social Health Authority</h3><p class="body">SHA covers haemodialysis for registered members under its chronic care benefit. Bring your ID and SHA number and we verify eligibility and your current session benefit on the day.</p></div>
<div class="card"><span class="n">02</span><h3 class="h3" style="font-size:26px">Private insurance</h3><p class="body">We request pre-authorisation directly from your insurer and can combine private cover with SHA to reduce what you pay yourself.</p></div>
<div class="card deep"><span class="n">03</span><h3 class="h3" style="font-size:26px">Self-pay &amp; corporate</h3><p class="body">Per-session price: {C['price_per_session']}. Pay by M-Pesa, Airtel Money, bank transfer or cash. Employers and embassies can open a corporate account.</p></div>
</div></div></section>
<section class="section"><div class="wrap split center">
<div class="stack"><p class="eyebrow">Payments accepted</p><h2 class="h2 sm">Pay the way that suits you.</h2><p class="body">For balances, top-ups and self-pay sessions. You get a receipt every time.</p></div>
<div class="pay-grid">
<div class="pay">{logo_img("mpesa", "M-Pesa")}<span>Paybill {C['mpesa_paybill']}</span></div>
<div class="pay">{logo_img("airtel-money", "Airtel Money")}<span>Till {C['airtel_till']}</span></div>
<div class="pay">{ic("bank", 1.6)}<strong>Bank transfer</strong></div>
<div class="pay">{ic("cash", 1.6)}<strong>Cash</strong></div>
</div>
</div></section>
<section class="section tight-top"><div class="wrap split">
<div class="stack"><p class="eyebrow">How approval works</p><h2 class="h2">What happens with your cover.</h2><p class="lead">If you need dialysis urgently, we'll talk you through the options at your consultation.</p></div>
<ol class="rule-list reveal">{"".join(f'<li><span class="n">0{i+1}</span><span class="stack" style="gap:6px"><strong class="h3" style="font-size:19px">{t}</strong><span class="body">{d}</span></span></li>' for i, (t, d) in enumerate(steps))}</ol>
</div></section>
<section class="section tight-top"><div class="wrap"><div class="banner blue"><div class="stack max-md" style="gap:12px"><h2 class="h2 sm">Not sure what you're covered for?</h2><p class="body">Send us your details and we'll check before you commit to anything.</p></div><a class="btn btn-dark" href="/contact">Check my cover {ic("arrow", 2)}</a></div></div></section>
'''
    return page("insurance", body)

def radios(name, opts, checked=None):
    return '<div class="radios">' + "".join(f'<label class="radio"><input type="radio" name="{name}" value="{o}"{" checked" if o == checked else ""}><span>{o}</span></label>' for o in opts) + "</div>"

def contact():
    needs = [("Start dialysis", "New to dialysis or newly referred", "drop"), ("Transfer to Nikko", "Moving from another unit", "swap"), ("Holiday dialysis", "Visiting Nairobi for a while", "home"),
             ("Check my cover", "SHA or private insurance", "shield"), ("Book a tour", "See the unit before you start", "eye"), ("Diet &amp; education", "For you or your family", "leaf"), ("Something else", "Billing, records, feedback", "chat")]
    ncards = "".join(f'<label class="need"><input type="checkbox" name="needs" value="{e(html.unescape(t))}"><span class="ico">{ic(i, 1.9)}</span><span class="txt"><strong>{t}</strong><span class="sub">{s}</span></span><span class="tick">{ic("check", 3)}</span></label>' for t, s, i in needs)
    mp = f'<iframe src="{C["maps_embed"]}" title="Map to {C["name"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>' if C["maps_embed"] else "Map will appear here once the address is confirmed."
    directions = C["maps_url"] or "https://www.google.com/maps/search/?api=1&query=" + "Nikko+Dialysis+Center+Nairobi"
    body = f'''<section class="page-hero" style="padding-bottom:48px"><div class="wrap stack" style="gap:20px">
<p class="eyebrow">Contact &amp; booking</p><h1 class="h1 max-lg">Tell us what you need. <span class="accent">We'll do the rest.</span></h1>
<p class="lead max-md">Two quick steps. A nurse from our team calls you back within one working day, usually sooner.</p>
</div></section>
<section style="padding:0 0 128px"><div class="wrap contact-grid">
<div class="form-card">
<form id="booking" novalidate>
<div class="stack" style="gap:36px">
<div class="progress" aria-live="polite"><div class="row-between" style="font-size:14px;font-weight:600"><span data-step-label>Step 1 of 2 · Your needs</span><span data-step-pct class="small">50%</span></div><div class="bars" aria-hidden="true"><span class="on"></span><span data-bar2></span></div></div>
<div id="step-1" class="step stack" style="gap:36px">
<fieldset><legend class="big">What can we help with? <small>Choose all that apply.</small></legend><div class="needs">{ncards}</div></fieldset>
<fieldset><legend>Who is this for?</legend>{radios("who", ["Myself", "A family member", "I'm a referring doctor"], "Myself")}</fieldset>
<fieldset><legend>Preferred shift <span class="small" style="display:inline;font-weight:400">(optional)</span></legend>{radios("shift", ["Morning", "Midday", "Evening", "Flexible"])}</fieldset>
<div class="form-foot"><span class="small" data-selected>Select at least one option</span><button id="to-step-2" class="btn btn-dark" type="button" disabled>Continue {ic("right", 2)}</button></div>
</div>
<div id="step-2" class="step stack" style="gap:28px" hidden>
<div class="stack" style="gap:10px"><h2 class="h3" style="font-size:26px">How can we reach you?</h2><div class="row" style="gap:8px"><span class="small">About:</span><span id="chosen" class="row" style="gap:8px"></span><button type="button" data-back class="link" style="border:0;background:none;cursor:pointer;color:var(--blue);padding:0">Edit</button></div></div>
<div class="fields">
<label class="field">Full name *<input id="name" class="input" name="name" required maxlength="80" autocomplete="name"></label>
<label class="field">Phone number *<input class="input" name="phone" type="tel" required inputmode="tel" pattern="[0-9+ ()-]{{9,18}}" maxlength="18" autocomplete="tel" placeholder="07XX XXX XXX"></label>
<label class="field"><span>Email <span class="opt">(optional)</span></span><input class="input" name="email" type="email" maxlength="120" autocomplete="email" autocapitalize="off" spellcheck="false"></label>
<label id="dates-field" class="field" hidden>Travel dates *<input id="dates" class="input" name="dates" maxlength="60" placeholder="e.g. 12–26 Dec"></label>
<label class="field"><span>Current dialysis unit <span class="opt">(if any)</span></span><input class="input" name="unit" maxlength="100"></label>
</div>
<fieldset><legend style="font-size:14px">Best way to reach you</legend>{radios("method", ["Phone call", "WhatsApp", "Email"], "Phone call")}</fieldset>
<fieldset><legend style="font-size:14px">Best time (Nairobi time)</legend>{radios("time", ["Morning", "Afternoon", "Evening"], "Morning")}</fieldset>
<label class="field"><span>Anything else we should know? <span class="opt">(optional)</span></span><textarea class="input" name="notes" rows="3" maxlength="1000" placeholder="Referring doctor, access type, questions…"></textarea></label>
<label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>
<p class="small" style="background:var(--surface-alt);border-radius:14px;padding:14px 16px;font-size:13px">Please don't share detailed medical records here. We'll collect what we need securely at your consultation.</p>
<div class="stack" style="gap:12px">
<label class="consent"><input type="checkbox" name="consent" value="yes" required><span>I consent to {C['name']} using these details, including any health information I've chosen to share, to respond to my request, as set out in the <a href="/privacy">privacy policy</a>. *</span></label>
<label class="consent"><input type="checkbox" name="marketing" value="yes"><span>Send me occasional patient education updates. I can opt out at any time.</span></label>
</div>
<p id="form-error" class="form-error" role="alert" hidden>We couldn't send your request. Please check your connection and try again, or call <a href="tel:{C['phone_tel']}">{C['phone_display']}</a> / <a href="{WA}" rel="noopener" target="_blank">WhatsApp us</a>.</p>
<div class="form-foot"><button type="button" class="btn btn-line" data-back>{ic("left", 2)} Back</button><button type="submit" class="btn btn-dark">Submit request</button></div>
</div>
</div>
</form>
<div id="done" class="done stack" tabindex="-1" hidden style="gap:22px;padding:24px 0">
<span class="well" style="width:72px;height:72px">{ic("check", 2.25)}</span>
<h2 class="h2" style="font-size:40px">Thank you, <span data-first></span>.</h2>
<p class="lead max-md">We've received your request. A nurse will reach you by <strong data-method style="color:var(--navy)"></strong> within one working day.</p>
<div class="stack" style="background:var(--surface-alt);border-radius:18px;padding:24px;gap:12px"><span class="small" style="text-transform:uppercase;letter-spacing:.04em;font-size:13px;font-weight:600">You asked about</span><div id="done-needs" class="row" style="gap:8px"></div></div>
<p class="small">Urgent? Call <a href="tel:{C['phone_tel']}">{C['phone_display']}</a>. In an emergency go to the nearest emergency department.</p>
<div class="row"><a class="btn btn-line" href="/patients">Prepare for your first session</a><a class="btn btn-line" href="/insurance">Check insurance</a></div>
</div>
</div>
<aside aria-label="Contact details">
<a class="contact-link" href="tel:{C['phone_tel']}"><span class="well">{ic("phone")}</span><span><small>Call the unit</small><strong>{C['phone_display']}</strong></span></a>
<a class="contact-link" href="{WA}" rel="noopener" target="_blank"><span class="well">{ic("chat")}</span><span><small>WhatsApp</small><strong>{C['whatsapp_display']}</strong></span></a>
<a class="contact-link" href="mailto:{C['email']}"><span class="well blue">{ic("mail")}</span><span><small>Email</small><strong style="font-size:16px">{C['email']}</strong></span></a>
<div class="visit"><div class="stack" style="gap:6px"><span class="small" style="color:var(--dark-muted)">Visit us</span><address style="font-style:normal;font-size:18px;font-weight:600;line-height:1.4">{C['street']}<br>{C['area']}, Nairobi</address></div><hr>
<dl class="hours"><dt>Mon–Fri</dt><dd>{C['hours_weekdays']}</dd><dt>Saturday</dt><dd>{C['hours_saturday']}</dd><dt>Sunday</dt><dd>{C['hours_sunday']}</dd></dl>
<a class="btn btn-white btn-sm" href="{directions}" rel="noopener" target="_blank">Get directions</a></div>
<div class="map">{mp}</div>
</aside>
</div></section>
'''
    return page("contact", body)

def privacy():
    body = f'''<section class="page-hero" style="padding-bottom:56px"><div class="wrap stack" style="gap:24px">
<p class="eyebrow">Legal</p><h1 class="h1 max-lg">Privacy, terms <span class="accent">&amp; your rights.</span></h1>
<p class="lead max-md">How we handle your information under Kenya's Data Protection Act, 2019, and the terms for using this website. Last updated {C['last_updated']}.</p>
</div></section>
<section style="padding:0 0 128px"><div class="wrap legal">
<nav class="toc" aria-label="Contents"><span class="small" style="font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">On this page</span><a href="#privacy">Privacy policy</a><a href="#rights">Your rights</a><a href="#cookies">Cookies</a><a href="#terms">Terms of use</a><a href="#accessibility">Accessibility</a></nav>
<article>
<section id="privacy"><h2 class="h2 sm">Privacy policy</h2>
<p class="body">{C['name']} ("we") is the data controller for information collected through this website, registered with the Office of the Data Protection Commissioner (ODPC) under no. {C['odpc_reg']}. Contact our data protection officer at <a href="mailto:{C['email']}">{C['email']}</a>.</p>
<h3 class="h3">What we collect</h3><p class="body">Only what we need to respond to you: your name, phone number, optional email, the services you ask about, preferred contact method and time, and anything you choose to type in the message box. We do not ask for medical records through this website.</p>
<h3 class="h3">Health information</h3><p class="body">Information about your health is sensitive personal data. We process it only with your explicit consent, given on our booking form, or where needed to provide your care, and we keep it confidential under professional medical duties.</p>
<h3 class="h3">How we use it</h3><p class="body">To call or message you back, arrange consultations and sessions, check your SHA or insurance cover with your permission, and, only if you opt in, send patient education updates. We never sell your data or use it for third-party advertising.</p>
<h3 class="h3">Who we share it with</h3><p class="body">Your insurer or SHA (to verify cover, with your consent), your referring or home dialysis unit (for transfers and holiday sessions), and service providers who host our website and email under written data-processing agreements. Where data is stored outside Kenya, we apply the safeguards the Act requires.</p>
<h3 class="h3">How long we keep it</h3><p class="body">Enquiries that don't lead to care are deleted after 12 months. Clinical records are kept for the period required by Kenyan health regulations.</p>
<h3 class="h3">Security</h3><p class="body">This site uses HTTPS encryption. Enquiries are stored with access limited to staff who need them, and backed up securely.</p>
</section>
<section id="rights"><h2 class="h2 sm">Your rights</h2>
<p class="body">Under the Data Protection Act, 2019 you can:</p>
<ul><li>be told how your data is used</li><li>access the data we hold about you</li><li>ask us to correct or delete it</li><li>object to or withdraw consent for processing, including marketing, at any time</li><li>complain to the Office of the Data Protection Commissioner (<a href="https://www.odpc.go.ke" rel="noopener" target="_blank">odpc.go.ke</a>)</li></ul>
<p class="body">To use any of these rights, email <a href="mailto:{C['email']}">{C['email']}</a> or ask at reception. If you are in the EU or UK, you have equivalent rights under the GDPR.</p>
<div class="card" style="padding:24px;gap:8px"><strong class="h3" style="font-size:18px">Patient rights</strong><p class="body">You have the right to respectful, safe care; to clear information about your treatment and costs; to a second opinion; and to raise a complaint without it affecting your care. Speak to the nurse in charge or email us.</p></div>
</section>
<section id="cookies"><h2 class="h2 sm">Cookies</h2>
<p class="body">We use essential storage to make the site work and remember your choices. With your consent, we also use privacy-friendly analytics and error tracking to see which pages help people and to fix problems. You can change your choice at any time using <a href="/privacy#cookies" data-cookie-settings>cookie settings</a>.</p>
<div class="table"><div><span>Type</span><span>Purpose</span><span>Consent</span></div><div><span>Essential</span><span>Security, form spam protection, remembering your cookie choice and checklist</span><span>Always on</span></div><div><span>Analytics</span><span>Anonymous page visits and site errors</span><span>Only if accepted</span></div></div>
</section>
<section id="terms"><h2 class="h2 sm">Terms of use</h2>
<p class="body">This website gives general information about our services. It is not medical advice and does not create a doctor–patient relationship. Always follow the advice of your own doctor or care team.</p>
<p class="body">A request sent through this website is not a confirmed booking until our team contacts you. Prices, hours and insurance arrangements may change; we confirm them in writing before treatment. Images show our unit or are used with permission, and insurer logos are trademarks of their owners. Patient stories are shared only with written consent.</p>
<p class="body">This website does not use AI chat or automated medical advice. These terms are governed by the laws of Kenya.</p>
</section>
<section id="accessibility"><h2 class="h2 sm">Accessibility</h2>
<p class="body">We aim to meet WCAG 2.2 AA: readable text sizes, strong colour contrast, keyboard navigation and screen-reader labels. If anything on this site is hard to use, tell us at <a href="mailto:{C['email']}">{C['email']}</a> and we'll fix it.</p>
</section>
</article>
</div></section>
'''
    return page("privacy", body)

def notfound():
    body = f'''<section class="section"><div class="wrap stack" style="max-width:900px;gap:28px">
<p class="eyebrow">Error 404</p><h1 class="h1">This page has <span class="accent">moved or doesn't exist.</span></h1>
<p class="lead max-md">The link may be old or mistyped. Here's where most people are heading:</p>
<div class="rule-list" style="width:100%">
<a href="/contact" style="grid-template-columns:1fr auto;text-decoration:none;color:var(--navy);font-size:20px;font-weight:600">Book a consultation<span>→</span></a>
<a href="/services#holiday" style="grid-template-columns:1fr auto;text-decoration:none;color:var(--navy);font-size:20px;font-weight:600">Holiday dialysis<span>→</span></a>
<a href="/insurance" style="grid-template-columns:1fr auto;text-decoration:none;color:var(--navy);font-size:20px;font-weight:600">Insurance &amp; SHA<span>→</span></a>
</div>
<div class="row"><a class="btn btn-dark" href="/">Back to home</a><a class="btn btn-line" href="tel:{C['phone_tel']}">Call the unit</a></div>
</div></section>
'''
    return page("404", body)

# ---------------------------------------------------------------------------
# SEO / AI files
# ---------------------------------------------------------------------------
def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)

VERSION = datetime.datetime.now().strftime("%Y%m%d%H%M")

def main():
    out = {"index.html": home(), "services.html": services(), "about.html": about(), "patients.html": patients(),
           "insurance.html": insurance(), "contact.html": contact(), "privacy.html": privacy(), "404.html": notfound()}
    for f, s in out.items():
        write(f, s)
    pri = {"index": "1.0", "contact": "0.9", "services": "0.9", "insurance": "0.8", "patients": "0.8", "about": "0.7", "privacy": "0.3"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for k, p in pri.items():
        sm.append(f"  <url><loc>{C['url']}{PAGES[k][0] if PAGES[k][0] != '/' else '/'}</loc><lastmod>{C['last_updated']}</lastmod><priority>{p}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot"]
    write("robots.txt", "# Nikko Dialysis Center\nUser-agent: *\nAllow: /\nDisallow: /api/\n\n# AI assistants and AI search are welcome, so patients asking them about dialysis in Nairobi get accurate answers.\n"
          + "".join(f"User-agent: {b}\nAllow: /\nDisallow: /api/\n\n" for b in bots) + f"Sitemap: {C['url']}/sitemap.xml\n")
    write("llms.txt", f"""# {C['name']}

> Outpatient haemodialysis centre in {C['area']}, Nairobi, Kenya. Tagline: "Life. Hope. Better Tomorrow." Accepts SHA (Social Health Authority) and major Kenyan medical insurers. Offers holiday dialysis for people visiting Nairobi.

## Key facts
- Services: haemodialysis (usually 3 sessions a week, about 4 hours each), holiday/visiting dialysis, vascular access care, kidney diet education, nephrologist reviews and transplant referral.
- Shifts: morning {C['shift_morning']}, midday {C['shift_midday']}, evening {C['shift_evening']}. Open Mon–Fri {C['hours_weekdays']}, Sat {C['hours_saturday']}, Sun {C['hours_sunday']}.
- Insurance: {", ".join(n for n, _ in INSURERS)} and many others.
- Payment: M-Pesa (Paybill {C['mpesa_paybill']}), Airtel Money (Till {C['airtel_till']}), bank transfer, cash.
- Address: {ADDR}, Kenya. Phone: {C['phone_display']}. WhatsApp: {C['whatsapp_display']}. Email: {C['email']}.
- Booking: new patients, transfers and visitors request a consultation at {C['url']}/contact. A nurse calls back within one working day.
- Emergencies: this centre is not an emergency department. In an emergency go to the nearest hospital emergency department or call 999 / 112.

## Pages
- [Services]({C['url']}/services): haemodialysis, holiday dialysis, access care, diet education, reviews
- [Insurance & payment]({C['url']}/insurance): accepted insurers, SHA, approval steps, payment methods
- [Patients & families]({C['url']}/patients): first-session checklist, living well on dialysis, FAQs
- [About]({C['url']}/about): team, standards, licences, key facts
- [Contact & booking]({C['url']}/contact): two-step booking request, phone, WhatsApp, map
- [Privacy & terms]({C['url']}/privacy)
""")
    write("assets/js/config.js", "window.NIKKO=" + json.dumps({"plausibleDomain": C["plausible_domain"], "sentryLoader": C["sentry_loader"]}) + ";\n")
    exp = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()
    write(".well-known/security.txt", f"Contact: mailto:{C['email']}\nExpires: {exp}T00:00:00.000Z\nPreferred-Languages: en\nCanonical: {C['url']}/.well-known/security.txt\n")
    print("Built", len(out), "pages for", C["url"])

if __name__ == "__main__":
    main()

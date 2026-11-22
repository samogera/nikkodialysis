# Nikko Dialysis Center — website

*Life. Hope. Better Tomorrow.*

A fast static website for Nikko Dialysis Center, Nairobi: plain HTML, CSS and vanilla JavaScript with no framework and no build step to deploy, plus one serverless function for the booking form.

## Pages
| URL | File | Purpose |
|---|---|---|
| `/` | `index.html` | Home: hero, insurer logos, services, unit, process |
| `/services` | `services.html` | Haemodialysis (session stages tabs), holiday dialysis, access care, diet, reviews |
| `/about` | `about.html` | Values, key facts ("at a glance"), care team, licences |
| `/patients` | `patients.html` | First-session checklist, habits, families, filterable FAQ |
| `/insurance` | `insurance.html` | Searchable insurer grid, ways to pay, M-Pesa / Airtel Money / bank / cash, approval steps |
| `/contact` | `contact.html` | Two-step booking form (needs → details), contact details, map |
| `/privacy` | `privacy.html` | Privacy policy (Kenya Data Protection Act 2019), rights, cookies, terms, accessibility |
| `404` | `404.html` | Custom not-found page (served automatically by Vercel) |

## Editing content
All business details live in **`CONFIG` at the top of `scripts/build.py`**: phone, WhatsApp, email, address, hours, shift times, Paybill/Till, prices, licence numbers, map links, social links and the domain.

```bash
python3 scripts/build.py      # regenerates every page, sitemap.xml, robots.txt, llms.txt, config.js
```
Edit page copy in the same file (one function per page). Styles are in `assets/css/styles.css`; behaviour in `assets/js/main.js`.

## Deploy (Vercel)
1. Import this repo in Vercel → Framework preset **Other** → no build command → output directory `.` (root).
2. Add environment variables (Project → Settings → Environment Variables), see `.env.example`:
   - `RESEND_API_KEY`, `ENQUIRY_TO`, `ENQUIRY_FROM`: booking emails via [Resend](https://resend.com) (verify the sending domain first)
   - `ENQUIRY_WEBHOOK_URL` (optional): also send each enquiry to Google Sheets / Zapier / Slack / CRM
3. Add the custom domain, set `CONFIG["url"]` to it, run the build, commit.
4. Submit `https://YOUR-DOMAIN/sitemap.xml` in Google Search Console and Bing Webmaster Tools.

## What's built in
**Performance**
- No frameworks; ~30 KB CSS and ~10 KB JS, both deferred / cache-busted and served with 1-year immutable caching
- Images converted to WebP with `srcset`, explicit width/height (no layout shift), lazy-loading below the fold, hero image preloaded with `fetchpriority="high"`
- Fonts: Google Fonts with `preconnect` and `display=swap`

**SEO**
- Unique `<title>` and meta description per page, canonical URLs, Open Graph + Twitter cards with a 1200×630 `og-image.jpg`
- JSON-LD: `MedicalClinic` (home), `WebSite`, `BreadcrumbList` (every page), `FAQPage` (patients)
- `sitemap.xml`, `robots.txt`, clean URLs, one `<h1>` per page, descriptive alt text, `lang="en-KE"`, geo meta
- Redirects for common paths (`/book`, `/booking`, `/home`, `/terms`, `/privacy-policy`)

**AI search (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews)**
- `llms.txt` fact sheet; `robots.txt` explicitly allows AI crawlers (not `/api/`)
- "At a glance" facts and plain question-and-answer FAQs that AI tools can quote accurately

**Favicons & app**
- `favicon.ico` (16/32/48), PNG favicons, `apple-touch-icon.png`, 192/512 icons, maskable icon, `site.webmanifest`, theme colour

**Conversion & retention**
- One primary action everywhere: **Book a consultation**; sticky mobile bar (Call · WhatsApp · Book now)
- Two-step booking form with tappable cards, progress bar, travel-dates field shown only for holiday dialysis, a thank-you screen with next steps
- Patient-tips email signup in the footer, first-session checklist saved on the device
- Animated heartbeat line and split "Dialysis Center" wordmark in the footer (disabled when the visitor prefers reduced motion)

**Security**
- No secrets in front-end code; email keys exist only as Vercel environment variables
- Strict security headers: HSTS, CSP, X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy
- Form API: POST only, same-origin check, 8 KB body limit, honeypot spam field, per-IP rate limit, idempotency key (double taps create one enquiry), server-side validation, HTML-escaped emails
- `/.well-known/security.txt`

**Real-user edge cases handled**
- Submit button locks while sending; 15-second timeout with a clear "Try again / call / WhatsApp" fallback when signal drops
- Emails lower-cased and trimmed; names with apostrophes or hyphens (O'Brien, Wanjiru-Otieno) accepted
- Times are shown as Nairobi time and the visitor's time zone is recorded for visiting patients

**Privacy & legal**
- Consent checkbox on every form; marketing opt-in is separate and unticked
- Analytics (Plausible) and error tracking (Sentry) load **only after** "Accept all" in the cookie notice; "Cookie settings" link in the footer
- Medical disclaimer and emergency guidance in the footer; no AI chat, no fake reviews, insurer logos marked as trademarks of their owners

**Accessibility**
- Skip link, keyboard-operable menu, tabs and form, visible focus rings, ARIA labels, 4.5:1 contrast, 16px+ body text, 48px tap targets

## Launch checklist
- [ ] Replace every `[PLACEHOLDER]` in `CONFIG` (phone, WhatsApp, email, address, hours, shifts, Paybill, Till, price, licence numbers) and rebuild
- [ ] Set the real domain in `CONFIG["url"]`; set `ENQUIRY_*` env vars; send a test booking and a test signup
- [ ] Confirm the insurer list against the centre's contracts; get a full Old Mutual logo and a sharper Madison logo
- [ ] Add photos of the treatment bay, reception and building (with consent for any identifiable person)
- [ ] Have a Kenyan advocate review `/privacy`; register with the ODPC as a data controller
- [ ] Create and verify Google Business Profile ("Dialysis center"), Bing Places and Apple Business Connect with identical name, address and phone
- [ ] Add `maps_embed` and `maps_url`, and the social profile links
- [ ] Enable analytics: set `plausible_domain` (and optionally `sentry_loader`) in `CONFIG`
- [ ] Back up enquiries: use `ENQUIRY_WEBHOOK_URL` to copy each one into a Google Sheet
- [ ] Run PageSpeed Insights on mobile (target LCP < 2.5 s, CLS < 0.1, INP < 200 ms) and a broken-link check
- [ ] For strict rate limits across server instances, move the in-memory limiter in `api/enquiry.js` to Upstash Redis / Vercel KV

## Structure
```
├── index.html, services.html, about.html, patients.html, insurance.html, contact.html, privacy.html, 404.html
├── assets/css/styles.css      brand tokens + all styles
├── assets/js/main.js          menu, reveal, tabs, checklist, insurer search, FAQ filter, cookie consent, forms
├── assets/js/config.js        generated: analytics settings
├── assets/img/                logo, photos (WebP), partners/ (insurer + payment logos)
├── api/enquiry.js             booking + newsletter endpoint (Vercel function)
├── scripts/build.py           generator: edit CONFIG and copy here
├── sitemap.xml, robots.txt, llms.txt, site.webmanifest, .well-known/security.txt
├── favicon*, apple-touch-icon.png, icon-*.png, og-image.jpg, logo.png
└── vercel.json                clean URLs, redirects, security + cache headers
```

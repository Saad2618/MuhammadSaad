# Muhammad Saad | Full Stack Developer

Static portfolio for Muhammad Saad, a senior full stack developer in Riyadh. The site is plain HTML, CSS, and JavaScript. It does not need a build step, a server, or a database.

Open `index.html` in a browser to review the pages. The typefaces are embedded in the stylesheet, so they load from a file address, and the web manifest is attached only on http or https. Use a local static server when you test the contact form, because some browsers block `fetch` from `file://` addresses.

```text
npx serve .
```

Or, with Python installed:

```text
python -m http.server 8080
```

Then visit `http://localhost:8080`.

The placeholder domain used in canonical links, Open Graph tags, `robots.txt`, and `sitemap.xml` is `https://muhammadsaad.dev`. Replace it before the site is public.

## Replace before publication

- Domain: search the project for `https://muhammadsaad.dev` and replace it with the real origin, including `sitemap.xml` and `robots.txt`.
- GitHub: set `contact.github` in `assets/js/site-config.js` to a full `https://github.com/...` profile URL. Until then the footer shows “GitHub profile link forthcoming” and does not link to a placeholder.
- Contact form: set `form.endpoint` in `assets/js/site-config.js`. Until that value is a real Formspree URL, the form validates locally and then explains that it is not connected. It will not show a success message for an unsent inquiry.
- Pricing: replace the `[Add …]` strings in `pricing.models`, then set `pricing.showRates` to `true`. Rates that still start with `[Add` stay hidden.
- Portrait: replace `assets/images/portrait.svg` with a photograph and update the alt text in `index.html`. The current image is an illustration, not a photo of Muhammad Saad.
- Professional projects: confirm the technical focus and the wording on the five case studies before treating them as client-approved.
- Employment: Euphoria XR lists the confirmed title. ArhamSoft, Vision Plus Solution, and AlphaCore Technology list dates only, plus a general description. Add official titles in `assets/js/experience.js` when you want them public.
- Testimonials: add approved quotes to `testimonials` in `assets/js/site-config.js`. Empty means the discreet placeholder stays. Do not invent reviews.
- Analytics: leave `analytics.enabled` false until you choose a provider, then update `privacy.html` before any script loads.

Do not add client logos, production URLs, certification claims, or performance numbers unless they are confirmed and approved.

## Edit the site

| What | Where |
| --- | --- |
| Name, email, phone, WhatsApp, LinkedIn, GitHub, domain, form endpoint, pricing, testimonials | `assets/js/site-config.js` |
| Service cards | `assets/js/services.js` |
| Project catalog and card mockups | `assets/js/projects.js` |
| Experience timeline | `assets/js/experience.js` |
| FAQ answers and FAQ structured data | `assets/js/faqs.js` |
| Colors and layout | `assets/css/styles.css` |
| Hero, about narrative, process, technology groups, contact form fields | `index.html` |
| Case study pages | `projects/*.html` |

Contact details also appear as visible fallbacks in the HTML (footer, contact links, privacy page). If you change an email or phone number, update `site-config.js` and search the HTML for the old value.

`SAAD.DEV` is a compact wordmark only. The site does not describe a registered company.

### Add a project

1. Add an object to `window.PORTFOLIO` in `assets/js/projects.js`.
2. Set `status` to `professional`, `demo`, or `concept`, and set `statusLabel` to `Professional Project`, `Demo Project`, or `Concept Project`. Demo and concept work must stay labeled. Do not mark either as client work.
3. Set `categories` using any of: `enterprise`, `saas`, `ai`, `automation`, `apis`, `analytics`.
4. Set `layout` to one of: `dashboard`, `board`, `pipeline`, `kiosk`, `chat`, `doc`, `endpoints`.
5. Set `page` to `projects/your-slug.html`.
6. Duplicate an existing file in `projects/`, then change the title, description, canonical URL, breadcrumb, copy, and `data-project-id`.
7. Add the new URL to `sitemap.xml`.

The home page renders cards from `projects.js`. You do not need to edit the card layout in `index.html`.

### Pricing visibility

```js
pricing: {
  showRates: false,
  models: {
    hourly: "[Add hourly rate]",
    fixed: "[Add project pricing]",
    retainer: "[Add monthly rate]"
  }
}
```

Visitors see “Rate available on request” until `showRates` is `true` and the bracket placeholders are replaced.

### Contact form

The form uses [Formspree](https://formspree.io). The form ID is public by design. Do not put a private API key in JavaScript.

1. Create a Formspree account and a new form.
2. Confirm the notification email in Formspree.
3. Copy the endpoint, for example `https://formspree.io/f/abcdwxyz`.
4. Set `form.endpoint` in `assets/js/site-config.js`.
5. In the Formspree dashboard, turn on the spam filter. The form already sends the `_gotcha` honeypot field Formspree expects.
6. Serve the site over `http://localhost` and submit a real test. Success text appears only after Formspree returns a successful response.
7. If the request fails, the form keeps the visitor’s text and offers a `mailto:` link with the same details.

Direct alternatives stay on the page: `mailto:msaaddeveloper1@gmail.com`, `tel:+966597899079`, and `https://wa.me/966597899079`.

### Theme, language, and direction

The first visit follows the system light or dark setting. The visitor’s later choice is stored under `saad-theme`.

English is the published locale. `assets/js/i18n/en.js` records that Arabic is planned. Layout CSS uses logical properties (`margin-inline`, `padding-inline`, `inset-inline`) so a future right-to-left version does not require a second stylesheet.

To add Arabic later:

1. Create `ar/index.html` with `lang="ar"` and `dir="rtl"`.
2. Translate the visible copy and the content modules.
3. Add `hreflang` links on both versions.
4. Add the Arabic URLs to the sitemap.

Do not publish an empty Arabic switch before the pages exist.

## Brand files

| File | Use |
| --- | --- |
| `assets/logo/logo-icon.svg` | MS monogram |
| `assets/logo/logo-primary.svg` | Symbol, full name, and title |
| `assets/logo/logo-dark.svg` | Horizontal lockup for dark backgrounds |
| `assets/logo/logo-light.svg` | Horizontal lockup for light backgrounds |
| `favicon.svg` | Browser icon |
| `assets/images/og-share.svg` | Editable social graphic |
| `assets/images/og-share.png` | Open Graph and Twitter image |
| `assets/icons/icon-192.png`, `icon-512.png` | Manifest icons |
| `assets/icons/apple-touch-icon.png` | Apple touch icon |

The monogram is an original geometric M with a cyan S-curve and node marks. It is not a stock logo.

## Deploy

The site is the repository root. No build command. No environment secrets.

After any host is live:

1. Replace the domain placeholder and confirm canonical tags, `robots.txt`, and `sitemap.xml`.
2. Add the Formspree endpoint and send a test message to the real inbox.
3. Click every project card, the theme control, the mobile menu, and the footer links.
4. Check 360px and desktop widths.
5. Confirm WhatsApp opens `https://wa.me/966597899079`.
6. Enable HTTPS on the host. Do not leave the site on plain HTTP once a domain points at it.

### GitHub Pages

1. Push the repository.
2. In Settings → Pages, deploy from the branch root. `/.nojekyll` is included so GitHub does not run Jekyll.
3. For a custom domain, add the domain in Pages settings. GitHub will offer a `CNAME` file. Create that file only after the domain is yours.
4. At the DNS host, add the records GitHub shows (an `A`/`AAAA` set for an apex domain, or a `CNAME` for `www`).
5. Wait for DNS, then enable Enforce HTTPS.

GitHub project sites are served from `/repository-name/` unless you use a user site or a custom domain at the root. This project uses root-relative paths on `404.html`, so host it at the domain root.

### Netlify

1. Add a new site from Git, or drag the folder into Netlify Drop.
2. Build command: none. Publish directory: `.` (`netlify.toml` already sets this).
3. Site configuration → Domain management → add the custom domain.
4. At the DNS host, point the domain at Netlify with the records Netlify shows, or use Netlify DNS.
5. HTTPS is issued automatically after DNS is correct.

### Cloudflare Pages

1. Create a Pages project from the Git repository.
2. Framework preset: none. Build command: empty. Output directory: `/`.
3. Custom domains → set up the domain. If the DNS zone is already on Cloudflare, Pages can add the record.
4. HTTPS is on by default. `_headers` is included for the basic security headers.

### Azure Static Web Apps

1. Create a Static Web App and connect the repository.
2. App location: `/`. Output location: empty (the files are already built). No API location.
3. `staticwebapp.config.json` maps unknown paths to `404.html` and sets basic headers.
4. Custom domains → add the domain and the TXT or CNAME record Azure shows.
5. Azure provisions the certificate after the domain validates.

## Pre-launch checklist

- Logo, name, and “Senior Full Stack Developer” match on the home page, project pages, privacy page, and 404 page.
- Layout checked at 360px, 768px, 1280px, and a wide desktop.
- Mobile menu opens, closes, and moves focus. Escape closes it.
- Theme toggle switches and survives a reload. A first visit with no saved choice follows the system theme.
- Each category filter and the professional/concept filter show the matching cards.
- Every “View case study” link opens the correct file.
- WhatsApp, email, phone, and LinkedIn URLs are correct.
- Contact form: empty submit shows field errors; a configured endpoint shows success only after a real 2xx response; a bad endpoint shows the error and the email fallback; an empty endpoint does not claim the message was sent.
- No broken image paths.
- Sitemap and canonical URLs use the live domain.
- No secrets in JavaScript.
- No invented testimonials, certifications, client logos, or performance claims.
- `pricing.showRates` is still `false` unless the numbers are final.

## Stack

HTML, CSS, and vanilla JavaScript. Self-hosted Inter and IBM Plex Mono (SIL Open Font License; see `assets/fonts/`).

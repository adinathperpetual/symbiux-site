# Symbiux — self-hosted clone

A standalone copy of **symbiux.lovable.app** that runs entirely from local files.
Nothing is fetched from `lovable.app`, Google Fonts, or any CDN at runtime.

## Run locally

Requires Node.js 16+ (no `npm install` needed — the server has zero dependencies).

```bash
node server.js            # http://localhost:8080
PORT=3000 node server.js  # custom port
```

Or serve the `public/` folder with any static host (nginx, Apache, Netlify, Vercel,
GitHub Pages, S3, cPanel `public_html`, `npx serve public`, `python3 -m http.server -d public`).
The site is a single page, so no rewrite rules are required.

## Layout

```
public/
  index.html              pre-rendered page (hydrates into the React app)
  assets/index-*.js       app + framework bundles (TanStack Start / React)
  assets/styles-*.css     Tailwind build
  assets/fonts.css        local @font-face rules (Inter 400/500/600, Space Grotesk 400–700)
  assets/fonts/*.woff2    font files (latin + latin-ext, from @fontsource, OFL licensed)
  assets/hero-bg-*.jpg, logo.jpg, favicon.png, robots.txt
server.js                 static server with caching headers + SPA fallback
```

## Changes from the original export

- The Google Fonts `<link>` and two `preconnect` tags were replaced by `/assets/fonts.css`
  in both `index.html` and the router `head()` config inside `assets/index-CFR8YE9c.js`
  (so React hydration doesn't re-inject the Google link).
- Two hover effects that were defined in the original build but never rendered were fixed
  with a small CSS block appended to the end of `assets/styles-Dx2-Micj.css`
  (marked `clone fixes`):
  1. Glass cards (problem cards, case studies) with `hover:border-primary/40|50` — an unlayered
     `.glass{border-color}` rule was overriding Tailwind's layered hover utilities.
  2. Solution cards' 4px hover lift — Framer Motion leaves an inline `transform:none` after the
     reveal animation, which cancelled the CSS `:hover` transform. The lift now uses the
     independent `translate` property and is skipped under `prefers-reduced-motion`.
- No other code was modified. The original export contained no references to
  `lovable.app`, no server functions, no API calls and no analytics.

## Outbound links (user clicks only, never auto-loaded)

WhatsApp (`wa.me/919270286339`), `mailto:symbiuxofficial@gmail.com`, `tel:+919270286339`,
and the case-study sites `makeuca.com` and `nutricfood.in`.

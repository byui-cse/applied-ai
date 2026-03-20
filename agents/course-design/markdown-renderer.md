# Role

You are a highly talented UI/UX designer and web design and developer who specializes in delivering well formatted, clean, and easy-to-navigate content to the user.

# Task

Your **task** is to build a dynamic website (only in HTML/JS/CSS, static only with no server), which will render any of the markdown pages listed inside of the content/ folder. 

## Style

Design System Instructions: 2026 Magazine/Editorial Framework

# Modern Newspaper Web Design: 2026 Design System

---

## Philosophy & Aesthetic Direction

The 2026 newspaper aesthetic fuses the **authority of print heritage** with the
**breathability of editorial minimalism**. The guiding tension: density that never
feels cluttered, whitespace that never feels empty. Think the *Financial Times*
meets a Scandinavian design studio — credible, restrained, precise.

---

## Typography

### Type Scale
The typographic system is built on **two contrasting typefaces** — a **serif display**
for headlines and a **humanist sans-serif** for body and UI. This contrast is
non-negotiable; it creates the editorial identity.

- **Display / Headline**: A high-contrast editorial serif — `Playfair Display`,
  `Freight Display`, `Canela`, or `GT Alpina`. Weights: 400 (italic for features),
  700 (breaking news), 300 (longform). Used at aggressive sizes.
- **Body / UI**: A legible, low-contrast sans — `Söhne`, `Neue Haas Grotesk`,
  `Aktiv Grotesk`, or `Switzer`. Never Inter, never Roboto.
- **Monospaced accent**: `JetBrains Mono` or `IBM Plex Mono` for timestamps,
  section labels, data labels, and live tickers. Used sparingly.

### Type Sizes (fluid, clamp-based)
| Role              | Size              | Weight | Leading |
|-------------------|-------------------|--------|---------|
| Hero Headline     | 64–96px           | 700    | 1.0–1.05 |
| Section Headline  | 36–52px           | 700    | 1.1 |
| Card Headline     | 20–28px           | 600    | 1.2 |
| Body Copy         | 17–19px           | 400    | 1.65–1.75 |
| Byline / Label    | 11–13px           | 500    | 1.4 |
| Caption           | 12px              | 400    | 1.5 |

### Type Rules
- Headline kerning is **tight to very tight** (`letter-spacing: -0.02em` to `-0.04em`).
- Body copy uses **generous leading** (1.65–1.75) and **max-width: 65–72ch** for
  optimal reading columns.
- ALL CAPS labels use `letter-spacing: 0.08em–0.12em` and are set in the sans at 11–13px.
- **No bold body text** — emphasis is achieved through *italic* or color contrast alone.
- Section labels use a **hairline horizontal rule** above or below them.

---

## Color

### Base Palette
The palette is near-neutral with one **editorial accent**. Not dark mode everywhere —
newspapers live in **warm off-white**, not pure white.

# Steps

1. Create a single index.html file. This will be the entry point. This will be rendered from Github Pages.
2. Create a folder for styles and js files, and finally one for images.
3. Create the index.html HTML structure. Use query params for the actual page, for exmaple https://byui-cse.github.io/applied-ai?page=content/phase-1/week-1/day-1.md
4. Create the styles.css and link it up to the index.html based on the style design system defined above
5. Create the javascript file to perform the rendering and any other smooth interaction.
6. Create a scripts/server.py to run this file locally

## Implementation notes (repo)

- **Layout:** `index.html` (entry), `styles/styles.css`, `js/app.js`, `images/` (assets).
- **Routing:** `?page=content/phase-1/week-1/day-1.md` (default: `content/syllabus.md`).
- **Manifest:** `content/manifest.json` lists all `.md` files for the Browse sidebar and FAB. Regenerate when you add or remove pages, e.g.  
  `find content -name '*.md' | sort | python3 -c 'import json,sys; print(json.dumps({"pages": [l.strip() for l in sys.stdin if l.strip()]}, indent=2))' > content/manifest.json`

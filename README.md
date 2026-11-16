# Bāyit Bagels - website rebuild

Static site: plain HTML, one stylesheet, one small script, no framework. Keeps the original Readymag look (palette, light mono type, pencil bagels, wordmark, hairline rules, line map) and adds what the site was missing. The evaluation that drove it is in [../site-evaluation/REPORT.md](../site-evaluation/REPORT.md).

## Pages

| URL | File | Notes |
|---|---|---|
| `/` | `index.html` | Hero with hover/tap photo reveal, 3-day process, photos, favourites, festive band, story, stats, suppliers, Instagram, visit |
| `/menu/` | `menu/index.html` | Full menu (prices word for word from the live site), dietary filter, glossary |
| `/cateringwholesale/` | `cateringwholesale/index.html` | Services, how it works, festive, enquiry form, FAQ |
| `/suppliers/` | `suppliers/index.html` | All supplier copy from the live site + allotment, foraging |
| `/findus/` | `findus/index.html` | Line map, hours with today highlighted, directions |
| 404 | `404.html` | |

URLs match the live site so Google rankings carry over. `vercel.json` redirects the old `/s4/` and `/bayitbagels/` addresses.

## Edit and preview

Page content lives in `_src/pages/*.html`; the shared header, footer, meta tags and schema live in `_src/build.py`. After editing:

```bash
python "Clients/Bayit/website/_src/build.py"
```

```bash
python -m http.server 4321 --directory "Clients/Bayit/website"
```

Then open http://localhost:4321. (Opening the HTML files directly won't work - links and assets use root paths.) `_screens/` holds QA screenshots and can be deleted.

## Deploy

Push the `website/` folder to a GitHub repo and import it in Vercel (no build step, output = root). Then point bayithospitality.co.uk's DNS at Vercel and cancel the Readymag plan. Do this only once Oli has approved.

## Confirm with Oli before going live

These are written from the call research, not from the live site:

1. **The 3-day process copy** (Mix / Rest / Boil & bake) - the general steps are right, the wording needs Oli's eye.
2. **The story section** - siblings, Oli's decade in kitchens (London, New Zealand, Italy), opening in Feb 2025. From The Argus.
3. **Festive catering items** (party platters, salmon & schmear bar, office buffets, sweet treats) - from their Instagram. Add real items and prices when he sends the festive menu.
4. **Delivery** - the site says collection first, delivery "please ask". Check what he actually offers.
5. **Photo captions** on the home page and the person in the foraging photo.
6. **Stats** ("9 producers" counts the 9 named suppliers on the menu and suppliers page).
7. Optionally add **Google rating and Argus press quotes** - left out until we have the exact wording.

## Known limits / next steps

- **The enquiry form opens the visitor's email app** with everything filled in (no server). It works today, but some people don't have a mail app set up. Next step: post it to Formspree or Supabase, or better, replace it with the **Bāyit Orders** system (lead time, daily caps, Stripe deposit, prep list) from the call-prep offer.
- **Fonts:** the live site uses a licensed Type Today mono. This uses DM Mono Light (free) as a very close stand-in. If louisthings can share the licence, swap it in `_src/build.py` and `assets/css/styles.css`.
- **Photos:** all images come from the current site. More food photos from their Instagram would make it stronger - ask Oli for originals.

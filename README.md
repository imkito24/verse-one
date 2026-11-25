# VERSE ONE 2.1 — local open-source pilot

This is a working local reading/search prototype, with a basic single-screen presentation mode, not a published site or a production church presentation system. No accounts, subscriptions or paid APIs are required. Scripture is imported, never generated.

## Start on a computer

1. Extract the entire ZIP.
2. Install Python 3 if it is not already present.
3. Open a terminal in the extracted `verse-one-2` folder.
4. Run `python3 serve.py` (Windows: `py serve.py`).
5. Open http://127.0.0.1:8080/ in a modern browser.
6. Click **Install for offline** for each desired edition. All source packs are already in this ZIP; installation copies them to browser storage and checks their checksum.
7. Wait for the application shell status to say cached; reload once. Then disconnect the network or stop the server and test an installed edition.

Opening `index.html` directly from Files, an email preview or a `file://` URL will not run module workers or service workers correctly. This package does not provide an iPhone-accessible live URL. iPhone installation requires a separately approved HTTPS deployment or a trusted HTTPS local setup. Do not expose the local server to the public internet.

The launcher binds only to 127.0.0.1. Use the same browser profile, hostname and port to retain the installed data. Browser deletion, private browsing or storage eviction can remove it. Local proof-of-concept storage is not encrypted and should not contain confidential sermons.

## Reading and searching

- Select a book/chapter or enter `John 3:16-18`, `Jn 3:16`, or a publisher-provided native book name/abbreviation.
- Select **All words** for a whole-token AND search. Select **Exact phrase**, or quote a phrase, for an exact normalized substring within one source verse unit.
- Search normalization uses NFC, lowercase, whitespace consolidation, joiner-insensitive matching and equivalent Malayalam chillu forms. These operations apply to the search index, never to displayed Scripture.
- Cross-chapter ranges, fuzzy spelling, transliteration and cross-verse phrases are not supported in this pilot.
- Reference bridges return their full source unit, with its original number label. Empty source entries are visibly explained, never filled from another translation.
- Source notes can be expanded under a verse. Font size is adjustable.
- Search uses a dedicated worker and a prebuilt per-edition index. Changing queries invalidates older results.

## Basic presentation

After installing an edition, click **Present verse** below a verse. Use previous/next within the same chapter, change the theme, or enter fullscreen where the browser permits. The source reference and attribution stay visible. This is single-screen presentation, not remote casting.

## Evidence

Open `dist/integrity.html` through the local server or inspect `reports/validation.json`. Every shipped verse-body string is compared to a separately parsed USFM export; USFX supplies the reader pack. Every source book/chapter/verse-label inventory is checked. All six scoped editions contain 66 books and 1,189 chapters. “Source-compared” means preservation of these pinned publisher exports, not an independent scholarly certification.

Verse-unit totals differ: English 31,103; Malayalam 31,102; Hindi 31,104; Marathi 31,087; Tamil 31,103; Telugu 31,004. Do not compare these counts to KJV as a completeness test. Five English units have no verse-body text in both exports. English USFX includes extra books not selected for this Protestant collection; those are listed in the report.

Original archives, metadata, copyright notices, per-edition inventories and SHA-256 hashes are included. The source date is the downloaded edition's metadata; the retrieval date is 15 November 2026 IST. The two exports come from the same publisher. Their agreement is strong import evidence, not independent evidence that the publisher has no errors. Translation-to-translation verse alignment has not been certified.

## Rebuild and test

Requires Python 3.10+ and Node.js 22+. No npm dependencies.

```
python3 scripts/build_library.py
node scripts/index.mjs
python3 scripts/report.py
python3 tests/integrity_test.py
node --test tests/core.test.mjs
```

Do not replace `sources/` files casually. The source lock is pinned. A new upstream release requires a reviewed source diff, metadata/licensing check, exception review, then regeneration of the lock and pack catalog. Archived publisher signatures are retained but were not cryptographically authenticated against an independently trusted key in this phase.

The parser fails on unrecognized XML elements and duplicate USFM verse labels. Conversion consolidates layout whitespace, separates notes/headings, and omits lexical markup from the reader. Poetry/paragraph typography, front matter and some metadata are not fully rendered. Original archives preserve them.

## Scope not implemented

No remote or separate-screen church projector controls, dual-language projection, sermon playlists, cloud sync, login, user management, automatic publisher updates, additional canons or commercial translations. These belong to later authorized phases. KJV and ASV are not included. The current application interface is English; Scripture and source book labels support six languages.

## Before any deployment

Publishing is not authorized by this package. A private pilot requires real server/edge authentication protecting every route and data asset, including alternate deployment hostnames. Never substitute robots.txt, an obscure URL or a JavaScript password. Local downloaded content cannot be remotely revoked instantly. Keep sensitive church records separate.

For an approved deployment: serve `dist/` on HTTPS; add CSP and standard security headers compatible with module workers; protect the origin; test auth and cache boundaries; exclude `qa-mobile.html`; verify all packs and licenses; test iOS Safari, Android Chrome, storage pressure and fresh offline launch. Service-worker updates take effect after older tabs close. Invalidate caches only with a reviewed version change; preserve the previous working installation until the new one is ready.

## Costs

The six selected text licenses require no royalty payment under their published terms. Local use costs no hosting fee. A future small static pilot may fit a free hosting tier; private access, domain registration, larger storage and maintenance depend on the chosen provider. Nothing was purchased or published.

## Rights

English WEBP is public domain; its name identifies a faithful copy of the source edition. The five Indian Revised Version texts are CC BY-SA 4.0, with ownership and source notices in `dist/licenses/`. Converted IRV data contributions are also CC BY-SA 4.0. No endorsement is implied. See `LICENSE.txt` for software terms and the integrity report for data attribution.

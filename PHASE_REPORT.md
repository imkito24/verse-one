# VERSE ONE 2.0 — completed foundation phase

Six locally searchable Scripture editions imported from official eBible USFM and USFX archives. 31 automated tests pass. The application remains unpublished, with no private account access or purchases.

| Language | Edition | Books | Chapters | Source verse units |
|---|---|---:|---:|---:|
| English | WEBP | 66 | 1189 | 31,103 |
| Malayalam | IRVMAL | 66 | 1189 | 31,102 |
| Hindi | IRVHin | 66 | 1189 | 31,104 |
| Marathi | IRVMar | 66 | 1189 | 31,087 |
| Tamil | IRVTam | 66 | 1189 | 31,103 |
| Telugu | IRVTel | 66 | 1189 | 31,004 |

All 186,503 imported verse units were compared with the source exports; there are zero unexplained verse-body differences after the documented whitespace/markup conversion. This verifies the import against those sources, not the underlying translation against original manuscripts. Five English source entries have empty verse bodies, preserved and explained. Verse bridges and edition differences are retained. The scope is 66 Protestant books, not all Christian canons.

## Built

- Responsive reading room and six local edition packs.
- Reference, verse-range, native-book-name, keyword and phrase search.
- Prebuilt indexes and a dedicated search worker.
- Checksum-verified, transactional browser installation.
- Cached application shell and offline-capable local data access.
- Source attribution, original archives, licensing notices and machine-readable per-edition reports.
- Reproducible build scripts, local launcher and tests.

## Validation

Five Python integrity tests and 26 JavaScript tests pass. These cover source fingerprints, every imported verse body, every available reference, native aliases, ranges, corrupted-pack rejection, ambiguous references, phrase search and sampled index/full-scan agreement. Modern Malayalam chillu forms are handled in search only; display text is unchanged.

Browser checks confirmed English installation, reference ranges, phrase results, Malayalam installation/rendering and the cached-shell status. A final browser check could not continue after the session interruption. Physical iPhone/Android testing, narrow-screen visual signoff, actual disconnected cold restart, quota exhaustion and interrupted-update browser testing remain pending. These are explicitly NOT reported as passed.

## Still outside this approved phase

Full church presentation controls, dual-language projection, sermon playlists, private hosting/login and production certification. No public or private live website has been deployed. The app interface is English; Scripture is in six languages.

## Open locally

Extract `VERSE_ONE_2_Foundation.zip`, open a terminal in `verse-one-2`, and run `python3 serve.py` (Windows: `py serve.py`). Open `http://127.0.0.1:8080/` on that computer. Do not open index.html directly in an iPhone file preview. A phone-accessible HTTPS site requires a separately approved deployment.

All needed Scripture packs are in the ZIP. Install the editions you need using the app. Keep the same browser profile and address. Browser clearing/eviction can remove offline data.

## Rights and costs

WEBP is public domain. Malayalam, Hindi, Marathi, Tamil and Telugu IRV texts are CC BY-SA 4.0 with the original notices included. Conversion contributions to IRV data use the same license. No text royalty, hosting charge or service purchase was incurred. Local operation is free. Future hosting, access controls and domains depend on the selected provider. No guarantee of permanent free hosting is made.

See `README.md`, `dist/integrity.html`, and `reports/` in the package for source URLs, hashes, numbering exceptions, exclusions, test output and deployment constraints.

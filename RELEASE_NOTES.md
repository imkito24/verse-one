# VERSE ONE 2.1 — GitHub preparation (2026-11-25)

Recovered the previous 2.0 Foundation source archive and retained all six editions, original pinned archives, publisher notices, rebuild scripts and tests. Added a single-screen verse presentation dialog, light/dark theme, previous/next nonempty verse navigation within the chapter, fullscreen request where supported and persistent source attribution. No translation content or data checksums were modified. CONTRIBUTING.md and .gitignore added. Software remains MIT; translation licenses remain separate. The earlier PHASE_REPORT.md and historical QA reports describe version 2.0, not the new presentation implementation.

## Current checks

- Python source integrity: 5/5 passed (including every shipped verse-body comparison against archived USFM and source SHA-256 locks).
- Node search tests: 26/26 passed.
- JavaScript syntax: app and service worker passed Node syntax checks.
- Browser integration: not completed. Local server port was occupied and Chromium navigation was blocked by administrator policy. The new presentation mode, offline cold reload, fullscreen and physical iOS/Android behavior are not certified. Prior foundation checks are recorded in PHASE_REPORT.md. No deployment or GitHub changes made.

## Upload

Extract the ZIP. Upload the *contents* of the verse-one-2 folder to the repository root, preserving directories. Do not upload the ZIP itself as the only project file. Existing README.md can be replaced with the supplied technical README; the supplied LICENSE.txt explains the software and separate data license scope. Keep the repository private until rights, testing and publication are reviewed. Desktop GitHub web upload or Git CLI is recommended because this archive has nested directories. The application requires a localhost HTTP server or HTTPS hosting; Files preview is not a runnable app. No premium subscription eligibility is implied.

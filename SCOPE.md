# Print Scope — Part C Addendum PDF

**As of: 2026-08-07.** This note records the deliverable scope of the published PDF (`ies-report.pdf`) for the IES Task Force closure submission, per the Chief Architect's direction of 2026-08-05: the PDF is the Part C addendum to the Task Force white paper — deliverable material only, scrubbed for the public/media surface. Nothing has been deleted from this repository or the GitBook; pages are either excluded from the print scope or moved to the clearly-labelled [`draft/`](draft/README.md) section.

## Mechanism

The PDF is built from **`SUMMARY.print.md`** — a curated print manifest consumed by `scripts/build_pdf.py` and independently re-verified by `scripts/verify_pdf.py`. The GitBook navigation (`SUMMARY.md`, via `.gitbook.yaml`) is unchanged in behaviour and continues to publish the full documentation. PDF title: **"India Energy Stack (IES) — Technical Documentation"**.

**Current build: 126 pages** (target ~100–150).

## In the PDF

1. Home
2. Glossary
3. FAQ
4. **What IES Provides** — Overview, Register, Discover, Exchange, Verifiable Credentials, **Security** (new page), Schemas Overview (landing page)
5. **Use Case Overviews** — finalised (Piloted) only: Overview, Consumer Energy Passport, Consumer Meter Digest, Smart Meter Data Exchange, DER Visibility
6. **Appendix — Schemas Reference** — every schema family from `schemas/` at its latest version, plus External Schemas

## Out of the PDF (unchanged in the GitBook)

- **How you implement IES** (Setup Register, Issue Credentials, DigiLocker, Setup Exchange, Build Adapter, Conformance) — developer manual
- **Use Case Implementation Guides** (`use-cases/`) — developer builds
- **IES Schemas (developer)** (`schemas-ies/`) — generated developer mirror of the appendix
- **Schemas Overview per-family subpages** — deep-dive pages duplicating appendix field detail; the landing page prints, the families print in full in the appendix
- **P2P Energy Transaction** (overview + guide) — status "In progress", not finalised
- **Status, Pathways, Propose a Schema, Download PDF, Contributors** — site-only / self-referential pages

## Moved to `draft/` (excluded from the PDF, labelled WIP in the GitBook)

- DISCOM Regulatory Filing (WIP) — overview → `draft/use-cases-overview/discom-regulatory-filing.md`, guide → `draft/use-cases/discom-regulatory-filing/`
- Policy as Code (WIP) — overview → `draft/use-cases-overview/tariff-intelligence.md`, guide → `draft/use-cases/tariff-intelligence/`

Both now sit under a **Draft (Work in Progress)** section of the GitBook navigation, behind [`draft/README.md`](draft/README.md), which states that nothing in the section is part of the deliverable.

## WIP / Draft flags applied

- **MeterDataRequestCredential v0.1** — "(Draft)" in navigation titles; ⚠️ DRAFT banner added to `schemas/MeterDataRequestCredential/README.md` and `v0.1/README.md`
- **OutageNotification v0.1** — "(Draft)" in navigation titles; already carried ⚠️ WORK IN PROGRESS banners on both pages
- **ArrFiling v0.5** — remains in the appendix at its existing "Draft for technical review" status (its field reference is complete); its parent use case is in `draft/`
- Use Case Overviews table labels DISCOM Regulatory Filing and Policy as Code 🚧 WIP and P2P Energy Transaction "In progress"

## Media scrub

All in-scope pages were checked for present-tense "live / running / active / in production / deployed" claims against **STATUS.md** (which controls). Pilot activity is uniformly described as the completed, dated 30-day DISCOM Challenge, deferring to STATUS.md for current-status representations. One overclaim was softened (OutageNotification overview: "a live system of record" → "a real DISCOM system of record"). STATUS.md itself is not in the print scope; PDF pages cite it by name as the repository's current-status page.

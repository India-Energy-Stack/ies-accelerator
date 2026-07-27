# Status

**As of: 2026-07-26.**

This page is the single source for claims about whether IES, its sandbox, or any pilot is currently active. Other pages in this GitBook describe the 30-day DISCOM Challenge and other pilot activity as historical, completed events, and link here rather than re-asserting a present-tense status of their own. If a page's wording and this page ever disagree, this page controls.

---

## What repository evidence supports, as of this date

- **The specifications are published.** The schemas, JSON-LD contexts, RDF vocabularies and worked example payloads under `schemas/` are checked into this repository and rendered as this GitBook.
- **The specifications are checkable.** The validator scripts under `scripts/` (and the per-family validators, e.g. `schemas/MeterData/v0.6/validation/`) run against the shipped examples and can be re-run by anyone who clones the repository.
- **A completed, historical pilot.** Four pilot DISCOMs — PVVNL, APEPDCL, DGVCL and Tata Power — each built an IES adapter and completed a 30-day IES DISCOM Challenge, demonstrating a first set of use cases (DER Visibility, Consumer Energy Passport, Consumer Meter Digest, Smart Meter Data Exchange) against the IES specifications and the pilot sandbox. This is recorded in [Pilots and status](README.md#pilots-and-status) and [Contributors](contributors.md). It is a dated, completed event, not a description of anything running today.

## What this repository does not establish

This repository contains no dated, owner-maintained evidence that, as of the as-of date above:

- the pilot sandbox is currently running or reachable;
- any of the four pilot DISCOMs is currently building in, or exchanging data through, the sandbox; or
- any IES use case is in current production use by any organisation.

**On DER Visibility specifically:** the Challenge recorded DER Visibility as one of the four demonstrated use-case outcomes (see [Pilots and status](README.md#pilots-and-status)). This repository does not establish *how* that outcome was produced — in particular, it does not establish that a PII-free, per-feeder aggregate was issued and validated as an ElectricityCredential v1.2 payload. A pilot DISCOM demonstrating "DER Visibility" as an outcome is not, by itself, proof of that specific schema claim; see [DER Visibility §1](use-cases-overview/der-visibility.md#id-1.-scope-and-purpose) for what is executable today versus illustrative. Absent dated, owner-maintained evidence of the exact implementation path used during the Challenge, this page does not assert one.

Other pages in this GitBook should not be read as making any of these claims unless they cite dated, owner-maintained evidence for the specific date in question. Absent such evidence, treat any undated "live", "running" or "active" wording elsewhere in this GitBook as referring to the historical Challenge outcome above, not to the present day.

## What "demonstrated in pilot" meant during the Challenge

Each of the four use cases listed above had to clear the same evidentiary bar to count as demonstrated:

1. the DISCOM's adapter was running;
2. its `did:web` identity was resolvable;
3. its subscriber record was present in the network registry;
4. it produced an issued credential or a completed exchange; and
5. that result was independently verified by a counterparty.

That bar describes what was verified during the dated 30-day Challenge. It is not a claim that the same adapters, registrations or exchanges are still active today.

## Keeping this page current

This page is maintained separately from the narrative chapters and is updated by the repository owner when there is verifiable evidence to add or correct. If you are relying on this GitBook for a current-status representation (e.g. in a filing or a partner evaluation), cite this page and its as-of date, not the narrative chapters.

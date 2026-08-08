# Print manifest — deliverable PDF scope

<!--
  This file defines the PRINT SCOPE of the published PDF (ies-report.pdf),
  consumed by scripts/build_pdf.py and independently re-parsed by
  scripts/verify_pdf.py. It is NOT the GitBook navigation — that stays in
  SUMMARY.md (see .gitbook.yaml). Same grammar as SUMMARY.md: canonical
  starred title-plus-path list entries with even-space indentation.

  Scope policy (IES Task Force closure, Aug 2026): the PDF is the formal
  Part C addendum to the Task Force white paper — deliverable material only.
  Developer implementation manuals (how-you-implement-ies/, use-cases/,
  schemas-ies/), site-only pages (Propose a Schema, Download PDF, Pathways,
  Status, Contributors), draft/ content, and any use case not finalised
  (P2P Energy Transaction — in progress) are deliberately NOT listed here.
  They remain in the GitBook; they are not printed. Entries under schemas/
  are pulled into the trailing "Appendix — Schemas Reference". -->

* [Home](README.md)
* [Reference Material](print/reference-material.md)

## What IES Provides

* [Overview](what-ies-provides/README.md)
* [Register](what-ies-provides/register.md)
* [Discover](what-ies-provides/discover.md)
* [Exchange](what-ies-provides/exchange.md)
* [Verifiable Credentials](what-ies-provides/energy-credentials/README.md)
* [Security](what-ies-provides/security.md)
* [Schemas Overview](what-ies-provides/schemas-overview/README.md)

## Use Case Overviews

* [Overview](use-cases-overview/README.md)
* [Consumer Energy Passport](use-cases-overview/consumer-energy-passport.md)
* [Consumer Meter Digest](use-cases-overview/consumer-meter-digest.md)
* [Smart Meter Data Exchange](use-cases-overview/smart-meter-data-exchange.md)
* [DER Visibility](use-cases-overview/der-visibility.md)

## Appendix — Schemas Reference

* [ElectricityCredential](schemas/ElectricityCredential/README.md)
  * [v1.2](schemas/ElectricityCredential/v1.2/README.md)
* [MeterData](schemas/MeterData/README.md)
  * [v0.6](schemas/MeterData/v0.6/README.md)
* [MeterDataCredential](schemas/MeterDataCredential/README.md)
  * [v0.6](schemas/MeterDataCredential/v0.6/README.md)
* [MeterDataRequest](schemas/MeterDataRequest/README.md)
  * [v0.6](schemas/MeterDataRequest/v0.6/README.md)
* [MeterDataRequestCredential](schemas/MeterDataRequestCredential/README.md)
  * [v0.1](schemas/MeterDataRequestCredential/v0.1/README.md)
* [ArrFiling (WIP)](schemas/ArrFiling/README.md)
  * [v0.5](schemas/ArrFiling/v0.5/README.md)
* [OutageNotification (WIP)](schemas/OutageNotification/README.md)
  * [v0.1](schemas/OutageNotification/v0.1/README.md)
* [External Schemas](schemas/external/README.md)

## Back matter

<!-- Printed after the schemas appendix (BACK_MATTER_PATHS in build_pdf.py);
  the "Reference Material" page after Home points readers here. -->

* [Glossary](glossary.md)
* [FAQ](faq.md)

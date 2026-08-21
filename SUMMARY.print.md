# Print manifest — deliverable PDF scope

<!--
  This file defines the PRINT SCOPE of the published PDF (ies-report.pdf),
  consumed by scripts/build_pdf.py and independently re-parsed by
  scripts/verify_pdf.py. It is NOT the GitBook navigation — that stays in
  SUMMARY.md (see .gitbook.yaml). Same grammar as SUMMARY.md: canonical
  starred title-plus-path list entries with even-space indentation.

  Scope policy (technical-reference refactor, Aug 2026): the PDF mirrors the
  refactored GitBook — the technical reference a reader needs to understand
  and build on IES. Site-only pages (Propose a Schema, Pathways) and draft/ content
  are deliberately NOT listed here. Entries under schemas/ are pulled into the
  trailing "Appendix — Schemas Reference". -->

* [Getting Started](README.md)

## Schemas Overview

* [Schemas Overview](what-ies-provides/schemas-overview/README.md)
  * [ElectricityCredential](what-ies-provides/schemas-overview/electricity-credential.md)
  * [MeterData](what-ies-provides/schemas-overview/meter-data.md)
  * [MeterDataCredential](what-ies-provides/schemas-overview/meter-data-credential.md)
  * [MeterDataRequest](what-ies-provides/schemas-overview/meter-data-request.md)
  * [MeterDataRequestCredential](what-ies-provides/schemas-overview/meter-data-request-credential.md)
  * [ArrFiling](what-ies-provides/schemas-overview/arr-filing.md)
  * [OutageNotification (WIP)](what-ies-provides/schemas-overview/outage-notification.md)

## Use Case Overviews

* [Consumer Energy Passport](use-cases-overview/consumer-energy-passport.md)
* [Consumer Meter Digest](use-cases-overview/consumer-meter-digest.md)
* [Smart Meter Data Exchange](use-cases-overview/smart-meter-data-exchange.md)
* [DER Visibility](use-cases-overview/der-visibility.md)
* [P2P Energy Transaction](use-cases-overview/p2p-energy-trading.md)

## Use Case Implementation Guides

* [Consumer Energy Passport](use-cases/consumer-energy-passport/README.md)
* [Consumer Meter Digest](use-cases/consumer-meter-digest/README.md)
* [Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md)
  * [IES Meter Data Model](use-cases/smart-meter-data-exchange/ies-meter-data-model.md)
* [DER Visibility](use-cases/der-visibility/README.md)
* [P2P Energy Transaction](use-cases/p2p-energy-trading/README.md)

## Concepts

* [Before you build](how-you-implement-ies/README.md)
* [Setting up Register](how-you-implement-ies/setup-register.md)
  * [Register & Identifiers in depth](what-ies-provides/register.md)
* [Setting up Discover & Exchange](how-you-implement-ies/setup-exchange.md)
  * [Discover in depth](what-ies-provides/discover.md)
  * [Exchange in depth](what-ies-provides/exchange.md)
* [Issuing Credentials](how-you-implement-ies/issue-credentials.md)
  * [Verifiable Credentials in depth](what-ies-provides/energy-credentials/README.md)
  * [DigiLocker delivery](how-you-implement-ies/digilocker.md)
* [Build your Internal-facing Adapter](how-you-implement-ies/build-adapter.md)
* [Security Model](what-ies-provides/security.md)
* [Conformance Checklist](how-you-implement-ies/conformance.md)

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

# Table of contents

* [Home](README.md)
* [Status](STATUS.md)
* [Glossary](glossary.md)
* [FAQ](faq.md)
* [Propose a Schema](propose-a-schema.md)
* [Download PDF](download-pdf.md)

## What IES Provides

* [Overview](what-ies-provides/README.md)
* [Register](what-ies-provides/register.md)
* [Discover](what-ies-provides/discover.md)
* [Exchange](what-ies-provides/exchange.md)
* [Verifiable Credentials](what-ies-provides/energy-credentials/README.md)
* [Schemas Overview](what-ies-provides/schemas-overview/README.md)
  * [ElectricityCredential](what-ies-provides/schemas-overview/electricity-credential.md)
  * [MeterData](what-ies-provides/schemas-overview/meter-data.md)
  * [MeterDataCredential](what-ies-provides/schemas-overview/meter-data-credential.md)
  * [MeterDataRequest](what-ies-provides/schemas-overview/meter-data-request.md)
  * [MeterDataRequestCredential](what-ies-provides/schemas-overview/meter-data-request-credential.md)
  * [ArrFiling](what-ies-provides/schemas-overview/arr-filing.md)
  * [OutageNotification](what-ies-provides/schemas-overview/outage-notification.md)

<!-- HIDDEN FROM GITBOOK — do not un-comment without reading this note.

GitBook publishes exactly what SUMMARY.md lists, so commenting this section
out removes it from the site navigation while every file stays in the repo
(and on GitHub Pages, where the canonical schema URLs are served). The
developer-facing "IES Schemas" section below is what readers browse instead.

The PDF build is deliberately unaffected: scripts/build_pdf.py — and the
independent grammar in scripts/verify_pdf.py — match entries line by line and
do not track HTML comments, so the printed guide keeps its full schema
appendix. Teaching either parser about comments would silently drop those
chapters from the PDF.

Known consequence: in-book relative links to schemas/… (from pathways/,
use-cases/, what-ies-provides/ and schemas-ies/) now point at pages GitBook
does not publish, and will 404 on the site until they are repointed.

## Schemas

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
* [ArrFiling](schemas/ArrFiling/README.md)
  * [v0.5](schemas/ArrFiling/v0.5/README.md)
* [OutageNotification](schemas/OutageNotification/README.md)
  * [v0.1](schemas/OutageNotification/v0.1/README.md)
* [External Schemas](schemas/external/README.md)

(end of hidden Schemas section — this closing line must not begin with a
bullet character, or the strict SUMMARY grammar in scripts/verify_pdf.py
rejects it) -->

## IES Schemas (developer)

* [All schemas](schemas-ies/README.md)
* [ElectricityCredential](schemas-ies/ElectricityCredential.md)
* [MeterData](schemas-ies/MeterData.md)
* [MeterDataCredential](schemas-ies/MeterDataCredential.md)
* [MeterDataRequest](schemas-ies/MeterDataRequest.md)
* [MeterDataRequestCredential](schemas-ies/MeterDataRequestCredential.md)
* [ArrFiling](schemas-ies/ArrFiling.md)
* [OutageNotification](schemas-ies/OutageNotification.md)
* [External Schemas](schemas-ies/external.md)

## How you implement IES

* [Overview](how-you-implement-ies/README.md)
* [Setup Register](how-you-implement-ies/setup-register.md)
* [Issue Credentials](how-you-implement-ies/issue-credentials.md)
  * [DigiLocker delivery](how-you-implement-ies/digilocker.md)
* [Setup Exchange](how-you-implement-ies/setup-exchange.md)
* [Build your Internal-facing Adapter](how-you-implement-ies/build-adapter.md)
* [Conformance Checklist](how-you-implement-ies/conformance.md)

## Use Case Overviews

* [Overview](use-cases-overview/README.md)
* [Consumer Energy Passport](use-cases-overview/consumer-energy-passport.md)
* [Consumer Meter Digest](use-cases-overview/consumer-meter-digest.md)
* [Smart Meter Data Exchange](use-cases-overview/smart-meter-data-exchange.md)
* [DER Visibility](use-cases-overview/der-visibility.md)
* [DISCOM Regulatory Filing (WIP)](use-cases-overview/discom-regulatory-filing.md)
* [Policy as Code (WIP)](use-cases-overview/tariff-intelligence.md)
* [P2P Energy Transaction](use-cases-overview/p2p-energy-trading.md)

## Use Case Implementation Guides

* [Overview](use-cases/README.md)
* [Consumer Energy Passport](use-cases/consumer-energy-passport/README.md)
* [Consumer Meter Digest](use-cases/consumer-meter-digest/README.md)
* [Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md)
  * [IES Meter Data Model](use-cases/smart-meter-data-exchange/ies-meter-data-model.md)
* [DER Visibility](use-cases/der-visibility/README.md)
* [DISCOM Regulatory Filing (WIP)](use-cases/discom-regulatory-filing/README.md)
* [Policy as Code (WIP)](use-cases/tariff-intelligence/README.md)
* [P2P Energy Transaction](use-cases/p2p-energy-trading/README.md)

## Pathways

* [Overview](pathways/README.md)
* [Authority / Regulator Pathway](pathways/authority.md)
* [Utility Pathway](pathways/utility.md)
* [Technology Service Provider Pathway](pathways/tsp.md)
* [Researcher / Analyst Pathway](pathways/researcher.md)
* [Secretariat Pathway](pathways/secretariat.md)

## Contributors

* [Contributors](contributors.md)

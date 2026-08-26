<!-- Issue body: proposal for MeterData v0.7 (additive). The PR that implements it links here. -->

# Proposal: MeterData v0.7 — itemised bill components on `BILL_DETAILS` (additive)

**Type:** schema change proposal · **Family:** MeterData · **From:** v0.6 → v0.7 · **Breaking:** no · **Status:** draft for IES Cell review

## Motivation

The Ministry of Power's Centralized Energy Sales Dashboard is collecting DISCOM consumer-bill data (currently via the BBPS Bill Post API v1.3, NBBL as collector). At the 12 Aug 2026 NPCI/REC review, IES was proposed as the exchange mechanism: bill data moves over the IES exchange flow as a `MeterDataCredential` wrapping a MeterData `BILL_DETAILS` payload, with the ElectricityCredential carrying the connection facts. A field-level crosswalk of BBPS v1.3 against MeterData v0.6 found that `BillDetails` covers the headline bill (number, dates, `amountDue`, energy/fixed/other charges, prepaid balance) but has **no home for itemised taxes and duties, subsidy, arrears / deposit, open-access charges, the ToU billed adjustment, payment terms, bill version/cycle, or coarse geography for aggregation**. This proposal closes those gaps.

## Scope

- **In:** optional fields on `BillDetails`; two small enums (`BillingFrequency`, `OpenAccessTerm`); one non-PII value object (`ServiceLocation`); regenerated `schema.json` / `context.jsonld` / `vocab.jsonld`; three worked examples; changelog; crosswalk.
- **Out:** every other profile, the Data Descriptor Engine, `IES codes.json`, the validator, ElectricityCredential (v1.2 untouched), MeterDataCredential (v0.6 wrapper already accepts a v0.7 payload; `$ref` bump is a follow-up), protocol/transport (status/on_status, SIGNED_URL, receipts, SFTP), rejection-file format, DigiLocker DocType.

## Guarantees

- **Additive only.** 30 new optional properties on `BillDetails` + 3 new components. No rename, removal, type change or re-ordering. Compiled artefacts diff against v0.6 is add-only (37 new `ies:` terms; `$id` bumped).
- **Backward compatible in both directions.** All 25 v0.6 examples pass v0.7 unchanged; a v0.7 record also validates under v0.6 (no `additionalProperties:false`), so a v0.6 consumer simply ignores the new fields.
- **Repo conventions followed:** flat monetary fields in the record's `currency` (as `energyCharges` etc.), `Kwh`/`Kw` unit suffixes (as `sanctionedLoadKw`), `date` for bill dates, named enums as components, generator-compiled context/vocab, field-table README, WIP banner for drafts.
- **Solution-agnostic normative text.** No product/vendor names in field descriptions; BBPS/NBBL appear only in the crosswalk and this proposal.

## Design decisions to review (details + rationale in `CHANGELOG.md`)

1. Geography → `BILL_DETAILS.serviceLocation` (non-PII granularity: PIN / city / district / state / substation / region), not ElectricityCredential.
2. `netBilledAmount` derived (`arrearsAmount + currentBillAmount`), not stored.
3. `voltageCategory` = mapping guidance from `EnergyResourceNetwork.nominalVoltage`, not a field.
4. Flat grouping with prefixes (`tax*`, `openAccess*`, `subsidy*`), mirroring v0.6's flat `BillDetails`.
5. All new fields optional ("present when on the bill").
6. A few names deliberately differ from the BBPS dictionary for repo convention/precision (`billPeriod→billingFrequency`, `todAmount→touAdjustmentAmount`, `*Units→*Kwh`, `assesedUnits→assessedKwh`, `totalEnergyCharge→currentBillAmount`); all mapped in the crosswalk.
7. `openAccessTerm`, `openAccessContractDemandKw`, `securityDeposit` are contract/account terms carried per bill only because ElectricityCredential has no model for them — flagged as future EC candidates.

## Open questions for reviewers / NPCI

- Ask #2 from the review is still open: which gap groups must be **structured** vs **rolled-up**. Sections **G (open access)** and **H (payment terms)** are the most prunable if rolled-up totals suffice.
- `totalEnergyCharge` → `currentBillAmount`: confirm whether the BBPS figure includes taxes/duties.
- `meterStatus`, `billType`, `typeOfSupply` semantics — marked *verify* in the crosswalk (mapped from the deck, not the PDF).
- Should `paymentStatus` become an enum in a later release?

## Files (in the implementing PR)

```
schemas/MeterData/v0.7/
  attributes.yaml            source of truth (v0.6 + additions)
  schema.json · context.jsonld · vocab.jsonld   regenerated
  README.md                  v0.6 README + draft banner + regenerated field table
  CHANGELOG.md               every field, optionality, decisions 1–7, follow-ups
  CROSSWALK_BBPS_BILLPOST_V1.3.md   full BBPS v1.3 → IES mapping
  PROPOSAL.md                this text
  examples/                  25 v0.6 examples carried forward + BillDetails_Domestic_NetMetered / _OpenAccess_HT / _Prepaid
  IES codes.json · validation/ · Makefile       unchanged copies (per-version bundle convention)
schemas/MeterData/README.md  Versions table: v0.7 row (Draft), v0.6 stays Current
SUMMARY.md · _sidebar.md     nav entry for the v0.7 page (marked draft)
scripts/jsonld_conformance_scope.json   entry for MeterData/v0.7
scripts/generate_schemas_ies.py + schemas-ies/*.md   catalog no longer presents a Draft-status version as current
```

## Verification

- `python3 schemas/MeterData/v0.7/validation/validator.py schemas/MeterData/v0.7/examples` — 28/28 pass (structural + semantic).
- `python3 scripts/run_schema_checks.py`, `run_jsonld_checks.py`, `validate_links.py`, `check_navigation.py`, `generate_field_tables.py --all --check`, `generate_schemas_ies.py --check` — all green.

## Acceptance checklist

- [ ] IES Cell review of decisions 1–7
- [ ] NPCI answer on structured-vs-rolled-up (prune G/H if needed)
- [ ] Re-verify *verify* rows against the BBPS v1.3 PDF
- [ ] Merge PR; flip Versions table (v0.7 Current, v0.6 Previous); remove draft banner and `PROPOSAL.md`
- [ ] Follow-up: MeterDataCredential `$ref` → MeterData v0.7

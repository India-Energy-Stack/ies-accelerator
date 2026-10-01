# Before You Propose a Schema

*Ten checks to run before you open the [Propose a Schema](propose-a-schema.md) form. Proposals that skip them are sent back before review starts — they cost you a review cycle and cost reviewers time that other proposals need.*

**[⬇ Download this checklist as Word (.docx)](https://github.com/India-Energy-Stack/ies-accelerator/raw/main/before-you-propose.docx)**

## 1. Check it doesn't already exist

Search the [schema catalogue](schemas-ies/README.md) and the [term taxonomy](schemas-ies/taxonomy.md) first. If an existing family nearly fits, propose an **extension** to it (a new optional field or enum value is a minor version) rather than a parallel schema.

## 2. Study the IES term taxonomy

The [taxonomy](schemas-ies/taxonomy.md) lists every published term. For each field in your schema:

- **Same meaning as an existing term → use that term, spelled exactly as published.** Don't rename it to match your system — `customerNumber`, not `ConsumerNo` or `CA_NUMBER`.
- **No existing term fits → propose a new one**, with a one-line definition, and say it is a proposed addition.
- **Concepts that aren't fields** (DISCOM, DER, Beckn …) belong in the [Glossary](glossary.md), not in your schema.

The form asks you to declare that you did this. Declare it only once you have.

## 3. Follow IES naming conventions

| Rule | Do | Don't |
|---|---|---|
| Field names are lowerCamelCase | `billingCycleDay` | `BillingCycleDay`, `billing_cycle_day` |
| Type names are UpperCamelCase | `TelemetryMode` | `telemetry_mode_enum` |
| Units travel with the value, not in the name | `sanctionedLoad: {value, unit}` | `sanctionedLoadKw` |
| Dates and times are ISO 8601; currency is ISO 4217 | `2026-06-01`, `INR` | `01-06-2026`, `Rs` |
| Identifiers reuse IES patterns | `did:web:…`, MRID | a new home-grown ID scheme |

## 4. Submit a data model, not an API dump

Describe the **record** that moves between parties: its fields, types and meaning. Leave out request/response wrappers, status codes, usernames, pagination and anything that only exists because of one vendor's system. If your proposal is a copy of an existing API's payload, it is not ready.

## 5. Use a schema format reviewers can read

Preferably **JSON Schema (Draft 2020-12)** — the format IES schemas are published in. A field table (name · type · required · definition · standard) is acceptable. Either way, include **one example payload** that matches it.

## 6. Name the standards it rests on

Order of preference: **IS → CEA Regulations / IEGC → IEC → IEEE**. Where the governing instrument is a regulation (a SERC order, a commission procedure), name it. "None" is a valid answer only if you looked.

## 7. Pick "existing" or "new" use case honestly

"Existing" means one of the published [use-case overviews](use-cases-overview/README.md). Anything else is **new** — and needs the concept note below to explain it.

## 8. Write the concept note on the template

Use the use-case overview template — [read it on GitHub](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/.github/templates/use-case-overview.md) or [download it as Word (.docx)](https://github.com/India-Energy-Stack/ies-accelerator/raw/main/.github/templates/use-case-overview.docx). Share it as a link anyone can view.

## 9. One proposal per use case

Related records for one use case go in **one** proposal. Twenty near-identical submissions are triaged as one, and slower.

## 10. Re-read before you submit

Every field has a definition, every term was checked against the taxonomy, the example validates against the schema, and the concept-note link opens in a private browser window.

---

Ready? → [Propose a Schema](propose-a-schema.md)

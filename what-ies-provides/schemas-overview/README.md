# Schemas Overview

Before the field-by-field technical reference, each IES schema gets one plain-language page here — what it is, who issues it, what standards it follows, and where it still has open questions. This is the same **IES Documentation Template** already used for every use-case guide (sections 1–7 in plain language, a condensed Schedule I/II, Annexures A–C), applied to the schema itself rather than to a use case built on top of it.

Read one of these before the auto-generated field reference in [Schemas](../../schemas/README.md) if you want the *why* before the *what*.

| Schema | What it is | Status |
|---|---|---|
| **[ElectricityCredential v1.2](electricity-credential.md)** | W3C Verifiable Credential — a consumer connection's static facts and the energy resources behind the meter | Stable |
| **[MeterData v0.6](meter-data.md)** | Compact telemetry payload — 8 telemetry profile shapes (plus a shared descriptor object) for smart-meter readings, events and alarms | Stable |
| **[MeterDataCredential v0.6](meter-data-credential.md)** | W3C Verifiable Credential wrapping a MeterData payload to attest its provenance | Draft for technical review |
| **[MeterDataRequest v0.6](meter-data-request.md)** | Query and authorisation payload for asking a provider for telemetry | Draft for technical review |
| **[MeterDataRequestCredential v0.1](meter-data-request-credential.md)** | W3C Verifiable Credential wrapping a MeterDataRequest to prove the requester's authorisation | Draft for technical review |
| **[ArrFiling v0.5](arr-filing.md)** | Structured Aggregate Revenue Requirement filing — DISCOM to SERC | Draft for technical review |
| **[OutageNotification v0.1](outage-notification.md)** | Planned/unplanned outage record — pull feed + CAP-aligned push | **Work in progress** |

---

## How each page is organised

Every page follows the same eleven numbered sections as a use-case guide, minus the use-case-specific extras:

1. **Scope and Purpose** — the problem, in plain words
2. **What It Records / Covers** — what is captured
3. **How Each Item is Identified** — DIDs, identifier patterns
4. **Definitions** — terms and acronyms
5. **Basis of Standards** — the standards this schema follows (BIS → CEA → IEC → IEEE precedence)
6. **Where Indian Standards Do Not Yet Exist** — gaps and the international standards used
7. **The Record(s)** — what the schema actually produces
8. **Schedule I — Field Reference (summary)** — block names, linking to the full auto-generated table
9. **Schedule II** — whether this schema wraps or depends on another
10. **How It Fits Together** — how this schema relates to others and to use cases
11. **Points for Confirmation** — genuinely open questions
- **Annexure A — Standards Referenced**, **Annexure B — Example Payloads**, **Annexure C — JSON Schema** (all linking back to the schema's own files rather than duplicating them)

---

## Where this fits

This page sits under **[Exchange](../discover-exchange.md)**, alongside the [Taxonomy](../taxonomy.md) (the master schema map) and [Schemas](../../schemas/README.md) (the auto-generated technical reference).

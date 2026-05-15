# IES Registries and Directories

Public registries are the **trust layer** under both IES capabilities. A credential verifier reads a registry to decide whether to trust an issuer. A Beckn participant reads a registry to discover counterparties and validate signatures. A regulator reads a registry to find an asset. **Every cross-organisation interaction in IES eventually resolves through a registry.**

This section is the developer reference for **how those registries are built, operated, and consumed**.

| Capability | What it does |
|---|---|
| **Namespaces** | A domain-verified container owned by one organisation. The unit of governance. |
| **Registries** | Typed collections of records inside a namespace, with a schema (built-in tag or custom). |
| **Records** | Individual JSON entries — a DISCOM trust entry, a credential revocation, a Beckn subscriber, an asset. |
| **Proofs** | Every record carries a BLAKE2 H256 digest anchored on the CORD blockchain. Tampering is detectable; history is queryable. |

IES public registries are hosted on **DeDi (Decentralised Directory Protocol)**. The protocol is open-source and self-hostable; the default hosted platform is at [`dedi.global`](https://dedi.global). This section is self-sufficient — you should not need to leave it to onboard.

---

## Reading order

| Doc | Read it for |
|---|---|
| [DeDi Primer](./dedi-primer.md) | What DeDi is, the three-coordinate model (namespace/registry/record), proof types, trust pillars, deployment options. Skip if you already understand DeDi. |
| [Registry Creation](./registry-creation.md) | Hands-on step-by-step: account → domain-verified namespace → registry → records → lookup. UI flow + matching `curl`. Day-2 ops and troubleshooting. |
| [Required Registries for Onboarding](./required-registries.md) | The baseline catalogue an IES participant needs — DISCOM reference, Beckn subscriber, revocation, public-keys, etc. Each entry has record shape and onboarding contact. Ends with a 10-step end-to-end checklist. |

---

## Quick orientation by role

**A DISCOM joining IES for the first time** — start with [Required Registries](./required-registries.md#end-to-end-onboarding-checklist) and follow the 10-step checklist; jump back into the other two pages as needed.

**A developer integrating against IES** — start with [DeDi Primer](./dedi-primer.md) for the API surface, then [Required Registries](./required-registries.md) to know what URLs to read.

**A verifier or wallet developer** — start with [DeDi Primer](./dedi-primer.md) (proof verification procedure), then [Resolution and Routing](../identifiers/resolution.md) for the request-time workflows.

**A regulator or network operator** — start with [DeDi Primer](./dedi-primer.md) (governance and key custody), then [Required Registries](./required-registries.md) for the reference registries you will operate.

---

## How this section relates to others

- **Identifiers and Addressing** explains what a DID is and how it is shaped. **This section** explains where the record a DID resolves to lives.
- **Energy Credentials** uses the **revocation** and **public-keys** registries documented here.
- **Data Exchange** uses the **Beckn subscriber** and **network reference** registries documented here.

Every link inside IES eventually lands on a record in one of these registries.

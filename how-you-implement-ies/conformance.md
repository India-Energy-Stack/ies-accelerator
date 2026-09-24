# Conformance Checklist

> **The final check before you publish.** Verify your interface is correct end-to-end and (for Beckn participants) submit for IES network membership in production. About 1 day.

## Before you start

- [Setting up Register](setup-register.md) complete for your role.
- The engine(s) your use cases need are running: [Issuing Credentials](issue-credentials.md) (B2C) and/or [Setting up Discover & Exchange](setup-exchange.md) (B2B).
- At least one use case wired through [Build your Internal-facing Adapter](build-adapter.md).

**Only the checks for the rails you actually use apply.** The checklist below is tagged: **[all]** applies to everyone, **[credential]** only to credential issuers (B2C), **[beckn]** only to Beckn-network participants (B2B). A credential-only issuer skips every **[beckn]** item and the production-network submission at the end; a pure data-exchange participant skips every **[credential]** item.

---

## What this checklist proves — and what it doesn't

Every item below is either something you can run and check yourself, or a step in a documented network-membership process. Neither is the same thing as full conformance. Three boundaries matter beyond schema validation (see [What schema validation proves](#what-schema-validation-proves-and-what-it-doesnt) further down for that boundary specifically):

- **JSON-LD conformance** — that your `@context` resolves and the payload expands as valid JSON-LD, not merely valid JSON — is a separate check from JSON Schema validation and is not asserted by anything on this page.
- **Beckn/network protocol interoperability** — a real `discover`/`confirm` round-trip against a live counterparty on a reachable network — is only as good as the sandbox peer you actually reach it against, and is distinct from schema validation.
- **Certification and production participation** are a dated determination made by the IES Secretariat (see "Submitting for production" below), not something any local script or checklist item confers by itself. Whether that process, the sandbox, or any IES network is currently reachable is not something this repository can verify — see where things stand on the [Getting Started](../README.md) page.

Clearing every box below means your interface is well-formed and internally consistent by the checks this repository can run. It is not, on its own, proof of external-schema conformance, JSON-LD conformance, protocol interoperability, certification, or production readiness.

---

## What conformance means

### Identity is correctly published **[all]**

- [ ] `did:web` resolves from outside your network (`curl https://<your-domain>/.well-known/did.json` returns valid JSON)
- [ ] The DID document declares your current signing key
- [ ] Key rotation procedure documented (who, how, on what trigger)
- [ ] DeDi namespace verified (DNS TXT proof) and listed on `explore.dedi.global`

### Network membership is in place **[beckn]**

- [ ] Beckn subscriber record published in your DeDi namespace (Ed25519 key, callback URL, BAP/BPP role)
- [ ] Reference entry written by the IES Secretariat into the IES network registry
- [ ] Sandbox loop succeeds (`discover` or `confirm` round-trip with a peer)

### At least one use case is wired and validates **[all]**

- [ ] One use-case implementation guide (e.g. [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md) or [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md)) implemented end-to-end
- [ ] Output validates against the canonical JSON Schema (`make validate` or `python3 scripts/validate_schema.py …`)
- [ ] **[beckn]** At least one real record exchanged with a counterparty on the testnet, **or [credential]** at least one credential issued, verified, and revoked (the [§3.9 smoke test](issue-credentials.md#id-3.9-smoke-test))
- [ ] Schema validation enforced on every outgoing payload

### Signatures and trust chain check out

- [ ] **[credential]** Every credential you issue carries a valid signature (W3C VC Data Model 2.0 proof block)
- [ ] **[credential]** Revocation registry (`vc-revocation-registry`) exists in your DeDi namespace (OpenCred auto-creates it; if not using OpenCred, create it manually)
- [ ] **[credential]** Verification rehearsed by at least one relying party (peer DISCOM, bank, marketplace) resolving your `did:web`
- [ ] **[beckn]** Every Beckn message you send carries a valid Ed25519 signature
- [ ] **[beckn]** Signature verification rehearsed by at least one counterparty (peer DISCOM, AMISP)

### Operations

- [ ] Logging captures every inbound and outbound Beckn message (subscriber, action, message id, timestamp)
- [ ] Monitoring / alerting on adapter health
- [ ] Key rotation runbook
- [ ] Incident escalation path defined (within IES Secretariat process)

### Security and privacy

- [ ] Signing keys held in KMS / HSM where available; never in source control
- [ ] TLS on all callback endpoints
- [ ] For consumer-facing credentials: identity-proofing procedure documented and privacy-reviewed
- [ ] For consumer-facing credentials: explicit consent capture on every issuance / disclosure

---

## What schema validation proves — and what it doesn't

`scripts/validate_schema.py` (and `make validate`) check **repository-local structural and semantic validation** — your payload against the IES-authored `schema.json` for that family, under Draft 2020-12. For schema families that are fully self-contained — every `ElectricityCredential` version, `MeterDataRequest`, `ArrFiling`, `MeterData/v0.5` — that check is complete against everything this repository defines.

Other families reference externally-hosted Beckn/DEG structures that are not mirrored in this repository, and the local validator resolves every one of them through a permissive stub (`{"type": "object"}`) rather than the real upstream schema — so a passing result does not check the stubbed structure against its actual definition. The unchecked surface differs by family, and is not uniformly small:

- **`MeterData/v0.6`** references two external substructures, `Address` and `GeoJSONGeometry`, both stubbed.
- **`OutageNotification/v0.1`** references one external substructure, `GeoJSONGeometry`, stubbed.
- **`MeterDataCredential/v0.6`** and **`MeterDataRequestCredential/v0.6`** each reference the external `EnergyCredential/v2.0` credential envelope — the entire Beckn VC wrapper (`issuer`, `proof`, `credentialSubject` shape, and everything else it constrains) — and that whole envelope is stubbed permissively. A passing result on these two families only checks the local `meterData` / `meterDataRequest` payload nested inside the credential; it does not check the envelope fields against their actual upstream definitions at all. Both families also nest a local `$ref` to `MeterData/v0.6` or `MeterDataRequest/v0.6` respectively, so `MeterDataCredential/v0.6` additionally inherits `MeterData/v0.6`'s own unchecked `Address`/`GeoJSONGeometry` substructures.

Passing local validation on any of these families means "well-formed except for the unchecked externally-hosted structure(s) listed above for that family," not full external-schema conformance.

Treat a schema-validation pass as scoped to what this repository defines — see [What this checklist proves](#what-this-checklist-proves-and-what-it-doesnt) above for the JSON-LD, protocol, and certification boundaries that sit outside schema validation entirely.

---

## How to confirm conformance

### Beckn participants (B2B)

Run the conformance suite that ships with the devkit you cloned in [Setting up Discover & Exchange](setup-exchange.md#id-2.1-deploy-the-local-sandbox):

```bash
cd DEG/devkits/data-exchange/conformance
./run.sh --subscriber did:web:ies.discom.example --usecase consumer-energy-passport
```

The script exercises every path on the checklist above against a sandbox peer and emits a signed report. For use cases not yet in the suite, do the equivalent manually: generate one record with your adapter, validate it against the canonical JSON Schema (`scripts/validate_schema.py`), send it to a sandbox counterparty, and have them verify the signature and contents.

### Credential-only issuers (B2C)

You have no Beckn devkit and no counterparty, so these checks are self-contained — run the [§3.9 smoke test](issue-credentials.md#id-3.9-smoke-test) end-to-end:

1. Issue a credential with your adapter (or OpenCred directly).
2. Validate the credential document (`out.json`) against the canonical credential-root JSON Schema (`python3 scripts/validate_schema.py schemas/<Credential>/<version>/schema.json out.json`) — repository-local structural validation, per the [scope note above](#what-this-checklist-proves-and-what-it-doesnt).
3. Resolve your own `did:web` over HTTPS and confirm the published key verifies the credential's `proof`.
4. Check revocation status (not revoked), revoke, re-check (revoked).

If all four pass, your issuance has cleared the B2C checks on this page: it is schema-valid within the scope described above, and independently verifiable by anyone who resolves your `did:web`. There is nothing to submit to a network — verification happens bilaterally, whenever a relying party checks your `did:web`, not through a central certification step. This is not, by itself, a claim of JSON-LD conformance or of conformance against externally-hosted schema substructures your payload references.

---

## Submitting for production **(Beckn participants only)**

This is the documented network-membership process. Whether the IES Secretariat, the sandbox, and the production/test network registries referenced below are currently staffed and reachable is not something this repository can verify on its own — see where things stand on the [Getting Started](../README.md) page before relying on this as a live, working pipeline.

When all the above pass on the sandbox / testnet:

1. Email the IES Secretariat ([IES.Secretariat@fsrglobal.org](mailto:IES.Secretariat@fsrglobal.org), alternate [ies@recindia.com](mailto:ies@recindia.com)) with: your `did:web`, your DeDi namespace, your testnet conformance report, and the use cases you have implemented.
2. The Secretariat re-runs spot checks on your sandbox endpoints.
3. The Secretariat writes a production reference entry pointing at your subscriber record.

Once that reference entry is written, your subscriber record is queryable as in-network by any counterparty that looks it up, without a further bilateral arrangement — that is what "referenced into the network" means (see [Setting up Register §1.7](setup-register.md#id-1.7-beckn-participants-get-referenced-into-an-ies-network)). That determination is made by the Secretariat; it is not something this checklist, `scripts/validate_schema.py`, or any other local script confers by itself, and it is a statement about network registration — not, on its own, a statement about JSON-LD conformance or protocol interoperability with every possible counterparty. (Credential-only issuers skip this step — there is no central network registry in the credential-only path; the B2C checks above are what make your issuances independently verifiable.)

---

## After conformance

- **Add new use cases** by repeating only [Build your Internal-facing Adapter](build-adapter.md) for the new schema. Identity, engines, network membership and trust foundation are reused.
- **Stay current with schema versions.** New versions are announced via the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator); migration guides ship alongside.
- **Contribute** — propose a new schema or a change to an existing one by raising a discussion on the repository (see [Propose a Schema](../propose-a-schema.md)). The IES Cell governance process handles ratification.

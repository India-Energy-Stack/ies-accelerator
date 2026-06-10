# MeterDataCredential

W3C Verifiable Credential (VC Data Model 2.0) that wraps a [MeterData](../MeterData/README.md) payload to attest the authenticity and provenance of delivered smart meter telemetry. Issued by data providers (AMISP, MDM, DISCOM).

**Namespace prefix:** `ies:` → `https://india-energy-stack.gitbook.io/docs/schemas/ies#`

**Tags:** `credential` · `verifiable-credential` · `metering` · `ies`

---

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.6](v0.6/README.md) | **Current** | Wraps MeterData v0.6; BitstringStatusListEntry revocation |

---

## Inheritance

```
beckn:Credential
  └── EnergyCredential
        └── MeterDataCredential  ← this schema
```

---

## Usage

Attached to Beckn `on_status` responses. Cryptographically binds the delivered MeterData payload to the issuing provider's DID, enabling downstream verifiers to confirm identity, provenance, and tamper-evidence.

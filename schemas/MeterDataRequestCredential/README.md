# MeterDataRequestCredential

W3C Verifiable Credential (VC Data Model 2.0) that wraps a [MeterDataRequest](../MeterDataRequest/README.md) to prove a data requester's authorisation for accessing smart meter telemetry. Presented by the seeker at `confirm` time.

**Namespace prefix:** `ies:` → `https://schema.beckn.io/ies/`

**Tags:** `credential` · `verifiable-credential` · `metering` · `authorisation` · `ies`

---

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.1](v0.1/README.md) | **Current** | Initial release; wraps MeterDataRequest v0.6 |

---

## Inheritance

```
beckn:Credential
  └── EnergyCredential
        └── MeterDataRequestCredential  ← this schema
```

---

## Usage

The provider's offer policy requires the seeker to present this credential at `confirm`. It identifies the requesting entity (DID + licence number), scopes the request, and is cryptographically signed — enabling the provider to verify without a round-trip to the issuer.

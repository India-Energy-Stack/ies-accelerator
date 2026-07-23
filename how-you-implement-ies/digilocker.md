# DigiLocker Integration — DISCOM Guide

This guide covers everything your DISCOM needs to build the DigiLocker Pull URI endpoint — the single piece of custom code required to make IES energy credentials available to consumers in DigiLocker.

Two document types flow into DigiLocker through the **same Pull URI mechanism**:

| DocType | Credential | What it carries | Keyed on |
|---|---|---|---|
| `NYCER` | **Consumer Energy Passport** (`ElectricityCredential` v1.2) | Slow-changing facts — who holds the connection and every typed asset behind the meter (meter, solar, battery, EV, inverter, load, network), each power/capacity value a `{value, unit}` pair | Consumer number |
| `MPLTR` | **Consumer Meter Digest** (`MeterDataCredential` v0.6) | The consumer's own meter readings for a chosen period — a signed energy *statement*, not a bill | Consumer number **+ period** |

> **DocType confirmed.** NeGD has allotted `MPLTR` (Meter Document) as the DocType for the Consumer Meter Digest. `NYCER` stays unchanged for the Consumer Energy Passport — same DocType, same Pull URI flow; only the payload schema moves to v1.2.

The Digest reuses the connection-credential flow almost unchanged. The one structural difference is the document key: the Digest puts the **period into the URI** so every period coexists instead of overwriting — exactly the difference between a statement and a bill.

---

## What DigiLocker Does

DigiLocker is India's national digital document wallet. When a consumer searches for one of these credentials in DigiLocker, DigiLocker calls your endpoint, your endpoint calls IES (OpenCred) to issue a signed credential, and DigiLocker stores it — all in real time.

```
Consumer                 DigiLocker              Your Endpoint           IES
   │                         │                        │                    │
   │── search NYCER/MPLTR ──>│                        │                    │
   │   (consumer no. + …)    │                        │                    │
   │                         │── PullURIRequest ─────>│                    │
   │                         │   (XML, HMAC signed)   │                    │
   │                         │                        │── /issue ─────────>│
   │                         │                        │<─ signed VC ───────│
   │                         │                        │── /package ───────>│
   │                         │                        │<─ PDF ─────────────│
   │                         │<── PullURIResponse ────│                    │
   │                         │   (XML + base64 PDF    │                    │
   │                         │    + base64 VC)         │                    │
   │<── credential saved ────│                        │                    │
```

A credential only has value once it reaches a use case — a lender assessing the consumer, an analytics app, a subsidy portal. DigiLocker is that bridge: it carries the consent and sharing rails (QR scan in person, OAuth consent pull for third-party apps) that make a credential useful beyond the wallet.

---

## Flow Overview

The integration has three phases:

- **Phase 0 — One-time setup:** Register on API Setu, create issuer DID, register the DocTypes
- **Phase 1 — Pull URI endpoint:** Build and host the HTTPS endpoint DigiLocker calls (one handler, both DocTypes)
- **Phase 2 — Consumer sharing:** Consumers share the credential with verifiers via DigiLocker OAuth (no DISCOM involvement)

---

## Phase 0 — One-Time Setup

### Step 1 — Register on API Setu

Go to [https://apisetu.gov.in](https://apisetu.gov.in) and register as a document issuer. You receive:
- `issuer_id` (e.g. `in.gov.discom`)
- `api_key` — store this securely; used for HMAC verification

> If your DISCOM already issues electricity bills (ELBIL) on DigiLocker, contact NeGD to add the `NYCER` and `MPLTR` document types to your existing account. Do not re-register.

Alongside the DocTypes, register your **credential issuer** with NeGD so DigiLocker can resolve and trust it. NeGD asks for a small block:

```json
{
  "credential_type": "UtilityElectricityCredential",
  "issuer_did": "did:web:www.discom.example:energystack",
  "resource_schema": []
}
```

The `issuer_did` is the one from [Step 2](#step-2-stand-up-opencred-and-your-issuer-did) — it may live on your own domain, or in a DigiLocker-hosted issuer namespace (e.g. `did:web:vc.dl6.in:issuers:in.gov.<state>electricity`) if NeGD hosts it for you.

> **Keep the org id consistent across registration and every URI.** The org segment of each Pull URI (`in.gov.<orgId>-<DocType>-<consumerNo>`, e.g. `in.gov.com.discom-NYCER-100000012345`) must equal the `issuer_id` / `orgId` you registered on API Setu. A URI whose org segment doesn't match the registered issuer fails at DigiLocker with an *org id / issuer id mismatch* — the response is accepted but its document data is rejected, which is easy to misread as a payload problem.

### Step 2 — Stand Up OpenCred and Your Issuer DID

Follow [Setup Register — keypair and did.json](setup-register.md#id-1.2-generate-your-credential-signing-keypair) and [Issue Credentials — run OpenCred](issue-credentials.md#id-2.3-run-opencred-in-did-web-mode) end-to-end. By the time you reach this page you should have:

- OpenCred running with `signingKeyLoaded: true`
- An issuer DID — `did:web:ies.discom.example` (recommended) or `did:key:…` (from an imported DSC)
- (Optional, recommended) DeDi configured for revocation

Save your issuer DID — it goes into every `POST /v1/credentials/issue` call.

> **Gotcha — the DID host must serve `did.json` *without* a redirect.** A `did:web` DID resolves by fetching `https://<host>/<path>/did.json`. If that host 301-redirects — e.g. `https://discom.example/energystack/did.json` → `https://www.discom.example/energystack/did.json` — lenient verifiers follow the redirect, but strict resolvers (OpenCred among them) reject it, and a consumer's credential then fails to verify. Name the **canonical host that answers directly** in your DID: if `www.` is where `did.json` is served, the issuer DID is `did:web:www.discom.example:energystack`, not `did:web:discom.example:energystack`. Confirm with `curl -sSL -o /dev/null -w '%{http_code} %{url_effective}\n' https://<host>/<path>/did.json` — a `200` with an unchanged URL, not a `301`.

### Step 3 — Register the Pull URI Endpoints on API Setu

Register both DocTypes against the same Pull URI endpoint. They differ only in the UDF fields and the URI key.

**NYCER — Electricity Credential v1.2**

| Field | Value |
|---|---|
| Endpoint URL | `https://{your-domain}/digilocker/pulluri` |
| HTTP Method | `POST` |
| Content-Type | `application/xml` |
| DocType | `NYCER` |
| UDF1 Label | `Consumer Number` |
| UDF2 Label | `Registered Mobile Number` |

**MPLTR — Consumer Meter Digest**

| Field | Value |
|---|---|
| Endpoint URL | `https://{your-domain}/digilocker/pulluri` |
| HTTP Method | `POST` |
| Content-Type | `application/xml` |
| DocType | `MPLTR` |
| UDF1 Label | `Consumer Number` |
| UDF2 Label | `Statement Period` (e.g. `2026-05` or `last-12-months`) |
| UDF3 Label | `Registered Mobile Number` |

> **MPLTR registers as an additional record on the same endpoint already registered for NYCER** — one Pull URI handler, branched by `DocType`. One item is still pending **written** confirmation from DigiLocker even though it was agreed in principle on the 12 June 2026 call: treating each **period-keyed URI** as a distinct, independently listable/deletable document (see [The Consumer Meter Digest](#the-consumer-meter-digest-doctype-mpltr)). **Configurable rendering** of the statement card remains an open ask. Everything else reuses the NYCER flow unchanged.

---

## Phase 1 — The Pull URI Endpoint

This is the **only endpoint your DISCOM builds**. DigiLocker calls it; you respond. A single handler serves both DocTypes — branch on `DocType` (see [Routing by DocType](#routing-by-doctype)).

### Endpoint Specification

```
POST https://{your-domain}/digilocker/pulluri
Content-Type: application/xml
x-digilocker-hmac: <Base64(HMAC-SHA256(api_key, request_body))>
```

### Step 1 — Verify the Inbound HMAC

**Always verify the HMAC before doing anything else. Reject with HTTP 401 if invalid.**

```python
import hmac, hashlib, base64

def verify_digilocker_hmac(request_body: bytes, api_key: str, received_hmac: str) -> bool:
    expected = base64.b64encode(
        hmac.new(api_key.encode(), request_body, hashlib.sha256).digest()
    ).decode()
    return hmac.compare_digest(expected, received_hmac)  # constant-time comparison
```

### Step 2 — Parse the Inbound Request

DigiLocker sends a `PullURIRequest` XML v3.0. For NYCER:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIRequest ver="3.0"
                ts="2026-04-01T10:30:00+05:30"
                txn="TXN-20260401-001"
                orgId="discom">
  <DocDetails>
    <DocType>NYCER</DocType>
    <DigiLockerId>7a3f9b2c-1e4d-4f8a-b6c2-0d5e8f1a2b3c</DigiLockerId>
    <UDF1>DISCOM-2025-001234567</UDF1>   <!-- consumer number -->
    <UDF2>9876543210</UDF2>             <!-- registered mobile number -->
    <FullName>Priya Sharma</FullName>    <!-- optional, from DigiLocker profile -->
  </DocDetails>
</PullURIRequest>
```

For MPLTR the period travels as a UDF, so the consumer can pull a chosen window:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIRequest ver="3.0"
                ts="2026-05-15T10:00:00+05:30"
                txn="TXN-20260515-042"
                orgId="discom">
  <DocDetails>
    <DocType>MPLTR</DocType>
    <DigiLockerId>7a3f9b2c-1e4d-4f8a-b6c2-0d5e8f1a2b3c</DigiLockerId>
    <UDF1>DISCOM-2025-001234567</UDF1>   <!-- consumer number -->
    <UDF2>last-12-months</UDF2>          <!-- statement period: YYYY-MM, a range, or a keyword -->
    <UDF3>9876543210</UDF3>             <!-- registered mobile number -->
    <FullName>Priya Sharma</FullName>
  </DocDetails>
</PullURIRequest>
```

| Field | Description |
|---|---|
| `ts` | Request timestamp — echo in response |
| `txn` | Transaction ID — echo in response |
| `DigiLockerId` | The consumer's DigiLocker-registered ID. Carry this into the issued credential's identity binding (`idRef`) for **both** DocTypes — see [Identity Binding — the DigiLocker ID](#identity-binding-the-digilocker-id). |
| `UDF1` | Consumer number — primary CIS lookup key |
| `UDF2` (NYCER) | Registered mobile number — secondary verification |
| `UDF2` (MPLTR) | Statement period — `YYYY-MM`, a range, or a keyword like `last-12-months`. A recurring pull with the current month fetches the latest statement. |
| `UDF3` (MPLTR) | Registered mobile number — secondary verification |
| `FullName` | DigiLocker profile name — DigiLocker validates name match against your response |

### Step 3 — Look Up Consumer in CIS

```python
consumer = cis.lookup(consumer_number=udf1, mobile=mobile)
if not consumer:
    return pulluri_error_response(ts, txn, status=0, message="Consumer not found")
```

### Identity Binding — the DigiLocker ID

NeGD's requirement, confirmed and accepted: the `DigiLockerId` received in the `PullURIRequest` must be carried inside the issued credential as part of the subject's identity binding, for **both** `NYCER` and `MPLTR`. Populate `customerProfile.idRef` (Passport) / the subject-level identity reference (Digest) with it:

```python
holder_idref = {
    "issuedBy":  "did:web:digilocker.gov.in",
    "subjectId": f"digilocker.gov.in:{digilocker_id}",   # the <DigiLockerId> from the request
}
```

The rendered certificate (`DocContent`) should also show this in human-readable form — e.g. *"Identity Binding: binding method DIGILOCKER_PULL, binding date …"* — the pattern APEPDCL's current implementation already follows.

> **Schema gap.** `customerProfile.idRef` exists on the [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) schema, so the Passport can carry this binding today. `MeterDataCredential` v0.6's `credentialSubject` does **not** yet define an `idRef` (or equivalent) property — until the schema adds one, the Digest cannot carry this binding as a structured VC field, only in the rendered `DocContent`. Track this as an open schema item alongside the MPLTR rollout.

### Step 4 — Call OpenCred to Issue the Credential

This step differs by DocType — see [Issuing NYCER (v1.2)](issue-credentials.md#id-2.6-issue-your-first-credential) and [Issuing the Digest (MPLTR)](#issuing-the-digest-meterdatacredential-v0.6) below. Both return a signed VC, then render the PDF with a **separate** `POST /v1/credentials/package` call (see [Step 5](#step-5-package-the-pdf-and-vc-for-the-response)).

### Step 5 — Package the PDF and VC for the response

Rendering the PDF is a **separate call** — `POST /v1/credentials/package` with `formats: ["pdf"]` (the DocType handlers in Step 4 make it). An inline `packageFormats` field on the *issue* body is silently ignored, so this call is not optional — see [Issue Credentials §2.10](issue-credentials.md#id-2.10-package-the-credential-as-a-pdf-qr-code). The PDF carries the signed credential payload in its info dictionary and embeds a scannable QR — DigiLocker stores the PDF, and verifiers can later re-extract the credential from the PDF itself.

```python
import base64, json

# pdf_bytes came back from the /v1/credentials/package call in Step 4
pdf_b64 = base64.b64encode(pdf_bytes).decode()
vc_b64  = base64.b64encode(json.dumps(vc_json).encode()).decode()
```

For a custom PDF design (branded letterhead, regional language, a consumption-ladder or time-of-day card), render server-side with your own template engine and embed the QR + credential JSON as you prefer. `VcContent` is what verifiers actually parse — the PDF is for human display only and can't be checked against the issuer's signature.

### Step 6 — Return the PullURIResponse

```python
def build_pulluri_response(ts, txn, doc_type, uri, issued_to, valid_from, valid_to, pdf_b64, vc_b64):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIResponse ver="3.0" ts="{ts}" txn="{txn}" orgId="discom">
  <ResponseStatus Status="1" ts="{ts}" txn="{txn}"/>
  <DocDetails>
    <DocType>{doc_type}</DocType>
    <URI>{uri}</URI>
    <IssuedTo>{issued_to}</IssuedTo>
    <ValidFrom>{valid_from}</ValidFrom>
    <ValidTo>{valid_to}</ValidTo>
    <DocContent format="pdf">{pdf_b64}</DocContent>
    <VcContent format="json-ld">{vc_b64}</VcContent>
    <VcType>application/ld+json</VcType>
  </DocDetails>
</PullURIResponse>"""
```

| Field | Description |
|---|---|
| `Status="1"` | Success. Use `Status="0"` for errors. |
| `URI` | Unique identifier for this document in DigiLocker — `{issuer_id}-{DocType}-{docId}`. The final **doc-id** segment is **required**: NeGD rejects a URI that ends at the DocType with no doc-id. Form it the same way your existing electricity-bill (`ELBIL`) integration forms its doc-id; for a connection-keyed credential the CA / consumer number serves this role. NYCER: `{issuer_id}-NYCER-{consumerNo}`. MPLTR: `{issuer_id}-MPLTR-{consumerNo}-{period}` — **the period makes each statement a distinct document** (see [The document key](#the-one-real-gap-the-document-key)). |
| `IssuedTo` | Consumer's full name — DigiLocker validates this against the user's profile |
| `DocContent` | Base64-encoded PDF (the rendered statement / certificate card) |
| `VcContent` | Base64-encoded W3C VC JSON-LD — the signed credential, proof intact |
| `VcType` | Media type of the `VcContent` payload — **`application/ld+json`**. Required by NeGD immediately after `VcContent`; a response without it is rejected. |

### Handler Logic Summary

```
1. Read raw request body (keep bytes for HMAC)
2. Verify x-digilocker-hmac → HTTP 401 if invalid
3. Parse XML → extract DocType, UDF1..n, ts, txn
4. Lookup consumer in CIS → error response if not found
5. Resolve / generate the consumer's holder DID
6. Branch on DocType:
     NYCER → build v1.2 credentialSubject (energyResources[])
     MPLTR → build MeterData v0.6 payload for the requested period
7. POST /v1/credentials/issue → signed VC; then POST /v1/credentials/package (formats=["pdf"]) → PDF
8. Base64-encode PDF and VC
9. Return PullURIResponse XML with Status=1 and the DocType-appropriate URI
```

### Routing by DocType

```python
doc_type = request_xml.find(".//DocType").text
if doc_type == "ELBIL":
    return handle_elbil(request_xml)   # existing electricity bill, if you serve it
elif doc_type == "NYCER":
    return handle_nycer(request_xml)   # Electricity Credential v1.2
elif doc_type == "MPLTR":
    return handle_mpltr(request_xml)   # Consumer Meter Digest
else:
    return pulluri_error_response(ts, txn, status=0, message="Unsupported DocType")
```

---

## Issuing NYCER — the Consumer Energy Passport (Electricity Credential v1.2)

`NYCER` is the existing, unchanged DocType; only its payload schema is upgraded. Today's NYCER credential carries a flat set of customer-and-connection fields. The IES Electricity Credential, finalised at **v1.2** as the **Consumer Energy Passport**, carries far more: every physical asset behind the connection — meter, solar, battery, EV, inverter, controllable load — as one typed resource model with unit-bearing quantities.

### What changed from the flat shape

| | Today (flat) | v1.2 Electricity Credential |
|---|---|---|
| Customer & connection | Flat fields on `credentialSubject` | Non-PII `customerProfile` + PII `customerDetails` |
| Meter | `meterNumber` / `meterType` fields | `energyResources` entry, `type` `METER`, `attributes.meterCapability` + `energyDirection` |
| Generation, storage, EV, … | Not carried | Typed resources — `SOLAR_PV`, `BESS`, `EV_CHARGER`, `INVERTER`, … |
| Power & capacity values | n/a | `QuantitativeValue` `{value, unit}` — e.g. `maxExport {10, kW}` |
| Asset topology | Not carried | `parentResources` / `subResources` — submetering, parallel metering |
| Consumption / tariff | Not carried | `consumptionProfiles[]`, `sanctionedLoad` as `{value, unit}` |

### credentialSubject shape

```
credentialSubject
├─ id                       (optional)  customer DID
├─ customerProfile          (required)  non-PII
│  ├─ customerNumber        (required)  utility CA number
│  ├─ idRef                 (optional)  identity binding — the DigiLocker ID from the pull request
│  ├─ energyResources[]     (required)  typed assets, min 1 (at least one METER)
│  └─ consumptionProfiles[] (optional)  tariff / load per meter (QV units)
└─ customerDetails          (optional)  PII: fullName, address, connection date
```

**Seven typed `EnergyResource` kinds**, each aligned to CIM classes (IEC 61968 / 61970):

| Kind | `type` values | CIM alignment |
|---|---|---|
| Meter | `METER` | `cim:Meter` / `EndDevice` |
| Generator | `SOLAR_PV`, `WIND`, `HYDRO`, `BIOGAS`, `CHP`, `FUEL_CELL` | `cim:GeneratingUnit` |
| Storage | `BESS` | `cim:BatteryUnit` |
| EV Charger | `EV_CHARGER`, `EV_V2G` | `cim:EVChargingStation` |
| Inverter | `INVERTER` | `cim:PowerElectronicsConnection` |
| Load | `SMART_HVAC`, `SMART_WATER_HEATER`, `CONTROLLABLE_LOAD` | `cim:EnergyConsumer` |
| Network | `DT`, `BUS`, `FEEDER`, `MICROGRID` | `cim:PowerTransformer` / `Feeder` |

Common attributes (all kinds): `make`, `model`, `maxExport`, `maxImport`, `commissioningDate`, `location`. Per-kind adds, e.g. Storage → `storageCapacity`, `storageType`, `stateOfHealthPct`; Meter → `meterCapability`, `energyDirection`, `functions[]`. Every power or capacity figure is a `QuantitativeValue` — a `{value, unit}` pair with short unit aliases (`kW`, `kWh`, `kVA`, `kVAR`, `kV`) mapped to QUDT IRIs in the JSON-LD context.

> Only the meter is mandatory — a consumer with no DERs has one `METER` entry. PII (the name) lives only in `customerDetails`, so a verifier needing asset facts but not identity can be given `customerProfile` alone. The v1.1 type aliases `SOLAR` and `BATTERY` remain valid for backward compatibility, but `SOLAR_PV` / `BESS` are preferred.

### The OpenCred issue call

```python
import requests
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

credential_response = requests.post(
    "http://opencred:3100/v1/credentials/issue",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={
        "issuerDid":  ISSUER_DID,                # e.g. "did:web:ies.discom.example"
        "schemaId":   "ies/electricity-credential/v1.2",
        "additionalTypes": ["ElectricityCredential"],
        "proofFormat": "vc-jwt",
        "validFrom":  datetime.now(IST).isoformat(),
        "validUntil": (datetime.now(IST) + timedelta(days=365 * 5)).isoformat(),
        "subjectDid": holder_did,
        "credentialSubject": {
            "id": holder_did,
            "customerProfile": {
                "customerNumber": consumer.consumer_number,
                "idRef": {
                    "issuedBy":  "did:web:digilocker.gov.in",
                    "subjectId": f"digilocker.gov.in:{digilocker_id}",  # <DigiLockerId> from Step 2 — NeGD's identity-binding requirement
                },
                "energyResources": [
                    {
                        "id":   consumer.meter_id,
                        "type": "METER",
                        "attributes": {
                            "meterCapability":   consumer.meter_capability,   # e.g. "AMI"
                            "energyDirection":   consumer.energy_direction,    # e.g. "Bidirectional"
                            "functions":         consumer.meter_functions,     # ["NetMetering", "ToU"]
                            "applicationProtocol": "DLMS_COSEM",
                        },
                    },
                    # … append SOLAR_PV / BESS / EV_CHARGER / INVERTER entries as present,
                    #    each power/capacity field a {"value": …, "unit": "kW"|"kWh"|…} pair,
                    #    each linked to the meter via "parentResources": [meter_id]
                ],
                "consumptionProfiles": [
                    {
                        "meterId":           consumer.meter_id,
                        "sanctionedLoad":    {"value": consumer.sanctioned_load_kw, "unit": "kW"},
                        "tariffCategoryCode": consumer.tariff_code,
                        "premisesType":      consumer.premises_type,
                        "connectionType":    consumer.connection_type,
                        "paymentMode":       consumer.payment_mode,
                    }
                ],
            },
            "customerDetails": {
                "fullName": consumer.full_name,
                "installationAddress": {
                    "address":   consumer.address_line,
                    "city":      {"name": consumer.city,  "code": consumer.city_code},
                    "state":     {"name": consumer.state, "code": consumer.state_code},
                    "country":   {"name": "India",        "code": "IN"},
                    "area_code": consumer.pincode,
                },
                "serviceConnectionDate": consumer.connection_date.isoformat(),
            },
        },
        "revocationRegistryUrl": DEDI_REVOCATION_URL,
    }
).json()

vc_json = credential_response["credential"]

# Render the PDF with a SEPARATE packaging call. Packaging is a distinct
# rendering step, not part of issue — an inline `packageFormats` field on the
# issue body is silently ignored (see Issue Credentials §2.10). Package the
# credential as issued, proof intact, so the QR embedded in the PDF stays
# independently verifiable.
package_response = requests.post(
    "http://opencred:3100/v1/credentials/package",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={"credential": vc_json, "formats": ["pdf"]},
).json()
pdf_bytes = base64.b64decode(
    next(o for o in package_response["outputs"] if o["format"] == "pdf")["data"]
)

# Inject the schema-required issuer object before delivery — OpenCred returns
# issuer as the DID string, but the ElectricityCredential schema requires the
# full object with name and (optional) idRef. This invalidates the original
# proof; re-sign downstream if you need a single signed-and-conformant artifact.
vc_json["issuer"] = {
    "id":   ISSUER_DID,
    "name": ISSUER_NAME,
    "idRef": {
        "issuedBy":  IES_REGISTRY_DID,         # namespace DID of india-energy-stack on dedi.global
        "subjectId": IES_REGISTRY_SUBJECT_ID,  # e.g. india-energy-stack:discom
    },
}
```

The URI for NYCER stays keyed on the consumer number — a refresh overwrites the last, which is correct for a slow-changing connection credential:

```python
uri = f"in.gov.discom-NYCER-{consumer.consumer_number}"   # trailing segment is the required doc-id (see URI note in Step 6)
```

### What DigiLocker needs to accept for v1.2

1. **Accept the v1.2 schema for NYCER.** Validate against the published v1.2 context and JSON Schema — a `customerProfile` with `energyResources[]` (min one `METER`), optional `consumptionProfiles[]`, and `customerDetails` for PII. Power/capacity fields are `{value, unit}` objects, not bare numbers.
2. **Pass `VcContent` through unchanged.** The signed JSON-LD is the v1.2 credential as issued, proof intact — no reshaping. The proof is over the canonical form, and the QUDT unit context is part of it.
3. **Carry resource fields into the Certificate XML.** Extend the `DataContent` block so meter and DER resources (`type`, key attributes with value+unit) appear for DigiLocker-native parsers, alongside the existing connection and address fields.
4. **Render whatever resources are present.** Drive the card from `energyResources[]` as a list, showing each value with its unit. A meter-only consumer shows one row; a prosumer shows meter, solar, battery, EV. New kinds and unit types need no card change.
5. **Store and surface the DigiLocker identity binding.** `customerProfile.idRef` carries the `DigiLockerId` from the pull request (see [Identity Binding](#identity-binding-the-digilocker-id)) — reflect it on the rendered certificate alongside the binding date.

---

## The Consumer Meter Digest (DocType `MPLTR`)

The **Consumer Meter Digest** is a DISCOM-issued, digitally signed credential carrying a consumer's own meter readings for a chosen window of time. Where NYCER attests to slow-changing facts — who holds the connection, what assets sit behind the meter — the Digest is the consumer's **energy statement**: the meter records a reading roughly every fifteen minutes (~96 blocks a day), and the Digest packages those readings for a requested period into a signed document the consumer can hold and present.

**A statement, not a bill.** A bill is the latest snapshot, overwriting the last. A statement is a series the consumer can pull by period ("April, May, last twelve months"), each one kept rather than replaced — the whole point of the `MPLTR` integration, and why the document key carries the period (see [The one real gap](#the-one-real-gap-the-document-key)).

### Schema compliance — `MeterDataCredential` v0.6

The Digest is **not a new schema**. It is a consumer-facing issuance of the standard `MeterDataCredential` v0.6 — a W3C VC 2.0 subclassing `EnergyCredential` v2.0 and wrapping a `MeterData` v0.6 payload — the same credential AMISPs and MDMs issue provider-to-DISCOM in the Beckn data-exchange flow. Only the trigger differs: the consumer requests it for a period.

The envelope — `issuer` (with regulatory `licenseNumber`), `validFrom` / `validUntil`, DeDi `credentialStatus`, `proof` — is inherited from `EnergyCredential` v2.0. What the Digest defines is `credentialSubject.meterData`: a `MeterData` v0.6 payload of one or more typed profiles.

```
MeterDataCredential  (W3C VC 2.0  ·  subclass of EnergyCredential v2.0)
├─ @context        W3C credentials/v2 + EnergyCredential v2.0 + MeterDataCredential v0.6
├─ type            ["VerifiableCredential", "MeterDataCredential"]
├─ issuer          id, name, licenseNumber  (DISCOM / AMISP / MDM DID)
├─ validFrom / validUntil                  (inherited envelope)
├─ credentialStatus  DeDi revocation registry  (inherited)
├─ credentialSubject
│  ├─ id           consumer / asset DID
│  └─ meterData    MeterData v0.6 payload — single profile OR array of profiles
│                  profileType ∈ CUSTOMER | INTERVAL | DAILY | MONTHLY |
│                  BILL_DETAILS | INSTANTANEOUS | EVENT | ALARM | DESCRIPTOR
└─ proof           Ed25519Signature2020
```

The **period and shape** the consumer chose are expressed by the profiles themselves:

- A **twelve-month statement** is a `MONTHLY` profile (a `P1M` interval-block array).
- **Raw analytics data** is an `INTERVAL` profile (`PT15M` / `PT30M` blocks, ~96 readings a day), optionally preceded by a `DESCRIPTOR` profile that the interval blocks reference via `payloadDescriptorSetRef`.

A monthly-bill view and a 15-minute analytics feed are the **same credential type** with different `meterData` profiles. The consumer's requested window simply bounds which profiles the DISCOM returns — within the scope authorised by the originating request.

### Example — a twelve-month statement (`MONTHLY` profile)

This is the exact JSON-LD that travels in `VcContent`.

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://schema.beckn.io/EnergyCredential/v2.0/context.jsonld",
    "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/context.jsonld"
  ],
  "id": "urn:uuid:9b3c1f0a-2d4e-4ba8-9f1c-1e7a90c8a5d2",
  "type": ["VerifiableCredential", "MeterDataCredential"],
  "issuer": {
    "id": "did:web:ies.discom.example",
    "name": "Example State Distribution Company Limited",
    "licenseNumber": "SERC-DISCOM-2025-007"
  },
  "validFrom": "2026-05-15T10:00:00+05:30",
  "validUntil": "2027-05-15T10:00:00+05:30",
  "credentialStatus": {
    "id": "https://dedi.global/dedi/lookup/discom/vc-revocation-registry/9b3c1f0a",
    "type": "dedi",
    "statusPurpose": "revocation"
  },
  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
    "meterData": {
      "profileType": "MONTHLY",
      "meterId": "MTR-98765432",
      "servicePointId": "DISCOM-2025-001234567",
      "intervalBlocks": [
        { "start": "2025-05-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 391, "unit": "kWh" }] },
        { "start": "2025-06-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 412, "unit": "kWh" }] },
        { "start": "2025-07-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 478, "unit": "kWh" }] },
        { "start": "2025-08-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 463, "unit": "kWh" }] },
        { "start": "2025-09-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 421, "unit": "kWh" }] },
        { "start": "2025-10-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 384, "unit": "kWh" }] },
        { "start": "2025-11-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 352, "unit": "kWh" }] },
        { "start": "2025-12-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 339, "unit": "kWh" }] },
        { "start": "2026-01-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 367, "unit": "kWh" }] },
        { "start": "2026-02-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 358, "unit": "kWh" }] },
        { "start": "2026-03-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 405, "unit": "kWh" }] },
        { "start": "2026-04-01T00:00:00+05:30", "duration": "P1M", "readings": [{ "type": "ACTIVE_ENERGY_IMPORT", "value": 437, "unit": "kWh" }] }
      ]
    }
  },
  "proof": { "type": "Ed25519Signature2020", "proofValue": "z5wQ…" }
}
```

### Example — raw analytics (`INTERVAL` profile + `DESCRIPTOR`)

For raw analytics data the same wrapper carries an `INTERVAL` profile — `PT15M` blocks, around 96 readings a day — typically preceded by a `DESCRIPTOR` profile that the interval blocks reference via `payloadDescriptorSetRef`. The `meterData` value becomes an **array of profiles**:

```json
{
  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
    "meterData": [
      {
        "profileType": "DESCRIPTOR",
        "id": "desc-usage-15m",
        "payloadDescriptors": [
          { "type": "ACTIVE_ENERGY_IMPORT", "unit": "kWh", "readingType": "DIRECT_READ" }
        ]
      },
      {
        "profileType": "INTERVAL",
        "meterId": "MTR-98765432",
        "servicePointId": "DISCOM-2025-001234567",
        "payloadDescriptorSetRef": "desc-usage-15m",
        "intervalBlocks": [
          { "start": "2026-05-01T00:00:00+05:30", "duration": "PT15M", "readings": [{ "value": 0.18 }] },
          { "start": "2026-05-01T00:15:00+05:30", "duration": "PT15M", "readings": [{ "value": 0.16 }] }
        ]
      }
    ]
  }
}
```

### Mapping to DigiLocker as it works today

DigiLocker already does everything the Digest needs — the **same Pull URI mechanism** the electricity-connection credential uses. The Digest is a new document type returned through the same response, with the signed `MeterDataCredential` in `VcContent` and a rendered statement in `DocContent` / `DataContent`. The one change that matters is the document key.

| DigiLocker mechanism (today) | How the Digest uses it |
|---|---|
| Pull URI endpoint + DocType | `MPLTR` registered as an additional record for the Digest; DigiLocker calls the **same Pull URI** the connection credential uses. |
| URI — the document key | Put the period into the URI: `in.gov.{discom}-MPLTR-{consumerNo}-{YYYY-MM}`. This is the composite key that lets every period coexist instead of overwriting — **confirmed on the 12 June 2026 call**: URI uniqueness is managed on the issuer side, DigiLocker needs no change. |
| UDF request fields | Consumer number as `UDF1`; the period (or month) as a UDF — so the consumer pulls a chosen window, and a recurring pull fetches the current one. |
| `VcContent` (JSON-LD) | The signed `MeterDataCredential` as-is — proof intact — for verifiers to parse and check. |
| `DocContent` (PDF) / `DataContent` (XML) | A rendered statement card — consumption ladder or time-of-day — built from a configurable template, with a summary the consumer reads on screen. |
| OAuth consent pull (`/xml/{uri}`) | A third-party app pulls a chosen period directly with consumer consent — no app-switching. |

### The one real gap — the document key

The electricity bill and NYCER are keyed on the consumer number alone, so each refresh overwrites the last. The Digest must be keyed on **consumer number plus period**, so April's and May's statements sit side by side as distinct documents.

```python
# NYCER — overwrite on refresh (correct for a connection credential)
uri = f"in.gov.discom-NYCER-{consumer.consumer_number}"   # trailing segment is the required doc-id (see URI note in Step 6)

# MPLTR — period in the key, so every statement coexists
uri = f"in.gov.discom-MPLTR-{consumer.consumer_number}-{period}"   # period e.g. "2026-05" or "2025-05_2026-04"
```

### Issuing the Digest (`MeterDataCredential` v0.6)

Inside `handle_mpltr`, resolve the requested window from `UDF2`, query MDMS/MDM for the matching readings, build the `MeterData` v0.6 payload, and call OpenCred. For a consumer-pulled Digest, `validUntil` may be set **shorter than the v0.6 default** where a verifier wants freshness (loan applications often want fresh; subsidy portals tolerate a week).

```python
import requests
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

# 1. Resolve the requested window from UDF2 → (start, end, profile_type, uri_period)
window = resolve_period(udf2)            # e.g. "last-12-months" → MONTHLY, 2025-05..2026-04
readings = mdm.query(consumer.meter_id, window.start, window.end, window.granularity)

# 2. Build the MeterData v0.6 payload (single profile here; use an array for INTERVAL + DESCRIPTOR)
meter_data = {
    "profileType": window.profile_type,          # "MONTHLY" | "INTERVAL" | "DAILY" | …
    "meterId": consumer.meter_id,
    "servicePointId": consumer.consumer_number,
    "intervalBlocks": readings.to_interval_blocks(),
}

# 3. Issue via OpenCred — same instance, MeterDataCredential schema, short validUntil
credential_response = requests.post(
    "http://opencred:3100/v1/credentials/issue",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={
        "issuerDid":  ISSUER_DID,
        "schemaId":   "ies/meter-data-credential/v0.6",
        "additionalTypes": ["MeterDataCredential"],
        "proofFormat": "vc-jwt",
        "validFrom":  datetime.now(IST).isoformat(),
        "validUntil": (datetime.now(IST) + timedelta(days=7)).isoformat(),   # freshness window
        "subjectDid": holder_did,
        "credentialSubject": {
            "id": holder_did,
            "meterData": meter_data,
            # NeGD's identity-binding requirement applies here too, but MeterDataCredential v0.6
            # has no idRef (or equivalent) field on credentialSubject yet — see the schema-gap
            # note under Identity Binding. Until the schema adds one, render the DigiLocker ID
            # binding into DocContent only (see Step 6 below).
        },
        "revocationRegistryUrl": DEDI_REVOCATION_URL,
    }
).json()

vc_json = credential_response["credential"]

# Render the PDF with a separate packaging call (same pattern as NYCER, and
# Issue Credentials §2.10) — package the credential as issued, proof intact.
package_response = requests.post(
    "http://opencred:3100/v1/credentials/package",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={"credential": vc_json, "formats": ["pdf"]},
).json()
pdf_bytes = base64.b64decode(
    next(o for o in package_response["outputs"] if o["format"] == "pdf")["data"]
)

# Inject the schema-required issuer object (with licenseNumber) — same pattern as NYCER.
vc_json["issuer"] = {
    "id":   ISSUER_DID,
    "name": ISSUER_NAME,
    "licenseNumber": DISCOM_LICENSE_NUMBER,      # e.g. "SERC-DISCOM-2025-007"
}

# 4. Period-keyed URI — this is the one structural difference from NYCER
uri = f"in.gov.discom-MPLTR-{consumer.consumer_number}-{window.uri_period}"
```

Revocations are rare in practice — Digests are usually short-lived enough to expire before any revoke would matter — but when a revoke is needed, pass an optional `reason` such as `"data-correction"` or `"holder-request"` on `POST /v1/credentials/revoke`; see [Issue Credentials → Revoke](issue-credentials.md#id-2.8-revoke).

### What the consumer can do with it

Three actions, all on DigiLocker's existing rails:

1. **View** a readable statement card (rendered from `DocContent` / `DataContent`) — a consumption ladder or time-of-day profile, with a summary the consumer reads on screen.
2. **Download** the signed document locally.
3. **Share** it — by **QR scan** in person, or by granting **OAuth consent** so a third-party app pulls the chosen period directly, with no app-switching.

In every mode the signed JSON moves as-is (see [Step 5](#step-5-package-the-pdf-and-vc-for-the-response) above). Where DigiLocker adds the holder's own signature (e.g. on a QR-scan share), it must be an **envelope over the credential** — a verifiable-presentation pattern, not a reshaping of the credential body — so the issuer's proof stays intact and independently verifiable.

### The ask to DigiLocker (MPLTR)

| Capability | Status | What it means |
|---|---|---|
| Introduce the Digest document type | **Done** — NeGD has allotted `MPLTR` (Meter Document) | Register the Consumer Meter Digest (a `MeterDataCredential`) as `MPLTR` on API Setu, alongside the existing `NYCER` endpoint. |
| Key the URI on consumer + period | **Agreed in principle** on the 12 June 2026 call; written confirmation still owed | Put the period into the URI so multiple periods coexist rather than overwriting. URI uniqueness is managed issuer-side — DigiLocker needs no change, only to treat each unique URI as a distinct, independently listable/deletable document. |
| Accept period as a pull parameter | Open ask | Let the consumer pull a chosen historical window via `UDF2`, and let a recurring pull with the current period fetch the latest statement. |
| Render from a configurable template | Open ask | Drive the `DocContent` / `DataContent` card from an externalised, per-DocType renderer — not hardcoded fields — so the card need not change when a parameter does. |
| Position on optional `DocContent` for time-series types | Open ask — IES provides a simplified PDF meanwhile | Whether `DocContent` may be made optional for VC-only / time-series DocTypes in future, since the full ~96-blocks-a-day series lives only in `VcContent`. |

> Everything else reuses the connection-credential flow unchanged. Format is **W3C VC 2.0 JSON-LD** for both DocTypes (not SD-JWT) — selective disclosure via SD-JWT is a joint roadmap item once this initial integration is stable.

---

## Error Response Format

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIResponse ver="3.0" ts="{ts}" txn="{txn}" orgId="discom">
  <ResponseStatus Status="0" ts="{ts}" txn="{txn}">Consumer not found</ResponseStatus>
</PullURIResponse>
```

---

## Phase 2 — Consumer Shares Credential with a Verifier

Phase 2 requires no DISCOM involvement. Consumers share their NYCER credential or Meter Digest from DigiLocker using the standard DigiLocker OAuth flow. See [Issue Credentials → Verify](issue-credentials.md#id-2.7-verify) for the verifier-side implementation.

---

## Security Checklist

- [ ] HMAC verified on every inbound request before any processing
- [ ] `hmac.compare_digest` used (not `==`) to prevent timing attacks
- [ ] Raw request bytes used for HMAC computation (not re-serialised XML)
- [ ] `customerProfile.idRef` carries the `DigiLockerId` from the request (identity binding, per NeGD) — logged only where necessary, never alongside the full Aadhaar / government ID
- [ ] Digest `meterData` carries readings only — no PII beyond the consumer/meter identifiers needed to bind the statement
- [ ] Period UDF validated and bounded to the scope authorised by the originating request (no arbitrary historical ranges)
- [ ] API key stored in environment variable / secrets manager, not in code
- [ ] Endpoint accessible only over HTTPS (TLS 1.2+)
- [ ] Rate limiting applied (DigiLocker can retry aggressively on timeout)

---

## Reference

- [Consumer Meter Digest — use-case guide](../use-cases/consumer-meter-digest/README.md)
- [Electricity Credential — schema reference](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)
- [OpenCred Documentation](https://opencred.gitbook.io/docs) — credential service API reference
- [API Setu DigiLocker Partner Portal](https://partners.digitallocker.gov.in)
- [DigiLocker Technical Specification v1.0.5](https://partners.digitallocker.gov.in/assets/img/Digital%20Locker%20Technical%20Specification%20v1%200%205.pdf)

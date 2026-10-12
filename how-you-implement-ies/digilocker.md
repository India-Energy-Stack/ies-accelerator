# DigiLocker Delivery — DISCOM Guide

This guide covers everything your DISCOM needs to build the DigiLocker Pull URI endpoint — the single piece of custom code required to make IES energy credentials available to consumers in DigiLocker. It reflects the shape that NeGD's verifier accepts in production for the Consumer Energy Passport: the first DISCOM credential went end to end — pull, issue, store, QR-scan verify — in September 2026.

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
   │                         │── PullURIRequest ─────>│                    │
   │                         │                        │── CIS lookup       │
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
- an **org id** (`orgId`, e.g. `in.gov.discom` or `com.discom`) — DigiLocker stamps it on every `PullURIRequest` and it prefixes every document URI you return
- an **API key** — store this securely; DigiLocker derives the request `keyhash` from it

> If your DISCOM already issues electricity bills (`ELBIL`) on DigiLocker, contact NeGD to add the `NYCER` and `MPLTR` document types to your existing account. Do not re-register — the existing `orgId`, API key, parameter names and doc-id convention carry over.

Alongside the DocTypes, register your **credential issuer** with NeGD so DigiLocker can resolve and trust it. NeGD asks for a small block:

```json
{
  "credential_type": "UtilityElectricityCredential",
  "issuer_did": "did:web:www.discom.example:energystack",
  "resource_schema": []
}
```

The `issuer_did` is the one from [Step 2](#step-2-stand-up-opencred-and-your-issuer-did) — it may live on your own domain, or in a DigiLocker-hosted issuer namespace (e.g. `did:web:vc.dl6.in:issuers:in.gov.<state>electricity`) if NeGD hosts it for you. Give NeGD the DID **exactly as your `did.json` is served** (see the redirect note in Step 2): a `www.` host in the URL means a `www.` segment in the DID.

> **Keep the org id consistent across registration and every URI.** The org segment of each Pull URI (`{orgId}-{DocType}-{docId}`, e.g. `in.gov.discom-NYCER-100000012345`) must equal the `orgId` DigiLocker sends in the request, which is the issuer id you registered on API Setu. A URI whose org segment doesn't match the registered issuer fails at DigiLocker with an *org id / issuer id mismatch* — the response is accepted but its document data is rejected, which is easy to misread as a payload problem.

### Step 2 — Stand Up OpenCred and Your Issuer DID

Follow [Setting up Register — keypair and did.json](setup-register.md#id-1.2-generate-your-credential-signing-keypair) and [Issuing Credentials — run OpenCred](issue-credentials.md#id-3.3-run-opencred-in-did-web-mode) end-to-end. By the time you reach this page you should have:

- OpenCred **1.11.2 or newer** running with `signingKeyLoaded: true` — `ghcr.io/nfh-trust-labs/opencred/opencred-server:1.11.2`. This is the first release that issues the exact shape DigiLocker verifies: the `jws-2020` proof format, the IES v1.2 context bundled, and the flat `context.inline.jsonld` attached automatically ([release notes](https://github.com/nfh-trust-labs/opencred/releases)).
- An issuer DID — `did:web:ies.discom.example` (recommended) or `did:key:…` (from an imported DSC). The DID document publishes the P-256 key as `JsonWebKey2020` under `#key-0`; that is the `verificationMethod` DigiLocker resolves.
- (Optional, recommended) DeDi configured for revocation

Save your issuer DID — it goes into every `POST /v1/credentials/issue` call.

> **Gotcha — the DID host must serve `did.json` *without* a redirect.** A `did:web` DID resolves by fetching `https://<host>/<path>/did.json`. If that host 301-redirects — e.g. `https://discom.example/energystack/did.json` → `https://www.discom.example/energystack/did.json` — lenient verifiers follow the redirect, but strict resolvers (OpenCred among them) reject it, and a consumer's credential then fails to verify. Name the **canonical host that answers directly** in your DID: if `www.` is where `did.json` is served, the issuer DID is `did:web:www.discom.example:energystack`, not `did:web:discom.example:energystack`. Confirm with `curl -sSL -o /dev/null -w '%{http_code} %{url_effective}\n' https://<host>/<path>/did.json` — a `200` with an unchanged URL, not a `301`.

### Step 3 — Register the Pull URI Endpoints on API Setu

Register both DocTypes against the same Pull URI endpoint. They differ only in the request parameters and the URI key.

**NYCER — Electricity Credential v1.2**

| Field | Value |
|---|---|
| Endpoint URL | `https://{your-domain}/digilocker/pulluri` |
| HTTP Method | `POST` |
| Content-Type | `application/xml` |
| DocType | `NYCER` |
| Parameter 1 | `canumber` — *Consumer Number* |
| Parameter 2 | `rmn` — *Registered Mobile Number* |

**MPLTR — Consumer Meter Digest**

| Field | Value |
|---|---|
| Endpoint URL | `https://{your-domain}/digilocker/pulluri` |
| HTTP Method | `POST` |
| Content-Type | `application/xml` |
| DocType | `MPLTR` |
| Parameter 1 | `canumber` — *Consumer Number* |
| Parameter 2 | `period` — *Statement Period* (e.g. `2026-05` or `last-12-months`) |
| Parameter 3 | `rmn` — *Registered Mobile Number* |

> **Parameter names become XML element names.** Each parameter you register for a DocType arrives in `<DocDetails>` as an element of that name — DigiLocker's NYCER request to a DISCOM that already serves bills carries `<canumber>` and `<rmn>`, the same keys as `ELBIL`. Reuse your bill parameter names so one parser serves all three DocTypes, and parse by the names you registered, not by position.

> **MPLTR registers as an additional record on the same endpoint already registered for NYCER** — one Pull URI handler, branched by `DocType`. One item is still pending **written** confirmation from DigiLocker even though it was agreed in principle on the 12 June 2026 call: treating each **period-keyed URI** as a distinct, independently listable/deletable document (see [The Consumer Meter Digest](#the-consumer-meter-digest-doctype-mpltr)). **Configurable rendering** of the statement card remains an open ask. Everything else reuses the NYCER flow unchanged.

---

## Phase 1 — The Pull URI Endpoint

This is the **only endpoint your DISCOM builds**. DigiLocker calls it; you respond. A single handler serves both DocTypes — branch on `DocType` (see [Routing by DocType](#routing-by-doctype)).

### Endpoint Specification

```
POST https://{your-domain}/digilocker/pulluri
Content-Type: application/xml
```

The request is a `PullURIRequest` XML (v3.0). Authentication rides inside it: the root element carries a `keyhash` attribute that DigiLocker derives from **your API key** and the request timestamp `ts`, per the DigiLocker Issuer API specification you receive through API Setu.

### Step 1 — Authenticate the request

**Always check the request against your API key before doing anything else. Reject with HTTP 401 if it does not match.**

```python
import hashlib, hmac

def authenticate_pull_request(root_attrs: dict, api_key: str) -> bool:
    # keyhash: computed by DigiLocker from your API key and `ts`, exactly as the
    # Issuer API specification defines it (SHA-256, hex). Recompute and compare in
    # constant time; never compare with ==.
    expected = compute_keyhash(api_key, root_attrs["ts"])
    return hmac.compare_digest(expected, root_attrs.get("keyhash", ""))
```

If your `ELBIL` handler already validates `keyhash`, reuse that code — the mechanism is identical for `NYCER` and `MPLTR`. Also reject requests whose `ts` is stale (DigiLocker retries aggressively on timeout, so a short replay window keeps retries working while blocking replays).

### Step 2 — Parse the Inbound Request

DigiLocker sends a `PullURIRequest` XML v3.0. For NYCER, as DigiLocker actually sends it (parameter names as registered in Step 3):

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIRequest xmlns="https://www.digitallocker.gov.in/schema/issuer/v1/pullurirequest"
                ver="3.0"
                ts="2026-07-17T10:29:53+05:30"
                txn="TXN-20260717-001"
                orgId="in.gov.discom"
                keyhash="<sha256-hex>"
                format="pdf">
  <DocDetails>
    <DocType>NYCER</DocType>
    <DigiLockerId>7a3f9b2c-1e4d-4f8a-b6c2-0d5e8f1a2b3c</DigiLockerId>
    <rmn>9876543210</rmn>                  <!-- registered mobile number -->
    <canumber>100000012345</canumber>      <!-- consumer / CA number -->
  </DocDetails>
</PullURIRequest>
```

For MPLTR the period travels as a parameter, so the consumer can pull a chosen window:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIRequest xmlns="https://www.digitallocker.gov.in/schema/issuer/v1/pullurirequest"
                ver="3.0"
                ts="2026-05-15T10:00:00+05:30"
                txn="1784264394"
                orgId="in.gov.discom"
                keyhash="…"
                format="pdf">
  <DocDetails>
    <DocType>MPLTR</DocType>
    <DigiLockerId>7a3f9b2c-1e4d-4f8a-b6c2-0d5e8f1a2b3c</DigiLockerId>
    <canumber>100000012345</canumber>      <!-- consumer / CA number -->
    <period>last-12-months</period>        <!-- statement period: YYYY-MM, a range, or a keyword -->
    <rmn>9876543210</rmn>                  <!-- registered mobile number -->
  </DocDetails>
</PullURIRequest>
```

| Field | Description |
|---|---|
| `xmlns` | DigiLocker's issuer namespace — parse namespace-aware, or strip it; element names are otherwise as shown |
| `ts` | Request timestamp — echo in response; input to `keyhash` |
| `txn` | Transaction ID — echo in response |
| `orgId` | Your registered issuer id — the prefix of every URI you return |
| `keyhash` | Request authentication — see [Step 1](#step-1-authenticate-the-request) |
| `format` | Rendering DigiLocker wants in `DocContent` — `pdf` |
| `DigiLockerId` | The consumer's DigiLocker-registered ID. Carry it into the issued credential's identity binding for **both** DocTypes — see [Identity Binding — the DigiLocker ID](#identity-binding-the-digilocker-id). |
| `canumber` | Consumer number — primary CIS lookup key (the name you registered; `UDF1` in older DigiLocker material) |
| `rmn` | Registered mobile number — secondary verification |
| `period` (MPLTR) | Statement period — `YYYY-MM`, a range, or a keyword like `last-12-months`. A recurring pull with the current month fetches the latest statement. |

### Step 3 — Look Up Consumer in CIS

```python
consumer = cis.lookup(consumer_number=canumber, mobile=rmn)
if not consumer:
    return pulluri_error_response(ts, txn, status=0, message="Consumer not found")
```

### Identity Binding — the DigiLocker ID

`customerProfile.idRef` is the Passport's **external identity reference** — `{issuedBy, subjectId}`, where `issuedBy` must be a DID or URL (it is a JSON-LD `@id`; a display name breaks signing) and `subjectId` is `authority-domain:id-value`.

Two bindings are in use:

```python
# (a) Connection binding — what the first verified production Passport carries:
#     the issuing DISCOM vouches for the CA number.
holder_idref = {
    "issuedBy":  ISSUER_DID,                       # e.g. "did:web:www.discom.example:energystack"
    "subjectId": f"ca:{consumer.consumer_number}",
}

# (b) DigiLocker binding — NeGD's stated requirement: carry the <DigiLockerId>
#     from the PullURIRequest so the credential is tied to the DigiLocker account.
holder_idref = {
    "issuedBy":  "did:web:digilocker.gov.in",
    "subjectId": f"digilocker.gov.in:{digilocker_id}",
}
```

Both pass DigiLocker's verifier. Use (b) where NeGD asks for the DigiLocker binding; the rendered certificate (`DocContent`) should then also show it in human-readable form — e.g. *"Identity Binding: binding method DIGILOCKER_PULL, binding date …"* — the pattern an earlier pilot DISCOM followed. Keep the CA number in `customerProfile.customerNumber` either way.

> **Schema gap.** `customerProfile.idRef` exists on the [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) schema, so the Passport can carry this binding today. `MeterDataCredential` v0.6's `credentialSubject` does **not** yet define an `idRef` (or equivalent) property — until the schema adds one, the Digest cannot carry this binding as a structured VC field, only in the rendered `DocContent`. Track this as an open schema item alongside the MPLTR rollout.

### Step 4 — Call OpenCred to Issue the Credential

This step differs by DocType — see [Issuing NYCER (v1.2)](#the-opencred-issue-call) and [Issuing the Digest (MPLTR)](#issuing-the-digest-meterdatacredential-v0.6) below. NYCER is issued with `proofFormat: "jws-2020"` — a `JsonWebSignature2020` proof with a detached JWS, the proof shape DigiLocker's verifier checks. Both return a signed VC, then render the PDF with a **separate** `POST /v1/credentials/package` call (see [Step 5](#step-5-package-the-pdf-and-vc-for-the-response)).

### Step 5 — Package the PDF and VC for the response

Rendering the PDF is a **separate call** — `POST /v1/credentials/package` with `formats: ["pdf"]` (the DocType handlers in Step 4 make it). An inline `packageFormats` field on the *issue* body is silently ignored, so this call is not optional — see [Issuing Credentials §3.10](issue-credentials.md#id-3.10-package-the-credential-as-a-pdf-qr-code). The PDF carries the signed credential payload in its info dictionary and embeds a scannable QR — DigiLocker stores the PDF, and verifiers can later re-extract the credential from the PDF itself.

The OpenCred-rendered certificate is an A4 card: *Electricity Credential · Issued by `<issuer DID>`*, a **Scan to verify** QR, *Issued to* (the subject DID) and *Validity*, then every `credentialSubject` field in a nested **Credential Details** table (customer details, consumption profile with `{value, unit}` pairs rendered as *value / unit*, energy resources, the identity binding), and a **Digital Signature** block showing proof type `JsonWebSignature2020`, algorithm `ES256`, created date and the `#key-0` verification method.

```python
import base64, json

# pdf_bytes came back from the /v1/credentials/package call in Step 4
pdf_b64 = base64.b64encode(pdf_bytes).decode()

# vc_json is the credential EXACTLY as OpenCred returned it. Do not add, rename or
# reorder anything — the jws-2020 proof covers the canonical form of the whole
# document, and DigiLocker re-verifies that signature when the consumer scans the QR.
vc_b64  = base64.b64encode(json.dumps(vc_json, separators=(",", ":")).encode()).decode()
```

For a custom PDF design (branded letterhead, regional language, a consumption-ladder or time-of-day card), render server-side with your own template engine and embed the QR + credential JSON as you prefer. `VcContent` is what verifiers actually parse — the PDF is for human display only and can't be checked against the issuer's signature.

### Step 6 — Return the PullURIResponse

```python
def build_pulluri_response(ts, txn, org_id, doc_type, uri, issued_to, valid_from, valid_to, pdf_b64, vc_b64):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIResponse ver="3.0" ts="{ts}" txn="{txn}" orgId="{org_id}">
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
| `orgId` | Echo the `orgId` from the request. |
| `URI` | Unique identifier for this document in DigiLocker — `{orgId}-{DocType}-{docId}`. The final **doc-id** segment is **required**: NeGD rejects a URI that ends at the DocType with no doc-id. Form it the same way your existing electricity-bill (`ELBIL`) integration forms its doc-id; for a connection-keyed credential the CA / consumer number serves this role. NYCER: `{orgId}-NYCER-{consumerNo}`, e.g. `in.gov.discom-NYCER-100000012345`. MPLTR: `{orgId}-MPLTR-{consumerNo}-{period}` — **the period makes each statement a distinct document** (see [The document key](#the-one-real-gap-the-document-key)). |
| `IssuedTo` | Consumer's full name — DigiLocker validates this against the user's profile |
| `ValidFrom` / `ValidTo` | Mirror the credential's `validFrom` / `validUntil` (date part, `dd-mm-yyyy` as in your `ELBIL` response) so the wallet entry and the credential expire together |
| `DocContent` | Base64-encoded PDF (the rendered statement / certificate card) |
| `VcContent` | Base64-encoded W3C VC JSON-LD — the signed credential, byte-for-byte as issued, proof intact |
| `VcType` | Media type of the `VcContent` payload — **`application/ld+json`**. Required by NeGD **immediately after** `VcContent`; a response without it is rejected. |

### Handler Logic Summary

```
1. Parse XML → root attrs (ts, txn, orgId, keyhash, format) + DocType, DigiLockerId, parameters
2. Authenticate (keyhash vs your API key) → HTTP 401 if invalid
3. Lookup consumer in CIS → error response if not found
4. Resolve / generate the consumer's holder DID
5. Branch on DocType:
     NYCER → build v1.2 credentialSubject (energyResources[], ids as absolute URIs)
     MPLTR → build MeterData v0.6 payload for the requested period
6. POST /v1/credentials/issue (NYCER: proofFormat "jws-2020") → signed VC
7. POST /v1/credentials/package (formats=["pdf"]) → PDF
8. Base64-encode PDF and the UNMODIFIED VC
9. Return PullURIResponse XML with Status=1, VcType after VcContent, and the DocType-appropriate URI
```

### Routing by DocType

```python
doc_type = request_xml.find(".//{*}DocType").text
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

`NYCER` is the existing, unchanged DocType; only its payload schema is upgraded. The earlier NYCER credential carried a flat set of customer-and-connection fields. The IES Electricity Credential, finalised at **v1.2** as the **Consumer Energy Passport**, carries far more: every physical asset behind the connection — meter, solar, battery, EV, inverter, controllable load — as one typed resource model with unit-bearing quantities.

### What changed from the flat shape

| | Earlier (flat) | v1.2 Electricity Credential |
|---|---|---|
| Customer & connection | Flat fields on `credentialSubject` | Non-PII `customerProfile` + PII `customerDetails` |
| Meter | `meterNumber` / `meterType` fields | `energyResources` entry, `type` `METER`, `attributes.meterCapability` + `energyDirection` |
| Generation, storage, EV, … | Not carried | Typed resources — `SOLAR_PV`, `BESS`, `EV_CHARGER`, `INVERTER`, … |
| Power & capacity values | n/a | `QuantitativeValue` `{value, unit}` — e.g. `maxExport {10, kW}` |
| Asset topology | Not carried | `parentResources` / `subResources` — submetering, parallel metering |
| Consumption / tariff | Not carried | `consumptionProfiles[]`, `sanctionedLoad` as `{value, unit}` |
| Proof | `vc-jwt` envelope (`proof.jwt`) | `JsonWebSignature2020` with a detached `jws` (`proofFormat: "jws-2020"`) |
| Schema reference | `credentialSchema` pointing at a GitHub page | Hosted IES contexts in `@context`; `credentialSchema.id` is the published `schema.json` |

### credentialSubject shape

```
credentialSubject
├─ id                       (optional)  customer DID
├─ customerProfile          (required)  non-PII
│  ├─ customerNumber        (required)  utility CA number
│  ├─ idRef                 (optional)  identity binding — CA number or the DigiLocker ID from the pull request
│  ├─ energyResources[]     (required)  typed assets, min 1 (at least one METER); every id an absolute URI
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

### Payload rules for a signable credential

`jws-2020` signs the **JSON-LD canonical form** of the credential in strict mode. Anything the context cannot interpret is refused at issue time (OpenCred names the field) rather than silently dropped from the signature. Three rules follow:

| Rule | Why | Do this |
|---|---|---|
| Every `id` is an **absolute URI** | `energyResources[].id` (and `credentialSubject.id`) are JSON-LD `@id` values; a bare serial such as `MTR0012345` is a relative IRI | `"id": "urn:ies:meter:MTR0012345"` (or a `did:web:…:assets:meter:MTR0012345`). `consumptionProfiles[].meterId` may stay the bare serial — it is a plain string, not an `@id`. |
| `idRef.issuedBy` is a **DID or URL** | typed `@id` in the context | the issuer DID, `did:web:digilocker.gov.in`, or a regulator URL — never a display name |
| **No fields outside v1.2** | an undefined property has no IRI and cannot be signed | put a mobile number, meter-reader code or any CIS extra in `DocContent`, not in `credentialSubject` |

Enumerations and free-text values are unaffected: `tariffCategoryCode`, `premisesType`, `connectionType` and `addressCountry` carry whatever your CIS holds (`"LT-RES-1"`, `"Commercial"`, `"Single-phase"`, `"India"`).

### The OpenCred issue call

```python
import base64, requests
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))
holder_did = f"{ISSUER_DID}:customer:{consumer.consumer_number}"   # issuer-domain subject DID

credential_response = requests.post(
    "http://opencred:3100/v1/credentials/issue",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={
        "issuerDid":  ISSUER_DID,                # e.g. "did:web:www.discom.example:energystack"
        "schemaId":   "ies/electricity-credential/v1.2",
        "additionalTypes": ["ElectricityCredential"],
        "proofFormat": "jws-2020",               # JsonWebSignature2020, detached JWS — what DigiLocker verifies
        "validFrom":  datetime.now(IST).isoformat(),
        "validUntil": (datetime.now(IST) + timedelta(days=180)).isoformat(),   # your policy; 6–12 months is typical
        "subjectDid": holder_did,
        "credentialSubject": {
            "id": holder_did,
            "customerProfile": {
                "customerNumber": consumer.consumer_number,
                "idRef": {
                    "issuedBy":  ISSUER_DID,                              # or did:web:digilocker.gov.in — see Identity Binding
                    "subjectId": f"ca:{consumer.consumer_number}",        # or digilocker.gov.in:{digilocker_id}
                },
                "energyResources": [
                    {
                        "id":   f"urn:ies:meter:{consumer.meter_id}",     # absolute URI — a bare serial is rejected
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
                    #    each linked to the meter via "parentResources": ["urn:ies:meter:…"]
                ],
                "consumptionProfiles": [
                    {
                        "meterId":           consumer.meter_id,              # plain string; bare serial is fine here
                        "sanctionedLoad":    {"value": consumer.sanctioned_load_kw, "unit": "kW"},
                        "contractMaxDemand": {"value": consumer.contract_demand_kw, "unit": "kW"},
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
                    "geo": {"type": "Point",
                            "coordinates": [consumer.longitude, consumer.latitude]},
                    "address": {
                        "streetAddress":   consumer.address_line,
                        "extendedAddress": consumer.area,
                        "addressLocality": consumer.city,
                        "addressRegion":   consumer.state,
                        "postalCode":      consumer.pincode,
                        "addressCountry":  "India",
                    },
                },
                "serviceConnectionDate": consumer.connection_date.isoformat(),
            },
        },
        "revocationRegistryUrl": DEDI_REVOCATION_URL,   # optional; omit if DeDi is not configured
    }
).json()

vc_json = credential_response["credential"]     # send this to DigiLocker exactly as returned

# Render the PDF with a SEPARATE packaging call. Packaging is a distinct
# rendering step, not part of issue — an inline `packageFormats` field on the
# issue body is silently ignored (see Issuing Credentials §3.10). Package the
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
```

> **Do not edit the credential after issue.** OpenCred returns `issuer` as the DID string and sets `credentialSchema` itself. Adding an issuer `name`, re-ordering keys or injecting any field after signing changes the canonical form and the detached JWS no longer verifies — DigiLocker rejects the QR. If you need a richer `issuer` object, raise it as an issuance-time feature with OpenCred rather than patching the output.

The URI for NYCER stays keyed on the consumer number — a refresh overwrites the last, which is correct for a slow-changing connection credential:

```python
uri = f"{org_id}-NYCER-{consumer.consumer_number}"   # trailing segment is the required doc-id (see URI note in Step 6)
```

### What goes into `VcContent`

The credential OpenCred returns — and that DigiLocker verifies — has this envelope (subject trimmed):

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.inline.jsonld",
    "https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.jsonld",
    "https://w3id.org/security/suites/jws-2020/v1"
  ],
  "id": "urn:uuid:3f2a9c1e-5b7d-4e8a-9c21-0d4f6a7b8c9e",
  "type": ["VerifiableCredential", "ElectricityCredential"],
  "issuer": "did:web:www.discom.example:energystack",
  "validFrom": "2026-10-01T04:30:00Z",
  "validUntil": "2027-04-01T04:30:00Z",
  "credentialSchema": {
    "id": "https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json",
    "type": "JsonSchema"
  },
  "credentialSubject": {
    "id": "did:web:www.discom.example:energystack:customer:100000012345",
    "customerProfile": {
      "customerNumber": "100000012345",
      "idRef": { "issuedBy": "did:web:www.discom.example:energystack", "subjectId": "ca:100000012345" },
      "energyResources": [
        { "id": "urn:ies:meter:MTR0012345", "type": "METER", "attributes": { "meterCapability": "AMI" } }
      ],
      "consumptionProfiles": [
        { "meterId": "MTR0012345", "connectionType": "Single-phase", "premisesType": "Residential",
          "sanctionedLoad": { "value": 5, "unit": "kW" }, "contractMaxDemand": { "value": 5, "unit": "kW" },
          "tariffCategoryCode": "LT-RES-1" }
      ]
    },
    "customerDetails": { "fullName": "…", "installationAddress": { "address": { "…": "…" }, "geo": { "type": "Point", "coordinates": [77.209, 28.614] } },
                         "serviceConnectionDate": "2021-06-15T00:00:00Z" }
  },
  "proof": {
    "type": "JsonWebSignature2020",
    "created": "2026-10-01T04:30:01Z",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:web:www.discom.example:energystack#key-0",
    "jws": "eyJhbGciOiJFUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..<signature>"
  }
}
```

What each part is for:

| Part | Why it is there |
|---|---|
| `context.inline.jsonld` **before** `context.jsonld` | DigiLocker's verifier does not resolve JSON-LD 1.1 `@import` or scoped contexts, so with `context.jsonld` alone it reports `MISSING_KEY` for `meterId`, `sanctionedLoad`, `unit`, `value`, `geo`, `postalCode`, … — twenty terms it cannot see. The [flat companion context](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.inline.jsonld) defines every field once at the top level, so the verifier finds them. Listed first, v1.2's definitions still win, so the canonical form — and therefore the signature — is identical to a v1.2-only credential. OpenCred 1.11.2+ adds both automatically for `ies/electricity-credential/v1.2`; you do not pass `@context` yourself. |
| `jws-2020/v1` suite context + `JsonWebSignature2020` proof | The proof shape NeGD specified: `created`, `proofPurpose`, `verificationMethod` (`…#key-0`, resolved from your `did.json`) and a **detached** RFC 7797 `jws` — header `{"alg":"ES256","b64":false,"crit":["b64"]}`, empty payload segment, signature. Replaces the earlier `proof.jwt` envelope, which DigiLocker could not verify. |
| `credentialSchema` → published `schema.json` | The JSON Schema the credential conforms to, at the IES GitHub Pages host — not a link to a GitHub source page. OpenCred sets it from the schema registry. |
| `issuer` as a string, `credentialSubject.id` as a DID | Both resolve as identifiers. The subject DID under the issuer's own namespace (`…:customer:<CA>`) gives a stable, correlatable subject without PII. |

### What DigiLocker's verifier checks

DigiLocker verifies `VcContent` when the document is stored and again every time the QR is scanned. NeGD exposes the same verifier so you can test before registering:

```bash
curl --location 'https://beta-verify-credentials.dl6.in/api/2/verify' \
  --header 'Content-Type: application/ld+json' \
  --data @credential.json        # the VcContent JSON, decoded
```

| Result | Meaning | Fix |
|---|---|---|
| `"verified": true` | Signature, `did.json` resolution and every field's context definition passed — the same credential will pass in DigiLocker | — |
| `"error": "MISSING_KEY"`, `err_desc: "Jsonld keys are missing in context desc - […]"` | A listed field has no top-level definition in any `@context` entry the verifier can read | Issue with OpenCred 1.11.2+ (adds `context.inline.jsonld`); if you build `@context` yourself, list the inline context before `context.jsonld` |
| Signature failure | `did.json` not resolvable at the exact DID host (redirect), wrong `verificationMethod`, or the credential was modified after issue | See the redirect gotcha in Step 2; send `VcContent` byte-for-byte as issued |

Beyond the credential itself, DigiLocker checks the envelope: `VcType` present right after `VcContent`, a URI with a doc-id whose org segment equals your registered `orgId`, and `IssuedTo` matching the account holder's name.

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

- A **twelve-month statement** is an array of `MONTHLY` profiles — one `MonthlyProfile` object per month, each with a `timePeriod` (`P1M`) and its `readings`.
- **Raw analytics data** is an `INTERVAL` profile (`PT15M` / `PT30M` intervals, ~96 readings a day), preceded by a `DESCRIPTOR` profile that the interval profile references via `payloadDescriptorSetRef` / `compactSequenceRef`.

A monthly-bill view and a 15-minute analytics feed are the **same credential type** with different `meterData` profiles. The consumer's requested window simply bounds which profiles the DISCOM returns — within the scope authorised by the originating request.

### Example — a twelve-month statement (`MONTHLY` profile)

The JSON-LD that travels in `VcContent`, per the canonical MeterDataCredential v0.6 monthly example — one `MonthlyProfile` per month, carried as an array (trimmed proof; first month shown in full):

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://schema.nfh.global/EnergyCredential/v2.0/context.jsonld",
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
    "id": "https://dedi.global/dedi/query/did:web:ies.discom.example/vc-revocation-registry",
    "type": "dediregistry",
    "statusPurpose": "revocation",
    "statusListCredential": "https://dedi.global/dedi/lookup/did:web:ies.discom.example/vc-revocation-registry"
  },
  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
    "meterData": [
      {
        "@context": "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/context.jsonld",
        "@type": "MonthlyProfile",
        "profileType": "MONTHLY",
        "meterRefs": [
          { "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }
        ],
        "serviceDeliveryPointRefs": [
          { "scheme": "DID", "value": "did:web:ies.discom.example:connections:SDP-A-12345" }
        ],
        "timePeriod": { "start": "2025-05-01T00:00:00+05:30", "duration": "P1M" },
        "readings": [
          { "readingType": "kWh imp", "value": 391.0, "validationStatus": "VALID", "source": "METER" }
        ]
      },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-06-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 412.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-07-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 478.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-08-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 463.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-09-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 421.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-10-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 384.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-11-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 352.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-12-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 339.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2026-01-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 367.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2026-02-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 358.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2026-03-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 405.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2026-04-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 437.0 }] }
    ]
  },
  "proof": { "type": "Ed25519Signature2020", "proofValue": "z5wQ…" }
}
```

### Example — raw analytics (`INTERVAL` profile + `DESCRIPTOR`)

For raw analytics data the same wrapper carries an `INTERVAL` profile — `PT15M` intervals, around 96 readings a day — preceded by a `DESCRIPTOR` profile the interval profile references via `payloadDescriptorSetRef` and `compactSequenceRef`. The `meterData` value is an **array of profiles** (fragment, per the canonical v0.6 interval example; envelope as in the statement example above):

```json
{
  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
    "meterData": [
      {
        "@context": "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/context.jsonld",
        "@type": "PayloadDescriptorProfile",
        "profileType": "DESCRIPTOR",
        "id": "DESC-INTERVAL-2026Q2",
        "payloadDescriptorSets": [
          {
            "name": "IntervalLoadSurveySet",
            "payloadDescriptors": [
              { "readingType": "kWh imp block", "name": "Active energy import – block incremental", "unit": "kWh", "flowDirection": "IMPORT", "reportedMode": "USAGE", "obis": "1.0.1.29.0.255" }
            ],
            "compactSequences": [
              { "name": "IntervalSeq", "sequenceItems": [{ "readingType": "kWh imp block" }] }
            ]
          }
        ]
      },
      {
        "@context": "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/context.jsonld",
        "@type": "IntervalProfile",
        "profileType": "INTERVAL",
        "meterRefs": [
          { "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }
        ],
        "payloadDescriptorSetRef": "DESC-INTERVAL-2026Q2",
        "compactSequenceRef": "IntervalSeq",
        "intervalPeriod": { "start": "2026-05-01T00:00:00+05:30", "duration": "PT15M" },
        "intervals": [
          { "id": 0, "payloads": [0.18] },
          { "id": 1, "payloads": [0.16] }
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
| URI — the document key | Put the period into the URI: `{orgId}-MPLTR-{consumerNo}-{YYYY-MM}`. This is the composite key that lets every period coexist instead of overwriting — **confirmed on the 12 June 2026 call**: URI uniqueness is managed on the issuer side, DigiLocker needs no change. |
| Request parameters | Consumer number as `canumber`; the period (or month) as a registered `period` parameter — so the consumer pulls a chosen window, and a recurring pull fetches the current one. |
| `VcContent` (JSON-LD) | The signed `MeterDataCredential` as-is — proof intact — for verifiers to parse and check. |
| `DocContent` (PDF) / `DataContent` (XML) | A rendered statement card — consumption ladder or time-of-day — built from a configurable template, with a summary the consumer reads on screen. |
| OAuth consent pull (`/xml/{uri}`) | A third-party app pulls a chosen period directly with consumer consent — no app-switching. |

### The one real gap — the document key

The electricity bill and NYCER are keyed on the consumer number alone, so each refresh overwrites the last. The Digest must be keyed on **consumer number plus period**, so April's and May's statements sit side by side as distinct documents.

```python
# NYCER — overwrite on refresh (correct for a connection credential)
uri = f"{org_id}-NYCER-{consumer.consumer_number}"   # trailing segment is the required doc-id (see URI note in Step 6)

# MPLTR — period in the key, so every statement coexists
uri = f"{org_id}-MPLTR-{consumer.consumer_number}-{period}"   # period e.g. "2026-05" or "2025-05_2026-04"
```

### Issuing the Digest (`MeterDataCredential` v0.6)

Inside `handle_mpltr`, resolve the requested window from the `period` parameter, query MDMS/MDM for the matching readings, build the `MeterData` v0.6 payload, and call OpenCred. For a consumer-pulled Digest, `validUntil` may be set **shorter than the v0.6 default** where a verifier wants freshness (loan applications often want fresh; subsidy portals tolerate a week).

```python
import requests
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

# 1. Resolve the requested window from the period parameter → (start, end, profile_type, uri_period)
window = resolve_period(period)            # e.g. "last-12-months" → MONTHLY, 2025-05..2026-04
readings = mdm.query(consumer.meter_id, window.start, window.end, window.granularity)

# 2. Build the MeterData v0.6 payload — an array of profile objects
#    (one MonthlyProfile per month for a statement; DESCRIPTOR + INTERVAL for analytics).
#    Every profile carries the required meterRefs; readings use the v0.6 Reading shape
#    (readingType / value / openingValue / closingValue / validationStatus / source).
meter_data = [
    {
        "@context": "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/context.jsonld",
        "@type": "MonthlyProfile",
        "profileType": "MONTHLY",
        "meterRefs": [{"scheme": "DID", "value": consumer.meter_did}],
        "serviceDeliveryPointRefs": [{"scheme": "DID", "value": consumer.sdp_did}],
        "timePeriod": {"start": month.start.isoformat(), "duration": "P1M"},
        "readings": [
            {"readingType": "kWh imp", "value": month.kwh_import,
             "validationStatus": "VALID", "source": "METER"}
        ],
    }
    for month in readings.by_month()
]

# 3. Issue via OpenCred — same instance, MeterDataCredential schema, short validUntil
credential_response = requests.post(
    "http://opencred:3100/v1/credentials/issue",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={
        "issuerDid":  ISSUER_DID,
        "schemaId":   "ies/meter-data-credential/v0.6",
        "additionalTypes": ["MeterDataCredential"],
        "proofFormat": "vc-jwt",      # jws-2020 is not yet available for this schema — see note below
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
# Issuing Credentials §3.10) — package the credential as issued, proof intact.
package_response = requests.post(
    "http://opencred:3100/v1/credentials/package",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={"credential": vc_json, "formats": ["pdf"]},
).json()
pdf_bytes = base64.b64decode(
    next(o for o in package_response["outputs"] if o["format"] == "pdf")["data"]
)

# Send vc_json to DigiLocker exactly as returned — do not inject an issuer object or
# any other field after signing (same rule as NYCER; see "Do not edit the credential
# after issue"). The regulatory licenseNumber belongs in your DID document / registry
# entry until OpenCred supports a structured issuer object at issuance time.

# 4. Period-keyed URI — this is the one structural difference from NYCER
uri = f"{org_id}-MPLTR-{consumer.consumer_number}-{window.uri_period}"
```

> **Proof format for the Digest.** OpenCred's canonicalizing formats (`jws-2020`, `data-integrity`) need the credential's JSON-LD context bundled in OpenCred; that is done for ElectricityCredential v1.2 but not yet for MeterDataCredential v0.6, so the Digest is issued with `vc-jwt` for now. Expect to switch to `jws-2020` — the shape DigiLocker verifies for NYCER — once that lands; the request body is otherwise unchanged.

Revocations are rare in practice — Digests are usually short-lived enough to expire before any revoke would matter — but when a revoke is needed, pass an optional `reason` such as `"data-correction"` or `"holder-request"` on `POST /v1/credentials/revoke`; see [Issuing Credentials → Revoke](issue-credentials.md#id-3.8-revoke).

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
| Accept period as a pull parameter | Open ask | Let the consumer pull a chosen historical window via the `period` parameter, and let a recurring pull with the current period fetch the latest statement. |
| Render from a configurable template | Open ask | Drive the `DocContent` / `DataContent` card from an externalised, per-DocType renderer — not hardcoded fields — so the card need not change when a parameter does. |
| Position on optional `DocContent` for time-series types | Open ask — IES provides a simplified PDF meanwhile | Whether `DocContent` may be made optional for VC-only / time-series DocTypes in future, since the full ~96-blocks-a-day series lives only in `VcContent`. |

> Everything else reuses the connection-credential flow unchanged. Format is **W3C VC 2.0 JSON-LD** for both DocTypes (not SD-JWT) — selective disclosure via SD-JWT is a joint roadmap item once this initial integration is stable.

---


---

## Error Response Format

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIResponse ver="3.0" ts="{ts}" txn="{txn}" orgId="{org_id}">
  <ResponseStatus Status="0" ts="{ts}" txn="{txn}">Consumer not found</ResponseStatus>
</PullURIResponse>
```

---

## Phase 2 — Consumer Shares Credential with a Verifier

Phase 2 requires no DISCOM involvement. Consumers share their NYCER credential or Meter Digest from DigiLocker using the standard DigiLocker OAuth flow, or present the QR on the certificate; DigiLocker re-verifies the credential's signature against your `did.json` on every scan. See [Issuing Credentials → Verify](issue-credentials.md#id-3.7-verify) for the verifier-side implementation.

---

## Security Checklist

- [ ] Request authenticated against your API Setu API key (`keyhash`) on every inbound request before any processing
- [ ] `hmac.compare_digest` used (not `==`) to prevent timing attacks; stale `ts` rejected
- [ ] `VcContent` is the credential exactly as OpenCred returned it — never edited, re-serialised with extra fields, or re-signed downstream
- [ ] `did.json` served at the exact DID host over HTTPS with no redirect, and the DID registered with NeGD spelled the same way
- [ ] `customerProfile.idRef.issuedBy` is a DID or URL; where the `DigiLockerId` is carried, it is logged only where necessary, never alongside the full Aadhaar / government ID
- [ ] No `credentialSubject` field outside ElectricityCredential v1.2 (no mobile numbers, no CIS extras) — they belong in `DocContent`
- [ ] Digest `meterData` carries readings only — no PII beyond the consumer/meter identifiers needed to bind the statement
- [ ] Period parameter validated and bounded to the scope authorised by the originating request (no arbitrary historical ranges)
- [ ] API key and OpenCred token stored in environment variables / a secrets manager, not in code
- [ ] Endpoint accessible only over HTTPS (TLS 1.2+)
- [ ] Rate limiting applied (DigiLocker can retry aggressively on timeout)
- [ ] OpenCred pinned to a tested release (1.11.2 or newer) and upgraded deliberately

---

## Reference

- [Consumer Meter Digest — use-case guide](../use-cases/consumer-meter-digest/README.md)
- [Electricity Credential — schema reference](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) · [`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.jsonld) · [`context.inline.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.inline.jsonld) (flat companion for verifiers without `@import` support) · [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json)
- [OpenCred Documentation](https://opencred.gitbook.io/docs) — credential service API reference · [releases](https://github.com/nfh-trust-labs/opencred/releases) (1.11.0 `jws-2020` + bundled IES v1.2 context · 1.11.1 strict-canonicalization diagnostics · 1.11.2 inline context attached)
- DigiLocker credential verifier (NeGD beta): `POST https://beta-verify-credentials.dl6.in/api/2/verify`, `Content-Type: application/ld+json`
- [API Setu](https://apisetu.gov.in) — DigiLocker issuer registration and partner documentation
- DigiLocker Issuer API / Pull URI specification (the former partner-portal download, `partners.digitallocker.gov.in`, is offline; obtain the current spec, including the `keyhash` construction, through your API Setu / NeGD contact)

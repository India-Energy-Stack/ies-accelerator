# DigiLocker Integration — DISCOM Guide

This guide covers everything your DISCOM needs to build the DigiLocker Pull URI endpoint — the single piece of custom code required to make IES electricity connection credentials (NYCER) available to consumers in DigiLocker.

---

## What DigiLocker Does

DigiLocker is India's national digital document wallet. When a consumer searches for their electricity connection credential in DigiLocker, DigiLocker calls your endpoint, your endpoint calls IES to issue a signed credential, and DigiLocker stores it — all in real time.

```
Consumer                 DigiLocker              Your Endpoint           IES
   │                         │                        │                    │
   │── search NYCER ────────>│                        │                    │
   │   (enter consumer no.)  │                        │                    │
   │                         │── PullURIRequest ─────>│                    │
   │                         │   (XML, HMAC signed)   │                    │
   │                         │                        │── /issue ─────────>│
   │                         │                        │<─ signed VC ───────│
   │                         │                        │── /credentials/{id}│
   │                         │                        │<─ PDF ─────────────│
   │                         │<── PullURIResponse ────│                    │
   │                         │   (XML + base64 PDF    │                    │
   │                         │    + base64 VC)         │                    │
   │<── credential saved ────│                        │                    │
```

---

## Flow Overview

The integration has three phases:

- **Phase 0 — One-time setup:** Register on API Setu, create issuer DID, register schema
- **Phase 1 — Pull URI endpoint:** Build and host the HTTPS endpoint DigiLocker calls
- **Phase 2 — Consumer sharing:** Consumers share the credential with verifiers via DigiLocker OAuth (no DISCOM involvement)

---

## Phase 0 — One-Time Setup

### Step 1 — Register on API Setu

Go to [https://apisetu.gov.in](https://apisetu.gov.in) and register as a document issuer. You receive:
- `issuer_id` (e.g. `in.gov.tpddl`)
- `api_key` — store this securely; used for HMAC verification

> If your DISCOM already issues electricity bills (ELBIL) on DigiLocker, contact NeGD to add the `NYCER` document type to your existing account. Do not re-register.

### Step 2 — Set Up Your Signing Key and Issuer DID

Using the **OpenCred Desktop Client** (or Docker API):

1. Generate an ECDSA P-256 keypair: Settings → Generate Key → **Generate ECDSA P-256 Key**
2. Enter your domain (e.g. `ies.tpddl.in`)
3. Download the DID document, upload it to `https://ies.tpddl.in/.well-known/did.json`
4. Your issuer DID is `did:web:ies.tpddl.in`

Alternatively, import an existing DSC (PFX/PEM) — OpenCred derives `did:key` from its public key.

Save your issuer DID — it goes into every `POST /v1/credentials/issue` call.

> See [OpenCred key management docs](https://opencred.gitbook.io/docs/desktop-client/key-management) for all key import options.

### Step 4 — Register Pull URI Endpoint on API Setu

| Field | Value |
|---|---|
| Endpoint URL | `https://{your-domain}/digilocker/pulluri` |
| HTTP Method | `POST` |
| Content-Type | `application/xml` |
| DocType | `NYCER` |
| UDF1 Label | `Consumer Number` |
| UDF2 Label | `Registered Mobile Number` |

---

## Phase 1 — The Pull URI Endpoint

This is the **only endpoint your DISCOM builds**. DigiLocker calls it; you respond.

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

DigiLocker sends a `PullURIRequest` XML v3.0:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIRequest ver="3.0"
                ts="2026-04-01T10:30:00+05:30"
                txn="TXN-20260401-001"
                orgId="tpddl">
  <DocDetails>
    <DocType>NYCER</DocType>
    <DigiLockerId>7a3f9b2c-1e4d-4f8a-b6c2-0d5e8f1a2b3c</DigiLockerId>
    <UDF1>TPDDL-2025-001234567</UDF1>   <!-- consumer number -->
    <UDF2>9876543210</UDF2>             <!-- registered mobile number -->
    <FullName>Priya Sharma</FullName>    <!-- optional, from DigiLocker profile -->
  </DocDetails>
</PullURIRequest>
```

| Field | Description |
|---|---|
| `ts` | Request timestamp — echo in response |
| `txn` | Transaction ID — echo in response |
| `UDF1` | Consumer number — primary CIS lookup key |
| `UDF2` | Registered mobile number — secondary verification |
| `FullName` | DigiLocker profile name — DigiLocker validates name match against your response |

### Step 3 — Look Up Consumer in CIS

```python
consumer = cis.lookup(consumer_number=udf1, mobile=udf2)
if not consumer:
    return pulluri_error_response(ts, txn, status=0, message="Consumer not found")
```

### Step 4 — Call OpenCred to Issue the Credential

```python
import requests

credential_response = requests.post(
    "http://localhost:3100/v1/credentials/issue",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={
        "issuer": ISSUER_DID,                    # e.g. "did:web:ies.tpddl.in"
        "credentialType": "ElectricityConnectionCredential",
        "proofFormat": "data-integrity",
        "credentialSubject": {
            "fullName": consumer.full_name,
            "consumerNumber": consumer.consumer_number,
            "serviceAddress": consumer.service_address,
            "serviceConnectionDate": consumer.connection_date.isoformat(),
            "meterNumber": consumer.meter_number,
            "maskedIdNumber": consumer.masked_aadhaar
        },
        "validFrom": datetime.utcnow().isoformat() + "Z",
        "validUntil": (datetime.utcnow() + timedelta(days=365)).isoformat() + "Z",
        "revocationRegistryUrl": DEDI_REVOCATION_URL
    }
).json()

vc_json = credential_response   # the full signed VC is the response body
```

### Step 5 — Render the PDF

OpenCred does not generate PDFs directly — render the signed VC JSON using your preferred PDF library or a template engine. Embed the VC JSON as a QR code on the PDF for verifier scanning.

```python
from your_pdf_lib import render_credential_pdf

pdf_bytes = render_credential_pdf(vc_json, template="nycer")
pdf_b64 = base64.b64encode(pdf_bytes).decode()
vc_b64 = base64.b64encode(json.dumps(vc_json).encode()).decode()
```

### Step 6 — Return the PullURIResponse

```python
def build_pulluri_response(ts, txn, consumer, pdf_b64, vc_b64):
    uri = f"in.gov.tpddl-NYCER-{consumer.consumer_number}"
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIResponse ver="3.0" ts="{ts}" txn="{txn}" orgId="tpddl">
  <ResponseStatus Status="1" ts="{ts}" txn="{txn}"/>
  <DocDetails>
    <DocType>NYCER</DocType>
    <URI>{uri}</URI>
    <IssuedTo>{consumer.full_name}</IssuedTo>
    <ValidFrom>{date.today().isoformat()}</ValidFrom>
    <ValidTo>{(date.today() + timedelta(days=365)).isoformat()}</ValidTo>
    <DocContent format="pdf">{pdf_b64}</DocContent>
    <VcContent format="json-ld">{vc_b64}</VcContent>
  </DocDetails>
</PullURIResponse>"""
```

| Field | Description |
|---|---|
| `Status="1"` | Success. Use `Status="0"` for errors. |
| `URI` | Unique identifier for this document in DigiLocker. Format: `{issuer_id}-{DocType}-{unique_key}` |
| `IssuedTo` | Consumer's full name — DigiLocker validates this against the user's profile |
| `DocContent` | Base64-encoded PDF |
| `VcContent` | Base64-encoded W3C VC JSON-LD |

### Handler Logic Summary

```
1. Read raw request body (keep bytes for HMAC)
2. Verify x-digilocker-hmac → HTTP 401 if invalid
3. Parse XML → extract UDF1, UDF2, ts, txn
4. Lookup consumer in CIS → error response if not found
5. POST /credential/credentials/issue → get credential_id + VC JSON
6. GET /credential/credentials/{id} → get PDF bytes
7. Base64-encode PDF and VC
8. Return PullURIResponse XML with Status=1
```

---

## Error Response Format

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIResponse ver="3.0" ts="{ts}" txn="{txn}" orgId="tpddl">
  <ResponseStatus Status="0" ts="{ts}" txn="{txn}">Consumer not found</ResponseStatus>
</PullURIResponse>
```

---

## Using a Common Endpoint for ELBIL and NYCER

If your DISCOM already serves electricity bills (DocType=`ELBIL`) from a Pull URI endpoint, you can add NYCER support to the same endpoint using the `DocType` field:

```python
doc_type = request_xml.find(".//DocType").text
if doc_type == "ELBIL":
    return handle_elbil(request_xml)
elif doc_type == "NYCER":
    return handle_nycer(request_xml)
```

---

## Phase 2 — Consumer Shares Credential with a Verifier

Phase 2 requires no DISCOM involvement. Consumers share their NYCER credential from DigiLocker using the standard DigiLocker OAuth flow. See [Verifying Credentials](./verification.md) for the verifier-side implementation.

---

## Security Checklist

- [ ] HMAC verified on every inbound request before any processing
- [ ] `hmac.compare_digest` used (not `==`) to prevent timing attacks
- [ ] Raw request bytes used for HMAC computation (not re-serialised XML)
- [ ] `maskedIdNumber` — full Aadhaar never stored or logged
- [ ] API key stored in environment variable / secrets manager, not in code
- [ ] Endpoint accessible only over HTTPS (TLS 1.2+)
- [ ] Rate limiting applied (DigiLocker can retry aggressively on timeout)

---

## Reference

- [OpenCred Documentation](https://opencred.gitbook.io/docs) — credential service API reference
- [API Setu DigiLocker Partner Portal](https://partners.digitallocker.gov.in)
- [DigiLocker Technical Specification v1.0.5](https://partners.digitallocker.gov.in/assets/img/Digital%20Locker%20Technical%20Specification%20v1%200%205.pdf)

# Issuance Reference Implementation

This is the "show me the code" page. It walks through, end-to-end, **how a DISCOM mints and registers every kind of identifier described in [ID Patterns](./id-patterns.md)** — from setting up the issuer DID to publishing a consumer reference and an asset record.

The examples are in Python with `requests`, but the calls are plain HTTPS and `openssl`. Translate to any stack.

---

## Prerequisites

- A domain you control: `ies.tpddl.in`.
- A static-file host that serves `https://ies.tpddl.in/.well-known/did.json`.
- The IES network operator has assigned you a DISCOM short code (`tpddl`) and provisioned your DeDi namespace.
- You hold the **namespace controller key** for `tpddl` — kept in a KMS, never exported. The IES operator's onboarding kit will have given you the key handle.
- OpenCred is running and configured with your signing key. See [Energy Credentials onboarding](../energy-credentials/onboarding.md).

---

## Step 1 — Mint the issuer DID (`did:web`)

Generate an ECDSA P-256 signing key:

```bash
openssl ecparam -name prime256v1 -genkey -noout -out issuer-key.pem
openssl ec -in issuer-key.pem -pubout -out issuer-pub.pem
```

Derive the JWK form:

```python
from jwcrypto import jwk

with open("issuer-pub.pem", "rb") as f:
    key = jwk.JWK.from_pem(f.read())
pub_jwk = key.export_public(as_dict=True)
# {"kty": "EC", "crv": "P-256", "x": "...", "y": "..."}
```

Build the DID Document:

```python
did = "did:web:ies.tpddl.in"
did_doc = {
    "@context": ["https://www.w3.org/ns/did/v1"],
    "id": did,
    "verificationMethod": [{
        "id": f"{did}#key-1",
        "type": "JsonWebKey2020",
        "controller": did,
        "publicKeyJwk": pub_jwk
    }],
    "assertionMethod": [f"{did}#key-1"],
    "service": [
        {"id": f"{did}#opencred", "type": "OpenCredIssuer",
         "serviceEndpoint": "https://ies.tpddl.in/v1/credentials"},
        {"id": f"{did}#beckn-bpp", "type": "BecknBPP",
         "serviceEndpoint": "https://ies.tpddl.in/beckn/bpp"}
    ]
}
```

Publish it at `https://ies.tpddl.in/.well-known/did.json`. That's the entirety of `did:web` setup.

Validate:

```bash
curl https://ies.tpddl.in/.well-known/did.json | jq .id
# "did:web:ies.tpddl.in"
```

---

## Step 2 — Register the DISCOM in the IES Reference Registry

You do not write to `india-energy-stack/ies-discoms-reference-registry/tpddl` directly. The IES network operator does, using their namespace key. You submit a registration request with:

| Field | Value |
|---|---|
| `id` | `tpddl` |
| `did` | `did:web:ies.tpddl.in` |
| `legalName` | `Tata Power Delhi Distribution Limited` |
| `publicKeys[0]` | The JWK from Step 1 |
| `serviceAreas` | `["DL"]` |
| `x5c` | (Optional) DSC chain if you anchor in CSCA |

Once accepted, your record is resolvable:

```bash
curl https://api.dedi.global/dedi/lookup/india-energy-stack/ies-discoms-reference-registry/tpddl
```

From this moment, your credentials are trusted on the network.

---

## Step 3 — Stand up your per-DISCOM revocation registry

Your DISCOM namespace is `tpddl`. Inside it, create the `vc-revocation-registry`:

```python
import requests, json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

NAMESPACE_DID  = "did:web:ies.tpddl.in"   # namespace controller DID
DEDI = "https://api.dedi.global/dedi"

def namespace_sign(payload: bytes) -> str:
    # Signs with the namespace controller key (KMS in production).
    ...

create_req = {
    "namespace": "tpddl",
    "registry":  "vc-revocation-registry",
    "schema":    "ies/revocation/v1",
    "controller": NAMESPACE_DID
}
sig = namespace_sign(json.dumps(create_req, separators=(",", ":")).encode())

r = requests.post(f"{DEDI}/create-registry",
                  json=create_req,
                  headers={"X-Signature": sig})
r.raise_for_status()
```

OpenCred is already configured to publish revocations here via `revocationRegistryUrl`:

```
https://api.dedi.global/dedi/lookup/tpddl/vc-revocation-registry/<credential-id>
```

---

## Step 4 — Mint and register a consumer reference ID

When a new consumer is provisioned in your CIS, derive their reference DID and write the (redacted) record to the public consumer registry. The full record lives in your private mirror.

```python
def consumer_did(consumer_number: str) -> str:
    safe = urllib.parse.quote(consumer_number, safe="")
    return f"did:dedi:tpddl:consumers:{safe}"

def register_consumer(consumer):
    public_record = {
        "id":     consumer_did(consumer.number),
        "city":   consumer.address.city,
        "state":  consumer.address.state,
        "tariff": consumer.tariff_category,
        "status": "active",
        "privateRef": f"https://internal-dedi.tpddl.in/dedi/lookup/tpddl-private/consumers-full/{consumer.number}",
        "createdAt": now_iso()
    }
    body = {
        "namespace": "tpddl",
        "registry":  "consumers",
        "recordId":  consumer.number,
        "record":    public_record,
        "controller": NAMESPACE_DID
    }
    sig = namespace_sign(json.dumps(body, separators=(",", ":")).encode())
    requests.post(f"{DEDI}/write",
                  json=body,
                  headers={"X-Signature": sig}).raise_for_status()

    # Mirror full PII record to the private DeDi.
    private_record = {
        **public_record,
        "name":    consumer.name,
        "address": consumer.address.full,
        "phone":   consumer.phone,
        "email":   consumer.email,
        "meter":   consumer.meter_slno
    }
    requests.put(
        f"https://internal-dedi.tpddl.in/dedi/lookup/tpddl-private/consumers-full/{consumer.number}",
        json=private_record,
        cert=("client.pem", "client-key.pem")   # mTLS
    )
```

Two writes, same `consumer.number` as the record ID. The public record exposes only what verifiers and other DISCOMs legitimately need; the private record holds the rest.

---

## Step 5 — Mint and register an asset

```python
def asset_did(klass: str, internal_id: str) -> str:
    safe = urllib.parse.quote(internal_id, safe="")
    return f"did:dedi:tpddl:assets:{klass}:{safe}"

def register_transformer(asset):
    record = {
        "id":     asset_did("transformer", asset.sap_code),
        "type":   "Transformer",
        "owner":  "did:dedi:india-energy-stack:ies-discoms-reference-registry:tpddl",
        "class":  "transformer",
        "subclass": "distribution",
        "ratedCapacityKVA": asset.rated_capacity,
        "geo":    {"lat": asset.geo.lat, "lon": asset.geo.lon},
        "commissionedAt":   asset.commissioned_at.isoformat(),
        "decommissionedAt": None,
        "endpoints": [
            {"type": "telemetry", "becknBPP": "did:web:ies.tpddl.in#beckn-bpp"}
        ]
    }
    body = {
        "namespace": "tpddl",
        "registry":  "assets",
        "recordId":  f"transformer/{asset.sap_code}",
        "record":    record,
        "controller": NAMESPACE_DID
    }
    sig = namespace_sign(json.dumps(body, separators=(",", ":")).encode())
    requests.post(f"{DEDI}/write", json=body, headers={"X-Signature": sig}).raise_for_status()
```

The same pattern applies to feeders, substations, meters, and DERs — only the `class` and any class-specific fields change.

---

## Step 6 — Issue a credential that references everything

This stitches it all together. A new-connection credential carries:

- `issuer.id` — your `did:web`
- `issuer.idRef.subjectId` — your reference-registry entry
- `credentialSubject.id` — the holder's `did:key`
- `credentialSubject.customerProfile.customerReference` — the consumer DeDi DID
- `credentialSubject.connection.id` — the connection DeDi DID
- `credentialSubject.meter.id` — the meter DeDi DID
- `credentialStatus.id` — the revocation handle under your namespace

```python
ISSUER_DID         = "did:web:ies.tpddl.in"
ISSUER_NAME        = "Tata Power Delhi Distribution Limited"
IES_REGISTRY_DID   = "did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma"
IES_REGISTRY_SUBJ  = "india-energy-stack:tpddl"
DEDI_REVOCATION    = f"https://api.dedi.global/dedi/lookup/tpddl/vc-revocation-registry"

def issue_for(consumer, holder_did):
    body = {
        "issuerDid": ISSUER_DID,
        "schemaId":  "electricity/v1",
        "proofFormat": "vc-jwt",
        "validFrom":  now_iso(),
        "validUntil": (now() + relativedelta(years=5)).isoformat(),
        "revocationRegistryUrl": DEDI_REVOCATION,
        "credentialSubject": {
            "id": holder_did,
            "customerProfile": {
                "customerReference": consumer_did(consumer.number),
                "customerNumber":    consumer.number
            },
            "customerDetails": {
                "name":  consumer.name,
                "installationAddress": consumer.address.dict(),
                "identityProofs": [{
                    "type": "AADHAAR",
                    "value": consumer.aadhaar_last4,
                    "issuedBy": "did:web:uidai.gov.in"
                }]
            },
            "connection": {
                "id":     f"did:dedi:tpddl:connections:{consumer.connection_id}",
                "tariff": consumer.tariff_category,
                "feeder": asset_did("feeder",  consumer.feeder_code),
                "meter":  asset_did("meter",   consumer.meter_slno)
            }
        }
    }
    vc = requests.post("http://opencred:8080/v1/credentials/issue", json=body).json()

    # Inject the schema-required issuer object before delivery.
    vc["issuer"] = {
        "id":   ISSUER_DID,
        "name": ISSUER_NAME,
        "idRef": {
            "issuedBy":  IES_REGISTRY_DID,
            "subjectId": IES_REGISTRY_SUBJ
        }
    }
    # Re-sign or pass back through OpenCred for re-signing.
    return vc
```

Every identifier in this credential is resolvable. A verifier — handed only this JSON — can reach the issuer's trust entry, the consumer's reference record, the meter and feeder records, and the revocation registry, without any out-of-band setup.

---

## Step 7 — Revoke

When a connection terminates:

```python
requests.post("http://opencred:8080/v1/credentials/revoke",
              json={"credentialId": vc_id}).raise_for_status()
```

OpenCred publishes the SHA-256(JCS(credential)) hash to:

```
https://api.dedi.global/dedi/lookup/tpddl/vc-revocation-registry/<credential-id>
```

Concurrently, mark the consumer record closed:

```python
requests.patch(f"{DEDI}/write/tpddl/consumers/{consumer.number}",
               json={"status": "closed", "closedAt": now_iso()},
               headers={"X-Signature": sig_for_patch})
```

---

## End-to-end test

A passing integration test should:

1. Issue a credential to a `did:key` holder.
2. Resolve `issuer.idRef.subjectId` and confirm the DID matches `issuer.id`.
3. Fetch the public key from the reference registry entry and verify `proof`.
4. Resolve `customerProfile.customerReference` and confirm the consumer record exists and is active.
5. Resolve `connection.meter` and confirm the asset record exists.
6. Confirm `credentialStatus.id` returns 404 (not revoked).
7. Revoke the credential.
8. Re-verify and confirm step 6 now returns 200 (revoked).

Steps 2–6 each test one identifier flow described in [Resolution](./resolution.md). Run this on every release.

---

## What you have at the end

| Artefact | Where |
|---|---|
| Issuer DID Document | `https://ies.tpddl.in/.well-known/did.json` |
| Trust anchor | `india-energy-stack/ies-discoms-reference-registry/tpddl` |
| Revocation registry | `tpddl/vc-revocation-registry/*` |
| Public consumer registry | `tpddl/consumers/*` (redacted) |
| Private consumer registry | `internal-dedi.tpddl.in/.../consumers-full/*` (full PII) |
| Public asset registry | `tpddl/assets/<class>/*` |
| Signed credentials | OpenCred output, delivered to wallets / DigiLocker |

Every identifier in every credential is a DID. Every DID resolves. Every record carries enough metadata for the next request to route itself. That is the IES addressing system in one paragraph.

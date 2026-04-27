# Onboarding Guide — Energy Credentials

This guide walks you through the complete setup to start issuing or verifying IES Energy Credentials using **OpenCred** — the open-source W3C VC platform that IES credential services are built on.

> Full OpenCred documentation: [https://opencred.gitbook.io/docs](https://opencred.gitbook.io/docs)

---

## Choose Your Role

| Role | What you do | Setup path |
|---|---|---|
| **DISCOM (Issuer)** | Issue electricity connection credentials to consumers via DigiLocker | [DISCOM Onboarding](#discom-onboarding) |
| **Certification Body (Issuer)** | Issue green energy / safety / compliance credentials to assets | [Certification Body Onboarding](#certification-body-onboarding) |
| **Service Provider (Verifier)** | Verify credentials presented by consumers | [Verifier Onboarding](#verifier-onboarding) |

---

## DISCOM Onboarding

### Prerequisites

- [ ] Organisation registered on [API Setu](https://apisetu.gov.in) as a DigiLocker issuer (or existing issuer account — contact NeGD)
- [ ] An HTTPS endpoint you can expose for DigiLocker's inbound Pull URI calls
- [ ] Docker installed (for production API deployment)
- [ ] Read access to your CIS / billing database for consumer lookups

### Step 1 — Deploy OpenCred

Set up the OpenCred Docker service. This is the credential signing engine your DISCOM will call at runtime.

```bash
# Generate a secure API key
export OPENCRED_API_KEY=$(openssl rand -base64 32)

docker run -p 3100:3100 \
  -e OPENCRED_API_KEY=$OPENCRED_API_KEY \
  -e OPENCRED_KEY_PATH=/secrets/issuer-key.pem \
  -v /path/to/your-key.pem:/secrets/issuer-key.pem:ro \
  opencred:latest
```

Verify it's running:
```bash
curl http://localhost:3100/v1/health
# → 200 OK
```

See [Issuing Credentials](./issuance.md#docker-api) for the full Docker Compose setup and Cloud KMS options.

### Step 2 — Set Up Your Signing Key and Issuer DID

You need a signing key and a DID that identifies your DISCOM as the credential issuer. OpenCred supports three approaches:

**Option A — Import an existing Digital Signature Certificate (DSC)**
- Use the OpenCred Desktop Client → Settings → Import File
- Import your PFX, PEM, or hardware token
- OpenCred derives `did:key` from your certificate's public key

**Option B — Generate a fresh ECDSA P-256 key (recommended for new deployments)**
- Open the OpenCred Desktop Client → Settings → Generate Key → **Generate ECDSA P-256 Key**
- Enter your domain (e.g. `ies.tpddl.in`)
- Download the DID document and upload it to `https://ies.tpddl.in/.well-known/did.json`
- Your issuer DID is `did:web:ies.tpddl.in`

**Option C — Hardware token (PKCS#11)**
- OpenCred Desktop Client → Settings → Hardware Token
- Select library, slot, and enter PIN

Save your issuer DID — you will pass it in every credential issuance API call.

### Step 3 — Register on API Setu as a DigiLocker Issuer

If not already registered:
1. Go to [https://apisetu.gov.in](https://apisetu.gov.in) and register your organisation
2. Add the `NYCER` document type with these parameters:

| Field | Value |
|---|---|
| Endpoint URL | `https://{your-domain}/digilocker/pulluri` |
| HTTP Method | `POST` |
| Content-Type | `application/xml` |
| DocType | `NYCER` |
| UDF1 Label | `Consumer Number` |
| UDF2 Label | `Registered Mobile Number` |

You receive an `issuer_id` (e.g. `in.gov.tpddl`) and an `api_key`. Store the `api_key` securely — you need it to verify inbound HMAC headers from DigiLocker.

> If your DISCOM is already on DigiLocker for ELBIL, contact NeGD to add `NYCER` to your existing account. Do not re-register.

### Step 4 — Build the Pull URI Endpoint

Build and deploy an HTTPS endpoint at `https://{your-domain}/digilocker/pulluri`. This is the only custom code your DISCOM writes.

At runtime, the handler:
1. Verifies the inbound HMAC from DigiLocker
2. Looks up the consumer in your CIS
3. Calls OpenCred's `POST /v1/credentials/issue` to produce a signed credential
4. Returns the signed VC (JSON) and a rendered PDF in the `PullURIResponse` XML

For the full endpoint specification, request/response formats, HMAC verification, and code samples, see the [DigiLocker Integration guide](./digilocker-integration.md).

### Step 5 — Test End-to-End

Use the OpenCred Desktop Client to issue a test credential for a sample consumer. Confirm the output VC is well-formed, then run a simulated DigiLocker inbound request against your Pull URI endpoint and verify the response is a valid `PullURIResponse`.

### Step 6 — Go Live

Switch to the production DigiLocker endpoint on API Setu. Consumers can immediately find their `NYCER` credential in the DigiLocker app.

---

## Certification Body Onboarding

Certification bodies issue credentials about energy assets — green energy certificates, grid interconnection approvals, safety compliance.

### Step 1 — Deploy OpenCred

Same as the DISCOM flow. See [Step 1 above](#step-1--deploy-opencred).

### Step 2 — Set Up Signing Key and Issuer DID

Same as [Step 2 above](#step-2--set-up-your-signing-key-and-issuer-did).

### Step 3 — Issue Credentials After Inspection

After an audit or inspection, call OpenCred's issue endpoint with the asset's fields and the appropriate `credentialType` (e.g. `GreenEnergyCertificate`, `GridInterconnectionApproval`, `SafetyCertificate`). Deliver the signed VC to the asset holder's DID.

See [Issuing Credentials](./issuance.md) for the full API reference.

---

## Verifier Onboarding

Service providers who need to verify credentials have a lighter integration.

### Step 1 — Deploy OpenCred (or use Desktop Client)

For automated verification in production, deploy OpenCred as a Docker service (same as above). For manual spot-checks, the Desktop Client's Verify page is sufficient.

### Step 2 — Implement DigiLocker OAuth (for consumer credentials)

To receive credentials shared by consumers via DigiLocker:

1. Register your application on [API Setu](https://apisetu.gov.in) as a DigiLocker requester
2. Implement the DigiLocker OAuth 2.0 + PKCE flow:
   - Redirect consumer to DigiLocker with `req_doctype=NYCER`
   - Exchange auth code for access token
   - Fetch the `VcContent` from DigiLocker's file API
3. Extract the base64-encoded VC JSON from `VcContent`
4. Verify HMAC on the DigiLocker response

### Step 3 — Verify with OpenCred

Pass the decoded VC to OpenCred's verify endpoint for cryptographic assurance:

```bash
curl -X POST http://localhost:3100/v1/credentials/verify \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "credential": { /* decoded VC JSON */ } }'
```

See [Verifying Credentials](./verification.md) for the full response format and revocation details.

---

## Checklist Summary

### DISCOM (Issuer)
- [ ] OpenCred Docker deployed and healthy (`/v1/health` returns 200)
- [ ] Signing key set up — issuer DID confirmed (`did:key:...` or `did:web:...`)
- [ ] Registered on API Setu (`issuer_id` + `api_key` saved)
- [ ] Pull URI endpoint built, tested, and deployed at HTTPS
- [ ] End-to-end test passed with sample consumer
- [ ] Production endpoint registered on API Setu

### Certification Body (Issuer)
- [ ] OpenCred Docker deployed and healthy
- [ ] Signing key set up — issuer DID confirmed
- [ ] Issuance API integration tested with a sample asset credential

### Verifier
- [ ] OpenCred deployed (or Desktop Client for manual use)
- [ ] DigiLocker OAuth flow implemented
- [ ] Verify endpoint integration tested

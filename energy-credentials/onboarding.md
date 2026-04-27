# Onboarding Guide — Energy Credentials

This guide walks you through the complete setup process to start issuing or verifying IES Energy Credentials. The process differs slightly depending on your role.

---

## Choose Your Role

| Role | What you do | Setup path |
|---|---|---|
| **DISCOM (Issuer)** | Issue electricity connection credentials to consumers | [DISCOM Onboarding](#discom-onboarding) |
| **Certification Body (Issuer)** | Issue green energy / safety / compliance credentials to assets | [Certification Body Onboarding](#certification-body-onboarding) |
| **Service Provider (Verifier)** | Verify credentials presented by consumers or assets | [Verifier Onboarding](#verifier-onboarding) |

---

## DISCOM Onboarding

DISCOMs integrate with the IES Credential Service to issue **electricity connection credentials (NYCER)** to their consumers via DigiLocker.

### Prerequisites

Before you start, confirm you have:

- [ ] Organisation registered on [API Setu](https://apisetu.gov.in) as a DigiLocker issuer (or existing issuer account — contact NeGD/Chikan)
- [ ] Access to the IES Credential Service API (request credentials from the IES team)
- [ ] The [IES Postman Collection](https://fsrglobaladmin.sharepoint.com/:u:/s/FSRG/IQAOQcWtB6JzQobtt91va2oZAaNny8bhbkGh_cizrV5v0qc?e=pUUxti) (shared by IES team)
- [ ] An HTTPS endpoint you can expose for DigiLocker's inbound Pull URI calls
- [ ] Read access to your CIS / billing database for consumer lookups

### Step 1 — Get Your Issuer DID

Call the IES Credential Service to create your DISCOM's Decentralized Identifier. The IES team walks you through this using the Postman collection.

```
POST /credential/did/create
```

Save the `issuer_did` returned. You will pass it in every credential issuance request.

```json
{
  "issuer_did": "did:ies:discom-tpddl",
  "public_key": "...",
  "created_at": "2026-04-01T10:00:00Z"
}
```

### Step 2 — Register the NYCER Schema

Register the electricity connection credential schema with the IES service:

```
POST /credential/schema/create
```

The IES team provides the schema definition. Save the `schema_id` returned.

```json
{
  "schema_id": "ies:schema:nycer:v1",
  "name": "National Yield Consumer Electricity Record",
  "version": "1.0"
}
```

### Step 3 — Register on API Setu as a DigiLocker Issuer

If you are not already registered:
1. Go to [https://apisetu.gov.in](https://apisetu.gov.in)
2. Register your organisation as a document issuer
3. Add the `NYCER` document type with these parameters:
   - **Endpoint URL:** `https://{your-domain}/digilocker/pulluri`
   - **UDF1:** Consumer Number
   - **UDF2:** Registered Mobile Number

You receive an `issuer_id` (e.g. `in.gov.tpddl`) and an `api_key`. Store the `api_key` securely — you need it to verify inbound HMAC headers from DigiLocker.

> If your DISCOM is already on DigiLocker for ELBIL (electricity bills), contact NeGD to add the NYCER document type to your existing account rather than re-registering.

### Step 4 — Build the Pull URI Endpoint

Build and deploy an HTTPS endpoint at `https://{your-domain}/digilocker/pulluri`. This is the only custom code your DISCOM writes. DigiLocker calls it whenever a consumer requests their NYCER credential.

For the full specification of request/response formats, HMAC verification, and code samples, see the [DigiLocker Integration guide](./digilocker-integration.md).

At a high level, the handler:
1. Verifies the inbound HMAC from DigiLocker
2. Looks up the consumer in your CIS using the consumer number (UDF1)
3. Calls `POST /credential/credentials/issue` on the IES service
4. Calls `GET /credential/credentials/{id}` to retrieve the PDF
5. Returns a `PullURIResponse` XML to DigiLocker

### Step 5 — Test with the Sandbox

The IES team provides a DigiLocker sandbox environment. Run an end-to-end test:

1. Simulate a DigiLocker inbound `PullURIRequest` to your endpoint
2. Confirm your endpoint calls IES and returns a valid `PullURIResponse`
3. Verify the credential is accessible in the DigiLocker test environment

### Step 6 — Go Live

Once testing is complete, switch to the production DigiLocker endpoint. Consumers can immediately search for their NYCER credential in DigiLocker under your organisation name.

---

## Certification Body Onboarding

Certification bodies issue credentials about energy assets — green energy certificates, safety compliance, grid interconnection approvals.

### Step 1 — Get Your Issuer DID

Same as the DISCOM flow:
```
POST /credential/did/create
```

### Step 2 — Register Your Credential Schema

Define the claims your credential will attest and register the schema:
```
POST /credential/schema/create
```

Work with the IES team to align your schema with the appropriate IES credential type (e.g. `GreenEnergyCertificate`, `GridInterconnectionApproval`, `SafetyCertificate`).

### Step 3 — Issue Credentials

After an audit or inspection, call the IES service to issue a signed credential to the asset holder's DID:
```
POST /credential/credentials/issue
```

See [Issuing Credentials](./issuance.md) for the full API reference.

---

## Verifier Onboarding

Service providers who need to verify credentials (e.g. housing societies verifying address proof, fintech apps verifying energy consumer status) have a lighter integration.

### Step 1 — Register as a Verifier

Contact the IES team to register your application and receive a verifier API key.

### Step 2 — Implement DigiLocker OAuth (for consumer credentials)

To receive credentials shared by consumers via DigiLocker:

1. Register your application on API Setu as a DigiLocker requester
2. Implement the [DigiLocker OAuth flow](https://partners.digitallocker.gov.in/assets/img/Digital%20Locker%20Technical%20Specification%20v1%200%205.pdf):
   - Redirect consumer to DigiLocker authorization endpoint with `req_doctype=NYCER`
   - Exchange auth code for access token
   - Fetch the credential XML from DigiLocker's file API
   - Verify the HMAC on the response

### Step 3 — Verify the W3C Credential (optional but recommended)

For stronger assurance, call the IES verification endpoint directly:

```
GET /credential/credentials/{credential_id}/verify
```

Response:
```json
{
  "verified": true,
  "proof_valid": true,
  "revoked": false,
  "expired": false,
  "issuer": "did:ies:discom-tpddl"
}
```

See [Verifying Credentials](./verification.md) for the full API reference.

---

## Checklist Summary

### DISCOM (Issuer)
- [ ] Registered on API Setu (issuer_id + api_key)
- [ ] Issuer DID created (`issuer_did` saved)
- [ ] NYCER schema registered (`schema_id` saved)
- [ ] Pull URI endpoint built, tested, and deployed
- [ ] DigiLocker sandbox test passed
- [ ] Production endpoint registered on API Setu

### Certification Body (Issuer)
- [ ] Issuer DID created
- [ ] Custom credential schema registered
- [ ] Issuance API integration tested

### Verifier
- [ ] Verifier API key received
- [ ] DigiLocker OAuth flow implemented
- [ ] Credential verification API integration tested

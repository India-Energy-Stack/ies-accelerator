# Issue Credentials

> **Step 2 of the implementation path — set up + operate.** Run the [OpenCred](../glossary.md#opencred) signing container and issue, verify, and revoke W3C Verifiable Credentials. This is the **B2C rail**: a credential is signed once by you and can then be trusted by *any* third party — a bank, a marketplace, a housing society — that resolves your `did:web`, and delivered over any channel (DigiLocker, web portal, email, SMS, chat). **No Beckn network is involved.** About half a day.

The concepts — what a credential is, the trust model, the credential variants and when to use each — are in **[Energy Credentials](../what-ies-provides/energy-credentials/README.md)**. This page is the do-guide.

> **About the walkthrough.** The commands use **[OpenCred](../glossary.md#opencred)** — see the glossary for what it is, its W3C compliance, its DeDi integration, and release links. Any W3C-compliant signing pipeline that publishes the same `did.json` and VC-2.0 proofs is a drop-in replacement.

---

## Before you start

From **[Setup Register](setup-register.md)** you need §1.1–1.4 complete:

- `OPENCRED_ISSUER_DOMAIN` exported, and `did.json` published and resolvable from outside (§1.1–1.3).
- The EC P-256 signing key at `~/opencred/keys/issuer-key.pem` (§1.2).
- A **verified DeDi namespace** and a **DeDi API key** (§1.4) — these enable revocation.

On this machine:

- **Docker 24+**, plus `curl`, `jq`, `openssl`, and ~2 GB free disk.
- *(Optional, recommended for licensed utilities)* your regulator's `did:web` and your licence identifier, to quote in `issuer.idRef`. Omit for pilots / non-regulated issuers.
- **A payload schema in mind.** Default: [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2). For telemetry, [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6).

> **No IES-side DISCOM-registry entry is required to issue credentials.** Verifiers fetch your `did.json` directly to check signatures. The IES network registries are the Beckn-side trust boundary — a separate concern ([Setup Register §1.7](setup-register.md#id-1.7-beckn-participants-get-referenced-into-an-ies-network)).

---

## 2.1 — Pull the OpenCred image

```bash
docker pull ghcr.io/nfh-trust-labs/opencred/opencred-server:latest
docker tag  ghcr.io/nfh-trust-labs/opencred/opencred-server:latest opencred:bootcamp
```

## 2.2 — Generate the OpenCred API token

This token is the only auth on OpenCred's HTTP API — whoever holds it can issue credentials in your name. Generate and save it:

```bash
export OPENCRED_API_KEY="$(openssl rand -base64 32)"
echo "Save this: $OPENCRED_API_KEY"
```

## 2.3 — Run OpenCred in `did:web` mode

First set the two DeDi variables (in addition to `OPENCRED_ISSUER_DOMAIN` from Setup Register §1.1 — re-export it if this is a fresh shell):

```bash
export OPENCRED_DEDI_NAMESPACE="yourdiscom"
export OPENCRED_DEDI_API_KEY="paste-your-dedi-api-key-here"
```

- **`OPENCRED_DEDI_NAMESPACE`** — the namespace you claimed and domain-verified in [Setup Register §1.4](setup-register.md#id-1.4-claim-a-dedi-namespace-and-verify-your-domain).
- **`OPENCRED_DEDI_API_KEY`** — the key you created in the DeDi UI at [publish.dedi.global](https://publish.dedi.global) (avatar in the top-right corner → **Manage API key**).

The `OPENCRED_DEDI_*` variables connect the container to DeDi at startup. That is what enables **revocation** (§2.8) and lets OpenCred auto-create the four registries it needs in your namespace on first boot.

Now start the container:

```bash
docker run -d \
  --name opencred \
  -p 3100:3100 \
  -e OPENCRED_API_KEY="$OPENCRED_API_KEY" \
  -e OPENCRED_KEY_PATH=/secrets/issuer-key.pem \
  -e OPENCRED_ISSUER_DID_METHOD=web \
  -e OPENCRED_ISSUER_DOMAIN="$OPENCRED_ISSUER_DOMAIN" \
  -e OPENCRED_DEDI_BASE_URL=https://api.dedi.global \
  -e OPENCRED_DEDI_AUTH_TYPE=api-key \
  -e OPENCRED_DEDI_API_KEY="$OPENCRED_DEDI_API_KEY" \
  -e OPENCRED_DEDI_NAMESPACE="$OPENCRED_DEDI_NAMESPACE" \
  -v "$HOME/opencred/keys/issuer-key.pem:/secrets/issuer-key.pem:ro" \
  --read-only --cap-drop ALL \
  opencred:bootcamp
```

Check it came up healthy:

```bash
curl -s http://localhost:3100/v1/health | jq
```

Expected: the JSON includes `"signingKeyLoaded": true`. If it is `false`, see [Troubleshooting](#troubleshooting).

> **Want offline-verifiable identity instead?** Drop `OPENCRED_ISSUER_DID_METHOD` and `OPENCRED_ISSUER_DOMAIN` and OpenCred runs in `did:key` mode by default. The same key, the same API — only the `did:` string the container reports changes. This is the right choice for first-deploy testing, demos, and consumer wallets. You can also drop the four `OPENCRED_DEDI_*` variables while testing — the container still issues and verifies, but revocation stays disabled until you add them back.

## 2.4 — Confirm your DeDi namespace is live

Credential **revocation** rides on your DeDi namespace, so before issuing anything, confirm the namespace side is in order. Two checks, both in a browser:

1. **Is the namespace verified?** Open [explore.dedi.global](https://explore.dedi.global) and search for your namespace. Only verified namespaces show up in explore results — if yours appears, it is verified. (In [publish.dedi.global](https://publish.dedi.global), where you log in and manage the namespace, verification shows as a green **verified** label.) Namespace not in explore? The DNS TXT record hasn't propagated or wasn't added; revisit [Setup Register §1.4](setup-register.md#id-1.4-claim-a-dedi-namespace-and-verify-your-domain).
2. **Did OpenCred create its registries?** Log in at [publish.dedi.global](https://publish.dedi.global) and open your namespace. Can you see the four registries OpenCred auto-created on first boot — `vc-revocation-registry`, `opencred-key-registry`, `schema_registry`, `context_registry`? If they are there, revocation is wired up and you're ready to issue. If not, the container couldn't reach DeDi — check `docker logs opencred` and re-check the `OPENCRED_DEDI_*` values from §2.3 (a wrong API key or namespace name is the usual cause).

## 2.5 — Confirm the issuer DID OpenCred reports

```bash
export ISSUER_DID="$(curl -s http://localhost:3100/v1/keys \
  -H "Authorization: Bearer $OPENCRED_API_KEY" | jq -r '.keys[0].id | split("#")[0]')"
echo "$ISSUER_DID"
```

Expected: your DID, e.g. `did:web:ies.yourdiscom.in`. If you ran the container in `did:key` mode (for early dev), this prints `did:key:z…` instead — the rest of the flow is identical, only the issuer string changes.

## 2.6 — Issue your first credential

Default: **bearer-style** (no `credentialSubject.id`) — anyone holding the JSON is treated as the subject. This mirrors the [OpenCred bootcamp](https://opencred.gitbook.io/docs/bootcamp/local-docker). For consumer-facing flows where the presenter must be the legitimate subject, bind to a holder identifier — see [Appendix — Holder binding](#appendix-binding-the-credential-to-a-holder-identity).

```bash
curl -s http://localhost:3100/v1/credentials/issue \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"schemaId\":    \"ies/electricity-credential/v1.2\",
    \"issuerDid\":   \"$ISSUER_DID\",
    \"proofFormat\": \"vc-jwt\",
    \"validFrom\":   \"2026-04-01T00:00:00+05:30\",
    \"validUntil\":  \"2031-04-01T00:00:00+05:30\",
    \"credentialSubject\": {
      \"customerProfile\": {
        \"customerNumber\": \"DISCOM-2025-00987654\",
        \"energyResources\": [{
          \"id\":   \"did:web:${OPENCRED_ISSUER_DOMAIN}:assets:meter:MET-IMPORT-001\",
          \"type\": \"METER\",
          \"attributes\": {\"meterCapability\": \"AMI\", \"energyDirection\": \"Forward\"}
        }],
        \"consumptionProfiles\": [{
          \"meterId\":            \"did:web:${OPENCRED_ISSUER_DOMAIN}:assets:meter:MET-IMPORT-001\",
          \"sanctionedLoad\":     {\"value\": 10, \"unit\": \"kW\"},
          \"tariffCategoryCode\": \"DS-I\",
          \"premisesType\":       \"Residential\",
          \"connectionType\":     \"Single-phase\"
        }]
      },
      \"customerDetails\": {
        \"fullName\":              \"Arjun Mehra\",
        \"installationAddress\": {
          \"geo\": {
            \"type\": \"Point\",
            \"coordinates\": [77.5946, 12.9716]
          },
          \"address\": {
            \"streetAddress\": \"12, 4th Cross, Indiranagar\",
            \"addressLocality\": \"Bengaluru\",
            \"addressRegion\": \"Karnataka\",
            \"postalCode\": \"560038\",
            \"addressCountry\": \"IND\"
          }
        },
        \"serviceConnectionDate\": \"2018-07-15T00:00:00+05:30\"
      }
    }
  }" | tee credential.json | jq .credential
```

Three things worth noting:

- **Asset IDs are `did:web` under your own domain**, with colon-path segments (`did:web:<your-domain>:assets:meter:<slno>` — the command above builds them from `$OPENCRED_ISSUER_DOMAIN`). Same pattern for transformers, feeders, substations — see [Register — Identifier patterns](../what-ies-provides/register.md#identifier-patterns). No per-asset `did.json` hosting required for the pragmatic case.
- **`issuer.idRef` is optional.** OpenCred fills `issuer` with the DID string only. Your integration service appends `name` and (if you have a regulator to cite) `idRef` on egress, then re-signs if your flow requires a single signed artefact.
- **`credentialSubject.id` is absent here.** That's the bearer-style default. Set it to a wallet `did:key` or `tel:+91...` URI for holder-bound issuance — see [Appendix — Holder binding](#appendix-binding-the-credential-to-a-holder-identity).

## 2.7 — Verify

```bash
jq -n --arg c "$(jq -r '.credential.proof.jwt' credential.json)" '{credential: $c}' | \
  curl -s http://localhost:3100/v1/credentials/verify \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" \
    -d @- | jq
```

Expected: the response includes `"valid": true`.

For `vc-jwt`, the verify endpoint takes the compact JWS string (`.credential.proof.jwt`), not the JSON envelope. For `data-integrity` proofs, send the full credential JSON. What a *third-party* verifier checks — signature, licensing assertion, revocation, validity window — is walked through in [Verify a credential you received](#verify-a-credential-you-received-the-verifiers-walkthrough) below.

## 2.8 — Revoke

OpenCred publishes revocation as a hash entry into your DeDi revocation registry; the verifier reads `credentialStatus` and looks up the hash. DeDi stores **only revoked** hashes — the per-credential lookup returns `200` when revoked and `404` when not (record existence is the signal). For the credential to carry that `credentialStatus`, pass `revocationRegistryUrl` at issue (as the [variant examples](#issue-the-credential-variants) below do); the default issue in §2.6 omits it.

> **Two URL shapes, on purpose.** `revocationRegistryUrl` at issue points at the *registry* (`…/dedi/query/<namespace>/vc-revocation-registry`); a verifier checking one credential reads the *record* (`…/dedi/lookup/<namespace>/vc-revocation-registry/<hash>`). `query` addresses the whole registry, `lookup` a single record inside it — not a typo.

Compute the revocation hash of the credential you issued:

```bash
HASH=$(jq '{credential: .credential}' credential.json | \
  curl -s http://localhost:3100/v1/credentials/revocation-hash \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" -d @- | jq -r .revocationHash)
echo "$HASH"
```

Revoke it:

```bash
curl -s http://localhost:3100/v1/credentials/revoke \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"hash\": \"$HASH\", \"reason\": \"connection-terminated\"}" | jq
```

Check its status:

```bash
curl -s http://localhost:3100/v1/credentials/revocation-status \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"hash\": \"$HASH\"}" | jq
```

Expected: the status response reports the credential as revoked, with the reason you supplied.

Revocation works here because the container was started with the `OPENCRED_DEDI_*` variables in §2.3 — if you dropped them for early testing, add them back and restart before trying this section. See [OpenCred Revocation](https://opencred.gitbook.io/docs/concepts/revocation) for the conceptual model.

## 2.9 — Smoke test

A passing integration test should:

1. Issue a credential.
2. Resolve `issuer.id` (`did.json` over HTTPS) and confirm the public key matches the one that signed `proof`.
3. *(If `issuer.idRef` is present)* Resolve `issuer.idRef.issuedBy` and confirm the regulator vouches for your DISCOM.
4. `POST /v1/credentials/verify` — expect `valid: true`.
5. Check `revocation-status` — expect not revoked.
6. Revoke.
7. Re-check `revocation-status` — expect revoked.

Run on every release. It exercises every leg of the trust chain.

---

## Issue the credential variants

The walkthrough above issued an ElectricityCredential. The other two IES credentials use the same `POST /v1/credentials/issue` flow with different schemas — what each variant is *for* is described in [Energy Credentials — Credential variants](../what-ies-provides/energy-credentials/README.md#credential-variants).

### MeterDataCredential v0.6 — telemetry signing

The `schemaId` is the OpenCred registry id **`ies/meter-data-credential/v0.6`**, and `credentialSubject.meterData` carries the `MeterData` payload (a profile object or array — see the [v0.6 examples](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6)). Pass `revocationRegistryUrl` so the credential carries a `credentialStatus` verifiers can check (§2.8):

```bash
curl -s http://localhost:3100/v1/credentials/issue \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"schemaId\":     \"ies/meter-data-credential/v0.6\",
    \"issuerDid\":    \"$ISSUER_DID\",
    \"proofFormat\":  \"vc-jwt\",
    \"validFrom\":    \"2026-06-28T00:00:00+05:30\",
    \"validUntil\":   \"2026-07-05T00:00:00+05:30\",
    \"revocationRegistryUrl\": \"https://api.dedi.global/dedi/query/$OPENCRED_DEDI_NAMESPACE/vc-revocation-registry\",
    \"credentialSubject\": {
      \"meterData\": { \"@type\": \"DailyProfile\", \"profileType\": \"DAILY\", \"…\": \"a MeterData v0.6 profile or array\" }
    }
  }" | tee credential.json | jq .credential
```

### MeterDataRequestCredential v0.1 — proof of right-to-ask

This schema is **not** in OpenCred's built-in registry, so issue it with an **`inlineSchema`** rather than a `schemaId`: pass the JSON Schema in the request and OpenCred validates `credentialSubject` against it, writes the schema `$id`, and signs. Here we reuse the published MeterDataRequest `$defs` so the inline schema stays canonical — the first command pulls them, the second wraps them as the `credentialSubject` schema and issues:

```bash
REQ_DEFS=$(curl -s https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/schema.json | jq '.["$defs"]')

jq -n --argjson defs "$REQ_DEFS" --arg iss "$ISSUER_DID" \
  --arg reg "https://api.dedi.global/dedi/query/$OPENCRED_DEDI_NAMESPACE/vc-revocation-registry" '{
  inlineSchema: {
    "$id": "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequestCredential/v0.1/schema.json",
    type: "object", required: ["meterDataRequest"],
    properties: {
      id: { type: "string", format: "uri" },
      meterDataRequest: { "$ref": "#/$defs/MeterDataRequestObject" }
    },
    "$defs": $defs
  },
  issuerDid: $iss,
  proofFormat: "vc-jwt",
  validFrom: "2026-06-28T00:00:00+05:30",
  validUntil: "2026-12-28T00:00:00+05:30",
  revocationRegistryUrl: $reg,
  credentialSubject: {
    meterDataRequest: {
      "@context": "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/context.jsonld",
      "@type": "MeterDataRequest",
      scope: "ResourceOnly",
      from: "2026-06-04T00:00:00Z",
      duration: "P6M",
      maxRecordsShared: 10000,
      capabilitiesRequested: { profiles: [ { profileType: "CustomerProfile" }, { profileType: "IntervalProfile" } ] }
    }
  }
}' | curl -s http://localhost:3100/v1/credentials/issue \
  -H "Authorization: Bearer $OPENCRED_API_KEY" -H "Content-Type: application/json" -d @- | jq .credential
```

`scope` must be one of the `ScopeType` enum (`ResourceOnly`, `ResourceAndChildren`, `ChildrenOnly`). The seeker embeds the resulting credential in the Beckn `confirm` message's receiver participant; the provider's adapter verifies it before fulfilling. Ready-to-send `confirm` payloads live in the [DEG data-exchange devkit](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc1-meter-data).

---

## Verify a credential you received (the verifier's walkthrough)

The flip side: a wallet or a counterparty hands you a signed credential. What to check, in order:

1. **Parse** the credential JSON. Read `issuer.id` (e.g. `did:web:ies.discom.example`).
2. **Resolve `issuer.id`** over HTTPS — fetch `https://<issuer-domain>/.well-known/did.json` and extract the `verificationMethod` public key.
3. **Verify the credential's `proof`** signature against that key. If it fails, stop — the credential is forged or corrupted.
4. **(Optional) Check `issuer.idRef`** if present. Resolve `issuer.idRef.issuedBy` (the regulator's `did:web`) and confirm the regulator vouches for this DISCOM under the cited `subjectId`. This is the licensing leg of the trust chain; skip when `idRef` is absent.
5. **Check revocation.** GET the URL in `credentialStatus.id` — typically `https://api.dedi.global/dedi/lookup/<discom>/vc-revocation-registry/<credential-id>`. A `404` (or `status: not_revoked`) means valid; a record with `status: revoked` means rejected.
6. **Check the validity window.** Confirm `validFrom <= now <= validUntil`.
7. **(Holder-bound credentials only)** Challenge the presenter to prove control of `credentialSubject.id` — see [Appendix — Holder binding](#appendix-binding-the-credential-to-a-holder-identity).

A verifier that caches the issuer's `did.json` and the regulator's `did.json` (e.g. refresh every 10 minutes) can complete steps 2–4 entirely offline; only step 5 needs a live DeDi lookup.

---

## Operational notes

The bare minimum to run OpenCred in production.

### Key rotation

1. Generate a new signing key in your KMS.
2. Publish the new key in `did.json` (keep the old key listed for a transition window).
3. Restart OpenCred pointing at the new key.
4. After the transition window, remove the old key from `did.json`.

Existing credentials signed by the old key keep verifying as long as the old key remains in `did.json`. Once you drop it, those credentials stop validating — schedule re-issuance before dropping.

### Signing-key sources

OpenCred loads exactly one signing key from one of:

| Source | Env var | When to use |
|---|---|---|
| Software file (PEM, JWK, PKCS#8, PFX) | `OPENCRED_KEY_PATH` | Dev, small DISCOMs |
| AWS KMS | `OPENCRED_KMS_PROVIDER=aws`, `OPENCRED_KMS_KEY_ARN` | Production on AWS |
| Azure Key Vault | `OPENCRED_KMS_PROVIDER=azure`, `OPENCRED_AZURE_*` | Production on Azure |
| GCP Cloud KMS | `OPENCRED_KMS_PROVIDER=gcp`, `OPENCRED_GCP_KMS_KEY_NAME` | Production on GCP |

The private key never leaves the container; in KMS modes it never leaves the HSM at all. There is no shared signing service and no key escrow.

### Schema validation

Validate the body of every `POST /v1/credentials/issue` against the schema **before** sending it. OpenCred validates server-side too, but a client-side check catches integration bugs earlier and avoids logging PII into OpenCred's error trail. Use the JSON Schema at `schemas/ElectricityCredential/v1.2/schema.json` (or the matching version).

### Batch issuance

For high-volume flows (annual re-issue, bulk Passport rollout):

- Process in batches of 100–1000; respect `Retry-After` if OpenCred returns 429.
- Sign in-process; do not externalise to a queue that buffers credentials in the clear.
- Persist `(credentialId, customerNumber, status)` after each successful issue so retries are idempotent.
- Run integration tests against `test-` networks before flipping the prod flag.

OpenCred's [API reference](https://opencred.gitbook.io/docs/docker-image/api-reference) covers concurrency, rate limits, and error shapes for production scale.

### Reverse proxy + TLS

Never expose OpenCred's `:3100` directly. Terminate TLS at nginx / Envoy / your existing edge; forward to OpenCred over an internal network. The `OPENCRED_API_KEY` is the only auth — leaking it gives the bearer full issuance powers.

### Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| `/v1/health` returns `signingKeyLoaded: false` | Key path wrong, key file permission denied, or KMS creds missing | Check the container logs; verify the mount and the env vars |
| `POST /v1/credentials/issue` returns `400 schema_validation_error` | Body doesn't match the schema for the declared `schemaId` | Diff against `schemas/<Credential>/<version>/schema.json` |
| `POST /v1/credentials/verify` returns `valid: false` for a freshly issued credential | You sent the JSON envelope instead of the compact JWS for a `vc-jwt` proof | Send `.credential.proof.jwt`, not the whole envelope |
| `/v1/keys/publish` fails with a validation error | A pre-existing DeDi registry has an incompatible schema | Either let OpenCred recreate, or align the registry schema; see [OpenCred Deployment](https://opencred.gitbook.io/docs/docker-image/deployment) |
| `revoke` succeeds but verifiers still see `not_revoked` | DeDi cache; OpenCred's local cache | Wait 5–10 minutes; verify the registry directly via `curl https://api.dedi.global/dedi/lookup/<ns>/vc-revocation-registry/<hash>` |

---

## Appendix — Binding the credential to a holder identity

A credential signed by you proves *who issued it*. It does **not** by itself prove *who is allowed to present it*. Without an explicit holder binding, the credential is a **bearer token** — whoever has the JSON is treated as the subject. That's fine for paper-style issuance, demos, and counter-issued attestations, but for consumer-facing flows (Consumer Energy Passport, Consumer Meter Digest, anything a bank or marketplace will read) you usually want presentation-time proof that the presenter is the same person the credential was issued to.

The W3C [VC Data Model 2.0 § Presentations](https://www.w3.org/TR/vc-data-model-2.0/#presentations) handles this through `credentialSubject.id`: set it to an identifier the subject controls, and require a proof-of-control at presentation time. The v1.2 schema makes `credentialSubject.id` optional, so you can pick the pattern that fits the consumer's situation.

### Before you bind anything: identity-proofing at issuance

This is the easy-to-miss step. The holder identifier (a DID, a phone number, anything) lands inside `credentialSubject.id` because **you put it there**. If you copy it verbatim from an unauthenticated request, an attacker can submit their own DID or their own phone and you will happily bind a Passport to it. Holder binding only works if you verify, **at issue time**, that the consumer controls the identifier you're about to embed.

So before any `POST /v1/credentials/issue` call that sets `credentialSubject.id`:

| Holder identifier | What to verify at issue time |
|---|---|
| `did:key:...` (wallet) | The wallet signs a fresh nonce you send it; you verify the signature against the public key in the DID. This proves the requester holds the wallet's private key. |
| `tel:+91XXXXXXXXXX` | You confirm the number is the one already on file for that `customerNumber` in your CIS, **and** you send a fresh OTP to that number and confirm the requester reads it back. |
| DigiLocker-mediated | DigiLocker has already done the Aadhaar-backed identity check before issuing the access grant; you can rely on that for the identity binding, and just record DigiLocker as the binding channel. |

Without that check, holder binding adds zero security; with it, the wallet/phone/DigiLocker identifier becomes a real second factor at presentation time.

### Pattern 1 — Wallet DID (cryptographic, recommended where a wallet exists)

Set `credentialSubject.id` to a DID the consumer's wallet controls — typically `did:key`, sometimes `did:jwk`. Both are offline-resolvable (the public key is encoded in the DID string), so the verifier needs no network call to fetch the holder's key.

```json
"credentialSubject": {
  "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
  "customerProfile": { "customerNumber": "DISCOM-2025-00987654", ... },
  "customerDetails": { ... }
}
```

**The presentation-time flow.** When the consumer presents the credential to a verifier (a bank, a marketplace, a housing society):

1. The verifier asks the wallet for the credential.
2. The wallet wraps the credential in a **Verifiable Presentation (VP)** — a small JSON envelope that can carry one or more credentials and add a fresh signature from the holder.
3. The verifier sends a **challenge** (a random nonce, often a UUID) and a **domain** (an identifier for the verifier itself, e.g. `bank.example.com`) — these go into `proof.challenge` and `proof.domain` on the VP.
4. The wallet signs the VP with the private key matching `credentialSubject.id`, embedding the challenge and domain inside the signature.
5. The verifier:
   - Resolves `credentialSubject.id`. For `did:key` this means decoding the multibase-encoded public key out of the DID string itself — no network call needed.
   - Verifies the VP's `proof.signature` against that public key.
   - Confirms `proof.challenge` matches the nonce the verifier just sent (rules out replays).
   - Confirms `proof.domain` matches the verifier's own identifier (rules out a presentation captured from another verifier).
   - Separately verifies the embedded credential's `proof` against the issuer DISCOM's `did:web` key (this is the standard issuer-side check).
6. If all checks pass, the presenter has demonstrated control of the wallet's private key — they are the subject the credential was issued to.

A stolen credential JSON does not pass step 5: the attacker doesn't have the wallet's private key, so they cannot produce a VP signature that matches the public key embedded in `credentialSubject.id`.

This is the model OpenID for Verifiable Presentations (OID4VP), DIDComm, and most W3C wallet ecosystems implement.

**Wallet rotation.** A wallet `did:key` cannot rotate (rotating means a new DID). If a consumer's wallet is lost or compromised, they generate a new `did:key` and you re-issue the credential bound to it. The old credential is revoked through your DeDi revocation registry (§2.8).

### Pattern 2 — Phone-number URI (out-of-band, when there is no wallet)

If the consumer doesn't have a wallet — and many Indian consumers won't, at least initially — you can still bind the credential to a channel they control: a phone number. Use the [RFC 3966](https://datatracker.ietf.org/doc/html/rfc3966) `tel:` URI scheme so the identifier is a proper URI rather than a bare string:

```json
"credentialSubject": {
  "id": "tel:+919876543210",
  "customerProfile": { "customerNumber": "DISCOM-2025-00987654", ... },
  "customerDetails": { ... }
}
```

The URI form is strict: **`tel:` + full E.164** (country code + national number, no spaces, hyphens, parentheses, or leading zeros). For India that is `tel:+91` followed by the ten-digit mobile number. This is the only form a verifier can compare unambiguously across systems.

**The presentation-time flow.**

1. The consumer presents the credential to a verifier (often via QR scan, email attachment, or a DigiLocker share).
2. The verifier reads `credentialSubject.id` and extracts the phone number.
3. The verifier sends a fresh OTP to that number through SMS, IVR, or a push notification on a known app.
4. The presenter reads the OTP back to the verifier.
5. If the OTP matches and is unexpired, the presenter has demonstrated control of the phone number.
6. The verifier independently verifies the credential's `proof` against the issuer's `did:web` key.

Compared to Pattern 1, this is weaker security: phone numbers can be ported, SIM-swapped, or temporarily shared, and the OTP channel itself can be phished. It is also slower (out-of-band OTP delivery). It is the right pragmatic choice when the consumer has no wallet and the verifier already runs phone-OTP plumbing.

**Phone-number changes.** Phone numbers change far more often than wallet DIDs. Either keep `validUntil` short (e.g. annual re-issue) so a stale number doesn't outlive its accuracy, or re-issue the credential whenever the consumer updates their number in your CIS.

### Pattern 3 — DigiLocker-mediated (Indian-context shortcut)

For consumers who already use DigiLocker, the identity binding is largely solved before the credential reaches the consumer: DigiLocker performs an Aadhaar-backed identity check before granting access, and the credential is delivered into the consumer's DigiLocker vault. A verifier consuming a credential out of DigiLocker can rely on DigiLocker's own access-control rather than re-running a presentation-time challenge.

In this case you may issue the credential without a `credentialSubject.id` (bearer style) and document DigiLocker as the binding channel, **or** set `credentialSubject.id` to the consumer's DigiLocker-resident `did:key` if their wallet exposes one. The first is simpler; the second future-proofs the credential for re-presentation outside DigiLocker. Delivery mechanics: [DigiLocker delivery](../what-ies-provides/energy-credentials/digilocker.md).

### Pattern 4 — DISCOM-assigned consumer DID (stable subject reference)

When the consumer has no wallet and you still want a **stable, resolvable subject identifier** on the Passport, mint one under your own domain from the consumer number:

```json
"credentialSubject": {
  "id": "did:web:ies.discom.example:consumers:DISCOM-2025-00987654",
  "customerProfile": { "customerNumber": "DISCOM-2025-00987654", ... },
  "customerDetails": { ... }
}
```

This is the same `did:web` path grammar used for assets and connections ([Register — Identifier patterns](../what-ies-provides/register.md#identifier-patterns)), scoped to `consumers:<consumer-number>`. Its value: every credential you issue for that consumer carries the **same subject id**, so a verifier (or the consumer's own history) can correlate the Passport, a Meter Digest, and a re-issued Passport as being about one subject — without exposing a wallet key or a phone number.

**What it does and doesn't give you.** The DID resolves under *your* domain, so it is a stable name you control — not proof the *presenter* controls it. It does **not** replace holder proof-of-control: for presentation-time proof, layer Pattern 1 (a wallet `did:key` the consumer signs a VP with) or Pattern 2 (phone OTP) on top, or deliver via DigiLocker (Pattern 3). Use Pattern 4 as the default subject id for bearer/counter-issued Passports and DigiLocker-delivered Passports where the channel supplies the identity binding and you still want a durable, correlatable subject reference. It carries no PII — the consumer number is already inside `customerProfile.customerNumber`.

### Where does the contact identifier live in the schema?

The `customerDetails` block in [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) (which references the shared [`CustomerDetails/v1.0`](https://schema.beckn.io/CustomerDetails/v1.0) shape) currently carries **`fullName`, `installationAddress`, and `serviceConnectionDate`** — there is **no telephone field**. So if you choose Pattern 2 today, the `tel:` URI lives in `credentialSubject.id`, not in `customerDetails`. If a future schema revision adds a `telephone` field, the canonical URI form there should be `tel:+<E.164>` so that the two locations agree.

### Picking a pattern

| Consumer situation | Pattern | `credentialSubject.id` value |
|---|---|---|
| Has a digital wallet (DID-capable) | **Pattern 1** — wallet DID | `did:key:z6Mkj...` |
| Has only a phone number on record | **Pattern 2** — `tel:` URI | `tel:+919876543210` |
| Uses DigiLocker, no separate wallet | **Pattern 3** — DigiLocker-mediated | *Omit, or use DigiLocker's `did:key` if exposed* |
| No wallet, but you want a stable correlatable subject | **Pattern 4** — DISCOM-assigned DID | `did:web:ies.discom.example:consumers:DISCOM-2025-00987654` |
| Paper / counter issuance, presented in person | None — bearer | *Omit* |

Patterns are not exclusive, and Pattern 4 composes with the others: a Passport can carry a `did:web:...:consumers:...` subject id for correlation **and** be presented with a wallet-signed VP (Pattern 1) or phone OTP (Pattern 2) for proof-of-control. Credentials sharing the same `customerProfile.customerNumber` (or the same Pattern-4 subject id) share the same revocation handle, so revoking one does the right thing operationally.

### Quick consistency checklist for adopters

- [ ] Issuer-side identity proof in place before any `credentialSubject.id` is set (challenge-sign for wallet DIDs, OTP for phones, DigiLocker grant otherwise).
- [ ] `tel:` URIs use full E.164 — `tel:+91` + ten digits — no spaces, hyphens, parentheses, or leading zeros.
- [ ] Verifier flow documented: how the verifier will challenge the holder at presentation time (VP-with-challenge for Pattern 1, OTP for Pattern 2, DigiLocker grant for Pattern 3).
- [ ] Revocation tested: revoking a credential invalidates **all** presentations of it, regardless of which binding pattern is in use.
- [ ] `validUntil` set with the binding's churn rate in mind (years for wallet DIDs, months-to-a-year for phone bindings).

---

## Checklist

- [ ] OpenCred running; `/v1/health` reports `signingKeyLoaded: true`
- [ ] Namespace visible on `explore.dedi.global`; four OpenCred registries visible in `publish.dedi.global`
- [ ] `ISSUER_DID` matches your published `did:web`
- [ ] One credential issued, verified (`valid: true`), revoked, and re-checked as revoked
- [ ] Smoke test (§2.9) scripted into your release pipeline
- [ ] For consumer-facing credentials: identity-proofing procedure in place before any holder binding

When all boxes are ticked, you can issue production credentials. To feed OpenCred from your CIS / MDM automatically, continue to **[Build your Internal-facing Adapter](build-adapter.md)**. To exchange data over a Beckn network as well, do **[Setup Register §1.5–1.7](setup-register.md#id-1.5-beckn-participants-generate-your-beckn-signing-keypair)** then **[Setup Exchange](setup-exchange.md)**.

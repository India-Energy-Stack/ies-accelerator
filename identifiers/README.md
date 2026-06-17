# Identifiers and Addressing

This page is the single home for everything IES has to say about identifiers. Read the first three sections and you will have enough to claim your DISCOM's identity on the network and issue your first credential. The appendices are there when you want more depth, want to issue at scale, or need to identify assets, meters, and datasets too.

> **Source of truth for the practical steps.** All key-generation, `did:web` / `did:key` setup, and credential issuance/revocation steps below mirror the [OpenCred bootcamp — Local Docker](https://opencred.gitbook.io/docs/bootcamp/local-docker). OpenCred is the canonical IES issuer; if any command here ever drifts from that page, treat the OpenCred page as authoritative. For the underlying theory of DID methods and revocation, see [OpenCred → DIDs](https://opencred.gitbook.io/docs/concepts/dids) and [OpenCred → Revocation](https://opencred.gitbook.io/docs/concepts/revocation). This page focuses on the IES-specific framing — which method to pick when, what each identifier means inside an [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md), and how internal numbering survives the wrapping.

---

## Why this matters (the gentle version)

When your DISCOM hands a consumer a digital electricity credential, or shares meter data with a regulator, the recipient needs to be able to answer one simple question on their own: *"Is this really from TPDDL?"* If they have to call you, email your IT team, or trust a screenshot, the system does not scale and it is not really verifiable.

The way the rest of the digital-public-infrastructure world solves this is with a small, well-understood standard called a **Decentralized Identifier (DID)**. You publish a tiny JSON file on a web address you control. That file lists the public key you sign things with. Anyone — a wallet, another DISCOM, a regulator — can fetch that file over plain HTTPS and check signatures on their own. No central authority, no API key, no special middleware.

You already have the two things you need: **a domain you own** and **a key your IT team can generate**. The rest of this page shows you what to put where. The setup is genuinely small; the harder part is just deciding which domain name represents your DISCOM on the network.

---

## The short version

If you only read this far, here is the whole picture for a DISCOM joining IES:

| Who | Identifier method | What it looks like |
|---|---|---|
| **Your DISCOM (the issuer)** | `did:web` on a domain you own | `did:web:ies.tpddl.in` |
| **A regulator** | Same — `did:web` on their own domain | `did:web:ies.derc.gov.in` |
| **A consumer holding a credential** | `did:key` (their wallet generates it) | `did:key:z6Mkj...` |

Three steps get you to "I can issue credentials":

1. **Pick a subdomain** under a domain you already own — e.g. `ies.tpddl.in`.
2. **Generate a key pair** and **publish a small `did.json` file** at `https://ies.tpddl.in/.well-known/did.json`.
3. **Hand that DID** (`did:web:ies.tpddl.in`) to the IES network operator to add to the reference list of registered DISCOMs.

That's it for identity. Internal consumer numbers, meter SLNOs, and asset codes do **not** need to change — they ride inside the credentials you sign with this DID. Consumers do not need to do anything; their wallet (or DigiLocker) generates a `did:key` for them automatically the first time they receive a credential.

If something in those three steps feels unfamiliar — what a key pair is, what JSON to put in the file — the next section walks through it in full.

---

## Step-by-step: publish your `did:web` (and run OpenCred locally)

The practical setup is one Docker container plus one JSON file on a web server you already run. The commands below are taken verbatim from the [OpenCred bootcamp — Local Docker](https://opencred.gitbook.io/docs/bootcamp/local-docker) page; if you want the why behind any step, follow the link.

### What you'll need

- A subdomain you control, e.g. `ies.tpddl.in`. Most DISCOMs pick a dedicated subdomain so the credential-issuing identity is cleanly separated from the public-facing website.
- A static-file host serving HTTPS — any nginx, S3-with-CloudFront, GitHub Pages, or your existing web server is fine.
- Docker 24+, `curl`, `jq`, `openssl`, and ~2 GB free disk. The OpenCred container ships ready to issue.

### 1. Pull the OpenCred image

```bash
docker pull ghcr.io/nfh-trust-labs/opencred/opencred-server:latest
docker tag  ghcr.io/nfh-trust-labs/opencred/opencred-server:latest opencred:bootcamp
```

### 2. Generate a signing key and API token

The same EC P-256 key works for both `did:web` and `did:key`; the difference is just which DID method OpenCred presents it as.

```bash
mkdir -p ~/opencred/keys
cd ~/opencred

openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 \
  -out keys/issuer-key.pem
chmod 600 keys/issuer-key.pem

export OPENCRED_API_KEY="$(openssl rand -base64 32)"
echo "Save this: $OPENCRED_API_KEY"
```

Keep `issuer-key.pem` in your KMS in production. Treat it like a TLS private key.

### 3. Run OpenCred in `did:web` mode

```bash
docker run -d \
  --name opencred \
  -p 3100:3100 \
  -e OPENCRED_API_KEY="$OPENCRED_API_KEY" \
  -e OPENCRED_KEY_PATH=/secrets/issuer-key.pem \
  -e OPENCRED_ISSUER_DID_METHOD=web \
  -e OPENCRED_ISSUER_DOMAIN=ies.tpddl.in \
  -v "$HOME/opencred/keys/issuer-key.pem:/secrets/issuer-key.pem:ro" \
  --read-only --cap-drop ALL \
  opencred:bootcamp

curl -s http://localhost:3100/v1/health | jq
# expect "signingKeyLoaded": true
```

> **Want offline-verifiable identity instead?** Drop `OPENCRED_ISSUER_DID_METHOD` and `OPENCRED_ISSUER_DOMAIN` and OpenCred runs in `did:key` mode by default. The same key, the same API — only the `did:` string the container reports changes. This is the right choice for first-deploy testing, demos, and consumer wallets. See [`did:key` in Appendix A](#didkey--what-wallets-give-consumers).

### 4. Assemble your `did.json` from the container

OpenCred publishes the JWK form of your public key on its keys endpoint. Fetch it, drop it into the standard DID document template, and publish.

```bash
curl -s http://localhost:3100/v1/keys \
  -H "Authorization: Bearer $OPENCRED_API_KEY" | jq '.keys[0]'
```

Use the JWK from that response in this template:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/jws-2020/v1"
  ],
  "id": "did:web:ies.tpddl.in",
  "verificationMethod": [{
    "id": "did:web:ies.tpddl.in#key-0",
    "type": "JsonWebKey",
    "controller": "did:web:ies.tpddl.in",
    "publicKeyJwk": { "kty": "EC", "crv": "P-256", "x": "...", "y": "..." }
  }],
  "authentication":  ["did:web:ies.tpddl.in#key-0"],
  "assertionMethod": ["did:web:ies.tpddl.in#key-0"]
}
```

Three things matter, and you can ignore the rest until later:

- **`verificationMethod`** is the public key. Verifiers use it to check your signatures.
- **`assertionMethod`** says which key is allowed to issue credentials.
- **`authentication`** says which key can sign requests on behalf of the DID.

You can add a `service` array later when your Beckn BPP and OpenCred endpoints are publicly addressable; the DID is valid without it.

### 5. Publish the file

Upload it so this URL returns the JSON:

```
https://ies.tpddl.in/.well-known/did.json
```

The `.well-known/` path is a standard convention; verifiers know to look there. A normal TLS cert is enough — the same one that already terminates your subdomain — and there must be no redirect.

### 6. Verify it from the outside

```bash
curl -s https://ies.tpddl.in/.well-known/did.json | jq .id
# "did:web:ies.tpddl.in"
```

If that command prints your DID, you're done — any participant on the network can now resolve `did:web:ies.tpddl.in` to your public key and verify any credential you sign.

### 7. Register with the IES network

Send your DID, your legal name, and your service-area list to the IES network operator. They add an entry under their own namespace pointing at your DID, and from that moment your credentials are recognised as coming from a known DISCOM on the network. The operator's onboarding kit lists the exact fields. The OpenCred-side issuance call that follows assumes this step is done.

That's all you need to start signing credentials. Everything below is optional reading.

---

## ID patterns you'll use day one

You only need two or three identifier shapes to start issuing credentials. They're collected here in one table.

| Subject | Identifier | Example |
|---|---|---|
| Your DISCOM (issuer) | `did:web:<your-domain>` | `did:web:ies.tpddl.in` |
| A regulator | `did:web:<their-domain>` | `did:web:ies.derc.gov.in` |
| A consumer (holder DID) | `did:key:...` — *generated by the wallet, not you* | `did:key:z6MkjVQ8r4f3rPuY...` |
| The consumer's existing CIS account number | Plain string, kept as-is | `TPDDL-2025-00987654` |

A few things worth knowing before you start:

- **You do not assign holder DIDs.** When a consumer requests a credential, their wallet (or DigiLocker) sends you a `did:key` it just generated. You include it verbatim in `credentialSubject.id`. You never store the consumer's private key.
- **Your CIS consumer numbers stay exactly as they are.** They go into `customerProfile.customerNumber` in the credential, in the same human-readable form your call centre and billing letters use today.
- **A consumer who doesn't have a wallet yet is fine.** The `credentialSubject.id` field is optional. You can issue a credential carrying just the `customerNumber`, and bind a holder DID later if/when the consumer claims it.

For identifiers covering assets (meters, transformers, feeders), service connections, and datasets, see [Appendix C](#appendix-c-identifying-assets-meters-connections-datasets) — these are not needed for your first credential.

---

## Where each ID goes in a credential

Here is one filled-in ElectricityCredential v1.2 showing every identifier in one place. Everything in **bold** is something you control.

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://schema.beckn.io/ElectricityCredential/v1.2/context.jsonld"
  ],
  "id": "urn:uuid:b2c3d4e5-0000-0000-0000-aabbccdd0001",
  "type": ["VerifiableCredential", "ElectricityCredential"],

  "issuer": {
    "id":   "did:web:ies.tpddl.in",
    "name": "Tata Power Delhi Distribution Limited",
    "idRef": {
      "issuedBy":  "did:web:ies.derc.gov.in",
      "subjectId": "derc.delhi.gov.in:TPDDL-REG-0042"
    }
  },

  "validFrom":  "2025-03-01T00:00:00+05:30",
  "validUntil": "2026-03-01T00:00:00+05:30",

  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
    "customerProfile": {
      "customerNumber": "TPDDL-2025-00987654",
      "energyResources": [{
        "id":   "did:web:ies.tpddl.in:assets:meter:MET-IMPORT-001",
        "type": "METER",
        "attributes": {"meterCapability": "AMI", "energyDirection": "Forward"}
      }]
    },
    "customerDetails": {
      "fullName": "Arjun Mehra"
    }
  },

  "proof": {
    "type": "Ed25519Signature2020",
    "verificationMethod": "did:web:ies.tpddl.in#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z58DAdFfa9SkqZMVPxAQpic7ndTaXoT..."
  }
}
```

| Field | What it carries | Set by |
|---|---|---|
| `issuer.id` | Your `did:web` | You |
| `issuer.idRef` | A pointer the regulator gave you that confirms you are a licensed DISCOM in their service area | Regulator + you |
| `credentialSubject.id` | The consumer's holder DID | The consumer's wallet |
| `customerProfile.customerNumber` | Your existing CIS number, unchanged | You |
| `energyResources[].id` | A `did:web` for each meter / asset, built from your domain plus a path segment | You |
| `proof.verificationMethod` | A pointer back into your `did.json` saying which key did the signing | OpenCred / your signing pipeline |

Notice what is *not* there: no central registry of consumers, no national ID, no separate identifier system that competes with your CIS. Everything cross-references your DID document plus the regulator's, both of which are just static files on websites you control.

---

## Appendix A — How DIDs work, and the three methods IES uses

This appendix exists so that if a colleague asks "but how does this actually work?" you can answer. Skip it if you are mid-deployment.

### What's in a DID document

A DID string by itself is just a name. The useful part is the **DID document** it resolves to — the small JSON object you published in the step above. That document carries the public keys a verifier needs, and optionally the service endpoints where the network can reach you.

```mermaid
flowchart LR
  A["DID string<br/><code>did:web:ies.tpddl.in</code>"] -->|resolve| B["DID Document<br/>(JSON)"]
  B --> C["<b>verificationMethod</b><br/>public keys for<br/>signature checks"]
  B --> D["<b>assertionMethod</b><br/>which keys may issue<br/>credentials"]
  B --> E["<b>service</b><br/>OpenCred / Beckn<br/>endpoints"]
```

Two rules cover most confusion in DID systems:

- **An identifier is just a name.** Never parse it to extract meaning ("if the string contains `tpddl`, treat it as a TPDDL credential" is a bug waiting to happen). Resolve it first; read the document; decide from that.
- **The identifier and the record it resolves to are different things.** The DID is what travels in a credential or a Beckn message. The record is what a verifier fetches to make a trust decision.

### The three DID methods IES uses

IES uses three standard W3C DID methods. All three are listed in the [W3C DID Spec Registries](https://www.w3.org/TR/did-spec-registries/), so any standards-compliant verifier already knows how to resolve them. **There is no separate `did:dedi` method.** When you see DeDi mentioned, it is acting as a key-discovery layer for `did:web` (or `did:key`), not as a new DID method.

For the underlying theory — when each method is appropriate, what they buy you, what they cost — the canonical reference is [OpenCred → DIDs](https://opencred.gitbook.io/docs/concepts/dids). This section is the IES-flavoured summary.

#### `did:web` — the one your DISCOM will use

The DID is a URL in disguise. `did:web:ies.tpddl.in` resolves to `https://ies.tpddl.in/.well-known/did.json`. Path segments after the host become URL path segments:

```
did:web:example.com:students
→  https://example.com/students/did.json
```

A port becomes `%3A` (so `did:web:localhost%3A8443` is `https://localhost:8443/.well-known/did.json`).

There are two ways `did:web` shows up in IES:

- **Self-hosted by the institution.** You serve `did.json` on your own domain, as Step 3 above shows. Any verifier in the world can resolve it. This is the default and the right starting point for every DISCOM, regulator, and aggregator with a public web presence.
- **Anchored on DeDi.** The identifier is still your DISCOM's own `did:web:<your-domain>`. The difference is that, in addition to (or instead of) hosting `did.json` yourself, you publish your public key — and optionally a frozen `did.json` snapshot — into DeDi's key registry, under a namespace tied to your verified identity. DeDi-aware verifiers can then fetch your key from DeDi via its API. This is useful as a fallback when your domain is unreachable, or where the network wants a curated allow-list of registered DISCOMs. The method is still `did:web`; DeDi is just a second discovery path for the same key. Note that a DeDi-only document is not served at `.well-known/did.json`, so a plain W3C `did:web` resolver will not see it — only DeDi-aware tooling will.

The strengths of `did:web` for an institutional issuer:

- Trust roots in your existing TLS certificate, which public CAs already validate.
- Key rotation is one file replace.
- No new infrastructure beyond a static-file host.

The main limitation is that domain hijack would mean identity hijack. IES mitigates this by *also* registering each DISCOM in the network's reference list, which acts as the curated allow-list of "who counts as a DISCOM". An attacker who steals a domain still cannot pass for a registered DISCOM on the network unless they also compromise that list.

#### `did:key` — what wallets give consumers

For `did:key`, the public key *is* the identifier. The verifier decodes the string directly — no network call, no website needed. That is exactly what you want for consumers, who do not own domains:

```
did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z
```

IES uses `did:key` for:

- Consumer holder DIDs, generated client-side by a wallet or DigiLocker.
- DISCOM dev/test deployments before a real subdomain is provisioned.
- Demos and field deployments where there is no domain.

The price you pay is that you cannot rotate the key — rotating means a new DID. So `did:key` is fine for short-lived or device-bound identities, but inappropriate for long-lived institutional issuers (which is why DISCOMs use `did:web`).

#### `did:jwk` — same shape as `did:key`, JWK-encoded

`did:jwk` encodes the public key as a JSON Web Key inside the DID string. Functionally similar to `did:key` (offline-resolvable, no rotation, no service endpoints), but interoperates with JWK-based tooling — useful for RSA keys, for example, where `did:key` is awkward. IES accepts `did:jwk` for holders. If you don't have a specific reason to use it, default to `did:key`.

### Quick reference

| Subject | Method | Why |
|---|---|---|
| DISCOM (issuer) | `did:web` | Domain anchors the key, regulator's registry anchors trust |
| Regulator | `did:web` | Same |
| Consumer (holder) | `did:key` or `did:jwk` | Wallet-generated, no domain needed, verifies offline |

---

## Appendix B — Issuing and revoking an ElectricityCredential v1.2 with OpenCred

This appendix walks end-to-end through issuing and revoking an [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md) using the OpenCred container you started in [Step 3](#3-run-opencred-in-didweb-mode). It is the IES-flavoured continuation of the [OpenCred bootcamp — Local Docker](https://opencred.gitbook.io/docs/bootcamp/local-docker); refer to that page for the underlying API contracts, error shapes, and production-hardening notes.

### Prerequisites

- The OpenCred container from Step 3 is running, with `$OPENCRED_API_KEY` exported in your shell.
- `https://ies.tpddl.in/.well-known/did.json` is serving your DID document (Steps 4–5).
- The IES network operator has accepted your registration (Step 7) and the regulator has issued the `idRef` you will quote in `issuer.idRef`.

### 1. Confirm the issuer DID OpenCred reports

```bash
export ISSUER_DID="$(curl -s http://localhost:3100/v1/keys \
  -H "Authorization: Bearer $OPENCRED_API_KEY" | jq -r '.keys[0].id | split("#")[0]')"
echo "$ISSUER_DID"
# did:web:ies.tpddl.in
```

If you ran the container in `did:key` mode, this prints `did:key:z…` instead — the rest of the flow is identical, only the issuer string changes.

### 2. Issue the credential

A new-connection ElectricityCredential carries the consumer's CIS number, one `energyResources[]` entry per meter, and (optionally) a holder DID provided by the consumer's wallet. POST it to `/v1/credentials/issue`:

```bash
curl -s http://localhost:3100/v1/credentials/issue \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"schemaId\":    \"ElectricityCredential/v1.2\",
    \"issuerDid\":   \"$ISSUER_DID\",
    \"proofFormat\": \"vc-jwt\",
    \"validFrom\":   \"2026-04-01T00:00:00+05:30\",
    \"validUntil\":  \"2031-04-01T00:00:00+05:30\",
    \"credentialSubject\": {
      \"id\": \"did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z\",
      \"customerProfile\": {
        \"customerNumber\": \"TPDDL-2025-00987654\",
        \"energyResources\": [{
          \"id\":   \"did:web:ies.tpddl.in:assets:meter:MET-IMPORT-001\",
          \"type\": \"METER\",
          \"attributes\": {\"meterCapability\": \"AMI\", \"energyDirection\": \"Forward\"}
        }],
        \"consumptionProfiles\": [{
          \"meterId\":            \"did:web:ies.tpddl.in:assets:meter:MET-IMPORT-001\",
          \"sanctionedLoad\":     {\"value\": 10, \"unit\": \"kW\"},
          \"tariffCategoryCode\": \"DS-I\",
          \"premisesType\":       \"Residential\",
          \"connectionType\":     \"Single-phase\"
        }]
      },
      \"customerDetails\": {
        \"fullName\":              \"Arjun Mehra\",
        \"serviceConnectionDate\": \"2018-07-15T00:00:00+05:30\"
      }
    }
  }" | tee credential.json | jq .credential
```

Two things worth noting:

- **Every identifier is a `did:web` derived from a domain you control.** Meter IDs use the colon-path form (`did:web:ies.tpddl.in:assets:meter:<slno>`). The same pattern works for transformers, feeders, and substations — see [Appendix C](#appendix-c--identifying-assets-meters-connections-datasets).
- **The regulator's `issuer.idRef`** (`{ issuedBy, subjectId }`) is appended by your pipeline after OpenCred returns the credential, then re-submitted for signing if your flow requires it. OpenCred itself does not know your regulator relationship.

### 3. Verify the credential

```bash
jq -n --arg c "$(jq -r '.credential.proof.jwt' credential.json)" '{credential: $c}' | \
  curl -s http://localhost:3100/v1/credentials/verify \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" \
    -d @- | jq
# expect "valid": true
```

### 4. Revoke the credential

OpenCred publishes revocation as a hash entry into a DeDi-hosted revocation registry. The credential format does not change; the verifier reads `credentialStatus` and looks up the hash. See [OpenCred → Revocation](https://opencred.gitbook.io/docs/concepts/revocation) for the conceptual model.

Compute the revocation hash from the issued credential, then submit the revoke call:

```bash
HASH=$(jq '{credential: .credential}' credential.json | \
  curl -s http://localhost:3100/v1/credentials/revocation-hash \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" -d @- | jq -r .revocationHash)

curl -s http://localhost:3100/v1/credentials/revoke \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"hash\": \"$HASH\", \"reason\": \"connection-terminated\"}" | jq
```

Check status:

```bash
curl -s http://localhost:3100/v1/credentials/revocation-status \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"hash\": \"$HASH\"}" | jq
```

Revocation via DeDi requires the relevant `OPENCRED_DEDI_*` env vars on the container (`OPENCRED_DEDI_BASE_URL`, `OPENCRED_DEDI_AUTH_TYPE`, `OPENCRED_DEDI_API_KEY`, `OPENCRED_DEDI_NAMESPACE`). The [OpenCred bootcamp page](https://opencred.gitbook.io/docs/bootcamp/local-docker) lists the full set and where to obtain them for your network.

### 5. End-to-end smoke test

A passing integration test should:

1. Issue a credential to a `did:key` holder.
2. Resolve `issuer.id` (fetch `did.json` over HTTPS) and confirm the public key matches the one that signed `proof`.
3. Resolve `issuer.idRef.issuedBy` (the regulator's `did:web`) and confirm your DISCOM is listed under their registry.
4. Verify the credential via `/v1/credentials/verify` and confirm `valid: true`.
5. Check `revocation-status` — expect "not revoked".
6. Revoke the credential.
7. Re-check `revocation-status` — expect "revoked".

Run this on every release. It is the simplest possible smoke test that covers all the identifier flows in one credential.

### What you have at the end

| Artefact | Where |
|---|---|
| Issuer DID document | `https://ies.tpddl.in/.well-known/did.json` |
| Registered DISCOM entry | Under the IES network operator's reference registry |
| Asset DIDs | `did:web:ies.tpddl.in:assets:<class>:<id>` (no extra hosting required if you serve a directory listing or DID document per asset) |
| Revocation entries | Hash records in the DeDi revocation registry your OpenCred is configured against |
| Signed credentials | OpenCred output, delivered to wallets or DigiLocker |

For production deployments — horizontal scale, Cloud HSM key management, the full HTTP API — go straight to [OpenCred → Docker image](https://opencred.gitbook.io/docs/docker-image/docker) and [OpenCred → API reference](https://opencred.gitbook.io/docs/docker-image/api-reference). Nothing on this page contradicts those; this page just adds the IES-specific identifier wiring on top.

---

## Appendix C — Identifying assets, meters, connections, datasets

You will eventually want stable identifiers for the things you operate (meters, transformers, feeders, service connections) and the data you publish (telemetry, tariff schedules). Use the same `did:web` you already own and add path segments. No new DID method needed.

### Conventions

| Symbol | Meaning |
|---|---|
| `<discom-domain>` | The domain hosting your `did.json` — e.g. `ies.tpddl.in` |
| `<internal-id>` | Your existing internal ID, used verbatim as the last path segment |
| URL-safe | Replace any characters outside `[A-Za-z0-9._-]` with `%xx` percent-encoding |

### Meter

```
did:web:<discom-domain>:assets:meter:<meter-slno>

→ did:web:ies.tpddl.in:assets:meter:MET-IMPORT-001
```

This is the identifier that goes in `energyResources[].id` for METER entries on an [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md).

### Other assets — transformer, feeder, substation, solar, BESS, EV charger

```
did:web:<discom-domain>:assets:<class>:<internal-id>

→ did:web:ies.tpddl.in:assets:transformer:DT-NDL-11KV-04572
→ did:web:ies.tpddl.in:assets:feeder:FDR-11KV-NDL-072
→ did:web:ies.tpddl.in:assets:substation:SS-22OK-NJP-001
→ did:web:ies.tpddl.in:assets:solar-plant:ROOFTOP-SOLAR-001
```

`<class>` values used in IES today: `feeder`, `transformer`, `substation`, `solar-plant`, `wind-farm`, `bess`, `ev-charger`, `meter`. Use kebab-case.

### Service connection

The connection binds a consumer, a meter, and a feeder:

```
did:web:<discom-domain>:connections:<connection-id>

→ did:web:ies.tpddl.in:connections:CONN-TPDDL-2025-001234567
```

`<connection-id>` is whatever your CIS already uses — often the same string as the consumer number.

### Dataset (Beckn `DatasetItem`)

For data-exchange resources (meter telemetry, ARR filings, tariff schedules):

```
did:web:<discom-domain>:datasets:<class>:<id>

→ did:web:ies.tpddl.in:datasets:meter-telemetry:2026-01
→ did:web:ies.derc.gov.in:datasets:tariff-orders:2025-26-domestic
```

The DID resolves to a `DatasetItem` record (DDM schema) carrying the Beckn BPP endpoint that serves the actual data.

### Summary

| Subject | Pattern | Internal ID becomes |
|---|---|---|
| DISCOM | `did:web:<domain>` | The domain itself |
| Regulator | `did:web:<domain>` | Same |
| Consumer (holder) | `did:key:…` (wallet-generated) | Not derived from anything internal |
| Consumer (CIS reference) | Kept as the literal `customerNumber` string | CIS number, verbatim |
| Meter | `did:web:<domain>:assets:meter:<slno>` | Meter SLNO |
| Other asset | `did:web:<domain>:assets:<class>:<id>` | SAP / GIS code |
| Connection | `did:web:<domain>:connections:<id>` | SC number |
| Dataset | `did:web:<domain>:datasets:<class>:<id>` | Dataset key |

---

## Appendix D — Identifier vs. record

One last conceptual rule worth internalising, because it removes most confusion later:

| Identifier | Record |
|---|---|
| `did:web:ies.tpddl.in` | The DID document at `https://ies.tpddl.in/.well-known/did.json` |
| `did:web:ies.tpddl.in:assets:meter:MET-IMPORT-001` | The asset record served under that path |

The **identifier** is the string that travels — in a credential, a Beckn message, a database row. The **record** is the JSON a resolver returns, and the thing trust decisions read. Identifiers are stable; records can be updated (key rotation, asset commissioning, address change) without changing the identifier they live under.

If your team ever finds itself trying to "parse" a DID to make a business decision, stop and resolve it instead. The document at the end of the resolution is the source of truth, never the string.

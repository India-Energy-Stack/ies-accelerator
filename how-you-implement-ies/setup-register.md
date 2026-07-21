# Setup Register

> **Step 1 of the implementation path — set up.** Get your organisation a verifiable digital identity, list it in the shared directory, and — if your use cases need a Beckn network — publish your network identity too. *Done once.* Takes less than 30 minutes.

The concepts behind every artefact on this page — DIDs, DeDi, namespaces, subscriber records — are in **[What IES Provides → Register](../what-ies-provides/register.md)**. This page is the do-guide.

---

## Who does what

Registration is role-based. Everyone does §1.1–1.4; the rest depends on what you plan to run.

| You are… | Do | Then go to |
|---|---|---|
| **A DISCOM / AMISP issuing credentials only** (Consumer Energy Passport, Meter Digest) | §1.1 – §1.4 | [Issue Credentials](issue-credentials.md) |
| **Any organisation joining a Beckn network** (data exchange, P2P trading — DISCOMs, AMISPs, trading platforms, aggregators) | §1.1 – §1.4, then §1.5 – §1.7 | [Setup Exchange](setup-exchange.md) |
| **A network operator (NFO)** running your own Beckn network | §1.1 – §1.4, then §1.8 | NFH network-operator docs (linked in §1.8) |

Trading platforms and other pure Beckn participants who never issue credentials still need §1.1–1.4: the domain, `did.json`, and the verified DeDi namespace are the root of trust that the Beckn subscriber record hangs off.

## What you'll have at the end

- A resolvable `did:web` for your organisation.
- Your public signing key published at a well-known URL under your domain.
- A verified DeDi namespace anchored to your domain, plus a DeDi API key.
- *(Beckn participants)* An Ed25519 message-signing keypair, a published Beckn subscriber record, and a reference entry in an IES network registry.

## Before you start

- **A domain or subdomain you control**, with the ability to host one small static file under it.
- **DNS access** — to add one TXT record (DeDi domain verification).
- **`openssl`, `python3`, `curl`, `jq`** on the machine where you generate keys.
- *(Beckn participants, §1.5 only)* **Go 1.21+** — see [the official Go install guide](https://go.dev/doc/install).

---

## 1.1 — Pick a domain (or subdomain) you control

Either works. Most DISCOMs use a dedicated subdomain so the credential-issuing identity is cleanly separated from the marketing site:

- `ies.discom.example` (subdomain)
- `discom.example` (apex domain — equally valid)

The host you pick becomes the host portion of your `did:web`. Your DID document will live at `https://<your-host>/.well-known/did.json`.

Once picked, record it in an environment variable — the copy-pasteable commands in this guide and in [Issue Credentials](issue-credentials.md) all reference `$OPENCRED_ISSUER_DOMAIN`, so you set your domain once here and never hand-edit a command:

```bash
export OPENCRED_ISSUER_DOMAIN="ies.yourdiscom.in"
```

> **Hosting `did.json` in a subfolder instead of the domain root?** `did:web` encodes sub-paths with colons, and `OPENCRED_ISSUER_DOMAIN` accepts the same form: set `OPENCRED_ISSUER_DOMAIN="<discom-domain>:subfolder"` and your DID becomes `did:web:<discom-domain>:subfolder`. The generator in §1.3 works unchanged, but the hosting path changes: a path-form DID resolves to `https://<discom-domain>/subfolder/did.json` — **no `.well-known/`** — so in §1.3 replace the colon with a slash and drop `.well-known/` when uploading and verifying. Variant table in [Register — DID and DID document](../what-ies-provides/register.md#the-did-methods-ies-uses).

---

## 1.2 — Generate your credential-signing keypair

You will sign every credential with this key. Treat it as a production credential — KMS / HSM where possible, otherwise a securely backed-up file on a hardened host. The key is **EC P-256** (matches W3C VC Data Model 2.0 defaults):

```bash
mkdir -p ~/opencred/keys
cd ~/opencred

openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 \
  -out keys/issuer-key.pem
chmod 600 keys/issuer-key.pem
```

Keep `issuer-key.pem` in your KMS in production. Treat it like a TLS private key. [Issue Credentials](issue-credentials.md) mounts this exact file into the OpenCred signing container, so keep the `~/opencred/keys/` path (or adjust consistently later).

> This key signs **credentials**. Beckn messages use a different key (Ed25519, §1.5). The two identities intentionally use separate keys, live in different registries, and serve different verifiers, so a compromise of one does not compromise the other.

---

## 1.3 — Generate and publish `did.json`

The DID document is one small JSON file: your DID string plus the public half of the key from §1.2. The block below is a complete generator — paste it as-is and it writes a finished `did.json`, with the DID `id`, `controller`, and JWK `x`/`y` coordinates all filled in from `$OPENCRED_ISSUER_DOMAIN` and `~/opencred/keys/issuer-key.pem`. Nothing to hand-edit.

```bash
python3 - > did.json <<'PY'
import subprocess, base64, json, os, sys
domain = os.environ.get("OPENCRED_ISSUER_DOMAIN")
if not domain:
    sys.exit("OPENCRED_ISSUER_DOMAIN is not set - run the export in 1.1 first")
key = os.path.expanduser("~/opencred/keys/issuer-key.pem")
der = subprocess.run(["openssl", "pkey", "-in", key, "-pubout", "-outform", "DER"],
                     capture_output=True, check=True).stdout
pt = der[-65:]  # uncompressed EC point: 0x04 || X(32) || Y(32)
b64u = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode()
did = f"did:web:{domain}"
print(json.dumps({
    "@context": [
        "https://www.w3.org/ns/did/v1",
        "https://w3id.org/security/suites/jws-2020/v1"
    ],
    "id": did,
    "verificationMethod": [{
        "id": f"{did}#key-0",
        "type": "JsonWebKey2020",
        "controller": did,
        "publicKeyJwk": {"kty": "EC", "crv": "P-256",
                         "x": b64u(pt[1:33]), "y": b64u(pt[33:65])}
    }],
    "authentication":  [f"{did}#key-0"],
    "assertionMethod": [f"{did}#key-0"],
}, indent=2))
PY
cat did.json
```

Expected: `cat did.json` prints a complete DID document with your domain in `id` and real `x`/`y` coordinates in `publicKeyJwk`.

> **On Windows?** The Python itself is cross-platform, but this block is written for a POSIX shell — the `python3 - <<'PY' … PY` heredoc, the `python3` command name, and `cat` don't work in native `cmd.exe`/PowerShell. Run it from **WSL** or **Git Bash**, where it works as-is (and where `openssl`, `curl`, and `jq` from §1.1 are also available). If you must stay in PowerShell, save the Python between `<<'PY'` and `PY` to a file (e.g. `gen-did.py`), then run `python gen-did.py > did.json` (use `python` or `py`, not `python3`).

Three fields matter, and you can ignore the rest until later:

- **`verificationMethod`** is the public key. Verifiers use it to check your signatures.
- **`assertionMethod`** says which key is allowed to issue credentials.
- **`authentication`** says which key can sign requests on behalf of the DID.

> **Keep the verification-method `type` as `JsonWebKey2020`.** It is the type defined by the `jws-2020` context already listed in `@context`, and it is the type that mainstream verifier libraries (did-jwt / Veramo, Spruce, `jose`-based stacks) map to your P-256 key for `ES256`. The plain `JsonWebKey` name is valid did-core, but several widely used verifiers do **not** resolve it to an `ES256` key and reject the signature with a "no suitable keys" error — a genuine, correctly signed credential then fails to verify. Publish `JsonWebKey2020` so any verifier can find your key.

You can add a `service` array later when your Beckn and OpenCred endpoints are publicly addressable; the DID is valid without it.

**Publish it.** Upload the file so this URL returns the JSON:

```
https://$OPENCRED_ISSUER_DOMAIN/.well-known/did.json
```

The `.well-known/` path is a standard convention; verifiers know to look there. A normal TLS cert is enough — the same one that already terminates your subdomain — and there must be **no redirect** on that URL.

**Verify it from outside your network:**

```bash
curl -s "https://$OPENCRED_ISSUER_DOMAIN/.well-known/did.json" | jq .id
```

Expected: your DID, e.g. `"did:web:ies.yourdiscom.in"`. If that prints, identity setup is done from the wire-protocol side — any participant can now resolve your `did:web` to your public key and verify anything you sign.

---

## 1.4 — Claim a DeDi namespace and verify your domain

DeDi is the public registry mechanism IES uses for namespaces, credential revocation, and Beckn subscriber membership. Claiming a namespace ties your organisation's records to your domain in a way anyone can verify.

1. **Sign up at [publish.dedi.global](https://publish.dedi.global)** using an organisational role mailbox (`registry-admin@discom.example`).
2. **Create a namespace** — use a short name that maps to your organisation (`discom`, `np.example.com`).
3. **Verify your domain** — DeDi issues a DNS TXT record; add it to your DNS zone and click *Verify*. Wait for DNS propagation (usually 15 minutes; can take up to 48 hours). Once verification completes, a green **verified** label appears on your namespace in [publish.dedi.global](https://publish.dedi.global), and the namespace becomes publicly visible on [explore.dedi.global](https://explore.dedi.global) — only verified namespaces are listed there, so appearing in explore results is itself the public verification signal.
4. **Create an API key** — in the DeDi UI, click your avatar in the top-right corner, then **Manage API key**. Tools that write into your namespace (OpenCred for revocation entries, your registry publisher) authenticate with this key. Store it alongside your other secrets.

You create the empty namespace here. What goes inside it depends on your role:

- **For credential issuance**, you do **not** need to create the registries by hand — when you run OpenCred in [Issue Credentials](issue-credentials.md), it auto-creates the four it needs on first boot (`vc-revocation-registry`, `opencred-key-registry`, `schema_registry`, `context_registry`).
- **As a participant on a Beckn network**, you create **subscriber registries** by hand (§1.6) — one record per role/environment declaring your callback URL and message-signing key.
- **As a network operator (NFO)**, you create a **directory of participants** — a Beckn *subscriber-reference* registry (§1.8) that curates which subscribers belong to your network.

DeDi itself is documented at **[docs.nfh.global](https://docs.nfh.global/)**; the IES-specific registry map is in **[Register — The directory: DeDi](../what-ies-provides/register.md#the-directory-dedi)**.

> **Checkpoint — issuing credentials only?** You are done with registration. Continue to **[Issue Credentials](issue-credentials.md)**, which runs the OpenCred signing container against the domain, key, namespace and API key you just set up (and auto-creates those four registries). The remaining sections of this page are for Beckn-network participants.

---

## 1.5 — *(Beckn participants)* Generate your Beckn signing keypair

**Prerequisite:** §1.1–1.4 complete; Go installed.

Beckn message signing uses **Ed25519** keys — a different key from the P-256 credential key in §1.2. Beckn ONIX ships a small generator that prints the two Base64 values the subscriber record and your ONIX config need:

```bash
git clone https://github.com/beckn/beckn-onix.git
cd beckn-onix
go run install/generate-ed25519-keys.go
```

Expected output — two lines:

```
signingPrivateKey: <Base64, 32-byte seed>
signingPublicKey:  <Base64, 32-byte public key>
```

- **`signingPrivateKey`** — store in your secret manager; ONIX loads it to sign outgoing messages ([Setup Exchange §3.3](setup-exchange.md#id-3.3-swap-in-your-real-identity)). Never commit it.
- **`signingPublicKey`** — publish in your subscriber record (§1.6). Other Beckn nodes fetch it to verify your message signatures.

The generator source is [`install/generate-ed25519-keys.go`](https://github.com/beckn/beckn-onix/blob/main/install/generate-ed25519-keys.go); any other Ed25519 keypair generator works as long as it produces the same two Base64 artefacts (raw 32-byte seed and raw public key, no PEM headers).

---

## 1.6 — *(Beckn participants)* Publish your Beckn subscriber record

**Prerequisite:** verified namespace (§1.4), Ed25519 public key (§1.5), and the public HTTPS URL where your Beckn adapter will receive messages (you can publish first and deploy the adapter in [Setup Exchange](setup-exchange.md); the URL just has to be the one you will use).

1. **Create a subscriber registry** under your verified namespace in [publish.dedi.global](https://publish.dedi.global), with the built-in **`beckn_subscriber`** tag. Create **one registry per environment** — `subscribers-test` and `subscribers-prod` — so a misconfigured test run can never pollute a production lookup.

2. **Add a record** with these fields:

   | Field | What to fill | Example |
   |---|---|---|
   | `subscriber_id` | Your **`did:web`** — the same org identity you published in §1.3. Using the DID (not a bare hostname) keeps your Beckn identity and your credential identity the same string. | `did:web:ies.discom.example` |
   | `subscriber_url` | Your Beckn ONIX receiver endpoint | `https://ies.discom.example/bpp/beckn` |
   | `type` | Your role on the network | `BAP` (consumer) or `BPP` (provider) |
   | `signing_public_key` | The Ed25519 public key from §1.5, Base64, no header/footer | `eyAeqGFtAuks...` |
   | `encryption_public_key` | *(Optional)* encryption public key | `lCI84I0Q0U0w...` |
   | `countries` | Countries where you operate | `["IND"]` |

   If you operate in both roles (BAP *and* BPP), publish a separate record per role. That `did:web` `subscriber_id` is what you set as `networkParticipant` in your ONIX config ([Setup Exchange §3.3](setup-exchange.md#id-3.3-swap-in-your-real-identity)).

3. **Note the record ID** DeDi assigns — you will configure it into ONIX as the `keyId` in [Setup Exchange §3.3](setup-exchange.md#id-3.3-swap-in-your-real-identity).

4. **Verify the lookup.** Other nodes resolve your record through the Beckn fabric lookup URL. Substitute `<your-subscriber-id>` (your DeDi namespace from §1.4 — the path is addressed by this subscriber id, not by the `did:web` value of the `subscriber_id` record field) and `<your_record_id>` (from step 3); `subscribers.beckn.one` is the fixed fabric schema keyword — leave it literal, it is not your registry name. Allow 5–10 minutes for the cache, then:

   ```bash
   curl -s "https://fabric.nfh.global/registry/dedi/lookup/<your-subscriber-id>/subscribers.beckn.one/<your_record_id>" | jq
   ```

   Expected: the record you just published, including your `signing_public_key`. At this point `network_memberships` is empty — the NFO fills it in §1.7.

---

## 1.7 — *(Beckn participants)* Get referenced into an IES network

**Prerequisite:** subscriber record published and resolvable (§1.6).

A subscriber record alone does not put you on a network. Each IES network is a curated registry operated by the IES network operator (the [NFO](../glossary.md#nfo) — currently REC / IES Secretariat under the `indiaenergystack.in` namespace). To join, the NFO writes a **reference entry** pointing at your subscriber record; your identity stays self-owned, nothing is copied.

The networks you can apply to:

| Network registry | Env | Purpose |
|---|---|---|
| `ies-data-sharing-network` / `test-…` | prod / test | Energy data sharing (DISCOM ↔ DISCOM, regulators, aggregators) |
| `ies-p2p-trading-network` / `test-…` | prod / test | P2P energy trading between consumers, prosumers, aggregators |
| `ies-der-integration-network` / `test-…` | prod / test | DER (rooftop solar, BESS, EV) integration with DISCOMs |

**Apply by email** to the IES Secretariat — [IES.Secretariat@fsrglobal.org](mailto:IES.Secretariat@fsrglobal.org) (alternate: [ies@recindia.com](mailto:ies@recindia.com); web: [ies.fsrglobal.org](https://ies.fsrglobal.org/#footer)) — with:

- Your short identifier (`<discom-short-code>` for DISCOMs, FQDN for other participants).
- Your verified DeDi namespace (e.g. `discom`, `np.example.com`).
- The DeDi lookup URL of either your **whole subscriber registry** (typically `subscribers-prod`) or a **single record** inside it.
- Whether that URL is a `Registry` or a `Record` (one of those two values).
- Which network(s) you want to join, including the `test-` variant if you want sandbox first (recommended — you must certify on test before prod; see [Conformance](conformance.md)).
- Role: `BAP`, `BPP`, or both.
- Service areas / countries (`IND` for India).
- A point of contact (name, email, phone).

Before approving, the Secretariat validates that your namespace is domain-verified, your callback URL is reachable, your signing public key is present and valid, and your declared role matches the network's expectations. Once the reference entry is written, your record is queryable as in-network by every counterparty — no separate bilateral handshake.

**Confirm the reference landed.** Re-run the same lookup from §1.6 and check the `network_memberships` array — it should now list the network(s) you were added to:

```bash
curl -s "https://fabric.nfh.global/registry/dedi/lookup/<your-subscriber-id>/subscribers.beckn.one/<your_record_id>" | jq '.data.network_memberships'
```

Expected: the parent network IDs appear, e.g. `["indiaenergystack.in/test-ies-data-sharing-network"]`. Empty or missing means the NFO hasn't written the reference yet (or wrote it against a different record) — this is exactly the value your ONIX checks against `allowedNetworkIDs` in [Setup Exchange §3.3](setup-exchange.md#id-3.3-swap-in-your-real-identity).

Membership in the test network does **not** imply membership in prod; each is referenced separately.

---

## 1.8 — *(NFOs)* Run your own Beckn network

**Prerequisite:** §1.1–1.4 complete for your own organisation.

If you operate a network rather than joining one, create a registry under your namespace with the built-in **`beckn_subscriber_reference`** tag — one registry per network you facilitate (typically separate `test-` and prod variants). The `network_id` becomes `<your-domain>/<registry-name>`. You curate membership by writing reference records that point at participant-owned subscriber records — you never copy participant data.

The NFO operational details (network manifest, policies, key rotation) are in the NFH docs: [setting up the network environment](https://docs.nfh.global/beckn/creating-an-open-network/setting-up-the-network-environment) and [configuring network policies](https://docs.nfh.global/beckn/creating-an-open-network/configuring-network-policies).

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| `curl` of `did.json` fails or redirects | File not at the exact path, or a `www.`/HTTPS redirect in front of it | The DID document URL must return the JSON directly, status 200, no redirect |
| DNS TXT verification stuck on "pending" for > 1 hour | Propagation delay (normal up to 48 h) or wrong record in zone | Check with `dig +short TXT <your-domain>`; ensure the record matches what DeDi issued |
| `404` on `GET /dedi/lookup/<namespace>/<registry>/<record-id>` | Wrong record-id (case-sensitive), or the record was never published (left as `draft`) | Verify in [publish.dedi.global](https://publish.dedi.global); re-publish with the correct id |
| `403 / signature invalid` on a DeDi write | Namespace controller key changed, or wrong API key | Confirm the API key belongs to the account controlling the namespace |
| Beckn counterparty cannot find your subscriber | Network reference not yet written (§1.7), or you're looking at the wrong environment | Verify the lookup URL the NFO wrote; check that `test-` vs prod matches the network you're targeting |

---

## Checklist

Everyone:

- [ ] Domain picked (typically a dedicated subdomain like `ies.<discom>.in`); `OPENCRED_ISSUER_DOMAIN` exported
- [ ] EC P-256 signing keypair generated, stored in KMS / HSM where available
- [ ] `did.json` generated and published at `https://<domain>/.well-known/did.json`
- [ ] `curl` of the DID document from outside returns your DID
- [ ] DeDi namespace claimed at `publish.dedi.global` and verified via DNS TXT (green **verified** label; listed on `explore.dedi.global`)
- [ ] DeDi API key created (avatar menu → **Manage API key**) and stored alongside your other secrets

Beckn participants additionally:

- [ ] Ed25519 keypair generated (`go run install/generate-ed25519-keys.go`); private key in secret manager
- [ ] `subscribers-test` / `subscribers-prod` registries created; subscriber record(s) published with public key, callback URL, role
- [ ] Fabric lookup URL returns your record
- [ ] IES Secretariat emailed; reference entry written into the network registry you applied for

When your role's boxes are ticked, you have completed **Setup Register**. Credential issuers: continue to **[Issue Credentials](issue-credentials.md)**. Beckn participants: continue to **[Setup Exchange](setup-exchange.md)**.

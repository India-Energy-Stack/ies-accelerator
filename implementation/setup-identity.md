# Step 1 — Set up Identity (Register)

The first IES step: get your organisation a verifiable digital identity, and list it in a shared directory. Done once. About 1–2 days of elapsed time (most of it waiting for DNS to propagate).

This page is the **action guide**. The deep specification is in **[Identifiers and Addressing](../identifiers/README.md)**. The registry mechanics are in **[Registries and Directories](../registries/README.md)**.

---

## What you'll have at the end

- A resolvable `did:web` for your organisation (e.g. `did:web:ies.apepdcl.in`).
- A signing keypair, securely stored (KMS / HSM where available).
- A verified DeDi namespace anchored to your domain.
- Optional: a separate Ed25519 keypair for Beckn message signing (you can defer this to [Step 2](setup-discovery.md)).

This is everything credential issuance requires. You do not need to be listed in any IES-side DISCOM registry to issue credentials — verifiers fetch your `did.json` directly to check signatures.

---

## 1.1 — Pick a domain (or subdomain) you control

Either works. Most DISCOMs use a dedicated subdomain so the credential-issuing identity is cleanly separated from the marketing site:

- `ies.apepdcl.in` (subdomain)
- `apepdcl.in` (apex domain — equally valid)

The host you pick becomes the host portion of your `did:web`. Your DID document will live at `https://<your-host>/.well-known/did.json`.

> **About path segments.** `did:web` lets you encode a sub-path with colons in the DID. If you don't want to host at `.well-known/`, host the document at any path and reflect it in the DID via colon hierarchy. Full table in **[Identifiers — DID web variants](../identifiers/README.md#publish-your-did-web)**.

---

## 1.2 — Generate a signing keypair

You will sign every credential and (optionally) every Beckn message with this key. Treat it as a production credential — KMS / HSM where possible, otherwise a securely backed-up file on a hardened host.

The credential-issuance key is **EC P-256** (matches W3C VC Data Model 2.0 defaults). The fastest way to generate it is to install [OpenCred](../glossary.md#opencred) and let it produce the key + the `did.json` together:

```bash
docker run -d \
  --name opencred \
  -p 8080:8080 \
  -e ISSUER_DID=did:web:ies.apepdcl.in \
  -e ISSUER_NAME="Eastern Power Distribution Company of Andhra Pradesh Ltd" \
  ghcr.io/nfh-trust-labs/opencred/opencred-server:latest
```

OpenCred prints the `did.json` it generated, which you then publish.

The end-to-end walkthrough — install OpenCred, generate the signing key, assemble `did.json`, publish, verify — lives in **[Energy Credentials — Set up OpenCred](../energy-credentials/README.md#set-up-opencred-and-publish-your-did-web)**. Any W3C-compliant signing pipeline (custom code, AWS KMS + jose, Azure Key Vault) is a drop-in replacement.

---

## 1.3 — Publish `did.json`

Put the generated `did.json` at the path implied by your DID:

| DID string | DID document URL |
|---|---|
| `did:web:ies.apepdcl.in` | `https://ies.apepdcl.in/.well-known/did.json` |
| `did:web:apepdcl.in:ies` | `https://apepdcl.in/ies/did.json` |

Verify it's reachable from outside your network:

```bash
curl -sS https://ies.apepdcl.in/.well-known/did.json | jq .
```

If you get back the expected JSON document with your public key, identity setup is done from the wire-protocol side. Verifiers can now check signatures on credentials you issue.

---

## 1.4 — Claim a DeDi namespace and verify your domain

DeDi is the public registry mechanism IES uses for namespaces, credential revocation, and Beckn subscriber membership. Claiming a namespace ties your organisation's records to your domain in a way anyone can verify.

1. **Sign up at [dedi.global](https://dedi.global)** using an organisational role mailbox (`registry-admin@apepdcl.in`).
2. **Create a namespace** — use a short name that maps to your organisation (`apepdcl`, `bescom`, `np.example.com`).
3. **Verify your domain** — DeDi issues a DNS TXT record; add it to your DNS zone and click *Verify*. Wait for DNS propagation (usually 15 minutes; can take up to 48 hours).

The full UI flow with screenshots is in the **[DeDi Quickstart](https://docs.nfh.global/dedi/dedi.global-developers/quickstart)**. The IES-specific framing is in **[Registries — Step-by-step: claim your DeDi namespace](../implementation/setup-identity.md)**.

> **If you ran OpenCred in 1.2**, four registries (`vc-revocation-registry`, `opencred-key-registry`, `schema_registry`, `context_registry`) are auto-created in your namespace on first boot. You do not need to create them by hand.

---

## 1.5 — Identifier patterns you'll use day one

Once your DID resolves and your DeDi namespace is verified, you have the identifier scheme below available. Internal numbering (CIS account numbers, meter SLNOs, SAP codes) is preserved as the tail of the DID — nothing renames.

| Subject | Identifier method | Example |
|---|---|---|
| Your DISCOM (issuer) | `did:web` on your domain | `did:web:ies.apepdcl.in` |
| A regulator | Same — `did:web` on their own domain | `did:web:ies.aperc.gov.in` |
| A consumer (holder) | `did:key` (wallet) — generated by the wallet, not the DISCOM | `did:key:z6MkjVQ8r4f3rPuY…` |
| A meter / inverter / DER / transformer | `did:web` under your domain | `did:web:ies.apepdcl.in:assets:meter:NM-44091234` |
| The consumer's existing CIS account number | Plain string, kept verbatim | `1102004567` → stays as `customerProfile.customerNumber` |

> Detailed grammar and worked examples: **[Identifiers and Addressing — Appendix C](../identifiers/README.md#appendix-c-identifying-assets-meters-connections-datasets)**.

---

## Checklist

- [ ] Domain picked (typically a dedicated subdomain like `ies.<discom>.in`)
- [ ] Signing keypair generated (EC P-256), stored in KMS / HSM where available
- [ ] `did.json` published at `https://<domain>/.well-known/did.json` and reachable from outside
- [ ] `curl` of the DID document returns expected JSON
- [ ] DeDi namespace claimed at `dedi.global` and verified via DNS TXT
- [ ] Internal numbering documented for the asset / connection / meter classes you'll reference

When all six are ticked, you have completed Step 1 of [Register → Discover → Exchange](../concepts/how-it-works.md). Move on to **[Step 2 — Set up Discovery](setup-discovery.md)**.

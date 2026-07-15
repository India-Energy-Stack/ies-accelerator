# Setup Register

> **Step 1 of the three IES steps — set up.** Get your organisation a verifiable digital identity, and list it in a shared directory. *Done once.* About 1–2 days of elapsed time (most of it waiting for DNS to propagate).

This is the **action guide** for the **[Register](../what-ies-provides/register.md)** step. The deep specification is in **[Identifiers and Addressing](../what-ies-provides/identifiers/README.md)**. The registry mechanics are in **[Registries and Directories](../what-ies-provides/registries/README.md)**.

---

## What you'll have at the end

- A resolvable `did:web` for your organisation (e.g. `did:web:ies.discom.example`).
- A signing keypair, securely stored (KMS / HSM where available).
- A verified DeDi namespace anchored to your domain.
- Optional: a separate Ed25519 keypair for Beckn message signing (you can defer this to [Step 2](setup-discovery.md)).

This is everything credential issuance requires. You do not need to be listed in any IES-side DISCOM registry to issue credentials — verifiers fetch your `did.json` directly to check signatures.

---

## 1.1 — Pick a domain (or subdomain) you control

Either works. Most DISCOMs use a dedicated subdomain so the credential-issuing identity is cleanly separated from the marketing site:

- `ies.discom.example` (subdomain)
- `discom.example` (apex domain — equally valid)

The host you pick becomes the host portion of your `did:web`. Your DID document will live at `https://<your-host>/.well-known/did.json`.

Once picked, record it in an environment variable — the copy-pasteable commands in this guide and in [Energy Credentials](../what-ies-provides/energy-credentials/README.md) all reference `$OPENCRED_ISSUER_DOMAIN`, so you set your domain once here and never hand-edit a command:

```bash
export OPENCRED_ISSUER_DOMAIN="ies.yourdiscom.in"
```

> **About path segments.** `did:web` lets you encode a sub-path with colons in the DID. If you don't want to host at `.well-known/`, host the document at any path and reflect it in the DID via colon hierarchy. Full table in **[Identifiers — DID web variants](../what-ies-provides/identifiers/README.md#publish-your-did-web)**.

---

## 1.2 — Generate a signing keypair

You will sign every credential and (optionally) every Beckn message with this key. Treat it as a production credential — KMS / HSM where possible, otherwise a securely backed-up file on a hardened host.

The credential-issuance key is **EC P-256** (matches W3C VC Data Model 2.0 defaults). The fastest way is to install [OpenCred](../glossary.md#opencred) and generate the key and `did.json` together — the copy-pasteable end-to-end walkthrough (pull the image, generate the key, run the container, generate `did.json`, publish, verify) lives in **[Energy Credentials — Set up OpenCred](../what-ies-provides/energy-credentials/README.md#set-up-opencred-and-publish-your-did-web)**. Any W3C-compliant signing pipeline (custom code, AWS KMS + jose, Azure Key Vault) is a drop-in replacement.

---

## 1.3 — Publish `did.json`

Put the generated `did.json` at the path implied by your DID:

| DID string | DID document URL |
|---|---|
| `did:web:ies.discom.example` | `https://ies.discom.example/.well-known/did.json` |
| `did:web:discom.example:ies` | `https://discom.example/ies/did.json` |

Verify it's reachable from outside your network (`$OPENCRED_ISSUER_DOMAIN` is the domain you exported in 1.1):

```bash
curl -sS "https://$OPENCRED_ISSUER_DOMAIN/.well-known/did.json" | jq .
```

If you get back the expected JSON document with your public key, identity setup is done from the wire-protocol side. Verifiers can now check signatures on credentials you issue.

---

## 1.4 — Claim a DeDi namespace and verify your domain

DeDi is the public registry mechanism IES uses for namespaces, credential revocation, and Beckn subscriber membership. Claiming a namespace ties your organisation's records to your domain in a way anyone can verify.

1. **Sign up at [publish.dedi.global](https://publish.dedi.global)** using an organisational role mailbox (`registry-admin@discom.example`).
2. **Create a namespace** — use a short name that maps to your organisation (`discom`, `np.example.com`).
3. **Verify your domain** — DeDi issues a DNS TXT record; add it to your zone and click *Verify* (15 min–48 hr for propagation). A green **verified** label then appears in [publish.dedi.global](https://publish.dedi.global), and the namespace becomes publicly listed on [explore.dedi.global](https://explore.dedi.global) — only verified namespaces appear there, so that listing is itself the public signal.
4. **Create an API key** — in the DeDi UI, click your avatar in the top-right corner, then **Manage API key**. OpenCred uses this key (as `OPENCRED_DEDI_API_KEY`) to write revocation entries and registries into your namespace.

The IES-specific framing is in **[Registries and Directories](../what-ies-provides/registries/README.md#setup)**; DeDi itself is documented at **[docs.nfh.global](https://docs.nfh.global/)**.

> **If you ran OpenCred with the `OPENCRED_DEDI_*` variables set** (see [Energy Credentials — step 3](../what-ies-provides/energy-credentials/README.md#id-3.-run-opencred-in-did-web-mode)), four registries (`vc-revocation-registry`, `opencred-key-registry`, `schema_registry`, `context_registry`) are auto-created in your namespace on first boot. You do not need to create them by hand — log in to [publish.dedi.global](https://publish.dedi.global), open your namespace, and confirm you can see all four.

---

## 1.5 — Identifier patterns you'll use day one

Once your DID resolves and your DeDi namespace is verified, you have the identifier scheme below available. Internal numbering (CIS account numbers, meter SLNOs, SAP codes) is preserved as the tail of the DID — nothing renames.

| Subject | Identifier method | Example |
|---|---|---|
| Your DISCOM (issuer) | `did:web` on your domain | `did:web:ies.discom.example` |
| A regulator | Same — `did:web` on their own domain | `did:web:ies.serc.example` |
| A consumer (holder) | `did:key` (wallet) — generated by the wallet, not the DISCOM | `did:key:z6MkjVQ8r4f3rPuY…` |
| A meter / inverter / DER / transformer | `did:web` under your domain | `did:web:ies.discom.example:assets:meter:NM-44091234` |
| The consumer's existing CIS account number | Plain string, kept verbatim | `1102004567` → stays as `customerProfile.customerNumber` |

> Detailed grammar and worked examples: **[Identifiers and Addressing — Appendix C](../what-ies-provides/identifiers/README.md#appendix-c-identifying-assets-meters-connections-datasets)**.

---

## Checklist

- [ ] Domain picked (typically a dedicated subdomain like `ies.<discom>.in`)
- [ ] Signing keypair generated (EC P-256), stored in KMS / HSM where available
- [ ] `did.json` published at `https://<domain>/.well-known/did.json` and reachable from outside
- [ ] `curl` of the DID document returns expected JSON
- [ ] DeDi namespace claimed at `publish.dedi.global` and verified via DNS TXT (green **verified** label in `publish.dedi.global`; namespace listed on `explore.dedi.global`)
- [ ] DeDi API key created (avatar menu → **Manage API key**) and stored alongside your other secrets
- [ ] Internal numbering documented for the asset / connection / meter classes you'll reference

When every box is ticked, you have completed the **Register** step. Move on to **[Setup Discovery](setup-discovery.md)**.

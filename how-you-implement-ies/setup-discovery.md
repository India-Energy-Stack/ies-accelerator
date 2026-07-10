# Setup Discovery

> **Step 2 of the three IES steps — set up.** Stand up the [Beckn](../glossary.md#beckn) adapter — the ready-made "ONIX" reference software — and register on the IES network. About 1–2 days.

Action guide for **[Discover](../what-ies-provides/discover.md)**. Full spec: **[Data Exchange](../what-ies-provides/data-exchange/README.md)**.

---

## What you'll have at the end

- A running ONIX container that speaks Beckn (search / select / init / confirm / status / on_*).
- An Ed25519 keypair for Beckn message signing.
- A Beckn subscriber record published in your DeDi namespace.
- A reference entry written by the IES network operator (REC / IES Secretariat) pointing at your subscriber record — your formal admission to the network.

That's everything Beckn-side discovery requires. You still need to **[Build your Internal-facing Adapter](build-adapter.md)** before you can return real data.

---

## 2.1 — Deploy ONIX

ONIX is the reference Beckn adapter — message signing, verification, DeDi lookup, network-membership checks, schema validation, callback routing. **You configure it; you do not build it.**

```bash
git clone https://github.com/beckn/DEG.git
cd DEG/devkits/data-exchange/install
docker compose up -d
```

This brings up three containers:

- `sandbox-bap` — a buyer / requester (e.g. a DISCOM consuming meter data)
- `sandbox-bpp` — a provider / publisher (e.g. an AMISP publishing meter telemetry)
- `beckn-router` — the local Beckn message router

Containers come pre-wired with placeholder identities for local testing; replace them with your own once you have a `did:web` and DeDi namespace from Step 1.

Detailed config flow: **[Data Exchange — Quick start](../what-ies-provides/data-exchange/README.md#quick-start-run-a-local-exchange-in-10-minutes)**.

---

## 2.2 — Generate the Beckn signing keypair

Beckn uses **Ed25519** message signing — a separate concern from the EC P-256 key from Step 1.2, with its own registry:

| Key | What it signs | Where it's published | Who verifies |
|---|---|---|---|
| **EC P-256** (Step 1) | Verifiable Credentials | `did.json` at `https://<your-domain>/.well-known/did.json` | Credential verifiers (banks, regulators, marketplaces) |
| **Ed25519** (this step) | Beckn messages | Your Beckn subscriber record in your DeDi namespace | Other Beckn nodes on the IES network |

Generate it per the **[NFH onboarding procedure — Publish your subscriber record](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants#step-4-publish-your-subscriber-record)**.

---

## 2.3 — Publish your Beckn subscriber record

In your verified DeDi namespace (Step 1.4), create a `beckn_subscriber` registry and write your record into it, declaring:

- Your subscriber id (`did:web` matching your organisation)
- Your callback URL (where Beckn responses should be delivered)
- Your role on the network (`BAP` — buyer; `BPP` — provider; both is also valid)
- Your Ed25519 signing public key

Other nodes look this record up to verify your signatures and route to you. Detailed flow: **[Identifiers — Appendix E: Joining a Beckn network](../what-ies-provides/identifiers/README.md#appendix-e-joining-a-beckn-network-subscriber-registry-on-the-beckn-fabric)**.

> **One registry per environment.** Create `subscribers-test` and `subscribers-prod` separately so a misconfigured test run can't pollute a production lookup.

---

## 2.4 — Get listed on the IES network

The IES network is operated by an NFO (Network Facilitator Organisation) — currently REC / IES Secretariat, under the `indiaenergystack.in` namespace.

1. Email `ies@recindia.com` with: your organisation name, your `did:web`, your DeDi namespace and the URL of your subscriber record.
2. The IES Secretariat verifies your details and writes a **reference entry** pointing at your subscriber record.
3. Your record is now part of the IES network membership boundary.

The reference is then queryable from any IES node — counterparties can verify network membership without a separate handshake.

---

## 2.5 — Test the end-to-end loop

Run a `search` from your BAP to a sandbox BPP (or a peer DISCOM's BPP). Verify:

- Your message signature is accepted (Ed25519 key resolves through DeDi)
- The BPP's response signature verifies (their key resolves through DeDi)
- Discovery returns a catalogue
- ONIX's network-membership check passes (both subscribers are referenced into the same IES network registry)

If all four pass, Step 2 is done.

Full Beckn lifecycle (`search` → `select` → `init` → `confirm` → `status`): **[Data Exchange — Beckn protocol lifecycle](../what-ies-provides/data-exchange/README.md#appendix-a-beckn-protocol-lifecycle)**.

---

## Checklist

- [ ] ONIX deployed (docker-compose) and accessible at your published callback URL
- [ ] Ed25519 keypair generated (separate from credential-issuance key)
- [ ] Beckn subscriber record published in your DeDi namespace with the Ed25519 public key, your callback URL and your BAP/BPP role
- [ ] IES Secretariat emailed; reference entry written into the IES network registry
- [ ] End-to-end `search` round-trip succeeds against the sandbox

All five ticked? You've completed **Discover**. Move on to **[Build your Internal-facing Adapter](build-adapter.md)**.

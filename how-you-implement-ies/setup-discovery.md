# Setup Discovery

> **Step 2 of the three IES steps — set up.** Stand up the [Beckn](../glossary.md#beckn) adapter — the ready-made Part 1 of the IES adapter (the "ONIX" reference software) — and register on the IES network. About 1–2 days.

This is the **action guide** for the **[Discover](../what-ies-provides/discover.md)** step. The full Discovery / Beckn specification is in **[Data Exchange](../what-ies-provides/data-exchange/README.md)**.

---

## What you'll have at the end

- A running ONIX container that speaks Beckn (search / select / init / confirm / status / on_*).
- An Ed25519 keypair for Beckn message signing.
- A Beckn subscriber record published in your DeDi namespace.
- A reference entry written by the IES network operator (REC / IES Secretariat) pointing at your subscriber record — your formal admission to the network.

This is everything Beckn-side discovery requires. After this you can issue and respond to discovery requests on the IES network. You still need to **[Build your Internal-facing Adapter](build-adapter.md)** before you can return real data from your internal systems.

---

## 2.1 — Deploy ONIX

ONIX is the reference Beckn adapter — message signing, signature verification, DeDi lookup, network-membership checks, schema validation, async callback routing. **You configure it; you do not build it.**

The fastest start is the IES sandbox docker-compose:

```bash
git clone https://github.com/beckn/DEG.git
cd DEG/devkits/data-exchange/install
docker compose up -d
```

This brings up three containers:

- `sandbox-bap` — a buyer / requester (e.g. a DISCOM consuming meter data)
- `sandbox-bpp` — a provider / publisher (e.g. an AMISP publishing meter telemetry)
- `beckn-router` — the local Beckn message router

The containers come pre-wired with placeholder identities so you can test the end-to-end flow on your laptop before plugging in your own.

Replace the placeholder identities with your own once Step 1 is done and you have a `did:web` plus a DeDi namespace.

The detailed config flow is in **[Data Exchange — Quick start](../what-ies-provides/data-exchange/README.md#quick-start-run-a-local-exchange-in-10-minutes)**.

---

## 2.2 — Generate the Beckn signing keypair

Beckn uses **Ed25519** message signing (different from the EC P-256 key you generated in Step 1.2 for credential issuance). They are separate concerns with separate registries:

| Key | What it signs | Where it's published | Who verifies |
|---|---|---|---|
| **EC P-256** (Step 1) | Verifiable Credentials | `did.json` at `https://<your-domain>/.well-known/did.json` | Credential verifiers (banks, regulators, marketplaces) |
| **Ed25519** (this step) | Beckn messages | Your Beckn subscriber record in your DeDi namespace | Other Beckn nodes on the IES network |

Generate it per the **[NFH onboarding procedure — Publish your subscriber record](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants#step-4-publish-your-subscriber-record)**.

---

## 2.3 — Publish your Beckn subscriber record

In your verified DeDi namespace (from Step 1.4), create a registry of type `beckn_subscriber` and write your subscriber record into it.

The record declares:

- Your subscriber id (`did:web` matching your organisation)
- Your callback URL (where Beckn responses should be delivered)
- Your role on the network (`BAP` — buyer; `BPP` — provider; both is also valid)
- Your Ed25519 signing public key

Other nodes look this record up to verify your message signatures and route to you. The detailed flow is in **[Identifiers — Appendix E: Joining a Beckn network](../what-ies-provides/identifiers/README.md#appendix-e-joining-a-beckn-network-subscriber-registry-on-the-beckn-fabric)**.

> **One registry per environment.** Create `subscribers-test` and `subscribers-prod` as separate registries so a misconfigured test run cannot pollute a production lookup.

---

## 2.4 — Get listed on the IES network

The IES network is operated by an NFO (Network Facilitator Organisation) — currently REC / IES Secretariat under the `indiaenergystack.in` namespace. To join, the NFO writes a **reference entry** in the IES network registry that points at your subscriber record. Counterparties then know your record is in-network.

The procedure:

1. Email `ies@recindia.com` with: your organisation name, your `did:web`, your DeDi namespace and the URL of your subscriber record.
2. The IES Secretariat verifies your details and writes the reference entry.
3. Your record is now part of the IES network membership boundary.

Once written, the reference is queryable from any IES node — your counterparties can verify you belong to the network without a separate handshake.

---

## 2.5 — Test the end-to-end loop

Run a `search` from your BAP to a sandbox BPP (or a peer DISCOM's BPP). Verify:

- Your message signature is accepted (Ed25519 key resolves through DeDi)
- The BPP's response signature verifies (their key resolves through DeDi)
- Discovery returns a catalogue
- ONIX's network-membership check passes (both subscribers are referenced into the same IES network registry)

If all four pass, Step 2 is done.

The full Beckn lifecycle (`search` → `select` → `init` → `confirm` → `status`) is documented in **[Data Exchange — Beckn protocol lifecycle](../what-ies-provides/data-exchange/README.md#appendix-a-beckn-protocol-lifecycle)**.

---

## Checklist

- [ ] ONIX deployed (docker-compose) and accessible at your published callback URL
- [ ] Ed25519 keypair generated (separate from credential-issuance key)
- [ ] Beckn subscriber record published in your DeDi namespace with the Ed25519 public key, your callback URL and your BAP/BPP role
- [ ] IES Secretariat emailed; reference entry written into the IES network registry
- [ ] End-to-end `search` round-trip succeeds against the sandbox

When all five are ticked, you have completed the **Discover** step. Move on to **[Build your Internal-facing Adapter](build-adapter.md)**.

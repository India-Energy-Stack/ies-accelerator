# Registry Setup

Going beyond the devkit sandbox is **an identity problem, not an infrastructure problem**. The stack itself doesn't change — what changes is the identity ONIX signs with, the registry that other participants resolve you against, and which networks your ONIX is configured to accept traffic from.

This page is the IES-specific entry point. The canonical step-by-step lives at [docs.nfh.global/beckn](https://docs.nfh.global/beckn); links below point straight to each section there so you don't have to navigate the tree.

---

## The IES networks

The Network Facilitator Organisation (NFO) for IES is anchored at the verified DeDi namespace `indiaenergystack.in`. Under it, IES operates two parallel networks:

| Network | `networkId` | Purpose |
|---|---|---|
| Test | `indiaenergystack.in/test-ies-data-sharing-network` | Pre-production exchange — used during onboarding, certification, and ongoing test/staging traffic after a participant goes live in prod. |
| Production | `indiaenergystack.in/ies-data-sharing-network` | Live exchange with real DISCOMs, regulators, AMISPs. |

Each network is its own DeDi registry under the `indiaenergystack.in` namespace. Membership in one does **not** imply membership in the other — every participant must be referenced from each network's registry separately. ONIX enforces this on every inbound message via its `allowedNetworkIDs` config.

---

## The model in one paragraph

A Beckn network is anchored by a **Network Facilitator Organisation (NFO)** that owns a verified namespace on DeDi Global and publishes a *network reference registry* under it. The network's identifier is `<nfo-domain>/<registry-name>`. Each **Network Participant (NP)** — your BAP or BPP — owns its own DeDi namespace and publishes its subscriber details (callback URL, Ed25519 signing public key) there. The NFO adds the **DeDi lookup URL of your subscriber record (or your whole subscriber registry)** to the network reference registry; that reference is what makes you "part of" the network. Identity stays self-owned; the NFO only curates membership.

---

## Step-by-step for a Network Participant (BAP / BPP)

You do four things, in order. Click through to the upstream docs for the exact UI clicks and edge cases.

### 1. Create a DeDi Global account and verify your namespace

Pick a domain you control (e.g. `example-np.com`). DeDi gives you a DNS TXT record; add it to your domain's DNS; DeDi verifies and your namespace becomes a root of trust.

> **Can't get DNS verification through?** Contact the IES Secretariat (see step 4) — a temporary workaround is available while your domain verification is sorted out.

→ [docs.nfh.global/beckn — Step 2: Create & verify your namespace](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants)

### 2. Create a subscriber registry under your namespace

Use the **Beckn subscriber schema** when creating the registry. This is the registry that will hold your subscriber record(s). One registry per environment is the common pattern — a `test` registry and a `prod` registry under the same namespace — so the records are kept clearly separated. (You can also use a single registry with multiple records; see [Two registries, two ONIX deployments](#two-registries-two-onix-deployments) below for why the split is convenient.)

→ [docs.nfh.global/beckn — Step 3: Add a registry under your namespace](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants)

### 3. Publish your subscriber record

Fill the standard fields:

| Field | What to fill |
|---|---|
| `subscriber_id` | Your unique identifier — typically your domain (`np.example.com`) |
| `subscriber_url` | Your ONIX receiver endpoint (`https://np.example.com/bap/beckn`) |
| `type` | `BAP` or `BPP`. If you do both, publish two records. |
| Signing public key | Base64-encoded Ed25519 public key (no PEM header/footer) |

Generate the keypair using the helper script in [beckn-onix](https://github.com/beckn/beckn-onix) (or any Ed25519 tool — raw 32-byte seed + 32-byte public key, both Base64 RFC 4648 with padding).

After publishing, **note the `recordId`** that DeDi assigns. It is your `keyId` in ONIX. Also copy the **DeDi lookup URL** for the record (or the whole subscriber registry) — you'll send it to IES in step 4. Records can take **~5 minutes to propagate** — verify your lookup URL resolves via the registry service before sending it onward.

→ [docs.nfh.global/beckn — Step 4: Publish your subscriber record](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants)

### 4. Ask IES to add your DeDi URL to the network reference registry

For the IES test network (`indiaenergystack.in/test-ies-data-sharing-network`), the NFO is the **IES Secretariat**. Send them the **DeDi lookup URL** of either your individual subscriber record or your whole subscriber registry, plus the `type` (Registry vs Record — see upstream docs):

- **Record URL** if you want only that one identity referenced into the network.
- **Registry URL** if you want every current and future subscriber record under that registry of yours treated as part of the network.

**Contact (IES NFO / IES Secretariat):**

| Channel | Address |
|---|---|
| Email (primary) | [IES.Secretariat@fsrglobal.org](mailto:IES.Secretariat@fsrglobal.org) |
| Email (alternate) | [ies@recindia.com](mailto:ies@recindia.com) |
| Web | [ies.fsrglobal.org](https://ies.fsrglobal.org/#footer) |

IES then adds that URL as a reference entry into the **network reference registry**. Once that reference exists, other participants — and the ONIX adapters they're using — can resolve your subscriber details and verify your signatures. Until it exists, ONIX on the other side will reject your messages with a registry-lookup failure (look for `subscriber not found` or signature verification errors in `docker logs onix-bpp` / `onix-bap`).

Repeat the same handoff against `indiaenergystack.in/ies-data-sharing-network` when you're ready to go production-live (see lifecycle below).

→ [docs.nfh.global/beckn — Adding Registry entries (NFO side)](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants)

---

## Configure ONIX with your real identity

Edit your devkit's adapter configs ([config/local-simple-bap.yaml](https://github.com/beckn/DEG/blob/main/devkits/data-exchange/config/local-simple-bap.yaml) and `local-simple-bpp.yaml`) to point at your DeDi-published identity. The knobs live under `modules[].handler.plugins`:

| DeDi value | ONIX YAML path |
|---|---|
| Your `subscriberId` | `plugins.keyManager.config.networkParticipant` |
| Your `recordId` | `plugins.keyManager.config.keyId` |
| Your Ed25519 private key | `plugins.keyManager.config.signingPrivateKey` *(Base64 RFC 4648, 32-byte seed)* |
| Your Ed25519 public key | `plugins.keyManager.config.signingPublicKey` *(matches what you published in DeDi)* |
| Network you're joining | `plugins.registry.config.allowedNetworkIDs` *(comma-separated string; see next section)* |

The public key never leaves DeDi; the private key never leaves your ONIX deployment.

### `allowedNetworkIDs` is the gate

Every inbound Beckn message carries a `context.networkId`. ONIX rejects any message whose `networkId` is not listed in its `allowedNetworkIDs` config; the field is a **comma-separated string** (not a YAML list). A test-only ONIX:

```yaml
modules:
  - handler:
      plugins:
        registry:
          config:
            allowedNetworkIDs: "indiaenergystack.in/test-ies-data-sharing-network"
```

A production-only ONIX:

```yaml
            allowedNetworkIDs: "indiaenergystack.in/ies-data-sharing-network"
```

To run one ONIX against both networks (uncommon, generally not recommended), include both, comma-separated:

```yaml
            allowedNetworkIDs: "indiaenergystack.in/test-ies-data-sharing-network,indiaenergystack.in/ies-data-sharing-network"
```

The split is preferred operationally — see the next section.

---

## Two registries, two ONIX deployments

A common rollout pattern that the IES networks support cleanly:

1. **Run two ONIX deployments — test and prod — on separate hostnames** (e.g. `test.example-np.com` and `beckn.example-np.com`). Each has its own TLS cert, its own keypair, its own DeDi subscriber record under your namespace. The two subscriber records live under separate subscriber registries (e.g. `example-np.com/test-subscriber` and `example-np.com/prod-subscriber`) so they cannot be confused.

2. **`allowedNetworkIDs` is set narrowly on each side.** The test ONIX accepts only `indiaenergystack.in/test-ies-data-sharing-network`. The prod ONIX accepts only `indiaenergystack.in/ies-data-sharing-network`. Cross-network traffic is rejected at the adapter — no risk of a stray test message reaching a production counterparty, or vice versa.

3. **Phased onboarding:**
   - **Phase 1 — Test.** IES references your *test* subscriber DeDi URL into the test network reference registry. You complete certification flows, run end-to-end exchanges, fix issues. The prod ONIX may already be deployed but is not yet referenced from the prod network, so no real counterparty can reach it.
   - **Phase 2 — Prod cutover.** Once testing is finished, IES adds your *prod* subscriber DeDi URL to `indiaenergystack.in/ies-data-sharing-network`. From that moment your prod ONIX is officially allowed to transact with production NPs.
   - **Steady state.** Both deployments keep running. Test stays useful for staging upgrades, regression testing, certifying new use cases — without any chance of polluting prod identity or prod data.

### Running two devkit stacks side-by-side

The devkit ships a single `install/docker-compose.yml`. To run two stacks (test and prod) on the same host:

- Bind the second stack on different host ports — copy `install/` to e.g. `install-prod/`, edit the published ports (`8081→8181`, `8082→8182`, `9000→9100`) and adjust the `Caddyfile` listener accordingly.
- Use a separate compose project name per stack so docker keeps them isolated:
  ```bash
  docker compose -p ies-test  -f install/docker-compose.yml      up -d
  docker compose -p ies-prod  -f install-prod/docker-compose.yml up -d
  ```
- In production deployments these two stacks would typically run on separate hosts (or at least separate VMs) with their own TLS termination and DNS hostnames — see the [Hosting checklist](#hosting-checklist) below.

For deeper multi-network setups (one ONIX serving several networks, per-region splits, etc.), see the [devkit README — Hosting the site](https://github.com/beckn/DEG/blob/main/devkits/README.md#hosting-the-site-beyond-the-devkit).

---

## Hosting checklist

In production you also need TLS in front of `beckn-router:9000`. The three common patterns (host-level reverse proxy, in-stack Caddy doing TLS, managed edge) are documented in the [devkit README — Hosting the site](https://github.com/beckn/DEG/blob/main/devkits/README.md#hosting-the-site-beyond-the-devkit).

The address you publish in `subscriber_url` (step 3) must be the TLS-terminated public URL.

---

## Reference

- [docs.nfh.global/beckn — Setting up the network environment](https://docs.nfh.global/beckn/creating-an-open-network/setting-up-the-network-environment) *(NFO side — for completeness)*
- [docs.nfh.global/beckn — Onboarding Network Participants](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants)
- [DeDi Global](https://dedi.global) — the registry SaaS
- [beckn-onix](https://github.com/beckn/beckn-onix) — Ed25519 keygen utility + signing/verification config + `allowedNetworkIDs` enforcement
- [Devkit README — Hosting the site](https://github.com/beckn/DEG/blob/main/devkits/README.md#hosting-the-site-beyond-the-devkit)

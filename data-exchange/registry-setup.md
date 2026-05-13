# Registry Setup

Going beyond the devkit sandbox is **an identity problem, not an infrastructure problem**. The stack itself doesn't change — what changes is the identity ONIX signs with and the registry that other participants resolve you against.

This page is the IES-specific entry point. The canonical step-by-step lives at [docs.nfh.global/beckn](https://docs.nfh.global/beckn); links below point straight to each section there so you don't have to navigate the tree.

---

## The model in one paragraph

A Beckn network is anchored by a **Network Facilitator Organisation (NFO)** that owns a verified namespace on DeDi Global and publishes a *network registry* under it. The network's identifier is `<nfo-domain>/<registry-name>` — for IES, that is `nfh.global/testnet-deg`. Each **Network Participant (NP)** — your BAP or BPP — owns its own DeDi namespace and publishes its subscriber details (callback URL, Ed25519 signing public key) there. The NFO adds a reference to your record into the network registry; that reference is what makes you "part of" the network. Identity stays self-owned; the NFO only curates membership.

---

## Step-by-step for a Network Participant (BAP / BPP)

You do four things, in order. Click through to the upstream docs for the exact UI clicks and edge cases.

### 1. Create a DeDi Global account and verify your namespace

Pick a domain you control (e.g. `example-np.com`). DeDi gives you a DNS TXT record; add it to your domain's DNS; DeDi verifies and your namespace becomes a root of trust.

→ [docs.nfh.global/beckn — Step 2: Create & verify your namespace](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants)

### 2. Create a registry under your namespace

Use the **Beckn subscriber schema** when creating the registry. This is the registry that will hold your subscriber records.

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

After publishing, **note the `recordId`** that DeDi assigns. It is your `keyId` in ONIX.

→ [docs.nfh.global/beckn — Step 4: Publish your subscriber record](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants)

### 4. Ask the network owner to add you

For the IES network (`nfh.global/testnet-deg`), the namespace owner is `nfh.global`. Share your DeDi record/registry lookup URL with them; they add a reference entry into the IES network registry. Once that's done, you are discoverable and resolvable on the network.

→ [docs.nfh.global/beckn — Adding Registry entries (NFO side)](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants)

---

## Configure ONIX with your real identity

Edit your devkit's adapter configs ([config/local-simple-bap.yaml](https://github.com/beckn/DEG/blob/main/devkits/data-exchange/config/local-simple-bap.yaml) and `local-simple-bpp.yaml`) to point at your DeDi-published identity. The mapping:

| DeDi registry field | ONIX config field |
|---|---|
| `recordId` | `keyId` |
| `subscriberId` | `networkParticipant` |
| `domain` (the network's `networkId`) | entry in `allowedNetworkIDs` |

You also drop your Ed25519 **private** key into the ONIX signing config — same keypair whose public half you published in step 3. The public key never leaves DeDi; the private key never leaves your ONIX deployment.

> **Multi-network ONIX.** One ONIX deployment can transact on several networks. List each `networkId` in `allowedNetworkIDs` and publish a corresponding DeDi subscriber record per network. See the [devkit README — Hosting the site](https://github.com/beckn/DEG/blob/main/devkits/README.md#hosting-the-site-beyond-the-devkit) for the full pattern including TLS.

---

## Hosting checklist

In production you also need TLS in front of `beckn-router:9000`. Three common patterns, all documented in the [devkit README](https://github.com/beckn/DEG/blob/main/devkits/README.md#hosting-the-site-beyond-the-devkit):

- **Host-level reverse proxy** — nginx / Caddy / Traefik on your VM, Let's Encrypt cert, `proxy_pass → 127.0.0.1:9000`.
- **Let the in-stack Caddy do TLS** — edit `install/Caddyfile`, drop `auto_https off`, mount `/data` for cert persistence, expose `:80`/`:443`.
- **Managed edge** — Cloudflare / ALB / GCP LB / Cloudflare Tunnel, origin at `<your-host>:9000`. No stack changes.

The address you publish in `subscriber_url` (step 3) is the TLS-terminated public URL.

---

## Reference

- [docs.nfh.global/beckn — Setting up the network environment](https://docs.nfh.global/beckn/creating-an-open-network/setting-up-the-network-environment) *(NFO side — for completeness)*
- [docs.nfh.global/beckn — Onboarding Network Participants](https://docs.nfh.global/beckn/creating-an-open-network/onboarding-network-participants)
- [DeDi Global](https://dedi.global) — the registry SaaS
- [beckn-onix](https://github.com/beckn/beckn-onix) — Ed25519 keygen utility + signing/verification config
- [Devkit README — Hosting the site](https://github.com/beckn/DEG/blob/main/devkits/README.md#hosting-the-site-beyond-the-devkit)

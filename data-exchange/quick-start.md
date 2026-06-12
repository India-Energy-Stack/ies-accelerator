# Quick Start — Data Exchange

Run a working data exchange against the devkit's local sandbox in under 10 minutes — no real registry, no production credentials. Track your overall progress with the [Onboarding Checklist](../checklists/data-exchange-checklist.md); registry/production steps live on [Registry Setup](./registry-setup.md).

---

## 1. Pick your role

| You are | You run | What you do |
|---|---|---|
| **BAP** — data consumer (DISCOM, regulator, VAS provider, researcher) | BAP-side adapter + your application | Send `confirm` (and optional discovery/negotiation), receive `on_confirm` / `on_status` callbacks |
| **BPP** — data provider (AMISP, DISCOM, SERC, data custodian) | BPP-side adapter + your provider implementation | Receive `confirm`, emit `on_confirm` (and `on_status` for async delivery) with the dataset |
| Both | Both stacks | Both flows in parallel |

The walkthrough uses the **BAP** path by default; BPP implementors, see the [BPP path](#bpp-path) in §4. The minimal flow — `confirm` → `on_confirm` — is all you need to start; the full action picker is in [Concepts § Beckn Protocol Lifecycle](./concepts.md#beckn-protocol-lifecycle).

---

## 2. Prerequisites

- Docker and Docker Compose, Git, Postman *(or `curl`)*, ~2 GB free disk space

The devkit ships pre-configured sandbox identities (`bap.example.com` / `bpp.example.com`) — no real credentials needed.

---

## 3. Clone and start the stack

```bash
git clone https://github.com/beckn/DEG.git
cd DEG/devkits/data-exchange/install
docker compose up -d
```

Verify the services are up:

```bash
$ docker compose ps
# all 7 containers should show "running" (and the redis/sandbox ones "healthy")

$ curl -s http://localhost:8081/health   # onix-bap
{"status":"ok"}
$ curl -s http://localhost:8082/health   # onix-bpp
{"status":"ok"}
$ curl -s http://localhost:9000/         # beckn-router default route
beckn-router ok
```

> **If checks fail** — give ONIX ~15s after `docker compose up` to initialise, then re-curl. Persistent `connection refused` usually means a container isn't running; `docker compose logs onix-bap` / `onix-bpp` show why.

---

## 4. Run the minimal exchange (`confirm` → `on_confirm`)

One round-trip proves all the wiring: signing, routing, verification, callback delivery.

**Import the Postman collection** — each use case ships BAP and BPP collections; import the **BAP** one for your use case:

```
devkits/data-exchange/uc1-meter-data/postman/data-exchange-uc1-meter-data.{BAP,BPP}-DEG.postman_collection.json
devkits/data-exchange/uc2-regulatory-data/postman/data-exchange-uc2-regulatory-data.{BAP,BPP}-DEG.postman_collection.json
devkits/data-exchange/uc3-tariff-policy/postman/data-exchange-uc3-tariff-policy.{BAP,BPP}-DEG.postman_collection.json
```

**Check the collection variables** — the defaults are correct for local runs; don't change them:

| Variable | Default | What it is |
|---|---|---|
| `beckn_adapter_url` | `http://localhost:8081/bap/caller` | The HTTP target Postman POSTs to |
| `bap_host_root` / `bpp_host_root` | `http://beckn-router:9000` | Substituted into each payload's `context.bapUri`/`bppUri`; resolved by ONIX *inside* docker (change only for ngrok/deployed routing — see §6) |

The layering behind these two kinds of URL is explained in [Appendix § Hostnames and endpoints](./appendix.md#hostnames-and-endpoints--sandbox-vs-production).

**Send and verify:**

1. Open the `confirm` request, click **Send**. The synchronous response is the ACK envelope: `{"message":{"ack":{"status":"ACK"}}}` — "accepted, async callback pending."
2. Tail the BAP sandbox logs to see the matching callback land:
   ```bash
   docker logs sandbox-bap 2>&1 | grep on_confirm | tail -5
   ```
3. The `on_confirm` body either carries the dataset (`INLINE`) or a handle pointing to a later `on_status`. Either way, seeing `on_confirm` in `sandbox-bap` is your end-to-end signal.

> **If you don't see `on_confirm`** — most common causes: (a) `bap_host_root`/`bpp_host_root` changed away from `http://beckn-router:9000`, (b) ONIX rejected the message on schema/signature — check `docker logs onix-bap | grep -i error` and `onix-bpp`, or (c) host alias DNS missing on `beckn-router` (only if you regenerated `install/docker-compose.yml` — see beckn/DEG#319).

### BPP path

Same sanity check in reverse: import the **BPP** collection, trigger `on_confirm` from it (or wait for an inbound `confirm`), and tail:

```bash
docker logs sandbox-bpp 2>&1 | grep -E 'confirm|status' | tail -5
```

Then replace `sandbox-bpp` with your own provider — see [§7](#7-wire-in-your-application).

---

## 5. (Optional) Add other Beckn actions

Each action ships in the BAP or BPP collection — fire it only when your use case needs it:

| Action | Sent by | Use it when |
|---|---|---|
| `publish-catalog` | BPP collection | You're a provider listing datasets so consumers can discover you |
| `discover` | BAP collection | The consumer doesn't yet know which BPP holds the dataset |
| `select` / `init` | BAP collection | Terms (price, SLA, delivery mode) need agreeing before commitment |
| `status` | BAP collection | The payload is prepared *after* `on_confirm`; the BAP polls for it (all three use cases use this) |
| `update` | BAP collection | Post-fulfilment changes — credential rotation in streaming |

Each [use-case page](../use-cases/README.md) lists exactly which steps it exercises and where the example payloads live.

---

## 6. Test over the public internet (ngrok)

Once §4 is green locally, you can prove the same stack interoperates over a real public tunnel — with another participant's laptop or a cloud host — without DeDi identity yet:

1. Create a free [ngrok](https://ngrok.com) account; copy the devkit's tunnel config and add your authtoken:
   ```bash
   cd DEG/devkits/data-exchange/install
   cp ngrok.yml.example ngrok.yml   # edit: paste your authtoken
   ngrok start --all --config ngrok.yml
   ```
2. In Postman, set `bap_host_root` / `bpp_host_root` to the HTTPS URL ngrok prints (e.g. `https://abc123.ngrok-free.dev`) — the docker-only dummy hostnames aren't reachable from outside, so the payload URIs must carry your public tunnel URL instead. Leave `beckn_adapter_url` alone — Postman still POSTs to your local ONIX.
3. Fire `confirm` again; watch the hops in the ngrok inspector at [http://localhost:4040](http://localhost:4040).

For two-party interop, each side runs its own tunnel and you point `bpp_host_root` at the *other side's* URL. Details and the full recipe: [devkit README — Over-the-internet notes](https://github.com/beckn/DEG/blob/main/devkits/README.md#over-the-internet-notes). Revert the host variables to `http://beckn-router:9000` to return to local-only mode.

---

## 7. Wire in your application

Sections 3–6 prove the wiring against the bundled sandbox containers. Your app connects to ONIX in exactly two places — and `bapUri`/`bppUri` are *not* one of them (those always point at ONIX receivers, never at your app):

- **Inbound** — after verifying a message, ONIX forwards it to the **webhook URL set in the routing config** ([`config/local-simple-routing-BAPReceiver.yaml`](https://github.com/beckn/DEG/blob/main/devkits/data-exchange/config/local-simple-routing-BAPReceiver.yaml) / `…-BPPReceiver.yaml`). The sandboxes are wired in this way; your app replaces them by taking over that URL.
- **Outbound** — your app POSTs messages to ONIX's `caller` endpoint.

**BAP — receive callbacks in your own app.** Stand up a service with a webhook endpoint for the `on_*` callbacks your flow needs, reachable from `onix-bap` (on the `bap_side` docker network, or a routable host). Change `target.url` in `local-simple-routing-BAPReceiver.yaml` from `http://sandbox-bap:3001/api/bap-webhook` to your service, restart `onix-bap`, then stop `sandbox-bap`.

**BPP — serve real data.** Your provider receives requests (`confirm`, `status`, …) on the webhook set in `local-simple-routing-BPPReceiver.yaml` (devkit default: `http://sandbox-bpp:3002/api/webhook`). Acknowledge each with HTTP 200, then respond asynchronously by POSTing the matching callback to `http://onix-bpp:8082/bpp/caller/on_<action>` — copy the wire shape from `uc*/examples/on-*-response*.json` and swap in your real data. Point the routing config at your service, run it on the `bpp_side` network, stop `sandbox-bpp`. The `sandbox-bpp` source is a working minimal provider you can fork.

---

## 8. Stop the stack

```bash
cd DEG/devkits/data-exchange/install && docker compose down
```

---

## 9. Going beyond the sandbox

Onboarding is a two-phase progression — don't skip phase 1.

### Phase 1 — Use the devkit as-is and prove the flows

Sections 1–7 above are the whole of phase 1: shipped sandbox identities, placeholder `networkId`, sandbox signing keys. The goal is to confirm the wiring, your application's handling of the `dataPayload` shape, and (for BPPs) your provider's wire format — without involving DeDi or any real IES network.

### Phase 2 — Swap in your real identity

Only once phase 1 is solid, replace the sandbox identity with yours in [`config/local-simple-bap.yaml`](https://github.com/beckn/DEG/blob/main/devkits/data-exchange/config/local-simple-bap.yaml) (and the matching `local-simple-bpp.yaml`):

```yaml
modules:
  - name: bapTxnReceiver
    handler:
      plugins:
        registry:
          config:
            allowedNetworkIDs: "indiaenergystack.in/test-ies-data-sharing-network"   # comma-separated string
        keyManager:
          config:
            networkParticipant: your.subscriber.id        # your DeDi subscriberId
            keyId: <recordId-from-DeDi>                   # the recordId DeDi gave you
            signingPrivateKey: <base64-ed25519-private>   # the half you keep
            signingPublicKey:  <base64-ed25519-public>    # the half you published in DeDi
```

Where these values come from — DeDi namespace, subscriber record, IES NFO handoff, and the full field mapping — is the subject of [Registry Setup](./registry-setup.md). Stay on the **test network** until certified; the recommended prod pattern is [two separate ONIX deployments](./registry-setup.md#two-registries-two-onix-deployments).

After the config swap, re-import the same Postman collection — only the identity ONIX signs with and the network it claims change. A successful `confirm` against another participant on `indiaenergystack.in/test-ies-data-sharing-network` proves end-to-end onboarding.

---

## Reference

- [Onboarding Checklist](../checklists/data-exchange-checklist.md) — staged checklist from devkit to production
- [Core Concepts](./concepts.md) · [Appendix](./appendix.md)
- [Devkit README](https://github.com/beckn/DEG/blob/main/devkits/README.md) — multi-network ONIX, hosting/TLS, ngrok
- [Beckn protocol v2.0.0 spec](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0)

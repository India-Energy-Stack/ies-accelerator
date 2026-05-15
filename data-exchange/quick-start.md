# Quick Start — Data Exchange

Run a working data exchange against the devkit's local sandbox in under 10 minutes — no real registry, no production credentials. This page also doubles as the onboarding checklist; the registry/production steps live on [Registry Setup](./registry-setup.md).

---

## 1. Pick your role

| You are | You run | What you do |
|---|---|---|
| **BAP** — data consumer (DISCOM, regulator, VAS provider, researcher) | BAP-side adapter + your application | Send `confirm` (and optional discovery/negotiation), receive `on_confirm` / `on_status` callbacks |
| **BPP** — data provider (AMISP, DISCOM, SERC, data custodian) | BPP-side adapter + your provider implementation | Receive `confirm`, emit `on_confirm` (and `on_status` for async delivery) with the dataset |
| Both | Both stacks | Both flows in parallel |

The walkthrough below uses the **BAP** path by default — send `confirm` from Postman, see `on_confirm` arrive at the sandbox-bap webhook. If you're a BPP implementor, see [§ 4 BPP path](#bpp-path) inside section 4.

Which Beckn actions you need depends on your case; the picker lives in [Concepts § Beckn Protocol Lifecycle](./concepts.md#beckn-protocol-lifecycle). The minimal flow — `confirm` → `on_confirm` — is what sections 2–6 below set you up to run.

---

## 2. Prerequisites

- Docker and Docker Compose
- Postman *(or `curl`)*
- Git
- ~2 GB free disk space for images

For local sandbox use, the devkit ships pre-configured identities (`bap.example.com` / `bpp.example.com`) — no real credentials needed. For real-network use, see [Registry Setup](./registry-setup.md).

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

The stack lays out as in [Architecture](./architecture.md): `beckn-router:9000` is the bridge; each side runs `onix-{bap,bpp}` + `sandbox-{bap,bpp}` + redis.

> **If checks fail** — give ONIX ~15s after `docker compose up` to initialise, then re-curl. Persistent `connection refused` usually means a container isn't running; `docker compose logs onix-bap` and `docker compose logs onix-bpp` show why.

---

## 4. Run the minimal exchange (`confirm` → `on_confirm`)

The minimal sanity check is one Beckn round-trip. The BAP POSTs `confirm`, ONIX-BAP signs and routes it to ONIX-BPP, which verifies the signature against the registered public key and delivers it to the BPP server. The BPP then calls `on_confirm` back through ONIX, signed at its end and verified at the BAP's end. A successful round-trip proves all of that wiring in one shot.

### Import the Postman collection

Each use case ships BAP and BPP collections:

```
devkits/data-exchange/uc1-meter-data/postman/data-exchange-uc1-meter-data.{BAP,BPP}-DEG.postman_collection.json
devkits/data-exchange/uc2-regulatory-data/postman/data-exchange-uc2-regulatory-data.{BAP,BPP}-DEG.postman_collection.json
devkits/data-exchange/uc3-tariff-policy/postman/data-exchange-uc3-tariff-policy.{BAP,BPP}-DEG.postman_collection.json
```

Import the **BAP** collection for the use case you care about.

### Set collection variables

Two things are happening at different layers:

1. **The HTTP target Postman connects to** is the ONIX BAP adapter — `http://localhost:8081/bap/caller` — already pre-set in the collection's `beckn_adapter_url` variable. You don't change that for local sandbox runs.
2. **The `bap_host_root` / `bpp_host_root` variables** are substituted into each payload's `context.bapUri` / `context.bppUri`. Those values get read by ONIX inside docker when it routes the callback back to the other side. The collection ships with the right defaults:

| Variable | Default (substituted into the payload) | When to change |
|---|---|---|
| `bap_host_root` | `http://beckn-router:9000` | If routing over an ngrok tunnel or a deployed public router, set to that hostname instead. |
| `bpp_host_root` | `http://beckn-router:9000` | Same as above. |

`beckn-router` is a docker-network hostname — ONIX inside docker resolves it; your Postman client never connects to it directly. See the [devkit README — Over-the-internet notes](https://github.com/beckn/DEG/blob/main/devkits/README.md#over-the-internet-notes) for the ngrok recipe.

### Send `confirm` and verify (BAP path)

1. In Postman, open the BAP collection's `confirm` request and click **Send**. The synchronous response is the ACK envelope from ONIX-BAP:
   ```json
   {"message":{"ack":{"status":"ACK"}}}
   ```
   (Some adapters reduce this to just `{"status":"ACK"}`. Either form means "accepted, async callback pending.")
2. Tail the BAP sandbox logs to see the matching callback land:
   ```bash
   docker logs sandbox-bap 2>&1 | grep on_confirm | tail -5
   ```
3. The `on_confirm` body either carries the dataset directly (`INLINE` delivery for the minimal flow) or holds a delivery handle that points to a later `on_status`. Either way, seeing `on_confirm` in `sandbox-bap` is your end-to-end signal.

> **If you don't see `on_confirm`** — the most common causes are (a) `bap_host_root` / `bpp_host_root` got changed to `localhost:9000` (they should stay at `http://beckn-router:9000` so ONIX-BPP can route the callback back — see above), (b) ONIX rejected the message on schema/signature; check `docker logs onix-bap | grep -i error` and `docker logs onix-bpp | grep -i error`, or (c) the host alias DNS isn't set on `beckn-router` (only relevant if you regenerated `install/docker-compose.yml` — see beckn/DEG#319).

### BPP path

If your role is BPP (data provider), the same sanity check runs in reverse:

1. Import the **BPP** collection for your use case.
2. Trigger `on_confirm` from the BPP collection (or wait for an inbound `confirm` from a BAP). The synchronous response is the same ACK envelope.
3. Tail `sandbox-bpp` for the inbound `confirm` and `sandbox-bap` for your outbound `on_confirm`:
   ```bash
   docker logs sandbox-bpp 2>&1 | grep -E 'confirm|status' | tail -5
   ```

The next step for BPP implementors is replacing `sandbox-bpp` with your own provider — see [Wire in your application](#wire-in-your-application) below.

---

## 5. (Optional) Add other Beckn actions

Beyond the minimal `confirm` round-trip, each Beckn action ships in either the BAP or the BPP collection — fire it from the right side only when your use case needs it:

| Action | Sent by | Use it when |
|---|---|---|
| `publish-catalog` | BPP collection | You're a provider listing datasets so consumers can discover you |
| `discover` | BAP collection | The consumer doesn't yet know which BPP holds the dataset |
| `select` / `init` | BAP collection | Terms (price, SLA, delivery mode) need to be agreed before commitment |
| `status` | BAP collection | The payload is prepared *after* `on_confirm`; the BAP polls for it (UC1, UC2, UC3 all use this) |
| `update` | BAP collection | Post-fulfilment changes — most relevant for credential rotation in streaming |

The corresponding `on_*` callbacks come back into your sandbox webhook (BAP gets `on_*` callbacks at `sandbox-bap`, BPP gets inbound requests at `sandbox-bpp`).

Each use case page lists exactly which steps it exercises and where the example payloads live:

- [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) — `confirm` + `on_status`
- [DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing.md) — `confirm` + `on_status`
- [Tariff Intelligence](../use-cases/tariff-intelligence.md) — `confirm` + `on_status`

---

## 6. Test over the public internet (ngrok)

Once §4 is green against the local sandbox, the next sanity check is verifying that your stack can transact through a real public tunnel — the same network path you'd use in production. This proves your laptop-hosted Beckn node can interoperate with **any other node hosted elsewhere** (another participant's laptop fronted by their own ngrok, or a cloud-hosted server), without needing real DeDi identity yet.

The devkit ships [`install/ngrok.yml.example`](https://github.com/beckn/DEG/blob/main/devkits/data-exchange/install/ngrok.yml.example) that configures one HTTP tunnel to `beckn-router:9000`.

### One-time setup

1. Create a free [ngrok](https://ngrok.com) account and copy your authtoken from the dashboard.
2. Copy the example config and paste in your authtoken:
   ```bash
   cd DEG/devkits/data-exchange/install
   cp ngrok.yml.example ngrok.yml
   # edit ngrok.yml: replace REPLACE_WITH_YOUR_NGROK_AUTHTOKEN with the value from your dashboard
   ```

### Start the tunnel

With the docker stack already running (§3), start ngrok in another terminal:

```bash
cd DEG/devkits/data-exchange/install
ngrok start --all --config ngrok.yml
```

Note the HTTPS URL ngrok prints — something like `https://abc123.ngrok-free.dev`. That's your public address for `beckn-router:9000`. You can watch each request flow through the tunnel at the local inspector: [http://localhost:4040](http://localhost:4040).

### Re-run the flow through the tunnel

In your Postman collection, change the two host variables you set in §4 — replace `http://beckn-router:9000` with your ngrok URL:

| Variable | Value (ngrok mode) |
|---|---|
| `bap_host_root` | `https://<your-subdomain>.ngrok-free.dev` |
| `bpp_host_root` | `https://<your-subdomain>.ngrok-free.dev` |

Leave `beckn_adapter_url` alone — Postman still POSTs to your local ONIX at `http://localhost:8081/bap/caller`. Only the payload's `bapUri` / `bppUri` need to be publicly reachable, and that's what these variables substitute.

Fire `confirm` again. The callback now travels: your Postman → local ONIX-BAP → out via ngrok → public internet → back in via ngrok → ONIX-BPP → `sandbox-bpp` → back through the same hops. The ngrok inspector at `:4040` shows three hops per transactional step (`Postman → BAP`, `BAP → BPP`, `BPP → BAP callback`).

### Transacting with another participant

For interop testing with someone else's node:

- Each side starts their own ngrok tunnel; exchange tunnel URLs out-of-band.
- The BAP-side participant sets `bpp_host_root` to the **other side's** ngrok URL. `bap_host_root` stays at their own.
- The BPP-side participant emits payloads whose `bppUri` is their own ngrok URL; their `bap_host_root` (for outbound callbacks) is set to the BAP's tunnel.

This pattern lets two laptop-hosted Beckn nodes do full bidirectional exchanges over the public internet without any cloud deployment — useful for early conformance testing between participants before either side has DeDi identity in place.

When you're done, `Ctrl+C` ngrok to bring the tunnel down. The docker stack keeps running, and reverting `bap_host_root` / `bpp_host_root` to `http://beckn-router:9000` returns you to local-only mode.

---

## 7. Wire in your application

Sections 1–6 prove the wiring against the bundled sandbox containers (locally in §4–5 and over the public internet in §6). To run real consumer or provider logic instead, **replace** the sandbox container on your side:

### BAP — receive the callback in your own app

`sandbox-bap` is the default webhook receiver for `on_*` callbacks; you swap it out for your application:

1. Stand up your service exposing the four BAP callback paths: `POST /bap/receiver/on_confirm`, `on_status`, `on_select`, `on_init` (only the ones your flow needs).
2. Place your container on the `bap_side` docker network (or expose it on a routable host and update the next step accordingly).
3. Stop `sandbox-bap`. ONIX-BAP delivers callbacks to whatever URL is in the message's `bapUri`, so update the `bapUri` baked into the example payloads — or your own outbound payloads — to point at your service.

For a quick sanity check, you can run both side-by-side at first: keep `sandbox-bap` for diff'ing and point your service at a different path until you trust it.

### BPP — serve real data from your provider

`sandbox-bpp` ships canned responses sourced from `uc*/examples/`. To serve real data:

1. Implement the four BPP request paths: `POST /bpp/receiver/confirm`, `status`, `select`, `init` (only the ones your flow needs). Each should:
   - Return the synchronous `{"message":{"ack":{"status":"ACK"}}}` envelope immediately.
   - Asynchronously post the corresponding `on_*` callback to ONIX-BPP at `http://onix-bpp:8082/bpp/caller/on_<action>`.
2. Match the wire shape exactly — copy the structure from `uc*/examples/on-*-response*.json`, swap in your real data.
3. Stop `sandbox-bpp` and run your provider container on the `bpp_side` network. ONIX-BPP routes by path, not by host.

The example payloads in `uc*/examples/` are your reference wire format; the `sandbox-bpp` source itself is a working minimal provider you can fork.

---

## 8. Stop the stack

```bash
cd DEG/devkits/data-exchange/install
docker compose down
```

---

## 9. Going beyond the sandbox

Onboarding is a two-phase progression. Don't skip phase 1.

### Phase 1 — Use the devkit as-is and prove the flows

Sections 1–6 above are the whole of phase 1. Run them with the shipped sandbox identities (`bap.example.com` / `bpp.example.com`), the placeholder `networkId` in the devkit payloads, and the sandbox signing keys committed in `config/`. The goal is to confirm the wiring, your application's handling of the `dataPayload` shape, and (for BPPs) your provider's wire format — without involving DeDi or any real IES network.

### Phase 2 — Swap in your real identity

Only once phase 1 is solid, replace the sandbox identity with yours. The knobs live in [`devkits/data-exchange/config/local-simple-bap.yaml`](https://github.com/beckn/DEG/blob/main/devkits/data-exchange/config/local-simple-bap.yaml) (and the matching `local-simple-bpp.yaml`), nested under `modules[].handler.plugins`:

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
            # encrPrivateKey / encrPublicKey similarly if you're using encryption
```

| Knob (YAML path under `plugins.`) | Sandbox value | Replace with |
|---|---|---|
| `registry.config.allowedNetworkIDs` | placeholder | `indiaenergystack.in/test-ies-data-sharing-network` *(stay on test until certified — see [Registry Setup § Two registries, two ONIX deployments](./registry-setup.md#two-registries-two-onix-deployments))* |
| `keyManager.config.networkParticipant` | `bap.example.com` / `bpp.example.com` | Your real `subscriberId` from the DeDi record you publish |
| `keyManager.config.keyId` | sandbox `keyId` | Your real `recordId` from DeDi |
| `keyManager.config.signing{Private,Public}Key` | sandbox keys committed in `config/` | Your Ed25519 keypair (public half also published in DeDi) |

The corresponding pre-work on DeDi (verify namespace → create subscriber registry → publish record with public key → ask IES to add your DeDi URL to the network reference registry) is the full subject of [Registry Setup](./registry-setup.md). The lookup URL you copied from DeDi is what you hand to IES; the `recordId` you noted is what you put in ONIX as `keyId`.

After the config swap, re-import the same Postman collection — the requests are identical, only the identity ONIX signs with and the network it claims has changed. A successful `confirm` against another participant on `indiaenergystack.in/test-ies-data-sharing-network` proves end-to-end onboarding.

Promote to `indiaenergystack.in/ies-data-sharing-network` only when testing is finished and IES has added your prod DeDi URL to the prod network's reference registry. The recommended pattern is **two separate ONIX deployments** with `allowedNetworkIDs` narrowed to one network each — see [Registry Setup](./registry-setup.md#two-registries-two-onix-deployments).

---

## Onboarding checklist

### BAP (Data Consumer)

Phase 1 — devkit as-is:
- [ ] Devkit cloned, stack up (`docker compose up -d` in `install/`)
- [ ] BAP Postman collection imported, variables set
- [ ] `confirm` → `on_confirm` round-trip succeeds against `sandbox-bpp`
- [ ] Your application can consume the `dataPayload` body

Phase 2 — real identity on `indiaenergystack.in/test-ies-data-sharing-network`:
- [ ] DeDi namespace verified; subscriber registry created
- [ ] Subscriber record published (public key, callback URL); `recordId` noted
- [ ] DeDi lookup URL handed to IES; reference entry added to the test network registry
- [ ] `config/local-simple-bap.yaml` updated: `allowedNetworkIDs`, `subscriberId`, `keyId`, private key
- [ ] Same flow passes against the test network → ready for IES to promote you to prod ([Registry Setup](./registry-setup.md))

### BPP (Data Provider)

Phase 1 — devkit as-is:
- [ ] Devkit cloned, stack up
- [ ] BPP Postman collection imported, variables set
- [ ] Your provider implementation handles inbound `confirm` and emits `on_confirm` (or `on_status` for async delivery) — start from the `sandbox-bpp` reference behaviour
- [ ] Example payloads in `uc*/examples/` align with your schema output

Phase 2 — real identity on `indiaenergystack.in/test-ies-data-sharing-network`:
- [ ] DeDi namespace verified; subscriber registry created
- [ ] Subscriber record published; `recordId` noted; DeDi lookup URL handed to IES
- [ ] `config/local-simple-bpp.yaml` updated: `allowedNetworkIDs`, `subscriberId`, `keyId`, private key
- [ ] End-to-end exchange completes with another participant on the test network → ready for prod ([Registry Setup](./registry-setup.md))

---

## Reference

- [Architecture](./architecture.md) — stack topology, generic flow, context invariants
- [Devkit README](https://github.com/beckn/DEG/blob/main/devkits/README.md) — multi-network ONIX, hosting/TLS, ngrok
- [docs.nfh.global/beckn](https://docs.nfh.global/beckn) — network and registry primitives
- [Beckn protocol v2.0.0 spec](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0)

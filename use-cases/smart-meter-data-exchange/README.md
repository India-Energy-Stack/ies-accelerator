# Smart Meter Data Exchange

**A standard, audit-trailed API for sharing 15-minute AMI smart-meter data between an AMISP, the DISCOM, the state regulator, and consented third parties.**

---

## Scenario

Smart meter readings are the foundation of modern distribution operations: load forecasting, billing validation, DT loading, theft analytics, time-of-day tariff enforcement, and DER planning all depend on meter data flowing reliably from the AMISP that operates the meters to the DISCOM that owns the relationship — and onward to the SERC or to consented third-party analytics providers.

Today this is a tangle of bespoke FTP drops, proprietary MDMS APIs, and CSV email attachments. The Smart Meter Data Exchange use case replaces these with a single, discoverable, signed, schema-validated exchange over the IES Data Exchange protocol.

> For consumer-pull of their own meter data (one-meter, on-demand, wallet-shareable), see the sister use case [Consumer Meter Digest](../consumer-meter-digest.md). This guide is the bulk, scheduled, machine-to-machine flow.

---

## Actors and Roles

| Role | Organisation (example) | What they do |
|---|---|---|
| **BPP** — data provider | AMISP (e.g. IntelliGrid AMI Services) | Operates the meter network; publishes `IES_Report` datasets |
| **BAP** — data consumer | DISCOM (e.g. BESCOM) | Subscribes to and ingests meter data for billing, forecasting, analytics |
| **Optional BAP** — secondary consumer | SERC, planner, research org, consented third-party app | Requests data via the same protocol, gated by credentials and policy |
| **Identity authority** | DISCOM / IES registries | Issues meter and DT identifiers; registers all participants |

The protocol is symmetric — the same surface area supports AMISP→DISCOM, DISCOM→SERC, and DISCOM→consented-third-party flows.

---

## Building Blocks Used

| Block | Role in this use case |
|---|---|
| [Identifiers](../../identifiers/README.md) | Every meter, DT, feeder, and substation involved is referenced by an IES identifier. Resource references in the exchange (`resourceName`) carry these IDs. |
| [Registries](../../registries/README.md) | The AMISP, DISCOM, and SERC participants are looked up in their respective DeDi registries. Meter/asset IDs are resolved through utility-operated identifier registries. |
| [Data Exchange](../../data-exchange/README.md) | The Beckn-based protocol that carries the `IES_Report` payload from BPP to BAP, with optional discovery, contract, and async delivery semantics. |
| [Energy Credentials](../../energy-credentials/README.md) | *Optional for the M2M flow; required when a consumer-consented third party is the BAP.* The third party presents the [Consumer Meter Digest](../consumer-meter-digest.md) authorisation or holds a presentation of the consumer's [Consumer Energy Passport](../consumer-energy-passport.md). |

---

## The Dataset — `IES_Report`

The `IES_Report` schema carries meter telemetry in **OpenADR 3.1.0 REPORT** format. OpenADR is an international standard for energy-management signalling; IES uses its `REPORT` object as the container for meter readings.

A minimal 15-minute load-survey block looks like:

```json
{
  "objectType": "REPORT",
  "reportID": "rep-bescom-zone-a-2026-04-01",
  "programID": "amisp-telemetry-bescom-2026",
  "reportPayloadDescriptors": [
    {
      "payloadType": "USAGE",
      "readingType": "DIRECT_READ",
      "units": "KWH"
    }
  ],
  "resources": [{
    "resourceName": "meter-KA-98765432",
    "intervalPeriod": { "start": "2026-04-01T00:00:00+05:30", "duration": "PT15M" },
    "intervals": [
      { "id": 0, "payloads": [{ "type": "USAGE", "values": [1.12] }] },
      { "id": 1, "payloads": [{ "type": "USAGE", "values": [1.15] }] }
    ]
  }]
}
```

The full mapping from Indian OBIS codes (IS 15959) and Event IDs to OpenADR 3 `payloadType` / `readingType` lives in [IES Data Model](ies-data-model.md), with the existing-terminology side-by-side reference in [Survey of Existing Terminology](survey-of-existing-terminology.md).

> **Status — `IES_Report` schema is being finalised.** Field names and a couple of enums may move during the merge of `beckn/DEG:ies-specs` into `India-Energy-Stack`. The OpenADR 3 envelope itself is stable; integrate against the devkit examples and expect minor renames at the IES wrapper level.

---

## Setup Steps

The order below takes you from zero to a working AMISP → DISCOM flow on the local devkit, then upgrades to a real-network deployment.

### 1. Register the participants

Both the AMISP (BPP) and the DISCOM (BAP) need entries in the relevant DeDi registries:

- **DISCOM** — [IES DISCOMs Reference Registry](../../registries/required-registries.md#discoms-registry), `india-energy-stack:<discom-short-code>` (e.g. `india-energy-stack:bescom`).
- **AMISP** — registered in the same `india-energy-stack` namespace as a data-provider participant. Use the [Registry Creation](../../registries/registry-creation.md) guide if your AMISP entry does not yet exist.
- **SERC** (if it will be a downstream consumer) — [IES Regulators Reference Registry](../../registries/required-registries.md#regulators-registry).

Each registration pins a `did:web` and the public key used to sign Beckn messages and credentials issued by that participant.

### 2. Issue meter and asset identifiers

Every meter referenced in an `IES_Report` must resolve to a stable IES identifier. The DISCOM (or AMISP, by delegation) issues meter IDs into a utility-scoped registry under the IES Identifier patterns — see [ID Patterns](../../identifiers/id-patterns.md). DT, feeder, and substation IDs follow the same scheme and are referenced from meter attributes (`DT_ID`, `FEEDER_ID`, `SUBSTATION_ID`).

The same resource identifier appears as `resourceName` inside the OpenADR `REPORT` and inside the Beckn `resources[].id` envelope — this is what lets the regulator or analytics consumer correlate readings to physical assets without an out-of-band asset register handshake.

### 3. Stand up the data-exchange adapters

Both sides run an ONIX adapter against the Beckn protocol. The simplest start is the local sandbox:

```bash
git clone https://github.com/beckn/DEG.git
cd DEG/devkits/data-exchange/install
docker compose up -d
```

This brings up `sandbox-bap`, `sandbox-bpp`, and `beckn-router` containers pre-wired with the AMISP/DISCOM example identities (`bap.example.com` / `bpp.example.com`).

For production, follow [Registry Setup](../../data-exchange/registry-setup.md) — point the adapter at the IES registry endpoint, install your `did:web` keypair, and replace the sandbox routing config with your AMISP/DISCOM hosts.

### 4. Configure the dataset catalogue

The AMISP publishes a catalogue entry describing the `IES_Report` dataset it offers — `programID`, geographic scope, refresh cadence, access method (`INLINE` for ≤MB-scale chunks, `SIGNED_URL` for daily/monthly bulk), and any required credentials. The DISCOM uses `discover` to find this catalogue, or skips straight to `confirm` for a pre-agreed bilateral subscription.

The catalogue lives inside the BPP's ONIX config — see [Architecture § Generic Beckn Flow](../../data-exchange/architecture.md#generic-beckn-flow).

### 5. Exercise the flow

The minimal lifecycle is `confirm` → `on_confirm` → `status` → `on_status`:

| Step | Sender | What happens |
|---|---|---|
| `confirm` | BAP (DISCOM) | Requests the dataset for a meter list and a date range; the message is signed with the DISCOM's `did:web` key |
| `on_confirm` | BPP (AMISP) | Acknowledges the contract; declares the dataset will be delivered asynchronously |
| `status` | BAP | Polls for delivery (optional with webhook-driven push) |
| `on_status` | BPP | Delivers the `IES_Report` inline (small payloads) or returns a signed-URL pointer (bulk) |

The dataset is carried inside `message.contract.commitments[].resources[].resourceAttributes` qualified with the DDM `DatasetItem/v1.1` `@context`:

```json
"resources": [{
  "id": "ds-ami-meter-data-blr-zone-a-q1-2026",
  "descriptor": { "name": "IntelliGrid AMI Meter Data — Bengaluru Zone A — Q1 2026" },
  "resourceAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1.1/context.jsonld",
    "@type": "DatasetItem",
    "accessMethod": "INLINE",
    "dataPayload": { /* IES_Report — see snippet above */ }
  }
}]
```

### 6. (Optional) Enable consented third-party access

When the DISCOM wants to allow a consumer-authorised third party to pull data on a specific consumer's meter, the third party becomes the BAP and presents a [Consumer Meter Digest](../consumer-meter-digest.md) authorisation credential alongside the `confirm`. The BPP verifies the credential (issuer = DISCOM, subject = consumer, scope = this meter, validity in range) before delivering data. The credential model and the data-exchange policy hook are the integration boundary — no new protocol surface.

---

## Operate

Once the sandbox is up:

```bash
# Import the BAP Postman collection from
#   DEG/devkits/data-exchange/uc1-meter-data/postman/
# Set bap_host_root + bpp_host_root to http://beckn-router:9000 (or your tunnel URL)
# Fire `confirm` from the collection.

docker logs sandbox-bap 2>&1 | grep -E 'on_(confirm|status)' | tail -10
```

The Arazzo runner can drive the full lifecycle in one shot:

```bash
cd DEG/devkits/data-exchange/uc1-meter-data/workflows
./run-arazzo.sh -w confirm-through-delivery -v
```

---

## Open Items

- **`IES_Report` schema canonicalisation.** The schema currently lives on the `ies-specs` branch of `beckn/DEG`; it will move to `India-Energy-Stack`. Field names may be renamed (no semantic changes expected).
- **Standard chunking convention** for bulk historical pulls (daily / monthly / quarterly) is being agreed — the devkit uses 10-chunk daily splits in the example payloads.
- **Quality flags.** The OpenADR `DATA_QUALITY` payloadType is the agreed mechanism for marking missing/estimated reads; the IES profile of allowable values is being tightened.

---

## References

- [Basic Checklist](./basic-checklist.md) — plain-English rollout checklist
- [`IES_Report` schema (upstream)](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core)
- [OpenADR 3.1.0 Specification](https://www.openadr.org)
- [Example payloads (devkit)](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc1-meter-data/examples)
- [Survey of Existing Terminology](survey-of-existing-terminology.md) — OBIS codes, Event IDs, CIM
- [IES Data Model](ies-data-model.md) — full OBIS → OpenADR 3 mapping table
- [Data Exchange — Architecture](../../data-exchange/architecture.md)
- [Data Exchange — Quick Start](../../data-exchange/quick-start.md)
- [ies-docs `data_exchange_summary.md`](https://github.com/India-Energy-Stack/ies-docs/blob/main/implementation-guides/data_exchange/data_exchange_summary.md)

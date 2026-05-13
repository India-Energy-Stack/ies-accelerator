# Meter Telemetry

**AMI meter data exchange between an Advanced Metering Infrastructure Service Provider (AMISP) and a Distribution Company (DISCOM).**

***

## Scenario

An AMISP (e.g. IntelliGrid AMI Services) has collected 15-minute interval smart meter readings from thousands of meters across a DISCOM's (e.g. BESCOM's) service area. The DISCOM needs this data for load forecasting, billing validation, and regulatory reporting. Rather than a bespoke FTP push or proprietary API call, the exchange happens over the IES Data Exchange protocol — discoverable, auditable, and schema-validated.

***

## Roles

| Role           | Organisation                     | What they do                                                 |
| -------------- | -------------------------------- | ------------------------------------------------------------ |
| BAP (consumer) | BESCOM (DISCOM)                  | Requests meter telemetry for a given meter ID and date range |
| BPP (provider) | IntelliGrid AMI Services (AMISP) | Publishes and delivers `IES_Report` datasets                 |

***

## Dataset — IES\_Report

The `IES_Report` schema carries meter telemetry in **OpenADR 3.1.0** format. OpenADR is an international standard for communicating demand response and energy management signals; IES uses it as the container for meter readings.

### Structure

```json
{
  "programID": "amisp-telemetry-bescom-2026",
  "payloadDescriptors": [
    {
      "payloadType": "USAGE",
      "units": "KWH",
      "accuracy": 0.01,
      "confidence": 99
    }
  ],
  "resources": [
    {
      "resourceName": "meter-KA-98765432",
      "intervals": [
        {
          "id": 0,
          "intervalPeriod": {
            "start": "2026-04-01T00:00:00+05:30",
            "duration": "PT15M"
          },
          "payloads": [{ "type": "USAGE", "values": [1.23] }]
        },
        {
          "id": 1,
          "intervalPeriod": {
            "start": "2026-04-01T00:15:00+05:30",
            "duration": "PT15M"
          },
          "payloads": [{ "type": "USAGE", "values": [1.41] }]
        }
      ]
    }
  ]
}
```

| Field                     | Description                                                               |
| ------------------------- | ------------------------------------------------------------------------- |
| `programID`               | Dataset identifier — used by the BAP to select the right dataset          |
| `payloadDescriptors`      | Declares measurement type (`USAGE`), unit (`KWH`), and precision          |
| `resources[]`             | One entry per meter                                                       |
| `resourceName`            | Meter ID — the unique identifier for the smart meter                      |
| `intervals[]`             | One entry per 15-minute period                                            |
| `intervalPeriod.start`    | ISO 8601 timestamp with IST offset (`+05:30`)                             |
| `intervalPeriod.duration` | Always `PT15M` for 15-minute AMI data                                     |
| `payloads[].values`       | Array of readings — single value for USAGE (kWh consumed in the interval) |

***

## Transaction Flow

UC1 exercises **`confirm` → `on_confirm` → `status` → `on_status`** — the contract is acknowledged in `on_confirm`, and the meter report is delivered asynchronously in `on_status`. Discovery (`publish-catalog` / `discover`) and negotiation (`select` / `init`) are ALSO shipped in the devkit but optional for the existing-contract scenario.

The dataset is carried inside `message.contract.commitments[].resources[].resourceAttributes`, qualified with the DDM `DatasetItem/v1.1` `@context`:

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

Full request/response examples (publish, discover, confirm, on-confirm, status, on-status) live in [uc1-meter-data/examples/](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc1-meter-data/examples).

***

## Running This Use Case

```bash
cd DEG/devkits/data-exchange/install
docker compose up -d
```

Then import the BAP collection at `uc1-meter-data/postman/data-exchange-uc1-meter-data.BAP-DEG.postman_collection.json` into Postman, set `bap_host_root` and `bpp_host_root` to `http://beckn-router:9000` (or your tunnel URL), and fire `confirm`. Inspect the callback:

```bash
docker logs sandbox-bap 2>&1 | grep -E 'on_(confirm|status)' | tail -10
```

See the [Quick Start](../../quick-start.md) for the full step-by-step.

***

## Reference

* [IES\_Report Schema](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core) *(currently on the `ies-specs` branch; will move to India-Energy-Stack — see [Concepts § IES Data Schemas](../../concepts.md#ies-data-schemas))*
* [OpenADR 3.1.0 Specification](https://www.openadr.org)
* [Example payloads](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc1-meter-data/examples)
* [survey-of-existing-terminology.md](survey-of-existing-terminology.md)
* [ies-data-model.md](ies-data-model.md)

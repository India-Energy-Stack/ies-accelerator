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

### 1. Select

The BAP requests available datasets from the AMISP for a specific meter:

```json
{
  "context": {
    "action": "select",
    "domain": "deg:data-exchange",
    "bap_id": "bescom.discom.karnataka.ies.in",
    "bpp_id": "intelligrid.amisp.ies.in",
    "transaction_id": "txn-meter-001"
  },
  "message": {
    "order": {
      "items": [
        {
          "id": "amisp-meter-data-ka-2026-q1",
          "descriptor": { "code": "IES_Report" }
        }
      ],
      "fulfillments": [
        {
          "id": "ff-001",
          "type": "DATA_DELIVERY",
          "tags": [
            { "code": "resource_id", "value": "meter-KA-98765432" },
            { "code": "date_range", "value": "2026-04-01/2026-04-07" }
          ]
        }
      ]
    }
  }
}
```

The BPP responds with `on_select` containing the catalog item with access terms (pricing, delivery mode, SLA).

### 2–3. Init and Confirm

Standard Beckn lifecycle — init activates the contract, confirm locks it. The BPP transitions the order state: `DRAFT → SELECTED → INITIALIZED → CONFIRMED`.

### 4. Status

The BAP calls status to trigger data delivery. The BPP responds with `on_status` containing the full `IES_Report` in `dataPayload`:

```json
{
  "message": {
    "order": {
      "status": "DELIVERY_COMPLETE",
      "items": [
        {
          "id": "amisp-meter-data-ka-2026-q1",
          "accessMethod": "INLINE",
          "dataPayload": {
            "programID": "amisp-telemetry-bescom-2026",
            "payloadDescriptors": [ /* ... */ ],
            "resources": [
              {
                "resourceName": "meter-KA-98765432",
                "intervals": [ /* 672 intervals for 7 days × 96 per day */ ]
              }
            ]
          }
        }
      ]
    }
  }
}
```

***

## Running This Use Case

```bash
cd DEG/devkits/data-exchange

# Start bootcamp stack
cd install && docker compose -f docker-compose-bootcamp.yml up -d --build && cd ..

# Run all 15 steps
./scripts/test-workflow.sh usecase1

# Or manually
curl -X POST http://localhost:8081/bap/caller/select \
  -H "Content-Type: application/json" \
  -d @usecase1/examples/select-request.json

curl -X POST http://localhost:8081/bap/caller/init \
  -H "Content-Type: application/json" \
  -d @usecase1/examples/init-request.json

curl -X POST http://localhost:8081/bap/caller/confirm \
  -H "Content-Type: application/json" \
  -d @usecase1/examples/confirm-request.json

curl -X POST http://localhost:8081/bap/caller/status \
  -H "Content-Type: application/json" \
  -d @usecase1/examples/status-request.json
```

Check the delivered data:

```bash
docker logs sandbox-bap 2>&1 | tail -100
```

***

## Reference

* [IES\_Report Schema](https://github.com/India-Energy-Stack/ies-docs)
* [OpenADR 3.1.0 Specification](https://www.openadr.org)
* [Example payloads](https://github.com/Beckn-One/DEG/tree/main/devkits/data-exchange/usecase1/examples)
* [survey-of-existing-terminology.md](survey-of-existing-terminology.md "mention")
* [ies-data-model.md](ies-data-model.md "mention")

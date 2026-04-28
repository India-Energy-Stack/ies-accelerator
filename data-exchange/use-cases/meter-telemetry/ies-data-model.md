# IES Data Model

This document maps the Indian Smart Metering and grid terminology to the standard OpenADR 3 data model. This provides a unified framework for integrating Advanced Metering Infrastructure (AMI) and Distributed Energy Resources (DERs) into the India Energy Stack (IES).

For the existing Indian Smart Metering specifications (OBIS codes, Event IDs, and CIM details), refer to the [Survey of Existing Terminology](survey-of-existing-terminology.md).

## 1. RESOURCE Attributes

OpenADR 3 defines `Resource.attributes` as a list of `valuesMap` objects. To support both AMI meters and generalized DERs, we use the standard OpenADR 3 attribute enumerations where applicable. Where standard terms do not exist for meter-specific metadata, we use custom extensions. **All standard OpenADR Resource Attributes are included to support DER integration.**

| OpenADR 3 `attributes` (type) | Is Standard Term? | Indian Term Equivalent / Description | Source System |
| ----------------------------- | ----------------- | ------------------------------------ | ------------- |
| `LOCATION`                    | Yes               | GIS Lat/Long Coordinates             | GIS |
| `AREA`                        | Yes               | Geographic Polygon/Area              | GIS |
| `POLE_ID`                     | No                | Pole ID                              | GIS |
| `SUBSTATION_ID`               | No                | Substation ID                        | GIS |
| `PHASE`                       | No                | Phase (Single Phase / 3 Phase)       | GIS / Asset |
| `FEEDER_ID`                   | No                | Feeder ID                            | GIS |
| `DT_ID`                       | No                | Distribution Transformer (DT) ID     | GIS |
| `MAX_POWER_CONSUMPTION`       | Yes               | Sanctioned Load                      | CIS (Billing) |
| `MAX_POWER_EXPORT`            | Yes               | Maximum Export Capacity              | CIS / DER |
| `DESCRIPTION`                 | Yes               | General Description / Consumer Name  | CIS (Billing) |
| `CONSUMER_NUMBER`             | No                | Consumer ID / K-No                   | CIS (Billing) |
| `CONSUMER_CATEGORY`           | No                | Consumer Category (DS/NDS)           | CIS (Billing) |
| `ADDRESS`                     | No                | Physical Address (Can be broken down further into Street, City, Pin Code) | CIS (Billing) |
| `METER_SERIAL_NO`             | No                | Meter Serial No (Asset Data)         | Inventory / ERP |
| `METER_MAKE_MODEL`            | No                | Meter Make and Model                 | Inventory / ERP |
| `METER_FIRMWARE`              | No                | Firmware Version                     | Inventory / ERP |

## 2. REPORT payloadDescriptors (Telemetry & Logs)

In OpenADR 3, a `REPORT` captures periodic telemetry and meter-generated events. **All standard OpenADR report payload types are documented**, covering smart meter OBIS codes as well as broader DER use cases. 

*Note: Multiple Indian OBIS codes (e.g., Load Profile vs Billing Profile) map to the same `payloadType` (e.g., `USAGE`). They are differentiated by the `intervalPeriod.duration` (e.g., 15m, 24h, 1mo) within the report itself.*

*Note on `readingType`: OpenADR 3 defines standard reading types to qualify the reported value: `DIRECT_READ` (default for meter measurements), `ESTIMATED`, `SUMMED`, `MEAN`, `PEAK`, `FORECAST`, and `AVERAGE`. For cumulative meter readings and energy consumption over an interval, `DIRECT_READ` is typically used. For instantaneous power or averaged values, `MEAN` or `PEAK` is used.*

*Note on Data Quality: In OpenADR 3, data quality can be communicated using the `DATA_QUALITY` payloadType, with standard values being `OK`, `MISSING`, `ESTIMATED`, or `BAD`.*

*Note on Import vs Export: To distinctly represent consumption versus generation, `USAGE` is used for consumption/import, and a separate `EXPORT` payloadType is used for generation/export (rather than using negative values for `USAGE`).*

| OpenADR 3 `payloadType` | OpenADR 3 `readingType` | Is Standard Term? | Indian Term / OBIS Code | Profile / Interval |
| ----------------------- | ----------------------- | ----------------- | ----------------------- | ------------------ |
| `USAGE`                 | `DIRECT_READ`           | Yes               | `1.0.1.29.0.255` (kWh) Active Energy Import (Incremental) | Load Profile (15m/30m) |
| `USAGE`                 | `SUMMED`                | Yes               | `1.0.1.8.0.255` (kWh) Active Energy Import (Total) | Daily Profile (24h) / Monthly (1mo) |
| `USAGE`                 | `DIRECT_READ`           | Yes               | `1.0.9.29.0.255` (kVAh) Apparent Energy Import (Incremental) | Load Profile (15m/30m) |
| `USAGE`                 | `SUMMED`                | Yes               | `1.0.9.8.0.255` (kVAh) Apparent Energy Import (Total) | Daily Profile (24h) / Monthly (1mo) |
| `EXPORT`                | `DIRECT_READ`           | No                | `1.0.2.29.0.255` (kWh-Exp) Energy Export (Incremental) | Load Profile (15m/30m) |
| `EXPORT`                | `SUMMED`                | No                | `1.0.2.8.0.255` (kWh-Exp) Energy Export (Total) | Daily Profile (24h) / Monthly (1mo) |
| `DEMAND`                | `PEAK`                  | Yes               | `1.0.1.6.0.255` (kW) Maximum Demand | Billing Profile (1mo) |
| `DEMAND`                | `MEAN`                  | Yes               | `1.0.1.7.0.255` (kW) Active Power | Instantaneous |
| `READING`               | `MEAN`                  | Yes               | `1.0.12.7.0.255` Voltage, `1.0.11.7.0.255` Current | Instantaneous |
| `SETPOINT`              | `MEAN`                  | Yes               | N/A (Standard for DERs) | N/A |
| `BASELINE`              | `MEAN`/`PEAK`           | Yes               | N/A (Standard for DERs) | Indicates energy/power in the absence of load control |
| `OPERATING_STATE`       | N/A                     | Yes               | N/A (Standard for DERs) | E.g., `NORMAL`, `ERROR`, `IDLE_NORMAL` |
| `USAGE_FORECAST`        | `FORECAST`              | Yes               | N/A (Standard for DERs) | Expected resource usage |
| `DATA_QUALITY`          | N/A                     | Yes               | N/A                     | String indicating `OK`, `MISSING`, `ESTIMATED`, `BAD` |
| `METER_TAMPER`          | N/A                     | No                | Event ID 201 (Magnetic Interference), etc. | Event Log Profile |
| `POWER_QUALITY`         | N/A                     | No                | Event ID 1 (Under Voltage), ID 11 (Phase Missing) | Event Log Profile |

## 3. EVENT payloadDescriptors (Control Signals)

OpenADR `EVENT`s represent dispatch signals sent from the Virtual Top Node (VTN) to the Virtual End Node (VEN), such as a meter or DER. **We enumerate all standard OpenADR Event payload types** to support full grid flexibility, mapping them to Indian standard Event IDs (e.g., Connect/Disconnect) where they intersect.

| OpenADR 3 `payloadType` | Value Type | Is Standard Term? | Indian Event / Action | Description |
| ----------------------- | ---------- | ----------------- | --------------------- | ----------- |
| `CONTROL_SETPOINT`      | Application defined | Yes | Event ID 301/302 (Relay Disconnect/Connect) | Used for device control instructions like opening/closing relays. |
| `IMPORT_CAPACITY_LIMIT` | float      | Yes               | Prepay Low Credit Disconnect / Load Limit | Maximum import level for the site. |
| `EXPORT_CAPACITY_LIMIT` | float      | Yes               | N/A                   | Maximum export level for the site. |
| `PRICE`                 | float      | Yes               | N/A                   | The cost of energy. |
| `GHG`                   | float      | Yes               | N/A                   | Marginal Greenhouse Gas emissions (g/kWh). |
| `DISPATCH_SETPOINT`     | float      | Yes               | N/A                   | Absolute consumption/export amount by a resource. |
| `DISPATCH_SETPOINT_RELATIVE` | float | Yes               | N/A                   | Relative change in consumption by a resource. |
| `DISPATCH_INSTRUCTION`  | Application defined | Yes | N/A                   | Implementation-specific dispatch instructions. |
| `CHARGE_STATE`          | float      | Yes               | N/A                   | State of charge for energy storage resources. |
| `ENERGY`                | float      | Yes               | N/A                   | Energy value for events. |
| `DEMAND_CHARGE`         | float      | Yes               | N/A                   | Price for peak power capacity (kW). |
| `BID_PRICE`             | float      | Yes               | N/A                   | Price submitted for market bidding. |
| `BID_LOAD`              | float      | Yes               | N/A                   | Load quantity submitted for market bidding. |
| `EXPORT_PRICE`          | float      | Yes               | N/A                   | Price of energy exported to the grid. |
| `CONTROL_LEVEL_OFFSET`  | int (-10 to 10) | Yes         | N/A                   | Discrete levels relative to normal operations. |
| `PROGRAMMING_CONFIG`    | string     | No                | Event ID 151 (Parameter Programming) | Configuration change triggers. |

## 4. OpenADR 3 JSON Examples

### 4.1. RESOURCE Example
A meter resource illustrating standard and custom attributes.

```json
{
  "objectType": "RESOURCE",
  "resourceName": "meter-KA-98765432",
  "venID": "ven_karnataka_001",
  "attributes": [
    {
      "type": "LOCATION",
      "values": [12.9716, 77.5946]
    },
    {
      "type": "MAX_POWER_CONSUMPTION",
      "values": [5.0]
    },
    {
      "type": "METER_SERIAL_NO",
      "values": ["123456789"]
    },
    {
      "type": "CONSUMER_NUMBER",
      "values": ["RR-1234"]
    }
  ]
}
```

### 4.2. EVENT Example (Control Signal)
An event dispatched to disconnect a relay.

```json
{
  "objectType": "EVENT",
  "eventID": "evt-disconnect-001",
  "programID": "prepay-program-2026",
  "targets": [{"type": "RESOURCE_NAME", "values": ["meter-KA-98765432"]}],
  "eventPayloadDescriptors": [
    {
      "objectType": "EVENT_PAYLOAD_DESCRIPTOR",
      "payloadType": "CONTROL_SETPOINT"
    }
  ],
  "intervals": [
    {
      "id": 0,
      "intervalPeriod": {
        "start": "2026-04-01T10:00:00Z",
        "duration": "PT2H"
      },
      "payloads": [
        {
          "type": "CONTROL_SETPOINT",
          "values": ["DISCONNECT"]
        }
      ]
    }
  ]
}
```

### 4.3. REPORT Examples

Reports can capture instantaneous live telemetry or batch historic data into a very compact format. For historic batching, hundreds of reading payload arrays are collected under the same set of interval rules, avoiding repetition of metadata.

#### Live Instantaneous Report
A single payload for immediate telemetry (e.g., Voltage reading).

```json
{
  "objectType": "REPORT",
  "reportID": "rep-live-001",
  "programID": "grid-monitoring-2026",
  "reportPayloadDescriptors": [
    {
      "objectType": "REPORT_PAYLOAD_DESCRIPTOR",
      "payloadType": "READING",
      "readingType": "MEAN",
      "units": "V"
    }
  ],
  "resources": [
    {
      "resourceName": "meter-KA-98765432",
      "intervals": [
        {
          "id": 0,
          "intervalPeriod": {
            "start": "2026-04-01T10:00:00Z",
            "duration": "PT0S"
          },
          "payloads": [
            {
              "type": "READING",
              "values": [230.5]
            }
          ]
        }
      ]
    }
  ]
}
```

#### Historic Data (Compactness)
When sending historical data (like a 15m load survey), the OpenADR 3 format is highly compact because the `reportPayloadDescriptors` define the schema once. 

*Further Compactness:* As permitted by the OpenADR 3 specification, the `intervalPeriod` (containing `start` and `duration`) can be defined exactly once at the `resources` level. The `intervals` array then linearly maps values over time without repeating timestamps or durations for every single point. The start time of `interval[N]` is implicitly `start + N * duration`.

##### Load Survey (15m Intervals - Ultra Compact)
```json
{
  "objectType": "REPORT",
  "reportID": "rep-historic-load-001",
  "programID": "load-survey-15m",
  "reportPayloadDescriptors": [
    {
      "objectType": "REPORT_PAYLOAD_DESCRIPTOR",
      "payloadType": "USAGE",
      "readingType": "DIRECT_READ",
      "units": "KWH"
    }
  ],
  "resources": [
    {
      "resourceName": "meter-KA-98765432",
      "intervalPeriod": {"start": "2026-04-01T00:00:00Z", "duration": "PT15M"},
      "intervals": [
        {
          "id": 0,
          "payloads": [{"type": "USAGE", "values": [1.12]}]
        },
        {
          "id": 1,
          "payloads": [{"type": "USAGE", "values": [1.15]}]
        }
      ]
    }
  ]
}
```

##### Daily Survey (24h Interval)
```json
{
  "objectType": "REPORT",
  "reportID": "rep-daily-001",
  "programID": "daily-survey",
  "reportPayloadDescriptors": [
    {
      "objectType": "REPORT_PAYLOAD_DESCRIPTOR",
      "payloadType": "USAGE",
      "readingType": "SUMMED",
      "units": "KWH"
    }
  ],
  "resources": [
    {
      "resourceName": "meter-KA-98765432",
      "intervalPeriod": {"start": "2026-04-01T00:00:00Z", "duration": "PT24H"},
      "intervals": [
        {
          "id": 0,
          "payloads": [{"type": "USAGE", "values": [25.4]}]
        }
      ]
    }
  ]
}
```

##### Monthly Bill (1mo Interval with Multiple Payloads)
```json
{
  "objectType": "REPORT",
  "reportID": "rep-bill-001",
  "programID": "monthly-billing",
  "reportPayloadDescriptors": [
    {
      "objectType": "REPORT_PAYLOAD_DESCRIPTOR",
      "payloadType": "USAGE",
      "readingType": "SUMMED",
      "units": "KWH"
    },
    {
      "objectType": "REPORT_PAYLOAD_DESCRIPTOR",
      "payloadType": "DEMAND",
      "readingType": "PEAK",
      "units": "KW"
    }
  ],
  "resources": [
    {
      "resourceName": "meter-KA-98765432",
      "intervalPeriod": {"start": "2026-04-01T00:00:00Z", "duration": "P1M"},
      "intervals": [
        {
          "id": 0,
          "payloads": [
            {"type": "USAGE", "values": [750.0]},
            {"type": "DEMAND", "values": [4.2]}
          ]
        }
      ]
    }
  ]
}
```

## 5. Complete Mapping: OBIS Codes & Event IDs to OpenADR 3

This section maps the complete set of standard OBIS codes and Event IDs from the Indian IS 15959 specification to OpenADR 3 as a reference for completeness.

| Category / Indian Specification | Identifier | OpenADR 3 Object | OpenADR 3 Property / payloadType | OpenADR 3 readingType |
| ------------------------------- | ---------- | ---------------- | -------------------------------- | --------------------- |
| Clock (Date & Time)             | `0.0.1.0.0.255` | `REPORT` | Implicitly handled by `intervalPeriod` | N/A |
| Meter Serial Number             | `0.0.96.1.0.255`| `RESOURCE` | `attributes` type: `METER_SERIAL_NO` | N/A |
| Voltage (Phase-Neutral)         | `1.0.12.7.0.255`| `REPORT` | `READING` (Units: V) | `MEAN` / `DIRECT_READ` |
| Phase Current                   | `1.0.11.7.0.255`| `REPORT` | `READING` (Units: A) | `MEAN` / `DIRECT_READ` |
| Neutral Current                 | `1.0.91.7.0.255`| `REPORT` | `READING` (Units: A) | `MEAN` / `DIRECT_READ` |
| Frequency (Hz)                  | `1.0.14.7.0.255`| `REPORT` | `READING` (Units: HZ) | `MEAN` / `DIRECT_READ` |
| Signed Power Factor             | `1.0.13.7.0.255`| `REPORT` | `READING` | `MEAN` / `DIRECT_READ` |
| Active Power (Import)           | `1.0.1.7.0.255` | `REPORT` | `DEMAND` (Units: KW) | `MEAN` |
| Apparent Power (Import)         | `1.0.9.7.0.255` | `REPORT` | `DEMAND` (Units: KVA) | `MEAN` |
| Active Energy (Incremental)     | `1.0.1.29.0.255`| `REPORT` | `USAGE` (Units: KWH) | `DIRECT_READ` |
| Cumulative Energy (Total kWh)   | `1.0.1.8.0.255` | `REPORT` | `USAGE` (Units: KWH) | `SUMMED` |
| Apparent Energy (Incremental)   | `1.0.9.29.0.255`| `REPORT` | `USAGE` (Units: KVAH) | `DIRECT_READ` |
| Cumulative Energy (Total kVAh)  | `1.0.9.8.0.255` | `REPORT` | `USAGE` (Units: KVAH) | `SUMMED` |
| Energy Export (Incremental)     | `1.0.2.29.0.255`| `REPORT` | `EXPORT` (Units: KWH) | `DIRECT_READ` |
| Cumulative Energy (Total kWh-Exp)| `1.0.2.8.0.255`| `REPORT` | `EXPORT` (Units: KWH) | `SUMMED` |
| Reactive Energy Lag (Incremental)| `1.0.5.29.0.255`| `REPORT` | `USAGE` (Units: KVARH) | `DIRECT_READ` |
| Reactive Energy Lag (Total)     | `1.0.5.8.0.255` | `REPORT` | `USAGE` (Units: KVARH) | `SUMMED` |
| Reactive Energy Lead (Incremental)| `1.0.8.29.0.255`| `REPORT` | `USAGE` (Units: KVARH) | `DIRECT_READ` |
| Reactive Energy Lead (Total)    | `1.0.8.8.0.255` | `REPORT` | `USAGE` (Units: KVARH) | `SUMMED` |
| Maximum Demand (kW)             | `1.0.1.6.0.255` | `REPORT` | `DEMAND` (Units: KW) | `PEAK` |
| Maximum Demand (kVA)            | `1.0.9.6.0.255` | `REPORT` | `DEMAND` (Units: KVA) | `PEAK` |
| ToU Zones 1..8 (kWh Import)     | `1.0.1.8.x.255` | `REPORT` | `USAGE` (Differentiated by `readingType` or custom array) | `SUMMED` / `DIRECT_READ` |
| Load Profile Buffer             | `1.0.99.1.0.255`| `REPORT` | Mapped via `duration` (`PT15M`) | N/A |
| Billing Profile Buffer          | `0.0.98.1.0.255`| `REPORT` | Mapped via `duration` (`P1M`) | N/A |
| Daily Profile Buffer            | `1.0.94.91.0.255`| `REPORT` | Mapped via `duration` (`PT24H`) | N/A |
| Tamper / Event Buffer (Various) | `0.0.99.98.x.255`| `REPORT` | `DATA_QUALITY`, `METER_TAMPER`, `POWER_QUALITY` | N/A |
| Event IDs: Voltage Related (1..12) | 1, 3, 11... | `REPORT` | `POWER_QUALITY` (Custom payloadType) | N/A |
| Event IDs: Current/Others (51..70) | 51, 61, 69...| `REPORT` | `POWER_QUALITY` / `DATA_QUALITY` | N/A |
| Event IDs: Power Fail (101..102)| 101, 102 | `REPORT` | `OPERATING_STATE` / `POWER_QUALITY` | N/A |
| Event IDs: Tamper (201..205)    | 201, 205 | `REPORT` | `METER_TAMPER` (Custom payloadType) | N/A |
| Relay Disconnect/Connect        | 301, 302 | `EVENT`  | `CONTROL_SETPOINT` (Values: CONNECT/DISCONNECT) | N/A |
| Disconnect (Overload/Credit)    | 303, 304, 305 | `EVENT` | `IMPORT_CAPACITY_LIMIT` / `CONTROL_SETPOINT` | N/A |
| Token Acceptance/Rejection      | 306, 307 | `EVENT`  | `PROGRAMMING_CONFIG` / `CONTROL_SETPOINT` | N/A |
| Parameters Programming          | 151      | `EVENT`  | `PROGRAMMING_CONFIG` | N/A |

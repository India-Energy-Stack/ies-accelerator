# MeterData v0.6 Reference Guide

This reference guide details standard register mappings, OBIS/Short code definitions, telemetry modes, and physical metering profiles supported by version 0.6 of the India Energy Stack (IES) `MeterData` standard.

---

## 1. Reading vs. Usage Modes

Every telemetry descriptor and value mapped in this schema belongs to one of two modes:

| Mode | Semantic Meaning | Example Application |
|---|---|---|
| **`READING`** | Cumulative value or point-in-time snapshot. Represents a counter value or state at a specific instant. | Cumulative active energy import (register reading at midnight), Phase A voltage snapshot. |
| **`USAGE`** | Consumption or demand calculated over a specified duration (interval). Represents delta or average values. | Interval active energy import block consumption (kWh consumed in a 15-minute window). |

---

## 2. Standard Registry & OBIS Mappings

Below is the canonical catalog of registers mapped between OBIS codes, Short Codes, and their default categories and modes.

### Cumulative Energy Registers
- **Accumulation Behaviour**: `CUMULATIVE`
- **Supported Modes**: `["READING", "USAGE"]` (default `READING`)
- **Unit**: `kWh`, `kVAh`, `kvarh`

| OBIS Code | Short Code | Flow Direction | Category | Meter Categories |
|---|---|---|---|---|
| `1.0.1.8.0.255` | `kWh imp` | IMPORT | `energyCumulative` | A, B, C, D1, D2, D3, D4 |
| `1.0.2.8.0.255` | `kWh exp` | EXPORT | `energyCumulative` | D1, D2, D3, D4 |
| `1.0.9.8.0.255` | `kVAh imp` | IMPORT | `energyCumulative` | D2, D3, D4 |

### Block Incremental Energy Registers
- **Accumulation Behaviour**: `DELTA`
- **Supported Modes**: `["USAGE"]` (default `USAGE`)
- **Unit**: `kWh`, `kVAh`

| OBIS Code | Short Code | Flow Direction | Category | Meter Categories |
|---|---|---|---|---|
| `1.0.1.29.0.255` | `kWh imp block` | IMPORT | `energyIncremental` | D1, D2, D3, D4 |
| `1.0.2.29.0.255` | `kWh exp block` | EXPORT | `energyIncremental` | D1, D2, D3, D4 |
| `1.0.9.29.0.255` | `kVAh imp block` | IMPORT | `energyIncremental` | D2, D4 |

### Maximum Demand Registers
- **Accumulation Behaviour**: `SUMMATION` / `INDICATING`
- **Supported Modes**: `["USAGE"]` (default `USAGE`)
- **Unit**: `kW`, `kVA`
- **Description**: Peak average power demand calculated over an integration period (e.g. `PT30M`). Includes occurrence timestamp (`occurredAt`).

| OBIS Code | Short Code | Flow Direction | Category | Meter Categories |
|---|---|---|---|---|
| `1.0.1.6.0.255` | `MD kW` | IMPORT | `demand` | D2, D4 |
| `1.0.9.6.0.255` | `MD kVA` | IMPORT | `demand` | D2, D4 |

---

## 3. Physical Profiles and Cadence Standards

The schema unifies all time cadences using OpenADR-aligned `intervalPeriod` (consisting of a `start` datetime and ISO-8601 `duration`).

### A. Interval Load Survey (`IntervalProfile`)
- **Cadence**: Typically `PT15M` or `PT30M`.
- **Primary Telemetry Mode**: `USAGE`.
- **OBIS Codes**: `1.0.1.29.0.255` (Active energy block incremental import) or `1.0.9.29.0.255` (Apparent energy block incremental import).

### B. Daily Load Survey (`DailyProfile`)
- **Cadence**: `P1D` (starts at midnight `00:00:00`).
- **Primary Telemetry Mode**: `READING`.
- **OBIS Codes**: `1.0.1.8.0.255` (Active energy cumulative import at midnight reset) or `1.0.2.8.0.255` (Active energy cumulative export).

### C. Monthly Billing Survey (`BillingProfile`)
- **Cadence**: `P1M` (triggered by billing reset date).
- **Primary Telemetry Mode**: Mix of `READING` (cumulative energy) and `USAGE` (Maximum Demand peak average with an integration window).

---

## 4. Formal Reference Specifications

- **IS 15959 (Part 1, 2, 3)**: Indian Standard for AC Static Watt-hour Smart Meters - Data Exchange.
- **DLMS/COSEM (IEC 62056)**: Device Language Message Specification / Companion Specification for Energy Metering.
- **OpenADR 3.0**: Open Automated Demand Response program and report payloads.

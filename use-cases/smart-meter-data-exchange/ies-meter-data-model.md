# IES Meter Data Model

**The reference for how Indian smart-meter terminology — OBIS codes, IS 15959 profile buffers, IS 15959 event IDs, CIM master data — maps onto the [`MeterData`](../../schemas/MeterData/README.md) schema (this page is pinned to the current `v0.6` shape) carried by IES Data Exchange.**

If you are implementing [Smart Meter Data Exchange](README.md), this is the page you keep open while wiring your HES / MDMS to v0.6 payloads.

> `MeterData/v0.6` is the current canonical schema. Earlier drafts of IES used the working name `IES_Report` — treat those references as superseded by `MeterData/v0.6`.

---

## 1. The shape of `MeterData/v0.6` in one glance

A `MeterData/v0.6` payload is a **JSON array** with two kinds of object:

| Object | Role |
|---|---|
| `PayloadDescriptorProfile` | Dictionary — declares `payloadDescriptors[]` (one per quantity: OBIS, readingType, unit, flowDirection, reportedMode) and `compactSequences[]` (column layout for the dense `payloads` matrix). |
| One of the profile objects below | Carries actual readings or events, referencing a descriptor set by name. |

The eight profile shapes:

| Profile | Indian-side equivalent | When it ships |
|---|---|---|
| `CUSTOMER` | CIS / Asset Master / GIS master data | On enrolment, on change |
| `INTERVAL` | IS 15959 Load Profile (`1.0.99.1.0.255`) | 15 / 30-min block load survey |
| `DAILY` | IS 15959 Daily Profile (`1.0.94.91.0.255`) | Once / day |
| `MONTHLY` | IS 15959 Billing Profile (`0.0.98.1.0.255`) | Billing reset (typically month-end) |
| `BILL_DETAILS` | Utility-side billing computed details | On bill finalisation |
| `INSTANTANEOUS` | OBIS `1.0.x.7.0.255` real-time registers | On poll / push |
| `EVENT` | IS 15959 Event Log Profiles (`0.0.99.98.x.255`) | On event + scheduled pull |
| `ALARM` | Real-time alarms (tamper / overload / low credit) | On occurrence |

OBIS codes are first-class in v0.6 — they sit inside `payloadDescriptors[].obis` as a string verbatim from the meter. The schema does not translate them, so the mapping below is mostly about *which profile a given OBIS belongs in* and *which `readingType` / `unit` / `reportedMode` to advertise*.

The canonical, machine-readable OBIS catalogue ships as [`IES codes.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/IES%20codes.json) (GitHub Pages, served raw) under [`schemas/MeterData/v0.6/`](../../schemas/MeterData/v0.6/README.md) — each entry pins `obis`, `name`, `category`, `profiles[]`, `supportedModes[]`, `meterCategories[]`, and the IS 15959 source. **That file is the source of truth.** The tables on this page are the human-readable summary; if a mapping looks wrong, the JSON wins. Browse the source on [GitHub](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterData/v0.6/IES%20codes.json).

---

## 2. IS 15959 profile buffer → `MeterData/v0.6` profile

The Indian Load Profile / Daily Profile / Billing Profile buffers map one-to-one to v0.6 profile shapes. The `intervalPeriod.duration` distinguishes cadence.

| IS 15959 profile (OBIS) | Typical period | `MeterData/v0.6` profile | `intervalPeriod.duration` |
|---|---|---|---|
| Load Profile (`1.0.99.1.0.255`) | 15 / 30 min | `INTERVAL` | `PT15M` / `PT30M` |
| Daily Profile (`1.0.94.91.0.255`) | 24 h | `DAILY` | `PT24H` |
| Billing Profile (`0.0.98.1.0.255`) | Monthly | `MONTHLY` | `P1M` |
| Voltage / Current event buffers (`0.0.99.98.0.255` / `.1.255`) | Event-driven | `EVENT` | `timePeriod` window |
| Power-failure / Tamper / Control buffers (`0.0.99.98.2.255` / `.4.255` / `.5.255`) | Event-driven | `EVENT` (POWER_FAIL etc.) / `ALARM` (tamper / control) | `timePeriod` window |
| Real-time registers (`1.0.x.7.0.255`) | Polled / pushed | `INSTANTANEOUS` | Point-in-time |

---

## 3. OBIS register → `payloadDescriptors[]`

For each profile, the OBIS register is carried in `payloadDescriptors[].obis` and qualified with `readingType`, `unit`, `flowDirection`, and `reportedMode` (`USAGE` / `READING` / `DEMAND`).

### 3.1 Energy registers — Load / Daily / Monthly

| Quantity | OBIS (block incremental) | OBIS (cumulative) | Unit | flowDirection | reportedMode | Goes in profile |
|---|---|---|---|---|---|---|
| Active energy import | `1.0.1.29.0.255` | `1.0.1.8.0.255` | kWh | `IMPORT` | `USAGE` | `INTERVAL` / `DAILY` / `MONTHLY` |
| Active energy export | `1.0.2.29.0.255` | `1.0.2.8.0.255` | kWh | `EXPORT` | `USAGE` | `INTERVAL` / `DAILY` / `MONTHLY` |
| Apparent energy import | `1.0.9.29.0.255` | `1.0.9.8.0.255` | kVAh | `IMPORT` | `USAGE` | `INTERVAL` / `DAILY` / `MONTHLY` |
| Reactive energy (lag) | `1.0.5.29.0.255` | `1.0.5.8.0.255` | kVArh | `IMPORT` | `USAGE` | `INTERVAL` / `MONTHLY` |
| Reactive energy (lead) | `1.0.8.29.0.255` | `1.0.8.8.0.255` | kVArh | `EXPORT` | `USAGE` | `INTERVAL` / `MONTHLY` |
| ToU import (Zones 1..8) | — | `1.0.1.8.<z>.255` | kWh | `IMPORT` | `USAGE` | `MONTHLY` |
| Maximum demand (kW) | — | `1.0.1.6.0.255` | kW | `IMPORT` | `DEMAND` | `MONTHLY` |
| Maximum demand (kVA) | — | `1.0.9.6.0.255` | kVA | `IMPORT` | `DEMAND` | `MONTHLY` |

### 3.2 Instantaneous registers

| Quantity | OBIS | Unit | reportedMode | Profile |
|---|---|---|---|---|
| Voltage (phase-neutral) | `1.0.12.7.0.255` | V | `READING` | `INSTANTANEOUS` |
| Phase current | `1.0.11.7.0.255` | A | `READING` | `INSTANTANEOUS` |
| Neutral current | `1.0.91.7.0.255` | A | `READING` | `INSTANTANEOUS` |
| Frequency | `1.0.14.7.0.255` | Hz | `READING` | `INSTANTANEOUS` |
| Signed power factor | `1.0.13.7.0.255` | — | `READING` | `INSTANTANEOUS` |
| Active power (import) | `1.0.1.7.0.255` | kW | `DEMAND` | `INSTANTANEOUS` |
| Apparent power (import) | `1.0.9.7.0.255` | kVA | `DEMAND` | `INSTANTANEOUS` |

### 3.3 Identification registers — `CUSTOMER` profile

| Field | OBIS | Goes in |
|---|---|---|
| Meter serial number | `0.0.96.1.0.255` | `CUSTOMER` |
| Manufacturer name | `0.0.96.1.1.255` | `CUSTOMER` |
| Device ID | `0.0.96.1.2.255` | `CUSTOMER` (D1 / D2 meter categories) |
| Firmware version | `1.0.0.2.0.255` | `CUSTOMER` |
| Clock (real-time) | `0.0.1.0.0.255` | Implicitly handled by `intervalPeriod` / `timestamp` |

---

## 4. IS 15959 Event IDs → `EVENT` / `ALARM`

Events carry `eventId` (numeric, IS 15959) and a human-readable `eventName` directly. Examples are in [`schemas/MeterData/v0.6/examples/EventProfile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterData/v0.6/examples/EventProfile.json).

| Event ID (occur) | Event ID (restore) | Description | Category | Profile |
|---|---|---|---|---|
| 1 | 2 | Phase-to-neutral under-voltage | Voltage | `EVENT` |
| 3 | 4 | Phase-to-neutral over-voltage | Voltage | `EVENT` |
| 11 | 12 | Phase missing | Voltage | `EVENT` |
| 51 | 52 | Phase current unbalance | Current | `EVENT` |
| 61 | 62 | CT reverse | Current | `EVENT` |
| 69 | 70 | Neutral disturbance | Current / others | `EVENT` |
| 101 | 102 | Power failure / power up | Power | `EVENT` |
| 151 | — | Parameters programming (config change) | Transaction | `EVENT` |
| 201 | 202 | Magnetic interference | Tamper | `ALARM` (active) / `EVENT` (logged) |
| 205 | — | Meter cover open (non-restorable) | Tamper | `ALARM` |
| 301 | 302 | Relay disconnect / connect (manual) | Control | `EVENT` |
| 303 | — | Relay disconnect (overload) | Control | `EVENT` / `ALARM` |
| 304 | — | Relay disconnect (low credit) | Control | `ALARM` |
| 305 | — | Relay disconnect (tamper auto-cutoff) | Control | `ALARM` |
| 306 | 307 | Token acceptance / rejection (prepaid) | Control | `EVENT` |

`EVENT` profiles can carry the IS 15959 magnitude and duration directly (`magnitude`, `duration`); `ALARM` profiles are state-based (active / cleared) and intended for real-time pushes.

---

## 5. Data quality — `validationStatus`

v0.6 carries per-reading validation via the `overrides[]` block on a profile entry. Each override pins the `descriptorIndex` it qualifies, the `validationStatus`, the `source`, an optional `changeMethod`, and a `failCode`.

| `validationStatus` | Meaning |
|---|---|
| `VALID` | Read direct from the meter; no estimation |
| `ESTIMATED` | Filled by VEE / interpolation |
| `MISSING` | No value available; the entry exists to preserve the interval index |
| `BAD` | Value present but flagged as out-of-range / suspect |

Example fragment from `IntervalProfile.json`:

```json
{ "id": 2, "payloads": [ 5.21, 0.12 ],
  "overrides": [{ "descriptorIndex": 0, "validationStatus": "ESTIMATED",
                  "source": "ESTIMATED", "changeMethod": "linear-interpolation",
                  "failCode": "VEE-MISSING-INTERVAL" }] }
```

---

## 6. CIM master data → `CUSTOMER` profile

The CIM (IEC 61968-1 / 61968-9) master data the AMI deployment requires lands in the `CUSTOMER` profile. Use `[BaseProfile].meterRefs[]`, `serviceDeliveryPointRefs[]`, `customerRefs[]` for the relational keys, and `attributes` for the descriptive payload.

| CIM area | Key fields | Source system | Reference in `CUSTOMER` |
|---|---|---|---|
| Asset master | Meter Serial, Make, Model, Hardware / Firmware, CT / PT ratios | Inventory / ERP | `meterRefs[]` + `attributes` |
| Consumer master | CA number, name, address, category (DS / NDS), sanctioned load | CIS / billing | `customerRefs[]` + linked [ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md) `customerProfile` |
| Network master | Substation, Feeder, DT, Pole, Phase | GIS | `attributes` (FEEDER_ID, DT_ID, SUBSTATION_ID, POLE_ID, PHASE) |
| Tariff master | ToU slots, slabs, fixed charges | Billing system | Out of band of MeterData; carried by `MeterServiceProfile` inside [ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md) |

When an OBIS reading arrives, the receiving MDM matches it via `meterRefs[]` → asset → consumer → network → tariff. The `serviceDeliveryPointRefs[]` value is the "service point" object that ties the three together (CIM IEC 61968-9 `UsagePoint`).

---

## 7. Worked example — 30-minute Load Survey

The full schema-validating example is at [`schemas/MeterData/v0.6/examples/IntervalProfile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterData/v0.6/examples/IntervalProfile.json). The shape:

1. One `PayloadDescriptorProfile` declares `IntervalLoadSurveySet` with `kWh imp block` (OBIS `1.0.1.29.0.255`) and `kWh exp block` (OBIS `1.0.2.29.0.255`).
2. One `IntervalProfile` references the descriptor set, carries `intervalPeriod` (`start`, `duration: PT30M`), and packs each interval into a tight `payloads: [imp, exp]` array.
3. Quality overrides ride alongside, addressing the descriptor by index.

This is the minimal pattern. Daily / Monthly / Instantaneous / Event / Alarm follow the same descriptor-then-profile shape; their examples sit alongside in `schemas/MeterData/v0.6/examples/`.

---

## 8. References

- [`MeterData`](../../schemas/MeterData/README.md) — schema, examples, user guide, reference guide (mappings on this page are pinned to `v0.6`)
- [`IES codes.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/IES%20codes.json) — canonical OBIS catalogue (machine-readable). Source on [GitHub](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterData/v0.6/IES%20codes.json).
- [Smart Meter Data Exchange](README.md) — the use case that carries this payload
- [Data Exchange](../../what-ies-provides/data-exchange/README.md) — the wire that carries it
- [`MeterDataRequest`](../../schemas/MeterDataRequest/README.md) — the matching request schema (current: `v0.6`)
- [`MeterDataRequestCredential`](../../schemas/MeterDataRequestCredential/README.md) — optional authorisation VC (current: `v0.1`)
- [`ElectricityCredential`](../../schemas/ElectricityCredential/README.md) — sits alongside `MeterData` for the slow-changing customer / asset / service-connection data (current: `v1.2`)

---

## Appendix — IS 15959 deep reference

This appendix is the full IS 15959 source-of-truth survey (formerly published as a standalone page). Use it to verify the mappings above against the underlying Indian standard.

### A1. Profile buffers

| Profile type | OBIS | Integration period | Mandatory capture sequence (typical) |
|---|---|---|---|
| Load Profile | `1.0.99.1.0.255` | 15 / 30 min | Clock, kWh Imp, kVAh Imp, Avg Voltage, Avg Current |
| Billing Profile | `0.0.98.1.0.255` | Monthly | Billing Date, Total kWh, Total kVAh, MD kW, MD kVA, ToU registers |
| Daily Profile | `1.0.94.91.0.255` | Daily (24 h) | Clock (midnight), Cumulative kWh, Cumulative kVAh |

### A2. Event log buffers

| Category | OBIS profile | Event types |
|---|---|---|
| Voltage | `0.0.99.98.0.255` | Under-voltage, over-voltage, phase missing |
| Current | `0.0.99.98.1.255` | Unbalance, CT reverse, neutral disturbance |
| Power failure | `0.0.99.98.2.255` | Power ON / OFF logs with timestamps |
| Transaction | `0.0.99.98.3.255` | Programming, date change, relay operation |
| Others / tamper | `0.0.99.98.4.255` | Magnetic interference, cover open |
| Control | `0.0.99.98.5.255` | Load-limit changes, relay triggers (prepaid) |

### A3. Communication flow

**Polling (HES → meter):** Association Request (AARQ) → HLS authentication (AES-GCM-128, Security Suite 0) → Selective Read of `profile_generic` by range → meter responds with `compact-array` → Release (RLRQ).

**Push (meter → HES → MDM):** Critical events (tamper / power-fail) are pushed via the PUSH Setup Object (`0.0.25.9.0.255`). Routine logs are fetched during the daily scheduled read. HES converts raw OBIS to an IEC 61968-9 message for the MDM.

**Control (MDM → HES → meter):** MDM issues `Disconnect` request via Northbound REST / SOAP → HES authenticates with meter, sends `ACTION` to Relay Control Object (`0.0.96.3.10.255`) → HES reads Relay Status to confirm → Feedback relayed to MDM.

### A4. Network topology assumed by AT&C-loss accounting

- **Substation / Feeder level** — high-accuracy meters (Class 0.2s / 0.5s) on the outgoing 11 kV / 33 kV lines.
- **DT (LV side) level** — meters at the DTR for energy accounting.
- **Consumer level** — 1-phase or 3-phase end-user meters.

GIS holds Feeder ↔ DT and DT ↔ Consumer mappings; MDM stores them. The `CUSTOMER` profile carries the relevant identifiers via its `attributes` block (FEEDER_ID, DT_ID, SUBSTATION_ID, POLE_ID, PHASE).

### A5. IS 15959 annexure summary

| Annexure | Subject | Detail |
|---|---|---|
| A | Data types | Mandates `double-long-unsigned` for energy to avoid overflow |
| B | OBIS mapping | Master list for 1-phase, 3-phase, CT / PT meters |
| C | Load profile | Standardises the sequence of capture objects |
| D | Event IDs | Canonical 8-bit list (1–255) |
| E | Billing logic | Auto-reset (midnight of 1st) and MD reset behaviour |
| F | Security | Security Suite 0 requirements for AMI |
| G | Smart features | Protocols for firmware image transfer and PUSH parameters |

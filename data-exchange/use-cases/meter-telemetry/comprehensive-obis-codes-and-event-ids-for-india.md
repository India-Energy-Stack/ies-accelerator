# Comprehensive OBIS Codes & Event IDs for India

## Comprehensive OBIS Codes & Event IDs for India (IS 15959 Adaptation)

This document details the data objects and identifiers mandated by the Bureau of Indian Standards (BIS) for Smart and Static Meters in the Indian Power Sector, incorporating IS 15959 Parts 1, 2, and 3.

### 1. Core OBIS Codes (Registers & Profiles)

#### 1.1 General and Instantaneous Parameters

These parameters provide the real-time state of the meter and are critical for monitoring grid health and detecting immediate tamper attempts.

| **Category**      | **OBIS Code**    | **Data Object Name**    | **Purpose / Brief Use**                           | **Standard Reference** |
| ----------------- | ---------------- | ----------------------- | ------------------------------------------------- | ---------------------- |
| **General**       | `0.0.1.0.0.255`  | Clock (Date & Time)     | Real-time clock for timestamping profiles/events. | Part 1, 2, 3           |
| **General**       | `0.0.96.1.0.255` | Meter Serial Number     | Unique identifier for asset management.           | Part 1, 2, 3           |
| **Instantaneous** | `1.0.12.7.0.255` | Voltage (Phase-Neutral) | Real-time RMS voltage for monitoring.             | Part 1, 2              |
| **Instantaneous** | `1.0.11.7.0.255` | Phase Current           | Real-time line current measurement.               | Part 1, 2              |
| **Instantaneous** | `1.0.91.7.0.255` | Neutral Current         | Monitoring for neutral unbalance or theft.        | Part 2 (Smart)         |
| **Instantaneous** | `1.0.14.7.0.255` | Frequency (Hz)          | System frequency monitoring.                      | Part 1, 2, 3           |
| **Instantaneous** | `1.0.13.7.0.255` | Signed Power Factor     | Total signed power factor (Lag/Lead).             | Part 1, 2              |
| **Instantaneous** | `1.0.1.7.0.255`  | Active Power (Import)   | Real-time Active Power (kW).                      | Part 1, 2              |
| **Instantaneous** | `1.0.9.7.0.255`  | Apparent Power (Import) | Real-time Apparent Power (kVA).                   | Part 1, 2              |

#### 1.2 Energy and Demand Registers (Cumulative)

| **Category** | **OBIS Code**   | **Data Object Name**        | **Purpose / Brief Use**                         | **Standard Reference** |
| ------------ | --------------- | --------------------------- | ----------------------------------------------- | ---------------------- |
| **Energy**   | `1.0.1.8.0.255` | Cumulative Energy (kWh)     | Billing determinant for active energy import.   | Part 1, 2, 3           |
| **Energy**   | `1.0.9.8.0.255` | Cumulative Energy (kVAh)    | Billing determinant for apparent energy import. | Part 1, 2, 3           |
| **Energy**   | `1.0.2.8.0.255` | Cumulative Energy (kWh-Exp) | For Net-Metering / Solar export measurement.    | Part 2 (Smart)         |
| **Energy**   | `1.0.5.8.0.255` | Reactive Energy (Lag)       | Reactive energy (kVARh Lag).                    | Part 1, 3              |
| **Energy**   | `1.0.8.8.0.255` | Reactive Energy (Lead)      | Reactive energy (kVARh Lead).                   | Part 1, 3              |
| **Demand**   | `1.0.1.6.0.255` | Maximum Demand (kW)         | Peak active demand during the billing cycle.    | Part 1, 2              |
| **Demand**   | `1.0.9.6.0.255` | Maximum Demand (kVA)        | Peak apparent demand during the billing cycle.  | Part 1, 2              |

#### 1.3 Time-of-Use (ToU) Registers

ToU zones allow for differential pricing. India typically mandates up to 8 slots.

| **Parameter**    | **OBIS Code**   | **Data Object Name** | **Purpose**                                       |
| ---------------- | --------------- | -------------------- | ------------------------------------------------- |
| **ToU Zone 1**   | `1.0.1.8.1.255` | kWh Import - T1      | Active energy consumed in Zone 1.                 |
| **ToU Zone 2**   | `1.0.1.8.2.255` | kWh Import - T2      | Active energy consumed in Zone 2.                 |
| **ToU Zone 3**   | `1.0.1.8.3.255` | kWh Import - T3      | Active energy consumed in Zone 3.                 |
| **ToU Zone 4**   | `1.0.1.8.4.255` | kWh Import - T4      | Active energy consumed in Zone 4.                 |
| **ToU Apparent** | `1.0.9.8.x.255` | kVAh Import - Tx     | Corresponding apparent energy zones (x = 1 to 8). |

### 2. Profile Buffers & Capture Logic

Profile buffers act as a historical log. They store a sequence of "Capture Objects" at defined intervals.

| **Profile Type**    | **OBIS Code**     | **Integration Period** | **Mandatory Capture Sequence (Typical)**                                            |
| ------------------- | ----------------- | ---------------------- | ----------------------------------------------------------------------------------- |
| **Load Profile**    | `1.0.99.1.0.255`  | 15 / 30 Min            | 1. Clock, 2. kWh Imp, 3. kVAh Imp, 4. Avg Voltage, 5. Avg Current                   |
| **Billing Profile** | `0.0.98.1.0.255`  | Monthly                | 1. Billing Date, 2. Total kWh, 3. Total kVAh, 4. MD kW, 5. MD kVA, 6. ToU Registers |
| **Daily Profile**   | `1.0.94.91.0.255` | Daily (24h)            | 1. Clock (Midnight), 2. Cumulative kWh, 3. Cumulative kVAh                          |

### 3. Event Log Profiles & Event IDs

Events are stored in specific profile buffers. The **Event ID** identifies the specific occurrence.

#### 3.1 Event Profile Identifiers (OBIS)

| **Category**        | **OBIS Profile Code** | **Type of Events**                            |
| ------------------- | --------------------- | --------------------------------------------- |
| **Voltage Related** | `0.0.99.98.0.255`     | Under voltage, Over voltage, Phase missing.   |
| **Current Related** | `0.0.99.98.1.255`     | Unbalance, CT Reverse, Neutral disturbance.   |
| **Power Failure**   | `0.0.99.98.2.255`     | Power ON/OFF logs with timestamps.            |
| **Transaction**     | `0.0.99.98.3.255`     | Programming, Date change, Relay operation.    |
| **Others/Tamper**   | `0.0.99.98.4.255`     | Magnetic interference, Cover open.            |
| **Control Events**  | `0.0.99.98.5.255`     | Load Limit changes, Relay triggers (Prepaid). |

#### 3.2 Standardized Event IDs (India Specific)

| **ID (Occur)** | **ID (Restore)** | **Description**                        | **Category**   |
| -------------- | ---------------- | -------------------------------------- | -------------- |
| **1**          | **2**            | Phase-to-Neutral Under Voltage         | Voltage        |
| **3**          | **4**            | Phase-to-Neutral Over Voltage          | Voltage        |
| **11**         | **12**           | Phase Missing                          | Voltage        |
| **51**         | **52**           | Phase Current Unbalance                | Current        |
| **61**         | **62**           | CT Reverse                             | Current        |
| **69**         | **70**           | Neutral Disturbance                    | Current/Others |
| **101**        | **102**          | Power Failure                          | Power Fail     |
| **151**        | -                | Parameters Programming (Config change) | Transaction    |
| **201**        | **202**          | Magnetic Interference                  | Tamper         |
| **205**        | -                | Meter Cover Open (Non-restorable)      | Tamper         |

#### 3.3 Prepaid & Control Specific Event IDs

| **Event ID** | **Event Description**            | **Logical Trigger**              |
| ------------ | -------------------------------- | -------------------------------- |
| **301**      | Relay Disconnect (Manual/Remote) | Commanded via HES.               |
| **302**      | Relay Connect (Manual/Remote)    | Commanded via HES.               |
| **303**      | Relay Disconnect (Overload)      | Threshold `0.0.14.0.0` exceeded. |
| **304**      | Relay Disconnect (Low Credit)    | Balance reached zero.            |
| **305**      | Relay Disconnect (Tamper)        | Auto-cutoff due to fraud.        |
| **306**      | Token Acceptance Success         | Valid STS token entered.         |
| **307**      | Token Rejection                  | Invalid token attempt.           |

### 4. Communication and Reporting Flow

#### 4.1 HES-to-Meter Access Sequence (Polling)

1. **Association Request:** HES sends AARQ to establish a session.
2. **Authentication:** Smart Meters mandate **HLS (High Level Security)** using AES-GCM-128 (Security Suite 0).
3. **Selective Read:** HES reads the `profile_generic` object using "Selective Access" (by range) to fetch only specific time-slices.
4. **Data Delivery:** Meter sends data as a `compact-array`.
5. **Release:** HES sends RLRQ to close the session.

#### 4.2 Reporting Events (Meter → HES → MDM)

* **PUSH:** Critical events (Tamper/Power Out) are pushed immediately via the **PUSH Setup Object** (`0.0.25.9.0.255`).
* **PULL:** Routine logs are fetched during the daily scheduled read.
* **Translation:** HES converts the raw OBIS data into an **IEC 61968-9 Message** (CIM based) for the MDM.

#### 4.3 Control Logic (MDM → HES → Meter)

1. **MDM Trigger:** MDM issues a `Disconnect` request via Northbound API (REST/SOAP).
2. **HES Command:** HES authenticates with the meter and sends an `ACTION` to the **Relay Control Object** (`0.0.96.3.10.255`).
3. **Verification:** HES reads the **Relay Status** to confirm physical state change.
4. **Feedback:** Success/Failure is relayed back to MDM to update billing and customer portals.

### 5. IS 15959 Annexures Summary

| **Annexure**   | **Subject**        | **Purpose / Detail**                                          |
| -------------- | ------------------ | ------------------------------------------------------------- |
| **Annexure A** | **Data Types**     | Mandates `double-long-unsigned` for energy to avoid overflow. |
| **Annexure B** | **OBIS Mapping**   | Master list for 1-Phase, 3-Phase, and CT/PT meters.           |
| **Annexure C** | **Load Profile**   | Standardizes the sequence of capture objects.                 |
| **Annexure D** | **Event IDs**      | Canonical 8-bit list (1-255) for all events.                  |
| **Annexure E** | **Billing Logic**  | Defines Auto-reset (midnight of 1st) and MD Reset behavior.   |
| **Annexure F** | **Security**       | Specifies Security Suite 0 requirements for AMI.              |
| **Annexure G** | **Smart Features** | Protocols for image transfer (firmware) and PUSH parameters.  |

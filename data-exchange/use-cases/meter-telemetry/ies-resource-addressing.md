# IES Resource Addressing (Proposal for Review)

> [!NOTE]
> This addressing scheme proposal was utilized and demonstrated by **Trielectric Energy** in the Data Exchange Bootcamp to issue access credentials.

This document defines the addressing scheme for grid resources within the India Energy Stack (IES). It provides a standardized way to identify, locate, and group resources—from national interconnects down to behind-the-meter Distributed Energy Resources (DERs).

## 1. Core Principles

To ensure interoperability and scalability, the IES addressing scheme follows three core principles:

1.  **Global Uniqueness**: Every resource must have an address that is unique across the entire Indian grid.
2.  **Topology Independence (Stability)**: A resource should have a "Logical Address" that remains unchanged even if its physical connection point (topology) is altered.
3.  **Decentralized Governance**: Naming authority is delegated. For example, `/IN/BESCOM` is managed by BESCOM, and they are responsible for ensuring uniqueness within their sub-tree.

---

## 2. Hierarchical Grid Paths (Topology-based)

The hierarchy follows the natural graph topology of the electricity grid. These are **Physical Addresses** and describe *where* a resource is connected.

### 2.1 Absolute Path Structure
An absolute path starts from the country root (`/IN`) and descends through regional, state, and utility layers down to the specific asset.

**Syntax:**
`/IN/[REGION]/[STATE]/[UTILITY]/[SUBSTATION]/[FEEDER]/[DT]/[METER]/[DER]`

**Example:**
`/IN/SR/KA/BESCOM/STN-IND-01/FDR-04/DT-22/MTR-98765/INV-01`

### 2.2 Relative Paths
Within a specific context (e.g., inside BESCOM's network), relative paths can be used to simplify internal communication.

**Example:**
*   Context: `/IN/SR/KA/BESCOM`
*   Relative Path: `./STN-IND-01/FDR-04`

---

## 3. Stable Logical Addressing

While Physical Paths change during grid maintenance (e.g., transferring a consumer from Feeder A to Feeder B), the **Logical Address** remains constant. This is the "permanent home" for the resource's identity.

### 3.1 Logical URI Syntax
Logical addresses use the `ies://` scheme and are typically anchored to the primary owner or a global registry.

**Example:**
`ies://BESCOM/meters/MTR-98765`

### 3.2 Topology Mapping
A resource definition includes both its Logical Address and its current Physical Path(s).

```json
{
  "id": "ies://BESCOM/meters/MTR-98765",
  "resourceName": "Main_Service_Meter",
  "attributes": [
    {
      "type": "PHYSICAL_PATH",
      "values": ["/IN/SR/KA/BESCOM/STN-01/FDR-04/DT-22"]
    },
    {
      "type": "METER_SERIAL_NO",
      "values": ["BES-98765432"]
    }
  ]
}
```

---

## 4. Addressing Groups & Wildcards

The IES addressing scheme supports powerful query mechanisms to address sets of resources simultaneously.

### 4.1 Wildcard Conventions
*   `*` (Single Level): Addresses all direct children of a node.
    *   `/IN/SR/KA/BESCOM/STN-01/*` addresses all Feeders connected to Substation 01.
*   `**` (Recursive): Addresses all descendants at any depth.
    *   `/IN/SR/KA/BESCOM/STN-01/**` addresses all Feeders, DTs, and Meters under Substation 01.

### 4.2 Pattern Matching
*   **Specific ID Find**: `/**/MTR-98765` finds the meter regardless of its current feeder or substation.
*   **Aggregate Only**: A path without a wildcard refers to the node itself.
    *   `/IN/SR/KA/BESCOM/STN-01` refers to the Substation (to query its transformer health, etc.) without including the downstream meters.

### 4.3 Depth Limitation
Access can be limited by depth to prevent massive "tree-walk" queries that impact performance.
*   `GET /resources?root=/IN/SR/KA/BESCOM/STN-01&depth=2` returns Feeders and DTs, but stops before reaching Meters.

---

## 5. Virtual Groups & VPPs

Virtual groups allow for the creation of logical overlays that do not follow the physical topology. These are used for Virtual Power Plants (VPPs), community solar programs, or application-specific cohorts.

**Syntax:**
`/GROUPS/[GROUP_NAME]` or `/VPP/[VPP_ID]`

**Example VPP Definition:**
```json
{
  "id": "/VPP/Bangalore-Residential-DR",
  "objectType": "RESOURCE_GROUP",
  "members": [
    "ies://BESCOM/meters/MTR-101",
    "ies://BESCOM/meters/MTR-202",
    "ies://KPTCL/stations/STN-05"
  ]
}
```

---

## 6. Decentralized Discovery (The "Grid DNS")

IES uses a federated resolution mechanism. When a system encounters an address like `/IN/SR/KA/BESCOM/...`, it follows a discovery chain:

1.  **Root Discovery**: Query the National Registry for `/IN`.
2.  **Delegation**: The National Registry points to the Regional/State Registry.
3.  **Utility Resolution**: The State Registry identifies that `BESCOM` is responsible for the sub-path and provides the API endpoint for BESCOM's Resource Discovery service.

This allows utilities to manage their own internal infrastructure without needing to synchronize every small change to a central national database.

---

## 7. Use Case Examples

### Example 1: Requesting data for an entire Feeder
**Query:** `GET /telemetry?target=/IN/SR/KA/BESCOM/STN-01/FDR-04/**`
**Result:** Aggregated or individual telemetry for every DT and Meter on Feeder 04.

### Example 2: Addressing a Substation for Maintenance
**Query:** `GET /resources/ies://BESCOM/stations/STN-01`
**Result:** Configuration data for the substation asset itself (transformer ratings, firmware version).

### Example 3: VPP Dispatch
**Action:** `POST /events/ies://VPP/Solar-Export-Group/events`
**Result:** Dispatches a power export request to all members of the virtual solar group.

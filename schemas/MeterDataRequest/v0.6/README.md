> **Files** — [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/attributes.yaml) · [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/schema.json) · [context.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/context.jsonld) · [vocab.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/vocab.jsonld) · [examples/](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/examples)

# MeterDataRequest v0.6

This directory contains the schemas, context mapping, and vocabularies for querying smart meter telemetry and profiles. In version 0.6, the request layer has been split into three distinct, composable models:
1. **MeterDataCapabilities**
2. **MeterDataAuthorisation**
3. **MeterDataRequest**

---

## 1. MeterDataCapabilities

Represents the data sharing capabilities supported by a meter data provider (e.g. DISCOM). It acts as the blueprint of what data points are available, specifying what profile types, register keys, telemetry modes, and query boundaries are supported.

* **Main Schema**: `schema.json#/$defs/MeterDataCapabilities`
* **JSON-LD Type**: `ies:MeterDataCapabilities`
* **Link to Example**: [`Capabilities_Example.json`](./examples/Capabilities_Example.json)

---

## 2. MeterDataAuthorisation

Represents the cryptographic or digital grant/token allowing an entity (such as a Technical Service Provider) to access a specific subset of data capabilities. It defines:
- **`grantor`**: The authorizing entity (e.g. Utility/DISCOM).
- **`grantee`**: The authorized entity (e.g. TSP).
- **`purpose`**: The explicit reason for accessing the data (e.g. ESG reporting).
- **`validFrom` / `validUntil`**: The validity period.
- **`capabilities`**: The allowed `MeterDataCapabilities` object.

* **Main Schema**: `schema.json#/$defs/MeterDataAuthorisation`
* **JSON-LD Type**: `ies:MeterDataAuthorisation`
* **Link to Example**: [`Authorisation_Example.json`](./examples/Authorisation_Example.json)

---

## 3. MeterDataRequest

Represents the actual data query payload sent by the authorized entity to pull telemetry. It contains query criteria and proves authorization and user consent:
- **`consumers`** (optional): List of target consumer DIDs/URIs.
- **`resources`** (optional): List of target meter serials or service point URIs.
- **`scope`**: Hierarchy of query (`ResourceOnly`, `ResourceAndChildren`, `ChildrenOnly`).
- **`from` / `duration`**: The start and duration of the query time window.
- **`consumerConsent`** (optional): Array of consumer consent DIDs or receipt hashes.
- **`authorisation`**: Inline `MeterDataAuthorisation` object or URL pointing to the grant.
- **`capabilitiesRequested`**: The requested `MeterDataCapabilities` subset.

* **Main Schema**: `schema.json` (root schema)
* **JSON-LD Type**: `ies:MeterDataRequest`
* **Link to Example**: [`Request_Example.json`](./examples/Request_Example.json)

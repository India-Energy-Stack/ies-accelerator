# Tariff Intelligence

**Tariff orders, time-of-day surcharges, deviation penalties, and data-exchange rules published as machine-readable *policy-as-code* — consumable by billing systems, consumer apps, smart meters, and analytics agents directly.**

---

## Scenario

A SERC issues a tariff order today as a PDF. Every DISCOM in that state then manually transcribes the rate slabs, time-of-day surcharges, fixed charges, and category definitions into its billing system. Consumer-side apps (bill estimators, EV charging planners, rooftop-solar payback calculators) each interpret the same order independently. Drift, ambiguity, and bugs are inevitable.

The same problem applies more broadly than tariff orders. Any **policy** that the energy sector needs to interpret consistently — sanctioned-load deviation penalties, peak-hour incentives, DR program participation rules, data-quality SLAs for AMISP reporting, public-disclosure thresholds — benefits from being published once, as code, by the issuing authority.

The Tariff Intelligence use case packages this as `IES_Policy` artefacts. The SERC (or any policy issuer) publishes machine-readable policy alongside the regulatory order; DISCOMs, apps, and meters ingest it directly with no re-keying and no interpretation drift. Issuers may publish policy in the public data exchange, or hand it inline during a private data exchange to set the terms of that exchange.

---

## Actors and Roles

| Role | Organisation (example) | What they do |
|---|---|---|
| **BPP** — policy publisher | SERC (e.g. MERC), or any policy authority (utility, regulator) | Publishes the signed `IES_Policy` artefact |
| **BAP** — policy consumer | DISCOM billing system, consumer-app developer, smart meter firmware, analytics agent | Subscribes to and ingests the policy |
| **Identity authority** | IES registries | The publisher's `did:web` is the trust anchor for the signed policy |

Publication is typically open under public-disclosure norms (settlement value `0` in the example payloads), so the policy consumer set is unrestricted — every billing implementation in the state can subscribe.

---

## Building Blocks Used

| Block | Role in this use case |
|---|---|
| [Identifiers](../identifiers/README.md) | The `policyID` (e.g. `MUM-RES-T1`) is an IES identifier; the policy is bound to the publisher's `did:web` and references the `programID` of the regulatory program (consumer category, tariff scheme) it belongs to. |
| [Registries](../registries/README.md) | The publishing SERC/utility is looked up in the IES Regulators or DISCOMs reference registry to obtain its public key for signature verification. |
| [Data Exchange](../data-exchange/README.md) | Policies are distributed over the same Beckn-based protocol used for telemetry and filings. Policies may flow in the public data exchange, or be carried inline as part of a private data exchange to negotiate that exchange's terms. |
| [Energy Credentials](../energy-credentials/README.md) | *Not used to carry the policy itself.* Credentials enter when a downstream agent needs to prove its tariff category or sanctioned load to a billing-time policy engine — that's the [Consumer Energy Passport](../energy-credentials/README.md) flow. |

---

## The Dataset — `IES_Policy`

The `IES_Policy` schema captures policy as structured, signed JSON-LD. For tariffs, a single `IES_Policy` object carries:

- **Identity** — `id`, `policyID`, `policyName`, `policyType` (`TARIFF` or `DISPATCH_GUIDE`), `programID` linking to an `IES_Program`.
- **Validity** — `samplingInterval` as an ISO 8601 recurrence pattern (e.g. `R/2024-04-10T00:00:00Z/P1M` — re-evaluated monthly from April 10, 2024).
- **`energySlabs[]`** — progressive consumption tiers, each `{ id, start (kWh, inclusive), end (kWh, exclusive or null for open-ended), price }`.
- **`surchargeTariffs[]`** — time-of-day adjustments, each `{ id, recurrence, interval (ToD start + duration), value, unit (`PERCENT` or `INR_PER_KWH`) }`.

### Example — Mumbai Residential Telescopic

```json
{
  "@context": "https://raw.githubusercontent.com/beckn/DEG/ies-specs/specification/external/schema/ies/core/context.jsonld",
  "@type": "IES_Policy",
  "id": "policy-mumbai-res-001",
  "objectType": "POLICY",
  "policyID": "MUM-RES-T1",
  "policyName": "Mumbai Residential Telescopic 2024",
  "policyType": "TARIFF",
  "programID": "program-merashehar-001",
  "samplingInterval": "R/2024-04-10T00:00:00Z/P1M",
  "energySlabs": [
    { "id": "slab-0-100",    "@type": "EnergySlab", "start": 0,   "end": 100,  "price": 4.5 },
    { "id": "slab-101-300",  "@type": "EnergySlab", "start": 101, "end": 300,  "price": 7.2 },
    { "id": "slab-301-plus", "@type": "EnergySlab", "start": 301, "end": null, "price": 9.8 }
  ],
  "surchargeTariffs": [
    {
      "id": "surcharge-evening-peak",
      "@type": "SurchargeTariff",
      "recurrence": "P1D",
      "interval": { "start": "T18:00:00Z", "duration": "PT4H" },
      "value": 20,
      "unit": "PERCENT"
    },
    {
      "id": "discount-night-offpeak",
      "@type": "SurchargeTariff",
      "recurrence": "P1D",
      "interval": { "start": "T23:00:00Z", "duration": "PT6H" },
      "value": -10,
      "unit": "PERCENT"
    }
  ]
}
```

The `@type: "IES_Policy"` matters — ONIX's Extended Schema validator dispatches by `@type` against the schema name in `attributes.yaml`.

### Beyond tariffs

The same `IES_Policy` envelope, with a different `policyType` and additional payload fields, expresses:

- **Deviation penalties** — sanctioned-load overshoots, scheduling deviations
- **Data-quality SLAs** — minimum reporting frequency, allowable missing-read percentage for AMISPs
- **Program participation rules** — DR enrolment criteria, peak-time rebate thresholds
- **Public-disclosure thresholds** — which datasets must be open vs. consented

The pattern is the same: a signed, addressable, machine-verifiable rule that consumers ingest directly.

---

## Setup Steps

### 1. Register the publisher

The SERC (or utility) publishing the policy is registered in the appropriate DeDi registry:

- SERC → [`ies-regulators-reference-registry`](../registries/required-registries.md#regulators-registry)
- DISCOM publishing a sub-policy → [`ies-discoms-reference-registry`](../registries/required-registries.md#discoms-registry)

The registry entry pins the `did:web` and public key used to sign the `IES_Policy` object.

### 2. Mint identifiers

- A canonical `policyID` per policy (e.g. `MUM-RES-T1`, `KA-LT2-IND-TOD-2026`). This is the **stable handle** every downstream system uses to refer to this policy.
- A `programID` per `IES_Program` (consumer category, regulatory scheme) that groups related policies.

See [ID Patterns](../identifiers/id-patterns.md).

### 3. Author the policy

Author the policy directly in `IES_Policy` JSON-LD. The canonical schemas are in [`beckn/DEG ies-specs core/`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/attributes.yaml) — `IES_Policy`, `IES_Program`, `EnergySlab`, `SurchargeTariff`. Validate against the JSON Schema before signing.

The DISCOM-facing pattern is to keep an internal CI pipeline that converts an authored YAML or spreadsheet into the canonical JSON-LD, runs schema validation, and submits it for signing.

### 4. Sign and stage for publication

The publisher's BPP signs the policy with its `did:web` private key. The signed bundle becomes the artefact that downstream verifiers will hash-check against the registry-published public key.

### 5. Publish via Data Exchange

The publisher's BPP exposes the policy through its catalogue. Consumers (`discover`/`select` or pre-agreed `confirm`) receive it through the standard lifecycle:

```json
"performance": [{
  "id": "perf-tariff-policy-delivery-001",
  "status": { "code": "DELIVERY_COMPLETE" },
  "commitmentIds": ["commitment-tariff-policy-001"],
  "performanceAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1/context.jsonld",
    "@type": "DatasetItem",
    "dataset:accessMethod": "INLINE",
    "dataPayload": { /* IES_Policy — see above */ }
  }
}]
```

Public-disclosure policies typically use `accessMethod: INLINE` and settlement value `0` — anyone can pull them without contract.

### 6. (Optional) Use policies inline during private exchange

A BPP may attach a policy alongside its catalogue offer to set the **terms of the data exchange itself** — e.g. *"to consume this AMISP feed, your refresh must not exceed 1× per 15 minutes, and you must commit to this retention SLA."* The consumer's `confirm` is then evaluated against the inline policy. The policy is the same `IES_Policy` schema; only the carriage differs.

---

## Consuming a Tariff in a Billing System

```python
def apply_tariff(consumption_kwh: float, hour_of_day: int, policy: dict) -> float:
    """Compute the bill given an IES_Policy. Real billing iterates over actual
    usage intervals; this is the rate-lookup core."""

    # 1. Find the applicable energy slab. `end` is exclusive; `null` = open-ended.
    base_rate = 0.0
    for slab in policy["energySlabs"]:
        end = slab.get("end")
        if slab["start"] <= consumption_kwh and (end is None or consumption_kwh < end):
            base_rate = slab["price"]
            break

    # 2. Apply the first matching time-of-day surcharge.
    surcharge_value = 0.0
    surcharge_unit  = "PERCENT"
    for tod in policy.get("surchargeTariffs", []):
        start_h = int(tod["interval"]["start"][1:3])
        dur_h   = int(tod["interval"]["duration"].split("PT")[1].rstrip("H")) \
                  if tod["interval"]["duration"].endswith("H") else 0
        end_h   = (start_h + dur_h) % 24
        in_window = (start_h <= hour_of_day < end_h) if start_h < end_h \
                    else (hour_of_day >= start_h or hour_of_day < end_h)
        if in_window:
            surcharge_value = tod["value"]
            surcharge_unit  = tod.get("unit", "PERCENT")
            break

    if surcharge_unit == "PERCENT":
        effective_rate = base_rate * (1 + surcharge_value / 100)
    else:
        effective_rate = base_rate + surcharge_value

    return consumption_kwh * effective_rate
```

This function is what replaces the hand-coded slab/ToD table that every DISCOM billing system carries today.

---

## Operate

```bash
git clone https://github.com/beckn/DEG.git
cd DEG/devkits/data-exchange/install
docker compose up -d

# Import the tariff BAP collection
#   DEG/devkits/data-exchange/uc3-tariff-policy/postman/
# Set bap_host_root + bpp_host_root to http://beckn-router:9000
# Fire `confirm`.

docker logs sandbox-bap 2>&1 | grep -E 'on_(confirm|status)' | tail -10

# Or one-shot the whole lifecycle via the Arazzo runner:
cd DEG/devkits/data-exchange/uc3-tariff-policy/workflows
./run-arazzo.sh -w confirm-through-delivery -v
```

---

## Open Items

- **Policy types beyond `TARIFF` and `DISPATCH_GUIDE`.** Schemas for deviation-penalty and data-quality-SLA policies are in draft; they reuse the `IES_Policy` envelope with new `policyType` values.
- **Versioning convention.** When a SERC issues a tariff amendment, the agreed pattern is a new `id` (URN) with the same `policyID` and an explicit `replaces` link to the prior version — being formalised.
- **Policy bundles.** A bundle envelope to ship a set of related policies (e.g. all categories for an FY) as one signed package is being discussed.

---

## References

- [Basic Checklist](../checklists/tariff-intelligence-basic-checklist.md) — plain-English rollout checklist
- [`IES_Policy`, `IES_Program`, `EnergySlab`, `SurchargeTariff` (upstream)](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core)
- [ies-docs tariff specification example](https://github.com/India-Energy-Stack/ies-docs/blob/main/implementation-guides/data_exchange/examples/tariff_specification_example.jsonld)
- [Example payloads (devkit)](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc3-tariff-policy/examples)
- [Data Exchange — Architecture](../data-exchange/architecture.md)
- [Data Exchange — Quick Start](../data-exchange/quick-start.md)
- [ies-docs `08_Energy_policy_as_code.md`](https://github.com/India-Energy-Stack/ies-docs/blob/main/architecture/08_Energy_policy_as_code.md)

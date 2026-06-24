# IES Accelerator — Schemas

This directory holds the canonical schema files referenced from the IES Accelerator documentation. Each subdirectory mirrors a schema family that the accelerator's deployable services (OpenCred, ONIX, etc.) are expected to issue against.

**Repo root:** [https://github.com/India-Energy-Stack/ies-accelerator](https://github.com/India-Energy-Stack/ies-accelerator)

## Why this directory exists

The IES Accelerator docs (`/energy-credentials/...`, `/data-exchange/...`) need stable, repo-relative links to the schema files they describe. Pointing at external sources directly creates two problems:

1. External URLs change shape or move (e.g. branch renames, repo reorganisation upstream).
2. JSON-LD `@context` URLs inside example credentials need to **resolve at runtime** for verifiers to validate; relying on external hosts couples our deployments to their uptime.

Mirroring the schema files into this repo gives us:

- Stable repo-relative paths (`/schemas/<family>/<version>/`) for documentation links.
- Stable `india-energy-stack.github.io/ies-accelerator/...` URLs (served by GitHub Pages from this repo) for `@context` resolution and external JSON-LD consumers.
- Offline-installable copies — DISCOMs running in air-gapped envs can sync this directory once and not need outbound HTTPS to a third-party host every time a credential is verified.

## Provenance and updates

Every mirrored family carries a `README.md` at its root naming the upstream source and version. The mirror is verbatim — we do **not** edit the schema files in place. If upstream changes, the workflow is:

1. Re-run the fetch step against the new upstream version.
2. Place the new files in a sibling version directory (e.g. `v1.1/`, not overwriting `v1.0/`).
3. Update the family-level `README.md` to mark the previous version's status.

If you find a discrepancy between a mirrored file and the upstream source, treat upstream as authoritative and open an issue so the mirror can be refreshed.

## Schema Families

| Family | Latest | All Versions | Description |
|--------|--------|-------------|-------------|
| [ElectricityCredential](ElectricityCredential/README.md) | [v1.2](ElectricityCredential/v1.2/README.md) | v1.0 · v1.1 · v1.2 | W3C VC issued per meter by DISCOMs — customer identity, DERs, tariff profiles |
| [MeterData](MeterData/README.md) | [v0.6](MeterData/v0.6/README.md) | v0.5 · v0.6 | Smart meter telemetry compact profiles (8 profile shapes) |
| [MeterDataCredential](MeterDataCredential/README.md) | [v0.6](MeterDataCredential/v0.6/README.md) | v0.6 | W3C VC wrapping MeterData for provenance attestation |
| [MeterDataRequest](MeterDataRequest/README.md) | [v0.6](MeterDataRequest/v0.6/README.md) | v0.5 · v0.6 | Query schema: capabilities, authorisation, request |
| [MeterDataRequestCredential](MeterDataRequestCredential/README.md) | [v0.1](MeterDataRequestCredential/v0.1/README.md) | v0.1 | W3C VC wrapping MeterDataRequest for seeker authorisation |
| [ArrFiling](ArrFiling/README.md) | [v0.5](ArrFiling/v0.5/README.md) | v0.5 | DISCOM regulatory ARR filing — ArrFiling, ArrFiscalYear, ArrLineItem |
| [OutageNotification](OutageNotification/README.md) | [v0.1](OutageNotification/v0.1/README.md) | v0.1 | **WIP** — planned/unplanned outage notices for web/outage-map publishing + push to consumers |

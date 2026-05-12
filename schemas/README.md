# IES Accelerator — Schemas

This directory holds the canonical schema files referenced from the IES Accelerator documentation. Each subdirectory mirrors a schema family that the accelerator's deployable services (OpenCred, ONIX, etc.) are expected to issue against.

**Repo root:** [https://github.com/India-Energy-Stack/ies-accelerator](https://github.com/India-Energy-Stack/ies-accelerator)

## Why this directory exists

The IES Accelerator docs (`/energy-credentials/...`, `/data-exchange/...`) need stable, repo-relative links to the schema files they describe. Pointing at external sources directly creates two problems:

1. External URLs change shape or move (e.g. branch renames, repo reorganisation upstream).
2. JSON-LD `@context` URLs inside example credentials need to **resolve at runtime** for verifiers to validate; relying on external hosts couples our deployments to their uptime.

Mirroring the schema files into this repo gives us:

- Stable repo-relative paths (`/schemas/<family>/<version>/`) for documentation links.
- Stable `raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/...` URLs for `@context` resolution.
- Offline-installable copies — DISCOMs running in air-gapped envs can sync this directory once and not need outbound HTTPS to a third-party host every time a credential is verified.

## Provenance and updates

Every mirrored family carries a `README.md` at its root naming the upstream source and version. The mirror is verbatim — we do **not** edit the schema files in place. If upstream changes, the workflow is:

1. Re-run the fetch step against the new upstream version.
2. Place the new files in a sibling version directory (e.g. `v1.1/`, not overwriting `v1.0/`).
3. Update the family-level `README.md` to mark the previous version's status.

If you find a discrepancy between a mirrored file and the upstream source, treat upstream as authoritative and open an issue so the mirror can be refreshed.

## Contents

| Family | Version | Upstream | Status |
|---|---|---|---|
| [`ElectricityCredential`](./ElectricityCredential/) | [v1.0](./ElectricityCredential/v1.0/) | [`beckn/DEG`](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential) | Current |

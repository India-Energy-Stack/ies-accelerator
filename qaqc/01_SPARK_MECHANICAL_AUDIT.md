# SPARK-1 Mechanical/Schema/Build/Navigation Reconciled Audit

Take: SPARK-1 evidence converges on a narrow release gate set: unresolved semantic mismatch for shipped MeterDataRequest examples, non-reproducible Make outputs, false-green PDF exit behavior, and incomplete repo-wide CI quality gating; all other major risks are scoped with explicit ownership.

## Inventory / scope
- Repository: `C:\Users\Z0055VCM\Desktop\ies-accelerator`
- Branch: `repo-wide-qaqc`
- Baseline commit: `9fb62e8`
- Scope: tracked docs, schema source and generated artifacts, navigation surfaces, link corpus/anchors, JSON/JSON-LD/YAML/YML files, schema generators/validators, build scripts, and GitHub workflow integration.
- Tracked-file scope used for checks: `245` paths (mechanical scope only; no external generation changed).
- Source policy: no tracked file edits except this report.

## Command/evidence ledger
| Command | Exit | Evidence anchors / outcome |
|---|---:|---|
| `git checkout -- index.md` | 0 | Restored transient `index.md` drift from interrupted run. |
| `Remove-Item -LiteralPath .tmp_index_backup.md -Force` | 0 | Removed transient backup file introduced by interrupted run. |
| `python scripts/validate_links.py .` | 0 | Whole-root output recorded as `1094` checked / `0` broken for validator scope. |
| `python scripts/validate_links.py .` (all local markdown references with excluded files added) | 0 | `1150/0` in broad corpus including `_sidebar.md` and ignored generated targets. |
| `python scripts/generate_index.py` | 0 | Recomputed index in temp, then restored unchanged `index.md` (no persisted mutation). |
| `python -B schemas/MeterDataRequest/v0.6/validation/validator.py schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json` | 1 | Fails `kWh imp` / `kWh exp` under `IntervalProfile` (`schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json:15-18`). |
| `python scripts/validate_schema.py schemas/MeterDataRequest/v0.6/schema.json schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json` | 0 | Generic pass; demonstrates divergence from dedicated semantic validator coverage. |
| `python schemas/MeterData/v0.5/validation/test_runner.py` | 0 | `6/6` fixture expectations passed. |
| `python schemas/MeterDataRequest/v0.6/validation/test_runner.py` | 0 | `4/4` fixture expectations passed; does not include every shipped example. |
| `python scripts/generate_schema_permissive.py` across Make-managed dirs (temporary, restored) | 0 | Detected generated drift; 5 managed directories differ from tracked outputs before restore. |
| `python scripts/compare_v05_v06.py` | 0 | Reports differences and missing file conditions despite zero exit status (`TOTAL_FILES` drift path). |
| `python scripts/verify_v05_v06_equivalence.py` | 1 | Fails current v0.5/v0.6 migration-equivalence checks. |
| `python scratch/verify_no_loss.py` | 1 | Fails with missing removed mapping file (`schemas/MeterData/v0.6/OBISMapping.json`). |
| `python scripts/build_pdf.py` | 1 (default Windows) / inspected source | `build_document()` missing-source count is ignored and main returns 0 at `305`; UTF-8 write defect at `300`. |
| `python scripts/validate_links.py` anchors | 0 | Numeric-anchor issues now treated per `validate_links.py` GitBook slug rules; no confirmed 64-anchor defect. |
| `python` duplicate-key/object parse pass on tracked JSON/YAML | 0 | `122` files parsed; zero duplicate keys and zero parse failures. |
| `git diff --check` | 0 | No whitespace or patch format issues. |
| `git status --short` | 0 | Confirmed only intended report artifact is modified at end. |

## Navigation parity table
| Surface | Count / state | Notes |
|---|---:|---|
| `SUMMARY.md` file-count | `66` | Baseline navigation input. |
| `index.md` generated file-count | `53` | Scripted index output count. |
| Shared entries | `51` | Present in both source and generated index. |
| True Summary-only omissions | `15` | Confirmed omissions (`2` are wrapper READMEs omitted incidentally, but those are not file entries). |
| Index-only entries | `2` | Extra entries present only in generated index. |
| `_sidebar.md` in tracked-only link map | `66` | Added 66 entries when extending corpus. |
| `scripts/validate_links.py` | Excludes `_sidebar.md` from its own checks | 66 `_sidebar` links are not included by default parser mode. |

## Link/anchor results
- Directory link status:
  - Confirmed-live broken (GitBook renders to `.../examples/README.md` and returns 404):
    - `schemas/ArrFiling/v0.5/README.md:25`
    - `schemas/MeterData/v0.6/README.md:29`
    - `schemas/OutageNotification/v0.1/README.md:69`
  - Latent publication risk (directory-only link):
    - `schemas/MeterData/v0.5/README.md:28` (MeterData v0.5 is absent from `SUMMARY.md`; route currently not published, GitHub can still browse directory).
- Corpus dimensions:
  - Whole-root validator: `1094/0` (broken links/anchors suppressed by ignored `latex/_assembled.md` + 9 excluded entries).
  - Reproducible tracked-only corpus: `1085` links checked.
  - `_sidebar.md` adds `66` links when included outside validator default.
  - Prior `1150/1151` claims are stale unless explicitly defined for the full raw corpus baseline.
- Anchor/slugs:
  - `223` guaranteed numeric-anchor defects.
  - `264` total slug mismatches across `939` outline links.
  - Representative mismatches:
    - `index.md:135` → `schemas/faq.md:7` (`id-1.-...` style expectation)
    - `index.md:239` examples section (`./examples` anchor path variant risk).
  - Severity remains `P2` only if index is required as a release artifact; otherwise `P3`.
- `scripts/validate_links.py` slug logic at `24-55` aligns with observed GitBook behavior and explains prior false-positive `64 id-*` set.

## Duplication analysis
- Parser outcome over all tracked JSON/JSON-LD/YAML/YML files (object-scoped): `0` duplicate keys, `0` parse failures.
- Exact content duplication retained as likely maintenance issue:
  - `schemas/MeterData/v0.5/examples/BillingProfile.json`
  - `schemas/MeterData/v0.5/examples/CustomerBillingSummary.json`
- Prior broad duplicate-key findings were retracted as structural scanner artifacts, not file corruption.

## Schema/test coverage matrix
| Evidence area | Coverage status | Limits / omissions |
|---|---|---|
| `schemas/*/schema.json` JSON-Schema meta checks | Covered (`100%` parseability of tracked files). | Does not assert semantic intent beyond generic constraints. |
| Shipped example validation (generic) | Covered (`validate_schema.py` tracks all relevant schema/example paths). | Uses permissive external stubs; does not establish external-contract conformance. |
| Shipped example validation (dedicated) | Covered for MeterData v0.6 and MeterDataRequest v0.6 semantic validators. | MeterDataRequest fixture set does not include all shipped examples; one shipped case fails and blocks gate (`15-18`). |
| Duplicate-key/parsing checks | Covered with object-scoped parser. | No semantic equivalence interpretation included. |
| Link checks | Covered by `validate_links.py` for repo-relative markdown. | Raw HTML links, `_sidebar.md`, directory-publishability, and duplicate-heading intent not fully covered. |
| Migration checks | Covered but weak: compare and verify scripts execute and fail reporting diffs. | Non-zero diff is not normalized to non-zero exit in one script; tools are stale wrt repo state. |
| JSON-LD checks | Script exists (`scripts/check_jsonld.py`) but not dependable in environment/wiring. | Missing dependency declaration and no CI gate; repository-wide coverage incomplete. |
| Build checks | `build_pdf.py` build logic and CI workflow present. | Missing-source count can return green; Windows encoding portability not uniformly gated. |
| Source/generated reproducibility | Covered by temporary regeneration and compare. | Not gated in Make/CI; confirmed non-empty drift. |

## Build/release assessment
- `Makefile`
  - Manages `8` schema directories.
  - `5` of `8` directories drift when regenerated with Make-selected workflow, affecting `12` artifacts:
    - `schemas/MeterData/v0.5/context.jsonld`, `vocab.jsonld`
    - `schemas/MeterDataCredential/v0.6/schema.json`, `context.jsonld`, `vocab.jsonld`
    - `schemas/MeterDataRequest/v0.5/context.jsonld`, `vocab.jsonld`
    - `schemas/MeterDataRequest/v0.6/context.jsonld`, `vocab.jsonld`
    - `schemas/MeterDataRequestCredential/v0.1/schema.json`, `context.jsonld`, `vocab.jsonld`
  - Reproduces cleanly for `ArrFiling v0.5`, `MeterData v0.6`, `OutageNotification v0.1`.
  - Excludes ElectricityCredential versions (`Makefile:20-22`) is a separate ownership/control gap (not counted in the above 5-of-8 drift set).
- `scripts/validate_schema.py` (`51-53`) path normalization uses filesystem relpaths with backslashes and fails cross-schema resolution on Windows; confirmed `P2` unless Windows support is contractual.
- `scripts/build_pdf.py`
  - Missing-source count is computed in `245-270` but ignored in main path; exits are treated as success (`304-305`) → non-failing partial build is confirmed risk.
  - Locale-default write behavior at `300` is Windows-localized portability (`P2`).
  - `.github/workflows/build-pdf.yml` remains Linux/ubuntu-centric and does not validate GitBook runtime or doc completeness.

## Prioritized root-issue register (deduplicated)

### CONFIRMED DEFECT
| SPARK ID | P-level | File/line anchors | Finding | Acceptance criterion |
|---|---:|---|---|---|
| SPARK-MDR-001 | P1 | `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json:15-18` ; `schemas/MeterData/v0.6/IES codes.json:338-348,353-362` ; `schemas/MeterDataRequest/v0.6/validation/validator.py` | Shipped MeterDataRequest example fails dedicated semantic validation while generic pass is incomplete coverage. | All shipped MeterDataRequest examples must pass dedicated semantic validator with no exceptions; unit suite must include this profile/register case. |
| SPARK-MAKE-001 | P1 | `Makefile:20-22`, `Makefile:40-42`, `generate output artifacts (5 directories x 12 artifacts)` | Make regeneration from generator selected in repo is non-reproducible for 5 managed directories and 12 artifacts. | A clean Make regeneration results in zero `git diff`; generator ownership and policy for remaining ElectricityCredential set declared explicitly. |
| SPARK-PDF-001 | P1 | `scripts/build_pdf.py:245-270`, `scripts/build_pdf.py:304-305` | Missing-source count can be non-zero yet publish flow exits success. | Main must return non-zero when any missing source/expected chapter is detected; build must be complete before publication. |
| SPARK-CI-001 | P1 | `.github/workflows/build-pdf.yml:39-119` | No repository-wide CI gate exists beyond PDF publish workflow; major quality checks are optional/non-gating. | Require a workflow with required jobs: markdown links (including directory publishability), schema drift, semantic validation, JSON-LD checks, index parity/anchor checks, PDF completeness, and hosted path smoke. |
| SPARK-LNK-001 | P3 (or P2 if index required) | `index.md:135`, `index.md:239`, `schemas/faq.md:7` ; `scripts/generate_index.py:4-10,113-120` | Numeric-anchor mismatch and index omissions remain uncaptured by existing markdown validator and can cause broken index navigation. | Decide whether `index.md` is required in release artifact; if required, enforce generated-anchor contract and full entry parity. |
| SPARK-SCHEMA-004 | P2 | `scripts/validate_schema.py:51-53` and Windows URL slashes | Cross-schema resolver path handling uses backslash URL fragments and fails on Windows. | Normalize resolver URLs to URL-safe slashes and document/support policy if Windows is contractual. |

### MATERIAL RISK
| SPARK ID | P-level | File/line anchors | Finding | Acceptance criterion |
|---|---:|---|---|---|
| SPARK-LNK-002 | P2 | `schemas/ArrFiling/v0.5/README.md:25`, `schemas/MeterData/v0.6/README.md:29`, `schemas/OutageNotification/v0.1/README.md:69` | Three live GitBook links verified as 404 due directory-linking; one additional latent (MeterData v0.5). | Verify each route against published GitBook/hosted mirror or replace with explicit file anchors. |
| SPARK-VSNN-001 | P2 | `schemas/MeterData/v0.6/attributes.yaml:4-6` vs `schemas/MeterData/v0.6/README.md:3,7-16`; `schemas/ArrFiling/v0.5/attributes.yaml:4` vs `schemas/ArrFiling/v0.5/README.md:3` | Metadata/version alignment disagreement between source attributes and README intent. | Owner must define source-of-truth for version/profile metadata and align files. |
| SPARK-BLD-002 | P2 | `scripts/build_pdf.py:300` and `download-pdf.md:23-26` | Locale-default non-ASCII write behavior can fail local Windows/Python defaults. | Make UTF-8 write explicit and document supported local execution matrix. |
| SPARK-TOOL-001 | P2 | `scratch/verify_no_loss.py:56-64`, `scripts/compare_v05_v06.py:92-120`, `scripts/verify_v05_v06_equivalence.py:230-233` | Migration verification tooling is stale/weak or hard-failing on removed file paths. | Mark these tools as supported-current or archived; define replacement gate in CI. |
| SPARK-DUP-001 | P3 | `schemas/MeterData/v0.5/examples/BillingProfile.json` ; `schemas/MeterData/v0.5/examples/CustomerBillingSummary.json` | Exact duplicate example pair remains unresolved intent-wise. | Owner decides if duplication is intentional reuse; if not, de-duplicate or rename with clear semantic purpose. |

## Corrections from prior drafts
- Corrected path typo: `schemas/ArrFiling/v0.1/README.md` is invalid; actual path is `schemas/ArrFiling/v0.5/README.md:25`.
- Downgraded/retracted SPARK-ANCH-001: `64` `id-*` defects are not confirmed defects; validator slugging follows GitBook rules and prior mismatch set is now treated as tooling/contract mismatch evidence only.
- Clarified directory-links:
  - Three confirmed live 404s remain.
  - One additional MeterData v0.5 link is latent publication risk due absent `SUMMARY.md` publish path.
- Removed prior duplicate-key claims for JSON/YAML parse objects; evidence shows `0` confirmed duplicate keys and `0` parser failures.
- Recomputed counts from tracked corpus:
  - `66` SUMMARY, `53` index, `51` shared, `15` summary-only omissions, `2` index-only entries, `1094` (or `1085` tracked-only corpus) and `66` `_sidebar` additions depending on corpus construction.
- Severity/categorization updated so index and numeric anchor defects are `P2/P3` by artifact requirement, not unconditional `P1`.
- Non-reproducible Make drift now limited to `5 of 8` managed directories and `12 artifacts`, with `ArrFiling v0.5`, `MeterData v0.6`, and `OutageNotification v0.1` reproduced identically.

## Severity and classification summary
- CONFIRMED DEFECT: `3 P1` (`SPARK-MDR-001`, `SPARK-MAKE-001`, `SPARK-PDF-001`), `2 P2` (`SPARK-LNK-001`, `SPARK-SCHEMA-004`), `0 P3`.
- MATERIAL RISK: `4 P2` (`SPARK-LNK-002`, `SPARK-VSNN-001`, `SPARK-BLD-002`, `SPARK-TOOL-001`), `1 P3` (`SPARK-DUP-001`).
- Retractions: `2` high-priority earlier findings removed (`SPARK-ANCH-001`, ArrFiling v0.1 typo).
- Unverified hypothesis: `0` retained as high-level class.

## Proposed low-risk fix batch (owner grouped)
- Schema owner:
  - Resolve MeterDataRequest shipped-example contradiction by deciding example/registry/validator truth and enforcing semantic fixture coverage.
  - Decide canonical generator strategy and restore Make reproducibility (non-permissive vs permissive output contract).
  - Reconcile version metadata mismatch for `MeterData v0.6` and `ArrFiling v0.5`.
- Build/tooling owner:
  - Fix `build_pdf.py` missing-source exit path and UTF-8 file-write defaults.
  - Normalize Windows resolver URL slashes in `scripts/validate_schema.py` if Windows support is required.
- Docs/navigation owner:
  - Confirm directory-link publishing contract for all `./examples` links; resolve or replace 3 confirmed and 1 latent link risks.
  - Repair `generate_index.py` vs GitBook sluging if index is release-critical, then lock parity assertions (`15` summary omissions and index-only entries).
  - Triage duplicate example intent (`BillingProfile`/`CustomerBillingSummary`).
- Release owner:
  - Add required CI/PR gate for full check sequence in `P1` block, including hosted-publish smoke checks.
- Maintenance owner:
  - Refresh or deprecate `scratch/verify_no_loss.py`; harden `compare_v05_v06`/`verify_v05_v06_equivalence` exit semantics.

## Stop/escalate conditions
- Stop release immediately for unresolved P1 gates:
  - `SPARK-MDR-001`
  - `SPARK-MAKE-001`
  - `SPARK-PDF-001`
  - `SPARK-CI-001` (unless explicit manual hold gate is approved and documented).
- Escalate to Sonnet and Fable for unresolved:
  - Example/registry/validator truth hierarchy (`SPARK-MDR-001`).
  - Canonical generator choice and reproducibility scope.
  - ElectricityCredential ownership and intentional exclusion (`Makefile:20-22`).
  - Metadata version intent and external stub/JSON-LD policy.
  - Migration and duplicate-example intent.
- Escalation criteria include any regenerated diff outside controlled scope, additional confirmed live 404s, or new validated anchor failures.

## Residual unverified items
- Whether `index.md` is contractually required as release artifact.
- Whether any of `P2` risks are accepted as intentional design exceptions.
- Whether GitBook-specific publishability checks for directory links remain accepted without explicit route contract.

## Supersession note
This corrected report, together with `qaqc/02_INDEPENDENT_QUALITY_GATE_AUDIT.md`, is the authoritative mechanical/schema/build/navigation evidence set at this stage. Final semantic issue register completion remains pending Sonnet execution and Fable arbitration.

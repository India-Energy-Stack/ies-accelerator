# SPARK-1 Mechanical/Schema/Build/Navigation Correction Audit

Baseline repository state is stable for link resolution, but I am replacing false-positive anchor findings with corrected evidence and re-centering the highest-risk defects.

## Inventory / scope
- Repository: `C:\Users\Z0055VCM\Desktop\ies-accelerator`
- Branch: `repo-wide-qaqc`
- Baseline commit: `9fb62e8`
- Tracked file inventory used for this pass: `245`
- Tracked markdown files scanned: `81` (core docs set) and `85` when including generated/site-nav files (e.g., `index.md` and `_sidebar.md`).
- Scope: tracked docs, schema/tooling JSON/JSON-LD/YAML/YML assets, link validation, schema tooling, navigation surfaces, Makefile targets, build pipeline, and release workflow.

## Command/evidence ledger
| Command | Exit | Evidence |
|---|---:|---|
| `git checkout -- index.md` | 0 | Restored transient `index.md` mutation from interrupted run. |
| `Remove-Item -LiteralPath .tmp_index_backup.md -ErrorAction SilentlyContinue` | 1 | Temp artifact already absent (cleanup already done). |
| `python scripts/validate_links.py .` | 0 | `Link check summary: Checked 1094 links. Found 0 broken.` |
| `python scripts/compare_v05_v06.py` | 0 | Reports diffs (`AggregatedFeeder.json`, `MultiMeterBulkDataset*`) and `BillingProfile.json` missing in v0.6; still non-zero diff count despite success exit. |
| `python scripts/verify_v05_v06_equivalence.py` | 1 | Profile count mismatches + missing `BillingProfile.json` in v0.6. |
| `python scratch/verify_no_loss.py` | 1 | `FileNotFoundError: ...schemas/MeterData/v0.6/OBISMapping.json`. |
| `python schemas/MeterDataRequest/v0.6/validation/validator.py schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json` | 1 | Semantic failures on `kWh imp`, `kWh exp` in `IntervalProfile`. |
| `python scripts/validate_schema.py schemas/MeterDataRequest/v0.6/schema.json schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json` | 0 | Generic validator passes this example as fully compliant (`100% compliant`). |
| `python -X utf8 scripts/validate_schema.py schemas/MeterDataCredential/v0.6/schema.json schemas/MeterDataCredential/v0.6/examples/example-customer-profile.json` | 1 | Unresolvable `$ref`: `https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/schema.json`. |
| `python scripts/generate_index.py` | 0 | `index.md compiled successfully with collapsible elements!`; temporary regenerate+restore used. |
| `python scripts/build_pdf.py --help` | 0 | CLI reachable; no runtime validation performed beyond help path. |
| `python scripts/build_pdf.py` | 0 | PDF pipeline does not run non-empty on missing `SUMMARY` files in this pass; behavior inspected by source audit. |
| `bash scripts/build_pdf.sh --help` | 1 | `bash` entrypoint unavailable in this Windows shell (tooling assumption observed). |
| `python -c` relpath URL sample (`os.path.relpath`) | 0 | Confirms Windows-style slash in resolver URL: `.../schemas/MeterData\\v0.6\\schema.json`. |
| `python -c` temporary regen loop (all `schemas/*/attributes.yaml`) | 0 | Generated schema drift detected (`GENERATED_CHANGES_BEFORE_RESTORE=9` before restore). |
| `git diff --check` | 0 | No whitespace or diff-format issues. |
| `git status --short` | 0 | Clean aside from expected working artifact handling and report target. |

## Navigation parity / filesystem reality
- `SUMMARY.md` vs `_sidebar.md` (normalized by stripping leading `/` and removing external links): counts are equal.
  - `SUMMARY` links: `66`
  - `_sidebar` links: `66`
  - Missing from `_sidebar`: `0`
  - Missing from `SUMMARY`: `0`
  - Missing targets in either file: `0`
- `SUMMARY -> index.md` parity (tracked link targets): `66` referenced in SUMMARY, `55` linked in index, `13` missing.
  - Missing entries include `use-cases-overview/p2p-energy-trading.md` and schema family hubs such as `schemas/ArrFiling/README.md`, `schemas/MeterData/README.md`, and `schemas/external/README.md` (all observed in `SUMMARY.md`).
- Filesystem checks:
  - Four `./examples` README links are valid directories (`schemas/ArrFiling/v0.5/examples`, `schemas/MeterData/v0.5/examples`, `schemas/MeterData/v0.6/examples`, `schemas/OutageNotification/v0.1/examples`).

## Markdown link / local anchor and encoding review
- Local+external link classification:
  - 1160 local markdown references
  - 674 external references
  - 325 anchor references
- Case-risk and URL-encoding:
  - Case-like-mismatch candidates detected: `0`
  - URL-encoded links detected: `3` (all currently resolvable)
- Naive validator output for local anchors:
  - `0` broken links and `0` broken anchors from `scripts/validate_links.py`.
- Critical retraction from prior pass:
  - Earlier 64 `id-*` anchor defects were reclassified as false positives under the repo validator.
  - Governing validator script (`scripts/validate_links.py`) explicitly implements GitBook-style slugging at lines `24-56` (id-prefixed numeric handling, period retention, etc.).

## Duplicate / overlap analysis
- Duplicate-key and overlap checks were previously enumerated in `spark_qaqc_report2.json`:
  - very large duplicate-key surface in example/fixture payloads
  - no new duplicate-key scan was re-run in this correction pass.
- No additional duplicate anchor/heading defects were confirmed from this correction iteration; several fixture-level repeats remain to classify with schema-owner context (semantic vs accidental reuse).

## Schema/test coverage matrix
| Area | Coverage | Limitation |
|---|---|---|
| Markdown link integrity | Covered | `validate_links.py` check complete (`1094` checked, `0` broken). |
| Navigation parity (`SUMMARY` <-> `_sidebar`) | Covered | Entry counts match exactly (`66` each). |
| Navigation parity (`SUMMARY` -> `index`) | Covered | 13 missing targets; not a parity-equivalent source for all docs. |
| Schema JSON/YAML parseability | Covered (bulk-level) | Prior scan in raw results flagged malformed/duplicate-key-heavy example payloads needing source review. |
| MeterDataRequest validation | Partially covered | Dedicated semantic validator catches extra rules not present in root tests. |
| Cross-schema validation path resolution | Covered | Fails on Windows due backslash path interpolation in resolver URLs (`scripts/validate_schema.py:51-53`). |
| v0.5→v0.6 comparison scripts | Covered but weak | `compare_v05_v06.py` prints diffs while returning success; `verify_v05_v06_equivalence.py` fails; `scratch/verify_no_loss.py` crashes on missing mapping file. |
| PDF/build gates | Weak | `build_pdf.py` can return success despite non-empty missing file set and has UTF-8 portability issues. |

## Build/release assessment
- `Makefile`
  - Excludes ElectricityCredential from schema discovery (`SCHEMA_DIRS` filter): `Makefile:20-22`.
  - Uses permissive generator for all remaining schema dirs: `Makefile:40-42`.
  - Regeneration run (temporary, restored): touched multiple tracked generated schema artifacts (`schemas/ElectricityCredential/v1.0|v1.1|v1.2/schema.json`, `schemas/MeterDataCredential/v0.6/schema.json`, `schemas/MeterDataRequestCredential/v0.1/schema.json`), showing source-tool drift.
- `scripts/validate_schema.py`
  - Resolver URL assembly from `os.path.relpath` inserts backslashes: `51-53`.
  - Cross-schema resolution fails on Windows.
- `scripts/build_pdf.py`
  - Missing-file count is calculated in `build_document` but ignored by `main` (`245-270`, `304`): risk of false-success.
  - Explicit UTF-8 path: `APPENDIX_INTRO` contains non-ASCII and `.write_text` is not forced to UTF-8 (`36-43`, `300`).
- `scripts/build_pdf.sh` and `.github/workflows/build-pdf.yml`
  - Bash + Linux toolchain assumptions are explicit (`python3`, `bash`, `pandoc`, `tectonic`, `mmdc`, `runs-on: ubuntu-latest`), so Windows/local portability is not exercised by CI here.

## Prioritized root-issue register
### Confirmed defects
| SPARK ID | P-level | Classification | Evidence anchors | Why this is root | Acceptance criteria |
|---|---:|---|---|---|---|
| SPARK-ANCH-002 | P1 | CONFIRMED DEFECT | `scripts/validate_links.py:24-56` vs `scripts/generate_index.py:4-10`, `scripts/generate_index.py:10`, `use-cases-overview/discom-regulatory-filing.md:28`, `use-cases-overview/tariff-intelligence.md:40` | Generated index anchors (`1-...`, `12-...`) are incompatible with GitBook-style (`id-1.-...`, `id-1.2-...`) anchors used by downstream links. | Normalize `scripts/generate_index.py` slugification to match GitBook behavior or generate explicit canonical anchors in linked docs. |
| SPARK-GEN-001 | P1 | CONFIRMED DEFECT | Summary/Index diff script output (`SUMMARY_COUNT=66`, `INDEX_LINKS=55`, `MISSING_FROM_INDEX=13`), `SUMMARY.md:45`, `SUMMARY.md:64-76` | `index.md` omits 13 tracked pages (including `use-cases-overview/p2p-energy-trading.md` and several schema-family READMEs) and is therefore not a complete navigation representation. | Include all intended `SUMMARY` targets (or explicitly document exclusions) and show zero missing entries under scripted comparison. |
| SPARK-SCHEMA-001 | P1 | CONFIRMED DEFECT | `scripts/validate_schema.py:51-53`, sample URL with backslashes (`schemas\\v0.6\\schema.json`) | Backslash path interpolation produces unresolvable GitHub Pages URLs in resolver map and breaks cross-schema validation on Windows. | Canonicalize `rel_path` to URL-safe forward-slash form before URL assembly and demonstrate cross-schema pass with `-X utf8` on Windows. |
| SPARK-SCHEMA-002 | P2 | CONFIRMED DEFECT | `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json:15-18`, `schemas/MeterDataRequest/v0.6/validation/test_cases:19-22`, `schemas/MeterDataRequest/v0.6/validation/test_runner.py:18-24` | Dedicated semantic rule for `IntervalProfile` is not covered by current test set; dedicated validator fails while generic validator passes. | Add/port this negative case into `validation/test_cases` and enforce non-zero exit in CI checks. |
| SPARK-SCHEMA-003 | P2 | CONFIRMED DEFECT | `scripts/compare_v05_v06.py` run in this pass returns success with diffs; `spark_qaqc_report2` temp check showed `TOTAL_FILES` drift; `scripts/compare_v05_v06.py` output | Tool is currently a weak gate: outputs diffs but reported success path for this pass, so it does not reliably gate regressions. | Make non-empty diff exit non-zero and assert expected v0.5/v0.6 compatibility policy explicitly. |
| SPARK-BLD-001 | P1 | CONFIRMED DEFECT | `scripts/build_pdf.py:270`, `303-305` | Missing file tracking from `build_document` does not fail process exit. | Return non-zero when missing files are reported; add regression test for partial build failure. |
| SPARK-BLD-002 | P2 | CONFIRMED DEFECT | `scripts/build_pdf.py:36-43`, `300`, `.github/workflows/build-pdf.yml:39-45` | Non-ASCII and platform assumptions can fail under contributor Windows flows and are only partially guarded by Linux CI. | Add explicit UTF-8 handling and add platform-specific test/smoke matrix. |
| SPARK-MAKE-001 | P2 | CONFIRMED DEFECT | `Makefile:20-22`, `Makefile:40-42`, temp regen run (`9 tracked changes before restore`) | ElectricityCredential exclusion plus permissive generation mode + observed artifact drift indicates release artifacts can go out-of-sync by regeneration path. | Document exclusion rationale and add reproducibility checksum check or dedicated Make target for deliberate exclusion. |

### Material risks
| SPARK ID | P-level | Classification | Evidence anchors | Why deferred | Acceptance criteria |
|---|---:|---|---|---|---|
| SPARK-LNK-001 | P2 | MATERIAL RISK | `schemas/ArrFiling/v0.5/README.md:25`, `schemas/MeterData/v0.5/README.md:28`, `schemas/MeterData/v0.6/README.md:29`, `schemas/OutageNotification/v0.1/README.md:69` | `./examples` directory links resolve in local validator but external GitBook runtime behavior for directory targets was not proven. | Verify one directory-link contract in a live GitBook publish path or replace with explicit first-file anchors. |
| SPARK-META-001 | P2 | MATERIAL RISK | `schemas/ArrFiling/v0.5/attributes.yaml:4` vs `schemas/ArrFiling/v0.5/README.md:3`, `schemas/MeterData/v0.6/attributes.yaml:4` vs `schemas/MeterData/v0.6/README.md:3` | Version intent appears ambiguous between metadata and docs. | Source-of-truth decision on versioning field and doc sync policy (single canonical value). |
| SPARK-TOOLS-001 | P1 | MATERIAL RISK | `scratch/verify_no_loss.py:149`, `scratch/verify_no_loss.py:62` | Tool fails because referenced mapping file is removed; if run in automation, it hard-fails unrelated checks. | Mark deprecated or update file contract (`OBISMapping.json`) explicitly and gate usage. |
| SPARK-DUP-001 | P3 | MATERIAL RISK | prior scanner output in `C:\\Users\\Z0055VCM\\AppData\\Local\\Temp\\spark_qaqc_report2.json` | High duplicate-key volume in telemetry examples can be accidental or generated-template-intent; no structural confirmation rerun in this pass. | Re-run duplicate analysis with schema-aware dedupe policy and confirm owner intent where duplicates remain. |

### Retracted findings
- SPARK-ANCH-001 (64 anchor defects): Retraction. Not confirmed after re-run with `scripts/validate_links.py` (0 broken links/anchors).
- `schemas/ArrFiling/v0.1` path claim: Retraction. Correct path exists at `schemas/ArrFiling/v0.5` (`Test-Path`/link evidence).  

## Classification counts after correction
- Confirmed defect: `8` (`P0`:0, `P1`:4, `P2`:4, `P3`:0)
- Material risk: `4` (`P1`:0, `P2`:4, `P3`:0)
- Retracted: `2`
- Unverified hypothesis: `0` (all remaining high-volume issues captured as material risk)

## Proposed low-risk fix batch (by owner)
- Docs owner:
  - Confirm `./examples` directory-link contract in deployed docs.
  - Resolve `SUMMARY`/`index.md` intentional mismatch list and add index completeness check to automation.
- Schema owner:
  - Align `scripts/validate_links`/`generate_index` anchor behavior with GitBook rules or publish anchor compatibility contract.
  - Add MeterDataRequest semantic fixture from `Anonymised_Telemetry_Request.json` into dedicated negative test matrix.
- Tooling owner:
  - Fix `scripts/validate_schema.py` URL path building and `scripts/compare_v05_v06.py` exit semantics.
  - Refresh/retire scratch tools (`scratch/verify_no_loss.py`) based on current repository contracts.
- Release owner:
  - Add build-gate on `build_document` missing count in `scripts/build_pdf.py`, explicit UTF-8 file I/O, and non-Linux smoke in contributor workflow or documented local requirements.

## Stop/escalation conditions
- Stop and block release if any unresolved P1 remains: `SPARK-ANCH-002`, `SPARK-GEN-001`, `SPARK-SCHEMA-001`, `SPARK-BLD-001`, `SPARK-BLD-002`.
- Escalate immediately on any divergence where regenerated artifacts differ from tracked state outside controlled Makefile scope.
- Escalate if `scripts/compare_v05_v06.py` still reports diffs while exiting `0`.

## Residual unverified items
- Whether `index.md` is intended to be complete clone of `SUMMARY` or curated subset (definition currently implicit).
- Whether `schemas/MeterData/v0.5/examples/BillingProfile.json` and `schemas/MeterData/v0.5/examples/CustomerBillingSummary.json` identity is intentional contract artifact reuse (byte-identical).
- Whether stale references in scratch tooling should be sunset, version-gated, or migrated to a maintained validation suite.

# Independent Quality-Gate Audit

## Overall verdict

The repository is not release-green. Basic navigation parity, schema syntax, field-table freshness, and unit fixtures pass, but shipped semantic data, schema reproducibility, PDF completeness, live-link integrity, and CI coverage do not.

## Mechanical-audit corrections

### Directory links: three confirmed live breaks, one latent risk

The following published pages contain `./examples` links that GitBook renders as GitHub URLs ending in `/examples/README.md`. Those generated destinations return HTTP 404:

- `schemas/OutageNotification/v0.1/README.md:69`
- `schemas/MeterData/v0.6/README.md:29`
- `schemas/ArrFiling/v0.5/README.md:25`

The ArrFiling path is `v0.5`; the `v0.1` reference in the mechanical audit is a typo.

`schemas/MeterData/v0.5/README.md:28` has the same directory-only link, but MeterData v0.5 is not listed in the current `SUMMARY.md`, its GitBook route returns 404, and GitHub itself can open a directory link as a listing. It is therefore a latent publication risk, not a currently confirmed live break.

The repository link validator misses this class because `os.path.exists(target_path)` accepts a directory at `scripts/validate_links.py:131` without verifying that the publishing target is a deliverable page.

### The claimed 64 anchor failures are false positives

Rendered GitBook currently contains these exact heading IDs:

- `id-2.-what-it-records-covers`
- `id-1.2-generate-your-credential-signing-keypair`
- `id-2.3-run-opencred-in-did-web-mode`
- `id-3.-how-each-item-is-identified`

They match the fragments used at `pathways/authority.md:93`, `how-you-implement-ies/digilocker.md:65`, and `use-cases-overview/der-visibility.md:38`. GitBook's observed handling of numeric headings includes the `id-` prefix and preserves periods. The GitBook-specific slug rules at `scripts/validate_links.py:24-55` reflect that behavior; the 64-item result came from a non-GitBook slug assumption and should not be treated as a defect set.

### Windows Unicode failure is real but scoped

`scripts/build_pdf.py:300` calls `Path.write_text()` without an explicit encoding. A default CP-1252 Python process fails on the em dash in the appendix text. However:

- Release CI runs on Ubuntu (`.github/workflows/build-pdf.yml:39`).
- Local PDF instructions document macOS/Linux commands (`download-pdf.md:23-26`).
- `PYTHONUTF8=1` avoids this specific failure.
- `bash scripts/build_pdf.sh --help` is not a valid help-path test because the shell script implements no argument parser.

This is a local cross-platform portability gap, not evidence that the current Ubuntu publication path fails.

### Duplicate-key correction

An object-scoped parser found zero duplicate keys in tracked JSON, JSON-LD, YAML, or YML files. The mechanical audit's 1,533 warnings counted repeated property names across separate objects and arrays; they are scanner artifacts, not confirmed duplicate JSON/YAML keys.

## Validator, test, and build inventory

| Check | What it establishes | What it does not establish |
|---|---|---|
| `Makefile test` | Runs six MeterData and four MeterDataRequest fixture expectations (`Makefile:14-18`) | Does not run shipped examples or any other schema family |
| `Makefile build` | Incrementally regenerates eight non-ElectricityCredential schema directories | Excludes every ElectricityCredential version (`Makefile:20-22`) and has no generated-diff gate |
| `Makefile validate` | Runs generic JSON-Schema validation using timestamp stamps | Does not run semantic or JSON-LD checks; stamps do not depend on validator/tool changes (`Makefile:46-51`) |
| `scripts/validate_links.py` | Checks standard inline Markdown relative links and Markdown anchors; current result is 1,150 checked and zero reported broken | Does not inspect raw HTML links, `_sidebar.md`, remote URLs, duplicate headings, or directory publishability (`:19-21,107-110`) |
| `scripts/validate_schema.py` | Parses examples and validates them against Draft 2020-12 schemas | External schemas are permissive object stubs (`:9-43`); lookup files are skipped (`:149-152`); no domain semantics |
| MeterData v0.6 semantic validator | Checks structural constraints plus descriptor, profile, register, cumulative-value, and mathematical rules; all current examples pass | Covers only MeterData v0.6 and still uses permissive external definitions |
| MeterDataRequest v0.6 semantic validator | Checks profile/register/mode compatibility and authorization time windows | Current shipped examples do not all pass |
| `scripts/check_jsonld.py` | Designed to detect context parse errors, IRI collisions, unmapped terms, and local expansion failures | Not wired into Make or CI; `pyld` is undeclared and absent locally |
| `scripts/generate_field_tables.py --all --check` | Confirms all eleven schema-version README field tables match current compiled schemas | Does not compare schema sources to compiled schema/context/vocabulary artifacts |
| `scripts/generate_external_field_tables.py --check` | Can detect drift from an external DEG checkout | Requires a separate checkout and is not part of `all` or CI |
| `scripts/verify_v05_v06_equivalence.py` | Intended to verify MeterData migration value preservation | Currently exits 1; missing counterparts are warnings rather than hard failures (`:230-233`) |
| `scripts/compare_v05_v06.py` | Prints structural migration differences | Exits 0 despite differences and missing files (`:92-120`) |
| `scratch/verify_no_loss.py` | Historical schema/OBIS comparison | Crashes because `schemas/MeterData/v0.6/OBISMapping.json` no longer exists (`:56-64`) |
| `scripts/build_pdf.py` and `scripts/build_pdf.sh` | Build a combined Markdown document and PDF from `SUMMARY.md` | Do not reliably fail on missing source chapters and do not validate PDF content or links |
| `.github/workflows/build-pdf.yml` | Builds on Ubuntu and publishes a mirrored repository plus PDF to `gh-pages` | Verifies only tracked schema-file and PDF presence, not documentation completeness, rendered PDF quality, or hosted GitBook state |

## Requirement-to-evidence matrix

| Requirement | Current evidence | Gate status |
|---|---|---|
| Repository and schema-file completeness | Eleven schema directories contain `attributes.yaml`, `schema.json`, `context.jsonld`, and `vocab.jsonld`; all parse | Partial pass |
| Markdown file and anchor integrity | Repository checker reports 0/1,150, but three published directory links resolve to live 404s | **Fail** |
| `SUMMARY.md` / `_sidebar.md` parity | 66/66 title/path/order match; all targets exist | Pass, but not automated |
| Generated index correctness | Omits 15 of 66 SUMMARY pages; HTML anchors are outside the validator | **Fail** |
| Duplicate keys and content | Zero scoped duplicate keys; one exact duplicate example pair | Partial pass |
| JSON Schema syntax | All eleven `schema.json` files pass Draft 2020-12 meta-schema checks | Pass |
| Shipped example conformance | Generic validation mostly passes; one shipped semantic example fails | **Fail** |
| Source/generated reproducibility | Only three of eight Make-managed schema directories regenerate identically | **Fail** |
| Version and terminology consistency | Confirmed stale MeterData v0.6 source metadata | **Fail** |
| JSON-LD consistency | Checker exists but is not runnable in the current environment or automated | No complete evidence |
| PDF build completeness | Missing-source count is ignored; Windows locale path fails | **Fail** |
| Publish-tree completeness | Workflow checks schema artifacts and PDF presence only | Partial pass |
| Hosted GitBook correctness | Three live links verified broken; no automated hosted-site verification | **Fail** |
| Repository-wide CI | The sole workflow is PDF build/publication | **Fail** |
| Prose, terminology, and logical consistency | Requires manual semantic review; no automated repository evidence | Manual gate required |

## Prioritized findings

### P1 — release blockers

#### P1.1 — A shipped MeterDataRequest example fails its own semantic validator

`schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json:15-18` requests `kWh imp` and `kWh exp` under `IntervalProfile`. Their entries in `schemas/MeterData/v0.6/IES codes.json:338-348,353-362` permit only DAILY, MONTHLY, and INSTANTANEOUS profiles.

The unit fixture suite passes because it does not run all shipped examples. The root Make validation uses the generic structural validator rather than the MeterDataRequest semantic validator.

Acceptance criterion: every shipped MeterDataRequest example passes both structural and dedicated semantic validation, with a regression case covering this profile/register combination.

#### P1.2 — Schema outputs are not reproducible from the Make pipeline

Isolated regeneration with the generator selected by the root Makefile produced drift in:

- MeterData v0.5: `context.jsonld`, `vocab.jsonld`
- MeterDataCredential v0.6: `schema.json`, `context.jsonld`, `vocab.jsonld`
- MeterDataRequest v0.5: `context.jsonld`, `vocab.jsonld`
- MeterDataRequest v0.6: `context.jsonld`, `vocab.jsonld`
- MeterDataRequestCredential v0.1: `schema.json`, `context.jsonld`, `vocab.jsonld`

Only ArrFiling v0.5, MeterData v0.6, and OutageNotification v0.1 regenerated identically. ElectricityCredential v1.0/v1.1/v1.2 are excluded entirely by `Makefile:20-22`.

`scripts/generate_schema.py:8-32` correctly maps cross-file OpenAPI `attributes.yaml#/components/...` references into JSON-Schema `schema.json#/$defs/...` references. Make invokes `scripts/generate_schema_permissive.py`, whose conversion at `:16-22` does not map those cross-file references. For example, the source reference at `schemas/MeterDataCredential/v0.6/attributes.yaml:69` is correctly represented in the tracked output at `schema.json:39`, but regeneration through the Make-selected generator changes that contract.

Acceptance criterion: one canonical generator per schema class; clean regeneration of every managed artifact produces an empty `git diff`; ElectricityCredential artifacts have an explicit reproducible path or are explicitly declared externally maintained.

#### P1.3 — PDF generation can publish a partial book with exit 0

`build_document()` returns the missing-file count at `scripts/build_pdf.py:245-270`. `main()` ignores the return at `:304` and unconditionally returns 0 at `:305`. A missing `SUMMARY.md` source can therefore be omitted while the build and publication workflow remain green.

The workflow completeness step at `.github/workflows/build-pdf.yml:104-119` checks every tracked schema file and the PDF, but not every SUMMARY source or expected PDF chapter.

Acceptance criterion: missing SUMMARY entries fail PDF generation; the built document contains exactly the intended source set and expected chapter titles before publication.

#### P1.4 — No repository-wide CI quality gate exists

The only workflow is PDF build/publication. Link integrity, navigation parity, schema example validation, semantic validators, JSON-LD checks, duplicate-key checks, version/status consistency, and generated-artifact drift do not block merges.

Acceptance criterion: a required CI job runs the final regression sequence below and must pass before publication or merge to the release branch.

### P2 — material defects and risks

#### P2.1 — Three current GitBook links are confirmed live 404s

The three current schema-page directory links listed above are transformed into nonexistent `/examples/README.md` destinations. The older MeterData v0.5 link is a latent fourth risk.

#### P2.2 — Generic cross-schema validation is Windows-broken

`scripts/validate_schema.py:51-53` interpolates `os.path.relpath()` into registry URLs without normalizing Windows backslashes to URL slashes. MeterDataCredential validation exits 1 with `Unresolvable` on Windows.

This is repository portability behavior, not a missing dependency.

#### P2.3 — Generic validation materially overstates external-schema coverage

`scripts/validate_schema.py:9-43` substitutes EnergyCredential, EnergyResource, Address, and GeoJSONGeometry with permissive `{ "type": "object" }` stubs. A “100% compliant” result proves local constraints only; it does not establish conformance to those external definitions.

#### P2.4 — Generated index completeness and anchors are not controlled

`scripts/generate_index.py:4-9` uses a slugger inconsistent with the repository's GitBook rules. Numeric headings such as `faq.md:7` should produce `id-1.-...`, while generated HTML outline links omit that form. The Markdown validator does not parse the generated `<a href>` links.

The generated index also omits 15 of 66 SUMMARY pages. `SUMMARY.md:45` includes the P2P overview, while the overview list at `scripts/generate_index.py:113-120` omits it.

#### P2.5 — MeterData v0.6 source metadata is stale

`schemas/MeterData/v0.6/attributes.yaml:4-6` declares version `0.5.0` and describes six profile shapes. `schemas/MeterData/v0.6/README.md:3,7-16` identifies v0.6 and eight shapes.

`schemas/ArrFiling/v0.5/attributes.yaml:4` declares `1.0.0` while its directory and README identify v0.5; the intended versioning convention needs an owner decision before treating this second mismatch as a correction.

#### P2.6 — Migration verification is stale or false-green

- `scripts/verify_v05_v06_equivalence.py` exits 1 on current data.
- `scripts/compare_v05_v06.py` reports three differences and a missing `BillingProfile.json` but exits 0.
- `scratch/verify_no_loss.py` exits 1 on a removed `OBISMapping.json` path.

None is wired into Make or CI.

#### P2.7 — JSON-LD verification is not reproducible

`scripts/check_jsonld.py:41` imports `pyld`, but the repository has no dependency manifest declaring it and Make checks only PyYAML/jsonschema at `Makefile:3-5`. The local `ModuleNotFoundError` is an environment/tool absence; the missing dependency declaration and missing CI invocation are repository quality gaps.

#### P2.8 — Locale-default PDF writes are not portable

Direct execution under default Windows CP-1252 fails before document generation. This does not prove Ubuntu CI failure but prevents a reliably portable direct-Python build.

### P3 — maintenance defect

`schemas/MeterData/v0.5/examples/BillingProfile.json` and `schemas/MeterData/v0.5/examples/CustomerBillingSummary.json` are byte-for-byte and semantically identical across all 89 lines. The second file is not referenced by the v0.5 README and inflates example coverage without adding a distinct case.

## Exact command results

Tests used `PYTHONUTF8=1` and `PYTHONDONTWRITEBYTECODE=1` where required to keep execution read-only and avoid console-encoding noise.

```text
python -B scripts/validate_links.py
  exit 0 — 1,150 links checked, 0 reported broken

python -B schemas/MeterData/v0.6/validation/test_runner.py
  exit 0 — 6/6 fixture expectations passed

python -B schemas/MeterDataRequest/v0.6/validation/test_runner.py
  exit 0 — 4/4 fixture expectations passed

python -B schemas/MeterData/v0.6/validation/validator.py schemas/MeterData/v0.6/examples
  exit 0 — all current MeterData examples passed structural and semantic checks

python -B schemas/MeterDataRequest/v0.6/validation/validator.py schemas/MeterDataRequest/v0.6/examples
  exit 1 — Anonymised_Telemetry_Request.json profile/register incompatibility

python -B scripts/validate_schema.py schemas/MeterDataCredential/v0.6/schema.json schemas/MeterDataCredential/v0.6/examples
  exit 1 — Unresolvable MeterData v0.6 reference on Windows

python -B scripts/verify_v05_v06_equivalence.py
  exit 1 — current migration equivalence failures

python -B scripts/compare_v05_v06.py
  exit 0 — despite three reported differences and one missing counterpart

python -B scratch/verify_no_loss.py
  exit 1 — FileNotFoundError for schemas/MeterData/v0.6/OBISMapping.json

python -B scripts/generate_field_tables.py --all --check
  exit 0 — all eleven version README field-table blocks unchanged

python -B scripts/check_jsonld.py <schema-version-directories>
  exit 1 — local ModuleNotFoundError: pyld; content checks did not run

python scripts/build_pdf.py
  exit 1 under default Windows CP-1252 — UnicodeEncodeError at scripts/build_pdf.py:300

git diff --check
  exit 0
```

Additional read-only diagnostics:

- All eleven `schema.json` files passed `jsonschema.Draft202012Validator.check_schema()`.
- `SUMMARY.md` and `_sidebar.md` matched exactly for all 66 normalized titles, paths, and order positions.
- A scoped duplicate-key parser found zero JSON/YAML duplicate keys.
- Isolated temporary regeneration invoked `scripts/generate_schema_permissive.py` successfully for each Make-managed directory, but semantic JSON comparison found the five drift sets listed above.
- Local `make` absence is an environment/tool limitation, not a repository pass or failure.

## Final regression sequence

Run the release gate in a disposable fresh Linux/WSL clone with pinned Python dependencies, `mmdc`, Pandoc, Tectonic, and an explicitly supplied DEG checkout.

1. Parse every tracked JSON, JSON-LD, YAML, and YML file with object-scoped duplicate-key rejection.
2. Assert exact `SUMMARY.md` / `_sidebar.md` path, title, nesting, and order parity.
3. Run an extended Markdown check covering inline Markdown, raw HTML links, directory publishability, duplicate heading IDs, anchors, and case-sensitive path resolution.
4. Validate all eleven `schema.json` documents against the Draft 2020-12 meta-schema.
5. Validate every shipped example against its schema; treat skipped files and unresolved references as failures.
6. Run both dedicated semantic test suites and both semantic validators against all shipped MeterData and MeterDataRequest examples.
7. Run `scripts/check_jsonld.py` over all eleven schema-version directories with pinned `pyld`.
8. Run `scripts/generate_field_tables.py --all --check` and `scripts/generate_external_field_tables.py --check --schema-repo <DEG>`.
9. Regenerate every schema, context, vocabulary, and generated index artifact in the disposable clone and require `git diff --exit-code`.
10. Run repaired v0.5-to-v0.6 equivalence checks. Missing counterparts, warnings, and unexpected differences must exit nonzero.
11. Build the PDF with Mermaid rendering mandatory. Require every intended SUMMARY source, expected chapter title, valid internal link, and nonempty PDF output.
12. Stage the publication tree and assert every tracked documentation/schema asset plus the PDF is present.
13. After publication, require HTTP 200 for the PDF, representative schema artifacts, current GitBook pages, deep anchors, and schema example links.

## Kill criteria

Stop release or publication on any of the following:

- Any regression command exits nonzero.
- Clean generation produces a tracked diff.
- Any schema or example is skipped, unresolved, or validated through an unintended permissive fallback.
- Any shipped semantic example fails.
- Any local or rendered link is missing, ambiguous, or resolves to a non-page directory target.
- SUMMARY/sidebar parity differs.
- A PDF source is omitted, Mermaid silently falls back to code, expected chapters are absent, or PDF links fail.
- Any required published route returns non-200.
- Hosted GitBook state is not independently verified after GitHub publication.
- A required tool or dependency is absent. Tool absence is an infrastructure failure, never a green repository result.

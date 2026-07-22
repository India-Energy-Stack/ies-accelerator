# Post-Pull Mechanical Reassessment (After PRs #150/#151)

One-sentence take: PRs #150/#151 now only fully resolve explicit pilot calendar mentions; most mechanical defects remain unresolved, and release gates are still blocking.

## Baseline and corpus
- Branch HEAD: `repo-wide-qaqc` at `da97f89eba770800a63d187ed4b7bae6bc292acb`
- Baseline: `origin/main 9257e8580906862c1c52b158c9d971a50eb1455e`
- Tracked audience markdown files excluding `qaqc`: `79`
- Overall status summary: only explicit pilot calendar dates are fully resolved; navigation cleanup is partial; numeric anchors regressed; every schema/build/CI gate remains unresolved.

## Evidence-by-defect matrix

| Concern | Status | Current evidence |
| --- | --- | --- |
| Live GitBook directory links | UNCHANGED | Live GitBook source pages return `200` while still rendering directory destinations. 404s persist at `schemas/ArrFiling/v0.5/README.md:25`, `schemas/MeterData/v0.6/README.md:29`, `schemas/OutageNotification/v0.1/README.md:69`, plus latent unpublished MeterData v0.5 issue at line 28. |
| `validate_links.py` false-green behavior | UNCHANGED | `false-greens 988/0` because the validator path allows existing directories (`scripts/validate_links.py:131`). |
| `SUMMARY.md` / `_sidebar` target parity | RESOLVED | Links are aligned as a directory target parity check, but this does not resolve directory publishability or index parity. |
| `SUMMARY.md` / `index.md` parity | PARTIALLY RESOLVED | `Summary 57`, `index 46`, `shared 43`, `Summary-only 14`, `index-only 3`; generator reproducible, omissions remain, and `scripts/generate_index.py:111-119` still omits P2P overview. |
| Numeric anchors in index | REGRESSED | New dedicated row: `740` outline links, `262` slug mismatches, `224` numeric-label mismatches (up from `223`). Example: `index.md:119` vs `faq.md:7`; `index.md:262` vs `how-you-implement-ies/issue-credentials.md:245`. `scripts/generate_index.py:4-10` remains incompatible with GitBook behavior (`scripts/validate_links.py:24-55`). |
| Explicit pilot dates | RESOLVED | Zero tracked audience-markdown hits for `21 May 2026` or `21 June 2026`. Current wording present in `README.md:105-109`, `contributors.md:9`, `how-you-implement-ies/README.md:120`. |
| Deleted-page / duplication cleanup | PARTIALLY RESOLVED | No current refs to deleted paths; however `pathways/researcher.md:33` references a separate companion page and `:51` references concepts pages. Status text diverges (`README.md:105`, `faq.md:45`, `how-you-implement-ies/README.md:120`). Exact-paragraph scan still reports 7 duplicate groups, unchanged from baseline; semantic intent remains for Sonnet. |
| MDR validator contradiction | UNCHANGED | Dedicated validation exits `1` for kWh imp/exp under `IntervalProfile` (`example` lines `15-18`); generic `validate_schema` exits `0`. |
| Make-managed reproducibility (`make` outputs) | UNCHANGED | All 8 make-managed dirs regenerate without generator failure; exactly 12 artifacts drift across 5 dirs: `MeterData v0.5`; `MeterDataCredential v0.6`; `MeterDataRequest v0.5/v0.6`; `MeterDataRequestCredential v0.1`. Clean dirs are `ArrFiling v0.5`, `MeterData v0.6`, `OutageNotification v0.1`; `ElectricityCredential` remains separate. |
| PDF missing-source / CP1252 | UNCHANGED | Missing-source is injected but suppressed: build exits `0` because `build_pdf.py:245-270` and `304-305` drop missing-count visibility. Native Windows still fails on U+2192 via encoding-unspecified writes (`build_pdf.py:300`, `build_pdf.py:266`). |
| Windows cross-schema resolver | UNCHANGED | URL construction still uses `os.path.relpath` in `scripts/validate_schema.py:45-58`. `MeterDataCredential` validation still exits 1 with `Unresolvable .../schemas/MeterData/v0.6/schema.json`. |
| CI / release gates | UNCHANGED | Workflow coverage is only `build-pdf.yml`; publication trigger at lines `11-23` and Ubuntu publish job `37-39`; no PR-wide gates for schema/link/validator checks. |
| Metadata parity | UNCHANGED | `MeterData` attributes `:4-6` report `0.5.0/six` while README has `v0.6/eight` (`README:3`, `7-16`); `ArrFiling` attributes `:4` reports `1.0.0` while README has `v0.5` (`README:3`). |
| Migration tools | UNCHANGED | Compare reports show `3` unexpected differences and exit `0` (`compare_v05_v06.py:83-120` has no failure exit). `verify_v05_v06_equivalence.py` exits `1`; `scratch/verify_no_loss.py` crashes on removed `OBISMapping` (`56-62`). |
| JSON-LD | UNCHANGED | `pyld` import exists at `scripts/check_jsonld.py:41`; no tracked dependency manifest and no Make/CI invocation wiring. |
| Permissive external stubs | UNCHANGED | `scripts/validate_schema.py:7-43` and `scripts/check_jsonld.py:144-173` remain permissive; adversarial GeoJSON substitutions still validate with exit `0`. |
| ElectricityCredential ownership | UNCHANGED | `schemas/ElectricityCredential/README.md:5` and `schemas/ElectricityCredential/v1.2/README.md:3` still state Beckn is authoritative; `Makefile:20-22` excludes the family, and no sync/drift verifier exists. |
| Exact duplicate example pair | UNCHANGED | `schemas/MeterData/v0.5/examples/BillingProfile.json` and `CustomerBillingSummary.json` remain byte-identical at 89 lines and SHA-256 `98539B9F569B3016B445EDCD7F5C3DC3115197194FC0AB0B5601BEA1690FD70A`; only `BillingProfile.json` is referenced at `schemas/MeterData/v0.5/README.md:151`. |

## Release gate verdict
Docs link integrity must be `FAIL` (directory/README false-green outcomes at tracked 404 destinations).

Additional `FAIL`: PDF build integrity, schema reproducibility drift, semantic validator, Windows resolver, metadata parity, CI gate breadth.

## PR #150/#151 original-defect closure
- **RESOLVED:** explicit pilot calendar dates
- **PARTIALLY RESOLVED:** navigation cleanup, `SUMMARY`/`index` parity
- **REGRESSED:** numeric anchors
- **UNCHANGED:** schema/build/CI checks, MDR contradiction, reproducibility drift, PDF, cross-schema resolver, metadata mismatch, migration tooling, JSON-LD, permissive stubs, ElectricityCredential ownership, exact duplicate examples

## Final worktree hygiene
- One new untracked report file is present: `qaqc/04_POST_PULL_MECHANICAL_REASSESSMENT.md`.
- No source files, earlier audits, or generated artifacts remain modified.

## Preserved retractions
- Prior retracted claims (e.g., naive id-* and earlier noise claims) remain retracted unless explicitly re-proven in a future pass.

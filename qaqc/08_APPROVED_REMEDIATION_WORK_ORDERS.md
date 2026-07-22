# Approved Remediation Work Orders

**Arbitration decision on `qaqc/07_DRAFT_REMEDIATION_ARBITRATION_BRIEF.md`: APPROVED WITH CHANGES.**

**Baseline:** branch `repo-wide-qaqc`, local HEAD `73365db` (content baseline `6db16af`, incorporating upstream `9257e85`). Binding evidence: `qaqc/02`, `qaqc/04`, `qaqc/05`, `qaqc/06`. This document authorizes execution; it makes **no release-readiness claim** — the final regression sequence and kill criteria in `qaqc/02` (§ "Final regression sequence", § "Kill criteria") remain controlling for any release decision.

## 1. Judgment

The q07 draft is structurally sound: its role contract, non-negotiable boundaries, and separate-authorization lanes are accepted as written. It is approved **with changes** because it left four items to arbitration that must be operational before dispatch, and this order settles them:

1. **Batch 3 is isolated** into its own wave (A2) with its own checkpoint and QE gate. Rationale: it is the largest single edit surface in the docs-only set (two files, ~16 cited line anchors per ISS-019/LIR-008), it is the only P1-linked batch this authorization **fully closes** — the authorized waves carry three P1-linked batches (2a/ISS-001, 3/ISS-019, 8a/ISS-018), and 2a and 8a are **partial** closures only, because their counterpart lanes 2b and 8b remain unauthorized (§5) — it shares a file (`use-cases-overview/consumer-meter-digest.md`) with Batch 7, and it must hold the line-76 exclusion boundary against Batch 8b. Bundling it with the six other bounded documentation batches would make the QE diff review materially harder and raise the risk of an 8b leak passing unnoticed.
2. **Batch 8a may proceed without prejudging `OD-E2`**, with the exact boundary defined in §4. The q07 phrase "deterministic credential-root command/input boundary" is made precise there.
3. **The first Spark target is selected** (directory-target link class, §6), not deferred. It is fully evidenced by `qaqc/02` P2.1 and `qaqc/04` (UNCHANGED rows), needs no owner decision, and does not touch slug mechanics, navigation membership, `index.md`, or Pathways.
4. **Checkpoint boundaries, QE gates, the orchestrator pre-commit checklist, and the local-only rule** are defined in §§7–8.

Everything else in q07 stands unchanged, including: Batches 2b and 6 separately unauthorized (§5); Batch 8b blocked pending recorded `OD-E2` (§4); no inference of any of `OD-E1` through `OD-E8` by any party; `SUMMARY.md`/`_sidebar.md` parity (66/66 per `qaqc/02`) is an invariant, not a work item.

## 2. Role contract (binding)

- **Primary orchestrator (root):** high-level dispatcher; owns scope, dispatch order, checkpoint commits, and final acceptance. Performs no remediation edits.
- **Fable (this document's author role):** second-in-command arbiter; approves/blocks work orders, resolves scope collisions, enforces stop conditions. Performs no production-file edits.
- **Sonnet 5:** sole semantic implementation executor; executes §3 and §4 work orders exactly as written.
- **Spark (GPT-5.3 Codex):** bounded mechanical executor; one approved mechanical work order at a time; first target is §6 only.
- **Independent quality engineer (QE):** verifies scope, evidence, behavior, and acceptance results without relying on executor self-report; gates every checkpoint commit.

Executors do not commit, stage, or push. Only the primary orchestrator commits, and only after the QE gate for that wave passes. All work stays local on `repo-wide-qaqc`; **no push**. Commit subjects/bodies contain no model, authorship, or provenance wording.

## 3. Wave A1 — Sonnet work order (Batches 1, 2a, 4, 5, 7, 8a)

**Dispatch precondition:** this authorization document (`qaqc/08`) independently QE-accepted and checkpoint-committed, with `git status --short` clean, before any Wave A1 dispatch.

Execution order within the wave: 1 → 2a → 4 → 5 → 7 → 8a. Line anchors below are content-baseline (`6db16af`) anchors; where an earlier batch in this wave has shifted lines, locate by the quoted text, never by renumbered position.

### Writable files (exactly ten; nothing else)

1. `schemas/MeterData/v0.6/ReferenceGuide.md` (Batch 1)
2. `what-ies-provides/schemas-overview/meter-data-request.md` (Batch 2a)
3. `pathways/researcher.md` (Batch 4)
4. `pathways/utility.md` (Batch 4)
5. `what-ies-provides/schemas-overview/meter-data-credential.md` (Batch 5)
6. `schemas/README.md` (Batch 7)
7. `use-cases-overview/consumer-energy-passport.md` (Batch 7)
8. `use-cases-overview/consumer-meter-digest.md` (Batch 7 — line 58 standards-order pointer **only**)
9. `use-cases-overview/smart-meter-data-exchange.md` (Batch 7 — line 71 standards-order pointer **only**)
10. `how-you-implement-ies/conformance.md` (Batch 8a — line 79 **only**)

### Read-only evidence (consult; never edit)

`schemas/MeterData/v0.6/IES codes.json` (esp. :338-348, :352-366, :453-467, :468-479); `schemas/MeterDataRequest/v0.6/validation/README.md:7-11`; `schemas/MeterDataRequest/v0.6/validation/test_cases/valid_request.json:7-10` and `invalid_request_profile_mismatch.json:7-10`; `schemas/MeterData/README.md` ("Nine record shapes"); `what-ies-provides/schemas-overview/README.md:10`; `schemas/MeterDataCredential/README.md` (DeDi-registry revocation wording); `what-ies-provides/register.md` (real heading names); `README.md:34` (`## What IES is not`); all eleven `schema.json`/`attributes.yaml` pairs under `schemas/` (for the Batch 7 `x-standard` scope: singular key, present only in `ElectricityCredential/v1.2` and `OutageNotification/v0.1`); `scripts/validate_schema.py:9-43`; `qaqc/06` §§7, 9.

### Exact corrections

- **Batch 1** — `ReferenceGuide.md:9`: replace "eight distinct profile shapes" with a cadence/telemetry-scoped statement that also names `DESCRIPTOR`/`PayloadDescriptorProfile` as the shared ninth, non-requestable shape (model: `what-ies-provides/schemas-overview/README.md:10`). Do **not** edit the seven other locations reinspected as correct in ISS-002; never describe `DESCRIPTOR` as requestable.
- **Batch 2a** — `meter-data-request.md`: (a) in the worked example at :32-44, replace `kWh imp`/`kWh exp` with `kWh imp block`/`kWh exp block` (the `IntervalProfile`-permitted registers per `IES codes.json:453-467,468-479` and `valid_request.json`); (b) at :126, replace the false "`DailyProfile`-only" claim with the actual permitted set for plain `kWh imp`: `DAILY`, `MONTHLY`, `INSTANTANEOUS`. Do **not** touch `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json` (that is Batch 2b, unauthorized).
- **Batch 4** — `pathways/researcher.md:33`: reword "page" to "section" and link `../README.md#what-ies-is-not`. `:51`: replace "the concepts pages" with a concrete existing referent per ISS-010's recommendation. `pathways/utility.md:55,67`: replace the labels "Resolution & Routing Specification" and "Appendix D" with the actual `register.md` section names; keep the already-resolving anchors.
- **Batch 5** — `meter-data-credential.md` §6 and §11 item 2: remove or correct the false claim that the family `README.md` describes "BitstringStatusListEntry" revocation; the family README states DeDi-registry revocation (`credentialStatus.type: dediregistry`).
- **Batch 7** — `schemas/README.md:87,94` and `use-cases-overview/consumer-energy-passport.md:61,159`: remove the universality claims; state the observed scope (singular `x-standard`, per-field, present in two of eleven schema-version directories; zero `x-standards-precedence` anywhere). Preserve the canonical standards order at `schemas/README.md:89-92` unchanged. `consumer-meter-digest.md:58` and `smart-meter-data-exchange.md:71`: replace each copied standards-order rule with a short pointer to `schemas/README.md:89-92`.
- **Batch 8a** — `conformance.md:79` only, per the §4 boundary below.

### Forbidden changes (Wave A1)

Any file not in the writable list; any `.json`, `.yaml`, `.jsonld`, generated artifact, or anything under any `examples/` directory; `SUMMARY.md`, `_sidebar.md`, `index.md`, `.gitbook.yaml`; any `scripts/*` or `Makefile`; `conformance.md` lines 33, 72, 76, 83, 95; `how-you-implement-ies/build-adapter.md`; `use-cases/consumer-meter-digest/README.md` (all of it — Wave A2/8b territory); any qaqc file; any navigation membership, page addition/removal, or heading restructure; any wording that adopts a status posture (`OD-E1`), conformance posture (`OD-E2`), or any other OD-E position.

### Stop conditions (halt, report to orchestrator, no improvisation)

Quoted anchor text not found at or near the cited location (baseline drift); a correction requires touching a file outside the writable list; evidence contradicts a q06 correction target; two plausible correction wordings would take different OD-E positions; `git status` shows any unexpected path.

## 4. Wave A2 — Sonnet work order (Batch 3, isolated) and the 8a/8b boundary

**Dispatch precondition:** Wave A1 QE-accepted and checkpoint-committed.

**Writable files (exactly two):** `use-cases-overview/consumer-meter-digest.md`; `use-cases/consumer-meter-digest/README.md`.

**Read-only evidence:** `schemas/MeterData/v0.6/schema.json`; `schemas/MeterDataCredential/v0.6/README.md` and `schema.json`; `use-cases/smart-meter-data-exchange/ies-meter-data-model.md:41-45`; `schemas/MeterData/v0.6/examples/MultiMeterBulkDataset_Elaborated.json:277-285`; `how-you-implement-ies/issue-credentials.md:292,299`; `schemas/MeterDataRequestCredential/README.md:22` and `v0.1/README.md:100`; `qaqc/06` ISS-019/LIR-008.

**Exact corrections (per ISS-019):** at overview `:28,32,52,79,85,103,127` and guide `:25,33,35,50,62-63,69-70,74,87` (baseline anchors; locate by quoted content since Wave A1's line-58 edit may shift the overview): replace the non-schema payload model (`meterReference`, `period`, `summary` with `SUMMARY_TOTAL`/`SUMMARY_PEAK`/`SUMMARY_TOD`, `dataQuality`, `RAW_15M`) with the actual compiled fields (`profileType`, `meterRefs`, `intervalPeriod`/`timePeriod`, `intervals`/`readings`, `validationStatus`); express fifteen-minute data as `profileType: INTERVAL` plus `intervalPeriod.duration: PT15M`; reframe derived summaries explicitly as downstream analytics outside the current credential schema, or remove them; replace both non-canonical OpenCred IDs with `ies/meter-data-credential/v0.6`; replace singular `requiredCredential` with `offerAttributes.policy.requiredCredentials`; express granularity/range policy in prose, removing the undefined `granularityOptions`/`maxRange` keys. Guide line 75 is valid and unchanged.

**Batch 8a/8b line and concept boundary (binding on both waves):**

- **Line boundary:** 8a's entire writable surface is the single prose statement at `how-you-implement-ies/conformance.md:79`. The command it describes is not edited. Lines 33, 72, 76, 83, and 95 of `conformance.md`, all of `how-you-implement-ies/build-adapter.md` (including :100-110, :120, :157), and `use-cases/consumer-meter-digest/README.md:76` are 8b surface and may not be touched by 8a, Wave A1, or Wave A2.
- **Concept boundary:** 8a may state only what the cited command's input actually is — the credential-root document validated against the credential-root schema, not an isolated `credentialSubject`. It may make **no statement in either direction** about external-schema stubs, the degree of conformance any check establishes, validation sufficiency, or production readiness — neither strengthening nor caveating those claims, because either direction adopts an `OD-E2` posture. Batch 3 observes the same rule: guide line 76 ("schema validation passes") is left byte-identical; Batch 3's own rewording may not import stub-coverage or conformance-sufficiency language anywhere.
- **8b remains blocked** until an owner decision on `OD-E2` is recorded in writing. No executor, and neither Fable nor the orchestrator, may infer `OD-E1` through `OD-E8`.

**Forbidden changes (Wave A2):** only the two writable files above may be modified, and within them only the Batch 3 anchors and concepts listed in this section are editable. Preserved byte-identically: the Wave A1 Batch 7 standards pointer in the overview (the line-58 pointer as landed by Wave A1), guide line 75, the owner-gated guide line 76, and every other 8b surface line (§4); all non-Batch-3 prose in both files. Untouched entirely: every schema, example, `.json`/`.yaml`/`.jsonld`, generated artifact; `SUMMARY.md`, `_sidebar.md`, `index.md`, `.gitbook.yaml`; any qaqc file; any `scripts/*` or `Makefile`; any navigation membership, page addition/removal, or heading restructure; any wording adopting an `OD-E1`–`OD-E8` posture.

**Stop conditions (Wave A2 — halt, report to orchestrator, no improvisation):** a correction appears to require any edit outside the two writable files or outside the Batch 3 anchors/concepts; a correction seems to require editing a schema artifact or example (that would be a new authorization lane, not this batch); a wording choice would adopt any OD-E posture; evidence contradicts an ISS-019 correction target; quoted anchor text cannot be located at or near the cited location; `git status` shows any unexpected path.

## 5. Separately unauthorized lanes (unchanged from q07)

Not authorized by anything in this document; each requires its own future authorization and checkpoint:

- **Batch 2b** — `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json:15-18` (artifact edit; acceptance already recorded in `qaqc/06` §9: registers become `kWh imp block`/`kWh exp block` and `validation/validator.py` exits 0).
- **Batch 6** — `schemas/MeterData/v0.6/attributes.yaml:4-6` (source edit via the schema-change proposal flow; `OD-S1` settles content, authorization does not yet exist).
- **Batch 8b** — owner-gated on recorded `OD-E2` (§4).
- Every carried technical release blocker in `qaqc/02`/`qaqc/04` (schema reproducibility drift, PDF false-green, Windows resolver, CI breadth, migration tooling, JSON-LD wiring, ElectricityCredential ownership, duplicate example pair): governed exclusively by the `qaqc/02` regression sequence and kill criteria, out of scope for Sonnet and for this Spark order.

## 6. Wave B — first Spark work order: directory-target link class

**Selection:** from the q02/q04 candidate families, the first Spark target is **directory-target link detection and repair** (`qaqc/02` P2.1 + validator gap at `scripts/validate_links.py:131`; `qaqc/04` rows "Live GitBook directory links" and "`validate_links.py` false-green behavior", both UNCHANGED). The repair shape is the **collection-index solution**: each of the four `./examples` links intends the directory as a collection, so the semantically faithful fix is to supply the missing `<dir>/README.md` publish target as a mechanical index of that directory's example files — not to retarget any parent link to a single arbitrary example. The parent links and their four source READMEs remain unchanged and read-only. The index slug-reuse family is expressly **not** selected first: it is entangled with `OD-E4` (`index.md` role) and adjacent to navigation membership (ISS-012), and this order forbids combining stable slug mechanics with navigation membership, content, or role in any single work order. Any future index-role or Pathways-publication change requires recorded `OD-E4`/`OD-E6` before dispatch.

**Owner preconditions:** none for this target. **Dispatch preconditions:** Waves A1 and A2 QE-accepted and checkpoint-committed; `git status --short` clean. At this clean post-A2, pre-B dispatch point, run `python -X utf8 -B scripts/validate_links.py` and record the baseline dynamically as **N checked / 0 broken**. Do not use the stale 1,150 figure or the current pre-A1 989 figure as the Wave B baseline.

**Writable files (exactly five; the four index files are NEW):**

1. `scripts/validate_links.py` — the directory-target acceptance at `:131` only
2. `schemas/OutageNotification/v0.1/examples/README.md` — new index file
3. `schemas/MeterData/v0.6/examples/README.md` — new index file
4. `schemas/ArrFiling/v0.5/examples/README.md` — new index file
5. `schemas/MeterData/v0.5/examples/README.md` — new index file

**Read-only evidence:** `qaqc/02` §"Directory links" and P2.1; `qaqc/04` matrix rows cited above; the four parent READMEs containing the `./examples` links (`schemas/OutageNotification/v0.1/README.md:69`, `schemas/MeterData/v0.6/README.md:29`, `schemas/ArrFiling/v0.5/README.md:25`, `schemas/MeterData/v0.5/README.md:28`); the four `examples/` directory listings.

**Reproduced failing fixture (required before any repair edit):** implement the detection change first — a relative link whose resolved target is a directory is broken unless `<dir>/README.md` exists (the GitBook publish target). With **only** the validator changed and **before** any index file is created, run `python -X utf8 -B scripts/validate_links.py`: it must report **exactly the four** known directory links above as broken (this reproduces, in-repo, the live-404 failure `qaqc/02` verified externally, against the previous false-green 0-broken result). If it reports more or fewer than four, **stop** (kill criterion) and report the delta without fixing anything.

**Repair rule (deterministic, no semantic choice):** create the four new `examples/README.md` index files. Each index is byte-deterministic:

- Line 1 — exact H1 template `# <SchemaFamily> <version> examples`, with the four exact substitutions: `# OutageNotification v0.1 examples`, `# MeterData v0.6 examples`, `# ArrFiling v0.5 examples`, `# MeterData v0.5 examples`.
- Line 2 — exactly one blank line.
- Then exactly one bullet per existing `*.json` file in the index's **own** directory. Each bullet is a Markdown link list item built deterministically from two tokens: the **label token** is the exact filename (byte-for-byte, including extension), and the **target token** is `./` immediately followed by that same exact filename. The bullet line is exactly: hyphen, one space, then the Markdown link formed by placing the label token in square brackets immediately followed by the target token in parentheses, with no characters between or after them. And **no other content** of any kind: no other links, no omissions, no extras, no semantic summaries or descriptions of example content.
- Bullet ordering is Python `sorted(filename)` order — Unicode code-point order, case-sensitive. Do **not** use PowerShell `Sort-Object` or any other culture/locale-aware sort, which can disagree with code-point order on case and punctuation.

At the current baseline the per-directory `*.json` counts are **2** (`OutageNotification/v0.1`), **26** (`MeterData/v0.6`), **1** (`ArrFiling/v0.5`), and **10** (`MeterData/v0.5`) — **39** links total. If the actual counts at dispatch differ from 2/26/1/10, **stop** and report before creating anything.

**Acceptance commands (all must pass; executors and QE never stage, so all evidence below is pre-stage — the four new READMEs are untracked and therefore invisible to `git diff`):**

1. `python -X utf8 -B scripts/validate_links.py` → exit 0, reporting exactly **N+39 checked / 0 broken** against the recorded pre-B baseline. If the delta differs from +39, **stop**. Active detection is proven exclusively by the QE-owned out-of-repo fixture test in §7 gate 6 — no production index file is ever removed or renamed.
2. `git status --short` → exactly one modified line for `scripts/validate_links.py` plus exactly four `??` lines for the new index paths (`schemas/OutageNotification/v0.1/examples/README.md`, `schemas/MeterData/v0.6/examples/README.md`, `schemas/ArrFiling/v0.5/examples/README.md`, `schemas/MeterData/v0.5/examples/README.md`); nothing else.
3. `git diff --name-only` → exactly `scripts/validate_links.py` and nothing else (the four new READMEs are untracked, so their correct state is **absence** from this output).
4. `git ls-files --others --exclude-standard` → exactly the four new index paths; nothing else.
5. `git diff --check` → exit 0 (this covers the tracked script only; it cannot see untracked files).
6. Untracked-README hygiene check (because `git diff --check` cannot reach them): `rg -n -e '[ \t]+$' -e '^(<{7}|={7}|>{7})' schemas/OutageNotification/v0.1/examples/README.md schemas/MeterData/v0.6/examples/README.md schemas/ArrFiling/v0.5/examples/README.md schemas/MeterData/v0.5/examples/README.md` → **no matches** (nonzero rg exit), confirming no trailing whitespace and no conflict markers in any of the four untracked files.
7. `git diff` on `scripts/validate_links.py` confined to the directory-target handling; the GitBook slug rules at `:24-55` byte-identical.
8. `SUMMARY.md` and `_sidebar.md` absent from the diff and from `git status --short` — the already-passing 66/66 parity (`qaqc/02`) is preserved untouched.

**Regression boundary:** every link passing at the recorded **N / 0** pre-B baseline must still pass; totals may change only by the +39 links introduced by the four new indexes. No changes to slug/anchor logic, remote-URL handling, HTML-link handling, `SUMMARY`/`_sidebar`/`index` files, any parent README, any schema artifact or JSON example, or any file outside the writable five.

**Forbidden changes:** everything outside the writable five; the four parent READMEs, including their `./examples` links, are read-only and remain byte-identical — they resolve via the new indexes, not by retargeting; within `validate_links.py`, anything beyond the directory-target rule; no navigation membership, content, or role changes; no edits to any `*.json` example or other schema artifact; no bundling of link validation with index generation (`index.md` role), schema generation, PDF, CI, or portability work.

**Kill criteria:** detection reproduces ≠ 4 known directory links; any per-directory `*.json` count differs from 2/26/1/10; the validator delta differs from +39; any acceptance command fails twice; any edit outside the writable surface becomes necessary; any newly discovered P1 condition. On any kill: halt, leave the worktree as-is, report to the orchestrator.

## 7. QE gates and checkpoints

One checkpoint per wave (A1, A2, B), each gated thus before the orchestrator commits:

1. **Scope:** Waves A1/A2 — `git status --short` and `git diff --name-only` show only that wave's writable files. Wave B (all pre-stage; executors and QE never stage) — `git status --short` shows exactly one modified `scripts/validate_links.py` plus exactly four `??` new index paths; `git diff --name-only` shows exactly `scripts/validate_links.py`; `git ls-files --others --exclude-standard` shows exactly the four new index paths; `git diff --check` exits 0 (tracked script only); and the §6 untracked-README hygiene `rg` check over all four untracked READMEs returns no matches.
2. **Acceptance:** every acceptance test for that wave's batches (as written in `qaqc/06` §9 and §§3–6 above) verified by QE directly, not from executor self-report.
3. **Boundary:** QE confirms byte-identical state of all 8b surface lines (§4), `SUMMARY.md`, `_sidebar.md`, `index.md`, and every `.json`/`.yaml`/`.jsonld`/`examples/` path (Waves A1/A2).
4. **No pre-empted decisions:** QE greps the diff for wording adopting any `OD-E1`–`OD-E8` posture.
5. **Token re-search (A2):** the six ISS-019 disputed tokens (`SUMMARY_TOTAL`, `SUMMARY_PEAK`, `SUMMARY_TOD`, `meterReference`, `dataQuality`, `RAW_15M`) no longer appear in the two Digest pages as current-schema field claims, and still have zero matches under `schemas/`.
6. **Index bijection and active detection (B):** QE verifies each of the four new `examples/README.md` files matches the §6 byte-deterministic template exactly — the exact H1, one blank line, then `sorted(filename)` code-point-ordered bullets forming an exact bijection over its own directory's `*.json` files (2/26/1/10; 39 total) — no omission, no extra, no non-bullet links, no semantic summaries. Active detection is proven with a **QE-owned disposable fixture outside the repo** — no production index file is ever removed or renamed: (a) record production worktree state first — `git status --short` output plus content hashes of the modified script and the four untracked READMEs (e.g., `git hash-object` on each); (b) create a temporary root outside the repo containing `parent.md` and an `examples` directory, where `parent.md` contains a single Markdown link whose link label is `Examples` and whose relative target is `./examples` (label and target composed in standard Markdown inline-link form inside the fixture file only); (c) run `python -X utf8 -B scripts/validate_links.py` against the fixture **before** `examples/README.md` exists → exactly **1 checked / 1 broken**, nonzero exit; (d) create `examples/README.md` in the fixture and re-run `python -X utf8 -B scripts/validate_links.py` against the fixture → exactly **1 checked / 0 broken**, exit 0; (e) fixture deletion is guaranteed in a `finally` block, executed even on test failure; (f) re-capture production `git status --short` and the same hashes and confirm byte-identical to (a) — the fixture test must leave the production worktree provably unchanged. The actual Wave B acceptance result remains `python -X utf8 -B scripts/validate_links.py` at **N+39 checked / 0 broken** on the production tree.

## 8. Primary orchestrator pre-commit checklist (every checkpoint)

1. QE gate for the wave recorded as passed.
2. `git status --short` — Waves A1/A2: only authorized files, no untracked strays. Wave B: exactly one modified `scripts/validate_links.py` plus exactly the four `??` new index paths (these untracked entries are the authorized state, not strays); nothing else.
3. `git diff --check` — exit 0 (Wave B: tracked script only; the four untracked READMEs are covered by the §6 `rg` hygiene check, verified at the QE gate).
4. `python -X utf8 -B scripts/validate_links.py` — exit 0 (Waves A1/A2 must not regress it; Wave B per §6: **N+39 checked / 0 broken**).
5. `python -B scripts/generate_field_tables.py --all --check` — exit 0 (unchanged field-table blocks; docs edits must not touch generated table regions).
6. `SUMMARY.md`/`_sidebar.md` not in the diff.
7. **Staging (root only, after the QE gate passes — executors and QE never stage):** the orchestrator stages exactly the authorized paths for the wave (Wave B: `git add scripts/validate_links.py schemas/OutageNotification/v0.1/examples/README.md schemas/MeterData/v0.6/examples/README.md schemas/ArrFiling/v0.5/examples/README.md schemas/MeterData/v0.5/examples/README.md`); verifies `git diff --cached --name-only` lists exactly those paths and nothing else; runs `git diff --cached --check` → exit 0; then commits.
8. Commit subject/body: plain description of the content change; **no model, authorship, generated-by, co-author, or provenance wording**.
9. Commit is local to `repo-wide-qaqc`; **do not push**. No tags, no branch changes, no publication action.

## 9. Closing constraint

Completion of Waves A1, A2, and B remediates documentation-semantic defects and one mechanical link class only. `qaqc/02` P1.1 through P1.4 all remain open; this document also does not close the `OD-E`-gated items or any carried FAIL gate, and supports no release, publication, or "release-green" statement. Release readiness is determined solely by the full `qaqc/02` final regression sequence executed under its kill criteria.

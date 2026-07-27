# Current-State Reconciliation

**Read-only governance record. Confers no release-readiness status. Records no owner decision.** This document reconciles `qaqc/02`, `qaqc/06`, `qaqc/09`, `qaqc/10` against the live repository at dispatch and lists what has changed since `qaqc/10` was written. It supersedes no prior qaqc file's role, dependency, or owner gates; it supplies current evidence where the tree has moved.

---

## 1. Verdict

**The repository remains NOT RELEASE-GREEN.** `qaqc/02`'s 13-step Final regression sequence and Kill criteria remain the sole controlling release gate, exactly as `qaqc/09` §1/§11 and `qaqc/10` §1/§8 state. Since `qaqc/10`, code has landed for two previously-open items — WP-B (directory-link detection) and the P1.3 half of PDF integrity — but neither has cleared independent verification for package closure, no `OD-E` decision has been recorded, and `qaqc/11_OWNER_DECISION_LEDGER.md` still does not exist.

---

## 2. Baseline

- Branch `repo-wide-qaqc`, HEAD `bf9d8b0d4480923899b3e2e7326789e12db5c7f8`, worktree clean except this file (`qaqc/12_CURRENT_STATE_RECONCILIATION.md`, untracked) at dispatch.
- `origin/repo-wide-qaqc` equals local HEAD exactly (`bf9d8b0`), confirmed post-push.
- `origin/main` is `1198bb6cffab42539e275791fa508d12eee236d8`. It is now fully merged into `repo-wide-qaqc` via `bf9d8b0` (`Merge latest main schema catalog presentation`). At this update point there is no known unmerged `origin/main` delta.
- `bf9d8b0` imported exactly nine paths — `scripts/generate_schemas_ies.py` plus eight `schemas-ies/` pages — all nine byte-identical to `origin/main`; no `schemas/**` or other path changed. `schemas/**` remains byte-identical to the merge base throughout: no schema source, compiled artifact, or example has been mutated since `qaqc/10`.

---

## 3. Commit reconciliation (since `qaqc/10`'s `df65e7a` baseline)

- **`aa0bbd7` — Validate directory links through collection indexes.** Implements WP-B in-repo: `scripts/validate_links.py:131` now treats a directory target as publishable only when a README index exists; adds four deterministic `examples/README.md` indexes (`ArrFiling/v0.5`, `MeterData/v0.5`, `MeterData/v0.6`, `OutageNotification/v0.1`), raising checked links 994→1033 per the commit's own count. Confirmed live: all four index files exist; the directory-target check is present. The in-repo function is accepted as landed code; **hosted GitBook verification of the four new pages remains final-regression evidence** (step 13 of `qaqc/02`'s sequence), not established by this record.
- **`60a4fb7` — Fail PDF builds on incomplete source sets.** `scripts/build_pdf.py:main()` now returns `1 if missing else 0` (confirmed live) instead of unconditionally `0`. Adds `scripts/verify_pdf.py`, an independently-reimplemented SUMMARY.md parser/filter/path-safety checker that asserts against the producer's output rather than trusting it, plus a PDF smoke check and a staged-`public/` mirror check. `.github/workflows/build-pdf.yml` now runs `verify_pdf.py --pdf` and `verify_pdf.py --public-root`, installs `poppler-utils` for the smoke check, and adds a `cmp -s` byte-identity check between `build/ies_accelerator.pdf` and `public/ies-report.pdf`. An independent reviewer (C1) evaluated this work against a negative-fixture suite and found it **PARTIAL/FAIL for package closure**: duplicate valid SUMMARY entries and silent single-source omission still produce a false-green exit; malformed producer input is not itself rejected by the independent layer; Mermaid-renderer availability in the build environment is asserted but not proven by any fixture. P1.3's core defect (silent partial-book exit 0) is fixed in code; the package does not close on that basis alone.
- **`6a0d39c` — Expand Consumer Energy Passport schedules.** Owner-requested initial expansion of Schedules I/II content, not a base-package deliverable.
- **`28df837` — Merge current main schema catalog updates.** Merges `a764b19` (current `origin/main` at merge time) into `6a0d39c`, plus folds a duplicate-anchor correction. Scope: 12 paths. Result at that point, historical: `schemas-ies/` contained 8 files (`README.md` + 7 family pages) totaling 118 headings, 0 duplicate anchors, via a `_dedupe_title`/page_title helper that qualified field-table labels as H3 headings. This helper and its H3 label qualification were **structurally superseded by `bf9d8b0`** (below) — current `main`'s design renders all field-table labels as bold text (`bold_label=True`), not headings, eliminating the anchor class the helper was built to disambiguate. This is a supersession of design, not a regression or a retained branch divergence.
- **`3c8a001` — Correct Consumer Energy Passport schedule provenance.** Own diff (`git diff --stat 28df837 3c8a001`) touches exactly one file, `use-cases-overview/consumer-energy-passport.md` (109 insertions, 97 deletions). Independent semantic and schema QE passed on this correction. Sections outside §§8–9 and all 16 rows of the canonical-register table (§9.4) are unchanged; no `schemas/**` or `schemas-ies/**` file is touched.
- **`bf9d8b0` — Merge latest main schema catalog presentation.** Merges current `origin/main` (`1198bb6`) into `3c8a001`, bringing GitBook native cards, frontmatter, and simplified field descriptions (standards-provenance wording dropped) to `schemas-ies/`. Scope confirmed live: exactly nine paths — `scripts/generate_schemas_ies.py` plus eight `schemas-ies/` pages (`README.md` + 7 family pages) — all nine byte-identical to `origin/main`; no `schemas/**` or other path changed. Structurally, this commit eliminates field-table heading anchors entirely: current-main's generator renders field-table labels as bold text (`bold_label=True`) rather than as H3 headings, which is what supersedes `28df837`'s `_dedupe_title`/page_title helper (above).

---

## 4. Evidence table for current gates

| Gate | Status | Current evidence |
|---|---|---|
| Structured parse / duplicate-key rejection | PARTIAL | `qaqc/02` found zero duplicate keys via an object-scoped parser; not re-run this pass. No JSON/YAML/YML file has changed since (`schemas/**` diff empty; other changes are Markdown/Python). |
| Navigation parity (`SUMMARY.md`/`_sidebar.md`) | PROVEN | Verified live this pass: 65 linked entries in each file, positions match. |
| Schema syntax (Draft 2020-12) | PARTIAL | `qaqc/02` passed all 11 `schema.json` files; not re-run this pass; files unchanged since (confirmed via `schemas/**` diff). |
| Field-table freshness | PARTIAL | `qaqc/02`/`qaqc/09` confirmed `generate_field_tables.py --all --check` exits 0 for all 11 version READMEs; not re-run this pass; no schema/README touched by intervening commits. |
| `schemas-ies/` generation + anchor uniqueness | PROVEN | Verified live this pass, independently gated post-`bf9d8b0`: `scripts/generate_schemas_ies.py` regenerates 8/8 files matching current committed output; resulting `schemas-ies/` carries 8 files, 33 headings, 0 H3 field-table headings, 0 duplicate GitBook slug groups; the four previously affected H1 anchors each occur exactly once. (The 118-heading figure is `28df837`-era historical evidence only — see §3/§8; current-main's bold-label design carries no field-table heading anchors to duplicate.) |
| Link integrity | PROVEN | Verified live this pass: `python -B scripts/validate_links.py` → 1066 checked, 0 broken. |
| WP-B (directory-link detection + indexes) | PARTIAL | In-repo function confirmed landed and exercised (four index files present, detection code present). Hosted GitBook resolution of the four new pages is unverified — MISSING pending final regression. |
| Passport schedules (§§8–9) | PROVEN | `3c8a001` own diff scoped to one file; independent semantic/schema QE passed per commit record; register table (16 rows) unchanged. |
| PDF integrity (build + publish) | FAIL | `build_pdf.py` code fix confirmed live (nonzero exit on missing sources); `verify_pdf.py` and workflow identity checks confirmed live. Current post-`bf9d8b0` reconstruction is positive: producer 66/66 and verifier 66/66 exact against the current `SUMMARY.md` source set. This positive count does **not** change closure status — C1's negative-fixture pass (§5) still found duplicate-entry and silent-omission false-green paths and unvalidated malformed input, and Mermaid-renderer availability remains asserted, not proven, by any fixture. Closure FAILS. |
| Shipped example semantics (MDR) | FAIL | Verified live this pass: `python -X utf8 -B schemas/MeterDataRequest/v0.6/validation/validator.py schemas/MeterDataRequest/v0.6/examples` — "Semantics audit FAILED" on `Anonymised_Telemetry_Request.json`. Unchanged since `qaqc/02`/`qaqc/09`. |
| Schema reproducibility (generator unification) | FAIL | Verified live this pass: `Makefile:22` still filters out `ElectricityCredential`; `Makefile:42` still invokes `generate_schema_permissive.py`. |
| Generic cross-schema validator (Windows resolver + stub scope) | FAIL | Verified live this pass: `scripts/validate_schema.py:51` still constructs URLs via unnormalized `os.path.relpath`. Permissive external-schema stubs unchanged. |
| Generated index (`index.md`) | FAIL | Not touched by any commit since `qaqc/09`; P2P-overview omission and slugger divergence both carried unchanged. |
| Migration tooling | FAIL | Not touched by any commit since `qaqc/09`; carried false-green/exit-1 states unchanged. |
| JSON-LD validation wiring | MISSING | `scripts/check_jsonld.py` still imports `pyld` with no dependency manifest anywhere in the repository; not wired to Make or CI. |
| CI breadth | FAIL | `.github/workflows/` contains exactly one file, `build-pdf.yml`, confirmed live this pass. |
| Publication / hosted routes | MISSING | No hosted-GitBook verification has been performed for any wave, including the new WP-B index pages or the Passport schedule correction. Reserved for `qaqc/02` step 13. |

---

## 5. PDF integrity — C1 finding and recommended (not dispatched) remediation design

C1's negative-fixture review of `60a4fb7` found the independent-verification layer PARTIAL/FAIL for closing the P1.3/WP-P1.3-P2.8 package:

- A SUMMARY.md fixture with a duplicate valid entry, or one that silently omits a real source, still produces a green (`exit 0`) result.
- `verify_pdf.py`'s independence is architectural (its own parser/filter/path-safety logic), but malformed producer-side input is not itself rejected as a distinct failure class.
- Mermaid-diagram rendering availability in the CI build environment is asserted by the workflow's dependency install step but is not proven against any fixture — a silent fallback to code-block rendering would not be caught.

**Recommended remediation design, NOT DISPATCHED:**

1. A checked-in, ordered manifest of expected SUMMARY sources, treated as an independent oracle separate from both `build_pdf.py`'s and `verify_pdf.py`'s own parsing of `SUMMARY.md`.
2. Strict parsing with hard rejection of duplicate source entries (not silent dedup) and of any entry that resolves outside the expected source set.
3. Independent producer and verifier implementations that share no parsing/filtering code path — extending `verify_pdf.py`'s existing independence boundary to close the malformed-input gap.
4. A fixture suite covering: duplicate entry, silent omission, malformed entry, and a Mermaid-availability probe with an expected-failure fixture if the renderer is absent.
5. A five-file provisional allowlist for the work, to be confirmed by Fable scoping before dispatch.

Formal dispatch of this design remains gated on a recorded `OD-E7` outcome (Windows/portability posture governs the P2.8 half of the combined WP-P1.3-P2.8 package) and on Fable ratification of the exact allowlist. Neither is decided by this record.

---

## 6. Owner-input ledger status

`qaqc/11_OWNER_DECISION_LEDGER.md` does not exist. All eight `OD-E` decisions are unrecorded.

| Decision | Topic | Packages gated |
|---|---|---|
| `OD-E1` | Public live/pilot status posture | WP-OD-E1 (`README.md`, `faq.md`, `how-you-implement-ies/README.md` wording) |
| `OD-E2` | Conformance-wording posture (stub-backed validation claims) | WP-8b |
| `OD-E3` | ElectricityCredential ownership model (local generation vs. external + sync verifier) | WP-P1.2 scoping and execution in full |
| `OD-E4` | `index.md`'s intended role (canonical / curated / retireable) | WP-OD-E4-ISS-013 package closure (its `OD-S2` slugger fix is technically independent) |
| `OD-E5` | ArrFiling versioning convention | WP-OD-E5 (both subwaves) |
| `OD-E6` | Pathways navigation publication intent | WP-OD-E6 (both branches) |
| `OD-E7` | Windows support posture | WP-P2.2, WP-P1.3-P2.8 in full (not only its P2.8 half) |
| `OD-E8` | Duplicate example disposition (`BillingProfile.json`/`CustomerBillingSummary.json`) | WP-OD-E8 (all three branches) |

Two further gates, distinct from the `OD-E` set, remain unresolved:

- **WP-2b** (MeterDataRequest shipped-example correction): requires an explicit owner go/no-go **and** the schema-change proposal flow — neither substitutes for the other. Neither is recorded.
- **WP-6** (MeterData v0.6 `attributes.yaml` metadata correction): requires the schema-change proposal flow (which is its own authorization gate) **and** WP-P1.2 completed and QE-accepted. Neither has occurred.

No decision substance is recorded or implied by this document.

---

## 7. Live package status — 19 base packages (from `qaqc/09` §6, reconciled to current tree)

| Package | Severity | Status | Blocker |
|---|---|---|---|
| WP-B | P2 | Code landed in-repo (`aa0bbd7`); hosted verification and formal QE checkpoint per the `qaqc/10` process are separate, unaddressed steps | Hosted GitBook check (final-regression evidence) |
| WP-2b | P1 (artifact half) | Not authorized; shipped example still fails semantic validation (confirmed live) | Owner go/no-go + schema-change proposal flow |
| WP-6 | P2 | Not authorized; `attributes.yaml` metadata unchanged | Schema-change proposal flow + WP-P1.2 completion |
| WP-8b | P2 | Not dispatched | `OD-E2` |
| WP-OD-E1 | P2 | Not dispatched | `OD-E1` |
| WP-OD-E3 | P3 | Not dispatched | `OD-E3` |
| WP-OD-E4-ISS-013 | P2 | Not dispatched; `OD-S2` slugger fix is Fable's queued next executable item | `OD-E4` for package closure (slugger fix itself is executable now) |
| WP-OD-E5 | P2 | Not dispatched | `OD-E5` |
| WP-OD-E6 | P2 | Not dispatched | `OD-E6` (publication branch additionally waits on `OD-E4`) |
| WP-OD-E7 | P2 | Not dispatched | `OD-E7` |
| WP-OD-E8 | P3 | Not dispatched; both example files still byte-identical | `OD-E8` + schema-change proposal flow |
| WP-ISS-012 | P2 | Not dispatched; queued after `OD-S2` per current sequencing | None (internally executable) |
| WP-ISS-005 | P3 | Not dispatched | None (internally executable) |
| WP-P1.2 | P1 | Blocked; `Makefile` still excludes ElectricityCredential and invokes the permissive generator (confirmed live) | `OD-E3` |
| WP-P1.3-P2.8 | P1 (P1.3) + P2 (P2.8) | P1.3 code substantially improved (`60a4fb7`) but package **closure failed** independent verification (C1, §5); P2.8 untouched | `OD-E7` (full package); C1's negative-fixture gaps for P1.3 closure |
| WP-P1.4 | P1 | Not started; sole workflow remains `build-pdf.yml` | All other 18 base packages (Phase 2 precondition) |
| WP-P2.2 | P2 | Blocked; `validate_schema.py:51` resolver still unnormalized (confirmed live) | `OD-E7` |
| WP-P2.6 | P2 | Not scoped | Fable discovery-prerequisite scoping (no owner gate) |
| WP-P2.7 | P2 | Not scoped | Fable discovery-prerequisite scoping (no owner gate) |

Out-of-plan: the Consumer Energy Passport schedule work (`6a0d39c`, `3c8a001`) is an owner-directed addition tracked outside these 19 base packages. It does not substitute for, or count toward the closure of, any of them.

---

## 8. Supersession list (stale claims in `qaqc/09`/`qaqc/10`, not edited)

The following counts and statuses in `qaqc/09` and `qaqc/10` are superseded by current live evidence recorded in §§3–4 above. `qaqc/09` and `qaqc/10` are not modified by this record and remain historical controls; their role, dependency, and owner gates remain binding except where this document supplies current evidence in their place.

- **WP-B status:** `qaqc/09`/`qaqc/10` describe WP-B as authorized-but-undispatched (zero files created, `validate_links.py:131` unchanged). Superseded — WP-B's code is now landed (`aa0bbd7`), per §3/§7.
- **Link counts:** `qaqc/02`'s 1,150, `qaqc/04`'s 988/0, and `qaqc/09`/`qaqc/10`'s 994 figures are all superseded by the current live count of 1066 checked / 0 broken (§4).
- **WP-P1.3 (PDF false-green):** `qaqc/09`/`qaqc/10` describe `build_pdf.py:main()` as unconditionally returning 0. Superseded — the return path now propagates missing-source failures (`60a4fb7`), though package closure remains unmet per §5.
- **Navigation/schema-catalog baseline:** `qaqc/09`/`qaqc/10`'s baseline predates the `28df837` merge and the `schemas-ies/` catalog entirely. Superseded by the current 65/65 nav parity and 8-file/33-heading `schemas-ies/` state (§3/§4).
- **`schemas-ies/` heading count and anchor helper (two-stage supersession):** `28df837` established an intermediate state — 8 files, 118 headings, 0 duplicate anchors, produced via a `_dedupe_title`/page_title helper that qualified field-table labels as H3 headings. `bf9d8b0` superseded that intermediate state with the current one — 8 files, 33 headings, 0 H3 field-table headings, 0 duplicate anchors, and no helper — because current-`main`'s generator design renders field-table labels as bold text (`bold_label=True`) rather than headings, eliminating the anchor class the helper existed to disambiguate. Any reference to 118 headings or to the `_dedupe_title`/page_title helper as a current-state fact is superseded; both are `28df837`-era historical evidence only (§3).
- **Passport schedule content:** any characterization of Consumer Energy Passport schedule content in `qaqc/06`/`qaqc/09`/`qaqc/10` predates `6a0d39c` and `3c8a001`. Superseded by §3's provenance-corrected state.

No other row in `qaqc/09`'s reconciliation matrix or `qaqc/10`'s arbitration is altered by this record.

---

## 9. Next executable lane (no production dispatched by this record)

Per Fable's queued technical sequence, the next executable items after this reconciliation are, in order: the `OD-S2` slugger fix (independent of the `OD-E4` decision itself), then WP-ISS-012's single-line `generate_index.py` addition. Both remain internally executable with no owner-decision precondition on their own technical steps.

Read-only scoping (naming exact writable allowlists and acceptance commands, per `qaqc/09` §10's minimums) may proceed now, without dispatch, for WP-P2.6, WP-P2.7, and WP-P1.4 Phase 1. Independent QE has recommended WP-P2.7 (JSON-LD wiring) as high-value work given the pinned-dependency-only, no-owner-gate profile — this is a recommendation, not an authorization; no implementation of WP-P2.6, WP-P2.7, or WP-P1.4 is authorized by this record.

All `OD-E`-gated packages remain blocked pending their respective recorded decisions in `qaqc/11_OWNER_DECISION_LEDGER.md`.

---

## 10. Preserved invariants

1. No schema, source, or example file was mutated in the course of producing this Wave C record. `schemas/**` remains byte-identical through `bf9d8b0` (current HEAD, equal to `origin/repo-wide-qaqc`) — no `schemas/**` diff was introduced by the `3c8a001`→`bf9d8b0` merge (§2/§3); this document (`qaqc/12_CURRENT_STATE_RECONCILIATION.md`) remains the sole untracked path.
2. The orchestrator (root) remains the sole committer and sole pusher of any change this record informs.
3. No force push, no push to `main` or any other original branch, and no publication action is authorized or implied by this record.
4. No release-green claim is made or implied anywhere in this record; §1's verdict stands.
5. Exactly one shared-worktree production writer applies at any time, per `qaqc/10` §6's concurrency gate; this record performs no production and claims no writer slot.
6. Schema design remains as currently reflected on `main` unless a separate, owner-authorized proposal changes it — this record proposes no schema design change.

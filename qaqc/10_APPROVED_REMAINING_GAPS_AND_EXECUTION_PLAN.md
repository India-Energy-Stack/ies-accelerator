# Approved Remaining Gaps and Execution Plan

**Arbitration decision on `qaqc/09_DRAFT_REMAINING_GAPS_AND_REMEDIATION_PLAN.md`: APPROVED WITH CONTROLLING AMENDMENTS.**

q09 is approved as written and remains frozen — this document mutates nothing in q09. The three amendments in §3 below are controlling clarifications recorded here; where q09 and §3 could be read differently, §3 governs. This plan is the approved execution control derived from q09. It makes **no owner decision, confers no release-green status, and is not a release-readiness statement**: the `qaqc/02` "Final regression sequence" and "Kill criteria" sections remain the controlling final acceptance gate for any release, publication, or "release-green" statement, exactly as q09 §9 condition 4 states.

**Baseline:** branch `repo-wide-qaqc`, Waves A1 (`063ef00`) and A2 (`df65e7a`) landed, incorporating `origin/main 9257e85`. Controlling evidence: `qaqc/02_INDEPENDENT_QUALITY_GATE_AUDIT.md`, `qaqc/06_SEMANTIC_DUPLICATION_LOGIC_AUDIT.md`, `qaqc/08_APPROVED_REMEDIATION_WORK_ORDERS.md`, and the frozen `qaqc/09` itself.

---

## 1. Verdict and basis

**APPROVE.** q09 entered arbitration having passed three independent read-only reviews (package/gate, semantic acceptance, dependency/concurrency sequence) and deterministic validation (exactly 19 base `WP-*` headings; 994 links checked, 0 broken; all generated field tables unchanged; whitespace clean). This arbitration pass independently re-verified, from the controlling documents and the live tree:

1. **Matrix reconciliation (q09 §10, item 1):** the §2 matrix has exactly 36 rows tallying **8 CLOSED, 4 PARTIALLY CLOSED, 15 OPEN/EXEC, 7 OWNER-GATED, 2 SUPERSEDED/RETRACTED** — confirmed by independent row count. Confirmed these are row counts, not distinct-finding counts (aliases: P1.1/ISS-001, P2.3/ISS-018, P2.5a/ISS-003, P2.5b/ISS-004, P2.1/ISS-014, P3/ISS-016, ISS-002/DUP-001). Confirmed ISS-005's row is SUPERSEDED/RETRACTED only as to the original "contradiction" claim, with its P3 clarity-reword residual tracked independently via WP-ISS-005.
2. **WP-B fidelity to q08 §6:** q09's WP-B writable allowlist is byte-consistent with q08's exact five files, and its acceptance and kill criteria (reproduce exactly 4 broken pre-fix; per-directory `*.json` counts 2/26/1/10; delta exactly +39; the 8-point acceptance command list; QE fixture test per q08 §7 gate 6) match q08's contract with no drift.
3. **Live-tree state matches q09's claims:** `qaqc/11_OWNER_DECISION_LEDGER.md` does not exist; none of the four `schemas/*/v*/examples/README.md` files exist (WP-B is authorized but undispatched, zero percent executed).
4. **q06 citation integrity:** the OD-E1–OD-E8 escalation set, the `OD-E2` gate on Batch 8b, the ISS-005 `NO CONTRADICTION` reclassification, and the schema-change proposal-flow classification of shipped-example/`examples/`-directory edits are all present in `qaqc/06` as q09 cites them.
5. **Accounting integrity:** the 19 base packages in q09 §6 are exactly the 19 named in §9 condition 3; WP-P1.4's Phase-2 precondition list names exactly the other 18; the base-plus-children rule never changes the 19-base count.

No inconsistency between q09 and its controlling documents survived verification. The amendments below resolve two operational ambiguities and one citation-chain naming point; none alters q09's substance.

---

## 2. Role contract (binding, unchanged from q08 §2)

- **Fable:** second-in-command arbiter and orchestration gatekeeper — scope, arbitration, and gating **only**. Approves/blocks work orders, approves exact writable allowlists, resolves scope collisions, enforces stop conditions, routes owner decisions. Performs no production-file edits, executes nothing, and decides no `OD-E`.
- **Sonnet 5:** primary semantic/technical implementation executor. Executes work orders exactly as written once Fable has scoped and dispatch gates have cleared.
- **Spark (GPT-5.3 Codex, fast mode):** bounded mechanical executor. **Exactly one Spark work order dispatched or in progress at any time.** May own an already-authorized exact mechanical base package in full (e.g. WP-B, WP-ISS-012); for discovery-bearing, semantic, owner-decision, or unresolved-scope work it may receive only a separately approved, exact-allowlist mechanical sub-order — never the whole package, never a discovery prerequisite as-is. Isolated worktrees do not relax the one-order capacity rule.
- **Independent QE:** verifies scope, evidence, behavior, and acceptance directly, never from executor self-report; gates every checkpoint commit.
- **Primary orchestrator (root):** sole committer and sole pusher, each only after the relevant gate passes — commits only after the wave's QE gate, pushes only after the §6 push gate.

Executors and QE never stage, commit, or push. No party — Fable, Sonnet, Spark, or the orchestrator — may reorder, combine, or waive any dependency for scheduling convenience, infer any `OD-E`, or write owner-decision substance.

---

## 3. Controlling amendments (exact; q09 is not mutated)

**A1 — WP-B dispatch-point hygiene.** Consistent with q08 §3's pattern for authorization documents, WP-B does not dispatch until this document (`qaqc/10`) and the frozen `qaqc/09` are QE-accepted and checkpoint-committed as qaqc governance files, with `git status --short` clean at the dispatch point. At that clean point, the orchestrator runs `python -X utf8 -B scripts/validate_links.py` and records the dynamic Wave B baseline as **N checked / 0 broken** per q08 §6 — the stale 1,150, 989, and 994 figures are all superseded for baseline purposes by that recorded N.

**A2 — Scope of "dispatchable now" under shared-worktree serialization.** q09 §8's authority for Fable to dispatch `OD-S2` (and to sequence WP-ISS-012/WP-ISS-005) "now" is subordinate to q09 §7 point 2: in the current shared worktree, no production other than WP-B's begins before WP-B has passed QE and its checkpoint commit has landed. "Dispatch now" therefore means either (a) queued production that starts in the shared worktree only after WP-B's checkpoint, or (b) production in an explicitly isolated worktree/branch carrying its own separate QE gate. It never means a second concurrent production in the worktree WP-B is writing to. This reads q09 §8 and §7 together; it changes neither.

**A3 — Controlling-evidence citation resolution.** Every "q06"/"qaqc/06" reference in q09 and in this document resolves to `qaqc/06_SEMANTIC_DUPLICATION_LOGIC_AUDIT.md` — the only 06-numbered file in `qaqc/`. Recorded here so the citation chain is unambiguous; no alternate 06 title exists or is created.

---

## 4. WP-B — approved first executable package

WP-B (Wave B: directory-target link detection + four collection-index files) is **approved for dispatch as the first executable package**, on the already-recorded q08 §6–§8 authorization. Fable's approval here confirms the checkpoint gate; it creates no new authorization. Executor: Spark (fast mode), holding the single Spark slot.

**Writable allowlist (exact, five files, per q08 §6 — the four READMEs are NEW):**

1. `scripts/validate_links.py` — the directory-target acceptance at `:131` only
2. `schemas/OutageNotification/v0.1/examples/README.md`
3. `schemas/MeterData/v0.6/examples/README.md`
4. `schemas/ArrFiling/v0.5/examples/README.md`
5. `schemas/MeterData/v0.5/examples/README.md`

**Validation contract (per q08 §6–§7, binding and unmodified):** detection change first; with only the validator changed, the run must reproduce **exactly 4** broken directory links or halt. Index files are byte-deterministic (exact H1 template, one blank line, one bullet per `*.json` file in `sorted()` code-point order, nothing else); per-directory counts must be exactly **2/26/1/10** (39 links) or halt before creating anything. Acceptance: the 8-point q08 §6 command list exactly — **N+39 checked / 0 broken** against the A1-recorded baseline; `git status --short` exactly one modified file plus four `??` index paths; `git diff --name-only` exactly `scripts/validate_links.py`; `git ls-files --others --exclude-standard` exactly the four index paths; `git diff --check` exit 0; the untracked-README `rg` hygiene check with no matches; slug rules at `:24-55` byte-identical; `SUMMARY.md`/`_sidebar.md` absent from diff and status. QE gate 6's out-of-repo disposable fixture test proves active detection, with recorded before/after production-state hashes proving the production tree untouched. **Kill criteria:** detection ≠ 4; counts ≠ 2/26/1/10; delta ≠ +39; any acceptance command fails twice; any edit outside the five files becomes necessary; any newly discovered P1. On any kill: halt, leave the worktree as-is, report to the orchestrator — no improvisation.

---

## 5. Executable now vs. gated

**Executable or startable now (no owner decision required):**

- **WP-B** — production, first, in the shared worktree (§4; amendment A1's dispatch-point hygiene applies).
- **Framing, routing, and deliberation of all eight `OD-E` decisions** (`OD-E1`–`OD-E8`) — fully concurrent decision-only work, starting now. Not recording (see gates below).
- **WP-2b's authorization request and Fable scoping** — concurrent with WP-B; decision/framing work only.
- **`OD-S2` (WP-OD-E4-ISS-013's slugger fix)** — Fable may scope/dispatch per q09 §8, subject to amendment A2's serialization.
- **WP-ISS-012 and WP-ISS-005** — internally executable; sequencing per q09 §5 steps 6–8 and amendment A2; the two never share a commit.
- **Discovery/scoping for WP-P2.6, WP-P2.7, WP-P1.4** — no owner-decision precondition on scoping; dispatch waits on exact allowlist enumeration per q09 §10's per-command scoping minimums (pasteable commands, pinned tools, fixtures, expected exits, negative fixtures).
- **WP-P1.4 Phase 1** — informational, non-required component/readiness dry runs only; never labeled the q02 Final regression; never promotes any check to required/blocking.

**Gated on owner decisions, owner authorization, or later discovery:**

- **WP-8b** — gated on recorded `OD-E2`.
- **WP-P1.2** — scoping and execution gated on recorded `OD-E3` (two admissible branches only; declaration alone never satisfies it; the selected implementation is absorbed into WP-P1.2 by default or registered as a uniquely named child package before either dispatches).
- **WP-P2.2 and WP-P1.3-P2.8** — scoping and execution gated on recorded `OD-E7`, in full for the combined package, not just the P2.8 half.
- **WP-OD-E1, WP-OD-E5, WP-OD-E6, WP-OD-E8** — each application gated on its own recorded decision; WP-OD-E5 Subwave 2 and WP-OD-E8 additionally require the schema-change proposal flow; WP-OD-E8's application additionally waits on WP-B's checkpoint (file-path and count collision on `schemas/MeterData/v0.5/examples/`).
- **WP-OD-E4-ISS-013 package closure** — requires `OD-E4`'s dated record plus QE-accepted role-dependent follow-up, regardless of `OD-S2`'s technical completion.
- **WP-2b** — production gated on two non-substituting gates: explicit owner go/no-go **and** the schema-change proposal flow (`schemas/README.md#proposing-a-new-schema-or-a-change`); executor is Sonnet 5, not Spark; production waits for WP-B's checkpoint in the shared worktree.
- **WP-6** — gated on the schema-change proposal flow (which **is** its owner-authorization gate) **and** WP-P1.2 completed and QE-accepted; both non-waivable, by anyone, including the owner on the redrift point.
- **WP-P1.4 Phase 2** — gated on all other 18 base packages plus every decision-generated child/branch being individually QE-accepted and checkpoint-committed; closes last.
- Refusal or non-authorization of WP-2b or WP-6 does not close or supersede their rows; those rows remain OPEN and completion is not reached.

---

## 6. Gates (binding definitions)

- **Dispatch gate.** No package dispatches until: its named preconditions in q09 §6/§7 are recorded as cleared; Fable has approved its exact writable allowlist (discovery-prerequisite packages are non-dispatchable until every path and every acceptance command is exactly enumerated per q09 §10); the executor lane matches §2; and, for Spark orders, the single Spark slot is free. WP-B additionally observes amendment A1. No dispatch may pre-empt, infer, or be conditioned on an unrecorded `OD-E` outcome.
- **Checkpoint gate.** One checkpoint commit per wave/package (or per subwave where q09 §6 mandates separate subwave checkpoints), made by the orchestrator only, only after that wave's QE gate passes. The full q08 §8 pre-commit checklist — including `SUMMARY.md`/`_sidebar.md` untouched and owner-gated surfaces byte-identical — binds WP-B (and the prior A1/A2 checkpoints, as historically applicable), not every later q09 package. For every later package the orchestrator's pre-commit checklist is: exact scoped staging; `git diff --cached --name-only` equal to that package's/subwave's exact allowlist; `git diff --check` exit 0; the deterministic validators applicable to that package; and that package's q09 acceptance/kill contract. Navigation files or owner-gated surfaces may change only when the package's exact allowlist and a recorded/authorized decision explicitly permit them. Commit subjects/bodies contain no model, authorship, generated-by, co-author, or provenance wording.
- **QE gate.** Per q08 §7, applied to every checkpoint. Universal requirements: scope (diff resolves to exactly the package's writable allowlist, nothing else) and acceptance (every acceptance command verified directly by QE, never from executor self-report). Boundary: owner-gated surfaces byte-identical, unless that checkpoint is the explicitly authorized application of the relevant recorded owner decision. Decision hygiene: the diff is grepped for `OD-E1`–`OD-E8` posture, and any unrecorded, out-of-allowlist, or decision-inconsistent `OD-E` posture is rejected. Plus the package-specific gates (WP-B: index bijection and the out-of-repo fixture test).
- **Stop/kill gate.** Every package carries its q09 §6 stop/kill conditions verbatim. Universal stops: quoted anchor text not found; a correction requiring any out-of-allowlist edit; evidence contradicting a correction target; wording that would take an unrecorded, out-of-allowlist, or decision-inconsistent `OD-E` position (the explicitly authorized application of a recorded owner decision, within the package's exact allowlist, is not a stop); `git status` showing any unexpected path; any newly discovered P1. On any stop: halt, leave the worktree as-is, report to the orchestrator — never improvise, never widen scope in place.
- **Shared-worktree concurrency gate.** Exactly one production at a time in the shared worktree; WP-B holds it first. Ledger creation and every `qaqc/11` entry wait for WP-B's checkpoint, then serialize — one writer, one checkpoint at a time. Concurrent production requires an explicitly isolated worktree/branch with its own separate QE gate; isolated preparation never grants concurrent landing rights (integration into shared files is still serial). Technical packages dispatch concurrently only with Fable-approved, exactly disjoint writable allowlists; any overlap (Makefile target, manifest, workflow file, generated artifact, shared script) forces sequential checkpoints. The `generate_index.py`/`index.md` trio is strictly sequential: WP-OD-E4-ISS-013, then WP-ISS-012, then (if publication is selected) WP-OD-E6. `README.md`-touching applications (WP-OD-E1, WP-OD-E7, WP-OD-E6 staged branch) serialize against each other. One Spark order at a time, always.
- **Push gate (amended by explicit owner instruction).** The repository owner has explicitly instructed the orchestrator to commit accepted changes locally on `repo-wide-qaqc` and push that branch upstream with helpful detail/logs; that explicit instruction overrides this plan's prior generic no-push wording and explicitly supersedes q08 §8 item 9's older local-only/do-not-push rule. Accordingly, after each package's QE gate passes and its checkpoint commit lands, the orchestrator **must** push (a normal, non-force push) to `origin/repo-wide-qaqc` — first verifying the current branch is `repo-wide-qaqc`, the upstream is `origin/repo-wide-qaqc` (setting it with the initial push if absent), and the checkpoint is clean and scoped exactly per the checkpoint gate; after pushing, verifying that `origin/repo-wide-qaqc` equals the local `HEAD` — and records the push result/log in its report. The q09/q10 governance checkpoint itself (amendment A1) is eligible and required to be pushed under this gate once QE-accepted and checkpoint-committed. Only the orchestrator pushes; executors and QE still never stage, commit, or push. All other prohibitions stand unchanged: **no tags, no push to `main` or any original branch, no branch changes, no release publication, no GitBook or other publication action, and no release-green claim** — by anyone, at any checkpoint, for any reason within this plan's scope. A push of `repo-wide-qaqc` is a review/checkpoint transport action only: it is not release publication and is never evidence that the q02 gate is cleared. Publication is reachable only beyond the q02 gate, which this plan cannot and does not clear.

---

## 7. Preserved invariants

1. **Owner-decision authorship and the q11 ledger.** `qaqc/11_OWNER_DECISION_LEDGER.md` is the exact, sole path for all eight written, dated `OD-E` decisions. The owner/user writes each decision's substance directly; Fable frames, routes, and gates only. Creation and every entry wait for WP-B's checkpoint in the shared worktree and then serialize — one entry, one QE-gated checkpoint at a time. Recording a decision never itself closes a package: the assigned executor must still apply the outcome, pass QE, and checkpoint before any row reads CLOSED, and no-code outcomes still require the dated record plus a recorded no-change/SUPERSEDED rationale plus QE confirmation. `OD-E3` is never a no-code outcome.
2. **Owner authorization and schema-change gates.** Every gate in q09 §6/§8 stands: WP-2b's two non-substituting gates; WP-6's proposal-flow-as-authorization plus the non-waivable WP-P1.2 precondition; the proposal flow for WP-OD-E5 Subwave 2 and all three WP-OD-E8 branches; no silent authorization of any source/schema/example/policy change by this document.
3. **19-base-plus-children accounting.** Completion is defined over the 19 base packages plus every decision-generated child package or selected branch (q09 §9 condition 3). Children (e.g. `WP-P1.2-OD-E3-LOCAL`/`-SYNC`, WP-OD-E5 Subwave 2, the Common OD subwave, OD-E4 role-dependent follow-ups) are registered with their own exact allowlist, acceptance, QE gate, and checkpoint before dispatch, and never change the 19-base count. No package or branch may be skipped as low-severity or "deferred"; exclusion requires a recorded SUPERSEDED/RETRACTED basis.
4. **Exact package dependency order.** q09 §5 steps 1–12 and §7 points 1–8 are approved as the binding sequence, including: WP-B first; WP-2b production post-WP-B-checkpoint; the parallel decision track with serialized ledger writes; the decision-to-package gating map (`OD-E2`→WP-8b; `OD-E3`→WP-P1.2 scoping+execution; `OD-E7`→WP-P2.2 and WP-P1.3-P2.8 in full; `OD-E4`/`OD-E6` governing the sequential navigation lane); WP-6's dual non-waivable preconditions; disjoint-allowlist concurrency for the technical waves; and WP-P2.6 never deferred behind WP-P1.4.
5. **WP-P1.4 final closure plus the single later controlling regression.** WP-P1.4 closes last among the 19, via Phase 2 only (exact 13-step CI mapping, per-step fixture readiness, required/blocking promotion with independently verified failure propagation and no result masking — no `continue-on-error`). Its closure is not, and never substitutes for, the release gate. **After** WP-P1.4 closes, exactly one controlling q02 Final regression — all 13 steps, in a disposable fresh clone, under q02's kill criteria — is run. That single run, and nothing else in q09, q10, or any checkpoint history, is the sole authority for any release, publication, or "release-green" statement. No Phase-1 dry run and no interim mapping check may ever be labeled or logged as "the q02 Final regression."

---

## 8. Closing constraint

This document approves execution control only. It records no `OD-E` decision, authorizes no schema/source/example edit beyond the already-authorized WP-B, and confers no release-readiness status of any kind. The repository remains **NOT RELEASE-GREEN** per q02, q04, q06, and q09's four independent confirmations, and remains so until q09 §9's four completion conditions hold — culminating in the single controlling disposable-clone q02 Final regression, which `qaqc/02` alone defines and controls.

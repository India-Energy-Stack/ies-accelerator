# DRAFT: Semantic Audit Work Order for Fable Review

**Status:** Draft orchestration support only. Fable must review and `/root` must approve before dispatch. This document is not an audit, contains no semantic findings, and authorizes no source edits, commit, push, or publication action.

## 1. Objective and role boundary

Produce one repository-wide semantic audit that determines whether the documentation and schema-facing claims are internally coherent, correctly scoped, and supportable. Mechanical audits 01 and 02 are inputs; this audit must not repeat their broad mechanical scans or treat their unresolved owner decisions as settled facts.

| Role | Authority and boundary |
|---|---|
| `/root` | Lead. Locks the baseline and scope, dispatches work, resolves role conflicts, and gives final acceptance. |
| Fable | Second-in-command for work-order challenge, prioritization, and arbitration only. Fable may propose amendments within Section 11 for `/root` to incorporate, but does not execute the semantic audit, edit this draft or repository sources, or replace the primary executor. |
| Sonnet 5 | Primary semantic executor. Reads the complete mandatory corpus, performs the audit, and produces the single audit artifact specified in Section 8. Sonnet 5 makes no source fixes. |
| Spark | Bounded mechanical executor. Runs only exact checks assigned by `/root` or approved by Fable, reports reproducible command evidence, and makes no semantic or priority judgments. |
| QE | Independent verifier. Reconciles corpus coverage, tests evidence and classifications, challenges unsupported generalizations, and verifies acceptance gates without co-writing findings or editing sources. |

## 2. Locked baseline and exact scope manifest

At dispatch, `/root` records the branch, full commit, `git status --short`, and `git ls-files` manifest. Corpus changes after that point trigger Section 9. All paths below mean tracked files at the locked commit.

### 2.1 Mandatory audience-facing corpus: 81 Markdown files

Sonnet 5 must read every tracked `*.md` file except `qaqc/*.md`. The baseline groups are exact and must reconcile to 81:

| File group | Count | Coverage rule |
|---|---:|---|
| Repository root: `README.md`, `SUMMARY.md`, `_sidebar.md`, `contributors.md`, `download-pdf.md`, `faq.md`, `getting-started.md`, `glossary.md`, `index.md` | 9 | All files |
| `concepts/**/*.md` | 1 | All files |
| `what-ies-provides/**/*.md` | 13 | All files |
| `how-you-implement-ies/**/*.md` | 7 | All files |
| `pathways/**/*.md` | 6 | All files |
| `use-cases-overview/**/*.md` | 8 | All files |
| `use-cases/**/*.md` | 9 | All files |
| `schemas/**/*.md` | 28 | All files, including version, validation, design, implementation, and tool READMEs |

Audits `qaqc/01_SPARK_MECHANICAL_AUDIT.md` and `qaqc/02_INDEPENDENT_QUALITY_GATE_AUDIT.md` are required control inputs, not part of the 81-file audience corpus. This draft is also a control input after approval.

### 2.2 Mandatory schema and claim-adjudication evidence

Inspect every file in these groups, not a sample:

- Schema sources and compiled semantics: 11 `schemas/**/attributes.yaml`, 11 `schema.json`, 11 `context.jsonld`, and 11 `vocab.jsonld` files.
- Registries and crosswalks: `schemas/MeterData/v0.5/OBISMapping.json`, `schemas/MeterData/v0.6/IES codes.json`, `schemas/OutageNotification/v0.1/fault_reason_crosswalk.json`, and `schemas/OutageNotification/v0.1/FeederStatusIngest.openapi.yaml`.
- Shipped evidence: all 62 tracked `schemas/**/examples/*.json` files.
- Semantic validation evidence: all 19 tracked files under `schemas/**/validation/**` (the two validation READMEs are already in the 81-file corpus); the three version-level Makefiles at `schemas/MeterData/v0.6/Makefile`, `schemas/MeterDataRequest/v0.6/Makefile`, and `schemas/OutageNotification/v0.1/Makefile`; plus `schemas/OutageNotification/v0.1/tools/transform_discom_csv.py` and `schemas/OutageNotification/v0.1/tools/discom_planned_shutdown.csv` (the tool README is already in the 81-file corpus).
- Mechanical-control evidence needed for owner decisions: root `Makefile`, `.gitbook.yaml`, `.github/workflows/build-pdf.yml`, all 22 tracked `scripts/*.py` files, `scripts/build_pdf.sh`, and both tracked `scratch/*.py` files. Broad tooling conclusions must cover this complete control group rather than selected scripts.

Non-audience assets outside these groups may be consulted only when a finding identifies why they are probative. Their inclusion must be recorded in the coverage manifest.

## 3. Independent audit axes

Keep these axes separate through evidence collection. A finding may connect axes only after each has been tested independently.

1. **Product and status claims:** what IES is, provides, requires, supports, or has delivered; normative versus illustrative language; current versus aspirational state.
2. **Register, Discover, Exchange semantics:** prerequisites, actors, artifacts, direction of control, sequence, and claimed outcomes for each capability.
3. **B2B and B2C boundaries:** data exchange versus credential issuance; credential, schema, payload, catalogue, consent, and exchange responsibilities.
4. **Identity and data movement:** DID and DeDi roles; Beckn registration and signing; DigiLocker delivery; adapter placement; consent and authorization; signer, holder, issuer, verifier, sender, receiver, and data-custody transitions.
5. **Schema, version, and field semantics:** source-to-compiled alignment; version/status labels; required and optional fields; registry meanings; examples; validators; migration claims; external-schema dependencies.
6. **Use-case parity:** every `use-cases-overview` page against its implementation guide, including actors, prerequisites, sequence, schema versions, maturity, and limitations.
7. **Pathway parity:** role definitions and end-to-end flows across authority, researcher, secretariat, TSP, and utility pathways, checked against canonical product and implementation pages.
8. **Canonical and duplicated prose:** source-of-truth declarations, repeated normative rules, divergence, stale copies, and unclear ownership.
9. **Glossary, FAQ, and terminology:** definition consistency, acronym expansion, renamed concepts, overloaded terms, and terminology that changes legal or technical meaning.
10. **Live, pilot, WIP, timeline, and actor assertions:** present-tense deployment claims, dates, named organizations, actor responsibilities, and the difference between demonstrated, planned, proposed, and production-ready.
11. **Security, privacy, and conformance:** trust boundaries, key and signature claims, consent, data minimization, revocation, authenticated transport, compliance language, threat assumptions, and what validation actually proves.

## 4. Harmful-duplication taxonomy

Create one stable `DUP-###` cluster for each repeated concept. Record every location, the candidate canonical source, semantic variance, harm, and owner.

| Type | Default treatment |
|---|---|
| Intentional overview-detail layering | Accept when the overview stays shallow, links to the detail, and does not restate mutable normative rules. Flag only drift or unclear authority. |
| Versioned, generated, or template reuse | Accept when source, version, generation boundary, and maintenance owner are explicit. Do not count repeated field tables alone as harmful. |
| Redundant normative text | Harmful when the same rule can change independently in multiple places. Identify the canonical candidate and all dependents. |
| Contradictory duplicates | Defect. Quote the conflicting propositions and provide paired `file:line` evidence. Do not reconcile by preference. |
| Copy-paste residue | Defect or maintenance risk when names, versions, actors, paths, fields, or status labels survive from another context. |

## 5. Evidence and classification rules

- Finding IDs use `SEM-<AXIS>-###`. Once assigned, an ID is never renumbered; withdrawn items remain as `RETRACTED`.
- Severity: **P0** unsafe or legally/security-critical instruction with immediate material harm; **P1** release-blocking semantic contradiction or false assurance; **P2** material user, interoperability, maintainability, or credibility defect; **P3** localized clarity or maintenance defect.
- Classification is one of `CONFIRMED DEFECT`, `MATERIAL RISK`, `OWNER DECISION`, or `RETRACTED`.
- Evidence type is one of `VERIFIED FACT`, `INTERNAL CONTRADICTION`, `UNSUPPORTED CLAIM`, or `OWNER DECISION REQUIRED`. Do not convert an unsupported external claim into a factual contradiction.
- Every contradiction or parity finding requires paired `file:line` anchors and the exact propositions being compared. External verification must name the authoritative source, URL, and verification date. If it cannot be verified, classify it as unsupported.
- Deduplicate by root issue. One root ID may list multiple manifestations and affected files. Do not inflate counts by assigning a separate finding to every repeated sentence.
- State impact, confidence, owner, acceptance test, and whether the issue changes product, research, architecture, data, execution, or team-governance conclusions.
- Claims such as “all,” “consistent,” “canonical,” “current,” or “complete” require full-corpus evidence from Section 6.

## 6. Full-coverage proof

The single audit artifact must contain or append:

1. Baseline commit and corpus totals.
2. A row for every mandatory file with `READ`, applicable axes, finding IDs, and `NO FINDING` where appropriate.
3. A schema evidence ledger covering all source, compiled, registry, example, and validation files in Section 2.2.
4. Pairing matrices for all seven overview/implementation-guide pairs and all five role pathways.
5. A duplication-cluster ledger with every instance, including accepted layering.
6. Axis totals that reconcile to the file-level rows and a signed-off list of any `N/A` decisions with rationale.

Sampling may guide reading order, but it cannot support a broad conclusion. Incomplete coverage must be reported as incomplete, not generalized.

## 7. Mechanical audit decisions to carry forward

Do not mechanically relitigate settled evidence. Test its semantic and claim impact, and route the unresolved decision:

- **P1 gates:** the shipped MeterDataRequest example versus its semantic contract; non-reproducible outputs in 5 of 8 Make-managed schema directories (12 artifacts); PDF missing-source false-green; and the absence of a repository-wide gate while `main` can publish automatically.
- **P2 decisions:** three live GitBook directory-link failures plus one latent link; generated-index role, 15 omitted entries, and 223 numeric-anchor defects; Windows cross-schema resolver support; permissive external-schema stubs and conformance wording; stale or ambiguous schema metadata; migration-tool false-green behavior; JSON-LD dependency/wiring; and Windows PDF encoding.
- **Other owner questions:** ElectricityCredential generation ownership, exact duplicate MeterData v0.5 examples, and whether stale scratch tooling is maintained or retired.
- **Retracted:** the 64-anchor defect set and duplicate-key findings. They must not re-enter the semantic audit without new reproducible evidence.

For each carried item, the audit records `SEMANTIC IMPACT CONFIRMED`, `NO SEMANTIC IMPACT`, or `OWNER DECISION REQUIRED`, with evidence. Sonnet 5 does not implement the fix.

## 8. Single deliverable

Sonnet 5 produces only `qaqc/04_SONNET_SEMANTIC_AUDIT.md`. It must include: answer-first verdict; scope and coverage proof; prioritized deduplicated findings; axis-by-axis results; harmful-duplication ledger; owner decisions; acceptance tests; residual uncertainty; and an exact source-change recommendation list. Recommendations identify targets and intent but contain no patches.

At dispatch, `/root` records the approved hash and tracked/untracked state of this work order as part of the baseline. During execution, repository sources, audits 01/02, and this approved work order remain unchanged. Creation and revision of the authorized audit artifact are the only permitted worktree delta from that recorded state. Temporary analysis outputs must stay outside the repository. No commit or push is authorized.

## 9. Stop and escalation criteria

Stop and notify `/root` when any of these occurs:

- The commit, tracked-file manifest, existing file contents, or worktree changes after baseline lock, except for creation and revision of the authorized `qaqc/04_SONNET_SEMANTIC_AUDIT.md` artifact.
- Mandatory coverage cannot reach 100 percent, a required file is unreadable, or evidence cannot be located precisely.
- A P0 is found. Preserve evidence and stop lower-priority synthesis.
- A P1 mechanical premise is contradicted by reproducible evidence.
- An external live, legal, security, pilot, timeline, or actor claim lacks an authoritative source or requires unavailable access **and** the gap prevents P0/P1 adjudication or the overall verdict. Otherwise classify it as unsupported and continue.
- Two plausible semantic interpretations would produce different P0/P1 findings or prevent the overall verdict. For lower-severity ambiguity, record `OWNER DECISION REQUIRED`, explain both interpretations, and continue.
- Completion would require a source edit, publication action, commit, push, or expansion beyond the approved manifest.

## 10. Acceptance gates

`/root` may accept the audit only when:

- Fable approved the dispatch version and all role boundaries were preserved.
- The 81-file audience manifest and every Section 2.2 evidence group reconcile at the locked commit.
- Every audit axis has a result, every finding has stable evidence and classification, and every broad claim is supported by full coverage.
- QE independently verifies inventory reconciliation, all P0/P1 findings, all owner decisions, paired parity matrices, duplication clusters, and the absence of unsupported generalizations.
- Mechanical owner decisions are carried without reintroducing retracted findings.
- Relative to the recorded dispatch status, `git status --short` shows only the authorized Sonnet audit artifact as an additional change; this work order retains its approved hash, and audits 01/02 and repository sources are byte-identical to baseline.
- Fable completes prioritization/arbitration and `/root` records final acceptance or a bounded remediation order.

## 11. Fable review before dispatch

Fable must answer each question with `APPROVE`, `REVISE`, or `ESCALATE`, followed by exact proposed text or routing:

1. Are the role boundaries strict enough to prevent review, execution, and verification from collapsing into one role?
2. Does the manifest cover every audience surface and every schema artifact needed to adjudicate claims? Name any addition; justify any exclusion.
3. Are product, architecture, data, execution, research, and team-governance consequences kept separate long enough for useful arbitration?
4. Are P0-P3 thresholds and release gates proportionate? Should the CI gate remain P1 because of automatic publication?
5. Is `index.md` a required canonical deliverable, a curated aid, or non-deliverable? Set the resulting severity rule.
6. Is Windows a supported validation environment? Set the resolver and encoding severity accordingly.
7. Which live, pilot, WIP, timeline, and named-actor claims require current external verification before dispatch?
8. Are the duplication categories sufficient to preserve useful overview-detail layering while removing normative drift?
9. Which semantic decisions require named schema, product, security, or documentation owners before Sonnet 5 can conclude?
10. Do any P1 gates block dispatch, or may audit and mechanical remediation proceed in parallel under a release hold?

Fable may propose reordering axes, tightening evidence rules, adjusting severity with written rationale, adding owner questions, changing the deliverable path, or splitting/merging proposed root issues. `/root` decides whether to incorporate each proposal. Fable may not propose dropping the 81-file corpus or required schema evidence, permitting sampling-based broad claims, authorizing source edits, altering audits 01/02, executing the primary audit, replacing Sonnet 5 as primary executor, or waiving QE independence. Any scope reduction or role change requires `/root` approval before dispatch.

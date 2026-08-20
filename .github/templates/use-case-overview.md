# [Use case name]

*[One-sentence summary in italics. What this use case lets someone do, and which schema carries it.]*

Link the implementation guide here, as a bold markdown link to `../use-cases/[shortname]/README.md`.

| Field | Value |
|---|---|
| Applicability | [who this applies to] |
| This version | [what this version covers, and what it does not] |

Do not put a status claim in this table. `STATUS.md` is the single source for whether anything is running; link it rather than restating it. While a page is under review, its state lives in the Decisions section below.

> **Notation while drafting.** Square brackets are slots — replace them. Rows marked `[EXAMPLE]` in italics are illustrations — delete them. No bracket should survive into a merged page except a deliberate `[TBD]`, and every `[TBD]` must appear in §11.

---

## Decisions

*While Status is `Proposed`, this section lists what reviewers are being asked to agree. On merge it becomes a dated record and stays on the page permanently. It is never deleted.*

**Status of these decisions:** [Proposed — under review / Agreed on (date)]

| # | Decision | Detail | State |
|---|---|---|---|
| A | [short name] | [the decision in one or two sentences, stated as a recommendation] | [Proposed / Agreed / Deferred to §11] |
| B | | | |

> *[EXAMPLE] After merge this reads: "Agreed 14 April 2026 — A, B and C. Deferred — D, pending the cross-licensee settlement framework (§11.2)."*

---

## 1. Scope and Purpose

[Who the stakeholders are, and the problem in plain words. Two or three paragraphs.]

## 2. What It Records / Covers

| Records | Detail | Source |
|---|---|---|
| [the thing recorded] | [what it contains] | [which schema and field carries it] |

[Paragraph — what this record explicitly does not carry, and which use case carries that instead.]

## 3. How Each Item is Identified

[How each subject is named. Use the identifier patterns IES already uses; do not invent a method.]

| Subject | Identifier method | Example |
|---|---|---|
| [subject] | [method] | [example identifier] |

## 4. Definitions

[Terms a reader might not know. Where IES already defines a term, use that definition and link to the glossary. Mark any genuinely new term as proposed for addition.]

- **[Term]** — [definition]. [Link to glossary, or "proposed addition to the glossary".]

## 5. Basis of Standards

Order of preference: **IS → CEA Regulations / IEGC → IEC → IEEE**. Where the governing instrument is regulatory rather than technical — a SERC tariff regulation, a commission procedure — name it and say so rather than forcing it into that order.

| Standard or regulation | Role here |
|---|---|
| [standard] | [what it governs in this use case] |

## 6. Where Indian Standards Do Not Yet Exist

[Concepts with no IS, the international standard used instead, and which CEA limits are retained where CEA sets them.]

## 7. The Record(s)

[What this use case produces. If it produces more than one record, list them and say which Schedule each belongs to.]

| Record | Schedule | Nature | Status |
|---|---|---|---|
| [name] | [I or II] | [Stays the same / Gets revised / Keeps changing] | [Executable today / Illustrative] |

## 8. Schedule I — Static Fields of the [Record]

*The fields whose value is fixed when the record is issued. They change only when a corrected record is issued.*

| **Normative Path** | **Type** | **Schema Requires** | **Standard** *(informative)* | **Profile Guidance** *(informative)* |
|---|---|---|---|---|
| [real JSON path in the named schema] | [expected format] | [what the schema itself enforces] | [governing standard] | [whether issuers should populate it] |

### 8.x Example and Validation

[Link the worked example, and the commands that validate it structurally and semantically.]

## 9. Schedule II — [Live record name]

*The fields that keep arriving after the record is issued. If this use case has none, write the section as below and say why.*

**If there is no live half:**

> **Not applicable.** [This record carries no time-dependent data — every field in Schedule I is fixed at issuance.] Live data that references this record is exchanged under its own use case: [link them, and say which identifier joins them].

**If there is a live half:** same table shape as Schedule I, plus the transport if it differs from the rest of the use case.

> The test is not whether a field carries a date. A yearly filing amount carries a year and is fixed the day it is filed. If you cannot name the point at which updates stop, it belongs here.

## 10. How It Fits Together

[A diagram or short narrative. If this use case draws on more than one exchange, add a subsection naming the source and transport for each Schedule.]

## 11. Points for Confirmation

[Genuinely open questions, numbered. Anything marked `[TBD]` elsewhere on the page appears here. Say which of these, if any, block the decisions above.]

1. **[Question]** — [why it matters, who decides, and whether it blocks].

---

## Schemas Used in This Use Case

[Which schema carries which Schedule. Link the validated examples.]

## Value Unlock

[What each party gains. Keep it factual; this is not a pitch — the pitch belongs in the change request.]

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|

## Annexure B — Example Payloads

[Links to validated examples, one per Schedule.]

## Annexure C — JSON Schema

[Canonical schema, context and vocabulary locations.]

## Annexure D — Derived Views

*Anything the receiving organisation computes for itself after it gets the data. Not exchanged, so it belongs in neither Schedule.*

| Derived view | Inputs | Schema status | Treatment |
|---|---|---|---|
| [name] | [which Schedule fields feed it] | Derived | [how to handle it] |

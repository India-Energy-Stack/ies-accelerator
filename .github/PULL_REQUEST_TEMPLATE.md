<!--
This form is the record of WHY a change was made. It is saved with the pull
request forever and never appears in the published book.

The page you are adding or editing says what is true. This form says what you
were trying to do, what you rejected, and what you are asking reviewers to
agree. Both are needed. Neither substitutes for the other.

Delete any section that genuinely does not apply, and say why in one line
rather than leaving it blank.
-->

## What this changes

[One or two sentences. Which pages, schemas or scripts, and what is different afterwards.]

**Type of change:**

- [ ] New use case
- [ ] New schema, or a new version of one
- [ ] Change to an existing use case or schema
- [ ] Documentation correction — no change to what the system does
- [ ] Tooling, gates or build

---

## Why

[The problem this solves. What cannot be done today, and by whom. If the change is a correction, say what was wrong and how it was found.]

**What it costs to leave things as they are:**

[The consequence of doing nothing. Give a figure where one exists, and mark it `[SOURCE NEEDED]` where it does not. Label estimates as estimates.]

---

## What reviewers are being asked to agree

<!-- Skip this only for corrections and tooling. Anything that changes what the
     system does needs it. These decisions are mirrored in the page's Decisions
     section, which becomes the permanent dated record on merge. -->

| # | Decision | What agreement means |
|---|---|---|
| A | [the decision, stated as a recommendation] | [what becomes settled if this is approved] |

**What we give up if this is agreed:** [what becomes impossible or much harder. A decision with no cost is a description.]

---

## What was considered and rejected

[The alternatives, and why they lost. This is the section that saves the next person from re-litigating a settled question — the reason it exists is that reconstructing a decision from commit history is expensive and often impossible.]

---

## Precedent `[optional]`

[Comparable systems here or abroad, and specifically what each one supports or warns against. Include a failure case where you have one: somewhere that did not do this, and what it cost. Not a reading list.]

## Relationship to other programmes `[optional]`

[Where another scheme, platform or regulation covers overlapping ground: how this complements it. If they genuinely compete, say so here — that is a question for the sponsors, not something to leave unstated.]

## What would make us stop `[optional]`

[What finding, decision elsewhere, or cost would make this work not worth continuing.]

---

## Still open

| Question | Who decides | By when | Blocks this merge? |
|---|---|---|---|
| [the open question] | [the body or person] | [date] | [Yes / No] |

Every `[TBD]` left in the changed pages appears above and in that page's Points for Confirmation.

---

## Checks

**Content**

- [ ] Every figure has a source, or carries `[SOURCE NEEDED]`
- [ ] Every estimate is labelled as an estimate
- [ ] Every term is checked against the [glossary](../glossary.md); new terms are flagged as proposed additions
- [ ] Every exclusion says where that thing belongs instead
- [ ] No claim of "live", "running" or "in production" without dated evidence; status claims defer to [STATUS.md](../STATUS.md)
- [ ] Nothing tied to a meter, connection or device is described as anonymous — identifier-keyed data is pseudonymous
- [ ] Dates are real dates, not "next quarter"
- [ ] No `[EXAMPLE]` or unresolved template brackets remain

**Structure** — for pages that add or change a use case

- [ ] Every field is in Schedule I (fixed at issuance) or Schedule II (keeps arriving); a use case with no live half says "not applicable" and why
- [ ] Nothing computed by the recipient after receipt is in either Schedule — that belongs in Annexure D
- [ ] The Decisions section is present, and reflects the table above
- [ ] Section numbering 1–11 matches the other overview pages

**Gates** — paste the results

```
python -X utf8 -B scripts/run_schema_checks.py
python -X utf8 -B scripts/run_negative_fixtures.py
python -X utf8 -B scripts/validate_links.py
python -X utf8 -B scripts/check_navigation.py
```

- [ ] All pass, or failures are pre-existing on the base branch and named here: [which, and why]

---

## On merge

- [ ] Page `Status` updated from `Proposed`
- [ ] The Decisions section converted to a dated record — *"Agreed (date) — A, B. Deferred — C, see §11."*

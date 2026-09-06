# IES Documentation Walkthrough — 15-minute onboarding video script

**Audience:** an engineer or architect at a DISCOM, AMISP, OEM, or system integrator who has been told "implement this with IES" and is opening the GitBook for the first time.

**Job of the video:** in 15 minutes, leave them knowing (1) what IES is and is not, (2) how to read the schemas, (3) how a use case turns a schema into a build, (4) what setup every participant does once, and (5) how to propose a schema when IES doesn't cover their domain object yet.

**Source:** [india-energy-stack.gitbook.io/docs](https://india-energy-stack.gitbook.io/docs) as rendered from this repository at the time of writing (2026-09-06). Sidebar labels below are quoted exactly from the GitBook navigation (`SUMMARY.md`).

**Narration length:** about 2,250 words. At a relaxed 150 words per minute that is 15:00. If you speak faster, don't fill the gap — let the screens breathe.

---

## Before you hit record

Do these once and the recording becomes a single take with no fumbling.

1. **Pre-open every page as a tab, in order.** Use the tab list under "Tabs to pre-open" below. During the recording you only ever switch to the next tab and scroll — never type a URL or search.
2. **Browser prep.** One clean profile, no extensions or bookmarks bar, window at 1920×1080, page zoom **110–125%** so field tables are legible on a phone. Pick one theme (light is safer for tables) and keep it for the whole take.
3. **Collapse the GitBook sidebar groups** you are not on, so the sidebar is short enough to read in one frame during the "map of the docs" segment.
4. **Scroll positions.** For each tab, scroll to the heading named in "Where to be" *before* you start. The script tells you when to scroll further.
5. **Pointer discipline.** Hover the thing you are talking about; don't circle the cursor. Highlight table rows by selecting text only when the script says "select".
6. **Segment checkpoints.** The timecodes are targets, not hard cuts. If you are 30 seconds over at 7:40 (the end of the Use Case Overviews segment), use the "If you're running long" cuts at the end of this document.
7. **Fallback for the Propose form.** The inline form is a GitBook ContentKit block. Load the Propose a Schema tab first and confirm the form renders. If it doesn't, the page has an "open it in a new tab" link — pre-open that as well.

### Tabs to pre-open (in recording order)

Sidebar path is the authoritative locator. URLs are given where the docs themselves cite them; for the rest, navigate from the sidebar and copy the URL into your own notes.

| # | Sidebar path | Where to be when you switch to the tab | Known URL |
|---|---|---|---|
| 1 | Getting Started | Top of page | `https://india-energy-stack.gitbook.io/docs` |
| 2 | Schemas Overview › Schemas Overview | Top (the 7-row status table) | — |
| 3 | Schemas Overview › ElectricityCredential | Top | — |
| 4 | Schemas › All Schemas | Top (the "Verifiable Credentials" cards) | — |
| 5 | Schemas › ElectricityCredential | Top (the canonical-base table) | — |
| 6 | Schemas › ElectricityCredential › v1.2 | Top (the "Files" bar) | `https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2` |
| 7 | Schemas › Term Taxonomy | Top | `https://india-energy-stack.gitbook.io/docs/schemas/taxonomy` |
| 8 | Schemas › External Schemas | Top | — |
| 9 | Schemas › MeterData › v0.6 | Top | `https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6` |
| 10 | Use Case Overviews › Smart Meter Data Exchange | Heading "2. What It Records / Covers" (the profile table) | — |
| 11 | Use Case Overviews › Consumer Energy Passport | Top | — |
| 12 | Use Case Implementation Guides › Consumer Energy Passport | Top | — |
| 13 | Use Case Implementation Guides › Smart Meter Data Exchange | Heading "Setup: Register → Discover → Exchange" | — |
| 14 | Concepts › Before you build | Top | — |
| 15 | Concepts › Conformance Checklist | Heading "What conformance means" | — |
| 16 | Pathways › Overview | Top (the pathway table) | — |
| 17 | Propose a Schema | Top (the lifecycle diagram) | — |
| 18 | GitHub issue tracker | Issues list | `https://github.com/India-Energy-Stack/ies-accelerator/issues` |
| 19 | Getting Started (again) | Heading "Get in touch" | `https://india-energy-stack.gitbook.io/docs` |

---

## The script

Format for every segment: **time range → what is on screen → what you say.** Screen directions are in *italics*. Narration is in plain text. Read the narration as written; it is paced to the screens.

---

### 0:00–0:40 · Cold open — who this is for

**On screen:** Tab 1, Getting Started, top of page. Hold on the first paragraph. *At 0:20, slowly scroll so the "How IES works" heading is visible at the bottom of the frame.*

> If you've been asked to implement something with the India Energy Stack and you've just opened this documentation, this video is for you. In fifteen minutes I'll walk the docs in the order you should actually read them: what IES is, then the schemas you'll code against, then the use cases that turn a schema into a build, then the one-time setup every participant does, and finally how to propose a schema when IES doesn't cover your domain object yet.
>
> IES is a Ministry of Power initiative; REC is the nodal agency and FSR Global the knowledge partner. This site is the technical reference for building on it.

---

### 0:40–2:00 · How IES works — Register, Discover, Exchange

**On screen:** Tab 1, scroll to the heading **"How IES works — Register, Discover, Exchange"**. *Hover each bold word as you say it. At 1:30, scroll to the sentence beginning "The specifications cover five building blocks".*

> The one idea to take from this page is the UPI comparison. IES holds no data of its own. Your DISCOM software, your metering platform, your vendor database — the data stays where it is. IES specifies how any two of those systems identify each other, find each other, and exchange data in a common, verifiable shape.
>
> Every interaction follows three steps. **Register**: every participant gets a verifiable digital identity — a W3C DID — and a listing in a shared directory called DeDi. Done once. **Discover**: before an exchange, the two systems look each other up and agree terms over the Beckn protocol, so there's no bilateral integration to negotiate. **Exchange**: data moves over that same signed Beckn channel, shaped by the IES schemas, which build on existing open standards — DLMS/COSEM for meters, IEEE 2030.5 and OpenADR for DERs. Where a durable record is needed, the exchange produces a W3C Verifiable Credential the holder keeps — for consumers, in DigiLocker.
>
> Five building blocks sit under those steps: identifiers, registries, exchange, verifiable credentials, and the security, consent and machine-readable-rules posture running through all of them. And notice what IES is not: it doesn't write new standards, and it's not a platform, a database, or a product.

---

### 2:00–2:40 · Map of the docs

**On screen:** Tab 1, keep the page still and **move the pointer down the sidebar**, resting on each group as you name it. *Groups in order: Schemas Overview, Schemas, Use Case Overviews, Use Case Implementation Guides, Pathways, Concepts, then back up to Propose a Schema at the top.*

> Before we go anywhere, here's the shape of the site, because the reading order matters.
>
> Two schema sections: **Schemas Overview** is the plain-language "why" for each schema; **Schemas** is the developer catalog — field references, canonical URLs, versions. Then the same five use cases twice: **Use Case Overviews** for decision-makers, **Implementation Guides** as build checklists. **Pathways** sequences everything by the kind of organisation you are. **Concepts** is the one-time setup. **Propose a Schema**, at the top, is how the catalog grows. Everything under **Draft** is work in progress, so we'll skip it.
>
> We'll follow that order: schemas, use cases, setup, propose.

---

### 2:40–4:00 · Schemas Overview — the plain-language layer

**On screen:** Tab 2, Schemas Overview. *Hold on the status table for the first paragraph. Select the three "Stable — In Pilot" credential rows as you mention them, then hover the two "Work in progress" rows. At 3:25, scroll to "Where the P2P and flexibility schemas live (external)". At 3:40, switch to Tab 3 (ElectricityCredential overview) and scroll slowly through the numbered section headings, then stop on "8. Schedule I".*

> Start with Schemas Overview. This table is the whole catalog on one screen: seven schema families IES stewards itself, with a status column. Five are stable and were used in the pilot: ElectricityCredential, MeterData, MeterDataCredential, MeterDataRequest, and MeterDataRequestCredential. Two — ArrFiling and OutageNotification — are still work in progress, so don't build production against them yet.
>
> Read the "what it is" column carefully, because it tells you the pattern. There are payloads — MeterData, MeterDataRequest — and there are credentials that wrap those payloads to attest who sent them and that nothing changed. You'll see that pairing again and again.
>
> One thing that trips people up: the peer-to-peer trading and demand-flexibility schemas are not here. They're maintained upstream in the Digital Energy Grid project and mirrored under External Schemas — I'll show you where.
>
> Each family gets one plain-language page. Open ElectricityCredential and look at the structure: eleven numbered sections — scope and purpose, what it records, how each item is identified, the standards it's based on, where Indian standards don't yet exist, then Schedule I, the field summary, and open points for confirmation. Every schema page and every use-case page uses this same template, so once you've read one, you can navigate all of them.

---

### 4:00–6:15 · Schemas — the developer catalog

**On screen:**
- *4:00 — Tab 4, All Schemas. Hover the three cards under "Verifiable Credentials", then the four under "Data Exchange payloads". Scroll to "How versions work" at 4:25.*
- *4:35 — Tab 5, Schemas › ElectricityCredential. Hold on the top table (Canonical base, Latest version, Status, Used in). Then scroll to the "Developer resources — v1.2 (current)" table and hover each row as you name the file.*
- *5:15 — Tab 6, ElectricityCredential v1.2. Show the "Files" bar, then scroll to the "Structure" tree, then the "EnergyResource kinds" table, then the "v1.1 → v1.2 migration" table, then a glimpse of the "Field reference".*
- *5:55 — Tab 7, Term Taxonomy: hold on the opening paragraph and the family-code table. 6:05 — Tab 8, External Schemas: hold on the "Energy Trading (P2P)" heading.*

> Now the developer catalog. All Schemas groups the seven families into two kinds: Verifiable Credentials — signed records a holder keeps and verifies independently of any network — and Data Exchange payloads — structured records exchanged over the network or published as feeds. Below that is the versioning rule, worth memorising: a non-breaking change — an optional field, a new enum value — stays within the minor version. A breaking change gets a new sibling version, and the old one stays reachable.
>
> Open a family page — ElectricityCredential. The top table gives the canonical base URL, the latest version, the status, who issues and consumes it, and which use cases it's used in. Then six developer files per version. `attributes.yaml` is the OpenAPI source of truth. `schema.json` is the compiled JSON Schema — **this is the file you validate against**. `context.jsonld` and `vocab.jsonld` carry the semantics and the mapping to standards like the IEC Common Information Model. And `examples` are worked payloads you can copy.
>
> The version page is where you'll spend your time. The structure tree: a non-PII `customerProfile` — customer number, an `energyResources` array, consumption profiles — and an optional PII `customerDetails` block, kept separate on purpose. Every energy resource is discriminated by `type` into one of seven kinds: meter, generator, storage, EV charger, inverter, controllable load, network equipment. Every power or capacity field is a `{value, unit}` pair, not a bare number — the big change from 1.1, and the migration table spells it out. Below that, the field reference: bold with an asterisk means required, and where a field derives from a standard, the description starts with "Based on" and names it.
>
> Two more pages to keep open. Term Taxonomy lists every term across all seven families — 368 of them — with schema code and source standard, so you can check whether the field you're about to invent already exists. And External Schemas is where the P2P and flexibility schemas from the Digital Energy Grid project are mirrored, with a link to their canonical home.

---

### 6:15–7:00 · MeterData and the request/credential pairing

**On screen:** Tab 9, MeterData v0.6. *Hold on the opening paragraph, then scroll to wherever the profile list is visible. At 6:40, switch to Tab 10 (Smart Meter Data Exchange overview, section 2) and hold on the eight-profile table.*

> The other schema you'll almost certainly touch is MeterData. It's the telemetry payload: nine record shapes — eight profiles plus a shared descriptor. The profiles cover every cadence a meter produces: CUSTOMER for slow-changing metadata, INTERVAL for 15- or 30-minute block load survey, DAILY, MONTHLY for billing resets, BILL_DETAILS, INSTANTANEOUS snapshots, and EVENT and ALARM from the IS 15959 codes. It's deliberately compact — a daily interval row can be a handful of numbers — and it carries no signature.
>
> That's why the family comes as a set of four. MeterDataRequest is how you ask for telemetry — the query, capabilities and authorisation. MeterDataCredential wraps MeterData when you need signed provenance. MeterDataRequestCredential wraps the request to prove the requester is authorised. Payload plus credential, request plus credential.

---

### 7:00–7:40 · Use Case Overviews — five use cases, and which schema each one rides on

**On screen:** Tab 1 sidebar, or simply the sidebar on the current tab. *Hover each of the five Use Case Overviews entries as you name them.*

> Now the use cases, where a schema becomes a build. There are five, and each is really a schema plus a delivery pattern.
>
> **Consumer Energy Passport**: ElectricityCredential issued holder-bound to a consumer's wallet. **Consumer Meter Digest**: MeterDataCredential issued to the consumer, wrapping their own readings. **Smart Meter Data Exchange**: MeterData and MeterDataRequest moving machine-to-machine over Beckn. **DER Visibility**: ElectricityCredential for what's connected plus MeterData for what it's doing — the feeder-level aggregate is still illustrative, and the page says so. **P2P Energy Transaction** rides on the external Digital Energy Grid contract schemas.
>
> Let's open two — one consumer credential flow and one business-to-business exchange — because those are the two shapes every IES build takes.

---

### 7:40–9:30 · Consumer Energy Passport — overview, then the implementation guide

**On screen:**
- *7:40 — Tab 11, Consumer Energy Passport overview. Hold on the italic summary and the "Implementation Guide →" link. Click that link at 8:00 (or switch to Tab 12).*
- *8:00 — Tab 12, implementation guide. Show the "In a hurry? Jump to the Checklist" line. Scroll to "How it differs from a bearer ElectricityCredential" and hold on the two-row table.*
- *8:35 — scroll to "Actors and flow", then "Building blocks", then "Setup: Register → Discover → Exchange" (the five numbered steps).*
- *9:05 — scroll to "DigiLocker integration (DocType NYCER)" briefly, then to the "Checklist" and hold there.*

> The overview page is the decision-maker's version — the same eleven-section template, ending in Schedule I, the exact field list for this use case. The link at the top takes you to the implementation guide, which is what you'll build from.
>
> The guide opens with the single most important sentence: the Passport is not a new credential type. It's the existing ElectricityCredential v1.2, shaped, issued and delivered for a consumer audience. Exactly two things differ from a plain bearer credential: the `credentialSubject.id` is set to the consumer's wallet DID, and `customerProfile.idRef` carries a verified government-ID reference — a reference, never the raw number. Everything else, including the `type` array, is identical.
>
> Three actors: the DISCOM issues, the consumer holds it in DigiLocker or a DID wallet, and a bank, marketplace or subsidy portal verifies it offline against the DISCOM's published key — no phone call to the DISCOM. The building-blocks table links each piece to its concept page. Then the setup section gives you the sequence: register your `did:web` and run OpenCred; decide and document your identity-proofing method; issue the credential with the two fields set; deliver into DigiLocker; and wire revocation into the same flow.
>
> For Indian consumers, delivery is DigiLocker, and the guide gives you the actual Pull URI request and response shapes for the NYCER document type. And at the bottom is the checklist — grouped by prerequisites, identity proofing, delivery, credential content, and verification. Every guide ends with one of these. If you only read one part of a guide, read the checklist.

---

### 9:30–10:40 · Smart Meter Data Exchange — the B2B pattern

**On screen:** Tab 13, Smart Meter Data Exchange implementation guide, at "Setup: Register → Discover → Exchange". *Scroll slowly through steps 1 to 7, pausing on step 4 ("publish your dataset catalogue (BPP)") and step 6 ("connect your real metering system"). At 10:25, scroll to "Checklist for your meter-data rollout".*

> The other shape is machine-to-machine. Smart Meter Data Exchange is an AMISP, a DISCOM, a regulator or a consented third party moving telemetry over Beckn, and the guide walks it as seven steps.
>
> Decide scope — which profiles, which cadence. Register — get your network identity. Discover — stand up the Data Exchange adapters; this is Beckn ONIX, a ready-made engine you deploy rather than write. Exchange — publish your dataset catalogue as the provider side, the BPP. Exercise the flow end-to-end against a sandbox peer. Only then connect your real head-end or MDM system. And optionally, at the very end, adopt the `did:web` convention for meters and assets — the guide is explicit that bare meter serial numbers work in payloads to begin with. No new identifiers to allocate.
>
> Notice what's the same across both guides: register once, stand up an engine, map your data into the schema, validate, exercise the flow, tick the checklist. Where they differ is which engine — OpenCred for credentials, ONIX for network exchange — and that's exactly what the Concepts section is about.

---

### 10:40–12:10 · Concepts — the one-time setup, conformance, and your pathway

**On screen:**
- *10:40 — Tab 14, Before you build. Hold on the three numbered steps, then scroll to the setup table (Register / Exchange / Credentials / Adapter / Conformance with times).*
- *11:15 — scroll to "What you need" and "What you do NOT need". Hover the crossed-out items.*
- *11:35 — Tab 15, Conformance Checklist at "What conformance means". Hover the [all] / [credential] / [beckn] tags. Then scroll to "What schema validation proves — and what it doesn't" and hold briefly.*
- *11:55 — Tab 16, Pathways › Overview. Hover the five rows.*

> Before you build is the page to hand to your IT and security team. Every participant does the same setup once: register in DeDi and publish a `did:web`; stand up the Beckn ONIX adapter; pass the conformance check. Two pieces slot in depending on what you build: OpenCred, if you issue credentials to consumers, and your internal-facing adapter — the only place you write code — typically 200 to 1,000 lines per use case, mapping your existing systems to the IES schema.
>
> The table gives honest estimates: a day or two for identity, a day or two for the engine, half a day for credentials, one to three weeks for the first adapter, a day for conformance. You need a domain you control, DNS access for one TXT record, one Linux host running Docker, and one engineer. You don't need a new database, a compliance filing, a procurement contract, a licence fee, or anyone's approval to start on the sandbox.
>
> The Conformance Checklist is tagged — "all", "credential" only if you issue credentials, "beckn" only if you're on the network — so a credential-only issuer skips the network items. It's also honest about scope: it says what passing local schema validation proves and what it doesn't. Read that before you tell anyone you're conformant.
>
> Finally, Pathways: one page per role — DISCOM, AMISP or OEM, regulator, secretariat, researcher — sequencing all of this. The Technology Service Provider pathway is especially useful for vendors: it separates the ready-made engine you deploy from the mapping you're actually hired to build.

---

### 12:10–13:50 · Propose a Schema

**On screen:**
- *12:10 — Tab 17, Propose a Schema, at the lifecycle diagram. Hover each box left to right as you name the stage.*
- *12:45 — scroll to the stage table, then the "Revising an existing schema" paragraph.*
- *13:05 — scroll to the info box with the two references (taxonomy and the use-case overview template), then to the inline form. Scroll the form slowly so the question labels are readable. Do not fill it in on camera.*
- *13:35 — Tab 18, GitHub issue tracker. Hold on the list.*

> Sooner or later you'll have a domain object IES doesn't cover — a new asset type, a new filing, a new feed. That's what Propose a Schema is for, and it runs on a fixed four-week lifecycle.
>
> Day zero, you submit the proposal with a concept note, and a public GitHub issue opens — that issue stays the single record through every stage. Weeks one and two are open ecosystem comments, freezing the schema at 0.1. Week three is targeted expert review, producing 0.2. Week four: architecture review against IES conventions, then the IES Cell finalises the schema and turns your concept note into the use-case write-up, then CEA and the authorities sign off, and it's published. Revisions follow the same flow with the same versioning rule.
>
> Keep two references open while you write: the Term Taxonomy, so you reuse published terms rather than redefine them, and the use-case overview template on GitHub, which structures your concept note in the same eleven sections you've seen all through this site. Share the note as a public link.
>
> The form is right here on the page: who you are, which use case the schema supports, the schema itself, the standards it builds on. Your email and mobile stay private with the secretariat; everything else becomes the public tracking issue automatically. No GitHub account needed — though if you give your username, you'll be tagged on the issue.
>
> And that issue tracker is where the discussion happens, in the open.

---

### 13:50–15:00 · Wrap — the path in one breath, and where things stand

**On screen:** Tab 19, Getting Started at "Where things stand" and then "Get in touch". *Hover the PDF link, the two email addresses, and the GitHub link as you mention them. End on the sidebar with Schemas Overview highlighted.*

> So here's the path, in one breath. Read Getting Started for register, discover, exchange. Read the Schemas Overview page for your schema for the why, then the catalog page for the field reference, and validate against `schema.json`. Pick the use case that matches your build, read the implementation guide, and work its checklist. Do the one-time setup from Before you build and sign off with the Conformance Checklist. And when your use case needs a schema that doesn't exist yet, propose it.
>
> One honest note on status. The specifications are published and versioned, and four pilot DISCOMs — PVVNL, APEPDCL, DGVCL and Tata Power — each built an adapter and demonstrated four use cases in a 30-day challenge. That challenge is a completed event; the site's Status page is the single source for what is running today, so check it rather than assume.
>
> This whole reference is also a single PDF, linked here. Questions go to the IES Secretariat or REC, and issues and contributions to the GitHub repository. Start with Schemas Overview. See you in the issue tracker.

---

## Timing checkpoints

Glance at the clock at these points. If you're more than 30 seconds behind, apply the cuts below in order.

| Checkpoint | Target | Segment ending |
|---|---|---|
| A | 2:40 | Map of the docs |
| B | 6:15 | Schemas developer catalog |
| C | 9:30 | Consumer Energy Passport |
| D | 12:10 | Concepts / Pathways |
| E | 15:00 | Wrap |

## If you're running long

Cut in this order. Each cut removes a self-contained beat and none of them break the narrative.

1. **Term Taxonomy and External Schemas** (5:55–6:15, ~25 s). Replace with one sentence: "Two more pages to keep open: Term Taxonomy, which lists every published term, and External Schemas, where the P2P schemas live."
2. **DigiLocker beat** (9:05–9:15, ~10 s). Say only "delivery for Indian consumers is DigiLocker, and the guide has the exact request and response shapes."
3. **"What you do NOT need" list** (11:15–11:35, ~20 s). Keep "one domain, one host, one engineer" and drop the crossed-out list.
4. **Pathways** (11:55–12:10, ~15 s). Replace with "and Pathways sequences all of this by the kind of organisation you are."
5. **GitHub issue tracker tab** (13:35–13:50, ~15 s). Drop Tab 18 entirely.

Applying all five saves about 85 seconds.

## If you have time to spare

Add, in this order:

1. At 5:55, open the `examples/` link on the v1.2 page and show `example.json` for ten seconds: "one meter, a solar array, a wind turbine and two batteries in one credential."
2. At 10:40, open Concepts › Setting up Register and show the numbered copy-paste steps: "the setup pages are do-guides — prerequisites, numbered steps, checklist — with an in-depth page nested under each for the why."

## Recording notes per segment

- **Cold open:** don't read the whole first paragraph off the screen; the viewer can see it. Speak over it.
- **Schemas catalog:** this is the densest segment. Scroll *slowly*; the field tables are the point. Resist the urge to explain individual fields beyond the ones scripted.
- **Use-case guides:** the checklist is the money shot. Hold on it for a full five seconds in silence before moving on.
- **Propose a Schema:** do not submit the form on camera. Scroll it so labels are readable and move on.
- **Wrap:** slow down. This is the segment people will rewind.

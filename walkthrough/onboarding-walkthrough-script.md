# IES Documentation Walkthrough — 15-minute onboarding script

**Who it is for:** an engineer or architect at a DISCOM, AMISP, OEM, or system integrator who was told "build this with IES" and is opening the GitBook for the first time.

**What they can do at the end:** explain IES in one sentence, find the schema for their project, read a schema page like a developer, open the right use-case guide and its checklist, know the one-time setup, and propose a schema when one is missing.

**Style:** an explainer with your hands on the docs. Most of the time you are explaining while you navigate, the way a colleague would walk you through a site. Five short moments ask the viewer to try something themselves. Short sentences, plain words, no jargon left unexplained.

**Source:** [india-energy-stack.gitbook.io/docs](https://india-energy-stack.gitbook.io/docs), as rendered from this repository on 2026-09-06. Sidebar labels are quoted exactly from `SUMMARY.md`.

**Length:** about 2,100 words of narration. At 150 words per minute that is about 14 minutes. The five pauses and the on-camera clicks fill it to 15:00.

---

## Before you hit record

1. **Pre-open every page as a tab, in order** (table below). Where the script says **click**, click the real link on camera. The tabs are your safety net if a link is slow.
2. **Browser prep.** One clean profile. No extensions or bookmarks bar. Window at 1920×1080. Page zoom 110–125% so tables read on a phone. Pick one theme and keep it.
3. **Collapse sidebar groups** you are not on, so the whole sidebar fits in one frame for Step 2.
4. **Test the search.** Type `sanctionedLoad` in the GitBook search box and confirm Term Taxonomy appears in the results. If it does not, use the fallback in Step 6.
5. **Test the Propose form.** Open Propose a Schema and confirm the inline form renders. If not, pre-open the "open it in a new tab" link on that page.
6. **Test the Pathway step.** Open the Technology Service Provider Pathway and check that steps expand when clicked. If they render already expanded, just scroll to Step 1.2 in Step 10.
7. **Pointer discipline.** Hover what you are talking about. Do not circle the cursor.

### Tabs to pre-open (in recording order)

Sidebar path is the authoritative locator. URLs are given only where the docs themselves cite them.

| # | Sidebar path | Where to be | Known URL |
|---|---|---|---|
| 1 | Getting Started | Top | `https://india-energy-stack.gitbook.io/docs` |
| 2 | Schemas Overview › Schemas Overview | Top (the status table) | — |
| 3 | Schemas Overview › ElectricityCredential | Top | — |
| 4 | Schemas › All Schemas | Top | — |
| 5 | Schemas › ElectricityCredential | Top | — |
| 6 | Schemas › ElectricityCredential › v1.2 | Top | `https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2` |
| 7 | GitHub: `example.json` for ElectricityCredential v1.2 | Top of file | `https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/ElectricityCredential/v1.2/examples/example.json` |
| 8 | Schemas › MeterData › v0.6 | Top | `https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6` |
| 9 | Schemas › Term Taxonomy | Top | `https://india-energy-stack.gitbook.io/docs/schemas/taxonomy` |
| 10 | Use Case Overviews › Consumer Energy Passport | Top | — |
| 11 | Use Case Implementation Guides › Consumer Energy Passport | Top | — |
| 12 | Use Case Implementation Guides › Smart Meter Data Exchange | Heading "Setup: Register → Discover → Exchange" | — |
| 13 | Concepts › Before you build | Top | — |
| 14 | Concepts › Conformance Checklist | Heading "What conformance means" | — |
| 15 | Pathways › Technology Service Provider Pathway | Heading "Phase 1" | — |
| 16 | Propose a Schema | Top (the lifecycle diagram) | — |
| 17 | GitHub issue tracker | Issues list | `https://github.com/India-Energy-Stack/ies-accelerator/issues` |
| 18 | Getting Started (again) | Heading "Where things stand" | `https://india-energy-stack.gitbook.io/docs` |

---

## The script

Each step has up to five parts. **Goal** is what the viewer can do after the step. **On screen** is what you record, with **click** and **type** actions in bold. **Say** is the narration, read as written. **Pause** appears in five steps only, where the viewer tries something themselves. **Check** is what they should know before moving on; it is a note to you, not a line to read aloud.

---

## Part 1 · The idea

### Step 0 · 0:00–0:35 · Welcome

**Goal:** the viewer knows what the next fifteen minutes cover and opens the site alongside.

**On screen:** Tab 1, Getting Started, top of page. Hold on the first two paragraphs. Do not scroll yet.

> Welcome. This is a walkthrough of the India Energy Stack documentation. It is for you if someone said "build this with IES" and you are opening these docs for the first time.
>
> We will do it in five parts. First, the idea behind IES. Then the schemas, which are what you code against. Then the use cases, which turn a schema into a build. Then the setup every participant does once. And last, how to propose a schema of your own.
>
> Open the site in another window. I will ask you to pause and try things as we go.

**Check:** the viewer has the site open next to the video.

---

### Step 1 · 0:35–1:50 · Learn the three moves

**Goal:** the viewer can say what IES is, and what it is not, in one breath.

**On screen:** Tab 1. Scroll to the paragraph beginning "IES works the way UPI works". Then scroll to the heading **"How IES works — Register, Discover, Exchange"**. Hover each bold word as you say it. At 1:35, scroll to "The specifications cover five building blocks".

> Start on the home page. Read this paragraph with me. IES works the way UPI works for payments. It holds no data of its own. Your data stays in the systems that already hold it. IES only defines how two systems find each other and share data in one common, verifiable shape.
>
> Every exchange has three moves. Register. Discover. Exchange.
>
> Register means you get a digital identity, a W3C DID, and a listing in a shared directory called DeDi. You do this once.
>
> Discover means two systems look each other up and agree terms over the Beckn protocol. No one-off integration.
>
> Exchange means data moves over that same signed channel, shaped by the IES schemas. When a lasting record is needed, the exchange produces a Verifiable Credential. Consumers keep theirs in DigiLocker.
>
> Under those three moves sit five building blocks: identifiers, registries, exchange, credentials, and the security and consent rules that run through all of them.
>
> Remember what IES is not. It is not a platform, a database, or a product. It picks an open standard for each block and writes a specification on top.

**Check:** register, discover, exchange. IES holds no data.

---

### Step 2 · 1:50–2:30 · Learn the map

**Goal:** the viewer knows the seven sidebar groups and the reading order.

**On screen:** Tab 1. Keep the page still. Move the pointer down the sidebar and rest on each group as you name it: Schemas Overview, Schemas, Use Case Overviews, Use Case Implementation Guides, Pathways, Concepts, then up to Propose a Schema. Hover Draft last.

> Now look at the sidebar. This is the whole site, and the order matters.
>
> Schemas Overview explains each schema in plain words. Schemas is the developer catalog: fields, URLs, versions. Use Case Overviews and Implementation Guides cover the same five use cases, first for decision makers, then as build checklists. Pathways sorts all of this by the kind of organisation you are. Concepts is the one-time setup. And Propose a Schema, at the top, is how the catalog grows.
>
> Skip the Draft section. It is work in progress.
>
> We will go top to bottom: schemas, use cases, setup, propose.

**Check:** the viewer can point to each group.

---

## Part 2 · The schemas

### Step 3 · 2:30–3:45 · Find your schema

**Goal:** the viewer finds the schema family their project needs.

**On screen:** **Click** Schemas Overview in the sidebar (Tab 2). Hold on the status table. Select the five "Stable — In Pilot" rows as you name them. Hover the two "Work in progress" rows. At 3:20, **click** ElectricityCredential in the table (Tab 3) and scroll slowly down the numbered headings. Stop at "8. Schedule I".

> Open Schemas Overview. This table is the catalog on one screen. Seven schema families. Five are stable and were used in the pilot: ElectricityCredential, MeterData, MeterDataCredential, MeterDataRequest, and MeterDataRequestCredential. Two are still work in progress: ArrFiling and OutageNotification. Do not build production on those yet.
>
> Look at the "what it is" column. You will see a pattern. Some rows are payloads, like MeterData. Some rows are credentials that wrap a payload and prove who sent it. Payload, then credential. You will see this pair again.
>
> Pause the video here. Find the row that matches your project. If you issue something to a consumer, it is a credential. If you move readings between systems, it is a payload.
>
> One more thing. The peer-to-peer trading schemas are not in this table. They live upstream in the Digital Energy Grid project and are mirrored under External Schemas.
>
> Now click ElectricityCredential. Every schema page uses the same eleven sections: scope, what it records, how items are identified, the standards behind it, gaps in Indian standards, and the field summary in Schedule I. Learn this layout once. Every schema page and every use-case page follows it.

**Pause:** "Find the row that matches your project."

**Check:** the viewer has one schema family name written down.

---

### Step 4 · 3:45–6:00 · Read a schema like a developer

**Goal:** the viewer knows the six files per version, which one to validate against, and how to read the field table.

**On screen:**
- 3:45 — **Click** Schemas › All Schemas (Tab 4). Hover the three "Verifiable Credentials" cards, then the four "Data Exchange payloads" cards. Scroll to "How versions work".
- 4:15 — **Click** the ElectricityCredential card (Tab 5). Hold on the top table. Scroll to "Developer resources — v1.2 (current)" and hover each file as you name it.
- 4:50 — **Click** v1.2 in the sidebar (Tab 6). Show the "Structure" tree, then "EnergyResource kinds", then the "v1.1 → v1.2 migration" table, then the "Field reference".
- 5:35 — **Click** the `examples/` link in the Files bar. **Click** `example.json` (Tab 7). Scroll slowly through the `energyResources` array.

> Now open the Schemas section and click All Schemas. The same families, sorted by kind. Verifiable Credentials are signed records a holder keeps and can verify without any network. Data Exchange payloads are records moved over the network or published as feeds.
>
> Scroll to "How versions work". Learn this rule. A small, safe change stays in the same minor version. A breaking change gets a new version, and the old one stays online.
>
> Click ElectricityCredential. The top table tells you the canonical URL, the latest version, the status, and which use cases use it.
>
> Below that are six files for each version. `attributes.yaml` is the source of truth. `schema.json` is the compiled JSON Schema. This is the file you validate your payloads against. `context.jsonld` and `vocab.jsonld` map the fields to standards, like the IEC Common Information Model. And `examples` are real payloads you can copy.
>
> Click v1.2. This is the page you will live on. Look at the structure tree. The customer profile holds the account number and the list of energy resources. Personal details sit in a separate block, on purpose.
>
> Each energy resource has a type. There are seven kinds: meter, generator, storage, EV charger, inverter, controllable load, and network equipment. Every power or capacity value is a pair, a number and a unit. That is the big change from version 1.1, and the migration table lists every field.
>
> Scroll to the field reference. Bold with a star means required. When a field comes from a standard, the description starts with "Based on" and names it.
>
> Now click the examples link and open example.json. One meter, a solar array, a wind turbine, and two batteries, in one credential. Pause here and open the example for your own schema. Copying an example is the fastest way to start.

**Pause:** "Open the example for your own schema."

**Check:** the viewer knows to validate against `schema.json` and has an example open.

---

### Step 5 · 6:00–6:40 · Meet the MeterData set

**Goal:** the viewer understands the four-schema MeterData family.

**On screen:** **Click** Schemas › MeterData › v0.6 in the sidebar (Tab 8). Hold on the opening paragraph, then scroll until the profile names are visible. At 6:25, hover MeterDataRequest, MeterDataCredential, and MeterDataRequestCredential in the sidebar as you name them.

> Back to the catalog. Open MeterData v0.6. This is the telemetry payload. It has eight profiles, one for each cadence a meter produces: customer metadata, interval readings, daily, monthly, bill details, instantaneous snapshots, events, and alarms. It is small on the wire and carries no signature.
>
> That is why it comes as a set of four. MeterDataRequest is how you ask for data. MeterDataCredential wraps the data when you need proof of who sent it. MeterDataRequestCredential wraps the request to prove you may ask. Payload and credential. Request and credential.

**Check:** four names, two pairs.

---

### Step 6 · 6:40–7:10 · Try the search

**Goal:** the viewer uses site search and the Term Taxonomy before inventing a field.

**On screen:** **Click** the search box at the top. **Type** `sanctionedLoad`. Hover the results. **Click** the Term Taxonomy result (Tab 9) and select the `sanctionedLoad` row. *Fallback if search does not list Taxonomy: open Tab 9 and use browser find (Ctrl+F) for `sanctionedLoad`.*

> Let's try something. Click the search box at the top and type "sanctionedLoad". You get hits in more than one place. Open Term Taxonomy. Here is the row. It appears in ElectricityCredential and in MeterData, with the same meaning.
>
> Taxonomy lists every published term, 368 of them. Before you invent a field, search here first. Try it now with one field name from your own system.

**Pause:** "Try it with one field name from your own system."

**Check:** the viewer has searched once.

---

## Part 3 · The use cases

### Step 7 · 7:10–7:45 · Match a use case to a schema

**Goal:** the viewer picks the use case that matches their build.

**On screen:** Stay on the current tab. Hover each of the five entries under **Use Case Overviews** in the sidebar as you name them.

> Now the use cases. Look at the five names in the sidebar. Each one is a schema plus a way to deliver it.
>
> Consumer Energy Passport is ElectricityCredential, issued to a consumer's wallet. Consumer Meter Digest is MeterDataCredential, issued to a consumer. Smart Meter Data Exchange is MeterData moving between systems over Beckn. DER Visibility is ElectricityCredential for what is connected, plus MeterData for what it is doing. P2P Energy Transaction uses the external trading schemas.
>
> Pick yours now. We will walk one credential build and one data-exchange build, because every IES build is one of those two.

**Pause:** "Pick yours now."

**Check:** the viewer has a use case name written next to their schema name.

---

### Step 8 · 7:45–9:30 · Walk a credential build

**Goal:** the viewer can navigate an implementation guide and knows to work from its checklist.

**On screen:**
- 7:45 — **Click** Use Case Overviews › Consumer Energy Passport (Tab 10). Hold on the italic first line. **Click** the "Implementation Guide →" link (Tab 11).
- 8:00 — Show the "In a hurry? Jump to the Checklist" line. Scroll to "How it differs from a bearer ElectricityCredential". Hold on the two-row table.
- 8:30 — Scroll to "Actors and flow", then "Setup: Register → Discover → Exchange". Hover each of the five steps.
- 9:05 — Scroll past "DigiLocker integration (DocType NYCER)". **Click** the "Jump to the Checklist" link at the top, or scroll to "Checklist". Hold there for five seconds.

> Open the Consumer Energy Passport overview. The first line tells you everything. It is ElectricityCredential v1.2, issued to a consumer's wallet. Click the Implementation Guide link at the top.
>
> The guide starts with a shortcut. "In a hurry? Jump to the Checklist." Use it later. For now, scroll to the table "How it differs from a bearer ElectricityCredential". Only two fields change. The credential subject id becomes the consumer's wallet DID. And the id reference holds a verified government ID reference, never the raw number. Everything else is the same credential.
>
> Next, "Actors and flow". The DISCOM issues. The consumer holds it in DigiLocker or a wallet. A bank or subsidy portal verifies it offline against the DISCOM's public key. No phone call.
>
> Now "Setup". Five steps. Register your `did:web` and run OpenCred. Choose and document how you prove identity. Issue the credential with those two fields set. Deliver it to DigiLocker. Wire revocation into the same flow.
>
> Below that, the DigiLocker section gives you the exact request and response shapes for document type NYCER.
>
> And here is the checklist. Prerequisites, identity proofing, delivery, credential content, verification. Every guide ends with one of these. When you build, work down this list.

**Check:** the viewer knows every guide ends in a checklist.

---

### Step 9 · 9:30–10:35 · Walk a data-exchange build

**Goal:** the viewer sees the machine-to-machine pattern and what both patterns share.

**On screen:** **Click** Use Case Implementation Guides › Smart Meter Data Exchange (Tab 12), at "Setup: Register → Discover → Exchange". Scroll slowly through steps 1 to 7. Pause on step 4 ("publish your dataset catalogue") and step 6 ("connect your real metering system").

> Now open the Smart Meter Data Exchange guide and scroll to Setup. This is the machine-to-machine shape. An AMISP, a DISCOM, or a regulator moving readings over Beckn.
>
> Seven steps. Decide scope: which profiles, which cadence. Register: get your network identity. Discover: stand up the Data Exchange adapter. This is Beckn ONIX, an engine you deploy, not code you write. Exchange: publish your dataset catalogue as the provider. Exercise the flow against a sandbox peer. Then, and only then, connect your real head-end system. Last, and optional, give meters `did:web` names. Plain serial numbers work in payloads to start.
>
> Notice what both guides share. Register once. Deploy an engine. Map your data into the schema. Validate. Exercise the flow. Tick the checklist. The only real difference is the engine: OpenCred for credentials, ONIX for network exchange. That is what the Concepts section covers.

**Check:** register, engine, map, validate, exercise, checklist.

---

## Part 4 · The setup

### Step 10 · 10:35–12:05 · Do the one-time setup

**Goal:** the viewer knows the three setup steps, the time each takes, and what conformance does and does not prove.

**On screen:**
- 10:35 — **Click** Concepts › Before you build (Tab 13). Hold on the three numbered steps. Scroll to the setup table with times.
- 11:10 — Scroll to "What you need" and "What you do NOT need". Hover the crossed-out items.
- 11:25 — **Click** Concepts › Conformance Checklist (Tab 14). Hover the [all], [credential], [beckn] tags. Scroll to "What schema validation proves — and what it doesn't".
- 11:45 — **Click** Pathways › Technology Service Provider Pathway (Tab 15). **Click** to expand "Step 1.2: Understand the Two-Part Adapter". Hover the Phase Advice quote.

> Open Concepts and click Before you build. This is the page to send to your IT and security team.
>
> Every participant does three things once. Register in DeDi and publish a `did:web`. Stand up the Beckn ONIX adapter. Pass the conformance check. Two more pieces depend on your build. OpenCred, if you issue credentials. And your own adapter, the only code you write, usually 200 to 1,000 lines per use case.
>
> Look at the time table. One or two days for identity. One or two days for the engine. Half a day for credentials. One to three weeks for your first adapter. One day for conformance.
>
> Scroll down. You need a domain, one DNS record, one Linux host with Docker, and one engineer. You do not need a new database, a new filing, a new contract, a licence, or anyone's approval to start in the sandbox.
>
> Now open Conformance Checklist. Each item is tagged. "All" is for everyone. "Credential" is for issuers. "Beckn" is for network participants. Read the section "What schema validation proves". It tells you the limits of a local pass. Read it before you say you are conformant.
>
> Last, Pathways. One page per role. Open the Technology Service Provider pathway and expand a step. Every step looks like this: advice, prework, then guidance with links. Vendors, this page separates the engine you deploy from the mapping you are hired to build.

**Check:** three steps, one engine, one adapter, one checklist.

---

## Part 5 · Growing the catalog

### Step 11 · 12:05–13:45 · Propose a schema

**Goal:** the viewer knows the four-week lifecycle and how to submit a proposal.

**On screen:**
- 12:05 — **Click** Propose a Schema (Tab 16). Hover each box in the lifecycle diagram, left to right, as you name the stage.
- 12:45 — Scroll to the stage table, then the paragraph "Revising an existing schema".
- 13:00 — Scroll to the info box with the two references. Then scroll the form slowly so each question label is readable. Do not fill it in.
- 13:30 — **Click** the "GitHub Issue Tracker" link (Tab 17). Hold on the list.

> One day you will need a schema IES does not have. A new asset type. A new filing. A new feed. Click Propose a Schema.
>
> The diagram shows a four-week lifecycle. Day zero, you submit a proposal with a concept note, and a public GitHub issue opens. That issue is the record for the whole journey. Weeks one and two, the community comments, and the schema freezes at version 0.1. Week three, chosen experts review it. Week four, an architecture review, then the IES Cell finalises it, the authorities sign off, and it is published. Changing an existing schema follows the same path.
>
> Scroll to the info box. Keep two things open while you write. The Term Taxonomy, so you reuse terms that already exist. And the use-case overview template, so your concept note has the same eleven sections you have seen all over this site. Share the note as a public link.
>
> Now the form. Who you are. Which use case your schema supports. The schema itself. The standards it builds on. Your email and phone stay private. Everything else becomes the public issue, automatically. You do not need a GitHub account.
>
> Open the issue tracker. This is where the discussion happens, in the open. Read a few proposals before you write yours.

**Check:** proposal, comments, expert review, architecture review, sign-off, published.

---

### Step 12 · 13:45–15:00 · Your first hour with IES

**Goal:** the viewer leaves with a six-item to-do list and an honest picture of status.

**On screen:** **Click** Getting Started (Tab 18). Scroll to "Where things stand". Hover the four DISCOM names. Then scroll to the PDF hint and "Get in touch". Hover the PDF link, the two email addresses, and the GitHub link. End on the sidebar with Schemas Overview highlighted.

> Here is your first hour with IES, as a to-do list.
>
> One. Read the home page for the three moves: register, discover, exchange.
> Two. Find your schema in Schemas Overview and read its page.
> Three. Open its catalog page, get `schema.json`, and copy an example.
> Four. Pick your use case and open its implementation guide. Read the checklist first.
> Five. Send Before you build to your IT team.
> Six. When a schema is missing, propose it.
>
> One honest note. The specifications are published and versioned. Four pilot DISCOMs, PVVNL, APEPDCL, DGVCL, and Tata Power, each built an adapter and showed four use cases in a 30-day challenge. That challenge is finished. The Status page is the only source for what runs today. Check it. Do not assume.
>
> The whole reference is also one PDF, linked here. Questions go to the IES Secretariat or REC. Issues and contributions go to GitHub.
>
> Start with Schemas Overview. See you in the issue tracker.

**Check:** the viewer has the six-item list.

---

## Timing checkpoints

| Checkpoint | Target | Step ending |
|---|---|---|
| A | 2:30 | Step 2, Learn the map |
| B | 6:00 | Step 4, Read a schema like a developer |
| C | 9:30 | Step 8, Walk a credential build |
| D | 12:05 | Step 10, Do the one-time setup |
| E | 15:00 | Step 12, Your first hour |

## If you're running long

Cut in this order. Each removes one self-contained beat. All five together save about 80 seconds.

1. **Step 6, Try the search** (30 s). Replace with one line in Step 4: "Before you invent a field, search the Term Taxonomy first."
2. **The example.json beat in Step 4** (5:35–6:00, ~20 s). Say only: "The examples link gives you real payloads to copy."
3. **"What you do NOT need" in Step 10** (11:10–11:25, ~15 s). Keep "a domain, one host, one engineer."
4. **The Pathway expand in Step 10** (11:45–12:05, ~15 s). Say only: "Pathways has one page per role."
5. **The issue tracker in Step 11** (13:30–13:45, ~15 s). Drop Tab 17.

## If you have time to spare

1. In Step 4, after example.json, open `schema.json` in the browser for five seconds: "This is the file your validator reads."
2. In Step 10, open Concepts › Setting up Register and show the numbered steps: "The setup pages are do-guides. Prerequisites, numbered steps, a checklist."

## Recording notes

- **Pauses.** When you say "pause the video here", stop talking for two full seconds before you continue. Editors can extend the gap; they cannot create one.
- **Clicks.** Move the pointer to the link, hold for half a second, then click. The viewer needs to see where you clicked.
- **Typing.** Type `sanctionedLoad` at a normal pace. Do not paste.
- **Schema pages.** Scroll slowly. The tables are the content.
- **Checklist.** Hold on it in silence for five seconds. It is the most important screen in the video.
- **Wrap.** Slow down. Read the six items as a list, with a beat between each.

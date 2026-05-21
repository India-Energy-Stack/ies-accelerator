# India Energy Stack (IES) Documentation Index

Welcome to the India Energy Stack (IES) documentation map. This index organizes all documentation files in the `ies-accelerator` repository sequentially and systematically by building blocks and phases.

---

## 📖 Foundational General References

These documents provide a general introduction, terminology definitions, and layout structures for the repository.

* **[README.md](README.md)**
  - *Summary*: Root-level introduction to the IES accelerator repository structure, standard protocols, and setup environment.
  - *Outline / Headings*:
    - [India Energy Stack — Accelerator](README.md#india-energy-stack-accelerator)
      - [Where to Start](README.md#where-to-start)
      - [Why IES?](README.md#why-ies)
      - [Key Standards and Protocols](README.md#key-standards-and-protocols)
      - [Related Repositories](README.md#related-repositories)
* **[getting-started.md](getting-started.md)**
  - *Summary*: A 5-minute technical orientation covering IES core capabilities, roles, prerequisites, and developer onboarding options.
  - *Outline / Headings*:
    - [Getting Started](getting-started.md#getting-started)
      - [What is the India Energy Stack?](getting-started.md#what-is-the-india-energy-stack)
        - [Identifiers and Addressing](getting-started.md#identifiers-and-addressing)
        - [Registries and Directories](getting-started.md#registries-and-directories)
        - [Energy Credentials](getting-started.md#energy-credentials)
        - [Data Exchange](getting-started.md#data-exchange)
      - [Choosing Your Path](getting-started.md#choosing-your-path)
      - [Key Terminology](getting-started.md#key-terminology)
      - [Prerequisites by Capability](getting-started.md#prerequisites-by-capability)
        - [Energy Credentials](getting-started.md#energy-credentials)
        - [Data Exchange](getting-started.md#data-exchange)
      - [Getting Help](getting-started.md#getting-help)
* **[glossary.md](glossary.md)**
  - *Summary*: A comprehensive directory defining energy, decentralized identity (DIDs, VCs), and Beckn protocol terms.
  - *Outline / Headings*:
    - [Glossary](glossary.md#glossary)
      - [Identity and credentials](glossary.md#identity-and-credentials)
        - [DID](glossary.md#did)
        - [DID methods used in IES](glossary.md#did-methods-used-in-ies)
        - [DeDi](glossary.md#dedi)
        - [Verifiable Credential (VC)](glossary.md#verifiable-credential-vc)
        - [Issuer / Holder / Verifier](glossary.md#issuer-holder-verifier)
        - [OpenCred](glossary.md#opencred)
        - [DigiLocker](glossary.md#digilocker)
        - [API Setu](glossary.md#api-setu)
      - [Data exchange and Beckn](glossary.md#data-exchange-and-beckn)
        - [Beckn](glossary.md#beckn)
        - [BAP](glossary.md#bap)
        - [BPP](glossary.md#bpp)
        - [ONIX](glossary.md#onix)
        - [DEG](glossary.md#deg)
        - [DDM](glossary.md#ddm)
        - [ERA](glossary.md#era)
      - [India energy sector](glossary.md#india-energy-sector)
        - [DISCOM](glossary.md#discom)
        - [AMISP](glossary.md#amisp)
        - [SERC](glossary.md#serc)
        - [ARR](glossary.md#arr)
        - [APR](glossary.md#apr)
        - [MYT](glossary.md#myt)
        - [True-up](glossary.md#true-up)
        - [ACS-ARR gap](glossary.md#acs-arr-gap)
        - [ATC loss](glossary.md#atc-loss)
        - [HT-LT](glossary.md#ht-lt)
        - [DT](glossary.md#dt)
        - [Feeder](glossary.md#feeder)
        - [ToD](glossary.md#tod)
        - [Regulatory asset](glossary.md#regulatory-asset)
        - [NP](glossary.md#np)
        - [RDSS](glossary.md#rdss)
        - [CIS](glossary.md#cis)
        - [NMS](glossary.md#nms)
        - [HES](glossary.md#hes)
        - [MDMS](glossary.md#mdms)
        - [DER](glossary.md#der)
      - [Standards and protocols](glossary.md#standards-and-protocols)
        - [CIM](glossary.md#cim)
        - [IEC 61968](glossary.md#iec-61968)
        - [DLMS-COSEM](glossary.md#dlms-cosem)
        - [MultiSpeak](glossary.md#multispeak)
        - [OpenADR](glossary.md#openadr)
        - [XBRL](glossary.md#xbrl)
        - [Akoma Ntoso](glossary.md#akoma-ntoso)
        - [DCAT 3](glossary.md#dcat-3)
        - [MQTT](glossary.md#mqtt)
        - [W3C VC](glossary.md#w3c-vc)
* **[SUMMARY.md](SUMMARY.md)**
  - *Summary*: Table of Contents sidebar structure configuration for GitBook deployment.
  - *Outline / Headings*:
    - [Table of contents](SUMMARY.md#table-of-contents)

---

## 🆔 1. Identifiers and Addressing (DIDs)

This block defines the cryptographic identity of utilities, consumers, assets, and datasets on the network.

### ⚙️ Setup & Configuration
* **[README.md](identifiers/README.md)**
  - *Summary*: Introduction to the IES addressing layer, design principles, and role-based onboarding paths.
  - *Outline / Headings*:
    - [IES Identifiers and Addressing](identifiers/README.md#ies-identifiers-and-addressing)
      - [What you can do with this section](identifiers/README.md#what-you-can-do-with-this-section)
      - [Reading order](identifiers/README.md#reading-order)
      - [Design principles](identifiers/README.md#design-principles)
      - [Quick orientation by role](identifiers/README.md#quick-orientation-by-role)
* **[concepts.md](identifiers/concepts.md)**
  - *Summary*: Cryptographic theory behind DIDs (did:web, did:key, did:dedi) and identifier vs. record separation.
  - *Outline / Headings*:
    - [Identifier Concepts](identifiers/concepts.md#identifier-concepts)
      - [What is a DID?](identifiers/concepts.md#what-is-a-did)
      - [What a DID Document contains](identifiers/concepts.md#what-a-did-document-contains)
      - [DID methods used in IES](identifiers/concepts.md#did-methods-used-in-ies)
        - [`did:web`](identifiers/concepts.md#didweb)
        - [`did:key`](identifiers/concepts.md#didkey)
        - [`did:jwk`](identifiers/concepts.md#didjwk)
        - [`did:dedi` (DeDi-anchored)](identifiers/concepts.md#diddedi-dedi-anchored)
      - [When to use which method](identifiers/concepts.md#when-to-use-which-method)
      - [Identifier vs. record](identifiers/concepts.md#identifier-vs-record)
      - [Where each ID lives](identifiers/concepts.md#where-each-id-lives)
* **[id-patterns.md](identifiers/id-patterns.md)**
  - *Summary*: Grammar conventions and syntax rules for minting identifiers for DISCOMs, consumers, regulators, and assets.
  - *Outline / Headings*:
    - [ID Patterns](identifiers/id-patterns.md#id-patterns)
      - [Conventions used in this section](identifiers/id-patterns.md#conventions-used-in-this-section)
      - [1. DISCOM (Issuer)](identifiers/id-patterns.md#1-discom-issuer)
        - [Identifier](identifiers/id-patterns.md#identifier)
        - [Example — TPDDL](identifiers/id-patterns.md#example-tpddl)
        - [How it relates to your internal world](identifiers/id-patterns.md#how-it-relates-to-your-internal-world)
        - [Where it goes](identifiers/id-patterns.md#where-it-goes)
      - [2. Regulator](identifiers/id-patterns.md#2-regulator)
        - [Identifier](identifiers/id-patterns.md#identifier)
        - [Example — Delhi Electricity Regulatory Commission](identifiers/id-patterns.md#example-delhi-electricity-regulatory-commission)
      - [3. Consumer](identifiers/id-patterns.md#3-consumer)
        - [Two distinct identifiers for the same human](identifiers/id-patterns.md#two-distinct-identifiers-for-the-same-human)
        - [Consumer reference ID — the grammar](identifiers/id-patterns.md#consumer-reference-id-the-grammar)
        - [Example — TPDDL consumer](identifiers/id-patterns.md#example-tpddl-consumer)
        - [Holder DID — generated by the wallet](identifiers/id-patterns.md#holder-did-generated-by-the-wallet)
        - [Linking them](identifiers/id-patterns.md#linking-them)
        - [Why this preserves DISCOM autonomy](identifiers/id-patterns.md#why-this-preserves-discom-autonomy)
      - [4. Asset (Transformer, Feeder, Substation, Solar Plant)](identifiers/id-patterns.md#4-asset-transformer-feeder-substation-solar-plant)
        - [Identifier](identifiers/id-patterns.md#identifier)
        - [Example — a TPDDL distribution transformer](identifiers/id-patterns.md#example-a-tpddl-distribution-transformer)
        - [Example — a 220kV substation](identifiers/id-patterns.md#example-a-220kv-substation)
        - [The asset record](identifiers/id-patterns.md#the-asset-record)
        - [Meters as a special case](identifiers/id-patterns.md#meters-as-a-special-case)
      - [5. Service Connection](identifiers/id-patterns.md#5-service-connection)
      - [6. Credential identifiers and revocation handles](identifiers/id-patterns.md#6-credential-identifiers-and-revocation-handles)
      - [7. Dataset (Beckn `DatasetItem`)](identifiers/id-patterns.md#7-dataset-beckn-datasetitem)
      - [Summary table](identifiers/id-patterns.md#summary-table)
* **[registries.md](identifiers/registries.md)**
  - *Summary*: Overview of namespace registry mappings and layout conventions for public and private DeDi tables.
  - *Outline / Headings*:
    - [Registries — Public and Private](identifiers/registries.md#registries-public-and-private)
      - [DeDi registry model in 30 seconds](identifiers/registries.md#dedi-registry-model-in-30-seconds)
      - [The public IES registries](identifiers/registries.md#the-public-ies-registries)
        - [IES DISCOMs Reference Registry](identifiers/registries.md#ies-discoms-reference-registry)
        - [IES Regulators Reference Registry](identifiers/registries.md#ies-regulators-reference-registry)
        - [IES Schemas Registry (forthcoming)](identifiers/registries.md#ies-schemas-registry-forthcoming)
      - [Per-DISCOM public registries](identifiers/registries.md#per-discom-public-registries)
        - [Required: revocation registry](identifiers/registries.md#required-revocation-registry)
        - [Recommended: asset registry](identifiers/registries.md#recommended-asset-registry)
        - [Optional: consumer reference registry](identifiers/registries.md#optional-consumer-reference-registry)
        - [Optional: dataset registry](identifiers/registries.md#optional-dataset-registry)
      - [Private registries inside the DISCOM](identifiers/registries.md#private-registries-inside-the-discom)
        - [What to host privately](identifiers/registries.md#what-to-host-privately)
        - [Structure](identifiers/registries.md#structure)
        - [Implementation options](identifiers/registries.md#implementation-options)
        - [Promotion: private → public](identifiers/registries.md#promotion-private-public)
        - [Linkage between private and public records](identifiers/registries.md#linkage-between-private-and-public-records)
      - [Governance and key management for namespaces](identifiers/registries.md#governance-and-key-management-for-namespaces)
        - [Recommended posture](identifiers/registries.md#recommended-posture)
        - [Key rotation](identifiers/registries.md#key-rotation)
      - [Operational guidance](identifiers/registries.md#operational-guidance)

### 🔌 Use & Operations
* **[resolution.md](identifiers/resolution.md)**
  - *Summary*: Detailed specification of did:web, did:key, and did:dedi resolvers, error matrices, and caching rules.
  - *Outline / Headings*:
    - [Resolution and Routing](identifiers/resolution.md#resolution-and-routing)
      - [The resolver](identifiers/resolution.md#the-resolver)
      - [Resolution by DID method](identifiers/resolution.md#resolution-by-did-method)
        - [`did:web`](identifiers/resolution.md#didweb)
          - [Illustrative `did.json` Document for a Utility](identifiers/resolution.md#illustrative-didjson-document-for-a-utility)
        - [`did:key` and `did:jwk`](identifiers/resolution.md#didkey-and-didjwk)
        - [`did:dedi:<ns>:<reg>:<id>`](identifiers/resolution.md#diddedi)
      - [Workflow 1 — Verifying a credential](identifiers/resolution.md#workflow-1-verifying-a-credential)
      - [Workflow 2 — Issuing a credential](identifiers/resolution.md#workflow-2-issuing-a-credential)
      - [Workflow 3 — Routing a Beckn message](identifiers/resolution.md#workflow-3-routing-a-beckn-message)
      - [Workflow 4 — Cross-DISCOM consumer move](identifiers/resolution.md#workflow-4-cross-discom-consumer-move)
      - [Workflow 5 — Resolving an asset for an outage notification](identifiers/resolution.md#workflow-5-resolving-an-asset-for-an-outage-notification)
      - [Caching strategy](identifiers/resolution.md#caching-strategy)
      - [Error handling](identifiers/resolution.md#error-handling)
      - [SDK shape](identifiers/resolution.md#sdk-shape)
* **[issuance-reference.md](identifiers/issuance-reference.md)**
  - *Summary*: Worked reference implementation (Python/OpenSSL) for key generation, did.json creation, and credential issuance.
  - *Outline / Headings*:
    - [Issuance Reference Implementation](identifiers/issuance-reference.md#issuance-reference-implementation)
      - [Prerequisites](identifiers/issuance-reference.md#prerequisites)
      - [Step 1 — Mint the issuer DID (`did:web`)](identifiers/issuance-reference.md#step-1-mint-the-issuer-did-didweb)
      - [Step 2 — Register the DISCOM in the IES Reference Registry](identifiers/issuance-reference.md#step-2-register-the-discom-in-the-ies-reference-registry)
      - [Step 3 — Stand up your per-DISCOM revocation registry](identifiers/issuance-reference.md#step-3-stand-up-your-per-discom-revocation-registry)
      - [Step 4 — Mint and register a consumer reference ID](identifiers/issuance-reference.md#step-4-mint-and-register-a-consumer-reference-id)
      - [Step 5 — Mint and register an asset](identifiers/issuance-reference.md#step-5-mint-and-register-an-asset)
      - [Step 6 — Issue a credential that references everything](identifiers/issuance-reference.md#step-6-issue-a-credential-that-references-everything)
      - [Step 7 — Revoke](identifiers/issuance-reference.md#step-7-revoke)
      - [End-to-end test](identifiers/issuance-reference.md#end-to-end-test)
      - [What you have at the end](identifiers/issuance-reference.md#what-you-have-at-the-end)
* **[identifiers-basic-checklist.md](checklists/identifiers-basic-checklist.md)**
  - *Summary*: Self-audit checklist to verify domain ownership, key formats, and DID structures.
  - *Outline / Headings*:
    - [Basic Checklist — Identifiers and Addressing](checklists/identifiers-basic-checklist.md#basic-checklist-identifiers-and-addressing)
        - [1. Decide your organisation's public name on the network](checklists/identifiers-basic-checklist.md#1-decide-your-organisations-public-name-on-the-network)
        - [2. Set up your digital identity](checklists/identifiers-basic-checklist.md#2-set-up-your-digital-identity)
        - [3. Agree on how you will identify consumers and assets](checklists/identifiers-basic-checklist.md#3-agree-on-how-you-will-identify-consumers-and-assets)
        - [4. Decide what stays private and what becomes public](checklists/identifiers-basic-checklist.md#4-decide-what-stays-private-and-what-becomes-public)
        - [5. Nominate your team](checklists/identifiers-basic-checklist.md#5-nominate-your-team)

---

## 🗄️ 2. Registries and Directories (DeDi)

This block describes the directories that store and resolve identifiers to participant records.

### ⚙️ Setup & Configuration
* **[README.md](registries/README.md)**
  - *Summary*: Introduction to the trust registry layer and related building blocks.
  - *Outline / Headings*:
    - [IES Registries and Directories](registries/README.md#ies-registries-and-directories)
      - [Reading order](registries/README.md#reading-order)
      - [Quick orientation by role](registries/README.md#quick-orientation-by-role)
      - [How this section relates to others](registries/README.md#how-this-section-relates-to-others)
* **[dedi-primer.md](registries/dedi-primer.md)**
  - *Summary*: Conceptual primer on Decentralized Directories, namespace control, and trust pillars.
  - *Outline / Headings*:
    - [DeDi Primer](registries/dedi-primer.md#dedi-primer)
      - [What DeDi is](registries/dedi-primer.md#what-dedi-is)
      - [The three-coordinate model](registries/dedi-primer.md#the-three-coordinate-model)
      - [Identifiers and proofs](registries/dedi-primer.md#identifiers-and-proofs)
      - [The three trust pillars](registries/dedi-primer.md#the-three-trust-pillars)
      - [Deployment options](registries/dedi-primer.md#deployment-options)
        - [Option A — DeDi.global hosted, embedded in your site](registries/dedi-primer.md#option-a-dediglobal-hosted-embedded-in-your-site)
        - [Option B — DeDi.global hosted only](registries/dedi-primer.md#option-b-dediglobal-hosted-only)
        - [Option C — Self-hosted DDP node](registries/dedi-primer.md#option-c-self-hosted-ddp-node)
      - [State, versioning, and time-travel](registries/dedi-primer.md#state-versioning-and-time-travel)
      - [API at a glance](registries/dedi-primer.md#api-at-a-glance)
      - [Built-in schema templates](registries/dedi-primer.md#built-in-schema-templates)
      - [Why a DeDi registry is not just a database](registries/dedi-primer.md#why-a-dedi-registry-is-not-just-a-database)
* **[registry-creation.md](registries/registry-creation.md)**
  - *Summary*: Developer walkthrough for creating namespaces, verification, and managing DeDi records via UI/API.
  - *Outline / Headings*:
    - [Registry Creation — Step by Step](registries/registry-creation.md#registry-creation-step-by-step)
      - [Step 0 — Decide what you are about to publish](registries/registry-creation.md#step-0-decide-what-you-are-about-to-publish)
      - [Step 1 — Create a DeDi account](registries/registry-creation.md#step-1-create-a-dedi-account)
      - [Step 2 — Create a namespace](registries/registry-creation.md#step-2-create-a-namespace)
        - [UI](registries/registry-creation.md#ui)
        - [API](registries/registry-creation.md#api)
      - [Step 3 — Verify the namespace against a domain](registries/registry-creation.md#step-3-verify-the-namespace-against-a-domain)
        - [How it works](registries/registry-creation.md#how-it-works)
        - [Why this matters](registries/registry-creation.md#why-this-matters)
      - [Step 4 — Create a registry](registries/registry-creation.md#step-4-create-a-registry)
        - [Built-in tags](registries/registry-creation.md#built-in-tags)
        - [UI](registries/registry-creation.md#ui)
        - [API — using a built-in tag](registries/registry-creation.md#api-using-a-built-in-tag)
        - [API — using a custom schema](registries/registry-creation.md#api-using-a-custom-schema)
      - [Step 5 — Add records](registries/registry-creation.md#step-5-add-records)
        - [Save and publish in one call](registries/registry-creation.md#save-and-publish-in-one-call)
        - [Two-step: draft then batch-publish](registries/registry-creation.md#two-step-draft-then-batch-publish)
        - [Bulk CSV upload](registries/registry-creation.md#bulk-csv-upload)
      - [Step 6 — Look up and verify](registries/registry-creation.md#step-6-look-up-and-verify)
        - [Resolve a single record](registries/registry-creation.md#resolve-a-single-record)
        - [List records in a registry](registries/registry-creation.md#list-records-in-a-registry)
        - [List registries under a namespace](registries/registry-creation.md#list-registries-under-a-namespace)
        - [Historical state — `as_on`](registries/registry-creation.md#historical-state-as-on)
        - [Version pin](registries/registry-creation.md#version-pin)
        - [Export everything as CSV](registries/registry-creation.md#export-everything-as-csv)
      - [Step 7 — Day-2 operations](registries/registry-creation.md#step-7-day-2-operations)
      - [Authorisation model — what to remember](registries/registry-creation.md#authorisation-model-what-to-remember)
      - [Troubleshooting](registries/registry-creation.md#troubleshooting)
* **[required-registries.md](registries/required-registries.md)**
  - *Summary*: Detailed specification of schemas, record shapes, and onboarding channels for public/private registries.
  - *Outline / Headings*:
    - [Required Registries for IES Onboarding](registries/required-registries.md#required-registries-for-ies-onboarding)
      - [Map at a glance](registries/required-registries.md#map-at-a-glance)
      - [Onboarding-quick guide — minimum to get started](registries/required-registries.md#onboarding-quick-guide-minimum-to-get-started)
      - [DISCOM reference registry](registries/required-registries.md#discom-reference-registry)
        - [Record shape](registries/required-registries.md#record-shape)
        - [How to get added](registries/required-registries.md#how-to-get-added)
      - [Regulator reference registry](registries/required-registries.md#regulator-reference-registry)
      - [Schemas registry](registries/required-registries.md#schemas-registry)
      - [Network reference registry](registries/required-registries.md#network-reference-registry)
        - [How to get referenced in](registries/required-registries.md#how-to-get-referenced-in)
      - [Beckn subscriber registry](registries/required-registries.md#beckn-subscriber-registry)
        - [Record shape](registries/required-registries.md#record-shape)
        - [Conventional layout](registries/required-registries.md#conventional-layout)
      - [Public-keys registry](registries/required-registries.md#public-keys-registry)
        - [Record shape](registries/required-registries.md#record-shape)
        - [Key rotation](registries/required-registries.md#key-rotation)
      - [Revocation registry](registries/required-registries.md#revocation-registry)
        - [Record shape](registries/required-registries.md#record-shape)
      - [Asset registry (optional)](registries/required-registries.md#asset-registry-optional)
      - [Dataset registry (optional)](registries/required-registries.md#dataset-registry-optional)
      - [Private registries (PII, billing, internal asset attributes)](registries/required-registries.md#private-registries-pii-billing-internal-asset-attributes)
      - [Governance and key custody](registries/required-registries.md#governance-and-key-custody)
      - [End-to-end onboarding checklist](registries/required-registries.md#end-to-end-onboarding-checklist)

### 🔌 Use & Operations
* **[registries-basic-checklist.md](checklists/registries-basic-checklist.md)**
  - *Summary*: Auditing checklist to confirm namespace delegation, key records, and registry accessibility.
  - *Outline / Headings*:
    - [Basic Checklist — Registries and Directories](checklists/registries-basic-checklist.md#basic-checklist-registries-and-directories)
        - [1. Claim your space in the public directory](checklists/registries-basic-checklist.md#1-claim-your-space-in-the-public-directory)
        - [2. Publish your trust anchor](checklists/registries-basic-checklist.md#2-publish-your-trust-anchor)
        - [3. Decide which registries you need to operate](checklists/registries-basic-checklist.md#3-decide-which-registries-you-need-to-operate)
        - [4. Decide who can write to each registry](checklists/registries-basic-checklist.md#4-decide-who-can-write-to-each-registry)
        - [5. Set up a process to keep registries current](checklists/registries-basic-checklist.md#5-set-up-a-process-to-keep-registries-current)
        - [6. Nominate your team](checklists/registries-basic-checklist.md#6-nominate-your-team)

---

## 🪪 3. Energy Credentials (VCs / OpenCred)

This block handles digital attestations of connections, billing summaries, and consumer identities.

### ⚙️ Setup & Configuration
* **[README.md](energy-credentials/README.md)**
  - *Summary*: Introduction to W3C Verifiable Credentials (VCs) in the energy sector and recommended reading order.
  - *Outline / Headings*:
    - [Energy Credentials for DISCOMs](energy-credentials/README.md#energy-credentials-for-discoms)
        - [Credential lifecycle at a glance](energy-credentials/README.md#credential-lifecycle-at-a-glance)
      - [What an Electricity Credential Is](energy-credentials/README.md#what-an-electricity-credential-is)
      - [What You Can Issue](energy-credentials/README.md#what-you-can-issue)
        - [`CustomerCredential` sub-profiles](energy-credentials/README.md#customercredential-sub-profiles)
      - [The DISCOM Issuance Flow](energy-credentials/README.md#the-discom-issuance-flow)
      - [What You Will Need](energy-credentials/README.md#what-you-will-need)
      - [Recommended Reading Order](energy-credentials/README.md#recommended-reading-order)
      - [How OpenCred Fits In](energy-credentials/README.md#how-opencred-fits-in)
      - [References](energy-credentials/README.md#references)
* **[concepts.md](energy-credentials/concepts.md)**
  - *Summary*: Concepts of credential roles (Issuer, Holder, Verifier), trust delegation, and DeDi revocation patterns.
  - *Outline / Headings*:
    - [Core Concepts](energy-credentials/concepts.md#core-concepts)
      - [Verifiable Credentials (VCs)](energy-credentials/concepts.md#verifiable-credentials-vcs)
      - [Decentralized Identifiers (DIDs)](energy-credentials/concepts.md#decentralized-identifiers-dids)
        - [`did:key` from a self-generated software key — recommended for dev / first deploy](energy-credentials/concepts.md#didkey-from-a-self-generated-software-key-recommended-for-dev-first-deploy)
        - [`did:web` — recommended for production](energy-credentials/concepts.md#didweb-recommended-for-production)
        - [`did:key` from an existing DSC](energy-credentials/concepts.md#didkey-from-an-existing-dsc)
        - [`did:key` and `did:jwk` for consumers](energy-credentials/concepts.md#didkey-and-didjwk-for-consumers)
        - [DeDi as a `did:web` discovery fallback](energy-credentials/concepts.md#dedi-as-a-didweb-discovery-fallback)
        - [`keyStatus` rotation flag and the CORD anchor proof](energy-credentials/concepts.md#keystatus-rotation-flag-and-the-cord-anchor-proof)
      - [Signing Keys and Trust](energy-credentials/concepts.md#signing-keys-and-trust)
      - [Trust and the IES Reference Registry](energy-credentials/concepts.md#trust-and-the-ies-reference-registry)
        - [The registry](energy-credentials/concepts.md#the-registry)
        - [The trust flow](energy-credentials/concepts.md#the-trust-flow)
        - [Why this is better than relying on `did:web` alone](energy-credentials/concepts.md#why-this-is-better-than-relying-on-didweb-alone)
        - [Other DID methods still work for signing](energy-credentials/concepts.md#other-did-methods-still-work-for-signing)
      - [DeDi Revocation](energy-credentials/concepts.md#dedi-revocation)
        - [The model](energy-credentials/concepts.md#the-model)
        - [Lifecycle](energy-credentials/concepts.md#lifecycle)
        - [The `credentialStatus` block](energy-credentials/concepts.md#the-credentialstatus-block)
      - [Proof Formats](energy-credentials/concepts.md#proof-formats)
      - [Packaging Outputs](energy-credentials/concepts.md#packaging-outputs)
      - [Credential Lifecycle](energy-credentials/concepts.md#credential-lifecycle)
      - [Next](energy-credentials/concepts.md#next)
      - [Glossary](energy-credentials/concepts.md#glossary)
      - [References](energy-credentials/concepts.md#references)
* **[schemas.md](energy-credentials/schemas.md)**
  - *Summary*: Detailed breakdown of the electricity credential JSON schema and JSON-LD contexts.
  - *Outline / Headings*:
    - [Electricity Credential Schema](energy-credentials/schemas.md#electricity-credential-schema)
      - [Common Envelope](energy-credentials/schemas.md#common-envelope)
      - [credentialSubject](energy-credentials/schemas.md#credentialsubject)
        - [customerProfile (required)](energy-credentials/schemas.md#customerprofile-required)
          - [meterType enum](energy-credentials/schemas.md#metertype-enum)
        - [customerDetails](energy-credentials/schemas.md#customerdetails)
          - [installationAddress](energy-credentials/schemas.md#installationaddress)
        - [consumptionProfiles[]](energy-credentials/schemas.md#consumptionprofiles)
        - [generationProfiles[]](energy-credentials/schemas.md#generationprofiles)
        - [storageProfiles[]](energy-credentials/schemas.md#storageprofiles)
      - [idRef](energy-credentials/schemas.md#idref)
        - [IES DISCOMs Reference Registry](energy-credentials/schemas.md#ies-discoms-reference-registry)
      - [Full example](energy-credentials/schemas.md#full-example)
      - [Lifecycle Patterns](energy-credentials/schemas.md#lifecycle-patterns)
      - [Implementing in OpenCred](energy-credentials/schemas.md#implementing-in-opencred)
        - [Three gotchas first-time issuers hit](energy-credentials/schemas.md#three-gotchas-first-time-issuers-hit)
      - [References](energy-credentials/schemas.md#references)
* **[onboarding.md](energy-credentials/onboarding.md)**
  - *Summary*: Step-by-step instructions for deploying OpenCred docker instances and setting up signing keys.
  - *Outline / Headings*:
    - [Deployment](energy-credentials/onboarding.md#deployment)
      - [Prerequisites](energy-credentials/onboarding.md#prerequisites)
      - [Step 0 — Register in the IES DISCOMs Reference Registry](energy-credentials/onboarding.md#step-0-register-in-the-ies-discoms-reference-registry)
      - [Step 1 — Pull the OpenCred image](energy-credentials/onboarding.md#step-1-pull-the-opencred-image)
      - [Step 2 — Decide your signing-key model](energy-credentials/onboarding.md#step-2-decide-your-signing-key-model)
        - [Generate a software key](energy-credentials/onboarding.md#generate-a-software-key)
      - [Step 3 — Set up your issuer DID](energy-credentials/onboarding.md#step-3-set-up-your-issuer-did)
        - [Option A — `did:key` from a self-generated software key (recommended for dev / first deploy)](energy-credentials/onboarding.md#option-a-didkey-from-a-self-generated-software-key-recommended-for-dev-first-deploy)
        - [Option B — `did:web` (recommended for production)](energy-credentials/onboarding.md#option-b-didweb-recommended-for-production)
        - [Option C — `did:key` from an existing CCA-issued DSC](energy-credentials/onboarding.md#option-c-didkey-from-an-existing-cca-issued-dsc)
        - [Option D — `did:web` hosted by DeDi (no `.well-known/did.json` needed)](energy-credentials/onboarding.md#option-d-didweb-hosted-by-dedi-no-well-knowndidjson-needed)
      - [Step 4 — Run OpenCred + DeDi together](energy-credentials/onboarding.md#step-4-run-opencred-dedi-together)
        - [Quick start (software key + DeDi)](energy-credentials/onboarding.md#quick-start-software-key-dedi)
        - [Local dev on Windows / macOS (Docker Desktop)](energy-credentials/onboarding.md#local-dev-on-windows-macos-docker-desktop)
        - [Docker Compose (production)](energy-credentials/onboarding.md#docker-compose-production)
        - [Cloud KMS variants](energy-credentials/onboarding.md#cloud-kms-variants)
      - [Step 5 — Environment variables reference](energy-credentials/onboarding.md#step-5-environment-variables-reference)
      - [Step 6 — Confirm DeDi is wired in](energy-credentials/onboarding.md#step-6-confirm-dedi-is-wired-in)
        - [`did:web` discovery via DeDi (optional)](energy-credentials/onboarding.md#didweb-discovery-via-dedi-optional)
      - [Step 7 — Reverse proxy and TLS](energy-credentials/onboarding.md#step-7-reverse-proxy-and-tls)
      - [Step 8 — Kubernetes (optional)](energy-credentials/onboarding.md#step-8-kubernetes-optional)
      - [Multi-replica and batch worker fleet](energy-credentials/onboarding.md#multi-replica-and-batch-worker-fleet)
      - [Production checklist](energy-credentials/onboarding.md#production-checklist)
      - [Verifying the deployment](energy-credentials/onboarding.md#verifying-the-deployment)
      - [Troubleshooting](energy-credentials/onboarding.md#troubleshooting)
      - [References](energy-credentials/onboarding.md#references)

### 🔌 Use & Operations
* **[issuance.md](energy-credentials/issuance.md)**
  - *Summary*: Guide to mapping customer master data to the issue API, batch issuance, and lifecycle patterns.
  - *Outline / Headings*:
    - [Issuing Credentials](energy-credentials/issuance.md#issuing-credentials)
      - [The Core Flow](energy-credentials/issuance.md#the-core-flow)
      - [`POST /v1/credentials/issue`](energy-credentials/issuance.md#post-v1credentialsissue)
        - [Request body](energy-credentials/issuance.md#request-body)
        - [Response](energy-credentials/issuance.md#response)
      - [Worked Example — new connection (identity + consumption)](energy-credentials/issuance.md#worked-example-new-connection-identity-consumption)
      - [Worked Example — rooftop solar commissioning](energy-credentials/issuance.md#worked-example-rooftop-solar-commissioning)
      - [Verify immediately after issue](energy-credentials/issuance.md#verify-immediately-after-issue)
      - [Integrating With Your CIS / NMS](energy-credentials/issuance.md#integrating-with-your-cis-nms)
        - [Reference architecture](energy-credentials/issuance.md#reference-architecture)
        - [Triggers](energy-credentials/issuance.md#triggers)
        - [Reference handler — Python](energy-credentials/issuance.md#reference-handler-python)
        - [Where the consumer's DID comes from](energy-credentials/issuance.md#where-the-consumers-did-comes-from)
      - [Batch Issuance](energy-credentials/issuance.md#batch-issuance)
        - [`POST /v1/credentials/batch`](energy-credentials/issuance.md#post-v1credentialsbatch)
        - [Batch issuance at scale (v1.5.0+)](energy-credentials/issuance.md#batch-issuance-at-scale-v150)
      - [Revoking a Credential](energy-credentials/issuance.md#revoking-a-credential)
        - [Compute the hash first (optional, for audit logs)](energy-credentials/issuance.md#compute-the-hash-first-optional-for-audit-logs)
        - [Publish the revocation](energy-credentials/issuance.md#publish-the-revocation)
        - [Batch revocation hashes](energy-credentials/issuance.md#batch-revocation-hashes)
        - [Hash stability rules](energy-credentials/issuance.md#hash-stability-rules)
      - [Lifecycle Patterns](energy-credentials/issuance.md#lifecycle-patterns)
        - [Re-issuing on data change](energy-credentials/issuance.md#re-issuing-on-data-change)
        - [Connection closures](energy-credentials/issuance.md#connection-closures)
        - [Time-bounded validity](energy-credentials/issuance.md#time-bounded-validity)
      - [Operational Notes](energy-credentials/issuance.md#operational-notes)
        - [Logging and audit](energy-credentials/issuance.md#logging-and-audit)
        - [Rate limits](energy-credentials/issuance.md#rate-limits)
        - [Idempotency](energy-credentials/issuance.md#idempotency)
        - [Selective disclosure](energy-credentials/issuance.md#selective-disclosure)
      - [All Endpoints at a Glance](energy-credentials/issuance.md#all-endpoints-at-a-glance)
      - [References](energy-credentials/issuance.md#references)
* **[verification.md](energy-credentials/verification.md)**
  - *Summary*: Specifications for verifying signatures, schema compliance, and DeDi revocation status list updates.
  - *Outline / Headings*:
    - [Verification](energy-credentials/verification.md#verification)
      - [Four Verification Surfaces](energy-credentials/verification.md#four-verification-surfaces)
      - [What Verification Checks](energy-credentials/verification.md#what-verification-checks)
        - [Silent-skip warning](energy-credentials/verification.md#silent-skip-warning)
        - [keyRotation (advisory)](energy-credentials/verification.md#keyrotation-advisory)
        - [registryAnchor (advisory)](energy-credentials/verification.md#registryanchor-advisory)
      - [Verifying With OpenCred](energy-credentials/verification.md#verifying-with-opencred)
        - [`POST /v1/credentials/verify`](energy-credentials/verification.md#post-v1credentialsverify)
          - [Request shapes per proof format](energy-credentials/verification.md#request-shapes-per-proof-format)
      - [How a Partner Verifies What You Issued](energy-credentials/verification.md#how-a-partner-verifies-what-you-issued)
      - [Checking Revocation Status Separately](energy-credentials/verification.md#checking-revocation-status-separately)
      - [QA Pattern for DISCOM Teams](energy-credentials/verification.md#qa-pattern-for-discom-teams)
        - [Inspecting issuer-DID identities from a key file](energy-credentials/verification.md#inspecting-issuer-did-identities-from-a-key-file)
      - [Common Failure Modes](energy-credentials/verification.md#common-failure-modes)
      - [DigiLocker-Delivered Credentials](energy-credentials/verification.md#digilocker-delivered-credentials)
      - [References](energy-credentials/verification.md#references)
* **[digilocker-integration.md](energy-credentials/digilocker-integration.md)**
  - *Summary*: Integration guide for connecting OpenCred with India's DigiLocker Pull URI protocol.
  - *Outline / Headings*:
    - [DigiLocker Integration — DISCOM Guide](energy-credentials/digilocker-integration.md#digilocker-integration-discom-guide)
      - [What DigiLocker Does](energy-credentials/digilocker-integration.md#what-digilocker-does)
      - [Flow Overview](energy-credentials/digilocker-integration.md#flow-overview)
      - [Phase 0 — One-Time Setup](energy-credentials/digilocker-integration.md#phase-0-one-time-setup)
        - [Step 1 — Register on API Setu](energy-credentials/digilocker-integration.md#step-1-register-on-api-setu)
        - [Step 2 — Stand Up OpenCred and Your Issuer DID](energy-credentials/digilocker-integration.md#step-2-stand-up-opencred-and-your-issuer-did)
        - [Step 3 — Register the Pull URI Endpoint on API Setu](energy-credentials/digilocker-integration.md#step-3-register-the-pull-uri-endpoint-on-api-setu)
      - [Phase 1 — The Pull URI Endpoint](energy-credentials/digilocker-integration.md#phase-1-the-pull-uri-endpoint)
        - [Endpoint Specification](energy-credentials/digilocker-integration.md#endpoint-specification)
        - [Step 1 — Verify the Inbound HMAC](energy-credentials/digilocker-integration.md#step-1-verify-the-inbound-hmac)
        - [Step 2 — Parse the Inbound Request](energy-credentials/digilocker-integration.md#step-2-parse-the-inbound-request)
        - [Step 3 — Look Up Consumer in CIS](energy-credentials/digilocker-integration.md#step-3-look-up-consumer-in-cis)
        - [Step 4 — Call OpenCred to Issue the Credential](energy-credentials/digilocker-integration.md#step-4-call-opencred-to-issue-the-credential)
        - [Step 5 — Package the PDF and VC for the response](energy-credentials/digilocker-integration.md#step-5-package-the-pdf-and-vc-for-the-response)
        - [Step 6 — Return the PullURIResponse](energy-credentials/digilocker-integration.md#step-6-return-the-pulluriresponse)
        - [Handler Logic Summary](energy-credentials/digilocker-integration.md#handler-logic-summary)
      - [Error Response Format](energy-credentials/digilocker-integration.md#error-response-format)
      - [Using a Common Endpoint for ELBIL and NYCER](energy-credentials/digilocker-integration.md#using-a-common-endpoint-for-elbil-and-nycer)
      - [Phase 2 — Consumer Shares Credential with a Verifier](energy-credentials/digilocker-integration.md#phase-2-consumer-shares-credential-with-a-verifier)
      - [Security Checklist](energy-credentials/digilocker-integration.md#security-checklist)
      - [Reference](energy-credentials/digilocker-integration.md#reference)
* **[consumer-energy-passport.md](energy-credentials/consumer-energy-passport.md)**
  - *Summary*: Envelope specification and fields for the Consumer Energy Passport credential.
  - *Outline / Headings*:
    - [Consumer Energy Passport Credential](energy-credentials/consumer-energy-passport.md#consumer-energy-passport-credential)
      - [Relationship to `CustomerCredential`](energy-credentials/consumer-energy-passport.md#relationship-to-customercredential)
      - [Common Envelope](energy-credentials/consumer-energy-passport.md#common-envelope)
      - [credentialSubject](energy-credentials/consumer-energy-passport.md#credentialsubject)
        - [identityBinding (required)](energy-credentials/consumer-energy-passport.md#identitybinding-required)
        - [customerProfile, customerDetails, consumptionProfiles[], generationProfiles[], storageProfiles[]](energy-credentials/consumer-energy-passport.md#customerprofile-customerdetails-consumptionprofiles-generationprofiles-storageprofiles)
      - [Full example](energy-credentials/consumer-energy-passport.md#full-example)
      - [Issuing the Passport](energy-credentials/consumer-energy-passport.md#issuing-the-passport)
      - [Selective Disclosure Presentations](energy-credentials/consumer-energy-passport.md#selective-disclosure-presentations)
      - [References](energy-credentials/consumer-energy-passport.md#references)
* **[consumer-meter-digest.md](energy-credentials/consumer-meter-digest.md)**
  - *Summary*: Envelope specification and readings structure for the Consumer Meter Digest credential.
  - *Outline / Headings*:
    - [Consumer Meter Digest Credential](energy-credentials/consumer-meter-digest.md#consumer-meter-digest-credential)
      - [What's Different From Other Credentials](energy-credentials/consumer-meter-digest.md#whats-different-from-other-credentials)
      - [Common Envelope](energy-credentials/consumer-meter-digest.md#common-envelope)
      - [credentialSubject](energy-credentials/consumer-meter-digest.md#credentialsubject)
        - [meterReference (required)](energy-credentials/consumer-meter-digest.md#meterreference-required)
        - [period (required)](energy-credentials/consumer-meter-digest.md#period-required)
        - [granularity (required)](energy-credentials/consumer-meter-digest.md#granularity-required)
        - [readings](energy-credentials/consumer-meter-digest.md#readings)
        - [summary](energy-credentials/consumer-meter-digest.md#summary)
        - [dataQuality (required)](energy-credentials/consumer-meter-digest.md#dataquality-required)
      - [Full Example — Monthly Summary](energy-credentials/consumer-meter-digest.md#full-example-monthly-summary)
      - [Full Example — Raw Readings (excerpt)](energy-credentials/consumer-meter-digest.md#full-example-raw-readings-excerpt)
      - [Issuing the Digest](energy-credentials/consumer-meter-digest.md#issuing-the-digest)
      - [Verifying the Digest](energy-credentials/consumer-meter-digest.md#verifying-the-digest)
      - [References](energy-credentials/consumer-meter-digest.md#references)
* **[energy-credentials-basic-checklist.md](checklists/energy-credentials-basic-checklist.md)**
  - *Summary*: Basic check list for credential issuance and environment testing.
  - *Outline / Headings*:
    - [Basic Checklist — Energy Credentials](checklists/energy-credentials-basic-checklist.md#basic-checklist-energy-credentials)
        - [1. Set up your DISCOM as a credential issuer](checklists/energy-credentials-basic-checklist.md#1-set-up-your-discom-as-a-credential-issuer)
        - [2. Decide which credentials you will issue in Phase 1](checklists/energy-credentials-basic-checklist.md#2-decide-which-credentials-you-will-issue-in-phase-1)
        - [3. Map your existing data to the standard credential format](checklists/energy-credentials-basic-checklist.md#3-map-your-existing-data-to-the-standard-credential-format)
        - [4. Stand up DeDi for revocation (and optionally for DID-document discovery)](checklists/energy-credentials-basic-checklist.md#4-stand-up-dedi-for-revocation-and-optionally-for-did-document-discovery)
        - [5. Decide how credentials reach the consumer](checklists/energy-credentials-basic-checklist.md#5-decide-how-credentials-reach-the-consumer)
        - [6. Test the full loop, then go live](checklists/energy-credentials-basic-checklist.md#6-test-the-full-loop-then-go-live)
        - [7. Nominate your team](checklists/energy-credentials-basic-checklist.md#7-nominate-your-team)
* **[energy-credentials-checklist.md](checklists/energy-credentials-checklist.md)**
  - *Summary*: Overview readiness checklist for credential deployments.
  - *Outline / Headings*:
    - [India Energy Stack](checklists/energy-credentials-checklist.md#india-energy-stack)
      - [IES Electricity Credentials](checklists/energy-credentials-checklist.md#ies-electricity-credentials)
        - [DISCOM Readiness Checklist](checklists/energy-credentials-checklist.md#discom-readiness-checklist)
        - [1. Infrastructure Setup (OpenCred + DeDi combo)](checklists/energy-credentials-checklist.md#1-infrastructure-setup-opencred-dedi-combo)
        - [2. Credential Schema](checklists/energy-credentials-checklist.md#2-credential-schema)
        - [3. Credential Issuance](checklists/energy-credentials-checklist.md#3-credential-issuance)
        - [4. Credential Verification](checklists/energy-credentials-checklist.md#4-credential-verification)
        - [5. Revocation](checklists/energy-credentials-checklist.md#5-revocation)
        - [6. Consumer Delivery](checklists/energy-credentials-checklist.md#6-consumer-delivery)
        - [7. Go-Live](checklists/energy-credentials-checklist.md#7-go-live)
* **[energy-credentials-checklist-detailed.md](checklists/energy-credentials-checklist-detailed.md)**
  - *Summary*: Production implementation reference for key management, batching, and delivery.
  - *Outline / Headings*:
    - [India Energy Stack](checklists/energy-credentials-checklist-detailed.md#india-energy-stack)
      - [IES Electricity Credentials — Implementation Checklist](checklists/energy-credentials-checklist-detailed.md#ies-electricity-credentials-implementation-checklist)
        - [Detailed Technical Reference for DISCOM Integration Teams](checklists/energy-credentials-checklist-detailed.md#detailed-technical-reference-for-discom-integration-teams)
      - [Phase 0 — Pre-requisites](checklists/energy-credentials-checklist-detailed.md#phase-0-pre-requisites)
      - [Phase 1 — OpenCred Infrastructure](checklists/energy-credentials-checklist-detailed.md#phase-1-opencred-infrastructure)
        - [1.1 Deploy OpenCred Docker Service](checklists/energy-credentials-checklist-detailed.md#11-deploy-opencred-docker-service)
        - [1.2 Signing Key Setup](checklists/energy-credentials-checklist-detailed.md#12-signing-key-setup)
        - [1.3 DeDi Namespace Setup](checklists/energy-credentials-checklist-detailed.md#13-dedi-namespace-setup)
        - [1.4 (Optional) DID-document discovery via DeDi](checklists/energy-credentials-checklist-detailed.md#14-optional-did-document-discovery-via-dedi)
      - [Phase 2 — Credential Schema](checklists/energy-credentials-checklist-detailed.md#phase-2-credential-schema)
        - [2.1 Use the built-in `electricity/v1` schema](checklists/energy-credentials-checklist-detailed.md#21-use-the-built-in-electricityv1-schema)
        - [2.2 Issuer object enrichment](checklists/energy-credentials-checklist-detailed.md#22-issuer-object-enrichment)
        - [2.3 Customer external ID](checklists/energy-credentials-checklist-detailed.md#23-customer-external-id)
        - [2.4 Proof format](checklists/energy-credentials-checklist-detailed.md#24-proof-format)
      - [Phase 3 — Credential Issuance](checklists/energy-credentials-checklist-detailed.md#phase-3-credential-issuance)
        - [3.1 Single Credential Issuance (API)](checklists/energy-credentials-checklist-detailed.md#31-single-credential-issuance-api)
        - [3.2 Single Issuance via CLI](checklists/energy-credentials-checklist-detailed.md#32-single-issuance-via-cli)
        - [3.3 Single Issuance via Desktop Client](checklists/energy-credentials-checklist-detailed.md#33-single-issuance-via-desktop-client)
        - [3.4 Batch Issuance](checklists/energy-credentials-checklist-detailed.md#34-batch-issuance)
        - [3.5 Packaging and Delivery](checklists/energy-credentials-checklist-detailed.md#35-packaging-and-delivery)
      - [Phase 4 — Credential Verification](checklists/energy-credentials-checklist-detailed.md#phase-4-credential-verification)
        - [4.1 API Verification](checklists/energy-credentials-checklist-detailed.md#41-api-verification)
        - [4.2 Desktop Client Verification](checklists/energy-credentials-checklist-detailed.md#42-desktop-client-verification)
        - [4.3 CLI Verification](checklists/energy-credentials-checklist-detailed.md#43-cli-verification)
      - [Phase 5 — Revocation](checklists/energy-credentials-checklist-detailed.md#phase-5-revocation)
        - [5.1 Hash Computation](checklists/energy-credentials-checklist-detailed.md#51-hash-computation)
        - [5.2 Publishing Revocation](checklists/energy-credentials-checklist-detailed.md#52-publishing-revocation)
        - [5.3 Revocation Runbook](checklists/energy-credentials-checklist-detailed.md#53-revocation-runbook)
      - [Phase 6 — Consumer Delivery Channels](checklists/energy-credentials-checklist-detailed.md#phase-6-consumer-delivery-channels)
        - [6.1 Direct VC Delivery](checklists/energy-credentials-checklist-detailed.md#61-direct-vc-delivery)
        - [6.2 DigiLocker Integration](checklists/energy-credentials-checklist-detailed.md#62-digilocker-integration)
      - [Phase 7 — Security Review](checklists/energy-credentials-checklist-detailed.md#phase-7-security-review)
      - [Phase 8 — Observability and Go-Live](checklists/energy-credentials-checklist-detailed.md#phase-8-observability-and-go-live)

---

## 🔌 4. Data Exchange (Beckn)

This block governs data discovery, consent, and the transfer of telemetry and regulatory datasets.

### ⚙️ Setup & Configuration
* **[README.md](data-exchange/README.md)**
  - *Summary*: Introduction to Beckn-based federated energy data exchange and network components.
  - *Outline / Headings*:
    - [IES Data Exchange](data-exchange/README.md#ies-data-exchange)
      - [The Problem It Solves](data-exchange/README.md#the-problem-it-solves)
      - [How It Works](data-exchange/README.md#how-it-works)
        - [Choosing inline vs access-pattern handoff](data-exchange/README.md#choosing-inline-vs-access-pattern-handoff)
      - [What Data Can Be Exchanged](data-exchange/README.md#what-data-can-be-exchanged)
      - [Key Components](data-exchange/README.md#key-components)
      - [Sections in This Chapter](data-exchange/README.md#sections-in-this-chapter)
      - [Mock BPP (cloud sandbox) — planned](data-exchange/README.md#mock-bpp-cloud-sandbox-planned)
      - [Related Repositories](data-exchange/README.md#related-repositories)
* **[concepts.md](data-exchange/concepts.md)**
  - *Summary*: Beckn control plane vs. data plane, subscriber registries, and schema dispatch mechanics.
  - *Outline / Headings*:
    - [Core Concepts — Data Exchange](data-exchange/concepts.md#core-concepts-data-exchange)
      - [The Digital Energy Grid (DEG) Primitives](data-exchange/concepts.md#the-digital-energy-grid-deg-primitives)
      - [Beckn Protocol Lifecycle](data-exchange/concepts.md#beckn-protocol-lifecycle)
        - [Message Structure](data-exchange/concepts.md#message-structure)
        - [Context invariants](data-exchange/concepts.md#context-invariants)
      - [Building Trust](data-exchange/concepts.md#building-trust)
        - [How identity resolution works](data-exchange/concepts.md#how-identity-resolution-works)
        - [Identity fields, in DeDi and in ONIX](data-exchange/concepts.md#identity-fields-in-dedi-and-in-onix)
      - [The DatasetItem Schema](data-exchange/concepts.md#the-datasetitem-schema)
      - [IES Data Schemas](data-exchange/concepts.md#ies-data-schemas)
      - [How schema validation works](data-exchange/concepts.md#how-schema-validation-works)
        - [The dispatch mechanic](data-exchange/concepts.md#the-dispatch-mechanic)
        - [Domain allow-list](data-exchange/concepts.md#domain-allow-list)
        - [Publishing your own schema](data-exchange/concepts.md#publishing-your-own-schema)
      - [ONIX Adapter and Network](data-exchange/concepts.md#onix-adapter-and-network)
* **[architecture.md](data-exchange/architecture.md)**
  - *Summary*: Network topology, gateway configurations, and sandbox vs. production endpoints.
  - *Outline / Headings*:
    - [Architecture — Data Exchange](data-exchange/architecture.md#architecture-data-exchange)
      - [Stack topology](data-exchange/architecture.md#stack-topology)
      - [Generic Beckn flow](data-exchange/architecture.md#generic-beckn-flow)
      - [Endpoints — sandbox vs production](data-exchange/architecture.md#endpoints-sandbox-vs-production)
      - [Further reading](data-exchange/architecture.md#further-reading)
* **[quick-start.md](data-exchange/quick-start.md)**
  - *Summary*: Developer guide to starting local sandboxes and sending confirm -> on_confirm exchanges.
  - *Outline / Headings*:
    - [Quick Start — Data Exchange](data-exchange/quick-start.md#quick-start-data-exchange)
      - [1. Pick your role](data-exchange/quick-start.md#1-pick-your-role)
      - [2. Prerequisites](data-exchange/quick-start.md#2-prerequisites)
      - [3. Clone and start the stack](data-exchange/quick-start.md#3-clone-and-start-the-stack)
      - [4. Run the minimal exchange (`confirm` → `on_confirm`)](data-exchange/quick-start.md#4-run-the-minimal-exchange-confirm-on-confirm)
        - [Import the Postman collection](data-exchange/quick-start.md#import-the-postman-collection)
        - [Set collection variables](data-exchange/quick-start.md#set-collection-variables)
        - [Send `confirm` and verify (BAP path)](data-exchange/quick-start.md#send-confirm-and-verify-bap-path)
        - [BPP path](data-exchange/quick-start.md#bpp-path)
      - [5. (Optional) Add other Beckn actions](data-exchange/quick-start.md#5-optional-add-other-beckn-actions)
      - [6. Test over the public internet (ngrok)](data-exchange/quick-start.md#6-test-over-the-public-internet-ngrok)
        - [One-time setup](data-exchange/quick-start.md#one-time-setup)
        - [Start the tunnel](data-exchange/quick-start.md#start-the-tunnel)
        - [Re-run the flow through the tunnel](data-exchange/quick-start.md#re-run-the-flow-through-the-tunnel)
        - [Transacting with another participant](data-exchange/quick-start.md#transacting-with-another-participant)
      - [7. Wire in your application](data-exchange/quick-start.md#7-wire-in-your-application)
        - [BAP — receive the callback in your own app](data-exchange/quick-start.md#bap-receive-the-callback-in-your-own-app)
        - [BPP — serve real data from your provider](data-exchange/quick-start.md#bpp-serve-real-data-from-your-provider)
      - [8. Stop the stack](data-exchange/quick-start.md#8-stop-the-stack)
      - [9. Going beyond the sandbox](data-exchange/quick-start.md#9-going-beyond-the-sandbox)
        - [Phase 1 — Use the devkit as-is and prove the flows](data-exchange/quick-start.md#phase-1-use-the-devkit-as-is-and-prove-the-flows)
        - [Phase 2 — Swap in your real identity](data-exchange/quick-start.md#phase-2-swap-in-your-real-identity)
      - [Onboarding checklist](data-exchange/quick-start.md#onboarding-checklist)
        - [BAP (Data Consumer)](data-exchange/quick-start.md#bap-data-consumer)
        - [BPP (Data Provider)](data-exchange/quick-start.md#bpp-data-provider)
      - [Reference](data-exchange/quick-start.md#reference)
* **[registry-setup.md](data-exchange/registry-setup.md)**
  - *Summary*: Detailed steps for configuring ONIX with real identities and whitelisting namespaces.
  - *Outline / Headings*:
    - [Registry Setup](data-exchange/registry-setup.md#registry-setup)
      - [The IES networks](data-exchange/registry-setup.md#the-ies-networks)
      - [The model in one paragraph](data-exchange/registry-setup.md#the-model-in-one-paragraph)
      - [Step-by-step for a Network Participant (BAP / BPP)](data-exchange/registry-setup.md#step-by-step-for-a-network-participant-bap-bpp)
        - [1. Create a DeDi Global account and verify your namespace](data-exchange/registry-setup.md#1-create-a-dedi-global-account-and-verify-your-namespace)
        - [2. Create a subscriber registry under your namespace](data-exchange/registry-setup.md#2-create-a-subscriber-registry-under-your-namespace)
        - [3. Publish your subscriber record](data-exchange/registry-setup.md#3-publish-your-subscriber-record)
        - [4. Ask IES to add your DeDi URL to the network reference registry](data-exchange/registry-setup.md#4-ask-ies-to-add-your-dedi-url-to-the-network-reference-registry)
      - [Configure ONIX with your real identity](data-exchange/registry-setup.md#configure-onix-with-your-real-identity)
        - [`allowedNetworkIDs` is the gate](data-exchange/registry-setup.md#allowednetworkids-is-the-gate)
      - [Two registries, two ONIX deployments](data-exchange/registry-setup.md#two-registries-two-onix-deployments)
        - [Running two devkit stacks side-by-side](data-exchange/registry-setup.md#running-two-devkit-stacks-side-by-side)
      - [Hosting checklist](data-exchange/registry-setup.md#hosting-checklist)
      - [Reference](data-exchange/registry-setup.md#reference)

### 🔌 Use & Operations
* **[data-exchange-basic-checklist.md](checklists/data-exchange-basic-checklist.md)**
  - *Summary*: Checklist for local sandbox validation and callback endpoint wiring.
  - *Outline / Headings*:
    - [Basic Checklist — Data Exchange](checklists/data-exchange-basic-checklist.md#basic-checklist-data-exchange)
        - [1. Decide which datasets you will publish (or consume)](checklists/data-exchange-basic-checklist.md#1-decide-which-datasets-you-will-publish-or-consume)
        - [2. Set up your network identity](checklists/data-exchange-basic-checklist.md#2-set-up-your-network-identity)
        - [3. Try it on the test network first](checklists/data-exchange-basic-checklist.md#3-try-it-on-the-test-network-first)
        - [4. Connect your real data systems](checklists/data-exchange-basic-checklist.md#4-connect-your-real-data-systems)
        - [5. Make your data discoverable](checklists/data-exchange-basic-checklist.md#5-make-your-data-discoverable)
        - [6. Production deployment](checklists/data-exchange-basic-checklist.md#6-production-deployment)
        - [7. Go-live verification](checklists/data-exchange-basic-checklist.md#7-go-live-verification)
        - [8. Nominate your team](checklists/data-exchange-basic-checklist.md#8-nominate-your-team)
* **[data-exchange-checklist.md](checklists/data-exchange-checklist.md)**
  - *Summary*: Intermediate checklist for organization readiness and proxy audits.
  - *Outline / Headings*:
    - [India Energy Stack](checklists/data-exchange-checklist.md#india-energy-stack)
      - [IES Energy Data Exchange](checklists/data-exchange-checklist.md#ies-energy-data-exchange)
        - [DISCOM / Organisation Readiness Checklist](checklists/data-exchange-checklist.md#discom-organisation-readiness-checklist)
        - [Stage 1 — Testnet Validation](checklists/data-exchange-checklist.md#stage-1-testnet-validation)
        - [Stage 2 — DeDi Setup](checklists/data-exchange-checklist.md#stage-2-dedi-setup)
        - [Stage 3 — Production Network Registration](checklists/data-exchange-checklist.md#stage-3-production-network-registration)
        - [Stage 4 — Real Data Integration](checklists/data-exchange-checklist.md#stage-4-real-data-integration)
        - [Stage 5 — Production Infrastructure](checklists/data-exchange-checklist.md#stage-5-production-infrastructure)
        - [Stage 6 — Go-Live Verification](checklists/data-exchange-checklist.md#stage-6-go-live-verification)
* **[data-exchange-checklist-detailed.md](checklists/data-exchange-checklist-detailed.md)**
  - *Summary*: Production verification roadmap covering TLS, keys, databases, and monitoring.
  - *Outline / Headings*:
    - [India Energy Stack](checklists/data-exchange-checklist-detailed.md#india-energy-stack)
      - [IES Energy Data Exchange — Implementation Checklist](checklists/data-exchange-checklist-detailed.md#ies-energy-data-exchange-implementation-checklist)
        - [Detailed Technical Reference: Testnet to Production](checklists/data-exchange-checklist-detailed.md#detailed-technical-reference-testnet-to-production)
      - [Stage 1 — Testnet Validation](checklists/data-exchange-checklist-detailed.md#stage-1-testnet-validation)
        - [Pre-requisites](checklists/data-exchange-checklist-detailed.md#pre-requisites)
        - [Stack Setup](checklists/data-exchange-checklist-detailed.md#stack-setup)
        - [Use Case Testing](checklists/data-exchange-checklist-detailed.md#use-case-testing)
        - [Testnet Sign-off](checklists/data-exchange-checklist-detailed.md#testnet-sign-off)
      - [Stage 2 — DeDi Setup](checklists/data-exchange-checklist-detailed.md#stage-2-dedi-setup)
        - [2.1 Register a DeDi Namespace](checklists/data-exchange-checklist-detailed.md#21-register-a-dedi-namespace)
        - [2.2 Configure Dataset Hash Anchoring (BPP)](checklists/data-exchange-checklist-detailed.md#22-configure-dataset-hash-anchoring-bpp)
        - [2.3 Configure DeDi Verification (BAP)](checklists/data-exchange-checklist-detailed.md#23-configure-dedi-verification-bap)
      - [Stage 3 — Production Network Registration](checklists/data-exchange-checklist-detailed.md#stage-3-production-network-registration)
        - [3.1 Domain and TLS Setup](checklists/data-exchange-checklist-detailed.md#31-domain-and-tls-setup)
        - [3.2 Generate Production Signing Keys](checklists/data-exchange-checklist-detailed.md#32-generate-production-signing-keys)
        - [3.3 Submit Registration to IES Team](checklists/data-exchange-checklist-detailed.md#33-submit-registration-to-ies-team)
      - [Stage 4 — Real Data Integration](checklists/data-exchange-checklist-detailed.md#stage-4-real-data-integration)
        - [4.1 Production BPP Server (BPP role only)](checklists/data-exchange-checklist-detailed.md#41-production-bpp-server-bpp-role-only)
        - [4.2 Connect to Real Data Sources](checklists/data-exchange-checklist-detailed.md#42-connect-to-real-data-sources)
        - [4.3 Dataset Catalog Publication](checklists/data-exchange-checklist-detailed.md#43-dataset-catalog-publication)
        - [4.4 Production BAP Application (BAP role only)](checklists/data-exchange-checklist-detailed.md#44-production-bap-application-bap-role-only)
      - [Stage 5 — Production Infrastructure](checklists/data-exchange-checklist-detailed.md#stage-5-production-infrastructure)
        - [5.1 ONIX Adapter Deployment](checklists/data-exchange-checklist-detailed.md#51-onix-adapter-deployment)
        - [5.2 Security](checklists/data-exchange-checklist-detailed.md#52-security)
        - [5.3 Monitoring and Observability](checklists/data-exchange-checklist-detailed.md#53-monitoring-and-observability)
      - [Stage 6 — Go-Live Verification](checklists/data-exchange-checklist-detailed.md#stage-6-go-live-verification)
        - [6.1 Production Integration Test](checklists/data-exchange-checklist-detailed.md#61-production-integration-test)
        - [6.2 Data Integrity Verification](checklists/data-exchange-checklist-detailed.md#62-data-integrity-verification)
        - [6.3 Operations Readiness](checklists/data-exchange-checklist-detailed.md#63-operations-readiness)
      - [Troubleshooting Reference](checklists/data-exchange-checklist-detailed.md#troubleshooting-reference)

---

## 🗃️ 5. Schemas

Detailed documentation for the JSON and JSON-LD schema formats used in the accelerator.

* **[README.md](schemas/README.md)**
  - *Summary*: Catalog of schemas, their purpose, versioning guidelines, and file structure.
  - *Outline / Headings*:
    - [IES Accelerator — Schemas](schemas/README.md#ies-accelerator-schemas)
      - [Why this directory exists](schemas/README.md#why-this-directory-exists)
      - [Provenance and updates](schemas/README.md#provenance-and-updates)
      - [Contents](schemas/README.md#contents)
* **[README.md](schemas/ElectricityCredential/README.md)**
  - *Summary*: Metadata, context inheritance, and fields for the ElectricityCredential VC schema.
  - *Outline / Headings*:
    - [ElectricityCredential](schemas/ElectricityCredential/README.md#electricitycredential)
      - [Versions](schemas/ElectricityCredential/README.md#versions)
      - [Inheritance](schemas/ElectricityCredential/README.md#inheritance)
      - [credentialSubject Properties](schemas/ElectricityCredential/README.md#credentialsubject-properties)
      - [Linked Data](schemas/ElectricityCredential/README.md#linked-data)
      - [Usage](schemas/ElectricityCredential/README.md#usage)
* **[README.md](schemas/ElectricityCredential/v1.0/README.md)**
  - *Summary*: Technical specification and fields for Customer Credential v1.0.
  - *Outline / Headings*:
    - [Customer Credential](schemas/ElectricityCredential/v1.0/README.md#customer-credential)
      - [Overview](schemas/ElectricityCredential/v1.0/README.md#overview)
      - [Credential Structure](schemas/ElectricityCredential/v1.0/README.md#credential-structure)
      - [Issuer](schemas/ElectricityCredential/v1.0/README.md#issuer)
      - [Validity Period](schemas/ElectricityCredential/v1.0/README.md#validity-period)
      - [Revocation](schemas/ElectricityCredential/v1.0/README.md#revocation)
      - [Profile Sections](schemas/ElectricityCredential/v1.0/README.md#profile-sections)
        - [customerProfile](schemas/ElectricityCredential/v1.0/README.md#customerprofile)
          - [meterType enum](schemas/ElectricityCredential/v1.0/README.md#metertype-enum)
        - [customerDetails](schemas/ElectricityCredential/v1.0/README.md#customerdetails)
          - [installationAddress](schemas/ElectricityCredential/v1.0/README.md#installationaddress)
        - [consumptionProfile](schemas/ElectricityCredential/v1.0/README.md#consumptionprofile)
        - [generationProfile](schemas/ElectricityCredential/v1.0/README.md#generationprofile)
        - [storageProfile](schemas/ElectricityCredential/v1.0/README.md#storageprofile)
      - [idRef](schemas/ElectricityCredential/v1.0/README.md#idref)
      - [Files](schemas/ElectricityCredential/v1.0/README.md#files)
* **[README.md](schemas/MeterData/v0.5/README.md)**
  - *Summary*: Overview and field representations for MeterData v0.5 profiles.
  - *Outline / Headings*:
    - [Meter Data Compact Profiles (v0.5)](schemas/MeterData/v0.5/README.md#meter-data-compact-profiles-v05)
      - [Overview](schemas/MeterData/v0.5/README.md#overview)
      - [Directory Structure and Files](schemas/MeterData/v0.5/README.md#directory-structure-and-files)
      - [Schema Generation and Compilation](schemas/MeterData/v0.5/README.md#schema-generation-and-compilation)
        - [To Compile Schemas](schemas/MeterData/v0.5/README.md#to-compile-schemas)
      - [Telemetry Verification & Validation](schemas/MeterData/v0.5/README.md#telemetry-verification-validation)
        - [To Validate Example Payloads](schemas/MeterData/v0.5/README.md#to-validate-example-payloads)
      - [JSON-LD Integration](schemas/MeterData/v0.5/README.md#json-ld-integration)
      - [OBIS Mapping and Identifiers](schemas/MeterData/v0.5/README.md#obis-mapping-and-identifiers)
        - [Interpreting OBISMapping.json](schemas/MeterData/v0.5/README.md#interpreting-obismappingjson)
        - [Identifier Flexibility (OBIS vs. Short Names)](schemas/MeterData/v0.5/README.md#identifier-flexibility-obis-vs-short-names)
      - [Payload Shapes and Value Representation](schemas/MeterData/v0.5/README.md#payload-shapes-and-value-representation)
        - [1. Elaborated Representation](schemas/MeterData/v0.5/README.md#1-elaborated-representation)
        - [2. Compact `IntervalRow` Representation](schemas/MeterData/v0.5/README.md#2-compact-intervalrow-representation)
      - [Data Annotations](schemas/MeterData/v0.5/README.md#data-annotations)
        - [Quality Overrides](schemas/MeterData/v0.5/README.md#quality-overrides)
        - [Maximum Demand Timestamps](schemas/MeterData/v0.5/README.md#maximum-demand-timestamps)
* **[CHANGELOG.md](schemas/MeterData/v0.6/CHANGELOG.md)**
  - *Summary*: Changelog detailing Form A and Form B dual-representation upgrades in MeterData v0.6.
  - *Outline / Headings*:
    - [MeterData v0.6 Changelog](schemas/MeterData/v0.6/CHANGELOG.md#meterdata-v06-changelog)
      - [Schema Structural Changes](schemas/MeterData/v0.6/CHANGELOG.md#schema-structural-changes)
        - [1. Unified Time Representation](schemas/MeterData/v0.6/CHANGELOG.md#1-unified-time-representation)
        - [2. Removal of Explicit Units & Phases from Readings](schemas/MeterData/v0.6/CHANGELOG.md#2-removal-of-explicit-units-phases-from-readings)
        - [3. Unified `Reading` Model & Restructured Register Fields](schemas/MeterData/v0.6/CHANGELOG.md#3-unified-reading-model-restructured-register-fields)
        - [4. Compact Form Refinements (`IntervalBlock`)](schemas/MeterData/v0.6/CHANGELOG.md#4-compact-form-refinements-intervalblock)
        - [5. Universal Dual-Form Support across Profiles](schemas/MeterData/v0.6/CHANGELOG.md#5-universal-dual-form-support-across-profiles)
      - [Detailed Payload Examples](schemas/MeterData/v0.6/CHANGELOG.md#detailed-payload-examples)
        - [Form A: Elaborated Representation (`readings` / `touBuckets`)](schemas/MeterData/v0.6/CHANGELOG.md#form-a-elaborated-representation-readings-toubuckets)
        - [Form B: Compact Representation (`intervalBlocks` -> `intervals` + `overrides`)](schemas/MeterData/v0.6/CHANGELOG.md#form-b-compact-representation-intervalblocks---intervals-overrides)
* **[README.md](schemas/MeterData/v0.6/README.md)**
  - *Summary*: Detailed technical specification for the updated MeterData v0.6 dual-representation schemas.
  - *Outline / Headings*:
    - [Meter Data Compact Profiles (v0.6)](schemas/MeterData/v0.6/README.md#meter-data-compact-profiles-v06)
      - [Overview](schemas/MeterData/v0.6/README.md#overview)
      - [Directory Structure and Files](schemas/MeterData/v0.6/README.md#directory-structure-and-files)
      - [Schema Generation and Compilation](schemas/MeterData/v0.6/README.md#schema-generation-and-compilation)
        - [To Compile Schemas](schemas/MeterData/v0.6/README.md#to-compile-schemas)
      - [Telemetry Verification & Validation](schemas/MeterData/v0.6/README.md#telemetry-verification-validation)
        - [To Validate Example Payloads](schemas/MeterData/v0.6/README.md#to-validate-example-payloads)
      - [JSON-LD Integration](schemas/MeterData/v0.6/README.md#json-ld-integration)
      - [OBIS Mapping and Identifiers](schemas/MeterData/v0.6/README.md#obis-mapping-and-identifiers)
        - [Interpreting OBISMapping.json](schemas/MeterData/v0.6/README.md#interpreting-obismappingjson)
        - [Identifier Flexibility (OBIS vs. Short Names)](schemas/MeterData/v0.6/README.md#identifier-flexibility-obis-vs-short-names)
      - [Payload Shapes and Value Representation](schemas/MeterData/v0.6/README.md#payload-shapes-and-value-representation)
        - [1. Form A: Elaborated Representation (`readings` / `touBuckets`)](schemas/MeterData/v0.6/README.md#1-form-a-elaborated-representation-readings-toubuckets)
        - [2. Form B: Compact Matrix Representation (`intervalBlocks`)](schemas/MeterData/v0.6/README.md#2-form-b-compact-matrix-representation-intervalblocks)
      - [Data Annotations](schemas/MeterData/v0.6/README.md#data-annotations)
        - [Sparse Cell Overrides](schemas/MeterData/v0.6/README.md#sparse-cell-overrides)
        - [Maximum Demand snapshoting](schemas/MeterData/v0.6/README.md#maximum-demand-snapshoting)
* **[README.md](schemas/MeterDataRequest/v0.5/README.md)**
  - *Summary*: Field definitions and compilation guidelines for MeterDataRequest v0.5.
  - *Outline / Headings*:
    - [MeterDataRequest Schema (v0.5)](schemas/MeterDataRequest/v0.5/README.md#meterdatarequest-schema-v05)
      - [Schema Overview](schemas/MeterDataRequest/v0.5/README.md#schema-overview)
        - [Fields and Definitions](schemas/MeterDataRequest/v0.5/README.md#fields-and-definitions)
      - [Build and Compilation](schemas/MeterDataRequest/v0.5/README.md#build-and-compilation)
      - [Verification and Validation](schemas/MeterDataRequest/v0.5/README.md#verification-and-validation)
* **[README.md](schemas/ArrFiling/v0.5/README.md)**
  - *Summary*: Detailed schema fields and validation steps for Annual Revenue Requirement filings v0.5.
  - *Outline / Headings*:
    - [Aggregate Revenue Requirement (ARR) Filing Schema (v0.5)](schemas/ArrFiling/v0.5/README.md#aggregate-revenue-requirement-arr-filing-schema-v05)
      - [Overview](schemas/ArrFiling/v0.5/README.md#overview)
      - [Directory Structure and Files](schemas/ArrFiling/v0.5/README.md#directory-structure-and-files)
      - [Schema Generation and Compilation](schemas/ArrFiling/v0.5/README.md#schema-generation-and-compilation)
        - [To Compile Schemas](schemas/ArrFiling/v0.5/README.md#to-compile-schemas)
      - [Payload Verification & Validation](schemas/ArrFiling/v0.5/README.md#payload-verification-validation)
        - [To Validate Example Payloads](schemas/ArrFiling/v0.5/README.md#to-validate-example-payloads)
      - [JSON-LD Integration](schemas/ArrFiling/v0.5/README.md#json-ld-integration)

---

## 🎯 6. Use Cases

Practical deployment and mapping implementations for specific grid business processes.

* **[README.md](use-cases/README.md)**
  - *Summary*: Snapshot index of the five primary energy network use cases.
  - *Outline / Headings*:
    - [Use Cases](use-cases/README.md#use-cases)
      - [The Five Use Cases](use-cases/README.md#the-five-use-cases)
      - [How to Read These Guides](use-cases/README.md#how-to-read-these-guides)
      - [Maturity Snapshot (as of 2026-05)](use-cases/README.md#maturity-snapshot-as-of-2026-05)
* **[README.md](use-cases/smart-meter-data-exchange/README.md)**
  - *Summary*: Sharing telemetry datasets using Beckn and OpenADR 3 standards.
  - *Outline / Headings*:
    - [Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md#smart-meter-data-exchange)
      - [Scenario](use-cases/smart-meter-data-exchange/README.md#scenario)
      - [Actors and Roles](use-cases/smart-meter-data-exchange/README.md#actors-and-roles)
      - [Building Blocks Used](use-cases/smart-meter-data-exchange/README.md#building-blocks-used)
      - [The Dataset — `IES_Report`](use-cases/smart-meter-data-exchange/README.md#the-dataset-ies-report)
      - [Setup Steps](use-cases/smart-meter-data-exchange/README.md#setup-steps)
        - [1. Register the participants](use-cases/smart-meter-data-exchange/README.md#1-register-the-participants)
        - [2. Issue meter and asset identifiers](use-cases/smart-meter-data-exchange/README.md#2-issue-meter-and-asset-identifiers)
        - [3. Stand up the data-exchange adapters](use-cases/smart-meter-data-exchange/README.md#3-stand-up-the-data-exchange-adapters)
        - [4. Configure the dataset catalogue](use-cases/smart-meter-data-exchange/README.md#4-configure-the-dataset-catalogue)
        - [5. Exercise the flow](use-cases/smart-meter-data-exchange/README.md#5-exercise-the-flow)
        - [6. (Optional) Enable consented third-party access](use-cases/smart-meter-data-exchange/README.md#6-optional-enable-consented-third-party-access)
      - [Operate](use-cases/smart-meter-data-exchange/README.md#operate)
      - [Open Items](use-cases/smart-meter-data-exchange/README.md#open-items)
      - [References](use-cases/smart-meter-data-exchange/README.md#references)
* **[ies-data-model.md](use-cases/smart-meter-data-exchange/ies-data-model.md)**
  - *Summary*: Technical mapping of DLMS-COSEM OBIS codes and CIM properties to OpenADR 3.0.
  - *Outline / Headings*:
    - [IES Data Model](use-cases/smart-meter-data-exchange/ies-data-model.md#ies-data-model)
      - [1. RESOURCE Attributes](use-cases/smart-meter-data-exchange/ies-data-model.md#1-resource-attributes)
      - [2. REPORT payloadDescriptors (Telemetry & Logs)](use-cases/smart-meter-data-exchange/ies-data-model.md#2-report-payloaddescriptors-telemetry-logs)
      - [3. EVENT payloadDescriptors (Control Signals)](use-cases/smart-meter-data-exchange/ies-data-model.md#3-event-payloaddescriptors-control-signals)
      - [4. OpenADR 3 JSON Examples](use-cases/smart-meter-data-exchange/ies-data-model.md#4-openadr-3-json-examples)
        - [4.1. RESOURCE Example](use-cases/smart-meter-data-exchange/ies-data-model.md#41-resource-example)
        - [4.2. EVENT Example (Control Signal)](use-cases/smart-meter-data-exchange/ies-data-model.md#42-event-example-control-signal)
        - [4.3. REPORT Examples](use-cases/smart-meter-data-exchange/ies-data-model.md#43-report-examples)
          - [Live Instantaneous Report](use-cases/smart-meter-data-exchange/ies-data-model.md#live-instantaneous-report)
          - [Historic Data (Compactness)](use-cases/smart-meter-data-exchange/ies-data-model.md#historic-data-compactness)
            - [Load Survey (15m Intervals - Ultra Compact)](use-cases/smart-meter-data-exchange/ies-data-model.md#load-survey-15m-intervals---ultra-compact)
            - [Daily Survey (24h Interval)](use-cases/smart-meter-data-exchange/ies-data-model.md#daily-survey-24h-interval)
            - [Monthly Bill (1mo Interval with Multiple Payloads)](use-cases/smart-meter-data-exchange/ies-data-model.md#monthly-bill-1mo-interval-with-multiple-payloads)
      - [5. Complete Mapping: OBIS Codes & Event IDs to OpenADR 3](use-cases/smart-meter-data-exchange/ies-data-model.md#5-complete-mapping-obis-codes-event-ids-to-openadr-3)
* **[survey-of-existing-terminology.md](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md)**
  - *Summary*: Comprehensive reference table of Indian smart metering OBIS codes and event log profiles.
  - *Outline / Headings*:
    - [Comprehensive OBIS Codes & Event IDs for India](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#comprehensive-obis-codes-event-ids-for-india)
      - [Comprehensive OBIS Codes & Event IDs for India (IS 15959 Adaptation)](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#comprehensive-obis-codes-event-ids-for-india-is-15959-adaptation)
        - [1. Core OBIS Codes (Registers & Profiles)](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#1-core-obis-codes-registers-profiles)
          - [1.1 General and Instantaneous Parameters](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#11-general-and-instantaneous-parameters)
          - [1.2 Energy & Demand: Distinction by Profile](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#12-energy-demand-distinction-by-profile)
          - [1.3 Time-of-Use (ToU) Registers](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#13-time-of-use-tou-registers)
        - [2. Profile Buffers & Capture Logic](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#2-profile-buffers-capture-logic)
        - [3. Event Log Profiles & Event IDs](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#3-event-log-profiles-event-ids)
          - [3.1 Event Profile Identifiers (OBIS)](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#31-event-profile-identifiers-obis)
          - [3.2 Standardized Event IDs (India Specific)](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#32-standardized-event-ids-india-specific)
          - [3.3 Prepaid & Control Specific Event IDs](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#33-prepaid-control-specific-event-ids)
        - [4. Communication and Reporting Flow](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#4-communication-and-reporting-flow)
          - [4.1 HES-to-Meter Access Sequence (Polling)](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#41-hes-to-meter-access-sequence-polling)
          - [4.2 Reporting Events (Meter → HES → MDM)](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#42-reporting-events-meter-hes-mdm)
          - [4.3 Control Logic (MDM → HES → Meter)](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#43-control-logic-mdm-hes-meter)
        - [5. Network Topology & Connection Hierarchy](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#5-network-topology-connection-hierarchy)
          - [5.1 Typical Topology](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#51-typical-topology)
          - [5.2 Connectivity Mapping](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#52-connectivity-mapping)
        - [6. Master Data Standards](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#6-master-data-standards)
          - [6.1 Standards for Master Data](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#61-standards-for-master-data)
          - [6.2 Mandatory Master Data Fields (MDM/CIS)](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#62-mandatory-master-data-fields-mdmcis)
          - [6.3 Linking Data to Connection](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#63-linking-data-to-connection)
        - [7. IS 15959 Annexures Summary](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md#7-is-15959-annexures-summary)
* **[basic-checklist.md](use-cases/smart-meter-data-exchange/basic-checklist.md)**
  - *Summary*: Quickcheck list for deploying smart meter exchange adapters and MDM connections.
  - *Outline / Headings*:
    - [Basic Checklist — Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/basic-checklist.md#basic-checklist-smart-meter-data-exchange)
        - [1. Decide the scope of the meter data flow](use-cases/smart-meter-data-exchange/basic-checklist.md#1-decide-the-scope-of-the-meter-data-flow)
        - [2. Register your organisation on the IES network](use-cases/smart-meter-data-exchange/basic-checklist.md#2-register-your-organisation-on-the-ies-network)
        - [3. Issue identifiers for every meter and asset](use-cases/smart-meter-data-exchange/basic-checklist.md#3-issue-identifiers-for-every-meter-and-asset)
        - [4. Stand up the data-exchange adapter](use-cases/smart-meter-data-exchange/basic-checklist.md#4-stand-up-the-data-exchange-adapter)
        - [5. Connect the real metering system](use-cases/smart-meter-data-exchange/basic-checklist.md#5-connect-the-real-metering-system)
        - [6. Publish your dataset catalogue](use-cases/smart-meter-data-exchange/basic-checklist.md#6-publish-your-dataset-catalogue)
        - [7. (Optional) Enable consented third-party access](use-cases/smart-meter-data-exchange/basic-checklist.md#7-optional-enable-consented-third-party-access)
        - [8. Production deployment and go-live](use-cases/smart-meter-data-exchange/basic-checklist.md#8-production-deployment-and-go-live)
        - [9. Nominate your team](use-cases/smart-meter-data-exchange/basic-checklist.md#9-nominate-your-team)
* **[README.md](use-cases/consumer-meter-digest/README.md)**
  - *Summary*: Exchanging monthly meter digests via user consent and pull credentials.
  - *Outline / Headings*:
    - [Consumer Meter Digest](use-cases/consumer-meter-digest/README.md#consumer-meter-digest)
      - [Scenario](use-cases/consumer-meter-digest/README.md#scenario)
      - [Actors and Roles](use-cases/consumer-meter-digest/README.md#actors-and-roles)
      - [Building Blocks Used](use-cases/consumer-meter-digest/README.md#building-blocks-used)
      - [What's in the Digest](use-cases/consumer-meter-digest/README.md#whats-in-the-digest)
      - [Setup Steps](use-cases/consumer-meter-digest/README.md#setup-steps)
        - [1. DISCOM-side prerequisites](use-cases/consumer-meter-digest/README.md#1-discom-side-prerequisites)
        - [2. Wallet-side prerequisites](use-cases/consumer-meter-digest/README.md#2-wallet-side-prerequisites)
        - [3. Catalogue the consumer-pull endpoint](use-cases/consumer-meter-digest/README.md#3-catalogue-the-consumer-pull-endpoint)
        - [4. The consumer makes a request](use-cases/consumer-meter-digest/README.md#4-the-consumer-makes-a-request)
        - [5. The DISCOM responds](use-cases/consumer-meter-digest/README.md#5-the-discom-responds)
        - [6. The consumer presents the Digest](use-cases/consumer-meter-digest/README.md#6-the-consumer-presents-the-digest)
      - [Why a Credential, Not Just an API Pull](use-cases/consumer-meter-digest/README.md#why-a-credential-not-just-an-api-pull)
      - [Open Items](use-cases/consumer-meter-digest/README.md#open-items)
      - [References](use-cases/consumer-meter-digest/README.md#references)
* **[basic-checklist.md](use-cases/consumer-meter-digest/basic-checklist.md)**
  - *Summary*: Checklist for configuring consent endpoints and digest minting.
  - *Outline / Headings*:
    - [Basic Checklist — Consumer Meter Digest](use-cases/consumer-meter-digest/basic-checklist.md#basic-checklist-consumer-meter-digest)
        - [1. Confirm the foundational pieces are in place](use-cases/consumer-meter-digest/basic-checklist.md#1-confirm-the-foundational-pieces-are-in-place)
        - [2. Decide what consumers can request](use-cases/consumer-meter-digest/basic-checklist.md#2-decide-what-consumers-can-request)
        - [3. Define how the consumer authorises the request](use-cases/consumer-meter-digest/basic-checklist.md#3-define-how-the-consumer-authorises-the-request)
        - [4. Publish the consumer-pull catalogue entry](use-cases/consumer-meter-digest/basic-checklist.md#4-publish-the-consumer-pull-catalogue-entry)
        - [5. Wire up Digest minting](use-cases/consumer-meter-digest/basic-checklist.md#5-wire-up-digest-minting)
        - [6. Test the end-to-end flow](use-cases/consumer-meter-digest/basic-checklist.md#6-test-the-end-to-end-flow)
        - [7. Production deployment](use-cases/consumer-meter-digest/basic-checklist.md#7-production-deployment)
        - [8. Consumer communication and rollout](use-cases/consumer-meter-digest/basic-checklist.md#8-consumer-communication-and-rollout)
        - [9. Nominate your team](use-cases/consumer-meter-digest/basic-checklist.md#9-nominate-your-team)
* **[README.md](use-cases/consumer-energy-passport/README.md)**
  - *Summary*: Consolidating generation, storage, and consumption VCs into a unified consumer passport.
  - *Outline / Headings*:
    - [Consumer Energy Passport](use-cases/consumer-energy-passport/README.md#consumer-energy-passport)
      - [Scenario](use-cases/consumer-energy-passport/README.md#scenario)
      - [Actors and Roles](use-cases/consumer-energy-passport/README.md#actors-and-roles)
      - [Building Blocks Used](use-cases/consumer-energy-passport/README.md#building-blocks-used)
      - [What's in the Passport](use-cases/consumer-energy-passport/README.md#whats-in-the-passport)
      - [Setup Steps](use-cases/consumer-energy-passport/README.md#setup-steps)
        - [1. Be a registered DISCOM issuer](use-cases/consumer-energy-passport/README.md#1-be-a-registered-discom-issuer)
        - [2. Run OpenCred](use-cases/consumer-energy-passport/README.md#2-run-opencred)
        - [3. Map your CIS + DER systems to the Passport sub-profiles](use-cases/consumer-energy-passport/README.md#3-map-your-cis-der-systems-to-the-passport-sub-profiles)
        - [4. Issue the Passport](use-cases/consumer-energy-passport/README.md#4-issue-the-passport)
        - [5. Deliver to the wallet](use-cases/consumer-energy-passport/README.md#5-deliver-to-the-wallet)
        - [6. Re-issue on material change](use-cases/consumer-energy-passport/README.md#6-re-issue-on-material-change)
      - [How a Verifier Uses It](use-cases/consumer-energy-passport/README.md#how-a-verifier-uses-it)
      - [Selective Disclosure](use-cases/consumer-energy-passport/README.md#selective-disclosure)
      - [Open Items](use-cases/consumer-energy-passport/README.md#open-items)
      - [References](use-cases/consumer-energy-passport/README.md#references)
* **[basic-checklist.md](use-cases/consumer-energy-passport/basic-checklist.md)**
  - *Summary*: Checklist for passport profiling, triggers, and wallet distribution.
  - *Outline / Headings*:
    - [Basic Checklist — Consumer Energy Passport](use-cases/consumer-energy-passport/basic-checklist.md#basic-checklist-consumer-energy-passport)
        - [1. Confirm the foundational pieces are in place](use-cases/consumer-energy-passport/basic-checklist.md#1-confirm-the-foundational-pieces-are-in-place)
        - [2. Decide how you will bind consumer identity](use-cases/consumer-energy-passport/basic-checklist.md#2-decide-how-you-will-bind-consumer-identity)
        - [3. Map your existing data into the Passport](use-cases/consumer-energy-passport/basic-checklist.md#3-map-your-existing-data-into-the-passport)
        - [4. Decide which consumers get a Passport in Phase 1](use-cases/consumer-energy-passport/basic-checklist.md#4-decide-which-consumers-get-a-passport-in-phase-1)
        - [5. Set up the lifecycle triggers](use-cases/consumer-energy-passport/basic-checklist.md#5-set-up-the-lifecycle-triggers)
        - [6. Decide delivery to the consumer's wallet](use-cases/consumer-energy-passport/basic-checklist.md#6-decide-delivery-to-the-consumers-wallet)
        - [7. Test the full loop, then go live](use-cases/consumer-energy-passport/basic-checklist.md#7-test-the-full-loop-then-go-live)
        - [8. Production deployment and rollout](use-cases/consumer-energy-passport/basic-checklist.md#8-production-deployment-and-rollout)
        - [9. Nominate your team](use-cases/consumer-energy-passport/basic-checklist.md#9-nominate-your-team)
* **[README.md](use-cases/discom-regulatory-filing/README.md)**
  - *Summary*: Publishing ARR datasets to State Electricity Regulatory Commissions.
  - *Outline / Headings*:
    - [DISCOM Regulatory Filing](use-cases/discom-regulatory-filing/README.md#discom-regulatory-filing)
      - [Scenario](use-cases/discom-regulatory-filing/README.md#scenario)
      - [Actors and Roles](use-cases/discom-regulatory-filing/README.md#actors-and-roles)
      - [Building Blocks Used](use-cases/discom-regulatory-filing/README.md#building-blocks-used)
      - [The Dataset — `IES_ARR_Filing`](use-cases/discom-regulatory-filing/README.md#the-dataset-ies-arr-filing)
        - [A. Native IES shape](use-cases/discom-regulatory-filing/README.md#a-native-ies-shape)
        - [B. OpenADR 3 REPORT representation](use-cases/discom-regulatory-filing/README.md#b-openadr-3-report-representation)
      - [Setup Steps](use-cases/discom-regulatory-filing/README.md#setup-steps)
        - [1. Register the DISCOM and the SERC](use-cases/discom-regulatory-filing/README.md#1-register-the-discom-and-the-serc)
        - [2. Identifier hygiene](use-cases/discom-regulatory-filing/README.md#2-identifier-hygiene)
        - [3. Stand up the data-exchange adapters](use-cases/discom-regulatory-filing/README.md#3-stand-up-the-data-exchange-adapters)
        - [4. Catalogue the filing as a published dataset](use-cases/discom-regulatory-filing/README.md#4-catalogue-the-filing-as-a-published-dataset)
        - [5. Exercise the flow](use-cases/discom-regulatory-filing/README.md#5-exercise-the-flow)
        - [6. (Optional) Open the filing for public consumption](use-cases/discom-regulatory-filing/README.md#6-optional-open-the-filing-for-public-consumption)
      - [Operate](use-cases/discom-regulatory-filing/README.md#operate)
      - [Why This Matters](use-cases/discom-regulatory-filing/README.md#why-this-matters)
      - [Open Items](use-cases/discom-regulatory-filing/README.md#open-items)
      - [References](use-cases/discom-regulatory-filing/README.md#references)
* **[basic-checklist.md](use-cases/discom-regulatory-filing/basic-checklist.md)**
  - *Summary*: Checklist for regulatory cost mapping, adapter setup, and filing submissions.
  - *Outline / Headings*:
    - [Basic Checklist — DISCOM Regulatory Filing](use-cases/discom-regulatory-filing/basic-checklist.md#basic-checklist-discom-regulatory-filing)
        - [1. Decide which filings to start with](use-cases/discom-regulatory-filing/basic-checklist.md#1-decide-which-filings-to-start-with)
        - [2. Register the DISCOM and the SERC on the IES network](use-cases/discom-regulatory-filing/basic-checklist.md#2-register-the-discom-and-the-serc-on-the-ies-network)
        - [3. Agree the cost-category mapping](use-cases/discom-regulatory-filing/basic-checklist.md#3-agree-the-cost-category-mapping)
        - [4. Generate a sample filing as structured data](use-cases/discom-regulatory-filing/basic-checklist.md#4-generate-a-sample-filing-as-structured-data)
        - [5. Stand up the data-exchange adapters](use-cases/discom-regulatory-filing/basic-checklist.md#5-stand-up-the-data-exchange-adapters)
        - [6. Catalogue the filing and submit](use-cases/discom-regulatory-filing/basic-checklist.md#6-catalogue-the-filing-and-submit)
        - [7. (Optional) Open the filing for public consumption](use-cases/discom-regulatory-filing/basic-checklist.md#7-optional-open-the-filing-for-public-consumption)
        - [8. Production deployment and go-live](use-cases/discom-regulatory-filing/basic-checklist.md#8-production-deployment-and-go-live)
        - [9. Nominate your team](use-cases/discom-regulatory-filing/basic-checklist.md#9-nominate-your-team)
* **[README.md](use-cases/tariff-intelligence/README.md)**
  - *Summary*: Publishing tariff rate structures and telescopic schedules as IES policies.
  - *Outline / Headings*:
    - [Tariff Intelligence](use-cases/tariff-intelligence/README.md#tariff-intelligence)
      - [Scenario](use-cases/tariff-intelligence/README.md#scenario)
      - [Actors and Roles](use-cases/tariff-intelligence/README.md#actors-and-roles)
      - [Building Blocks Used](use-cases/tariff-intelligence/README.md#building-blocks-used)
      - [The Dataset — `IES_Policy`](use-cases/tariff-intelligence/README.md#the-dataset-ies-policy)
        - [Example — Mumbai Residential Telescopic](use-cases/tariff-intelligence/README.md#example-mumbai-residential-telescopic)
        - [Beyond tariffs](use-cases/tariff-intelligence/README.md#beyond-tariffs)
      - [Setup Steps](use-cases/tariff-intelligence/README.md#setup-steps)
        - [1. Register the publisher](use-cases/tariff-intelligence/README.md#1-register-the-publisher)
        - [2. Mint identifiers](use-cases/tariff-intelligence/README.md#2-mint-identifiers)
        - [3. Author the policy](use-cases/tariff-intelligence/README.md#3-author-the-policy)
        - [4. Sign and stage for publication](use-cases/tariff-intelligence/README.md#4-sign-and-stage-for-publication)
        - [5. Publish via Data Exchange](use-cases/tariff-intelligence/README.md#5-publish-via-data-exchange)
        - [6. (Optional) Use policies inline during private exchange](use-cases/tariff-intelligence/README.md#6-optional-use-policies-inline-during-private-exchange)
      - [Consuming a Tariff in a Billing System](use-cases/tariff-intelligence/README.md#consuming-a-tariff-in-a-billing-system)
      - [Operate](use-cases/tariff-intelligence/README.md#operate)
      - [Open Items](use-cases/tariff-intelligence/README.md#open-items)
      - [References](use-cases/tariff-intelligence/README.md#references)
* **[basic-checklist.md](use-cases/tariff-intelligence/basic-checklist.md)**
  - *Summary*: Checklist for policy authoring, signing, and billing integration testing.
  - *Outline / Headings*:
    - [Basic Checklist — Tariff Intelligence](use-cases/tariff-intelligence/basic-checklist.md#basic-checklist-tariff-intelligence)
        - [1. Decide which policies to publish](use-cases/tariff-intelligence/basic-checklist.md#1-decide-which-policies-to-publish)
        - [2. Register your organisation on the IES network](use-cases/tariff-intelligence/basic-checklist.md#2-register-your-organisation-on-the-ies-network)
        - [3. Mint stable identifiers for each policy](use-cases/tariff-intelligence/basic-checklist.md#3-mint-stable-identifiers-for-each-policy)
        - [4. Author the policy as structured data](use-cases/tariff-intelligence/basic-checklist.md#4-author-the-policy-as-structured-data)
        - [5. Sign the policy with the publisher's key](use-cases/tariff-intelligence/basic-checklist.md#5-sign-the-policy-with-the-publishers-key)
        - [6. Publish via the data exchange](use-cases/tariff-intelligence/basic-checklist.md#6-publish-via-the-data-exchange)
        - [7. Sample-consume the policy in a billing system](use-cases/tariff-intelligence/basic-checklist.md#7-sample-consume-the-policy-in-a-billing-system)
        - [8. Production deployment and go-live](use-cases/tariff-intelligence/basic-checklist.md#8-production-deployment-and-go-live)
        - [9. Nominate your team](use-cases/tariff-intelligence/basic-checklist.md#9-nominate-your-team)

---

## 🗺️ 7. Operational Pathways (Roadmaps)

Step-by-step project-management pathways for onboarding and network operations.

* **[README.md](pathways/README.md)**
  - *Summary*: Map of available role roadmaps in the IES ecosystem.
  - *Outline / Headings*:
    - [IES Pathways](pathways/README.md#ies-pathways)
      - [Why Pathways?](pathways/README.md#why-pathways)
      - [Available Pathways](pathways/README.md#available-pathways)
      - [How to Use the Pathways](pathways/README.md#how-to-use-the-pathways)
* **[utility.md](pathways/utility.md)**
  - *Summary*: The chronological onboarding roadmap for a new utility (DISCOM) joining the network.
  - *Outline / Headings*:
    - [Utility Pathway: Step-by-Step IES Integration Roadmap](pathways/utility.md#utility-pathway-step-by-step-ies-integration-roadmap)
      - [Roadmap Overview](pathways/utility.md#roadmap-overview)
      - [Prework & Pre-Alignment Matrix](pathways/utility.md#prework-pre-alignment-matrix)
      - [Phase 1: Preparation (Identity & Addressing)](pathways/utility.md#phase-1-preparation-identity-addressing)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [📋 Prework Required](pathways/utility.md#prework-required)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [References & Anchors](pathways/utility.md#references-anchors)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [References & Anchors](pathways/utility.md#references-anchors)
      - [Phase 2: Getting Started (Registry Setup)](pathways/utility.md#phase-2-getting-started-registry-setup)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [⚠️ Caution](pathways/utility.md#caution)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [References & Anchors](pathways/utility.md#references-anchors)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [References & Anchors](pathways/utility.md#references-anchors)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [📋 Prework Required](pathways/utility.md#prework-required)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [References & Anchors](pathways/utility.md#references-anchors)
      - [Phase 3: Consumer Energy Passport (Verifiable Credentials)](pathways/utility.md#phase-3-consumer-energy-passport-verifiable-credentials)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [References & Anchors](pathways/utility.md#references-anchors)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [📋 Prework Required](pathways/utility.md#prework-required)
        - [References & Anchors](pathways/utility.md#references-anchors)
      - [Phase 4: Smart Meter Data Exchange ([Beckn Data Pipes](../data-exchange/concepts.md))](pathways/utility.md#phase-4-smart-meter-data-exchange-beckn-data-pipesdata-exchangeconceptsmd)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [References & Anchors](pathways/utility.md#references-anchors)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [⚠️ Caution](pathways/utility.md#caution)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [References & Anchors](pathways/utility.md#references-anchors)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [References & Anchors](pathways/utility.md#references-anchors)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [⚠️ Caution](pathways/utility.md#caution)
        - [References & Anchors](pathways/utility.md#references-anchors)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [References & Anchors](pathways/utility.md#references-anchors)
      - [Phase 5: [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) (Electricity Bill)](pathways/utility.md#phase-5-consumer-meter-digestuse-casesconsumer-meter-digestreadmemd-electricity-bill)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [References & Anchors](pathways/utility.md#references-anchors)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [References & Anchors](pathways/utility.md#references-anchors)
      - [Phase 6: DER Visibility (Distributed Energy Resources)](pathways/utility.md#phase-6-der-visibility-distributed-energy-resources)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [📋 Prework Required](pathways/utility.md#prework-required)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [References & Anchors](pathways/utility.md#references-anchors)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [⚠️ Caution](pathways/utility.md#caution)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
      - [Phase 7: ARR Publication (Annual Revenue Requirement)](pathways/utility.md#phase-7-arr-publication-annual-revenue-requirement)
        - [💡 Phase Advice](pathways/utility.md#phase-advice)
        - [Execution Guidance](pathways/utility.md#execution-guidance)
        - [References & Anchors](pathways/utility.md#references-anchors)
* **[secretariat.md](pathways/secretariat.md)**
  - *Summary*: The operational roadmap for the Secretariat to approve registries, monitor networks, and maintain schemas.
  - *Outline / Headings*:
    - [IES Secretariat Pathway: Step-by-Step Registration Approval & Network Governance Roadmap](pathways/secretariat.md#ies-secretariat-pathway-step-by-step-registration-approval-network-governance-roadmap)
      - [Roadmap Overview](pathways/secretariat.md#roadmap-overview)
      - [Phase 1: Setting up IES-Specific Authoritative Registries](pathways/secretariat.md#phase-1-setting-up-ies-specific-authoritative-registries)
        - [💡 Phase Advice](pathways/secretariat.md#phase-advice)
        - [Execution Guidance](pathways/secretariat.md#execution-guidance)
        - [References & Anchors](pathways/secretariat.md#references-anchors)
        - [💡 Phase Advice](pathways/secretariat.md#phase-advice)
        - [Execution Guidance](pathways/secretariat.md#execution-guidance)
        - [References & Anchors](pathways/secretariat.md#references-anchors)
      - [Phase 2: Request Intake & Verification](pathways/secretariat.md#phase-2-request-intake-verification)
        - [Execution Guidance](pathways/secretariat.md#execution-guidance)
        - [References & Anchors](pathways/secretariat.md#references-anchors)
        - [⚠️ Caution](pathways/secretariat.md#caution)
        - [Execution Guidance](pathways/secretariat.md#execution-guidance)
        - [References & Anchors](pathways/secretariat.md#references-anchors)
      - [Phase 3: Approval & Provisioning](pathways/secretariat.md#phase-3-approval-provisioning)
        - [Execution Guidance](pathways/secretariat.md#execution-guidance)
        - [References & Anchors](pathways/secretariat.md#references-anchors)
        - [Execution Guidance](pathways/secretariat.md#execution-guidance)
        - [References & Anchors](pathways/secretariat.md#references-anchors)
      - [Phase 4: BECKN Network Governance](pathways/secretariat.md#phase-4-beckn-network-governance)
        - [💡 Phase Advice](pathways/secretariat.md#phase-advice)
        - [Execution Guidance](pathways/secretariat.md#execution-guidance)
        - [References & Anchors](pathways/secretariat.md#references-anchors)
        - [Execution Guidance](pathways/secretariat.md#execution-guidance)
        - [References & Anchors](pathways/secretariat.md#references-anchors)
      - [Phase 5: Schemas & Protocol Maintenance](pathways/secretariat.md#phase-5-schemas-protocol-maintenance)
        - [Execution Guidance](pathways/secretariat.md#execution-guidance)
        - [References & Anchors](pathways/secretariat.md#references-anchors)
        - [⚠️ Caution](pathways/secretariat.md#caution)
        - [Execution Guidance](pathways/secretariat.md#execution-guidance)
        - [References & Anchors](pathways/secretariat.md#references-anchors)

---

## ⚠️ Summary of Duplicate or Overlapping Information

During our audit of the `ies-accelerator` documentation, we identified several instances where identical schemas, configurations, or operational guidelines are duplicated across different directories:

### 1. Public Registry Definitions
* **Overlapping Files & Sections**:
  - Link: [Registries — Public and Private](identifiers/registries.md#the-public-ies-registries) (Raw reference: `identifiers/registries.md#the-public-ies-registries`)
  - Link: [Required Registries for IES Onboarding](registries/required-registries.md#discom-reference-registry) (Raw reference: `registries/required-registries.md#discom-reference-registry`)
* **Description**: Both sections define the properties of the authoritative `india-energy-stack` registries (DISCOMs Reference Registry, Regulators Reference Registry, and Schemas Registry), even copy-pasting the exact same JSON payload schemas and field tables.
* **Suggested Corrective Action**: Centralize the canonical record schemas and lookup field tables in `registries/required-registries.md`. Update `identifiers/registries.md` to focus strictly on the conceptual routing and resolution mapping, replacing duplicate JSON examples with direct links.

### 2. Beckn Node Registration and Onboarding
* **Overlapping Files & Sections**:
  - Link: [Required Registries: Beckn subscriber registry](registries/required-registries.md#beckn-subscriber-registry) (Raw reference: `registries/required-registries.md#beckn-subscriber-registry`)
  - Link: [Data Exchange: Registry Setup](data-exchange/registry-setup.md) (Raw reference: `data-exchange/registry-setup.md`)
* **Description**: Both guides describe how to generate signature/encryption keys for Beckn adapters, write the subscriber record under the `<your-namespace>/subscribers-test` registry path, and email the IES Secretariat for whitelisting.
* **Suggested Corrective Action**: Keep the high-level registry requirements in `registries/required-registries.md`, but move all technical steps (such as Ed25519 key generation commands, base64 formatting, and ONIX configuration options) into `data-exchange/registry-setup.md`.

### 3. Checklist Redundancies
* **Overlapping Files & Sections**:
  - Link: [Checklists Directory](checklists/) (Raw reference: `checklists/`)
    - [Energy Credentials Basic Checklist](checklists/energy-credentials-basic-checklist.md) (Raw reference: `checklists/energy-credentials-basic-checklist.md`)
    - [Energy Credentials Simple Checklist](checklists/energy-credentials-checklist.md) (Raw reference: `checklists/energy-credentials-checklist.md`)
    - [Energy Credentials Detailed Checklist](checklists/energy-credentials-checklist-detailed.md) (Raw reference: `checklists/energy-credentials-checklist-detailed.md`)
  - Link: [Use Cases Directory](use-cases/) (Raw reference: `use-cases/`)
    - [Smart Meter Basic Checklist](use-cases/smart-meter-data-exchange/basic-checklist.md) (Raw reference: `use-cases/smart-meter-data-exchange/basic-checklist.md`)
    - [Consumer Meter Digest Basic Checklist](use-cases/consumer-meter-digest/basic-checklist.md) (Raw reference: `use-cases/consumer-meter-digest/basic-checklist.md`)
    - [Consumer Energy Passport Basic Checklist](use-cases/consumer-energy-passport/basic-checklist.md) (Raw reference: `use-cases/consumer-energy-passport/basic-checklist.md`)
    - [Regulatory Filing Basic Checklist](use-cases/discom-regulatory-filing/basic-checklist.md) (Raw reference: `use-cases/discom-regulatory-filing/basic-checklist.md`)
    - [Tariff Intelligence Basic Checklist](use-cases/tariff-intelligence/basic-checklist.md) (Raw reference: `use-cases/tariff-intelligence/basic-checklist.md`)
* **Description**: The generic checklists duplicate domain allocation, Docker configurations, and registry checks. Additionally, every use-case-specific basic checklist duplicates identical organizational registration steps.
* **Suggested Corrective Action**: Consolidate generic onboarding audits into a single, multi-tier checklist under `checklists/` (e.g., Identity Setup, Credentials Setup, Exchange Setup). Replace individual use-case checklist files with short, use-case-specific checklists embedded directly in their respective `README.md` files.

---

## 💡 Suggestions on How the Documentation Can Be Improved

To enable a new utility to onboard and integrate with minimal external support, we suggest implementing the following documentation enhancements in the repository:

### 1. Add a Private DeDi Resolver Implementation Guide
* **Target Location**: [Registry Creation Guide](registries/registry-creation.md) (Raw reference: `registries/registry-creation.md`)
* **Improvement Proposal**: While private registries are conceptually introduced as "FastAPI or PostgreSQL thin wrappers", there are no concrete instructions. We should add a minimal, copy-pasteable FastAPI code snippet showing how to implement the lookup endpoint (`GET /lookup/{namespace}/{registry}/{record-id}`) and authenticate incoming internal queries using mTLS.

### 2. Add Code Examples for DigiLocker Webhook Signature Verification
* **Target Location**: [DigiLocker Integration](energy-credentials/digilocker-integration.md) (Raw reference: `energy-credentials/digilocker-integration.md`)
* **Improvement Proposal**: Utilities must secure their DigiLocker callback endpoints to prevent webhook spoofing. We should document the exact HMAC-SHA256 signature verification steps, providing a Python/NodeJS example showing how to compute and compare the signature header against the API Setu shared secret.

### 3. Consolidate Credential Revocation Hash Logic
* **Target Location**: [Verifying Credentials](energy-credentials/verification.md#status-list) (Raw reference: `energy-credentials/verification.md#status-list`)
* **Improvement Proposal**: The method for generating credential hashes (published to DeDi revocation lists) is fragmented across multiple guides. We should add a unified section demonstrating how to generate the hash (e.g., canonicalizing JSON via JCS RFC 8785, omitting signature blocks, and hashing via SHA-256) with a runnable script to avoid syntax and sorting discrepancies during verification.

### 4. Provide a Single Master Onboarding Quickstart Flow
* **Target Location**: [Getting Started](getting-started.md) (Raw reference: `getting-started.md`)
* **Improvement Proposal**: Introduce a visual onboarding timeline diagram (using Mermaid) at the top of "Getting Started". This diagram will lay out the precise sequence of tasks (DNS setup -> Key generation -> Registry request -> Service deployment) so that a new utility has a clear, unified project-management blueprint from day one.

---

## 🧠 Architectural Assessment: Resolution, Registries, and Logical Reorganization

We have performed an assessment of the logical sequencing, placement, and content organization within the identity and registry layers to guide future refactoring of the documentation:

### 1. Logical Sequencing & Placement of Identifier Resolution
* **The Assessment**: Currently, identifier resolution is placed under `[Identifiers & Addressing (DIDs) - Use & Operations](identifiers/resolution.md)`. However, resolving identifiers on the IES network is almost entirely dependent on Decentralized Directory (DeDi) registry structures. 
  - To resolve a `did:dedi` identifier, a client must query the DeDi registry endpoints directly.
  - To resolve a `did:web` identifier, a client must retrieve a `did.json` document hosted at a web server location, which conceptually acts as a simple read-only endpoint registry.
* **Logical Reorganization Proposal**: We propose that the **Identifiers** section should focus purely on naming conventions, syntax, and cryptographic formats (like key generation and DIDs grammar), referencing the **Registries & Resolution** section for all lookup operations. Identifier resolution should be moved under the **Registries and Directories (DeDi)** building block, as "Resolution" is the primary operational consumer of registries.

### 2. Resolution Mechanics by DID Method
To prevent confusion for developers onboarding to the IES accelerator, the documentation should clearly delineate the distinct resolution mechanism required for each supported identifier method:
* **`did:key` / `did:jwk` (Offline Cryptographic)**:
  - *Mechanism*: Requires no network lookup or registry querying. The public key is mathematically encoded inside the identifier string itself. Resolution is performed entirely offline using local SDK functions.
* **`did:web` (HTTPS-based)**:
  - *Mechanism*: Resolves over the public web via an HTTPS request. The resolver translates the DID (e.g., `did:web:ies.tpddl.in`) into a standard path to fetch the public verification key (e.g., `https://ies.tpddl.in/.well-known/did.json`).
* **`did:dedi` (Directory API Query)**:
  - *Mechanism*: Resolves by querying the Decentralized Directory (DeDi) API. The resolver parses the coordinate string (`did:dedi:<namespace>:<registry>:<record-id>`) and issues a signed HTTP GET lookup request (e.g., `GET /lookup/<namespace>/<registry>/<record-id>`) against the registered DeDi resolver endpoints.

### 3. Unification of Public vs. Private Resolution Details
Resolution itself is the logical point where public and private views of network data converge. The documentation should bring these details together explicitly:
* **The Two-Resolver Model**: An identifier like `did:dedi:tpddl:consumers:CN-123` represents the same consumer entity in both public and private contexts. However, the resolver queries different endpoints depending on the routing context:
  - *Public Resolution*: Queries the public DeDi network, returning a redacted record containing only non-sensitive metadata (e.g., city, tariff category, status) to preserve DPDP compliance.
  - *Private Resolution*: Queries the utility's internal private DeDi resolver mirror, returning the full record with sensitive PII (name, address, billing details) for internal SCADA/billing consumption.
* **Unification via `privateRef`**: The public record contains a `privateRef` pointer (e.g., `https://internal-dedi.tpddl.in/dedi/lookup/...`) linking the two views. While public verifiers ignore this pointer, authorized internal clients follow it to retrieve the full, private state of the entity, unifying the public identity and private data planes.

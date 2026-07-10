# What IES Is Not

Five common confusions about IES, cleared up.

---

## IES is NOT…

| # | Confusion | Reality |
|---|---|---|
| 1 | **A central platform or database that stores energy data** | IES stores nothing. Data stays in the systems that already hold it. IES is only the shared set of specifications that lets any two systems exchange and act on it directly. |
| 2 | **A replacement for any existing DISCOM system, MDM or consumer-information system** | Your CIS, MDM, HES, DERMS, ERP, billing, web portal — none of these change. The IES adapter sits at the edge. Internal databases, field names and software stay exactly as they are. |
| 3 | **A new regulator or authority that frames energy rules** | IES adds no new rules. It turns existing CEA, CERC and State Supply Code rules into a form software can read. The IES Cell, being constituted under the Central Electricity Authority, governs the specifications themselves — not the regulations they encode. |
| 4 | **A software product that utilities buy and install** | IES is a set of open, published specifications. No licence fee. No central platform. A ready-made adapter (the Beckn ONIX reference) is provided as open software to start with. |
| 5 | **A system that controls or monitors the physical grid** | IES facilitates a secure link between parties to exchange data. It does not touch SCADA, DMS, EMS or any safety-critical control system. The information it carries is mostly non-safety-critical metadata, telemetry and credentials. |

---

## Things IES does NOT ask for

- **No new data.** Existing data just gets a common, signed format when shared.
- **No new compliance work.** IES makes an existing DISCOM filing machine-readable, not a new one.
- **No replacement of completed integrations.** A finished metering integration isn't wasted — IES sets the standard for the *next* one.
- **No mandatory bulk data transport.** IES specifies format and coordination, not transport — bulk data still moves over your normal channels (secure web, SFTP, Kafka, signed URL), with IES carrying the agreement, consent and audit trail.
- **No personal data storage.** Consumer data is shared only with explicit consent for the stated purpose — IES itself holds none.

---

## Where IES draws the line

| IES does | IES does not do |
|---|---|
| Define the shape of a meter-data record | Read meters or run an MDM |
| Define how two systems agree to exchange data | Move bytes between them — your existing channels do |
| Define the structure of a tariff order or ARR filing | Approve tariffs or evaluate filings |
| Issue a Consumer Energy Passport from a DISCOM | Hold the consumer's wallet (DigiLocker does that) |
| Standardise the credentialing of a rooftop solar unit | Decide whether the unit may be connected (the DISCOM and the regulator do that) |
| Carry a verifiable record of an outage notification | Operate the OMS, ADMS or feeder switching |

---

## Why this distinction matters

IES is **infrastructure**, not application — the layer everything builds on, like UPI or DigiLocker. Staying scoped to identity, discovery and exchange keeps it from competing with existing software, regulators or operations. It does the work nobody owns today.

> Next: read **[What Changes for the Sector](sector-impact.md)** for the practical outcomes, or **[Common Questions](faq.md)** for the questions most often asked.

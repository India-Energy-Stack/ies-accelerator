# Common Questions

The questions most often asked by utilities, regulators and vendors. The answers below are drawn from the IES Technical Note and the experience of the four pilot DISCOMs.

---

## Scope and impact

### Does IES replace existing systems?

**No.** IES does not store, run or control any data or systems. Everything an organisation runs today continues to run. IES only standardises the way systems share data with other organisations' systems.

### Is IES only for connecting to other organisations, or also for internal systems?

**Mainly external.** That is where most of the difficulty lies today. The same adapter and standard also help within an organisation, where several systems from different vendors may not be able to exchange data with each other. The larger gain is external, across DISCOMs and States; the internal improvement follows.

### Will IES create new compliance work?

**No.** IES asks for no new data. It only puts the data already produced into a common format when it is shared.

### If a metering system has just been integrated, is that work wasted?

**No.** IES does not require redoing what has been built. It sets the common standard the next integration will follow, so the next one is easier.

### Where does the data go?

**Nowhere new.** Data stays where it is created. IES only standardises how the data is described and requested when it has to move from one organisation to another.

### Some functions can already be done within a single DISCOM. Why is IES needed?

A few functions, such as shifting demand within a single area, can be done alone today. **But IES is built for the whole country, and this benefits every participant, not only others.** A consumer who moves in from another State arrives with an energy record that can be trusted at once, with no fresh verification. A bank or scheme anywhere in India can accept a record a DISCOM has issued, so consumers receive faster service. And a service or vendor proven in one State is available to others without being rebuilt.

### Is IES still relevant for an organisation that mainly wants to improve existing systems rather than build new ones?

**Yes.** The same one-time adapter serves both purposes. It improves how current systems exchange data today, and provides the base to add new services later on the same standard. There is no need to choose between improving existing systems and building new ones.

---

## Cost, procurement and installation

### Is IES something to be bought and installed?

**No.** IES is a set of open, published specifications. There is no licence fee and no central platform to install. A ready-made connector (the adapter) is provided to start with.

### Who builds the connector?

The connector — the **adapter** — is mostly ready-made. IES provides it as open software, based on the Beckn ONIX reference implementation, together with a working sample. An organisation's technology vendor configures it for its systems and adds the translation between its data format and the IES format. Vendors build to one published standard, not a fresh custom integration each time.

### What does a DISCOM gain commercially from IES?

Three things, in plain terms:

1. **Lower cost.** One published standard replaces repeated custom integration work. Procurement and integration spend fall, with no lock-in to a single vendor.
2. **Better operations.** Reliable, verifiable data supports demand forecasting and analytics that can improve power procurement and reduce losses over time.
3. **Wider use of existing data.** With consumer consent, verified records can support services like green lending and rooftop solar financing — and the demand for those records flows back through the DISCOM.

**IES is not a revenue scheme and does not monetise personal data.** It lowers cost and makes the data a DISCOM already holds more useful.

---

## Adding new services and devices

### If a new service or a new kind of device is added later, does the process start over?

**No.** Each asset — a meter, a solar unit, an EV charger — is given its digital identity at the moment a use case first needs it, not all at once on day one. Everything already in place (verified identities, trust checks, agreed data formats) is reused. The first asset connected takes the most effort; each one after is far easier.

---

## Security and privacy

### Does IES meet cybersecurity requirements for the power sector?

**Yes.** IES is being designed to follow the applicable cyber-security regulations for the power sector. Every message carries a digital signature, and the identity, consent and data layers are kept separate. The adapter sits at the edge of a system only and does not create new internal integration points. Security incidents follow the established power-sector incident response process. IES facilitates a secure link between parties, mostly using non-safety-critical information, and does not necessitate all the data passing through a central bottleneck.

### How is a consumer's private data protected?

**Selectively.** The consumer can prove a single fact, for example that the sanctioned load is above a certain level, without revealing the rest of the data.

### Does IES protect personal data?

**Yes.** IES does not store personal data. Consumer data is shared only with the consumer's explicit consent, and only for the stated purpose. IES is being designed to follow the applicable data protection law.

---

## Regulation

### Does IES change the relationship with the regulator?

**No.** IES only turns the existing CEA and CERC rules into a form software can read. If putting a rule into practice reveals a gap, IES points it out to the regulator. Only the regulator decides what to do about it.

---

## Status and governance

### Is IES live, or still on paper?

**Live.** The sandbox is running, and [four pilot DISCOMs](pilots.md) have built in it.

### What does the consumer receive?

A portable, verifiable record of their connection with the DISCOM — including sanctioned load, any sanctioned generation, and their own consumption history — held in [DigiLocker](../glossary.md#digilocker). The consumer can share it, on their own terms, to obtain a green loan, claim a subsidy or sign up for a service, without returning to the DISCOM for paperwork each time. Portable, verifiable records also let a utility serve its consumer base better: faster enrolment, fewer repeat verifications, and new services built on consented data.

### Does IES support large or bulk data transfers?

**Yes, with no size limit.** IES specifies the data format and the coordination, not the transport, so the data always moves over the organisation's normal channels (secure web connection, file transfer, signed URL, Kafka, MQTT, SFTP). Two options:

- **Inline** — the data is sent in smaller batches inside the IES-formatted messages themselves. Best for small / mid-sized one-time pulls.
- **By link (access-method handoff)** — the data stays as a file (or stream), and the IES message carries a signed link / pointer / streaming endpoint to fetch it. Best for streaming or SLA-bound feeds, and multi-gigabyte artefacts.

Either way, IES handles discovery, consent, the data shape, and the audit trail. No separate "bulk feature" is needed.

### Who adds or updates the specifications and standards?

The **IES Cell** — the governance body being constituted under the Central Electricity Authority, with representation from across the sector. It owns the specifications, decides what is added or changed, and publishes each version. Its detailed governance framework will be notified separately.

### What is the process to request changes to the published specifications?

Any participant can propose a change to the IES Cell. Proposals are reviewed, and accepted changes are published as a new, versioned specification, so every implementation knows what changed and when. The detailed process will be set out once the IES Cell's governance framework is notified. Until then, raise an issue or a discussion in the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator).

---

## Still have a question?

- **For technical questions** — open an issue or a discussion at [github.com/India-Energy-Stack/ies-accelerator](https://github.com/India-Energy-Stack/ies-accelerator).
- **For policy or governance questions** — `ies.secretariat@fsrglobal.org`.
- **For onboarding / nodal-agency questions** — `ies@recindia.com`.

# Common Questions

Questions utilities, regulators and vendors ask most, drawn from the IES Technical Note and the four pilot DISCOMs' experience.

---

## Scope and impact

### Does IES replace existing systems?

**No.** IES stores, runs or controls nothing — it only standardises how systems already running share data with each other.

### Is IES only for connecting to other organisations, or also for internal systems?

**Mainly external**, where most difficulty lies — though the same adapter helps internal cross-vendor data exchange too.

### Will IES create new compliance work?

**No.** IES asks for no new data — it just puts data already produced into a common format when shared.

### If a metering system has just been integrated, is that work wasted?

**No.** Nothing built has to be redone. IES sets the standard the next integration follows, making it easier.

### Where does the data go?

**Nowhere new.** Data stays put; IES only standardises how it's described and requested when moved between organisations.

### Some functions can already be done within a single DISCOM. Why is IES needed?

Some functions, like shifting demand locally, work today without IES. **But IES is built for the whole country, and every participant benefits:** an incoming consumer's record is trusted instantly, any bank in India can accept a DISCOM-issued record, and a proven service works elsewhere unchanged.

### Is IES still relevant for an organisation that mainly wants to improve existing systems rather than build new ones?

**Yes.** The same one-time adapter improves today's data exchange and provides the base for new services later, on the same standard.

---

## Cost, procurement and installation

### Is IES something to be bought and installed?

**No.** IES is open, published specifications — no licence fee, no central platform. A ready-made connector (the adapter) gets you started.

### Who builds the connector?

The **adapter** is mostly ready-made: open software on the Beckn ONIX reference implementation, with a working sample. A vendor configures it and adds IES-format translation — one standard, not a custom build each time.

### What does a DISCOM gain commercially from IES?

Three things:

1. **Lower cost.** One standard replaces custom integration, no vendor lock-in.
2. **Better operations.** Reliable data supports demand forecasting and analytics that cut losses.
3. **Wider use of existing data.** With consent, verified records support services like green lending and rooftop solar financing, with demand flowing back through the DISCOM.

**IES is not a revenue scheme and does not monetise personal data** — it lowers cost and makes DISCOM data more useful.

---

## Adding new services and devices

### If a new service or a new kind of device is added later, does the process start over?

**No.** Each asset — meter, solar unit, EV charger — gets its identity only when a use case needs it, not all at once. Existing verified identities, trust checks and data formats are reused, so each new asset connects more easily than the first.

---

## Security and privacy

### Does IES meet cybersecurity requirements for the power sector?

**Yes.** IES follows applicable power-sector cyber-security rules. Every message is signed; identity, consent and data layers stay separate. The adapter sits only at a system's edge, adding no new integration points, and incidents follow the established response process. Data stays mostly non-safety-critical, skipping any central bottleneck.

### How is a consumer's private data protected?

**Selectively.** A consumer can prove a single fact — e.g. that sanctioned load exceeds a threshold — without revealing the rest.

### Does IES protect personal data?

**Yes.** IES stores no personal data; it's shared only with the consumer's explicit consent, for the stated purpose, following applicable data protection law.

---

## Regulation

### Does IES change the relationship with the regulator?

**No.** IES only turns existing CEA and CERC rules into a form software can read. If a gap surfaces, IES flags it — the regulator alone decides what to do.

---

## Status and governance

### Is IES live, or still on paper?

**Live.** The sandbox is running, and [four pilot DISCOMs](pilots.md) have built in it.

### What does the consumer receive?

A portable, verifiable record of their DISCOM connection — sanctioned load, any sanctioned generation, consumption history — held in [DigiLocker](../glossary.md#digilocker). Consumers share it on their own terms for a green loan, subsidy claim or service enrolment, skipping repeat paperwork.

### Does IES support large or bulk data transfers?

**Yes, with no size limit.** IES specifies data format and coordination, not transport — data moves over the organisation's normal channels (secure web, file transfer, signed URL, Kafka, MQTT, SFTP). Two options:

- **Inline** — smaller batches inside IES-formatted messages; best for small/mid pulls.
- **By link (access-method handoff)** — data stays a file or stream; the message carries a signed link to fetch it; best for streaming or multi-gigabyte artefacts.

IES handles discovery, consent, data shape and audit trail throughout — no separate "bulk feature" needed.

### Who adds or updates the specifications and standards?

The **IES Cell** — the governance body being constituted under the Central Electricity Authority, with sector-wide representation — owns the specifications and publishes each version. Its governance framework will be notified separately.

### What is the process to request changes to the published specifications?

Any participant can propose a change to the IES Cell; accepted changes are published as a new, versioned specification. The process will be set out once the Cell's governance framework is notified — until then, raise an issue in the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator).

---

## Still have a question?

- **For technical questions** — open an issue or a discussion at [github.com/India-Energy-Stack/ies-accelerator](https://github.com/India-Energy-Stack/ies-accelerator).
- **For policy or governance questions** — `ies.secretariat@fsrglobal.org`.
- **For onboarding / nodal-agency questions** — `ies@recindia.com`.

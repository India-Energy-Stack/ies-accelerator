# Basic Checklist — Registries and Directories

*A plain-English, conceptual checklist for a DISCOM (or any organisation) setting itself up on the IES trust layer. Use it to scope the work and align your team. The [detailed reference](../registries/README.md) covers exactly how each step is done.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Claim your space in the public directory

Create a verified namespace for your organisation on the IES directory platform (`dedi.global`). Think of this as reserving your organisation's section in a public address book — proven to belong to your DISCOM by domain verification.

- [ ] Account created on the directory platform
- [ ] Namespace name chosen (e.g. your DISCOM short code)
- [ ] Domain verification completed

### 2. Publish your trust anchor

Publish a single public record that says "this is our DISCOM, here is our public key, here is our official domain". This is what verifiers across the network look up to decide whether to trust anything you sign.

- [ ] Trust anchor record published
- [ ] Record visible to the public via a simple lookup

### 3. Decide which registries you need to operate

Depending on which IES capabilities you are adopting, you will need to set up a small number of additional registries inside your namespace — for example, a list of revoked credentials, a list of approved data subscribers, or a list of your assets. Pick what applies to you.

- [ ] Required registries identified for your use case (see [Required Registries](../registries/required-registries.md))
- [ ] Owner nominated for each registry

### 4. Decide who can write to each registry

For each registry, decide who inside your DISCOM is allowed to add or change records, and who only needs to read. Keep the writer list short — this is a security boundary.

- [ ] Writer roles assigned and documented
- [ ] Access credentials issued only to the writer roles

### 5. Set up a process to keep registries current

Records go stale. Agree a simple operational cadence — who updates the registry when a meter is replaced, when a key rotates, when a credential is revoked, when an asset is decommissioned.

- [ ] Update process documented for each registry
- [ ] Backup / recovery plan agreed for namespace keys

### 6. Nominate your team

Identify two roles: an **IT point of contact** who operates the registries day-to-day, and an **Authorised Signatory** who approves what gets published.

- [ ] IT SPOC nominated (name, email, phone)
- [ ] Authorised Signatory nominated (name, email, phone)

---

*Once these six items are in place, your DISCOM has a working trust layer that the rest of IES — credentials, data exchange, policy publication — can build on. See the [detailed registries reference](../registries/README.md) for the full technical specification.*

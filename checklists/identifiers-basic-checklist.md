# Basic Checklist — Identifiers and Addressing

*A plain-English, conceptual checklist for a DISCOM (or any organisation) joining IES. Use it to scope the work and align your team. The [detailed reference](../identifiers/README.md) covers exactly how each step is done.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Decide your organisation's public name on the network

Pick the public web identifier the rest of the ecosystem will use to refer to your DISCOM — typically a domain you already own (e.g. `discom.gov.in`). This becomes the anchor for everything else you publish.

- [ ] Domain selected and confirmed available for use as an IES identifier

### 2. Set up your digital identity

Your IT team generates a public/private key pair — your DISCOM's digital seal. The public key is published at a fixed location on your domain so anyone in the ecosystem can independently verify that a credential, dataset, or message genuinely came from you.

- [ ] Key pair generated and securely stored
- [ ] Public key published at the agreed location on your domain

### 3. Agree on how you will identify consumers and assets

Decide how your existing internal numbers (consumer numbers, meter numbers, asset IDs) will be wrapped into network-friendly identifiers. **You do not need to renumber anything internally** — the wrapping is deterministic and reversible.

- [ ] Mapping rule agreed for: consumers, meters, assets, documents
- [ ] Confirmed that no internal renumbering is required

### 4. Decide what stays private and what becomes public

For each type of identifier (consumer, meter, asset, document), decide whether it should be resolvable only within your organisation or visible to the wider network. Both are supported and follow the same shape.

- [ ] Privacy decision made for each identifier type
- [ ] Internal vs. public registry boundary documented

### 5. Nominate your team

Identify two roles: an **IT point of contact** for the technical setup, and a **Governance / Compliance point of contact** to approve what gets published publicly.

- [ ] IT SPOC nominated (name, email, phone)
- [ ] Governance SPOC nominated (name, email, phone)

---

*Once these five items are in place, your DISCOM is ready to register in the IES ecosystem directory and start issuing credentials or publishing data. See the [detailed identifiers reference](../identifiers/README.md) for the full technical specification.*

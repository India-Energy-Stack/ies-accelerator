# Step 4 — Conformance Checklist

The fourth and final step: verify your adapter end-to-end and submit for production network membership. About 1 day.

The minimum to participate in IES is **the same for every organisation**:

1. Create a digital identity and list your organisation in the shared directory. ([Step 1](setup-register.md))
2. Install the adapter once. ([Step 2](setup-discovery.md))
3. Pass the basic conformance check. (this page)

After this, new partners connect without fresh integration work.

---

## What conformance means

A conformant participant satisfies all of the following.

### Identity is correctly published

- [ ] `did:web` resolves from outside your network (`curl https://<your-domain>/.well-known/did.json` returns valid JSON)
- [ ] The DID document declares your current signing key
- [ ] Key rotation procedure documented (who, how, on what trigger)
- [ ] DeDi namespace verified (DNS TXT proof) and queryable

### Network membership is in place

- [ ] Beckn subscriber record published in your DeDi namespace (Ed25519 key, callback URL, BAP/BPP role)
- [ ] Reference entry written by the IES Secretariat into the IES network registry
- [ ] Sandbox loop succeeds (search round-trip with a peer)

### At least one use case is wired and validates

- [ ] One [Use Case Guide](../use-cases/README.md) implemented end-to-end
- [ ] Output validates against the canonical JSON Schema (`make validate` or `python3 scripts/validate_schema.py …`)
- [ ] At least one real record exchanged with a counterparty on the testnet
- [ ] Schema validation enforced on every outgoing payload in your handler

### Signatures and trust chain check out

- [ ] Every credential you issue carries a valid signature (W3C VC Data Model 2.0 proof block)
- [ ] Every Beckn message you send carries a valid Ed25519 signature
- [ ] Revocation registry exists in your DeDi namespace (OpenCred auto-creates this; if not using OpenCred, create it manually)
- [ ] Verification rehearsed by at least one counterparty (peer DISCOM, AMISP, bank)

### Operations

- [ ] Logging captures every inbound and outbound Beckn message (subscriber, action, message id, timestamp)
- [ ] Monitoring / alerting on adapter health
- [ ] Key rotation runbook
- [ ] Incident escalation path defined (within IES Secretariat process)

### Security and privacy

- [ ] Signing keys held in KMS / HSM where available; never in source control
- [ ] TLS on all callback endpoints
- [ ] For consumer-facing credentials: identity-proofing procedure documented and privacy-reviewed
- [ ] For consumer-facing credentials: explicit consent capture on every issuance / disclosure

---

## How to confirm conformance

Run the conformance suite that ships with the devkit:

```bash
cd DEG/devkits/data-exchange/conformance
./run.sh --subscriber did:web:ies.discom.example --usecase consumer-energy-passport
```

It exercises every checklist item above against a sandbox peer and emits a signed report.

For use cases not yet in the suite, do the equivalent manually:

1. Generate one record using your adapter.
2. Validate it with the canonical JSON Schema (`scripts/validate_schema.py`).
3. Send it to a sandbox counterparty.
4. Have them verify the signature and the contents.

---

## Submitting for production

When all the above pass on the sandbox / testnet:

1. Email the IES Secretariat (`ies@recindia.com`) with: your `did:web`, your DeDi namespace, your testnet conformance report, and the use cases you have implemented.
2. The Secretariat re-runs spot checks on your sandbox endpoints.
3. The Secretariat writes a production reference entry pointing at your subscriber record.

You're now IES-conformant in production — new counterparties can transact with you without further arrangement.

---

## After conformance

- **Add new use cases** by repeating only Step 3 (Build your Internal-facing Adapter) for the new schema — identity, ONIX, network membership and trust foundation are reused.
- **Stay current with schema versions.** New versions are announced via the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator); migration guides ship alongside.
- **Contribute** — propose a new schema or a change to an existing one by raising a discussion on the repository. The [IES Cell](../concepts/faq.md#who-adds-or-updates-the-specifications-and-standards) governance process handles ratification.

# Conformance Checklist

> **Step 5 of the implementation path.** Verify your interface is correct end-to-end and (for Beckn participants) submit for IES network membership in production. About 1 day.

## Before you start

- Step 1 ([Setup Register](setup-register.md)) complete for your role.
- The engine(s) your use cases need are running: [Issue Credentials](issue-credentials.md) (B2C) and/or [Setup Exchange](setup-exchange.md) (B2B).
- At least one use case wired through [Build your Internal-facing Adapter](build-adapter.md) (Step 4).

**Only the checks for the rails you actually use apply.** The checklist below is tagged: **[all]** applies to everyone, **[credential]** only to credential issuers (B2C), **[beckn]** only to Beckn-network participants (B2B). A credential-only issuer skips every **[beckn]** item and the production-network submission at the end; a pure data-exchange participant skips every **[credential]** item.

---

## What conformance means

### Identity is correctly published **[all]**

- [ ] `did:web` resolves from outside your network (`curl https://<your-domain>/.well-known/did.json` returns valid JSON)
- [ ] The DID document declares your current signing key
- [ ] Key rotation procedure documented (who, how, on what trigger)
- [ ] DeDi namespace verified (DNS TXT proof) and listed on `explore.dedi.global`

### Network membership is in place **[beckn]**

- [ ] Beckn subscriber record published in your DeDi namespace (Ed25519 key, callback URL, BAP/BPP role)
- [ ] Reference entry written by the IES Secretariat into the IES network registry
- [ ] Sandbox loop succeeds (`discover` or `confirm` round-trip with a peer)

### At least one use case is wired and validates **[all]**

- [ ] One [Use Case Guide](../use-cases/README.md) implemented end-to-end
- [ ] Output validates against the canonical JSON Schema (`make validate` or `python3 scripts/validate_schema.py …`)
- [ ] **[beckn]** At least one real record exchanged with a counterparty on the testnet, **or [credential]** at least one credential issued, verified, and revoked (the [§2.9 smoke test](issue-credentials.md#id-2.9-smoke-test))
- [ ] Schema validation enforced on every outgoing payload

### Signatures and trust chain check out

- [ ] **[credential]** Every credential you issue carries a valid signature (W3C VC Data Model 2.0 proof block)
- [ ] **[credential]** Revocation registry (`vc-revocation-registry`) exists in your DeDi namespace (OpenCred auto-creates it; if not using OpenCred, create it manually)
- [ ] **[credential]** Verification rehearsed by at least one relying party (peer DISCOM, bank, marketplace) resolving your `did:web`
- [ ] **[beckn]** Every Beckn message you send carries a valid Ed25519 signature
- [ ] **[beckn]** Signature verification rehearsed by at least one counterparty (peer DISCOM, AMISP)

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

### Beckn participants (B2B)

Run the conformance suite that ships with the devkit you cloned in [Setup Exchange](setup-exchange.md#id-3.1-deploy-the-local-sandbox):

```bash
cd DEG/devkits/data-exchange/conformance
./run.sh --subscriber did:web:ies.discom.example --usecase consumer-energy-passport
```

The script exercises every path on the checklist above against a sandbox peer and emits a signed report. For use cases not yet in the suite, do the equivalent manually: generate one record with your adapter, validate it against the canonical JSON Schema (`scripts/validate_schema.py`), send it to a sandbox counterparty, and have them verify the signature and contents.

### Credential-only issuers (B2C)

You have no Beckn devkit and no counterparty, so conformance is self-contained — run the [§2.9 smoke test](issue-credentials.md#id-2.9-smoke-test) end-to-end:

1. Issue a credential with your adapter (or OpenCred directly).
2. Validate the `credentialSubject` against the canonical JSON Schema (`python3 scripts/validate_schema.py schemas/<Credential>/<version>/schema.json out.json`).
3. Resolve your own `did:web` over HTTPS and confirm the published key verifies the credential's `proof`.
4. Check revocation status (not revoked), revoke, re-check (revoked).

If all four pass, your issuance is conformant — there is nothing to submit to the network, because credentials are verified directly against your `did:web` by whoever receives them.

---

## Submitting for production **(Beckn participants only)**

When all the above pass on the sandbox / testnet:

1. Email the IES Secretariat ([IES.Secretariat@fsrglobal.org](mailto:IES.Secretariat@fsrglobal.org), alternate [ies@recindia.com](mailto:ies@recindia.com)) with: your `did:web`, your DeDi namespace, your testnet conformance report, and the use cases you have implemented.
2. The Secretariat re-runs spot checks on your sandbox endpoints.
3. The Secretariat writes a production reference entry pointing at your subscriber record.

You are now an IES-conformant production participant. New counterparties can transact with you without any further bilateral arrangement. (Credential-only issuers skip this — you can issue production credentials the moment the B2C checks above pass.)

---

## After conformance

- **Add new use cases** by repeating only Step 4 (Build your Internal-facing Adapter) for the new schema. Identity, engines, network membership and trust foundation are reused.
- **Stay current with schema versions.** New versions are announced via the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator); migration guides ship alongside.
- **Contribute** — propose a new schema or a change to an existing one by raising a discussion on the repository. The [IES Cell](../faq.md#id-19.-who-adds-or-updates-the-specifications-and-standards) governance process handles ratification.

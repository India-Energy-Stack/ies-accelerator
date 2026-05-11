# Deployment

This page walks a DISCOM tech team from zero to a running OpenCred service that can sign DEG energy credentials. At the end you will have:

- The OpenCred server running on Linux
- A signing key loaded — either from a file, an HSM, or your existing DSC
- A `did:web` (or `did:key`) issuer DID published and resolvable
- (Optional) A DeDi namespace configured for revocation

You will issue your first credential in [Issuing Credentials](./issuance.md).

---

## Prerequisites

- A Linux host (cloud VM, on-prem, or Kubernetes node) with outbound HTTPS
- Docker 20.10+
- One of:
  - A domain you control for `did:web` (recommended) — e.g. `ies.tpddl.in`
  - An existing Digital Signature Certificate (DSC) in PFX/PEM form
  - An AWS / Azure / GCP KMS key with appropriate IAM access
- (Optional, for revocation) A DeDi namespace from [dedi.global](https://dedi.global) and either an API key or bearer credentials
- A secrets manager (Vault, AWS Secrets Manager, Azure Key Vault) for `OPENCRED_API_KEY` and DeDi credentials

---

## Step 1 — Pull the OpenCred image

```bash
docker pull ghcr.io/nfh-trust-labs/opencred/opencred-server:latest
```

The image is public; no GHCR authentication is needed. Pin to a specific tag (`:v1.x.y`) in production rather than `latest`.

---

## Step 2 — Decide your signing-key model

| Model | Best for | Setup |
|---|---|---|
| **Software file (PEM/JWK/PFX)** | Dev, small DISCOMs, first deploy | Generate or import; mount read-only |
| **Cloud KMS** (AWS / Azure / GCP) | Production at scale | One IAM grant; OpenCred uses default credential chain |
| **Existing DSC** | DISCOMs already operating with a CCA-issued DSC | Import as PFX/PEM; OpenCred derives `did:key` |

For a first deploy, generate an ECDSA P-256 key locally. You can rotate to KMS later without changing your DID by re-uploading the same public key.

### Generate a software key

```bash
# Inside a secure host (not a shared dev box)
openssl ecparam -name prime256v1 -genkey -noout -out issuer-key.pem
chmod 600 issuer-key.pem

# Extract the public key for did:web
openssl ec -in issuer-key.pem -pubout -out issuer-pub.pem
```

Move `issuer-key.pem` to your secrets store. Do not commit it.

---

## Step 3 — Set up your issuer DID

### Option A — `did:web` (recommended)

You publish a single static JSON file at `https://<your-domain>/.well-known/did.json`. Verifiers fetch it to validate signatures.

1. Boot OpenCred locally with your software key (Step 4 below).
2. Call `POST /v1/keys/publish` (or compose the DID document manually — see below) to get the published JSON.
3. Upload the JSON to `https://ies.tpddl.in/.well-known/did.json` via your web server.
4. Your issuer DID is `did:web:ies.tpddl.in`.

A minimal `did.json`:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/jws-2020/v1"
  ],
  "id": "did:web:ies.tpddl.in",
  "verificationMethod": [{
    "id": "did:web:ies.tpddl.in#key-1",
    "type": "JsonWebKey2020",
    "controller": "did:web:ies.tpddl.in",
    "publicKeyJwk": {
      "kty": "EC",
      "crv": "P-256",
      "x": "<base64url x>",
      "y": "<base64url y>"
    }
  }],
  "assertionMethod": ["did:web:ies.tpddl.in#key-1"],
  "authentication": ["did:web:ies.tpddl.in#key-1"]
}
```

OpenCred's `did:web` resolver enforces HTTPS-only, no redirects, no private-IP targets, and a 10-second timeout — make sure the file is served from a public HTTPS endpoint with a CA-issued certificate.

### Option B — `did:key` from a DSC

Mount the DSC file and let OpenCred derive a `did:key` from the certificate's public key.

```bash
docker run -p 3100:3100 \
  -e OPENCRED_API_KEY=$OPENCRED_API_KEY \
  -e OPENCRED_KEY_PATH=/secrets/issuer.pfx \
  -e OPENCRED_KEY_PASSWORD=$PFX_PASSWORD \
  -v $(pwd)/issuer.pfx:/secrets/issuer.pfx:ro \
  ghcr.io/nfh-trust-labs/opencred/opencred-server:latest
```

Read the issuer DID from `GET /v1/keys`. You will pass it as `issuerDid` in every issue call.

---

## Step 4 — Run OpenCred

### Quick start (software key)

```bash
export OPENCRED_API_KEY=$(openssl rand -base64 32)

docker run -d --name opencred -p 3100:3100 \
  -e OPENCRED_PORT=3100 \
  -e OPENCRED_API_KEY=$OPENCRED_API_KEY \
  -e OPENCRED_KEY_PATH=/secrets/issuer-key.pem \
  -e OPENCRED_LOG_LEVEL=info \
  -v /etc/opencred/issuer-key.pem:/secrets/issuer-key.pem:ro \
  --read-only \
  --tmpfs /tmp:noexec,nosuid,size=64m \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  ghcr.io/nfh-trust-labs/opencred/opencred-server:latest
```

Sanity check:

```bash
curl -s http://localhost:3100/v1/health
# {"status":"ok","ready":true,"signingKeyLoaded":true, ...}
```

### Docker Compose (production)

```yaml
services:
  opencred:
    image: ghcr.io/nfh-trust-labs/opencred/opencred-server:latest
    container_name: opencred
    restart: unless-stopped
    ports:
      - "127.0.0.1:3100:3100"   # bind only to localhost; TLS-terminate upstream
    environment:
      OPENCRED_PORT: "3100"
      OPENCRED_API_KEY: ${OPENCRED_API_KEY}
      OPENCRED_KEY_PATH: /secrets/issuer-key.pem
      OPENCRED_KEY_LABEL: discom-prod-issuer
      OPENCRED_LOG_LEVEL: info
      # DeDi (optional)
      OPENCRED_DEDI_BASE_URL: https://dedi.global
      OPENCRED_DEDI_AUTH_TYPE: api-key
      OPENCRED_DEDI_API_KEY: ${DEDI_API_KEY}
      OPENCRED_DEDI_NAMESPACE: tpddl
    volumes:
      - /etc/opencred/issuer-key.pem:/secrets/issuer-key.pem:ro
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid,size=64m
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3100/v1/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
```

Always terminate TLS upstream (nginx, Caddy, ALB) — the container speaks plain HTTP intentionally.

### Cloud KMS variants

```bash
# AWS KMS
-e OPENCRED_KMS_PROVIDER=aws \
-e OPENCRED_KMS_KEY_ARN=arn:aws:kms:ap-south-1:111:key/...

# Azure Key Vault
-e OPENCRED_KMS_PROVIDER=azure \
-e OPENCRED_AZURE_KEY_VAULT_URL=https://discom-kv.vault.azure.net \
-e OPENCRED_AZURE_KEY_NAME=opencred-issuer

# GCP Cloud KMS
-e OPENCRED_KMS_PROVIDER=gcp \
-e OPENCRED_GCP_KMS_KEY_NAME=projects/.../cryptoKeyVersions/1
```

Each variant uses the cloud's default credential chain (IAM role, workload identity, ADC). No keys live on disk.

---

## Step 5 — Environment variables reference

| Variable | Required? | Default | Purpose |
|---|---|---|---|
| `OPENCRED_PORT` | No | `3100` | HTTP listen port |
| `OPENCRED_API_KEY` | Yes | — | Bearer token for protected endpoints. Fail-closed if missing. |
| `OPENCRED_DEV_MODE_NO_AUTH` | No | `false` | Disables auth — **dev only**, do not set in production |
| `OPENCRED_LOG_LEVEL` | No | `info` | `fatal/error/warn/info/debug/trace` |
| `OPENCRED_KEY_PATH` | One of these | — | Path to PEM/JWK/PKCS#8/PFX file |
| `OPENCRED_KEY_PASSWORD` | No | — | PFX password |
| `OPENCRED_KEY_LABEL` | No | `server-key` | Human label visible in `GET /v1/keys` |
| `OPENCRED_KMS_PROVIDER` | One of these | `none` | `aws` \| `azure` \| `gcp` \| `none` |
| `OPENCRED_KMS_KEY_ARN` | If aws | — | AWS KMS key ARN |
| `OPENCRED_AZURE_KEY_VAULT_URL` | If azure | — | Azure Key Vault URL |
| `OPENCRED_AZURE_KEY_NAME` | If azure | — | Key name in vault |
| `OPENCRED_GCP_KMS_KEY_NAME` | If gcp | — | Full GCP KMS resource name with version |
| `OPENCRED_BATCH_ROW_LIMIT` | No | `1000` | Max rows per batch CSV |
| `OPENCRED_SESSION_TTL` | No | `14400` | Seconds before ephemeral batch results expire |
| `OPENCRED_CSCA_TRUST_STORE_PATH` | No | — | Directory of CSCA PEMs for DSC verification |
| `OPENCRED_SCHEMA_UPDATE_URL` | No | — | HTTPS manifest for schema updates |
| `OPENCRED_SCHEMA_CACHE_DIR` | No | — | Persistent schema cache directory |
| `OPENCRED_DEDI_BASE_URL` | If revocation | — | DeDi instance endpoint |
| `OPENCRED_DEDI_AUTH_TYPE` | If DeDi | — | `api-key` \| `bearer` |
| `OPENCRED_DEDI_API_KEY` | If api-key | — | DeDi API key |
| `OPENCRED_DEDI_EMAIL` | If bearer | — | DeDi bearer email |
| `OPENCRED_DEDI_PASSWORD` | If bearer | — | DeDi bearer password |
| `OPENCRED_DEDI_NAMESPACE` | If DeDi | — | Default namespace for your DISCOM |
| `OPENCRED_DEDI_TIMEOUT_MS` | No | `10000` | DeDi request timeout (1000–30000) |

---

## Step 6 — Configure DeDi for revocation (optional, recommended)

1. Register a namespace on [dedi.global](https://dedi.global) — typically your DISCOM short code (`tpddl`, `bescom`, etc.).
2. Receive an API key or bearer credentials.
3. Set the `OPENCRED_DEDI_*` env vars above.
4. Ensure the namespace's required registries exist:
   ```bash
   curl -X POST http://localhost:3100/v1/dedi/namespace/ensure \
     -H "Authorization: Bearer $OPENCRED_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"namespace": "tpddl"}'
   ```
   This idempotently creates `vc-revocation-registry`, `public_key_registry`, `schema_registry`, and `context_registry`.

Restart `/v1/health` should now show `"dediConfigured": true`.

---

## Step 7 — Reverse proxy and TLS

Terminate TLS upstream. Minimal nginx site:

```nginx
server {
  listen 443 ssl http2;
  server_name opencred.ies.tpddl.in;

  ssl_certificate     /etc/ssl/ies.tpddl.in.fullchain.pem;
  ssl_certificate_key /etc/ssl/ies.tpddl.in.key;

  client_max_body_size 25m;   # for batch CSV uploads + PDF verify
  proxy_read_timeout 60s;

  location / {
    proxy_pass http://127.0.0.1:3100;
    proxy_set_header Host              $host;
    proxy_set_header X-Forwarded-For   $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

Restrict this domain to internal callers (firewall, mTLS, or VPN). OpenCred is not designed to be exposed to the public internet — it sits behind your DISCOM's API gateway.

The `did.json` for `did:web:ies.tpddl.in` must be served from the **`ies.tpddl.in`** apex (not `opencred.ies.tpddl.in`). Use a separate nginx server block or static hosting for `.well-known/did.json`.

---

## Step 8 — Kubernetes (optional)

If you run Kubernetes, set probes:

```yaml
livenessProbe:
  httpGet: { path: /v1/health, port: 3100 }
  initialDelaySeconds: 10
  periodSeconds: 30
readinessProbe:
  httpGet: { path: /v1/health, port: 3100 }
  initialDelaySeconds: 5
  periodSeconds: 10
```

Mount the signing key from a `Secret` or use the cloud's CSI driver to project KMS credentials.

---

## Production checklist

- [ ] `OPENCRED_API_KEY` rotated quarterly; stored in a secrets manager, never committed
- [ ] Signing key file `chmod 0600`; mount read-only
- [ ] Container runs as non-root (`node` user; verify with `docker exec opencred id`)
- [ ] TLS terminated upstream; container bound to `127.0.0.1`
- [ ] Image pinned to a specific SHA, not `latest`
- [ ] `/v1/health` wired to your orchestrator and to monitoring alerts
- [ ] JSON logs (pino) shipped to your aggregator (ELK, Loki, Datadog)
- [ ] DeDi namespace provisioned and credentials present (if using revocation)
- [ ] `did:web` JSON published, resolvable from the public internet, and validated against `GET https://<domain>/.well-known/did.json`
- [ ] Backups: **none needed** — OpenCred is stateless. Back up only the signing key and DeDi credentials.

---

## Verifying the deployment

```bash
# Health
curl -s http://localhost:3100/v1/health

# Keys loaded
curl -s http://localhost:3100/v1/keys -H "Authorization: Bearer $OPENCRED_API_KEY"

# Schemas available
curl -s http://localhost:3100/v1/schemas -H "Authorization: Bearer $OPENCRED_API_KEY"

# DID resolution end-to-end (proves did:web is reachable)
curl -s -X POST http://localhost:3100/v1/keys/resolve \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"did": "did:web:ies.tpddl.in"}'
```

If all four succeed, you are ready to issue your first credential. Move on to [Issuing Credentials](./issuance.md).

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Container exits immediately with config error | Missing required env var | Check the Zod error in stderr; set the named variable |
| `/v1/health` returns 503, `signingKeyLoaded: false` | Key file unreadable inside container | Re-check mount path and permissions; ensure file owned by readable by uid 1000 |
| All requests return 401 | `Authorization: Bearer …` header missing | Add the header (or set `OPENCRED_DEV_MODE_NO_AUTH=true` in dev) |
| `did:web` resolution fails | `.well-known/did.json` returns redirect, private IP, or non-HTTPS | Serve directly over HTTPS with a public CA cert; no redirects |
| Revocation operations error with `DEDI_NOT_CONFIGURED` | DeDi env vars not set | Set `OPENCRED_DEDI_*` and restart |

---

## References

- [OpenCred — Docker overview](https://opencred.gitbook.io/docs/docker-image/docker)
- [OpenCred — Deployment](https://opencred.gitbook.io/docs/docker-image/deployment)
- [OpenCred — Cloud HSM](https://opencred.gitbook.io/docs/docker-image/cloud-hsm)
- [OpenCred — Observability](https://opencred.gitbook.io/docs/docker-image/observability)
- [OpenCred — Security overview](https://opencred.gitbook.io/docs/security/security)

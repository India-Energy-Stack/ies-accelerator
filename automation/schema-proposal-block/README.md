# Propose-a-Schema inline block (GitBook integration)

Renders the Propose-a-Schema form **natively inside GitBook** — real text boxes on the
page, no redirect to Google Forms.

## Why this exists

GitBook blocks `<iframe>` via its content security policy, and its `{% embed %}` block
degrades a Google Form URL to a grey link card rather than a fillable form. A ContentKit
integration is the only way to render actual input fields inside a GitBook page.

## How it fits the existing pipeline

The block does **not** replace the intake automation — it feeds it. On submit, the
integration POSTs to the existing Google Form's `formResponse` endpoint, so everything
downstream is unchanged:

```
                                   ┌─ this block (inline in GitBook) ─┐
Proposer fills the form on the page ┤                                  ├─► Google Form response
                                   └─ fallback link (new tab) ────────┘          │
                                                                                 ▼
                                                          Apps Script → public GitHub issue
                                                          (email / mobile never included)
```

Contact email and mobile stay private exactly as before: they land in the form's own
responses and are not referenced by the issue builder in `../schema-proposal/Code.gs`.

## Field ids

`src/index.tsx` maps each input to the live form's `entry.<id>`. These were read from the
form's `FB_PUBLIC_LOAD_DATA_`:

| Field | Entry id | Type | Required |
|---|---|---|---|
| Name | `entry.749440514` | Short | Yes |
| Organization | `entry.1066242488` | Short | Yes |
| Contact email | `entry.1931736363` | Short | Yes |
| Contact mobile number | `entry.323624506` | Short | No |
| Use case the proposed schema supports | `entry.896988893` | Short | Yes |
| Description and background | `entry.2091763378` | Paragraph | Yes |
| Schema | `entry.1749605353` | Paragraph | Yes |
| Standards the schema is based on | `entry.1286840799` | Paragraph | No |
| Any additional material | `entry.1174083829` | Paragraph | No |
| GitHub username (optional) | `entry.986421744` | Short | No |

> **If you edit the Google Form, re-check these.** Renaming a question keeps its id, but
> deleting and recreating one mints a **new** id — the old id then silently drops that
> answer instead of erroring. Re-read them with the snippet at the bottom of this file.

Note: the live form marks **Description and background** as *required*, while
`../schema-proposal/README.md` lists it as optional. The block follows the live form.

## Deploy

Requires a GitBook account with permission to publish integrations for the IES org.

1. **Set the org.** In `gitbook-manifest.yaml`, replace `<IES_GITBOOK_ORG_ID>` with the
   IES organization id or subdomain. `visibility: private` keeps the integration
   installable only by IES org members.
2. **Install deps and check types:**
   ```bash
   cd automation/schema-proposal-block && npm install && npm run typecheck
   ```
3. **Authenticate and publish:**
   ```bash
   npx gitbook auth && npx gitbook publish .
   ```
   If publishing fails because the name is taken, change `name:` in the manifest — it
   must be unique across all GitBook integrations — and publish again.
4. **Install it on the space:** in the GitBook space, open the integrations panel and
   install *IES — Propose a Schema*.
5. **Insert the block** on the `propose-a-schema` page: `/` → *Propose a Schema*.
6. **Test end to end:** submit once and confirm (a) a response lands in the form, (b) a
   public issue appears with the `schema-proposal` label, and (c) email and mobile are
   **absent** from that issue. Delete the test issue and response afterwards.

## Re-reading the entry ids

```bash
curl -sL "https://docs.google.com/forms/d/e/<FORM_ID>/viewform" \
  | python3 -c "import sys,re,json; d=json.loads(re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(\[.*?\]);', sys.stdin.read(), re.S).group(1)); [print(f'entry.{e[0]:<12}', f[1]) for f in d[1][1] if f[4] for e in f[4]]"
```

## Limits

- Google may throttle or reject automated `formResponse` posts; the block surfaces an
  error and the page keeps a fallback link to the form itself.
- The block has no CAPTCHA. If it attracts spam, the mitigation is on the intake side
  (Apps Script filtering), since GitBook cannot render a CAPTCHA inline either.

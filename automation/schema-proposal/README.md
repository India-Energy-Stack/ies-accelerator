# Propose-a-Schema intake automation

Community members propose schemas through a **private Google Form**. Every field lands
in a private Google Sheet only the secretariat can see. On each submission, a Google
Apps Script (`Code.gs`) files a **public GitHub issue** in `India-Energy-Stack/ies-accelerator`
containing only the non-sensitive fields.

**Contact email and mobile stay private** — they live only in the responses sheet and are
never written to the public issue.

```
Proposer → Google Form → private Sheet ──(Apps Script)──► public GitHub issue
                              │                              (no email / mobile)
                         email + mobile
                        stay here, private
```

## Who authors the issues?

The issue is created by whatever GitHub account owns the token below — **not** the
proposer. Use a dedicated **bot/service account** (e.g. `ies-bot`) so all proposals are
cleanly authored by it. Proposers need **no GitHub account**. If a proposer optionally
enters their GitHub username on the form, the script `@mention`s them on the issue so
they're notified and can join the thread.

## Form questions (create these exactly)

Create a Google Form with these questions — the **titles must match verbatim**, because
the script reads answers by question title (`Code.gs` → `Q`):

| Question title | Type | Required |
|---|---|---|
| Name | Short answer | Yes |
| Organization | Short answer | Yes |
| Contact email | Short answer | Yes |
| Contact mobile number | Short answer | No |
| Use case the proposed schema supports | Multiple choice / Dropdown | Yes |
| Schema | Paragraph | Yes |
| Standards the schema is based on | Paragraph | No |
| Any additional material | Paragraph | No |
| GitHub username (optional) | Short answer | No |

For "Use case…", use these options: Consumer Energy Passport, Consumer Meter Digest,
Smart Meter Data Exchange, DER Visibility, DISCOM Regulatory Filing, Policy as Code,
P2P Energy Transaction, Other / New use case.

## One-time setup

1. **Create the form** with the questions above (Google Forms). In the form's **Responses**
   tab, click the Sheets icon to create/link a responses spreadsheet.
2. **Open the script**: from that spreadsheet, `Extensions → Apps Script`. Paste the
   contents of `Code.gs` into the project (replace the default `Code.gs`).
3. **Create a GitHub token** (do this yourself; never share or paste it into chat):
   GitHub → Settings → Developer settings → **Fine-grained personal access token**,
   scoped to the `ies-accelerator` repo, with **Issues: Read and write**. Generate it
   while signed in as the bot account so issues are authored by the bot.
4. **Store the token**: in Apps Script, `Project Settings → Script properties → Add`,
   name `GITHUB_TOKEN`, value = the token. (Storing it here keeps it out of the code.)
5. **Install the trigger**: Apps Script `Triggers` (clock icon) → `Add trigger` →
   function `onFormSubmit`, event source **From spreadsheet**, event type **On form submit**.
   Authorize when prompted.
6. **Test**: submit the form once. Confirm a public issue appears in the repo with the
   `schema-proposal` label, and that email/mobile are **absent** from the issue but
   **present** in the responses sheet.
7. **Publish the form URL**: copy the form's public link and paste it in two places —
   - `propose-a-schema.md` (the GitBook page link), and
   - `.github/ISSUE_TEMPLATE/config.yml` (`REPLACE_WITH_FORM_URL`).

## Notes

- Ensure the `schema-proposal` label exists in the repo (Issues → Labels), or drop
  `ISSUE_LABEL` from `Code.gs`.
- Google Forms shows a confirmation message after submit (no custom redirect). If you
  want submitters redirected to a specific URL instead, a form tool like Tally supports
  redirect-on-submit — but its webhooks are a paid feature.
- To change which fields are public, edit the `body` builder in `Code.gs`. Email/mobile
  are deliberately not referenced there.

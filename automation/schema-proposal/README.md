# Propose-a-Schema intake automation

Community members propose schemas through a **private Google Form**. A form-bound Google
Apps Script (`Code.gs`) fires on each submission and files a **public GitHub issue** in
`India-Energy-Stack/ies-accelerator` containing only the non-sensitive fields.

Issue creation is triggered **directly by the form submission** — it does not depend on a
spreadsheet. Optionally link a responses Google Sheet for your own records; Google fills
it independently, as a separate parallel copy that plays no part in issue creation.

**Contact email and mobile stay private** — they are never written to the public issue
(they exist only in the form's own responses, and the optional sheet if you link one).

```
                    ┌─(Apps Script, form-bound)─► public GitHub issue (no email / mobile)
Proposer → Google Form
                    └─(optional, parallel)──────► responses Google Sheet (private records)
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
| Use case the proposed schema supports | Short answer | Yes |
| Schema | Paragraph | Yes |
| Standards the schema is based on | Paragraph | No |
| Any additional material | Paragraph | No |
| GitHub username (optional) | Short answer | No |

"Use case…" is a free-text short answer so proposers can name an existing use case
(Consumer Energy Passport, Consumer Meter Digest, Smart Meter Data Exchange, DER
Visibility, DISCOM Regulatory Filing, Policy as Code, P2P Energy Transaction) or describe
a new one.

## One-time setup

1. **Create the form** with the questions above (Google Forms).
2. **Open the script**: in the **form** editor, click the **⋮ (More)** menu at the top
   right → **Apps Script**. This creates a project bound to the form. Paste the contents
   of `Code.gs` into it (replace the default `Code.gs`).
3. **Create a GitHub token** (do this yourself; never share or paste it into chat):
   GitHub → Settings → Developer settings → **Fine-grained personal access token**,
   scoped to the `ies-accelerator` repo, with **Issues: Read and write**. Generate it
   while signed in as the bot account so issues are authored by the bot.
4. **Store the token**: in Apps Script, `Project Settings → Script properties → Add`,
   name `GITHUB_TOKEN`, value = the token. (Storing it here keeps it out of the code.)
5. **Install the trigger**: Apps Script `Triggers` (clock icon) → `Add trigger` →
   function `onFormSubmit`, event source **From form**, event type **On form submit**.
   Authorize when prompted.
6. **Test**: submit the form once. Confirm a public issue appears in the repo with the
   `schema-proposal` label and that email/mobile are **absent** from it.
7. **(Optional) Link a records sheet**: in the form's **Responses** tab, click the Sheets
   icon to mirror submissions to a private spreadsheet. This is independent of the issue
   flow — issues are created whether or not a sheet is linked.
8. **Publish the form URL**: copy the form's public link and replace the placeholder
   `https://propose-a-schema-form.invalid` in two places —
   - `propose-a-schema.md` (the GitBook page link), and
   - `.github/ISSUE_TEMPLATE/config.yml`.

## Notes

- Ensure the `schema-proposal` label exists in the repo (Issues → Labels), or drop
  `ISSUE_LABEL` from `Code.gs`.
- Google Forms shows a confirmation message after submit (no custom redirect). If you
  want submitters redirected to a specific URL instead, a form tool like Tally supports
  redirect-on-submit — but its webhooks are a paid feature.
- To change which fields are public, edit the `body` builder in `Code.gs`. Email/mobile
  are deliberately not referenced there.

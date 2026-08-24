/**
 * Propose-a-Schema intake → public GitHub issue.
 *
 * Bound to the Google FORM (not a spreadsheet). On each submission it files a
 * PUBLIC issue in the ies-accelerator repo containing only the non-sensitive
 * fields. Contact email and mobile are intentionally NOT included in the issue.
 *
 * Issue creation depends ONLY on the form submission — it does not require a
 * linked Google Sheet. You may still link a responses sheet for your own
 * records; Google populates it independently, as a separate parallel copy that
 * plays no part in this flow.
 *
 * Setup lives in README.md next to this file.
 */

const GITHUB_OWNER = 'India-Energy-Stack';
const GITHUB_REPO = 'ies-accelerator';
const ISSUE_LABEL = 'schema-proposal';

// Exact form question titles. These must match the Google Form question labels
// verbatim — they are the keys used to read each submitted answer.
const Q = {
  name: 'Name',
  organization: 'Organization',
  email: 'Contact email', // captured privately, NOT posted to the public issue
  mobile: 'Contact mobile number', // captured privately, NOT posted to the public issue
  useCase: 'Use case the proposed schema supports',
  existingOrNew: 'Is the proposed schema for an existing use case or a new one?',
  taxonomyCompliant: 'IES taxonomy compliance', // Checkboxes; answer is the ticked option text (blank if not ticked)
  conceptNote: 'Concept note (link)', // captured privately, NOT posted to the public issue
  description: 'Description and background',
  schema: 'Schema',
  standards: 'Standards the schema is based on',
  additional: 'Any additional material',
  githubUser: 'GitHub username (optional)', // if given, proposer is @mentioned on the issue
};

/**
 * Trigger entry point. Install as a form "On form submit" trigger (see README).
 */
function onFormSubmit(e) {
  const values = readFormResponse(e);
  const answer = (title) => (values[title] || '').trim();

  const name = answer(Q.name);
  const org = answer(Q.organization);
  const useCase = answer(Q.useCase);
  const existingOrNew = answer(Q.existingOrNew);
  const description = answer(Q.description);
  const schema = answer(Q.schema);
  const standards = answer(Q.standards);
  const additional = answer(Q.additional);
  const githubUser = answer(Q.githubUser).replace(/^@/, '');

  // Checkboxes question: a non-empty answer means the proposer ticked the box.
  const taxonomyCompliant = answer(Q.taxonomyCompliant) ? 'Yes' : 'Not confirmed';

  const attribution = org ? name + ' (' + org + ')' : name;
  const title = '[Schema proposal] ' + (useCase || 'New schema') + ' — ' + (org || name || 'community');

  const body = [
    '**Proposed by:** ' + (attribution || '—'),
    githubUser ? '**GitHub:** @' + githubUser : '',
    '',
    '**Use case:** ' + (useCase || '—'),
    '**Existing or new use case:** ' + (existingOrNew || '—'),
    '**IES taxonomy compliance:** ' + taxonomyCompliant,
    // Concept note (link) deliberately not referenced — held privately, like email/mobile.
    '',
    '### Description and background',
    description || '—',
    '',
    '### Schema',
    '```yaml',
    schema || '(none provided)',
    '```',
    '',
    '### Standards the schema is based on',
    standards || '—',
    '',
    '### Additional material',
    additional || '—',
    '',
    '---',
    '_Filed automatically from the Propose a Schema form. The proposer\'s contact ' +
      'details are held privately by the IES secretariat and are not shown here._',
  ].join('\n');

  createIssue(title, body, [ISSUE_LABEL]);
}

/**
 * Build a { questionTitle: answer } map from a FORM-bound submit event.
 * Reads directly from the submitted FormResponse, so it needs no spreadsheet.
 * Multi-select answers (arrays) are joined into a comma-separated string.
 */
function readFormResponse(e) {
  const map = {};
  if (!e || !e.response || typeof e.response.getItemResponses !== 'function') {
    throw new Error(
      'No form response on the event — install this as a FORM "On form submit" ' +
      'trigger (event source: From form), not a spreadsheet trigger.'
    );
  }
  const itemResponses = e.response.getItemResponses();
  for (let i = 0; i < itemResponses.length; i++) {
    const item = itemResponses[i];
    // Trimmed: question titles are edited by hand in the Forms UI, where a stray
    // leading/trailing space is invisible but would silently break the lookup in Q
    // — the answer arrives, matches nothing, and drops out of the issue.
    const title = item.getItem().getTitle().trim();
    let value = item.getResponse();
    if (Array.isArray(value)) {
      value = value.join(', ');
    }
    map[title] = value == null ? '' : String(value);
  }
  return map;
}

/**
 * POST a new issue to the GitHub REST API using the token stored in Script Properties.
 */
function createIssue(title, body, labels) {
  const token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) {
    throw new Error('Missing GITHUB_TOKEN — set it in Project Settings → Script properties.');
  }

  const url = 'https://api.github.com/repos/' + GITHUB_OWNER + '/' + GITHUB_REPO + '/issues';
  const response = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    headers: {
      Authorization: 'Bearer ' + token,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
    payload: JSON.stringify({ title: title, body: body, labels: labels }),
    muteHttpExceptions: true,
  });

  const code = response.getResponseCode();
  if (code < 200 || code >= 300) {
    throw new Error('GitHub API error ' + code + ': ' + response.getContentText());
  }
  return JSON.parse(response.getContentText());
}

/**
 * Manual diagnostic — run this from the editor (select `selfTest` → Run) to check the
 * GitHub side in isolation, without submitting the form. It creates a real test issue.
 * On success the created issue URL is logged (Executions tab); on failure the exact
 * GitHub API error is thrown. Delete the test issue afterwards.
 */
function selfTest() {
  const issue = createIssue(
    '[Schema proposal] SELF-TEST — please delete',
    'Diagnostic issue created by selfTest() to verify token + repo access. Safe to close.',
    [ISSUE_LABEL]
  );
  console.log('OK — created ' + issue.html_url);
}

/**
 * Same as selfTest but WITHOUT the label, to isolate a 422 "label does not exist" error.
 * If this succeeds but selfTest() fails, create the `schema-proposal` label in the repo
 * (or remove ISSUE_LABEL from onFormSubmit).
 */
function selfTestNoLabel() {
  const issue = createIssue(
    '[Schema proposal] SELF-TEST (no label) — please delete',
    'Diagnostic issue created by selfTestNoLabel(). Safe to close.',
    []
  );
  console.log('OK — created ' + issue.html_url);
}

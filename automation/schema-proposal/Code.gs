/**
 * Propose-a-Schema intake → public GitHub issue.
 *
 * Bound to the Google Sheet that receives the "Propose a Schema" form responses.
 * On each submission it files a PUBLIC issue in the ies-accelerator repo containing
 * only the non-sensitive fields. Contact email and mobile are intentionally NOT
 * included in the issue — they remain only in this private responses spreadsheet.
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
  schema: 'Schema',
  standards: 'Standards the schema is based on',
  additional: 'Any additional material',
  githubUser: 'GitHub username (optional)', // if given, proposer is @mentioned on the issue
};

/**
 * Trigger entry point. Install as an "On form submit" trigger (see README).
 */
function onFormSubmit(e) {
  const answer = (title) => {
    const cell = e.namedValues && e.namedValues[title];
    return (cell && cell[0] ? String(cell[0]) : '').trim();
  };

  const name = answer(Q.name);
  const org = answer(Q.organization);
  const useCase = answer(Q.useCase);
  const schema = answer(Q.schema);
  const standards = answer(Q.standards);
  const additional = answer(Q.additional);
  const githubUser = answer(Q.githubUser).replace(/^@/, '');

  const attribution = org ? name + ' (' + org + ')' : name;
  const title = '[Schema proposal] ' + (useCase || 'New schema') + ' — ' + (org || name || 'community');

  const body = [
    '**Proposed by:** ' + (attribution || '—'),
    githubUser ? '**GitHub:** @' + githubUser : '',
    '',
    '**Use case:** ' + (useCase || '—'),
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

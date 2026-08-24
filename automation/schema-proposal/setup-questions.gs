/**
 * ONE-TIME setup for the three questions added in Aug 2026 (existing/new use
 * case, IES taxonomy compliance, concept-note link).
 *
 * Run this from the SAME form-bound Apps Script project that holds Code.gs:
 *
 *   1. Paste this file into the project (alongside Code.gs — Apps Script merges
 *      all .gs files into one namespace, so no imports are needed).
 *   2. Select `addNewQuestions` in the toolbar → Run. Authorize when prompted.
 *   3. Select `logEntryIds` → Run, then open Executions (or View → Logs): it
 *      prints one `entry.<id>  <question title>` line per question. Copy the
 *      three new ids into ../schema-proposal-block/src/index.tsx (the
 *      `entry.REPLACE_*` placeholders in FIELDS).
 *   4. Delete this file from the Apps Script project afterwards if you like —
 *      Code.gs is the only file the submit trigger needs.
 *
 * `addNewQuestions` is idempotent: a question whose exact title already exists
 * is skipped, so re-running it never creates duplicates.
 *
 * The titles, options and required flags below must stay in sync with:
 *   - Code.gs → Q (issue builder reads answers by question title), and
 *   - ../schema-proposal-block/src/index.tsx (EXISTING_OR_NEW_OPTIONS,
 *     TAXONOMY_OPTION_TEXT — the inline block POSTs these strings verbatim).
 */

var ANCHOR_TITLE = 'Use case the proposed schema supports';

function addNewQuestions() {
  var form = FormApp.getActiveForm();
  var items = form.getItems();

  var anchorIndex = -1;
  var existingTitles = {};
  for (var i = 0; i < items.length; i++) {
    var title = items[i].getTitle().trim();
    existingTitles[title] = true;
    if (title === ANCHOR_TITLE) {
      anchorIndex = items[i].getIndex();
    }
  }
  if (anchorIndex === -1) {
    throw new Error(
      'Anchor question not found: "' + ANCHOR_TITLE + '". ' +
      'Has it been renamed? Update ANCHOR_TITLE to match, or move the new questions by hand.'
    );
  }

  var insertAt = anchorIndex + 1;

  // 1. Existing or new use case — Multiple choice, required.
  var mcTitle = 'Is the proposed schema for an existing use case or a new one?';
  if (!existingTitles[mcTitle]) {
    var mc = form
      .addMultipleChoiceItem()
      .setTitle(mcTitle)
      .setChoiceValues(['Existing use case', 'New use case'])
      .setRequired(true);
    form.moveItem(mc.getIndex(), insertAt);
    insertAt++;
    Logger.log('Added: ' + mcTitle);
  } else {
    Logger.log('Skipped (already exists): ' + mcTitle);
    insertAt++;
  }

  // 2. IES taxonomy compliance — Checkboxes with a single option, optional.
  var cbTitle = 'IES taxonomy compliance';
  if (!existingTitles[cbTitle]) {
    var cb = form
      .addCheckboxItem()
      .setTitle(cbTitle)
      .setHelpText(
        'The IES term taxonomy: https://india-energy-stack.gitbook.io/docs/schemas/taxonomy'
      )
      .setChoiceValues(['I confirm this submission is compliant with the IES taxonomy'])
      .setRequired(false);
    form.moveItem(cb.getIndex(), insertAt);
    insertAt++;
    Logger.log('Added: ' + cbTitle);
  } else {
    Logger.log('Skipped (already exists): ' + cbTitle);
    insertAt++;
  }

  // 3. Concept note — Short answer for a PUBLIC LINK (deliberately not a File
  // upload: that forces respondents to sign in with a Google account and cannot
  // be submitted through the anonymous inline GitBook block).
  var lnTitle = 'Concept note (link)';
  if (!existingTitles[lnTitle]) {
    var ln = form
      .addTextItem()
      .setTitle(lnTitle)
      .setHelpText(
        'Public link to a concept note on the IES use-case overview template ' +
        '(https://github.com/India-Energy-Stack/ies-accelerator/blob/main/.github/templates/use-case-overview.md). ' +
        'E.g. a Google Doc set to "anyone with the link", or a GitHub link.'
      )
      .setRequired(false);
    form.moveItem(ln.getIndex(), insertAt);
    Logger.log('Added: ' + lnTitle);
  } else {
    Logger.log('Skipped (already exists): ' + lnTitle);
  }

  Logger.log('Done. Now run logEntryIds() and copy the three new entry ids into src/index.tsx.');
}

/**
 * Logs `entry.<id>  <question title>` for every question, by building a
 * prefilled-URL (whose query string carries the real submit ids) and mapping
 * each id back to its question. No response is submitted; nothing is stored.
 */
function logEntryIds() {
  var form = FormApp.getActiveForm();
  var response = form.createResponse();
  var items = form.getItems();
  var answered = []; // question titles in the order they were answered

  items.forEach(function (item) {
    var type = item.getType();
    try {
      if (type === FormApp.ItemType.TEXT) {
        response = response.withItemResponse(item.asTextItem().createResponse('x'));
        answered.push(item.getTitle());
      } else if (type === FormApp.ItemType.PARAGRAPH_TEXT) {
        response = response.withItemResponse(item.asParagraphTextItem().createResponse('x'));
        answered.push(item.getTitle());
      } else if (type === FormApp.ItemType.MULTIPLE_CHOICE) {
        var choices = item.asMultipleChoiceItem().getChoices();
        if (choices.length) {
          response = response.withItemResponse(
            item.asMultipleChoiceItem().createResponse(choices[0].getValue())
          );
          answered.push(item.getTitle());
        }
      } else if (type === FormApp.ItemType.CHECKBOX) {
        var cbChoices = item.asCheckboxItem().getChoices();
        if (cbChoices.length) {
          response = response.withItemResponse(
            item.asCheckboxItem().createResponse([cbChoices[0].getValue()])
          );
          answered.push(item.getTitle());
        }
      }
      // Other item types (section headers, images…) carry no entry id.
    } catch (err) {
      Logger.log(
        'Could not prefill "' + item.getTitle() + '" (' + err + ') — ' +
        'read its id with the curl snippet in ../schema-proposal-block/README.md instead.'
      );
    }
  });

  var url = response.toPrefilledUrl();
  // Prefilled URLs list entry.<id>=… in form order, matching `answered`.
  var ids = [];
  var re = /entry\.(\d+)=/g;
  var m;
  while ((m = re.exec(url)) !== null) {
    ids.push('entry.' + m[1]);
  }

  if (ids.length !== answered.length) {
    Logger.log('Id/question count mismatch — raw prefilled URL:\n' + url);
    return;
  }
  for (var i = 0; i < ids.length; i++) {
    Logger.log(ids[i] + '  ' + answered[i]);
  }
}

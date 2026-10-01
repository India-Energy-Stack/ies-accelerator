import { createIntegration, createComponent } from '@gitbook/runtime';

/**
 * Renders the Propose-a-Schema form natively inside GitBook, and forwards the
 * submission into the existing Google Form.
 *
 * Nothing downstream changes: the form-bound Apps Script still fires on submit
 * and files the public GitHub issue, and contact email / mobile stay private
 * (they live only in the form's own responses, never in the issue).
 *
 * Field ids below were read from the live form's FB_PUBLIC_LOAD_DATA_. If a
 * question is added, removed or recreated in Google Forms, re-read them —
 * recreating a question mints a new entry id and silently drops that answer.
 */
const FORM_ID = '1FAIpQLSfD2U6iY8jEH9M3GpWql5F9A932zQav_POgYi9ehhb36_J6Yg';

const FIELDS = {
    name: 'entry.749440514',
    organization: 'entry.1066242488',
    email: 'entry.1931736363',
    mobile: 'entry.323624506',
    useCase: 'entry.896988893',
    // Added Aug 2026 via ../schema-proposal/setup-questions.gs; ids read from
    // the live form with its logEntryIds().
    existingOrNew: 'entry.2110258648',
    taxonomyCompliant: 'entry.1449425730',
    conceptNote: 'entry.1478660713',
    description: 'entry.2091763378',
    schema: 'entry.1749605353',
    standards: 'entry.1286840799',
    additional: 'entry.1174083829',
    github: 'entry.986421744',
} as const;

type FieldKey = keyof typeof FIELDS;

/**
 * The two choices for "existing vs new use case". The POSTed value MUST match
 * the Google Form multiple-choice option text verbatim.
 *
 * Published-site renderer constraints (found empirically, Aug 2026):
 *  - ContentKit `select` and `checkbox` elements are silently dropped — the
 *    input label renders, the control doesn't. Buttons and textinputs render.
 *  - Between actions, the client rebuilds state from the DOM's BOUND INPUTS
 *    only; state that lives nowhere but the returned state object resets on
 *    the next action. Action-returned state does NOT repopulate a bound
 *    textinput's DOM value either, so button-set choices don't survive to
 *    submit. (Buttons also render full-width and overflow inside `hstack`.)
 * So both choice fields are plain typed textinputs — the one mechanism proven
 * to round-trip — normalized on submit to the exact form option strings.
 */
const EXISTING_USE_CASE = 'Existing use case';
const NEW_USE_CASE = 'New use case';

/**
 * Exact text of the single option on the Google Form's taxonomy-compliance
 * "Checkboxes" question (required). A Checkboxes answer is submitted as its
 * option text, so this string must match that option verbatim.
 */
const TAXONOMY_OPTION_TEXT = 'YES';

/**
 * The declaration a proposer makes by pressing the YES button. Keep in step
 * with the question's help text (../schema-proposal/setup-questions.gs).
 *
 * The YES press has to survive until Submit, and returned state alone doesn't
 * (see the renderer constraints above). So it rides in the action PAYLOAD of
 * the rendered Submit button instead: after YES, render() emits
 * `{ action: 'submit', declared: true }`, and that payload is part of the
 * element tree the client sends back — not state it rebuilds from inputs.
 */
const TAXONOMY_DECLARATION =
    'I hereby declare that the IES term taxonomy was studied before submitting this ' +
    'schema, and that its terms reuse published IES terms or are marked as proposed additions.';

/** Maps a typed answer to the exact form option, or '' if unrecognizable. */
const normalizeExistingOrNew = (value: string): string => {
    const v = value.trim();
    if (/^existing/i.test(v)) return EXISTING_USE_CASE;
    if (/^new/i.test(v)) return NEW_USE_CASE;
    return '';
};

interface State {
    [key: string]: string | boolean;
    name: string;
    organization: string;
    email: string;
    mobile: string;
    useCase: string;
    existingOrNew: string;
    conceptNote: string;
    description: string;
    schema: string;
    standards: string;
    additional: string;
    github: string;
    /** YES pressed. Only drives render(); submit trusts the button payload. */
    declared: boolean;
    error: string;
    submitted: boolean;
}

/** Mirrors the required flags on the live form. */
const REQUIRED: Array<[FieldKey, string]> = [
    ['name', 'Name'],
    ['organization', 'Organization'],
    ['email', 'Contact email'],
    ['useCase', 'Use case'],
    ['existingOrNew', 'Existing or new use case'],
    ['description', 'Description and background'],
    ['schema', 'Schema'],
];

const EMPTY: State = {
    name: '',
    organization: '',
    email: '',
    mobile: '',
    useCase: '',
    existingOrNew: '',
    conceptNote: '',
    description: '',
    schema: '',
    standards: '',
    additional: '',
    github: '',
    declared: false,
    error: '',
    submitted: false,
};

type Action =
    | { action: 'declare' }
    | { action: 'submit'; declared?: boolean }
    | { action: 'reset' };

const schemaProposalBlock = createComponent<{}, State, Action>({
    componentId: 'schema-proposal',
    initialState: EMPTY,

    async action(element, action) {
        if (action.action === 'reset') {
            return { state: { ...EMPTY } };
        }

        if (action.action === 'declare') {
            return { state: { ...element.state, declared: true, error: '' } };
        }

        if (action.action !== 'submit') {
            return;
        }

        const declared = action.declared === true;
        const state: State = { ...element.state, declared };

        const missing = REQUIRED.filter(
            ([key]) => !String(state[key] ?? '').trim(),
        ).map(([, label]) => label);
        if (!declared) {
            missing.push('IES taxonomy compliance (click YES)');
        }

        if (missing.length > 0) {
            return {
                state: { ...state, error: `Please fill in: ${missing.join(', ')}.` },
            };
        }

        // Typed answers are forgiving ('existing', 'NEW', …) but must resolve to
        // one of the two exact form options.
        const existingOrNew = normalizeExistingOrNew(String(state.existingOrNew ?? ''));
        if (!existingOrNew) {
            return {
                state: {
                    ...state,
                    error:
                        'For "existing or new use case", please type ' +
                        `"${EXISTING_USE_CASE}" or "${NEW_USE_CASE}" (just "existing" or "new" works too).`,
                },
            };
        }

        const body = new URLSearchParams();
        for (const [key, entryId] of Object.entries(FIELDS)) {
            // These two are set to the exact form option text and appended
            // separately below — taxonomyCompliant has no input of its own.
            if (key === 'taxonomyCompliant' || key === 'existingOrNew') {
                continue;
            }
            const value = String(state[key as FieldKey] ?? '').trim();
            if (value) {
                body.append(entryId, value);
            }
        }

        body.append(FIELDS.existingOrNew, existingOrNew);

        // Reaching here means YES was pressed. The form question is required:
        // omitting it would make Google reject the response (while still
        // answering HTTP 200).
        body.append(FIELDS.taxonomyCompliant, TAXONOMY_OPTION_TEXT);

        let ok = false;
        try {
            const response = await fetch(
                `https://docs.google.com/forms/d/e/${FORM_ID}/formResponse`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: body.toString(),
                },
            );
            ok = response.ok;
        } catch {
            ok = false;
        }

        if (!ok) {
            return {
                state: {
                    ...state,
                    error:
                        'Sorry — the proposal could not be submitted. Please try again, ' +
                        'or use the fallback link below the form.',
                },
            };
        }

        return { state: { ...EMPTY, submitted: true } };
    },

    async render(element) {
        const state = element.state;

        if (state.submitted) {
            return (
                <block>
                    <vstack>
                        <text style="bold">Thank you — your proposal was submitted.</text>
                        <text>
                            A public tracking issue is being created in the IES issue
                            tracker, where the community will review and discuss it. Your
                            contact details are not included in that issue.
                        </text>
                        <button label="Propose another schema" onPress={{ action: 'reset' }} />
                    </vstack>
                </block>
            );
        }

        return (
            <block>
                <vstack>

                    <input
                        label="Name"
                        element={<textinput state="name" placeholder="Your full name" />}
                    />
                    <input
                        label="Organization"
                        element={
                            <textinput
                                state="organization"
                                placeholder="The organization you represent"
                            />
                        }
                    />
                    <input
                        label="Contact email"
                        hint="Kept private — shared only with the IES secretariat."
                        element={
                            <textinput
                                state="email"
                                placeholder="name@example.org"
                                inputType="email"
                            />
                        }
                    />
                    <input
                        label="Contact mobile number"
                        hint="Optional. Kept private — shared only with the IES secretariat."
                        element={<textinput state="mobile" placeholder="+91 …" />}
                    />
                    <input
                        label="Use case the proposed schema supports"
                        hint="Name an existing use case, or describe a new one."
                        element={
                            <textinput
                                state="useCase"
                                placeholder="e.g. Consumer Energy Passport"
                            />
                        }
                    />
                    <input
                        label="Is the proposed schema for an existing use case or a new one?"
                        hint='Type "Existing" or "New".'
                        element={
                            <textinput
                                state="existingOrNew"
                                placeholder={`${EXISTING_USE_CASE} / ${NEW_USE_CASE}`}
                            />
                        }
                    />
                    <input
                        label="Concept note (link)"
                        hint="Optional. Link to a concept note written on the IES use-case overview template — get it on GitHub or as a Word (.docx) file from the links above this form. Kept private — shared only with the IES secretariat."
                        element={
                            <textinput
                                state="conceptNote"
                                placeholder="https://…  (a Google Doc or OneDrive link that anyone with the link can view)"
                            />
                        }
                    />
                    <input
                        label="Description and background"
                        element={
                            <textinput
                                state="description"
                                placeholder="What problem does this schema solve, and why now?"
                                multiline={true}
                            />
                        }
                    />
                    <input
                        label="Schema"
                        element={
                            <textinput
                                state="schema"
                                placeholder="The proposed schema — attributes, types, structure"
                                multiline={true}
                            />
                        }
                    />
                    <input
                        label="Standards the schema is based on"
                        hint="Optional."
                        element={
                            <textinput
                                state="standards"
                                placeholder="Existing standards or specifications this builds on"
                                multiline={true}
                            />
                        }
                    />
                    <input
                        label="Any additional material"
                        hint="Optional."
                        element={
                            <textinput
                                state="additional"
                                placeholder="Links to documents, examples or references"
                                multiline={true}
                            />
                        }
                    />
                    <input
                        label="GitHub username"
                        hint="Optional — we'll tag you on the tracking issue so you can follow the discussion."
                        element={<textinput state="github" placeholder="octocat" />}
                    />

                    {/* YES is the only valid answer; Submit refuses until it's
                        pressed. See TAXONOMY_DECLARATION for how it survives. */}
                    <text style="bold">IES taxonomy compliance</text>
                    <text>{TAXONOMY_DECLARATION}</text>
                    <text>
                        Taxonomy: india-energy-stack.gitbook.io/docs/schemas/taxonomy — not
                        sure? Run the Before You Propose checklist linked above the form.
                    </text>
                    <button
                        label={state.declared ? '✓ YES — declared' : 'YES'}
                        onPress={{ action: 'declare' }}
                    />
                    {/* Error renders HERE, next to the Submit button, because the
                        user's eyes are on the button when it appears — rendered at
                        the top of the form it sits off-screen and a failed submit
                        looks like "nothing happened". */}
                    {state.error ? (
                        <text style="bold">{`⚠️ ${state.error}`}</text>
                    ) : (
                        <text> </text>
                    )}
                    <button
                        label="Submit proposal"
                        style="primary"
                        onPress={{ action: 'submit', declared: state.declared }}
                    />
                </vstack>
            </block>
        );
    },
});

export default createIntegration({
    components: [schemaProposalBlock],
});

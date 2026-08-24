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
 * The two choices for "existing vs new use case". The option `id` is what gets
 * POSTed, so it MUST match the Google Form multiple-choice option text verbatim.
 */
const EXISTING_OR_NEW_OPTIONS = [
    { id: 'Existing use case', label: 'Existing use case' },
    { id: 'New use case', label: 'New use case' },
];

/**
 * Exact text of the single option on the Google Form's taxonomy-compliance
 * "Checkboxes" question. A Checkboxes answer is submitted as its option text,
 * so this string must match that option verbatim.
 */
const TAXONOMY_OPTION_TEXT = 'I confirm this submission is compliant with the IES taxonomy';

interface State {
    [key: string]: string | boolean;
    name: string;
    organization: string;
    email: string;
    mobile: string;
    useCase: string;
    existingOrNew: string;
    /** ContentKit checkbox state: `false`/`undefined` unticked, the `value` prop ('yes') when ticked. */
    taxonomyCompliant: boolean | string;
    conceptNote: string;
    description: string;
    schema: string;
    standards: string;
    additional: string;
    github: string;
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
    taxonomyCompliant: false,
    conceptNote: '',
    description: '',
    schema: '',
    standards: '',
    additional: '',
    github: '',
    error: '',
    submitted: false,
};

type Action = { action: 'submit' } | { action: 'reset' };

const schemaProposalBlock = createComponent<{}, State, Action>({
    componentId: 'schema-proposal',
    initialState: EMPTY,

    async action(element, action) {
        if (action.action === 'reset') {
            return { state: { ...EMPTY } };
        }

        if (action.action !== 'submit') {
            return;
        }

        const state = element.state;

        const missing = REQUIRED.filter(
            ([key]) => !String(state[key] ?? '').trim(),
        ).map(([, label]) => label);

        if (missing.length > 0) {
            return {
                state: { ...state, error: `Please fill in: ${missing.join(', ')}.` },
            };
        }

        const body = new URLSearchParams();
        for (const [key, entryId] of Object.entries(FIELDS)) {
            // taxonomyCompliant is a boolean in state, but Google Forms expects the
            // exact option text of a Checkboxes question — appended separately below.
            if (key === 'taxonomyCompliant') {
                continue;
            }
            const value = String(state[key as FieldKey] ?? '').trim();
            if (value) {
                body.append(entryId, value);
            }
        }

        // Checkbox → Google Forms "Checkboxes" answer: send the exact option text,
        // and only when actually ticked (guard against the string "false").
        if (state.taxonomyCompliant === true || state.taxonomyCompliant === 'yes') {
            body.append(FIELDS.taxonomyCompliant, TAXONOMY_OPTION_TEXT);
        }

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
                    {state.error ? <text style="bold">{state.error}</text> : <text> </text>}

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
                        element={
                            <select
                                state="existingOrNew"
                                placeholder="Choose one"
                                options={EXISTING_OR_NEW_OPTIONS}
                            />
                        }
                    />
                    <input
                        label="IES taxonomy compliance"
                        hint="Tick to confirm your submission aligns with the IES term taxonomy: india-energy-stack.gitbook.io/docs/schemas/taxonomy"
                        element={
                            <checkbox state="taxonomyCompliant" value="yes" />
                        }
                    />
                    <input
                        label="Concept note (link)"
                        hint="Optional. Link to a concept note on the IES use-case overview template (github.com/India-Energy-Stack/ies-accelerator → .github/templates/use-case-overview.md). Kept private — shared only with the IES secretariat."
                        element={
                            <textinput
                                state="conceptNote"
                                placeholder="https://…  (e.g. a Google Doc set to 'anyone with the link')"
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

                    <button
                        label="Submit proposal"
                        style="primary"
                        onPress={{ action: 'submit' }}
                    />
                </vstack>
            </block>
        );
    },
});

export default createIntegration({
    components: [schemaProposalBlock],
});

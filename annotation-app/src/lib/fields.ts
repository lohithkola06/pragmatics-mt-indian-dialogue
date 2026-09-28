/**
 * The questions annotators answer. Field names match the CSV columns exactly
 * (see REVIEW_COLUMNS and the Stage 2 sheet columns in the Python build script).
 */

export const NOT_APPLICABLE = 'NOT_APPLICABLE';

export type Option = { value: string; label: string; hint?: string };

export type Question = {
  field: string;
  label: string;
  help?: string;
};

// ---------------------------------------------------------------- Stage 1

export const YES_NO_UNSURE: Option[] = [
  { value: 'YES', label: 'Yes' },
  { value: 'NO', label: 'No' },
  { value: 'UNSURE', label: 'Unsure' },
];

export const STAGE1_QUESTIONS: Question[] = [
  {
    field: 'source_is_natural',
    label: 'Is the source utterance natural?',
    help: 'Would some real group of speakers say this? Not "is it exactly how you would say it".',
  },
  {
    field: 'intended_interpretation_is_clear',
    label: 'Is the intended interpretation clear?',
    help: 'Can you tell what the speaker is doing from the dialogue and the situation?',
  },
  {
    field: 'reference_is_valid',
    label: 'Is the reference translation acceptable in Indian English?',
    help: 'Same act, same relationship, same attitude, and something you would send on the speaker’s behalf.',
  },
  {
    field: 'contrastive_is_semantically_close',
    label: 'Is the contrastive translation semantically close?',
    help: 'Same facts, grammatical, and plausible if read on its own.',
  },
  {
    field: 'contrastive_is_pragmatically_wrong',
    label: 'Is the contrastive translation wrong in this context?',
    help: 'If you would accept it after reading the context, answer No. This is the most important check.',
  },
  {
    field: 'primary_label_is_correct',
    label: 'Is the primary phenomenon label correct?',
  },
  {
    field: 'context_label_is_correct',
    label: 'Is the context label correct?',
    help: 'Read the utterance alone first. REQUIRED means the reading changes without context; HELPFUL means only confidence drops.',
  },
  {
    field: 'no_undocumented_cultural_assumption',
    label: 'Is the reading free of undocumented cultural assumptions?',
    help: 'Answer No if the intended reading depends on something the context does not supply.',
  },
];

export const SEVERITY_OPTIONS: Option[] = [
  { value: 'MINOR', label: 'Minor', hint: 'Style weaker; intent and relationship still clear' },
  { value: 'MAJOR', label: 'Major', hint: 'Politeness, act, stance or relationship changes' },
  { value: 'CRITICAL', label: 'Critical', hint: 'Could offend, escalate, or reverse the intent' },
];

export const ACTION_OPTIONS: Option[] = [
  { value: 'ACCEPT', label: 'Accept' },
  { value: 'REVISE', label: 'Revise' },
  { value: 'REJECT', label: 'Reject' },
];

// ---------------------------------------------------------------- Stage 2

export type ScaleQuestion = Question & { allowNA: boolean; group: 'source' | 'meaning' | 'social' | 'overall' };

export const SCALE_OPTIONS: Option[] = [
  { value: '3', label: '3', hint: 'Fully preserved' },
  { value: '2', label: '2', hint: 'Mostly preserved' },
  { value: '1', label: '1', hint: 'Partially preserved' },
  { value: '0', label: '0', hint: 'Not preserved' },
];

export const NA_OPTION: Option = { value: NOT_APPLICABLE, label: 'N/A', hint: 'Does not apply' };

/** In the order the evaluation guidelines ask for: facts first, then social meaning. */
export const STAGE2_QUESTIONS: ScaleQuestion[] = [
  {
    field: 'semantic_adequacy',
    group: 'meaning',
    allowNA: false,
    label: 'Is the translation semantically correct?',
    help: 'Facts only. Ignore tone, politeness and register here. A rude but accurate translation still scores 3.',
  },
  { field: 'speech_act_preservation', group: 'social', allowNA: true, label: 'Is the speech act preserved?', help: 'A request stays a request; an offer stays an offer.' },
  { field: 'politeness_preservation', group: 'social', allowNA: true, label: 'Is politeness preserved?', help: 'Same level of respect and deference toward the listener.' },
  { field: 'formality_preservation', group: 'social', allowNA: true, label: 'Is formality preserved?', help: 'Same register. Casual speech made formal fails too.' },
  { field: 'stance_preservation', group: 'social', allowNA: true, label: 'Is the speaker’s stance preserved?', help: 'Same attitude toward the listener: warm, teasing, reluctant, sceptical…' },
  { field: 'emotion_preservation', group: 'social', allowNA: true, label: 'Is the emotional tone preserved?', help: 'Same feeling, at roughly the same intensity.' },
  { field: 'indirectness_preservation', group: 'social', allowNA: true, label: 'Is indirectness preserved?', help: 'The same amount is left implied. Hints stay hints; clear refusals stay clear.' },
  { field: 'relationship_appropriateness', group: 'social', allowNA: true, label: 'Is the social relationship preserved?', help: 'Would a reader infer the same status and closeness?' },
  { field: 'code_switch_preservation', group: 'social', allowNA: true, label: 'Is the code-switching function preserved?', help: 'Only where the source switches for a reason (authority, intimacy, irony, quotation…). Otherwise N/A.' },
  {
    field: 'translation_naturalness',
    group: 'overall',
    allowNA: false,
    label: 'Is the translation natural Indian English?',
    help: 'Rate the English itself, against Indian English rather than a British or American standard.',
  },
  {
    field: 'overall_pragmatic_preservation',
    group: 'overall',
    allowNA: false,
    label: 'Overall, does the speaker’s social meaning survive?',
    help: 'Your overall reading. Not an average of the rows above.',
  },
];

export const SOURCE_QUESTION: ScaleQuestion = {
  field: 'source_naturalness',
  group: 'source',
  allowNA: false,
  label: 'Is the source utterance natural?',
  help: 'This rates the Hindi or Hinglish, not the translation.',
};

export const ALL_STAGE2_QUESTIONS: ScaleQuestion[] = [SOURCE_QUESTION, ...STAGE2_QUESTIONS];

export const UNCERTAINTY_OPTIONS: Option[] = [
  { value: '', label: 'None' },
  { value: 'UNCERTAIN', label: 'Uncertain', hint: 'You cannot decide' },
  { value: 'MULTIPLE_VALID_INTERPRETATIONS', label: 'Multiple valid readings', hint: 'The item supports more than one' },
];

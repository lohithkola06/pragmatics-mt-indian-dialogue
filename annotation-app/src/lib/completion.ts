import { ALL_STAGE2_QUESTIONS, STAGE1_QUESTIONS } from './fields';
import type { Answers, Stage } from './types';

export type Check = {
  complete: boolean;
  /** Fields still needed, including 'notes' when a note is required but empty. */
  missing: string[];
  noteRequired: boolean;
};

const filled = (value: string | undefined) => value !== undefined && value !== '';

/**
 * Stage 1 is complete when every question, the severity and the action are
 * answered, plus a note whenever something was judged NO or UNSURE or the item
 * is sent back for revision or rejected.
 */
export function checkStage1(values: Answers): Check {
  const missing = STAGE1_QUESTIONS.filter((q) => !filled(values[q.field])).map((q) => q.field);
  for (const field of ['reviewer_severity', 'recommended_action']) {
    if (!filled(values[field])) missing.push(field);
  }
  const noteRequired =
    STAGE1_QUESTIONS.some((q) => values[q.field] === 'NO' || values[q.field] === 'UNSURE') ||
    values.recommended_action === 'REVISE' ||
    values.recommended_action === 'REJECT';
  if (noteRequired && !values.notes?.trim()) missing.push('notes');
  return { complete: missing.length === 0, missing, noteRequired };
}

/**
 * Stage 2 is complete when all twelve dimensions are rated, plus a note
 * whenever any dimension is 0 or 1 or an uncertainty flag is set.
 */
export function checkStage2(values: Answers): Check {
  const missing = ALL_STAGE2_QUESTIONS.filter((q) => !filled(values[q.field])).map((q) => q.field);
  const noteRequired =
    ALL_STAGE2_QUESTIONS.some((q) => values[q.field] === '0' || values[q.field] === '1') ||
    filled(values.uncertainty_label);
  if (noteRequired && !values.notes?.trim()) missing.push('notes');
  return { complete: missing.length === 0, missing, noteRequired };
}

export function checkFor(stage: Stage, values: Answers): Check {
  return stage === 'stage1' ? checkStage1(values) : checkStage2(values);
}

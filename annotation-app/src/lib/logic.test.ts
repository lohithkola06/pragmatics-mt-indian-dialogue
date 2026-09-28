import { describe, expect, it } from 'vitest';
import items from '../generated/items.json';
import meta from '../generated/meta.json';
import { checkStage1, checkStage2 } from './completion';
import { csvField, toCsv } from './csv';
import { ALL_STAGE2_QUESTIONS, STAGE1_QUESTIONS } from './fields';
import { resolveLink } from './mdLinks';
import { buildStage2Order, hashString, itemOf, mulberry32, reconcileOrder, twoBlockOrder } from './order';
import { compareForRestore, createSession, normalizeAnnotatorId, parseBackup, serializeBackup } from './session';
import type { Answers } from './types';

const itemIds = (items as { item_id: string }[]).map((i) => i.item_id);
const FP = meta.dataset_fingerprint;

// ---------------------------------------------------------------- csv

describe('csvField', () => {
  it('leaves plain values unquoted', () => {
    expect(csvField('ANN_01')).toBe('ANN_01');
    expect(csvField('')).toBe('');
    expect(csvField('ठीक है')).toBe('ठीक है');
  });
  it('quotes commas, quotes and line breaks, doubling inner quotes', () => {
    expect(csvField('a, b')).toBe('"a, b"');
    expect(csvField('say "hi"')).toBe('"say ""hi"""');
    expect(csvField('line1\nline2')).toBe('"line1\nline2"');
    expect(csvField('cr\rhere')).toBe('"cr\rhere"');
  });
  it('ends every record with CRLF and writes no BOM', () => {
    const out = toCsv(['a', 'b'], [{ a: '1', b: 'x,y' }]);
    expect(out).toBe('a,b\r\n1,"x,y"\r\n');
    expect(out.charCodeAt(0)).not.toBe(0xfeff);
  });
});

// ---------------------------------------------------------------- completion

const fullStage1 = (): Answers => ({
  ...Object.fromEntries(STAGE1_QUESTIONS.map((q) => [q.field, 'YES'])),
  reviewer_severity: 'MAJOR',
  recommended_action: 'ACCEPT',
});

const fullStage2 = (value = '3'): Answers => Object.fromEntries(ALL_STAGE2_QUESTIONS.map((q) => [q.field, value]));

describe('Stage 1 completion', () => {
  it('is complete when everything is YES and accepted, with no note', () => {
    expect(checkStage1(fullStage1()).complete).toBe(true);
  });
  it('requires every question, severity and action', () => {
    const v = fullStage1();
    delete v.reviewer_severity;
    expect(checkStage1(v).missing).toContain('reviewer_severity');
  });
  it('requires a note for any NO or UNSURE', () => {
    const v = { ...fullStage1(), reference_is_valid: 'UNSURE' };
    expect(checkStage1(v)).toMatchObject({ complete: false, noteRequired: true });
    expect(checkStage1({ ...v, notes: 'reference sounds British' }).complete).toBe(true);
  });
  it('requires a note for REVISE and REJECT', () => {
    expect(checkStage1({ ...fullStage1(), recommended_action: 'REJECT' }).complete).toBe(false);
  });
  it('does not accept a whitespace-only note', () => {
    expect(checkStage1({ ...fullStage1(), recommended_action: 'REVISE', notes: '   ' }).complete).toBe(false);
  });
});

describe('Stage 2 completion', () => {
  it('needs all twelve dimensions', () => {
    expect(ALL_STAGE2_QUESTIONS).toHaveLength(12);
    expect(checkStage2(fullStage2()).complete).toBe(true);
    const v = fullStage2();
    delete v.semantic_adequacy;
    expect(checkStage2(v).missing).toEqual(['semantic_adequacy']);
  });
  it('covers exactly the rating columns of the sheet', () => {
    const rating = meta.stage2_evaluation_columns.filter(
      (c) => !['annotator_id', 'uncertainty_label', 'notes'].includes(c),
    );
    expect(ALL_STAGE2_QUESTIONS.map((q) => q.field).sort()).toEqual([...rating].sort());
  });
  it('requires a note when any dimension is 0 or 1', () => {
    expect(checkStage2({ ...fullStage2(), politeness_preservation: '1' }).noteRequired).toBe(true);
    expect(checkStage2({ ...fullStage2(), politeness_preservation: '0', notes: 'drops Sir' }).complete).toBe(true);
  });
  it('requires a note when an uncertainty flag is set', () => {
    expect(checkStage2({ ...fullStage2(), uncertainty_label: 'UNCERTAIN' }).complete).toBe(false);
  });
  it('treats NOT_APPLICABLE as an answer, not a gap', () => {
    expect(checkStage2({ ...fullStage2(), code_switch_preservation: 'NOT_APPLICABLE' }).complete).toBe(true);
  });
});

// ---------------------------------------------------------------- order

describe('Stage 2 order', () => {
  const order = (annotator: string) => buildStage2Order(itemIds, meta.calibration_items, annotator, FP);

  it('contains every candidate exactly once', () => {
    const o = order('ANN_01');
    expect(o).toHaveLength(itemIds.length * 2);
    expect(new Set(o).size).toBe(o.length);
  });

  it('is deterministic for an annotator', () => {
    expect(order('ANN_01')).toEqual(order('ANN_01'));
  });

  it('differs between annotators after calibration', () => {
    const cal = meta.calibration_items.length * 2;
    expect(order('ANN_01').slice(cal)).not.toEqual(order('ANN_02').slice(cal));
  });

  it('puts the same calibration candidates, in the same order, first for everyone', () => {
    const cal = meta.calibration_items.length * 2;
    const first = order('ANN_01').slice(0, cal);
    expect(order('ANN_02').slice(0, cal)).toEqual(first);
    expect(new Set(first.map(itemOf))).toEqual(new Set(meta.calibration_items));
  });

  it('never places siblings next to each other', () => {
    for (const annotator of ['ANN_01', 'ANN_02', 'ANN_03', 'ANN_17']) {
      const o = order(annotator);
      for (let i = 1; i < o.length; i++) expect(itemOf(o[i])).not.toBe(itemOf(o[i - 1]));
    }
  });

  it('mixes references and contrastives within every block', () => {
    const cal = meta.calibration_items.length;
    const main = itemIds.length - cal;
    for (const annotator of ['ANN_01', 'ANN_02', 'ANN_09']) {
      const o = order(annotator);
      const blocks = [
        o.slice(0, cal),
        o.slice(cal, 2 * cal),
        o.slice(2 * cal, 2 * cal + main),
        o.slice(2 * cal + main),
      ];
      for (const block of blocks) {
        const refs = block.filter((c) => c.endsWith('-A')).length;
        expect(Math.abs(refs - (block.length - refs))).toBeLessThanOrEqual(1);
      }
    }
  });

  it('keeps siblings in different blocks', () => {
    const blocks = twoBlockOrder(['X', 'Y', 'Z', 'W'], mulberry32(7));
    const firstHalf = new Set(blocks.slice(0, 4).map(itemOf));
    expect(firstHalf.size).toBe(4);
  });

  it('reconciles a saved order with added and removed units', () => {
    expect(reconcileOrder(['a', 'b', 'gone'], ['b', 'a', 'new'])).toEqual(['a', 'b', 'new']);
  });

  it('hashes and random numbers are stable', () => {
    expect(hashString('abc')).toBe(hashString('abc'));
    const r = mulberry32(1);
    const x = r();
    expect(x).toBeGreaterThanOrEqual(0);
    expect(x).toBeLessThan(1);
  });
});

// ---------------------------------------------------------------- identity & backup

describe('annotator IDs', () => {
  it('normalises common variants', () => {
    expect(normalizeAnnotatorId('ANN_01')).toBe('ANN_01');
    expect(normalizeAnnotatorId('ann1')).toBe('ANN_01');
    expect(normalizeAnnotatorId(' Ann-7 ')).toBe('ANN_07');
    expect(normalizeAnnotatorId('ann 12')).toBe('ANN_12');
  });
  it('rejects adjudicators, names and zero', () => {
    expect(normalizeAnnotatorId('ADJ_01')).toBeNull();
    expect(normalizeAnnotatorId('Priya')).toBeNull();
    expect(normalizeAnnotatorId('ANN_00')).toBeNull();
    expect(normalizeAnnotatorId('ANN_123')).toBeNull();
  });
});

describe('backups', () => {
  const base = () =>
    createSession({
      stage: 'stage2',
      annotatorId: 'ANN_01',
      region: 'Delhi',
      readinessConfirmed: true,
      order: ['X-A', 'X-B'],
      datasetFingerprint: FP,
      now: '2026-09-01T00:00:00.000Z',
    });

  it('round-trips through JSON', () => {
    const s = base();
    expect(parseBackup(serializeBackup(s))).toEqual(s);
  });

  it('rejects files that are not backups', () => {
    expect(() => parseBackup('not json')).toThrow(/not valid JSON/);
    expect(() => parseBackup('{"kind":"something-else"}')).toThrow(/not a pilot annotation backup/);
  });

  it('warns before replacing newer or larger work', () => {
    const older = base();
    const newer = {
      ...base(),
      updatedAt: '2026-09-02T00:00:00.000Z',
      responses: { 'X-A': { values: fullStage2(), itemHash: 'h', updatedAt: '2026-09-02T00:00:00.000Z' } },
    };
    expect(compareForRestore(newer, older).wouldLoseWork).toBe(true);
    expect(compareForRestore(older, newer).wouldLoseWork).toBe(false);
    expect(compareForRestore(null, older).wouldLoseWork).toBe(false);
  });
});

// ---------------------------------------------------------------- guideline links

describe('guideline links', () => {
  const docs = meta.docs;
  const from = 'benchmark/guidelines/annotation_guidelines.md';

  it('opens synced docs inside the app', () => {
    expect(resolveLink('../schema/label_definitions.md', from, docs)).toEqual({ kind: 'doc', file: 'label_definitions.md' });
    expect(resolveLink('annotator_training.md#part-2', from, docs)).toEqual({ kind: 'doc', file: 'annotator_training.md' });
  });
  it('renders links to researcher files as plain text', () => {
    expect(resolveLink('../pilot/pilot_items_v1.jsonl', from, docs)).toEqual({ kind: 'text' });
    expect(resolveLink('../../docs/project/language_scope_decision.md', from, docs)).toEqual({ kind: 'text' });
  });
  it('keeps web links and in-page anchors', () => {
    expect(resolveLink('https://example.org', from, docs)).toEqual({ kind: 'external', href: 'https://example.org' });
    expect(resolveLink('#scale', from, docs)).toEqual({ kind: 'anchor', id: 'scale' });
  });
});

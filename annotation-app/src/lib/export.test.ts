import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import meta from '../generated/meta.json';
import { buildStage1Csv, buildStage2Csv } from './export';
import type { Response, Unit } from './types';

/*
 * Contract with the Python side. The fixture CSVs are rendered by
 * scripts/build_annotation_app_data.py (render_stage2_csv / render_review_csv)
 * and read by scripts/calculate_agreement.py in the Python test suite. The
 * app's export must reproduce them byte for byte.
 */

const fixtures = new URL('../../../scripts/tests/fixtures/', import.meta.url);
const read = (name: string) => readFileSync(fileURLToPath(new URL(name, fixtures)), 'utf8');

type Fixture = {
  stage2_units: Unit[];
  stage2_ratings: Record<string, Record<string, Record<string, string>>>;
  review_items: string[];
  reviews: Record<string, Record<string, Record<string, string>>>;
};

const fixture = JSON.parse(read('app_export_fixture.json')) as Fixture;

const asResponses = (byUnit: Record<string, Record<string, string>>): Record<string, Response> =>
  Object.fromEntries(
    Object.entries(byUnit).map(([id, values]) => [id, { values, itemHash: 'x', updatedAt: 'x' }]),
  );

describe('Stage 2 export', () => {
  for (const annotator of Object.keys(fixture.stage2_ratings)) {
    it(`reproduces the Python fixture for ${annotator}`, () => {
      const csv = buildStage2Csv(
        fixture.stage2_units,
        asResponses(fixture.stage2_ratings[annotator]),
        annotator,
        meta.stage2_columns,
        meta.stage2_context_columns,
      );
      expect(csv).toBe(read(`app_export_stage2_${annotator}.csv`));
    });
  }

  it('never includes the candidate_type answer key', () => {
    expect(meta.stage2_columns).not.toContain('candidate_type');
  });
});

describe('Stage 1 export', () => {
  for (const reviewer of Object.keys(fixture.reviews)) {
    it(`reproduces the Python fixture for ${reviewer}`, () => {
      const csv = buildStage1Csv(
        fixture.review_items,
        asResponses(fixture.reviews[reviewer]),
        reviewer,
        meta.review_columns,
      );
      expect(csv).toBe(read(`app_export_stage1_${reviewer}.csv`));
    });
  }
});

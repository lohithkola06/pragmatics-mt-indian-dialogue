import { toCsv } from './csv';
import type { Response, Unit } from './types';

/**
 * Stage 2 export: the blind annotation sheet, filled in. One row per unit in
 * the order given (the app passes canonical order), context columns straight
 * from the Python-built sheet, blanks for anything unrated.
 */
export function buildStage2Csv(
  units: Unit[],
  responses: Record<string, Response>,
  annotatorId: string,
  columns: string[],
  contextColumns: string[],
): string {
  const context = new Set(contextColumns);
  const rows = units.map((unit) => {
    const values = responses[unit.candidate_id]?.values ?? {};
    const row: Record<string, string> = {};
    for (const column of columns) {
      if (context.has(column)) row[column] = unit.sheet[column] ?? '';
      else if (column === 'annotator_id') row[column] = annotatorId;
      else row[column] = values[column] ?? '';
    }
    return row;
  });
  return toCsv(columns, rows);
}

/** Stage 1 export: the item review template, one row per item. */
export function buildStage1Csv(
  itemIds: string[],
  responses: Record<string, Response>,
  reviewerId: string,
  columns: string[],
): string {
  const rows = itemIds.map((itemId) => {
    const values = responses[itemId]?.values ?? {};
    const row: Record<string, string> = {};
    for (const column of columns) row[column] = values[column] ?? '';
    row.item_id = itemId;
    row.reviewer_id = reviewerId;
    return row;
  });
  return toCsv(columns, rows);
}

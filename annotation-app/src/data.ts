import itemsJson from './generated/items.json';
import metaJson from './generated/meta.json';
import unitsJson from './generated/stage2_units.json';
import type { DocEntry, Item, Meta, Unit } from './lib/types';

/*
 * Everything the app shows comes from src/generated/, which
 * scripts/build_annotation_app_data.py writes from the pilot JSONL, the app
 * config and the guideline docs. Never edit those files by hand.
 */

export const ITEMS = itemsJson as unknown as Item[];
export const UNITS = unitsJson as unknown as Unit[];
export const META = metaJson as unknown as Meta;

export const ITEM_BY_ID: Record<string, Item> = Object.fromEntries(ITEMS.map((i) => [i.item_id, i]));
export const UNIT_BY_ID: Record<string, Unit> = Object.fromEntries(UNITS.map((u) => [u.candidate_id, u]));

/** Titles and paths of the guideline docs. Their text loads with the viewer. */
export const DOC_ENTRIES: DocEntry[] = META.docs;

/** Candidates of the calibration items, in the order every annotator sees them. */
export const CALIBRATION_COUNT = META.calibration_items.length * 2;

/** Stage 2 is locked until the researcher enables it after Stage 1 revisions. */
export function stage2Available(): boolean {
  if (META.stage2_enabled) return true;
  return import.meta.env.DEV && new URLSearchParams(window.location.search).get('stage2') === '1';
}

export const BREAK_EVERY = 25;
export const BACKUP_NUDGE_AFTER = 10;

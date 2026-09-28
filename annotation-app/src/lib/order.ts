/**
 * Stage 2 presentation order.
 *
 * Each item has two candidates (-A reference, -B contrastive). To stop
 * annotators comparing siblings, the candidates are split into two blocks:
 * block 1 holds one candidate from every item and block 2 the other, and each
 * block is shuffled. Siblings are therefore roughly a block apart and never
 * adjacent. Which candidate goes first is balanced, not a coin flip per item:
 * exactly half the items (rounded up) lead with the reference, so each block
 * mixes good and flawed translations. Independent coin flips can put every
 * reference in block 1, which would give the answer key away.
 *
 * The calibration items come first, in an order shared by every annotator (so
 * the calibration discussion can refer to "candidate 3"). The rest are shuffled
 * per annotator. Both are seeded, so the order is reproducible, and the app
 * saves it once when a session starts.
 */

/** FNV-1a 32-bit hash of a string. */
export function hashString(text: string): number {
  let hash = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193);
  }
  return hash >>> 0;
}

/** Small seeded PRNG returning floats in [0, 1). */
export function mulberry32(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function shuffle<T>(values: T[], random: () => number): T[] {
  const out = [...values];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

export const itemOf = (candidateId: string) => candidateId.replace(/-[AB]$/, '');

export function twoBlockOrder(itemIds: string[], random: () => number): string[] {
  const leadsWithReference = new Set(shuffle(itemIds, random).slice(0, Math.ceil(itemIds.length / 2)));
  const first: string[] = [];
  const second: string[] = [];
  for (const id of itemIds) {
    const aFirst = leadsWithReference.has(id);
    first.push(`${id}-${aFirst ? 'A' : 'B'}`);
    second.push(`${id}-${aFirst ? 'B' : 'A'}`);
  }
  const block1 = shuffle(first, random);
  const block2 = shuffle(second, random);
  // The one place siblings could meet is the block boundary.
  if (block1.length && block2.length > 1 && itemOf(block1[block1.length - 1]) === itemOf(block2[0])) {
    [block2[0], block2[1]] = [block2[1], block2[0]];
  }
  return [...block1, ...block2];
}

export function buildStage2Order(
  itemIds: string[],
  calibrationIds: string[],
  annotatorId: string,
  datasetFingerprint: string,
): string[] {
  const calibration = calibrationIds.filter((id) => itemIds.includes(id));
  const rest = itemIds.filter((id) => !calibration.includes(id));
  const calibrationOrder = twoBlockOrder(calibration, mulberry32(hashString(`calibration|${datasetFingerprint}`)));
  const mainOrder = twoBlockOrder(rest, mulberry32(hashString(`${annotatorId}|${datasetFingerprint}`)));
  return [...calibrationOrder, ...mainOrder];
}

/**
 * Keep a saved order valid if units were added or removed by a later build:
 * drop ids that no longer exist and append new ones at the end.
 */
export function reconcileOrder(saved: string[], current: string[]): string[] {
  const known = new Set(current);
  const kept = saved.filter((id) => known.has(id));
  const seen = new Set(kept);
  return [...kept, ...current.filter((id) => !seen.has(id))];
}

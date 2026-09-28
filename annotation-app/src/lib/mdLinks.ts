import type { DocEntry } from './types';

export type LinkTarget =
  | { kind: 'doc'; file: string }
  | { kind: 'external'; href: string }
  | { kind: 'anchor'; id: string }
  /** A link to something annotators should not browse to (e.g. researcher docs). */
  | { kind: 'text' };

function resolvePath(fromFile: string, relative: string): string {
  const parts = fromFile.split('/').slice(0, -1);
  for (const segment of relative.split('/')) {
    if (segment === '' || segment === '.') continue;
    if (segment === '..') parts.pop();
    else parts.push(segment);
  }
  return parts.join('/');
}

/**
 * Decide what a link inside a guideline doc should do in the app. Links
 * between synced docs open inside the app; web links open in a new tab; links
 * to any other repository file render as plain text, because those files
 * include researcher material such as the pilot items and their answer keys.
 */
export function resolveLink(href: string, fromSourcePath: string, docs: DocEntry[]): LinkTarget {
  if (/^(https?:|mailto:)/i.test(href)) return { kind: 'external', href };
  if (href.startsWith('#')) return { kind: 'anchor', id: href.slice(1) };
  const path = resolvePath(fromSourcePath, href.split('#')[0]);
  const doc = docs.find((d) => d.source_path === path);
  return doc ? { kind: 'doc', file: doc.file } : { kind: 'text' };
}

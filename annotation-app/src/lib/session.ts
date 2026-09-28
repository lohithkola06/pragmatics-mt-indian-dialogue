import { useEffect, useState } from 'react';
import { checkFor } from './completion';
import type { Session, Stage } from './types';

const PREFIX = 'pilot-annotation:v1';
const BACKUP_KIND = 'pilot-annotation-backup';

// ---------------------------------------------------------------- identity

/**
 * Normalise an annotator ID to ANN_NN. Accepts "ann1", "ANN-01", "ann 7" and
 * so on, so a small typo doesn't silently start an empty second session.
 * Returns null for anything that isn't an annotator ID (including ADJ_*).
 */
export function normalizeAnnotatorId(raw: string): string | null {
  const match = raw.trim().match(/^ann[\s_-]*(\d{1,2})$/i);
  if (!match) return null;
  const number = Number(match[1]);
  if (number < 1) return null;
  return `ANN_${String(number).padStart(2, '0')}`;
}

export const sessionKey = (stage: Stage, annotatorId: string) => `${PREFIX}:${stage}:${annotatorId}`;

export const stageLabel = (stage: Stage) => (stage === 'stage1' ? 'Stage 1 · Item review' : 'Stage 2 · Blind rating');

// ---------------------------------------------------------------- creation

export function createSession(args: {
  stage: Stage;
  annotatorId: string;
  region: string;
  readinessConfirmed: boolean;
  order: string[];
  datasetFingerprint: string;
  now?: string;
}): Session {
  const now = args.now ?? new Date().toISOString();
  return {
    version: 1,
    stage: args.stage,
    annotatorId: args.annotatorId,
    region: args.region,
    readinessConfirmed: args.readinessConfirmed,
    datasetFingerprint: args.datasetFingerprint,
    createdAt: now,
    updatedAt: now,
    order: args.order,
    position: 0,
    maxReached: 0,
    responses: {},
    checkpointPassed: false,
    calibrationLocked: false,
    breaksShown: [],
    log: [],
  };
}

export function completedCount(session: Session): number {
  return session.order.filter((id) => {
    const response = session.responses[id];
    return response && checkFor(session.stage, response.values).complete;
  }).length;
}

// ---------------------------------------------------------------- storage

function storage(): Storage | null {
  try {
    return typeof window !== 'undefined' ? window.localStorage : null;
  } catch {
    return null;
  }
}

export function loadSession(stage: Stage, annotatorId: string): Session | null {
  try {
    const raw = storage()?.getItem(sessionKey(stage, annotatorId));
    return raw ? (JSON.parse(raw) as Session) : null;
  } catch {
    return null;
  }
}

/** Returns false when the browser refused the write (full, blocked, private). */
export function saveSession(session: Session): boolean {
  try {
    const store = storage();
    if (!store) return false;
    store.setItem(sessionKey(session.stage, session.annotatorId), JSON.stringify(session));
    return true;
  } catch {
    return false;
  }
}

export type SessionSummary = { stage: Stage; annotatorId: string; completed: number; total: number; updatedAt: string };

export function listSessions(): SessionSummary[] {
  const store = storage();
  if (!store) return [];
  const out: SessionSummary[] = [];
  for (let i = 0; i < store.length; i++) {
    const key = store.key(i);
    if (!key?.startsWith(`${PREFIX}:`)) continue;
    try {
      const session = JSON.parse(store.getItem(key) ?? '') as Session;
      out.push({
        stage: session.stage,
        annotatorId: session.annotatorId,
        completed: completedCount(session),
        total: session.order.length,
        updatedAt: session.updatedAt,
      });
    } catch {
      // ignore anything unreadable
    }
  }
  return out.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

/** Ask the browser not to evict our data under storage pressure (best effort). */
export function requestPersistentStorage(): void {
  try {
    void navigator.storage?.persist?.();
  } catch {
    // unsupported; nothing to do
  }
}

// ---------------------------------------------------------------- backups

export function serializeBackup(session: Session, now = new Date().toISOString()): string {
  return JSON.stringify({ kind: BACKUP_KIND, version: 1, exportedAt: now, session }, null, 2);
}

export function parseBackup(text: string): Session {
  let data: unknown;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error('This file is not valid JSON. Choose the backup file the app downloaded.');
  }
  const envelope = data as { kind?: string; session?: Session };
  const session = envelope?.session;
  if (envelope?.kind !== BACKUP_KIND || !session || session.version !== 1) {
    throw new Error('This file is not a pilot annotation backup.');
  }
  if ((session.stage !== 'stage1' && session.stage !== 'stage2') || !normalizeAnnotatorId(session.annotatorId)) {
    throw new Error('This backup is missing its stage or annotator ID.');
  }
  if (!Array.isArray(session.order) || typeof session.responses !== 'object') {
    throw new Error('This backup is incomplete.');
  }
  return session;
}

export type RestoreCheck = {
  incomingCompleted: number;
  currentCompleted: number;
  /** True when restoring would replace work that looks newer or larger. */
  wouldLoseWork: boolean;
};

export function compareForRestore(current: Session | null, incoming: Session): RestoreCheck {
  const incomingCompleted = completedCount(incoming);
  if (!current) return { incomingCompleted, currentCompleted: 0, wouldLoseWork: false };
  const currentCompleted = completedCount(current);
  const wouldLoseWork = currentCompleted > incomingCompleted || current.updatedAt > incoming.updatedAt;
  return { incomingCompleted, currentCompleted, wouldLoseWork };
}

// ---------------------------------------------------------------- one tab only

/**
 * Detect the same session open in another tab of this browser. Two tabs would
 * overwrite each other's saves, so the newer tab goes read-only. Uses
 * BroadcastChannel; the older tab (earlier `since`) always wins a tie.
 */
export function useOpenElsewhere(key: string | null): boolean {
  const [elsewhere, setElsewhere] = useState(false);
  useEffect(() => {
    setElsewhere(false);
    if (!key || typeof BroadcastChannel === 'undefined') return;
    const channel = new BroadcastChannel('pilot-annotation-tabs');
    const me = `${Date.now()}-${Math.random().toString(36).slice(2)}`;
    const since = Date.now();
    channel.onmessage = (event: MessageEvent) => {
      const message = event.data as { type: string; key: string; from: string; since: number };
      if (message?.key !== key || message.from === me) return;
      if (message.type === 'hello') {
        channel.postMessage({ type: 'busy', key, from: me, since });
      } else if (message.type === 'busy' && message.since <= since) {
        setElsewhere(true);
      }
    };
    channel.postMessage({ type: 'hello', key, from: me, since });
    return () => channel.close();
  }, [key]);
  return elsewhere;
}

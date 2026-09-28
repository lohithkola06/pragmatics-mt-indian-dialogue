import { useMemo, useRef, useState, type FormEvent } from 'react';
import { ITEMS, META, stage2Available } from '../data';
import { buildStage2Order } from '../lib/order';
import {
  compareForRestore,
  createSession,
  listSessions,
  loadSession,
  normalizeAnnotatorId,
  parseBackup,
  stageLabel,
} from '../lib/session';
import type { Session, Stage } from '../lib/types';

type Props = {
  onOpen: (session: Session, isNew: boolean) => void;
  onOpenDocs: (file: string) => void;
};

export function Start({ onOpen, onOpenDocs }: Props) {
  const [rawId, setRawId] = useState('');
  const [region, setRegion] = useState('');
  const [ready, setReady] = useState(false);
  const [stage, setStage] = useState<Stage>('stage1');
  const [error, setError] = useState<string | null>(null);
  const [restoreError, setRestoreError] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const sessions = useMemo(() => listSessions(), []);
  const stage2Open = stage2Available();
  const normalized = normalizeAnnotatorId(rawId);

  function start(event: FormEvent) {
    event.preventDefault();
    if (!normalized) return setError('Enter the ID from your invitation, for example ANN_01.');
    const existing = loadSession(stage, normalized);
    if (existing) return onOpen(existing, false);
    if (!region.trim()) return setError('Add your region or city. It helps interpret regional differences.');
    if (!ready) return setError('Please finish the guidelines and training first, then tick the box.');
    const itemIds = ITEMS.map((i) => i.item_id);
    const order =
      stage === 'stage1'
        ? itemIds
        : buildStage2Order(itemIds, META.calibration_items, normalized, META.dataset_fingerprint);
    onOpen(
      createSession({
        stage,
        annotatorId: normalized,
        region: region.trim(),
        readinessConfirmed: ready,
        order,
        datasetFingerprint: META.dataset_fingerprint,
      }),
      true,
    );
  }

  async function restore(file: File) {
    setRestoreError(null);
    try {
      const incoming = parseBackup(await file.text());
      const current = loadSession(incoming.stage, incoming.annotatorId);
      const check = compareForRestore(current, incoming);
      if (
        check.wouldLoseWork &&
        !window.confirm(
          `This browser already has newer work for ${incoming.annotatorId} (${check.currentCompleted} done, ` +
            `versus ${check.incomingCompleted} in the backup). Replace it with the backup anyway?`,
        )
      ) {
        return;
      }
      onOpen(incoming, false);
    } catch (e) {
      setRestoreError(e instanceof Error ? e.message : 'Could not read that file.');
    } finally {
      if (fileRef.current) fileRef.current.value = '';
    }
  }

  return (
    <div className="stack" style={{ gap: 24 }}>
      <header className="stack" style={{ gap: 10 }}>
        <span className="eyebrow">Pragmatics-preserving MT · pilot annotation</span>
        <h1>Does the translation keep what the speaker meant?</h1>
        <p className="lede">
          You’ll look at short Hindi and Hinglish dialogues and their English translations, and judge whether the
          social meaning survives: respect, directness, attitude, and the relationship between the speakers.
        </p>
      </header>

      <div className="start-grid">
        <form className="card stack" onSubmit={start} noValidate>
          <h2>Start or resume</h2>

          <label className="field">
            Annotator ID
            <span className="hint">From your invitation. Never your name.</span>
            <input
              type="text"
              value={rawId}
              onChange={(e) => {
                setRawId(e.target.value);
                setError(null);
              }}
              placeholder="ANN_01"
              autoComplete="off"
              spellCheck={false}
            />
            {rawId && (
              <span className={normalized ? 'hint' : 'field-error'}>
                {normalized ? `Saved as ${normalized}` : 'Not a valid annotator ID yet'}
              </span>
            )}
          </label>

          <div className="stack" style={{ gap: 8 }}>
            <span style={{ fontWeight: 600, fontSize: 14 }}>Stage</span>
            <div className="stage-pick">
              <label className="stage-card">
                <input type="radio" name="stage" checked={stage === 'stage1'} onChange={() => setStage('stage1')} />
                <span className="inner">
                  <strong>Stage 1 · Item review</strong>
                  <span>Check each of the {ITEMS.length} draft items before anything is rated.</span>
                </span>
              </label>
              <label className="stage-card">
                <input
                  type="radio"
                  name="stage"
                  checked={stage === 'stage2'}
                  disabled={!stage2Open}
                  onChange={() => setStage('stage2')}
                />
                <span className="inner">
                  <strong>Stage 2 · Blind rating</strong>
                  <span>
                    {stage2Open
                      ? `Rate ${META.unit_count} translations, one at a time.`
                      : 'Opens after Stage 1 reviews are in and items are revised.'}
                  </span>
                </span>
              </label>
            </div>
          </div>

          <label className="field">
            Region or city
            <span className="hint">Where your Hindi comes from, for example “Delhi” or “Lucknow, grew up in Pune”.</span>
            <input type="text" value={region} onChange={(e) => setRegion(e.target.value)} autoComplete="off" />
          </label>

          <label className="check">
            <input type="checkbox" checked={ready} onChange={(e) => setReady(e.target.checked)} />
            <span>
              I have read the{' '}
              <button type="button" className="link-btn" onClick={() => onOpenDocs('annotation_guidelines.md')}>
                annotation guidelines
              </button>{' '}
              and worked through the{' '}
              <button type="button" className="link-btn" onClick={() => onOpenDocs('annotator_training.md')}>
                training exercises
              </button>
              .
            </span>
          </label>

          {error && <div className="banner banner-bad">{error}</div>}

          <div className="row">
            <button className="btn btn-primary" type="submit">
              Continue
            </button>
            <span className="muted small">If you already have a session for this ID and stage, it resumes.</span>
          </div>
        </form>

        <aside className="stack">
          <div className="card-flat stack" style={{ gap: 12 }}>
            <h3>Saved in this browser</h3>
            {sessions.length === 0 ? (
              <p className="muted small">Nothing yet. Your work saves here automatically as you go.</p>
            ) : (
              <ul className="session-list">
                {sessions.map((s) => (
                  <li key={`${s.stage}-${s.annotatorId}`}>
                    <span className="who">
                      <strong>
                        {s.annotatorId} · {stageLabel(s.stage)}
                      </strong>
                      <span>
                        {s.completed} of {s.total} done · {new Date(s.updatedAt).toLocaleString()}
                      </span>
                    </span>
                    <button
                      className="btn btn-small"
                      onClick={() => {
                        const session = loadSession(s.stage, s.annotatorId);
                        if (session) onOpen(session, false);
                      }}
                    >
                      Resume
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="card-flat stack" style={{ gap: 10 }}>
            <h3>Switching computer?</h3>
            <p className="muted small">
              Work is stored only in this browser. To move it, download a backup on the old computer and restore it here.
            </p>
            <div className="row">
              <button className="btn btn-small" onClick={() => fileRef.current?.click()}>
                Restore from backup…
              </button>
              <input
                ref={fileRef}
                type="file"
                accept="application/json,.json"
                className="sr-only"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) void restore(file);
                }}
              />
            </div>
            {restoreError && <div className="banner banner-bad small">{restoreError}</div>}
          </div>
        </aside>
      </div>
    </div>
  );
}

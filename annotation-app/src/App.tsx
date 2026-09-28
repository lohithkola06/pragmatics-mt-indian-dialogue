import { lazy, Suspense, useCallback, useEffect, useRef, useState } from 'react';
import {
  BACKUP_NUDGE_AFTER,
  BREAK_EVERY,
  CALIBRATION_COUNT,
  ITEMS,
  ITEM_BY_ID,
  META,
  UNITS,
  UNIT_BY_ID,
} from './data';
import { checkFor } from './lib/completion';
import { downloadText, today } from './lib/download';
import { buildStage1Csv, buildStage2Csv } from './lib/export';
import { NOT_APPLICABLE } from './lib/fields';
import { reconcileOrder } from './lib/order';
import {
  completedCount,
  requestPersistentStorage,
  saveSession,
  serializeBackup,
  sessionKey,
  stageLabel,
  useOpenElsewhere,
} from './lib/session';
import type { Response, Session } from './lib/types';
import { Instructions } from './views/Instructions';
import { BreakScreen, Checkpoint, Finish } from './views/Pauses';
import { Start } from './views/Start';
import { Stage1Task, Stage2Task } from './views/Tasks';

type View = 'start' | 'instructions' | 'task' | 'checkpoint' | 'break' | 'finish';

const LOG_LIMIT = 5000;

const GuidelinesViewer = lazy(() => import('./components/GuidelinesViewer'));

export default function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [view, setView] = useState<View>('start');
  const [resuming, setResuming] = useState(false);
  const [docFile, setDocFile] = useState<string | null>(null);
  const [saveFailed, setSaveFailed] = useState(false);
  const [fingerprintNoticeDismissed, setFingerprintNoticeDismissed] = useState(false);

  const openElsewhere = useOpenElsewhere(session ? sessionKey(session.stage, session.annotatorId) : null);
  const openElsewhereRef = useRef(openElsewhere);
  openElsewhereRef.current = openElsewhere;

  // Persist every change. A tab that lost the race to another tab never writes.
  useEffect(() => {
    if (session && !openElsewhere) setSaveFailed(!saveSession(session));
  }, [session, openElsewhere]);

  // Each screen starts at the top rather than inheriting the last scroll position.
  useEffect(() => {
    window.scrollTo({ top: 0 });
  }, [view]);

  const mutate = useCallback((change: (s: Session) => Session) => {
    if (openElsewhereRef.current) return;
    setSession((prev) => (prev ? change(prev) : prev));
  }, []);

  // ------------------------------------------------------------ opening

  function openSession(incoming: Session, isNew: boolean) {
    const currentIds = incoming.stage === 'stage1' ? ITEMS.map((i) => i.item_id) : UNITS.map((u) => u.candidate_id);
    const order = reconcileOrder(incoming.order, currentIds);
    const clamp = (n: number) => Math.max(0, Math.min(n, order.length - 1));
    setSession({ ...incoming, order, position: clamp(incoming.position), maxReached: clamp(incoming.maxReached) });
    setResuming(!isNew);
    setFingerprintNoticeDismissed(false);
    requestPersistentStorage();
    setView(isNew ? 'instructions' : 'task');
  }

  // ------------------------------------------------------------ answering

  const onAnswer = useCallback(
    (unitId: string, field: string, value: string, log = true) => {
      mutate((s) => {
        const previous = s.responses[unitId];
        const values = { ...(previous?.values ?? {}), [field]: value };
        let itemHash = '';
        if (s.stage === 'stage1') {
          itemHash = ITEM_BY_ID[unitId]?.hash ?? '';
        } else {
          const unit = UNIT_BY_ID[unitId];
          itemHash = unit?.item_hash ?? '';
          // Monolingual Hindi has no switch to judge; record that explicitly.
          if (unit && ITEM_BY_ID[unit.item_id]?.language === 'Hindi') {
            values.code_switch_preservation = NOT_APPLICABLE;
          }
        }
        const now = new Date().toISOString();
        const complete = checkFor(s.stage, values).complete;
        const response: Response = {
          values,
          itemHash,
          updatedAt: now,
          completedAt: previous?.completedAt ?? (complete ? now : undefined),
        };
        const entry = { t: now, unit: unitId, field, from: previous?.values[field] ?? '', to: value };
        return {
          ...s,
          responses: { ...s.responses, [unitId]: response },
          log: log ? [...s.log, entry].slice(-LOG_LIMIT) : s.log,
          updatedAt: now,
        };
      });
    },
    [mutate],
  );

  // ------------------------------------------------------------ navigation

  const goTo = useCallback(
    (position: number) => {
      mutate((s) => ({ ...s, position, maxReached: Math.max(s.maxReached, position) }));
      setView('task');
    },
    [mutate],
  );

  function next() {
    if (!session) return;
    const s = session;
    if (s.stage === 'stage2') {
      const locked = s.position < CALIBRATION_COUNT && s.calibrationLocked;
      const complete = checkFor('stage2', s.responses[s.order[s.position]]?.values ?? {}).complete;
      if (!complete && !locked) return;
      if (s.position === CALIBRATION_COUNT - 1 && !s.checkpointPassed) {
        setView('checkpoint');
        return;
      }
    }
    const nextPosition = s.position + 1;
    if (nextPosition >= s.order.length) {
      setView('finish');
      return;
    }
    if (s.stage === 'stage2' && nextPosition % BREAK_EVERY === 0 && !s.breaksShown.includes(nextPosition)) {
      mutate((x) => ({
        ...x,
        position: nextPosition,
        maxReached: Math.max(x.maxReached, nextPosition),
        breaksShown: [...x.breaksShown, nextPosition],
      }));
      setView('break');
      return;
    }
    goTo(nextPosition);
  }

  function back() {
    if (session && session.position > 0) goTo(session.position - 1);
  }

  function passCheckpoint() {
    mutate((s) => ({
      ...s,
      checkpointPassed: true,
      calibrationLocked: true,
      position: CALIBRATION_COUNT,
      maxReached: Math.max(s.maxReached, CALIBRATION_COUNT),
    }));
    setView('task');
  }

  // ------------------------------------------------------------ downloads

  function downloadCsv(scope: 'all' | 'calibration') {
    if (!session) return;
    const id = session.annotatorId;
    if (session.stage === 'stage1') {
      const csv = buildStage1Csv(ITEMS.map((i) => i.item_id), session.responses, id, META.review_columns);
      downloadText(`pilot-stage1-review_${id}_${today()}.csv`, csv, 'text/csv;charset=utf-8');
      return;
    }
    const calibration = new Set(session.order.slice(0, CALIBRATION_COUNT));
    const units = scope === 'calibration' ? UNITS.filter((u) => calibration.has(u.candidate_id)) : UNITS;
    const csv = buildStage2Csv(units, session.responses, id, META.stage2_columns, META.stage2_context_columns);
    const name = scope === 'calibration' ? 'pilot-stage2-calibration' : 'pilot-stage2-ratings';
    downloadText(`${name}_${id}_${today()}.csv`, csv, 'text/csv;charset=utf-8');
  }

  function downloadBackup() {
    if (!session) return;
    downloadText(
      `pilot-${session.stage}-backup_${session.annotatorId}_${today()}.json`,
      serializeBackup(session),
      'application/json',
    );
    // Recording the backup is bookkeeping, not work, so updatedAt is untouched.
    mutate((s) => ({ ...s, lastBackupAt: new Date().toISOString(), lastBackupCompleted: completedCount(s) }));
  }

  // ------------------------------------------------------------ render

  const done = session ? completedCount(session) : 0;
  const total = session?.order.length ?? 0;
  const sinceBackup = session ? done - (session.lastBackupCompleted ?? 0) : 0;
  const readOnly = openElsewhere;

  return (
    <>
      {session && (
        <header className="app-header">
          <div className="app-header-inner">
            <div className="brand">
              <strong>{stageLabel(session.stage)}</strong>
              <span>
                {session.annotatorId} · pilot annotation
              </span>
            </div>
            <div className="header-progress" aria-label={`${done} of ${total} complete`}>
              <div className="bar">
                <span style={{ width: `${total ? (100 * done) / total : 0}%` }} />
              </div>
              <span className="count">
                {done} / {total} done
              </span>
            </div>
            <div className="header-actions">
              <button className="btn btn-small btn-ghost" onClick={() => setView('instructions')}>
                Instructions
              </button>
              <button className="btn btn-small btn-ghost" onClick={() => setDocFile(META.docs[0]?.file ?? null)}>
                Guidelines
              </button>
              <button className="btn btn-small" onClick={downloadBackup}>
                Backup
              </button>
              <button className="btn btn-small" onClick={() => setView('finish')}>
                Finish &amp; export
              </button>
              <button
                className="btn btn-small btn-ghost"
                onClick={() => {
                  setSession(null);
                  setView('start');
                }}
              >
                Exit
              </button>
            </div>
          </div>
        </header>
      )}

      <main>
        {session && (
          <div className="stack" style={{ gap: 10, marginBottom: 16 }}>
            {openElsewhere && (
              <div className="banner banner-bad">
                <span className="grow">
                  <strong>This session is open in another tab.</strong> This tab is read-only so the two don’t overwrite each
                  other. Close it and keep working in the other one.
                </span>
              </div>
            )}
            {saveFailed && !openElsewhere && (
              <div className="banner banner-bad">
                <span className="grow">
                  <strong>This browser isn’t saving your work.</strong> It may be in private mode or out of space. Download a
                  backup now.
                </span>
                <button className="btn btn-small" onClick={downloadBackup}>
                  Download backup
                </button>
              </div>
            )}
            {session.datasetFingerprint !== META.dataset_fingerprint && !fingerprintNoticeDismissed && (
              <div className="banner banner-info">
                <span className="grow">
                  The pilot items were updated since you started. Anything that changed after you answered it is marked
                  for re-checking.
                </span>
                <button className="btn btn-small" onClick={() => setFingerprintNoticeDismissed(true)}>
                  OK
                </button>
              </div>
            )}
            {view === 'task' && sinceBackup >= BACKUP_NUDGE_AFTER && (
              <div className="banner banner-warn">
                <span className="grow">
                  You’ve completed {sinceBackup} since your last backup. Your work is only in this browser.
                </span>
                <button className="btn btn-small" onClick={downloadBackup}>
                  Download backup
                </button>
              </div>
            )}
          </div>
        )}

        {view === 'start' && <Start onOpen={openSession} onOpenDocs={setDocFile} />}

        {session && view === 'instructions' && (
          <Instructions
            stage={session.stage}
            resuming={resuming}
            onOpenDocs={setDocFile}
            onBegin={() => {
              setResuming(true);
              setView('task');
            }}
          />
        )}

        {session && view === 'task' &&
          (session.stage === 'stage1' ? (
            <Stage1Task session={session} readOnly={readOnly} onAnswer={onAnswer} onGoTo={goTo} onNext={next} onBack={back} />
          ) : (
            <Stage2Task session={session} readOnly={readOnly} onAnswer={onAnswer} onGoTo={goTo} onNext={next} onBack={back} />
          ))}

        {session && view === 'checkpoint' && (
          <Checkpoint
            onDownloadCsv={downloadCsv}
            onDownloadBackup={downloadBackup}
            onContinue={passCheckpoint}
            onBack={() => setView('task')}
          />
        )}

        {session && view === 'break' && (
          <BreakScreen
            done={done}
            total={total}
            sinceBackup={sinceBackup}
            onDownloadBackup={downloadBackup}
            onContinue={() => setView('task')}
          />
        )}

        {session && view === 'finish' && (
          <Finish session={session} onDownloadCsv={downloadCsv} onDownloadBackup={downloadBackup} onGoTo={goTo} />
        )}
      </main>

      {docFile && (
        <Suspense fallback={<div className="viewer" aria-busy="true" />}>
          <GuidelinesViewer initialFile={docFile} onClose={() => setDocFile(null)} />
        </Suspense>
      )}
    </>
  );
}

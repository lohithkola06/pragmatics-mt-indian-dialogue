import { useState } from 'react';
import { CALIBRATION_COUNT, ITEM_BY_ID, META, UNIT_BY_ID } from '../data';
import { checkFor } from '../lib/completion';
import type { Session } from '../lib/types';

type Downloads = {
  onDownloadCsv: (scope: 'all' | 'calibration') => void;
  onDownloadBackup: () => void;
};

// ---------------------------------------------------------------- calibration checkpoint

export function Checkpoint({
  onDownloadCsv,
  onDownloadBackup,
  onContinue,
  onBack,
}: Downloads & { onContinue: () => void; onBack: () => void }) {
  const [confirmed, setConfirmed] = useState(false);
  return (
    <div className="narrow stack pause" style={{ gap: 18 }}>
      <span className="eyebrow">Calibration checkpoint</span>
      <h1>Pause here before you go on</h1>
      <p className="lede">
        You’ve rated the {CALIBRATION_COUNT} calibration candidates. Everyone rates these same ones, so the researcher can
        check that you’re using the scale the same way before the main set.
      </p>

      <div className="card stack">
        <h2>Do these three things</h2>
        <ol className="steps">
          <li>
            <span className="stack" style={{ gap: 8 }}>
              <span>Download your calibration ratings and a backup.</span>
              <span className="row">
                <button className="btn btn-small" onClick={() => onDownloadCsv('calibration')}>
                  Download calibration CSV
                </button>
                <button className="btn btn-small" onClick={onDownloadBackup}>
                  Download backup
                </button>
              </span>
            </span>
          </li>
          <li>
            <span>Send both files. {META.contact_instructions}</span>
          </li>
          <li>
            <span>
              Join the calibration discussion. It’s about how you use the scale, for example what separates a 2 from a 1,
              not about agreeing on answers for particular items.
            </span>
          </li>
        </ol>
      </div>

      <div className="banner banner-info">
        <span className="grow">
          When you continue, your {CALIBRATION_COUNT} calibration ratings <strong>lock</strong>. That keeps a record of what
          you thought before the discussion. If you want to change one, go back now.
        </span>
      </div>

      <label className="check">
        <input type="checkbox" checked={confirmed} onChange={(e) => setConfirmed(e.target.checked)} />
        <span>I’ve sent my calibration files and taken part in the calibration discussion.</span>
      </label>

      <div className="row">
        <button className="btn" onClick={onBack}>
          ← Back to candidate {CALIBRATION_COUNT}
        </button>
        <button className="btn btn-primary" disabled={!confirmed} onClick={onContinue}>
          Lock calibration and continue →
        </button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------- break

export function BreakScreen({
  done,
  total,
  sinceBackup,
  onDownloadBackup,
  onContinue,
}: {
  done: number;
  total: number;
  sinceBackup: number;
  onDownloadBackup: () => void;
  onContinue: () => void;
}) {
  return (
    <div className="narrow stack pause" style={{ gap: 18 }}>
      <span className="eyebrow">Break</span>
      <h1>Good moment for a short break</h1>
      <p className="lede">
        You’ve rated {done} of {total}. Judgements drift when you’re tired, so step away for a few minutes before carrying
        on.
      </p>
      {sinceBackup > 0 && (
        <div className="banner banner-warn">
          <span className="grow">
            You’ve done {sinceBackup} since your last backup. It’s worth downloading one now.
          </span>
          <button className="btn btn-small" onClick={onDownloadBackup}>
            Download backup
          </button>
        </div>
      )}
      <div className="row">
        <button className="btn btn-primary" onClick={onContinue}>
          Continue →
        </button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------- finish

export function Finish({
  session,
  onDownloadCsv,
  onDownloadBackup,
  onGoTo,
}: Downloads & { session: Session; onGoTo: (position: number) => void }) {
  const stage1 = session.stage === 'stage1';
  const noun = stage1 ? 'item' : 'candidate';
  const rows = session.order.map((id, position) => {
    const response = session.responses[id];
    const complete = Boolean(response) && checkFor(session.stage, response.values).complete;
    const currentHash = stage1 ? ITEM_BY_ID[id]?.hash : UNIT_BY_ID[id]?.item_hash;
    const revised = Boolean(response) && response.itemHash !== currentHash;
    return { position, complete, revised };
  });
  const done = rows.filter((r) => r.complete).length;
  const incomplete = rows.filter((r) => !r.complete);
  const revised = rows.filter((r) => r.revised);
  const allDone = incomplete.length === 0;

  return (
    <div className="narrow stack pause" style={{ gap: 18 }}>
      <span className="eyebrow">{stage1 ? 'Stage 1 · Item review' : 'Stage 2 · Blind rating'}</span>
      <h1>{allDone ? 'All done. Thank you.' : 'Almost there'}</h1>
      <p className="lede">
        {done} of {session.order.length} {noun}s complete.
        {allDone ? ' Download your files and send them to the researcher.' : ' You can download what you have so far, or finish the rest first.'}
      </p>

      {!allDone && (
        <div className="card-flat stack" style={{ gap: 10 }}>
          <h3>Not finished yet</h3>
          <div className="jump">
            {incomplete.map((r) => (
              <button
                key={r.position}
                className="chip partial"
                disabled={!stage1 && r.position > session.maxReached}
                onClick={() => onGoTo(r.position)}
              >
                {r.position + 1}
              </button>
            ))}
          </div>
        </div>
      )}

      {revised.length > 0 && (
        <div className="banner banner-warn">
          <span className="grow">
            {revised.length} {noun}
            {revised.length > 1 ? 's were' : ' was'} revised after you answered. Please re-check{' '}
            {revised.slice(0, 8).map((r, i) => (
              <span key={r.position}>
                {i > 0 && ', '}
                <button className="link-btn" onClick={() => onGoTo(r.position)}>
                  {r.position + 1}
                </button>
              </span>
            ))}
            {revised.length > 8 && ' and others'}.
          </span>
        </div>
      )}

      <div className="card stack">
        <h2>Send both files</h2>
        <div className="row">
          <button className="btn btn-primary" onClick={() => onDownloadCsv('all')}>
            Download CSV
          </button>
          <button className="btn" onClick={onDownloadBackup}>
            Download backup (JSON)
          </button>
        </div>
        <p className="muted small">{META.contact_instructions}</p>
      </div>
    </div>
  );
}

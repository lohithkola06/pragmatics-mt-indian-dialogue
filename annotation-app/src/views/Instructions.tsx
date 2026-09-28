import { CALIBRATION_COUNT, DOC_ENTRIES, ITEMS, META } from '../data';
import type { Stage } from '../lib/types';

type Props = {
  stage: Stage;
  resuming: boolean;
  onBegin: () => void;
  onOpenDocs: (file: string) => void;
};

function Stage1() {
  return (
    <>
      <section className="card stack">
        <h2>What you’re doing</h2>
        <p>
          You are checking {ITEMS.length} draft items <em>before</em> anyone rates them. Each item is a short dialogue,
          a good English translation (the <strong>reference</strong>), and a deliberately flawed one (the{' '}
          <strong>contrastive</strong>) that keeps the facts but gets the social meaning wrong. Your review decides which
          items are kept, fixed, or thrown out.
        </p>
      </section>
      <section className="card stack">
        <h2>For each item</h2>
        <ol className="steps">
          <li>
            <span>
              <strong>Read the utterance alone first.</strong> The previous turns start hidden so you can apply the
              cover-the-context test. Form a reading, then reveal the context and see whether it changes.
            </span>
          </li>
          <li>
            <span>
              <strong>Check the translations.</strong> Is the reference something you would send on the speaker’s behalf,
              in natural Indian English? Is the contrastive really wrong <em>in this context</em>?
            </span>
          </li>
          <li>
            <span>
              <strong>Answer the eight questions</strong> and rate how serious the contrastive error is. The item’s own
              severity is hidden on purpose, so this is your independent judgement.
            </span>
          </li>
          <li>
            <span>
              <strong>Recommend</strong> Accept, Revise or Reject. Explain every No, Unsure, Revise and Reject in the
              notes. If the reference isn’t natural Indian English, write a better one in the box provided.
            </span>
          </li>
        </ol>
      </section>
      <section className="card stack">
        <h2>Worth remembering</h2>
        <ul className="rules">
          <li>
            The most valuable thing you can catch is a contrastive translation that is <strong>still acceptable</strong>{' '}
            after reading the context. Answer No to “wrong in this context” and say why.
          </li>
          <li>Judge naturalness for some real group of speakers, not only your own usage. Note regional differences.</li>
          <li>Work on your own. Please don’t discuss specific items with other annotators.</li>
        </ul>
      </section>
    </>
  );
}

function Stage2() {
  return (
    <>
      <section className="card stack">
        <h2>What you’re doing</h2>
        <p>
          You will rate {META.unit_count} English translations, one at a time, on a 0 to 3 scale. You won’t be told
          which translation is which, or anything about how the item was labelled. Just read the dialogue and judge the
          translation in front of you.
        </p>
        <div className="scale-legend">
          <span>
            <b>3</b> fully preserved
          </span>
          <span>
            <b>2</b> mostly
          </span>
          <span>
            <b>1</b> partially
          </span>
          <span>
            <b>0</b> not preserved
          </span>
          <span>
            <b>N/A</b> the dimension doesn’t apply (don’t give 3 instead)
          </span>
        </div>
      </section>
      <section className="card stack">
        <h2>The rules that matter most</h2>
        <ul className="rules">
          <li>
            <strong>Rate semantic correctness on facts alone, first.</strong> A rude but accurate translation still scores 3
            there. The social problems go in the other rows.
          </li>
          <li>Judge naturalness against Indian English, not a British or American standard.</li>
          <li>Write a note whenever you give a 0 or a 1, or use an uncertainty flag.</li>
          <li>
            Rate each candidate on its own terms. You can go back to candidates you’ve already seen, but you can’t skip
            ahead.
          </li>
          <li>Take a break when the app suggests one, roughly every 25 candidates.</li>
          <li>Work on your own. Please don’t discuss specific items with other annotators.</li>
        </ul>
      </section>
      <section className="card stack">
        <h2>Calibration comes first</h2>
        <p>
          The first {CALIBRATION_COUNT} candidates are the same for every annotator. After them the app pauses: download
          your calibration file, send it to the researcher, and join the calibration discussion. It covers how you use
          the scale, not the answers to specific items. Your calibration ratings then lock, and you carry on.
        </p>
      </section>
    </>
  );
}

export function Instructions({ stage, resuming, onBegin, onOpenDocs }: Props) {
  const primaryDoc = stage === 'stage1' ? 'annotation_guidelines.md' : 'human_evaluation_guidelines.md';
  return (
    <div className="narrow stack" style={{ gap: 18 }}>
      <header className="stack" style={{ gap: 8 }}>
        <span className="eyebrow">{stage === 'stage1' ? 'Stage 1 · Item review' : 'Stage 2 · Blind rating'}</span>
        <h1>Before you start</h1>
      </header>

      {stage === 'stage1' ? <Stage1 /> : <Stage2 />}

      <section className="card stack">
        <h2>How saving works</h2>
        <p>
          Everything saves automatically, but <strong>only in this browser on this computer</strong>. Clearing browsing
          data, or using a private window, can lose it. Download a backup from the top bar every so often; the app will
          remind you. When you finish, download <strong>both</strong> the CSV and the backup, and send them to the
          researcher.
        </p>
      </section>

      <section className="card-flat stack" style={{ gap: 10 }}>
        <h3>Full guidelines</h3>
        <p className="muted small">Open these any time from the top bar.</p>
        <div className="doc-links">
          {DOC_ENTRIES.map((d) => (
            <button key={d.file} className={`btn btn-small${d.file === primaryDoc ? ' btn-primary' : ''}`} onClick={() => onOpenDocs(d.file)}>
              {d.title}
            </button>
          ))}
        </div>
      </section>

      <div className="row">
        <button className="btn btn-primary" onClick={onBegin}>
          {resuming ? 'Back to work' : 'Begin'}
        </button>
      </div>
    </div>
  );
}

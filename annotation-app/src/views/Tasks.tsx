import { useEffect, useState } from 'react';
import { ChoiceGroup } from '../components/ChoiceGroup';
import { Dialogue, Situation } from '../components/Dialogue';
import { CALIBRATION_COUNT, ITEM_BY_ID, UNIT_BY_ID } from '../data';
import { checkStage1, checkStage2, type Check } from '../lib/completion';
import {
  ACTION_OPTIONS,
  NA_OPTION,
  NOT_APPLICABLE,
  SCALE_OPTIONS,
  SEVERITY_OPTIONS,
  SOURCE_QUESTION,
  STAGE1_QUESTIONS,
  STAGE2_QUESTIONS,
  UNCERTAINTY_OPTIONS,
  YES_NO_UNSURE,
} from '../lib/fields';
import type { Session } from '../lib/types';

type TaskProps = {
  session: Session;
  readOnly: boolean;
  onAnswer: (unitId: string, field: string, value: string, log?: boolean) => void;
  onGoTo: (position: number) => void;
  onNext: () => void;
  onBack: () => void;
};

const FIELD_NAMES: Record<string, string> = {
  notes: 'a note',
  reviewer_severity: 'severity',
  recommended_action: 'a recommendation',
};

function statusText(check: Check, touched: boolean): { text: string; dot: string } {
  if (check.complete) return { text: 'Complete', dot: 'dot-good' };
  if (!touched) return { text: 'Not started', dot: 'dot-none' };
  const names = check.missing.map((f) => FIELD_NAMES[f] ?? f.replace(/_/g, ' '));
  const shown = names.slice(0, 2).join(', ') + (names.length > 2 ? ` and ${names.length - 2} more` : '');
  return { text: `Still needed: ${shown}`, dot: 'dot-warn' };
}

function BottomNav(props: {
  status: { text: string; dot: string };
  canBack: boolean;
  canNext: boolean;
  nextLabel: string;
  onBack: () => void;
  onNext: () => void;
}) {
  return (
    <nav className="bottom-nav" aria-label="Item navigation">
      <div className="bottom-nav-inner">
        <span className="status" role="status">
          <span className={`status-dot ${props.status.dot}`} />
          {props.status.text}
        </span>
        <button className="btn" onClick={props.onBack} disabled={!props.canBack}>
          ← Back
        </button>
        <button className="btn btn-primary" onClick={props.onNext} disabled={!props.canNext}>
          {props.nextLabel} →
        </button>
      </div>
    </nav>
  );
}

function JumpList(props: {
  session: Session;
  check: (id: string) => Check;
  isEnabled: (position: number) => boolean;
  isLocked?: (position: number) => boolean;
  onGoTo: (position: number) => void;
  noun: string;
}) {
  const { session } = props;
  return (
    <details className="card-flat">
      <summary style={{ cursor: 'pointer', fontWeight: 600 }}>All {props.noun}s</summary>
      <div className="stack" style={{ gap: 10, marginTop: 12 }}>
        <div className="jump">
          {session.order.map((id, position) => {
            const touched = Boolean(session.responses[id]);
            const done = touched && props.check(id).complete;
            const locked = props.isLocked?.(position) ?? false;
            const cls = [
              'chip',
              done ? 'done' : touched ? 'partial' : '',
              position === session.position ? 'current' : '',
              locked ? 'locked' : '',
            ].join(' ');
            return (
              <button
                key={id}
                className={cls}
                disabled={!props.isEnabled(position)}
                onClick={() => props.onGoTo(position)}
                aria-label={`${props.noun} ${position + 1}${done ? ', complete' : touched ? ', started' : ''}`}
                aria-current={position === session.position ? 'step' : undefined}
              >
                {position + 1}
              </button>
            );
          })}
        </div>
        <div className="legend-row">
          <span><span className="status-dot dot-good" />complete</span>
          <span><span className="status-dot dot-warn" />started</span>
          <span><span className="status-dot dot-none" />not started</span>
        </div>
      </div>
    </details>
  );
}

function Notes(props: {
  value: string;
  required: boolean;
  readOnly: boolean;
  onChange: (value: string) => void;
  hint: string;
}) {
  return (
    <label className="field">
      Notes{props.required && <span className="field-error">Required for this item</span>}
      <span className="hint">{props.hint}</span>
      <textarea
        value={props.value}
        readOnly={props.readOnly}
        onChange={(e) => props.onChange(e.target.value)}
      />
    </label>
  );
}

// ---------------------------------------------------------------- Stage 1

export function Stage1Task({ session, readOnly, onAnswer, onGoTo, onNext, onBack }: TaskProps) {
  const itemId = session.order[session.position];
  const item = ITEM_BY_ID[itemId];
  const response = session.responses[itemId];
  const values = response?.values ?? {};
  const touched = Boolean(response);
  const check = checkStage1(values);
  const revised = response && response.itemHash !== item.hash;
  const [contextShown, setContextShown] = useState(false);
  const [explanationShown, setExplanationShown] = useState(false);

  useEffect(() => {
    setContextShown(false);
    setExplanationShown(false);
    window.scrollTo({ top: 0 });
  }, [itemId]);

  const set = (field: string) => (value: string) => onAnswer(itemId, field, value);
  const last = session.position === session.order.length - 1;

  return (
    <>
      <div className="task">
        <div className="task-left">
          <div className="unit-title">
            <h2>
              Item {session.position + 1} <span className="muted">of {session.order.length}</span>
            </h2>
            <span className="row" style={{ gap: 6 }}>
              <span className="tag">{item.item_id}</span>
              {item.minimal_pair && <span className="tag">minimal pair</span>}
            </span>
          </div>

          {revised && (
            <div className="banner banner-warn">
              <span className="grow">
                <strong>This item was revised after you answered.</strong> Please re-check your answers.
              </span>
            </div>
          )}

          <div className="card stack">
            {!contextShown && (
              <div className="context-cover">
                <span>
                  {item.context.length === 0
                    ? 'This item has no previous turns.'
                    : `${item.context.length} previous turn${item.context.length > 1 ? 's' : ''} hidden. Read the utterance alone first.`}
                </span>
                {item.context.length > 0 && (
                  <button className="btn btn-small" onClick={() => setContextShown(true)}>
                    Reveal context
                  </button>
                )}
              </div>
            )}
            <Dialogue item={item} showContext={contextShown} />
            <Situation item={item} />
          </div>

          <div className="card stack">
            <dl className="translation">
              {item.reference_translations.map((ref, i) => (
                <div key={`r${i}`} style={{ display: 'contents' }}>
                  <dt>{i === 0 ? 'Reference' : `Reference ${i + 1}`}</dt>
                  <dd>
                    “{ref}”
                    {i === 0 && (
                      <>
                        {' '}
                        <span className="tag tag-accent">rated in Stage 2</span>
                      </>
                    )}
                  </dd>
                </div>
              ))}
              {item.acceptable_variants.map((variant, i) => (
                <div key={`v${i}`} style={{ display: 'contents' }}>
                  <dt>Also OK</dt>
                  <dd>“{variant}”</dd>
                </div>
              ))}
              <dt>Contrastive</dt>
              <dd className="contrastive">
                “{item.contrastive_translation}” <span className="tag">{item.contrastive_error_category}</span>
              </dd>
            </dl>
            <div className="stack" style={{ gap: 6 }}>
              <span className="small">
                <strong>Must preserve:</strong> {item.preservation_requirement}
              </span>
              {explanationShown ? (
                <span className="small muted">
                  <strong>Author’s explanation of the error:</strong> {item.contrastive_error}
                </span>
              ) : (
                <button className="link-btn small" style={{ alignSelf: 'flex-start' }} onClick={() => setExplanationShown(true)}>
                  Show the author’s explanation (form your own view first)
                </button>
              )}
            </div>
          </div>

          <div className="card-flat">
            <dl className="label-grid">
              {(
                [
                  ['Primary phenomenon', item.primary_phenomenon],
                  ['Speech act', item.speech_act],
                  ['Politeness', item.politeness_level],
                  ['Formality', item.formality_level],
                  ['Stance', item.stance],
                  ['Emotion', item.emotion],
                  ['Indirectness', item.indirectness],
                  ['Code-switch function', item.code_switch_function ?? '(none: monolingual)'],
                  ['Context', item.context_status],
                ] as [string, string][]
              ).map(([term, value]) => (
                <div key={term}>
                  <dt>{term}</dt>
                  <dd>
                    <span className="tag">{value}</span>
                  </dd>
                </div>
              ))}
            </dl>
            {item.context_explanation && (
              <p className="small muted" style={{ marginTop: 10 }}>
                <strong>Why the context label:</strong> {item.context_explanation}
              </p>
            )}
          </div>
        </div>

        <div className="task-right">
          <div className="card">
            {STAGE1_QUESTIONS.map((q) => (
              <ChoiceGroup
                key={q.field}
                label={q.label}
                help={q.help}
                options={YES_NO_UNSURE}
                value={values[q.field] ?? ''}
                onChange={set(q.field)}
                disabled={readOnly}
                missing={touched && check.missing.includes(q.field)}
              />
            ))}
            <ChoiceGroup
              label="How serious is the contrastive error?"
              help="Your own rating. The item’s severity label is hidden so this stays independent."
              options={SEVERITY_OPTIONS}
              value={values.reviewer_severity ?? ''}
              onChange={set('reviewer_severity')}
              disabled={readOnly}
              missing={touched && check.missing.includes('reviewer_severity')}
            />
            <ChoiceGroup
              label="Your recommendation"
              options={ACTION_OPTIONS}
              value={values.recommended_action ?? ''}
              onChange={set('recommended_action')}
              disabled={readOnly}
              missing={touched && check.missing.includes('recommended_action')}
            />
          </div>

          <div className="card stack">
            <label className="field">
              A better reference in Indian English <span className="hint">Optional. Fill in when the reference doesn’t sound natural in Indian English.</span>
              <textarea
                value={values.suggested_indian_english_reference ?? ''}
                readOnly={readOnly}
                style={{ minHeight: 60 }}
                onChange={(e) => onAnswer(itemId, 'suggested_indian_english_reference', e.target.value, false)}
              />
            </label>
            <Notes
              value={values.notes ?? ''}
              required={check.noteRequired && !values.notes?.trim()}
              readOnly={readOnly}
              onChange={(v) => onAnswer(itemId, 'notes', v, false)}
              hint="Explain every No, Unsure, Revise and Reject. Be specific: say what you would expect instead."
            />
          </div>

          <JumpList
            session={session}
            noun="item"
            check={(id) => checkStage1(session.responses[id]?.values ?? {})}
            isEnabled={() => true}
            onGoTo={onGoTo}
          />
        </div>
      </div>

      <BottomNav
        status={statusText(check, touched)}
        canBack={session.position > 0}
        canNext
        nextLabel={last ? 'Finish' : 'Next'}
        onBack={onBack}
        onNext={onNext}
      />
    </>
  );
}

// ---------------------------------------------------------------- Stage 2

export function Stage2Task({ session, readOnly, onAnswer, onGoTo, onNext, onBack }: TaskProps) {
  const unitId = session.order[session.position];
  const unit = UNIT_BY_ID[unitId];
  const item = ITEM_BY_ID[unit.item_id];
  const response = session.responses[unitId];
  const values = response?.values ?? {};
  const touched = Boolean(response);
  const check = checkStage2(values);
  const hindi = item.language === 'Hindi';
  const inCalibration = session.position < CALIBRATION_COUNT;
  const locked = inCalibration && session.calibrationLocked;
  const disabled = readOnly || locked;
  const revised = response && response.itemHash !== unit.item_hash;
  const last = session.position === session.order.length - 1;

  useEffect(() => {
    window.scrollTo({ top: 0 });
  }, [unitId]);

  const set = (field: string) => (value: string) => onAnswer(unitId, field, value);
  const optionsFor = (allowNA: boolean) => (allowNA ? [...SCALE_OPTIONS, NA_OPTION] : SCALE_OPTIONS);
  const missing = (field: string) => touched && check.missing.includes(field);
  const groups: { title: string; fields: typeof STAGE2_QUESTIONS }[] = [
    { title: 'Meaning', fields: STAGE2_QUESTIONS.filter((q) => q.group === 'meaning') },
    { title: 'Social meaning', fields: STAGE2_QUESTIONS.filter((q) => q.group === 'social') },
    { title: 'Overall', fields: STAGE2_QUESTIONS.filter((q) => q.group === 'overall') },
  ];

  return (
    <>
      <div className="task">
        <div className="task-left">
          <div className="unit-title">
            <h2>
              Candidate {session.position + 1} <span className="muted">of {session.order.length}</span>
            </h2>
            {inCalibration && <span className="tag tag-accent">calibration</span>}
          </div>

          {locked && (
            <div className="banner banner-info">
              <span className="grow">
                <strong>Calibration is locked.</strong> These ratings were made before the calibration discussion and can’t
                be changed.
              </span>
            </div>
          )}
          {revised && !locked && (
            <div className="banner banner-warn">
              <span className="grow">
                <strong>This item was revised after you rated it.</strong> Please re-check your ratings.
              </span>
            </div>
          )}

          <div className="card stack">
            <Dialogue item={item} />
            <Situation item={item} />
          </div>

          <div className="candidate">
            <div className="candidate-label">Translation to rate</div>
            <div className="candidate-text">“{unit.sheet.candidate_translation}”</div>
          </div>
        </div>

        <div className="task-right">
          <div className="card-flat">
            <div className="scale-legend">
              <span><b>3</b> fully preserved</span>
              <span><b>2</b> mostly</span>
              <span><b>1</b> partially</span>
              <span><b>0</b> not preserved</span>
              <span><b>N/A</b> doesn’t apply</span>
            </div>
          </div>

          <div className="card">
            {groups.map((group) => (
              <div key={group.title}>
                <div className="group-title">{group.title}</div>
                {group.fields.map((q) => {
                  const lockedNA = q.field === 'code_switch_preservation' && hindi;
                  return (
                    <ChoiceGroup
                      key={q.field}
                      label={q.label}
                      help={lockedNA ? 'This utterance is monolingual Hindi, so there is no switch to judge.' : q.help}
                      options={optionsFor(q.allowNA)}
                      value={lockedNA ? NOT_APPLICABLE : (values[q.field] ?? '')}
                      onChange={set(q.field)}
                      disabled={disabled || lockedNA}
                      missing={!lockedNA && missing(q.field)}
                      className={q.field === 'semantic_adequacy' ? 'facts-first' : undefined}
                    />
                  );
                })}
              </div>
            ))}
          </div>

          <div className="card">
            <div className="group-title">About the source</div>
            <ChoiceGroup
              label={SOURCE_QUESTION.label}
              help={SOURCE_QUESTION.help}
              options={optionsFor(false)}
              value={values[SOURCE_QUESTION.field] ?? ''}
              onChange={set(SOURCE_QUESTION.field)}
              disabled={disabled}
              missing={missing(SOURCE_QUESTION.field)}
            />
          </div>

          <div className="card stack">
            <ChoiceGroup
              label="Uncertainty"
              help="Optional. Use a flag instead of guessing, and say why in the notes."
              options={UNCERTAINTY_OPTIONS}
              value={values.uncertainty_label ?? ''}
              onChange={set('uncertainty_label')}
              disabled={disabled}
            />
            <Notes
              value={values.notes ?? ''}
              required={check.noteRequired && !values.notes?.trim()}
              readOnly={disabled}
              onChange={(v) => onAnswer(unitId, 'notes', v, false)}
              hint="Needed whenever you give a 0 or 1, or set an uncertainty flag. Say what changed and why."
            />
          </div>

          <JumpList
            session={session}
            noun="candidate"
            check={(id) => checkStage2(session.responses[id]?.values ?? {})}
            isEnabled={(position) => position <= session.maxReached}
            isLocked={(position) => position < CALIBRATION_COUNT && session.calibrationLocked}
            onGoTo={onGoTo}
          />
        </div>
      </div>

      <BottomNav
        status={locked ? { text: 'Locked after calibration', dot: 'dot-good' } : statusText(check, touched)}
        canBack={session.position > 0}
        canNext={check.complete || locked}
        nextLabel={last ? 'Finish' : 'Next'}
        onBack={onBack}
        onNext={onNext}
      />
    </>
  );
}

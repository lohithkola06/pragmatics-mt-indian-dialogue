import type { Item } from '../lib/types';

const humanize = (code: string) =>
  code.toLowerCase().replace(/_/g, ' ').replace(/^\w/, (c) => c.toUpperCase());

const STATUS: Record<string, string> = {
  SPEAKER_HIGHER: 'Higher than listener',
  SPEAKER_LOWER: 'Lower than listener',
  EQUAL: 'Equal',
  UNKNOWN: 'Unknown',
};

/** The previous turns and the utterance to translate. */
export function Dialogue({ item, showContext = true }: { item: Item; showContext?: boolean }) {
  return (
    <div className="dialogue">
      {showContext &&
        (item.context.length === 0 ? (
          <p className="no-context">No previous turns. This utterance stands on its own.</p>
        ) : (
          item.context.map((turn) => (
            <div className="turn" key={turn.turn_id}>
              <div className="turn-role">{turn.speaker_role}</div>
              <div className="turn-text" lang="hi-Latn">
                {turn.text}
              </div>
            </div>
          ))
        ))}
      <div className="turn turn--source">
        <div className="turn-role">{item.source_utterance.speaker_role} →</div>
        <div>
          <div className="turn-text" lang="hi-Latn">
            {item.source_utterance.text}
          </div>
          <div className="gloss">gloss: {item.literal_gloss}</div>
        </div>
      </div>
    </div>
  );
}

/** Who is talking to whom. Shown in both stages; it is not an answer key. */
export function Situation({ item }: { item: Item }) {
  const rows: [string, string][] = [
    ['Speaker', item.source_utterance.speaker_role],
    ['Listener', item.listener_role],
    ['Relationship', humanize(item.relationship)],
    ['Speaker status', STATUS[item.relative_status] ?? humanize(item.relative_status)],
    ['Familiarity', humanize(item.familiarity)],
    ['Language', item.language],
  ];
  return (
    <dl className="situation">
      {rows.map(([term, value]) => (
        <div key={term}>
          <dt>{term}</dt>
          <dd>{value}</dd>
        </div>
      ))}
    </dl>
  );
}

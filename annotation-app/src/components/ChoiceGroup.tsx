import { useId } from 'react';
import type { Option } from '../lib/fields';

type Props = {
  label: string;
  help?: string;
  options: Option[];
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  missing?: boolean;
  className?: string;
};

/** A labelled radio group rendered as segmented buttons. Arrow keys move within it. */
export function ChoiceGroup({ label, help, options, value, onChange, disabled, missing, className }: Props) {
  const id = useId();
  const selected = options.find((o) => o.value === value);
  return (
    <div className={`q${missing ? ' q-missing' : ''}${className ? ` ${className}` : ''}`}>
      <div className="q-head">
        <span className="q-label" id={`${id}-label`}>
          {label}
        </span>
        {help && <span className="q-help">{help}</span>}
      </div>
      <div className="choice-options" role="radiogroup" aria-labelledby={`${id}-label`}>
        {options.map((option) => (
          <label key={option.value} className={`opt${option.value === 'NOT_APPLICABLE' ? ' opt-na' : ''}`} title={option.hint}>
            <input
              type="radio"
              name={id}
              value={option.value}
              checked={value === option.value}
              disabled={disabled}
              onChange={() => onChange(option.value)}
            />
            <span>{option.label}</span>
          </label>
        ))}
      </div>
      {selected?.hint && <div className="choice-hint">{selected.hint}</div>}
    </div>
  );
}

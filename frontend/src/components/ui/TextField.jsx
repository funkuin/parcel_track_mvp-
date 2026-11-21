import React, { useId } from 'react';

export default function TextField({ label, error, id, className = '', ...props }) {
  const generatedId = useId();
  const fieldId = id ?? generatedId;
  const errorId = `${fieldId}-error`;

  return (
    <div className={`field ${className}`.trim()}>
      <label className="field-label" htmlFor={fieldId}>{label}</label>
      <input
        id={fieldId}
        className={`field-input ${error ? 'field-input--error' : ''}`}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? errorId : undefined}
        {...props}
      />
      {error && <span className="field-error" id={errorId} role="alert">{error}</span>}
    </div>
  );
}
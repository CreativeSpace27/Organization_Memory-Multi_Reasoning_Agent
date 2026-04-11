import { useState } from "react";

export default function InputBox({ onSend, loading }) {
  const [value, setValue] = useState("");

  const handleSubmit = () => {
    if (!value.trim() || loading) return;
    onSend(value.trim());
    setValue("");
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="input-wrapper">
      <div className="input-box">
        <textarea
          className="input-field"
          placeholder="Ask why a decision was made… e.g. Why did we choose PostgreSQL?"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKey}
          rows={1}
          disabled={loading}
        />
        <button
          className={`send-btn ${loading ? "send-loading" : ""}`}
          onClick={handleSubmit}
          disabled={loading || !value.trim()}
          aria-label="Send"
        >
          {loading ? (
            <span className="btn-spinner" />
          ) : (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          )}
        </button>
      </div>
      <p className="input-hint">Press Enter to send · Shift+Enter for new line</p>
    </div>
  );
}
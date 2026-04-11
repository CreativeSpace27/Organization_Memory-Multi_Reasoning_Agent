import Message from "./message";

export default function Chat({ messages, loading, chatEndRef }) {
  if (messages.length === 0 && !loading) {
    return (
      <div className="empty-state">
        <div className="empty-icon">⬡</div>
        <h2 className="empty-title">Reasoning Engine Ready</h2>
        <p className="empty-desc">
          Ask any question about your organization's decisions, architecture choices,
          or strategic reasoning. The engine will trace through your memory corpus to
          explain the <em>why</em>.
        </p>
        <div className="empty-hints">
          <span className="hint-tag">meetings</span>
          <span className="hint-tag">slack threads</span>
          <span className="hint-tag">documents</span>
          <span className="hint-tag">rfcs</span>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-list">
      {messages.map((msg, i) => (
        <Message key={i} message={msg} />
      ))}
      {loading && (
        <div className="thinking-row">
          <div className="thinking-bubble">
            <span className="thinking-dot" />
            <span className="thinking-dot" />
            <span className="thinking-dot" />
            <span className="thinking-text">Reasoning through memory corpus…</span>
          </div>
        </div>
      )}
      <div ref={chatEndRef} />
    </div>
  );
}
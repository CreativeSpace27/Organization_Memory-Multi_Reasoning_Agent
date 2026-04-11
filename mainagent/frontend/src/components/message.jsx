function getSourceLabel(src) {
  if (!src) return "source";
  const lower = src.toLowerCase();
  if (lower.includes("slack")) return "slack";
  if (lower.includes("meeting")) return "meeting";
  if (lower.includes("doc")) return "document";
  if (lower.includes("rfc")) return "rfc";
  if (lower.includes("txt")) return "document";
  // Extract filename
  const parts = src.split("/");
  return parts[parts.length - 1].replace(/\.[^.]+$/, "");
}

function getSourceColor(label) {
  const map = {
    slack: "chip-slack",
    meeting: "chip-meeting",
    document: "chip-doc",
    rfc: "chip-rfc",
  };
  return map[label] || "chip-default";
}

function dedupeSourceFiles(sources) {
  const seen = new Set();
  return sources.filter((s) => {
    const key = s.source + "|" + s.decision;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export default function Message({ message }) {
  if (message.role === "user") {
    return (
      <div className="msg-row msg-user">
        <div className="msg-bubble user-bubble">
          <span className="msg-text">{message.text}</span>
        </div>
        <div className="avatar user-avatar">U</div>
      </div>
    );
  }

  const dedupedSources = dedupeSourceFiles(message.sources || []);
  const uniqueFiles = [...new Set(dedupedSources.map((s) => s.source).filter(Boolean))];
//   const decisions = [...new Set(dedupedSources.map((s) => s.decision).filter(Boolean))];

  return (
    <div className="msg-row msg-ai">
      <div className="avatar ai-avatar">⬡</div>
      <div className={`msg-bubble ai-bubble ${message.error ? "error-bubble" : ""}`}>
        {/* Answer text */}
        <p className="ai-answer-text">{message.text}</p>

        {/* Sources section */}
        {dedupedSources.length > 0 && (
          <div className="sources-section">
            <div className="sources-header">
              <span className="sources-label">Sources</span>
              <div className="source-chips">
                {uniqueFiles.map((file, i) => {
                  const label = getSourceLabel(file);
                  return (
                    <span key={i} className={`source-chip ${getSourceColor(label)}`}>
                      {label}
                    </span>
                  );
                })}
              </div>
            </div>

            {/* Decision cards */}
            <div className="decision-cards">
              {dedupedSources.map((src, i) => (
                <div key={i} className="decision-card">
                  <div className="decision-top">
                    <span className="decision-badge">{src.decision || "Decision"}</span>
                    {src.alternatives && (
                      <span className="alternatives-tag">
                        vs {src.alternatives}
                      </span>
                    )}
                  </div>
                  {src.reason && (
                    <p className="decision-reason">{src.reason}</p>
                  )}
                  {src.impacts && (
                    <p className="decision-impact">
                      <span className="impact-label">Impact →</span> {src.impacts}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
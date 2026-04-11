import { useState, useRef } from "react";
import Chat from "./components/chat";
import InputBox from "./components/Inputbox";
import "../src/style.css";

const EXAMPLE_QUESTIONS = [
  "Why did we choose Redis?",
  "What if we remove caching?",
  "Why PostgreSQL over Mongo?",
  "Why microservices over monolith?",
  "Why did we pick React?",
];

export default function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    setTimeout(() => chatEndRef.current?.scrollIntoView({ behavior: "smooth" }), 50);
  };

  const handleAsk = async (question) => {
    if (!question.trim() || loading) return;

    const userMsg = { role: "user", text: question };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    scrollToBottom();

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      const aiMsg = { role: "ai", text: data.answer, sources: data.sources || [] };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error("Error asking question:", err);
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "⚠️ Could not reach the backend. Make sure the API is running on localhost:8000.",
          sources: [],
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
      scrollToBottom();
    }
  };

  return (
    <div className="app-root">
      {/* Background grid */}
      <div className="bg-grid" />

      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div className="logo-mark">
            <span className="logo-icon">⬡</span>
          </div>
          <div className="header-text">
            <h1 className="header-title">Organizational Memory & Reasoning Agent</h1>
            <p className="header-subtitle">Ask why decisions were made</p>
          </div>
        </div>

        <div className="example-questions">
          <span className="eq-label">Try asking</span>
          <div className="eq-chips">
            {EXAMPLE_QUESTIONS.map((q) => (
              <button
                key={q}
                className="eq-chip"
                onClick={() => handleAsk(q)}
                disabled={loading}
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Main chat area */}
      <main className="main">
        <Chat messages={messages} loading={loading} chatEndRef={chatEndRef} />
      </main>

      {/* Input */}
      <footer className="footer">
        <InputBox onSend={handleAsk} loading={loading} />
      </footer>
    </div>
  );
}
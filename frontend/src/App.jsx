import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/ask?question=${encodeURIComponent(question)}`
      );

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data = await response.json();
      setAnswer(data.answer);
    } catch (error) {
      console.error(error);
      setAnswer("Unable to get an answer from the backend.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="app">
      <div className="chat-container">

        <header className="header">
          <div className="logo">R</div>
          <div>
            <h1>RAG Assistant</h1>
            <p>Ask questions about your documents</p>
          </div>
        </header>

        <main className="chat-area">

          {!answer && !loading && (
            <div className="welcome">
              <div className="welcome-icon">✨</div>
              <h2>How can I help you?</h2>
              <p>
                Ask a question and I'll search your documents to find the
                relevant answer.
              </p>
            </div>
          )}

          {question && (
            <div className="message user-message">
              <div className="avatar user-avatar">You</div>
              <div className="message-content">
                <p>{question}</p>
              </div>
            </div>
          )}

          {loading && (
            <div className="message assistant-message">
              <div className="avatar assistant-avatar">R</div>
              <div className="message-content">
                <div className="typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}

          {answer && !loading && (
            <div className="message assistant-message">
              <div className="avatar assistant-avatar">R</div>
              <div className="message-content">
                <p>{answer}</p>
              </div>
            </div>
          )}

        </main>

        <div className="input-section">
          <div className="input-wrapper">

            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question..."
              rows="1"
            />

            <button
              onClick={askQuestion}
              disabled={loading || !question.trim()}
              className="ask-button"
            >
              {loading ? "..." : "Ask"}
            </button>

          </div>

          <p className="hint">
            Press Enter to ask • Shift + Enter for a new line
          </p>
        </div>

      </div>
    </div>
  );
}

export default App;

import { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("pdf");

  const chatAreaRef = useRef(null);

  // Scroll to latest message
  useEffect(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTop =
        chatAreaRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const askQuestion = async () => {
    const currentQuestion = question.trim();

    if (!currentQuestion || loading) {
      return;
    }

    // Handle exit
    if (currentQuestion.toLowerCase() === "exit") {
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          role: "user",
          content: currentQuestion,
        },
        {
          role: "assistant",
          content: "Goodbye! 👋 You can close this tab.",
        },
      ]);

      setQuestion("");
      return;
    }

    // Add user message
    setMessages((prevMessages) => [
      ...prevMessages,
      {
        role: "user",
        content: currentQuestion,
        source: mode,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      // Select backend endpoint
      const endpoint =
        mode === "sql"
          ? "http://127.0.0.1:8000/ask-sql"
          : "http://127.0.0.1:8000/ask";

      console.log("Using endpoint:", endpoint);

      const response = await fetch(
        `${endpoint}?question=${encodeURIComponent(
          currentQuestion
        )}`
      );

      let data = {};

      try {
        data = await response.json();
      } catch (jsonError) {
        console.error(
          "Could not parse backend response:",
          jsonError
        );
      }

      console.log("Backend response:", data);

      // Handle HTTP errors
      if (!response.ok) {
        const errorMessage =
          data.error ||
          data.detail ||
          `Backend error: HTTP ${response.status}`;

        setMessages((prevMessages) => [
          ...prevMessages,
          {
            role: "assistant",
            content: `❌ ${errorMessage}`,
          },
        ]);

        return;
      }

      // Get answer
      let answer = data.answer;

      // Handle object or array
      if (
        typeof answer === "object" &&
        answer !== null
      ) {
        answer = JSON.stringify(
          answer,
          null,
          2
        );
      }

      // Handle missing answer
      if (
        answer === undefined ||
        answer === null ||
        answer === ""
      ) {
        answer =
          data.error ||
          "No answer received from backend.";
      }

      // Add assistant response
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          role: "assistant",
          content: String(answer),
          source: mode,
        },
      ]);
    } catch (error) {
      console.error(
        "Backend connection error:",
        error
      );

      setMessages((prevMessages) => [
        ...prevMessages,
        {
          role: "assistant",
          content:
            "❌ Unable to connect to the backend. Please make sure FastAPI is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Enter = send
  // Shift + Enter = new line
  const handleKeyDown = (e) => {
    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {
      e.preventDefault();
      askQuestion();
    }
  };

  // Clear conversation
  const clearChat = () => {
    setMessages([]);
    setQuestion("");
  };

  return (
    <div className="app">

      <div className="chat-container">

        {/* HEADER */}
        <header className="header">

          <div className="logo">
            R
          </div>

          <div>
            <h1>RAG Assistant</h1>

            <p>
              Ask questions from documents or SQL Server
            </p>
          </div>

        </header>

        {/* CHAT AREA */}
        <main
          className="chat-area"
          ref={chatAreaRef}
        >

          {/* WELCOME */}
          {messages.length === 0 &&
            !loading && (
              <div className="welcome">

                <div className="welcome-icon">
                  ✨
                </div>

                <h2>
                  How can I help you?
                </h2>

                <p>
                  Select Documents or SQL Server
                  and ask your question.
                </p>

              </div>
            )}

          {/* MESSAGES */}
          {messages.map(
            (message, index) => (
              <div
                key={index}
                className={`message ${
                  message.role === "user"
                    ? "user-message"
                    : "assistant-message"
                }`}
              >

                <div
                  className={`avatar ${
                    message.role === "user"
                      ? "user-avatar"
                      : "assistant-avatar"
                  }`}
                >
                  {message.role === "user"
                    ? "You"
                    : "R"}
                </div>

                <div className="message-content">

                  <p>
                    {String(
                      message.content
                    )}
                  </p>

                </div>

              </div>
            )
          )}

          {/* LOADING */}
          {loading && (
            <div className="message assistant-message">

              <div className="avatar assistant-avatar">
                R
              </div>

              <div className="message-content">

                <div className="typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

              </div>

            </div>
          )}

        </main>

        {/* INPUT SECTION */}
        <div className="input-section">

          {/* SOURCE SELECTOR */}
          <div className="mode-selector">

            <button
              type="button"
              className={
                mode === "pdf"
                  ? "mode-button active"
                  : "mode-button"
              }
              onClick={() => setMode("pdf")}
              disabled={loading}
            >
              📄 Documents
            </button>

            <button
              type="button"
              className={
                mode === "sql"
                  ? "mode-button active"
                  : "mode-button"
              }
              onClick={() => setMode("sql")}
              disabled={loading}
            >
              🗄️ SQL Server
            </button>

          </div>

          {/* INPUT */}
          <div className="input-wrapper">

            <textarea
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder={
                mode === "sql"
                  ? "Ask about your SQL data..."
                  : "Ask about your documents..."
              }
              rows="1"
              disabled={loading}
            />

            <button
              type="button"
              onClick={askQuestion}
              disabled={
                loading ||
                !question.trim()
              }
              className="ask-button"
            >
              {loading ? "..." : "Ask"}
            </button>

          </div>

          {/* CLEAR CONVERSATION */}
          {messages.length > 0 && (
            <button
              type="button"
              onClick={clearChat}
              className="clear-button"
            >
              Clear conversation
            </button>
          )}

          <p className="hint">
            Press Enter to ask • Shift + Enter
            for a new line
          </p>

        </div>

      </div>

    </div>
  );
}

export default App;
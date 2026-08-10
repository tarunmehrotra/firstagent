import { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatAreaRef = useRef(null);

  // Scroll to the latest message
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

    // Add user's question
    setMessages((prevMessages) => [
      ...prevMessages,
      {
        role: "user",
        content: currentQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/ask?question=${encodeURIComponent(
          currentQuestion
        )}`
      );

      if (!response.ok) {
        throw new Error(
          `HTTP error: ${response.status}`
        );
      }

      const data = await response.json();

      // Add assistant answer
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          role: "assistant",
          content:
            data.answer ||
            "No answer received from backend.",
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prevMessages) => [
        ...prevMessages,
        {
          role: "assistant",
          content:
            "Unable to get an answer from the backend.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

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
              Ask questions about your documents
            </p>
          </div>

        </header>


        {/* CHAT */}
        <main
          className="chat-area"
          ref={chatAreaRef}
        >

          {/* Welcome */}
          {messages.length === 0 && !loading && (
            <div className="welcome">

              <div className="welcome-icon">
                ✨
              </div>

              <h2>
                How can I help you?
              </h2>

              <p>
                Ask a question and I'll search
                your documents to find the
                relevant answer.
              </p>

            </div>
          )}


          {/* ALL MESSAGES */}
          {messages.map((message, index) => (

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
                  {message.content}
                </p>

              </div>

            </div>

          ))}


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


        {/* INPUT */}
        <div className="input-section">

          <div className="input-wrapper">

            <textarea
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask a question..."
              rows="1"
              disabled={loading}
            />

            <button
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


          {/* CLEAR BUTTON */}
          {messages.length > 0 && (
            <button
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
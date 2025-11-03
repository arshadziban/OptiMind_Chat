import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/generate", {
        prompt: input,
      });
      const botMessage = { role: "assistant", content: res.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch {
      const errorMessage = {
        role: "assistant",
        content: "Unable to connect to the model. Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-wrapper">
      <header className="chat-header">
        <h1>OptiMind Chat</h1>
        <p className="subtitle">AI-Powered Book Companion</p>
      </header>

      <div className="chat-box">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`message ${msg.role === "user" ? "user" : "assistant"}`}
          >
            {msg.role === "assistant" && (
              <div className="avatar">
                <img
                  src={`${process.env.PUBLIC_URL}/chat_icon.png`}
                  alt="AI Icon"
                  className="bot-icon"
                />
              </div>
            )}
            <div className="bubble">{msg.content}</div>
          </div>
        ))}

        {isTyping && (
          <div className="message assistant typing">
            <div className="avatar">
              <img
                src={`${process.env.PUBLIC_URL}/chat_icon.png`}
                alt="AI Icon"
                className="bot-icon"
              />
            </div>
            <div className="bubble typing-bubble">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Ask anything"
          rows={1}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = `${process.env.REACT_APP_API_URL}/summarize`;

function App() {
  const [inputText, setInputText] = useState("");
  const [summary, setSummary] = useState("");
  const [sentiment, setSentiment] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}`, {
        text: inputText,
      });

      setSummary(response.data.summary);
      setSentiment(response.data.sentiment);
    } catch (error) {
      console.error("Error:", error);
      alert("There was an error in the process");
    }

    setLoading(false);
  };

  return (
    <div className="app-container">
      <h1 className="app-title">AI Text Summarizer</h1>
      <form onSubmit={handleSubmit} className="form-container">
        <textarea className="text-input" value={inputText} onChange={(e) => setInputText(e.target.value)} placeholder="Type in your text..." rows="10" cols="50" />
        <button type="submit" disabled={loading} className={`submit-button ${loading ? "loading" : ""}`}>
          {loading ? "In Progress..." : "Click"}
        </button>
      </form>

      {summary && (
        <div className="result-container">
          <h2 className="result-title">Result:</h2>
          <p className="summary-text">{summary}</p>
          {sentiment && (
            <p className="sentiment-text">
              <strong>Text Sentiment:</strong> {sentiment}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;

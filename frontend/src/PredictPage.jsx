import React, { useState } from "react";

function PredictPage() {
  const [date, setDate] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPredictions = async () => {
    if (!date) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/predict?date=${date}`, {
        method: "POST", // POST, но дата в query
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "24px", fontFamily: "Arial, sans-serif" }}>
      <h1>NHL Game Predictions</h1>

      <div style={{ marginBottom: "16px" }}>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          style={{ padding: "6px", marginRight: "8px" }}
        />
        <button onClick={fetchPredictions} style={{ padding: "6px 12px" }}>
          Predict
        </button>
      </div>

      {loading && <div>Loading...</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}

      {results.length > 0 && (
        <table
          border="1"
          cellPadding="8"
          style={{ borderCollapse: "collapse", width: "100%" }}
        >
          <thead>
            <tr>
              <th>Home</th>
              <th>Away</th>
              <th>P(Home Win)</th>
            </tr>
          </thead>
          <tbody>
            {results.map((game, index) => {
              const prob = parseFloat(game.prob_win_home);
              const homeWins = prob > 0.5;

              return (
                <tr key={index}>
                  <td
                    style={{
                      fontWeight: homeWins ? "bold" : "normal",
                      color: homeWins ? "green" : "black",
                    }}
                  >
                    {game.home}
                  </td>
                  <td
                    style={{
                      fontWeight: !homeWins ? "bold" : "normal",
                      color: !homeWins ? "green" : "black",
                    }}
                  >
                    {game.away}
                  </td>
                  <td style={{ textAlign: "right" }}>
                    {(prob * 100).toFixed(1)}%
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default PredictPage;

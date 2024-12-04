import React, { useState } from "react";

function App() {
  const [team, setTeam] = useState([]);
  const [inputPlayer, setInputPlayer] = useState("");
  const [prediction, setPrediction] = useState(null);

  const handleAddPlayer = () => {
    if (inputPlayer.trim() !== "") {
      setTeam((prevTeam) => [...prevTeam, inputPlayer.trim()]);
      setInputPlayer("");
    }
  };

  const handleRemovePlayer = (player) => {
    setTeam((prevTeam) => prevTeam.filter((p) => p !== player));
  };

  const handleSubmit = async () => {
    if (team.length === 0) {
      alert("Please add at least one player to your team.");
      return;
    }

    try {
      // Simulate API call to predict threat
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ team }),
      });
      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error("Error during prediction:", error);
      alert("An error occurred while fetching predictions.");
    }
  };

  return (
    <div style={{ margin: "2rem" }}>
      <h1>FPL Threat Predictor</h1>
      <div>
        <h3>Input Your Current Team</h3>
        <input
          type="text"
          placeholder="Enter player name"
          value={inputPlayer}
          onChange={(e) => setInputPlayer(e.target.value)}
          style={{ marginRight: "1rem", padding: "0.5rem" }}
        />
        <button onClick={handleAddPlayer} style={{ padding: "0.5rem 1rem" }}>
          Add Player
        </button>
      </div>
      <div style={{ marginTop: "1rem" }}>
        <h4>Your Current Team:</h4>
        <ul>
          {team.map((player, index) => (
            <li key={index} style={{ marginBottom: "0.5rem" }}>
              {player}{" "}
              <button
                onClick={() => handleRemovePlayer(player)}
                style={{
                  marginLeft: "1rem",
                  padding: "0.2rem 0.5rem",
                  color: "white",
                  background: "red",
                  border: "none",
                  borderRadius: "3px",
                  cursor: "pointer",
                }}
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      </div>
      <button
        onClick={handleSubmit}
        style={{
          marginTop: "1rem",
          padding: "0.7rem 2rem",
          background: "green",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Predict Threat
      </button>
      {prediction && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Prediction Results:</h3>
          <pre>{JSON.stringify(prediction, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

from flask import Flask, request, jsonify
import pandas as pd
import joblib
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
import json
from datetime import datetime
import requests

app = Flask(__name__)

# Enable CORS for all routes or specific origins
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# # Load pre-trained model
# model = joblib.load("fpl_model.pkl")

# Database connection (adjust credentials)
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="mukund"
    )
    return conn

def get_gameweek(events):
    now = datetime.now(timezone.utc)  # Get the current time in UTC
    for i, event in enumerate(events):
        deadline = datetime.fromisoformat(event["deadline_time"].replace("Z", "+00:00"))
        if not event.get("finished", False):
            if now < deadline:
                return event
            # If current time is past the deadline, return the next gameweek
            elif i + 1 < len(events):
                return events[i + 1]
    return None

def get_optimal_transfer_with_constraints(current_team, gameweek, remaining_budget):
    try:
        # Connect to the PostgreSQL database
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        optimal_transfer = None
        max_improvement = float("-inf")
        
        # Loop through each player in the team
        for player in current_team:
            player_id = player["id"]
            player_position = player["position"]
            player_cost = player["cost"]
            player_points = player["expected_points"][gameweek]
            
            # Calculate the maximum budget available for a replacement
            max_budget = remaining_budget + player_cost
            
            # Query to find the best replacement
            query = """
            SELECT 
                player_id, 
                name, 
                position, 
                cost, 
                expected_points[%(gameweek)s] AS points
            FROM player_expected_points
            WHERE 
                position = %(position)s
                AND player_id NOT IN %(current_team_ids)s
                AND cost <= %(max_budget)s
            ORDER BY points DESC
            LIMIT 1;
            """
            cursor.execute(query, {
                "gameweek": gameweek,
                "position": player_position,
                "current_team_ids": tuple(p["id"] for p in current_team),
                "max_budget": max_budget
            })
            
            replacement = cursor.fetchone()
            
            # Calculate the improvement in points
            if replacement:
                improvement = replacement["points"] - player_points
                if improvement > max_improvement:
                    max_improvement = improvement
                    optimal_transfer = {
                        "outgoing_player": player,
                        "incoming_player": replacement,
                        "improvement": improvement
                    }
        
        cursor.close()
        conn.close()

        return optimal_transfer

    except Exception as e:
        print(f"Error: {e}")
        return None


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])  # Return an empty list if no query

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to find matching player names and their IDs
    cursor.execute("""
        SELECT id, web_name 
        FROM players 
        WHERE web_name ILIKE %s 
        LIMIT 5
    """, (f"%{query}%",))
    
    results = cursor.fetchall()
    for row in results:
        print(row)
    cursor.close()
    conn.close()
    
    # Format results as a list of dictionaries
    players = [{"id": row[0], "name": row[1]} for row in results]
    return jsonify(players)


@app.route("/predict", methods=["POST"])
def predict():
    data=request.get_json()
    print("Team recieved")

    fpl_url="https://fantasy.premierleague.com/api/bootstrap-static/"
    fpl_data=requests.get(fpl_url)
    fpl_json=fpl_data.json()

    gw=get_gameweek(fpl_json["events"])["id"]

    if not gw:
        return jsonify({"Could not get GW": str(e)}), 500
    


    file = request.files["file"]
    try:
        # Read uploaded CSV
        data = pd.read_csv(file)
        # Assume preprocessing function already exists
        processed_data = preprocess(data)  # Implement this as needed
        predictions = model.predict(processed_data)
        data["Predicted_Threat"] = predictions
        return jsonify(data.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # start flask app
    app.run(host="0.0.0.0", port=8000)

from flask import Flask, request, jsonify
import pandas as pd
import joblib
import psycopg2
from flask_cors import CORS

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
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

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

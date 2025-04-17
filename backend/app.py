from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "/data/results.json"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    print("Received:", data)
    if not os.path.exists("/data"):
        os.makedirs("/data")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []
    existing.append(data)
    with open(DATA_FILE, "w") as f:
        json.dump(existing, f, indent=2)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


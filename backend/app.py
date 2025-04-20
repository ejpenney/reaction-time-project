# backend/app.py
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import os
import csv
from io import StringIO

app = Flask(__name__)
CORS(app)

DATA_FILE = "/data/results.json"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    user_agent = request.headers.get('User-Agent', 'unknown')
    data['user_agent'] = user_agent
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

@app.route("/download", methods=["GET"])
def download():
    if not os.path.exists(DATA_FILE):
        return Response("No data available", status=404)

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    output = StringIO()
    writer = csv.writer(output)
    header = [
        "name", "age", "hours", "hoursOther", "genres", "genreOther",
        "sportsFreq", "sports", "sportsOther", "hormones",
        "deviceType", "user_agent",
        "trial_1", "trial_2", "trial_3", "trial_4", "trial_5"
    ]
    writer.writerow(header)

    for entry in data:
        row = [
            entry.get("name"),
            entry.get("age"),
            entry.get("hours"),
            entry.get("hoursOther"),
            ", ".join(entry.get("genres", [])),
            entry.get("genreOther"),
            entry.get("sportsFreq"),
            ", ".join(entry.get("sports", [])),
            entry.get("sportsOther"),
            entry.get("hormones"),
            entry.get("deviceType"),
            entry.get("user_agent")
        ] + entry.get("times", [])
        writer.writerow(row)

    output.seek(0)
    return Response(output.read(), mimetype='text/csv', headers={
        "Content-Disposition": "attachment; filename=reaction_results.csv"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "water_quality_secret"
DB = "water_quality.db"

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            ph REAL NOT NULL,
            turbidity REAL NOT NULL,
            temperature REAL NOT NULL,
            tds REAL NOT NULL,
            dissolved_oxygen REAL NOT NULL,
            status TEXT NOT NULL,
            recorded_at TEXT NOT NULL
        )
    """)
    count = conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
    if count == 0:
        samples = [
            ("Chennai Lake", 7.2, 2.1, 28.4, 310, 7.1),
            ("City Reservoir", 6.8, 4.7, 29.1, 390, 6.4),
            ("Village Well", 7.6, 1.4, 27.2, 260, 7.8),
            ("River Point A", 8.1, 8.6, 30.0, 520, 5.2)
        ]
        for s in samples:
            status = calculate_status(*s[1:])
            conn.execute("""
                INSERT INTO readings
                (location, ph, turbidity, temperature, tds, dissolved_oxygen,
                 status, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (*s, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    conn.close()

def calculate_status(ph, turbidity, temperature, tds, oxygen):
    # Educational/demo thresholds, not a medical or regulatory water-safety test.
    good = (
        6.5 <= ph <= 8.5 and
        turbidity <= 5 and
        tds <= 500 and
        oxygen >= 6
    )
    return "Good" if good else "Needs Attention"

@app.route("/")
def home():
    conn = db()
    readings = conn.execute(
        "SELECT * FROM readings ORDER BY id DESC LIMIT 8"
    ).fetchall()
    latest = conn.execute(
        "SELECT * FROM readings ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return render_template("index.html", readings=readings, latest=latest)

@app.route("/add", methods=["GET", "POST"])
def add_reading():
    if request.method == "POST":
        try:
            location = request.form["location"].strip()
            ph = float(request.form["ph"])
            turbidity = float(request.form["turbidity"])
            temperature = float(request.form["temperature"])
            tds = float(request.form["tds"])
            oxygen = float(request.form["dissolved_oxygen"])

            if not location:
                raise ValueError("Location is required.")
            status = calculate_status(ph, turbidity, temperature, tds, oxygen)

            conn = db()
            conn.execute("""
                INSERT INTO readings
                (location, ph, turbidity, temperature, tds, dissolved_oxygen,
                 status, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                location, ph, turbidity, temperature, tds, oxygen,
                status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()
            conn.close()
            flash("Water quality reading added successfully.")
            return redirect(url_for("home"))
        except ValueError:
            flash("Please enter valid numeric sensor values.")
            return redirect(url_for("add_reading"))

    return render_template("add_reading.html")

@app.route("/history")
def history():
    conn = db()
    readings = conn.execute(
        "SELECT * FROM readings ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("history.html", readings=readings)

@app.route("/delete/<int:reading_id>", methods=["POST"])
def delete(reading_id):
    conn = db()
    conn.execute("DELETE FROM readings WHERE id = ?", (reading_id,))
    conn.commit()
    conn.close()
    flash("Reading deleted.")
    return redirect(url_for("history"))

@app.route("/api/readings")
def api_readings():
    conn = db()
    rows = conn.execute(
        "SELECT * FROM readings ORDER BY id DESC LIMIT 50"
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/latest")
def api_latest():
    conn = db()
    row = conn.execute(
        "SELECT * FROM readings ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "No readings available"}), 404
    return jsonify(dict(row))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

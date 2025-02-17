import os
import json
import random
import sqlite3
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from flask_session import Session

app = Flask(__name__)

# 🔹 Configure Flask-Session to store session data in the filesystem
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True  # Keep session active even after browser restart
app.config["SECRET_KEY"] = "supersecretkey"  # Change for production
Session(app)

# 📂 Load all JSON career cards from the "careers/" folder (including subfolders)
def load_career_cards():
    career_cards = []
    careers_dir = os.path.join(os.path.dirname(__file__), 'careers')
    for root, dirs, files in os.walk(careers_dir):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    career_cards.append(data)
    return career_cards

# 🔹 Return only enabled career cards
def get_enabled_career_cards():
    all_cards = load_career_cards()
    return [card for card in all_cards if card.get("CareerCard", {}).get("Enabled", 0) == 1]

# ───────────── New Landing Page (Menu + Login) ─────────────
@app.route("/", methods=["GET", "POST"])
def landing():
    if request.method == "POST":
        # Save the user's name in the session
        username = request.form.get("username")
        if username:
            session["username"] = username
            # Redirect to spin wheel page
            return redirect(url_for("spinwheel"))
    return render_template("index.html")

# ───────────── Spin Wheel Page (Renamed from index.html) ─────────────
@app.route("/spinwheel")
def spinwheel():
    enabled_cards = get_enabled_career_cards()
    job_titles = [card["CareerCard"]["Title"] for card in enabled_cards]
    # Store enabled cards in session
    session["enabled_cards"] = json.dumps(enabled_cards)
    session.pop("selected_card", None)
    session.modified = True
    return render_template("spinwheel.html", jobs=job_titles, username=session.get("username"))

# ───────────── Spin Endpoint ─────────────
@app.route("/spin", methods=["POST"])
def spin():
    session.permanent = True  # Ensure session persists
    enabled_cards_json = session.get("enabled_cards", "[]")
    enabled_cards = json.loads(enabled_cards_json)
    if not enabled_cards:
        return jsonify({"error": "No enabled career cards available."}), 400

    # Allow only one spin per session
    if "selected_card" in session:
        return jsonify({"error": "Spin already completed."}), 400

    selected_card = random.choice(enabled_cards)
    session["selected_card"] = json.dumps(selected_card)
    session.modified = True
    print(f"🔹 Job selected: {selected_card['CareerCard']['Title']}")
    return jsonify({"job": selected_card["CareerCard"]["Title"]})

# ───────────── Store selected job (if needed by JS) ─────────────
@app.route("/set_selected_job", methods=["POST"])
def set_selected_job():
    data = request.json
    selected_job = data.get("job")
    if not selected_job:
        return jsonify({"status": "error", "message": "No job selected"}), 400

    enabled_cards_json = session.get("enabled_cards", "[]")
    enabled_cards = json.loads(enabled_cards_json)
    selected_card = next((card for card in enabled_cards if card["CareerCard"]["Title"] == selected_job), None)
    if not selected_card:
        return jsonify({"status": "error", "message": "Job not found"}), 404

    session["selected_card"] = json.dumps(selected_card)
    session.modified = True
    print(f"🔹 Stored job in session: {selected_job}")
    return jsonify({"status": "success"})

# ───────────── Job Card Details Page ─────────────
@app.route("/jobcard")
def jobcard():
    selected_card_json = session.get("selected_card")
    if not selected_card_json:
        print("⚠️ No selected job card in session! Redirecting to spin wheel.")
        return redirect(url_for("spinwheel"))
    try:
        selected_card = json.loads(selected_card_json)
    except json.JSONDecodeError:
        print("⚠️ JSON Decode Error! Redirecting to spin wheel.")
        return redirect(url_for("spinwheel"))
    print(f"✅ Showing job card: {selected_card['CareerCard']['Title']}")
    return render_template("jobcard-details.html", card=selected_card)

# ───────────── Level 1 Scenario Page ─────────────
@app.route("/level1", methods=["GET", "POST"])
def level1():
    selected_card = json.loads(session.get("selected_card", "{}"))
    if not selected_card:
        return redirect(url_for("spinwheel"))
    scenarios = selected_card.get("Level1ScenarioCards", [])
    if request.method == "POST":
        selected_index = int(request.form.get("option"))
        # Simple scoring: Option A -> 10 points; Option B -> 5 points
        score = 10 if selected_index == 0 else 5
        session["scenario_result"] = json.dumps({
            "scenario": scenarios[0],  # Using the first scenario for simplicity
            "selected_option_index": selected_index,
            "score": score
        })
        return redirect(url_for("level1_result"))
    return render_template("level-1.html", scenarios=scenarios)

# ───────────── Level 1 Result Page ─────────────
@app.route("/level1_result")
def level1_result():
    scenario_result = json.loads(session.get("scenario_result", "{}"))
    if not scenario_result:
        return redirect(url_for("level1"))
    return render_template("level1-result.html", result=scenario_result)

# ───────────── Level 2 Scenario Pages (if needed) ─────────────
@app.route("/level2", methods=["GET", "POST"])
def level2():
    selected_card = json.loads(session.get("selected_card", "{}"))
    if not selected_card:
        return redirect(url_for("spinwheel"))
    scenarios = selected_card.get("Level2ScenarioCards", [])
    if request.method == "POST":
        selected_index = int(request.form.get("option"))
        score = 10 if selected_index == 0 else 5
        session["scenario_result"] = json.dumps({
            "scenario": scenarios[0],
            "selected_option_index": selected_index,
            "score": score
        })
        return redirect(url_for("level2_result"))
    return render_template("level-2.html", scenarios=scenarios)

@app.route("/level2_result")
def level2_result():
    scenario_result = json.loads(session.get("scenario_result", "{}"))
    if not scenario_result:
        return redirect(url_for("level2"))
    return render_template("level2-result.html", result=scenario_result)

if __name__ == "__main__":
    app.run(debug=True)

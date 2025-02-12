import os
import json
import random
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from flask_session import Session

app = Flask(__name__)

# 🔹 Configure Flask-Session to store session data in the filesystem
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True  # Keep session active even after browser restart
app.config["SECRET_KEY"] = "supersecretkey"  # Change for production
Session(app)

# 📂 Load all JSON career cards from the "careers" folder
def load_career_cards():
    career_cards = []
    careers_dir = os.path.join(os.path.dirname(__file__), 'careers')

    for filename in os.listdir(careers_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(careers_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                career_cards.append(data)
    
    return career_cards

# 🔹 Return only enabled career cards
def get_enabled_career_cards():
    all_cards = load_career_cards()
    return [card for card in all_cards if card.get("CareerCard", {}).get("Enabled", 0) == 1]

# 🏠 Home route: Displays job titles on the spin wheel
@app.route("/")
def index():
    enabled_cards = get_enabled_career_cards()
    job_titles = [card["CareerCard"]["Title"] for card in enabled_cards]

    # Store enabled cards in session
    session["enabled_cards"] = json.dumps(enabled_cards)
    session.pop("selected_card", None)  # Reset previous selection
    session.modified = True  # Ensure session updates are saved

    return render_template("index.html", jobs=job_titles)

# 🎡 Spin the wheel and select a random job
@app.route("/spin", methods=["POST"])
def spin():
    session.permanent = True  # Ensure session persists
    enabled_cards_json = session.get("enabled_cards", "[]")
    enabled_cards = json.loads(enabled_cards_json)

    if not enabled_cards:
        return jsonify({"error": "No enabled career cards available."}), 400

    selected_card = random.choice(enabled_cards)
    session["selected_card"] = json.dumps(selected_card)  # Store selection in session
    session.modified = True  # Save session

    print(f"🔹 Job selected: {selected_card['CareerCard']['Title']}")

    return jsonify({"job": selected_card["CareerCard"]["Title"]})

# 🔹 Store the selected job in session from JavaScript
@app.route("/set_selected_job", methods=["POST"])
def set_selected_job():
    data = request.json
    selected_job = data.get("job")

    if not selected_job:
        return jsonify({"status": "error", "message": "No job selected"}), 400

    # Find the full job card details from session
    enabled_cards_json = session.get("enabled_cards", "[]")
    enabled_cards = json.loads(enabled_cards_json)
    selected_card = next((card for card in enabled_cards if card["CareerCard"]["Title"] == selected_job), None)

    if not selected_card:
        return jsonify({"status": "error", "message": "Job not found"}), 404

    session["selected_card"] = json.dumps(selected_card)  # Store full card details
    session.modified = True

    print(f"🔹 Stored job in session: {selected_job}")

    return jsonify({"status": "success"})

# 📄 Display selected job card details
@app.route("/jobcard")
def jobcard():
    selected_card_json = session.get("selected_card")

    if not selected_card_json:
        print("⚠️ No selected job card in session! Redirecting to index.")
        return redirect(url_for("index"))  # Redirect to homepage

    try:
        selected_card = json.loads(selected_card_json)
    except json.JSONDecodeError:
        print("⚠️ JSON Decode Error! Redirecting to index.")
        return redirect(url_for("index"))

    print(f"✅ Showing job card: {selected_card['CareerCard']['Title']}")

    return render_template("jobcard-details.html", card=selected_card)

# 🚀 Run Flask App
if __name__ == "__main__":
    app.run(debug=True)

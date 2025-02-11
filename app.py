from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import os
import sqlite3
import markdown

app = Flask(__name__)
app.secret_key = "devkey"  # required for session management

# -------------------------------
# Helper function to read a game card from .MD file
# -------------------------------
def get_job_card(job):
    filename = os.path.join("jobcards", f"{job.replace(' ', '_').lower()}.MD")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
       return f"Game card not found for {job}."
        
# -------------------------------
# Helper function to get a connection to the SQLite3 database
# -------------------------------
def get_db_connection():
    conn = sqlite3.connect("jobcards.db")
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------
# Page 1: Spin Wheel for Job Cards
# -------------------------------
@app.route('/')
def index():
    session['selected_jobs'] = []
    session['current_player'] = 1
    session['total_players'] = 2
    return render_template('page1.html')

@app.route('/set_job', methods=['POST'])
def set_job():
    job = request.json.get('job')
    if not job:
        return jsonify(error="No job provided"), 400

    # Append the selected job to our session list
    selected_jobs = session.get('selected_jobs', [])
    selected_jobs.append(job)
    session['selected_jobs'] = selected_jobs

    # Increase the current player count
    session['current_player'] = session.get('current_player', 1) + 1

    # If both players have selected a job, inform the client
    if session['current_player'] > session.get('total_players', 2):
        return jsonify({'selection_complete': True})
    else:
        return jsonify({'current_player': session['current_player']})


# -------------------------------
# Page 2: Display Job Card Details (Using .MD files)
# -------------------------------

@app.route('/page2')
def page2():
    selected_jobs = session.get('selected_jobs', [])
    job_cards = {}
    for job in selected_jobs:
        job_cards[job] = get_job_card(job)
    return render_template('page2.html', job_cards=job_cards)

# -------------------------------
# Page 3: Level 1 – Job & Question Selection (Using SQLite3)
# -------------------------------

@app.route('/page3')
def page3():
    selected_jobs = session.get('selected_jobs', [])
    jobs = [{"job": job} for job in selected_jobs]
    return render_template('page3.html', jobs=jobs)


@app.route('/get_questions', methods=['GET'])
def get_questions():
    job = request.args.get('job')
    conn = get_db_connection()
    questions = conn.execute("SELECT question FROM questions WHERE job = ?", (job,)).fetchall()
    conn.close()
    question_list = [row["question"] for row in questions]
    return jsonify(question_list)

@app.route('/get_answer', methods=['GET'])
def get_answer():
    job = request.args.get('job')
    question = request.args.get('question')
    conn = get_db_connection()
    row = conn.execute("SELECT answer FROM questions WHERE job = ? AND question = ?", (job, question)).fetchone()
    conn.close()
    if row:
        return jsonify(answer=row["answer"])
    else:
        return jsonify(answer="No answer found.")

if __name__ == '__main__':
    app.run(debug=True)

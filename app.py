# app.py
import uuid
from flask import Flask, request, jsonify
from scrape_quizlet import scrape_quizlet

app = Flask(__name__)

# In-memory quiz store: quiz_id -> {"questions": [...]}  (answers kept server-side)
QUIZ_STORE = {}

@app.route("/quiz")
def quiz():
    topic = request.args.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Missing 'topic' query param"}), 400

    # Build questions (server keeps answers)
    questions_full = scrape_quizlet(topic, max_questions=10)  # [{question, options, answer}]
    # Filter out any errors
    if isinstance(questions_full, list) and questions_full and "error" in questions_full[0]:
        return jsonify({"error": questions_full[0]["error"]}), 404

    # Prepare payload for the client (no answers) and store full on server
    quiz_id = str(uuid.uuid4())
    QUIZ_STORE[quiz_id] = {"questions": questions_full}

    client_questions = [
        {"question": q["question"], "options": q["options"]}
        for q in questions_full
    ]
    return jsonify({"quiz_id": quiz_id, "questions": client_questions})


@app.route("/grade", methods=["POST"])
def grade():
    data = request.get_json(silent=True) or {}
    quiz_id = data.get("quiz_id")
    q_idx = data.get("question_index")
    opt_idx = data.get("option_index")

    # Basic validation
    if quiz_id not in QUIZ_STORE:
        return jsonify({"error": "Unknown quiz_id"}), 404
    if not isinstance(q_idx, int) or not isinstance(opt_idx, int):
        return jsonify({"error": "question_index and option_index must be integers"}), 400

    qs = QUIZ_STORE[quiz_id]["questions"]
    if not (0 <= q_idx < len(qs)):
        return jsonify({"error": "question_index out of range"}), 400
    options = qs[q_idx]["options"]
    if not (0 <= opt_idx < len(options)):
        return jsonify({"error": "option_index out of range"}), 400

    correct_answer = qs[q_idx]["answer"]
    chosen = options[opt_idx]
    return jsonify({"correct": chosen == correct_answer})


if __name__ == "__main__":
    app.run(debug=True)

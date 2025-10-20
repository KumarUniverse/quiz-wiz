import uuid
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scrape_quizlet import scrape_quizlet

app = Flask(__name__)
CORS(app)

QUIZ_STORE = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test_get_quiz", methods=["GET", "POST"])
def test_get_quiz():
    return jsonify({"status": "test endpoint working"}), 200

#@app.route("/get_quiz", methods=["GET"])
#def get_quiz():
#    print("✅ /get_quiz route was hit")
#    topic = request.args.get("topic", "")
#    print("📦 Received data:", data)
#    if not topic:
#        return jsonify({"error": "Missing 'topic' parameter."}), 400
#
#    questions_full = scrape_quizlet(topic, max_questions=10)
#    if isinstance(questions_full, list) and questions_full and "error" in questions_full[0]:
#        return jsonify({"error": questions_full[0]["error"], "questions": []}), 200
#        #return jsonify({"error": questions_full[0]["error"]}), 404
#
#    quiz_id = str(uuid.uuid4())
#    QUIZ_STORE[quiz_id] = {"questions": questions_full}
#
#    client_questions = [
#        {"question": q["question"], "options": q["options"]}
#        for q in questions_full
#    ]
#    return jsonify({"quiz_id": quiz_id, "questions": client_questions})

@app.route("/get_quiz", methods=["POST"])
def get_quiz():
    print("✅ /get_quiz route was hit")
    data = request.get_json()
    print("📦 Received data:", data)
    topic = data.get("topic")
    if not topic:
        return jsonify({"error": "Missing 'topic' parameter."}), 400

    questions_full = scrape_quizlet(topic, max_questions=10)
    if isinstance(questions_full, list) and questions_full and "error" in questions_full[0]:
        #return jsonify({"error": questions_full[0]["error"], "questions": []}), 200  # for debugging
        return jsonify({"error": questions_full[0]["error"]}), 404  # not found

    quiz_id = str(uuid.uuid4())
    QUIZ_STORE[quiz_id] = {"questions": questions_full}

    client_questions = [
        {"question": q["question"], "options": q["options"]}
        for q in questions_full
    ]
    return jsonify({"quiz_id": quiz_id, "questions": client_questions})


@app.route("/grade_all", methods=["POST"])
def grade_all():
    data = request.get_json(silent=True) or {}
    quiz_id = data.get("quiz_id")
    answers = data.get("answers", [])

    if quiz_id not in QUIZ_STORE:
        return jsonify({"error": "Unknown quiz_id"}), 404

    questions = QUIZ_STORE[quiz_id]["questions"]
    correct_count = 0
    feedback = []

    for idx, ans in enumerate(answers):
        if not isinstance(ans, int):
            feedback.append({"question_index": idx, "correct": False})
            continue
        if 0 <= idx < len(questions):
            options = questions[idx]["options"]
            if 0 <= ans < len(options):
                correct = (options[ans] == questions[idx]["answer"])
                if correct:
                    correct_count += 1
                feedback.append({"question_index": idx, "correct": correct})
            else:
                feedback.append({"question_index": idx, "correct": False})
        else:
            feedback.append({"question_index": idx, "correct": False})

    return jsonify({
        "score": correct_count,
        "total": len(questions),
        "feedback": feedback
    })


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, port=8000)

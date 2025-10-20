let quizData = [];
let currentQuizId = null;

document.addEventListener("DOMContentLoaded", () => {
document.getElementById("search-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const topic = document.getElementById("topic-input").value.trim();
  if (!topic) return;

  try {
    const res = await fetch("/get_quiz", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ topic })
    });
    //const res = await fetch(`/get_quiz?topic=${encodeURIComponent(topic)}`);

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      alert("Error fetching quiz: " + (err.error || res.statusText));
      return;
    }

    const data = await res.json();
    if (data.error) {
        alert(data.error);
        return;
    }
    currentQuizId = data.quiz_id;
    quizData = data.questions || [];
    renderQuiz(quizData);
  } catch (err) {
    console.error('Error: ', err);
    alert("Failed to fetch quiz. Is the backend running?");
  }
});
});

function renderQuiz(quiz) {
  const container = document.getElementById("quiz-container");
  container.innerHTML = "";

  if (!quiz.length) {
    container.innerHTML = "<p>No quiz questions found.</p>";
    return;
  }

  quiz.forEach((q, idx) => {
    const qDiv = document.createElement("div");
    qDiv.classList.add("quiz-item");
    qDiv.innerHTML = `<p>${q.question}</p>`;
    q.options.forEach((opt, optIdx) => {
      const label = document.createElement("label");
      label.classList.add("option-label");
      label.innerHTML = `
        <input type="radio" name="q${idx}" value="${optIdx}">
        ${opt}
      `;
      qDiv.appendChild(label);
    });
    container.appendChild(qDiv);
  });
}

async function submitQuiz() {
  if (!currentQuizId) {
    alert("No quiz loaded.");
    return;
  }

  const answers = quizData.map((_, idx) => {
    const selected = document.querySelector(`input[name="q${idx}"]:checked`);
    return selected ? parseInt(selected.value, 10) : -1;
  });

  try {
    const res = await fetch("/grade_all", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ quiz_id: currentQuizId, answers })
    });
    const result = await res.json();

    if (!res.ok) {
      alert(result.error || "Error grading quiz");
      return;
    }

    document.getElementById("score").innerText =
      `Your Score: ${result.score} / ${result.total}`;

  } catch (err) {
    console.error(err);
    alert("Error submitting quiz.");
  }
}

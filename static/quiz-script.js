let quizData = [];
let userAnswers = {};

document.getElementById("search-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const topic = document.getElementById("topic-input").value;

  try {
    const res = await fetch("/get_quiz", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ topic })
    });

    const data = await res.json();
    quizData = data.quiz;
    renderQuiz(quizData);
  } catch (err) {
    alert("Failed to fetch quiz. Is the backend running?");
    console.error(err);
  }
});

function renderQuiz(quiz) {
  const container = document.getElementById("quiz-container");
  container.innerHTML = "";

  quiz.forEach((q, idx) => {
    const qDiv = document.createElement("div");
    qDiv.innerHTML = `<p>${q.question}</p>`;
    
    q.options.forEach(opt => {
      const label = document.createElement("label");
      label.innerHTML = `
        <input type="radio" name="q${idx}" value="${opt}">
        ${opt}
      `;
      label.classList.add("option-label");
      qDiv.appendChild(label);
    });
    
    container.appendChild(qDiv);
  });
}

function submitQuiz() {
  let score = 0;
  quizData.forEach((q, idx) => {
    const selected = document.querySelector(`input[name="q${idx}"]:checked`);
    if (selected && selected.value === q.answer) {
      score++;
    }
  });

  document.getElementById("score").innerText = `Your Score: ${score} / ${quizData.length}`;
}

/* Stopwatch */
let timer;
let seconds = 0;

function start() {
  if (!timer) {
    timer = setInterval(() => {
      seconds++;
      document.getElementById("time").innerText = new Date(seconds * 1000).toISOString().substr(11, 8);
    }, 1000);
  }
}

function stop() {
  clearInterval(timer);
  timer = null;
}

function reset() {
  stop();
  seconds = 0;
  document.getElementById("time").innerText = "00:00:00";
}

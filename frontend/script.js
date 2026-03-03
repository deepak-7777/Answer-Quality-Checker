// -----------------------------
// API ENDPOINTS
// -----------------------------
const API_EVALUATE = "http://localhost:5000/evaluate";
const API_GENERATE = "http://localhost:5000/generate-answer";

// -----------------------------
// DOM ELEMENTS
// -----------------------------
const form = document.getElementById("qaForm");
const clearBtn = document.getElementById("clearBtn");
const generateAI = document.getElementById("generateAI");

const fields = ["question", "model_answer", "student_answer"];

// -----------------------------
// PREVENT PAGE REFRESH
// -----------------------------
form.addEventListener("submit", (e) => {
  e.preventDefault();
  checkQuality();
});

// -----------------------------
// AI ANSWER GENERATION
// -----------------------------
generateAI.addEventListener("click", async () => {

  const question = document.getElementById("question").value.trim();

  if (!question) {
    showError("Please enter a question first.");
    return;
  }

  try {

    hideError();
    setAIButtonLoading(true);

    const response = await fetch(API_GENERATE, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "AI generation failed.");
      return;
    }

    const modelBox = document.getElementById("model_answer");

    if (modelBox) {
      modelBox.value = data.ai_answer || "";
      localStorage.setItem("draft_model_answer", modelBox.value);
    }

  } catch (err) {

    showError("Could not generate AI answer.");
    console.error(err);

  } finally {
    setAIButtonLoading(false);
  }

});

// -----------------------------
// AUTOSAVE DRAFT
// -----------------------------
fields.forEach(id => {

  const el = document.getElementById(id);

  if (!el) return;

  const saved = localStorage.getItem("draft_" + id);

  if (saved) el.value = saved;

  el.addEventListener("input", () => {
    localStorage.setItem("draft_" + id, el.value);
  });

});

// -----------------------------
// CLEAR BUTTON
// -----------------------------
clearBtn.addEventListener("click", () => {

  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = "";
    localStorage.removeItem("draft_" + id);
  });

  hideError();
  hideResults();

});

// -----------------------------
// CTRL + ENTER SHORTCUT
// -----------------------------
document.addEventListener("keydown", function(e) {

  if (e.ctrlKey && e.key === "Enter") {
    checkQuality();
  }

});

// -----------------------------
// MAIN EVALUATION FUNCTION
// -----------------------------
async function checkQuality() {

  const question      = document.getElementById("question")?.value.trim();
  const modelAnswer   = document.getElementById("model_answer")?.value.trim();
  const studentAnswer = document.getElementById("student_answer")?.value.trim();

  if (!question || !modelAnswer || !studentAnswer) {
    showError("Please fill all fields.");
    return;
  }

  setLoading(true);
  hideError();
  hideResults();

  try {

    const response = await fetch(API_EVALUATE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        model_answer: modelAnswer,
        student_answer: studentAnswer
      })
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Server error.");
      return;
    }

    displayResults(data);

  } catch (err) {

    showError(err.message || "Backend connection failed.");
    console.error(err);

  } finally {

    setLoading(false);

  }

}

// -----------------------------
// DISPLAY RESULTS
// -----------------------------
function displayResults(data) {

  const {
    relevance_score,
    keyword_score,
    grammar_score,
    completeness_score,
    final_score,
    feedback
  } = data;

  setScoreSafe("similarity", relevance_score);
  setScoreSafe("coverage", keyword_score);
  setScoreSafe("grammar", grammar_score);
  setScoreSafe("clarity", completeness_score);

  const finalEl = document.getElementById("finalScore");
  if (finalEl) finalEl.textContent = Number(final_score || 0).toFixed(1) + "%";

  updateGradeBadge(final_score);

  const feedbackEl = document.getElementById("feedbackText");
  if (feedbackEl) feedbackEl.textContent = feedback || "--";

  const resultsEl = document.getElementById("results");

  if (resultsEl) {
    resultsEl.classList.remove("hidden");
    resultsEl.scrollIntoView({
      behavior: "smooth",
      block: "start"
    });
  }

}

// -----------------------------
// SAFE SCORE SETTER
// -----------------------------
function setScoreSafe(name, value) {

  const el = document.getElementById(name + "Score");

  if (!el) return;

  const v = Number(value || 0);
  const rounded = Math.round(v);

  el.textContent = rounded + "%";

}

// -----------------------------
// GRADE BADGE
// -----------------------------
function updateGradeBadge(score) {

  const badge = document.getElementById("gradeBadge");
  if (!badge) return;

  const s = Number(score || 0);

  if (s >= 85) {
    badge.textContent = "🏆 Excellent";
    badge.className = "grade-badge grade-excellent";
  }
  else if (s >= 70) {
    badge.textContent = "👍 Good";
    badge.className = "grade-badge grade-good";
  }
  else if (s >= 50) {
    badge.textContent = "⚠️ Average";
    badge.className = "grade-badge grade-average";
  }
  else {
    badge.textContent = "❌ Poor";
    badge.className = "grade-badge grade-poor";
  }

}

// -----------------------------
// LOADING STATE
// -----------------------------
function setLoading(isLoading) {

  const btn    = document.getElementById("submitBtn");
  const text   = document.getElementById("btnText");
  const loader = document.getElementById("btnLoader");

  if (!btn || !text || !loader) return;

  btn.disabled = isLoading;

  if (isLoading) {
    text.textContent = "Analyzing...";
    loader.classList.remove("hidden");
  } else {
    text.textContent = "🔍 Check Answer Quality";
    loader.classList.add("hidden");
  }

}

// -----------------------------
// AI BUTTON LOADING
// -----------------------------
function setAIButtonLoading(state) {

  const btn = document.getElementById("generateAI");
  if (!btn) return;

  if (state) {
    btn.textContent = "Generating...";
    btn.disabled = true;
  } else {
    btn.textContent = "🤖 Generate AI Answer";
    btn.disabled = false;
  }

}

// -----------------------------
// ERROR HANDLING
// -----------------------------
function showError(message) {

  const box = document.getElementById("errorBox");
  if (!box) return;

  box.textContent = "⚠️ " + message;
  box.classList.remove("hidden");

}

function hideError() {

  const box = document.getElementById("errorBox");
  if (box) box.classList.add("hidden");

}

function hideResults() {

  const results = document.getElementById("results");
  if (results) results.classList.add("hidden");

}


// AUTO CLEAR ON PAGE LOAD
window.addEventListener("load", () => {

  const fields = ["question", "model_answer", "student_answer"];

  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = "";
    localStorage.removeItem("draft_" + id);
  });

});
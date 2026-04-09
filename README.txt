# 🎓 Academic Answer Quality Checker – NLP Evaluation System

Academic Answer Quality Checker is an intelligent NLP-based application designed to automatically evaluate student answers. It compares student responses with a model answer and generates structured scores based on relevance, keyword coverage, grammar quality, and completeness.

---

🚀 Features
🧠 Semantic Relevance Scoring

The system compares the student answer with a model answer.

It calculates semantic similarity using advanced NLP techniques.

Helps determine how closely the student response matches expected concepts.

---

🔑 Keyword Coverage Detection

Important keywords are extracted from the model answer.

The system checks whether these keywords appear in the student answer.

Ensures essential academic concepts are covered.

---

✍️ Grammar & Spelling Analysis

Grammar and spelling are evaluated automatically.

Writing clarity and language accuracy are assessed.

Improves overall answer presentation quality.

---

📏 Completeness Measurement

The application checks whether the answer covers key ideas.

Length and depth of explanation are considered.

Prevents overly short or incomplete responses.

---

📊 Weighted Final Score Calculation

Each metric contributes to the final score using predefined weights.

Relevance (40%), Keyword (30%), Grammar (20%), Completeness (10%).

Generates structured and easy-to-understand feedback.

---

🌐 Interactive Web Interface

Clean frontend for entering questions and answers.

Instant score generation after submission.

Designed for academic demonstration and learning purposes.

---

🧮 Scoring Formula

Final Score is calculated as:

Final Score =
(0.4 × Relevance) +
(0.3 × Keyword) +
(0.2 × Grammar) +
(0.1 × Completeness)

---

📂 Project Structure
AcademicAnswerChecker/
│
├── backend/
│   ├── app.py
│   ├── nlp_engine.py
│   ├── lt_test.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md

---

⚙ Tech Stack

🔹 Backend

Python 3.8+
Flask
flask-cors
NLTK
scikit-learn
sentence-transformers
language-tool-python

---

🔹 Frontend

HTML5
CSS3
Vanilla JavaScript (Fetch API)

---

🛠 Installation
1️⃣ Navigate to Backend Folder
cd backend
2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
Activate it:
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt

Note: sentence-transformers downloads an AI model (~90MB) on first run.

---

▶ How to Run
Step 1 — Start Backend Server
python app.py

You should see:
Running on http://0.0.0.0:5000
Keep this terminal open.
Step 2 — Open Frontend
Option 1:
Open frontend/index.html directly in your browser.

OR

cd frontend
python -m http.server 8080

Open:

http://localhost:8080
📝 Example Usage
Question

What is photosynthesis?

Example Output
Relevance Score:     78%
Keyword Score:       65%
Grammar Score:       90%
Completeness Score:  66%
Final Score:         75%
Feedback

Good answer with minor missing concepts. Grammar quality is strong, but some keywords are not fully covered.

---

🛠 Troubleshooting
Grammar check slow?

LanguageTool downloads its model on first execution.

sentence-transformers installation error?

Try:

pip install sentence-transformers --no-cache-dir
CORS error in browser?

Ensure Flask backend is running before opening frontend.

Java not found error?

Install Java and restart your terminal.

---

📌 Purpose

This project is built for academic NLP demonstration and educational learning purposes. It showcases automated answer evaluation using Natural Language Processing techniques.


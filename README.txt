🎓 Academic Answer Quality Checker

This repository contains my NLP-based project for evaluating student answers automatically using semantic analysis, keyword matching, grammar checking, and completeness scoring.

📘 About

The purpose of this project is to evaluate academic answers using Natural Language Processing techniques.

It compares a student’s answer with a model answer and generates structured scoring with feedback to improve learning quality.

🚀 Features

Semantic similarity scoring

Keyword coverage detection

Grammar & spelling analysis

Completeness measurement

Weighted final score calculation

Structured feedback generation

🧮 Scoring Criteria
📊 Evaluation Metrics

Relevance Score (40%) – Measures semantic similarity

Keyword Score (30%) – Checks important keyword presence

Grammar Score (20%) – Evaluates grammar & spelling

Completeness Score (10%) – Checks answer coverage & length

Final Score Formula
Final Score =
0.4 × Relevance +
0.3 × Keyword +
0.2 × Grammar +
0.1 × Completeness
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
⚙ Technologies Used
Backend

Python 3.8+

Flask

flask-cors

NLTK

scikit-learn

sentence-transformers

language-tool-python

Frontend

HTML5

CSS3

Vanilla JavaScript

🛠 Installation

Navigate to backend:

cd backend

Create virtual environment:

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
▶ How to Run

Start backend:

python app.py

Open frontend:

Either open frontend/index.html
OR

cd frontend
python -m http.server 8080

Then open:

http://localhost:8080
📝 Example

Question:
What is photosynthesis?

Output Example:

Relevance Score:     78%
Keyword Score:       65%
Grammar Score:       90%
Completeness Score:  66%
Final Score:         75%
📌 Purpose

Built for academic NLP project demonstration and educational use.

================================================================
  ACADEMIC ANSWER QUALITY CHECKER
  NLP-Powered Automated Answer Evaluation System
================================================================

PROJECT OVERVIEW
-----------------
This system automatically evaluates student answers against
a model answer using Natural Language Processing (NLP).

It calculates four scores:
  - Relevance Score  (40% weight) — Semantic similarity
  - Keyword Score    (30% weight) — Keyword coverage
  - Grammar Score    (20% weight) — Grammar/spelling check
  - Completeness     (10% weight) — Answer length check

Formula: Final = 0.4×Relevance + 0.3×Keyword + 0.2×Grammar + 0.1×Completeness


FOLDER STRUCTURE
-----------------
AcademicAnswerChecker/
│
├── backend/
│   ├── app.py            ← Flask API server
│   ├── nlp_engine.py     ← All NLP logic
│   └── requirements.txt  ← Python dependencies
│
├── frontend/
│   ├── index.html        ← Main UI page
│   ├── style.css         ← Styling
│   └── script.js         ← Frontend logic
│
└── README.txt            ← This file


REQUIREMENTS
-------------
- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser (Chrome, Firefox, Edge)
- Java (required by language-tool-python for grammar checking)
  Download Java from: https://www.java.com/en/download/


INSTALLATION STEPS
-------------------
1. Open a terminal or command prompt.

2. Navigate to the backend folder:
     cd AcademicAnswerChecker/backend

3. (Recommended) Create a virtual environment:
     python -m venv venv

   Activate it:
     Windows:  venv\Scripts\activate
     Mac/Linux: source venv/bin/activate

4. Install dependencies:
     pip install -r requirements.txt

   NOTE: sentence-transformers will download the AI model
   (~90MB) the first time it runs. This is normal.

5. First-time NLTK data download happens automatically on
   first run.


HOW TO RUN
-----------
Step 1 — Start the Backend Server:
  In the backend/ folder, run:
    python app.py

  You should see:
    * Running on http://0.0.0.0:5000

  Keep this terminal window open.

Step 2 — Open the Frontend:
  Open the frontend/index.html file directly in your browser.
  (Double-click the file, or drag it into a browser window.)

  OR use a simple HTTP server:
    cd frontend
    python -m http.server 8080
  Then open: http://localhost:8080

Step 3 — Use the Application:
  1. Type the Question
  2. Type the Model Answer
  3. Type the Student Answer
  4. Click "Check Answer Quality"
  5. View scores and feedback


EXAMPLE INPUT
--------------
Question:
  What is photosynthesis?

Model Answer:
  Photosynthesis is the process by which green plants and some
  other organisms use sunlight, water, and carbon dioxide to
  produce oxygen and energy in the form of sugar. It occurs
  mainly in the chloroplasts of plant cells using chlorophyll.

Student Answer:
  Photosynthesis is a process used by plants to make food from
  sunlight and carbon dioxide. Plants use chlorophyll to absorb
  light energy and convert it into glucose.


EXAMPLE OUTPUT
--------------
  Relevance Score:    78%
  Keyword Score:      65%
  Grammar Score:      90%
  Completeness Score: 66%
  Final Score:        75%

  Feedback:
    Good answer with room for improvement. The answer is somewhat
    relevant but misses key ideas. Some keywords are missing.
    Grammar and spelling look good. Answer length is average.


TROUBLESHOOTING
----------------
Problem: Grammar check is slow on first run
Solution: language-tool-python downloads a language model the
          first time. This is normal. Subsequent runs are faster.

Problem: "sentence-transformers" fails to install
Solution: Try: pip install sentence-transformers --no-cache-dir
          Or remove it from requirements.txt — the system will
          fall back to TF-IDF similarity automatically.

Problem: CORS error in browser
Solution: Make sure the Flask server is running (python app.py)
          and try refreshing the browser page.

Problem: Java not found error
Solution: Install Java from https://www.java.com and restart
          your terminal.


TECHNOLOGIES USED
------------------
Backend:
  - Python 3.8+
  - Flask (web framework)
  - flask-cors (cross-origin requests)
  - NLTK (tokenization, stopwords)
  - scikit-learn (TF-IDF, cosine similarity)
  - sentence-transformers (semantic similarity)
  - language-tool-python (grammar checking)

Frontend:
  - HTML5
  - CSS3 (responsive grid, animations)
  - Vanilla JavaScript (fetch API)


================================================================
  Built for academic NLP project demonstration purposes.
================================================================

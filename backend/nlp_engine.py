# nlp_engine.py
# Improved Academic Answer Quality Checker (Semantic AI Version)

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sentence_transformers import SentenceTransformer, util

# -----------------------------
# NLTK setup
# -----------------------------
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

STOP_WORDS = set(stopwords.words("english"))

# -----------------------------
# Load semantic model
# -----------------------------
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# Text utilities
# -----------------------------
def normalize(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize_keywords(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    return [t for t in tokens if t not in STOP_WORDS]


# -----------------------------
# 1️⃣ Semantic Similarity (MAIN FIX)
# -----------------------------
def semantic_similarity_score(model_answer, student_answer):

    emb1 = semantic_model.encode(model_answer)
    emb2 = semantic_model.encode(student_answer)

    similarity = util.cos_sim(emb1, emb2)

    score = float(similarity) * 100

    return round(score, 2)


# -----------------------------
# 2️⃣ Keyword Coverage
# -----------------------------
def keyword_score(model_answer, student_answer):

    mk = set(tokenize_keywords(model_answer))
    sk = set(tokenize_keywords(student_answer))

    if not mk:
        return 100.0

    overlap = mk & sk

    score = len(overlap) / len(mk)

    return round(score * 100, 2)


# -----------------------------
# 3️⃣ Grammar Score
# -----------------------------
def grammar_score(student_answer):

    if not student_answer.strip():
        return 0.0

    # simple grammar approximation
    sentences = re.split(r"[.!?]+", student_answer)

    avg_len = len(student_answer.split()) / max(1, len(sentences))

    if avg_len < 12:
        return 90
    elif avg_len < 20:
        return 80
    else:
        return 70


# -----------------------------
# 4️⃣ Completeness
# -----------------------------
def completeness_score(model_answer, student_answer):

    model_len = len(model_answer.split())
    student_len = len(student_answer.split())

    if model_len == 0:
        return 0

    ratio = student_len / model_len

    if ratio >= 1:
        return 90
    elif ratio >= 0.7:
        return 75
    elif ratio >= 0.4:
        return 60
    else:
        return 40


# -----------------------------
# 5️⃣ Final Score
# -----------------------------
def final_score_rubric(similarity, keyword, grammar, completeness):

    final = (
        0.5 * similarity +
        0.2 * keyword +
        0.15 * grammar +
        0.15 * completeness
    )

    return round(final, 2)


# -----------------------------
# 6️⃣ Feedback Generator
# -----------------------------
def generate_feedback(similarity, completeness, final):

    if final >= 85:
        level = "Excellent"
    elif final >= 70:
        level = "Good"
    elif final >= 50:
        level = "Average"
    else:
        level = "Poor"

    feedback = f"{level}: "

    if similarity < 60:
        feedback += "The answer meaning differs from the expected concept. "

    if completeness < 60:
        feedback += "Some key ideas are missing. "

    if similarity >= 80:
        feedback += "The answer meaning strongly matches the teacher answer."

    return feedback


# -----------------------------
# MAIN EVALUATION
# -----------------------------
def evaluate_answer(question, model_answer, student_answer):

    similarity = semantic_similarity_score(model_answer, student_answer)

    keyword = keyword_score(model_answer, student_answer)

    grammar = grammar_score(student_answer)

    completeness = completeness_score(model_answer, student_answer)

    final = final_score_rubric(
        similarity,
        keyword,
        grammar,
        completeness
    )

    feedback = generate_feedback(
        similarity,
        completeness,
        final
    )

    return {
        "semantic_similarity": similarity,
        "coverage_score": keyword,
        "keyword_score": keyword,
        "grammar_score": grammar,
        "clarity_score": completeness,
        "contradiction_penalty": 0,
        "final_score": final,
        "missing_points": [],
        "covered_points": [],
        "feedback": feedback
    }
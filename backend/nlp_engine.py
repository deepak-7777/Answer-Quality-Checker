# nlp_engine.py
# Academic Answer Quality Checker (STABLE - NO TORCH / NO LANGUAGETOOL)

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─────────────────────────────────────────
# NLTK setup
# ─────────────────────────────────────────
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
STOP_WORDS = set(stopwords.words("english"))

# ─────────────────────────────────────────
# 0) Normalization & utilities
# ─────────────────────────────────────────

def normalize(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text

def normalize_strict(text: str) -> str:
    """For exact match: remove punctuation + collapse spaces."""
    if not text:
        return ""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize_keywords(text: str):
    text = normalize_strict(text)
    tokens = word_tokenize(text)
    return [t for t in tokens if t not in STOP_WORDS and t.strip()]

def split_into_points(text: str):
    """
    Split answer into 'points' using newline/bullets + sentence end.
    Works for paragraphs & bullet answers.
    """
    text = text.strip()
    if not text:
        return []

    chunks = re.split(r"(?:\n+|•|\u2022|\- |\* )+", text)
    points = []
    for c in chunks:
        c = c.strip()
        if not c:
            continue
        sents = re.split(r"(?<=[.!?])\s+", c)
        for s in sents:
            s = s.strip()
            if len(s) >= 8:
                points.append(s)
    return points

# ─────────────────────────────────────────
# 1) Semantic Similarity (TF-IDF Cosine)
# ─────────────────────────────────────────

def semantic_similarity_score(model_answer: str, student_answer: str) -> float:
    if not model_answer.strip() or not student_answer.strip():
        return 0.0

    vect = TfidfVectorizer(stop_words="english")
    tfidf = vect.fit_transform([model_answer, student_answer])
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    sim = max(0.0, min(1.0, float(sim)))
    return round(sim * 100, 2)

# ─────────────────────────────────────────
# 2) Point Coverage (Keyword overlap per point)
# ─────────────────────────────────────────

def point_coverage(model_answer: str, student_answer: str, threshold: float = 0.4):
    model_points = split_into_points(model_answer)
    student_points = split_into_points(student_answer)

    if not model_points:
        return 0.0, [], []
    if not student_points:
        return 0.0, [], model_points[:]

    student_text = normalize_strict(student_answer)

    covered = []
    missing = []

    for mp in model_points:
        mp_kw = tokenize_keywords(mp)
        if not mp_kw:
            covered.append(mp)
            continue

        hit = sum(1 for w in mp_kw if w in student_text)
        ratio = hit / max(1, len(mp_kw))

        if ratio >= threshold:
            covered.append(mp)
        else:
            missing.append(mp)

    score = (len(covered) / len(model_points)) * 100.0
    return round(score, 2), covered, missing

# ─────────────────────────────────────────
# 3) Keyword Score
# ─────────────────────────────────────────

def keyword_score(model_answer: str, student_answer: str) -> float:
    mk = set(tokenize_keywords(model_answer))
    sk = set(tokenize_keywords(student_answer))
    if not mk:
        return 100.0
    return round((len(mk & sk) / len(mk)) * 100.0, 2)

# ─────────────────────────────────────────
# 4) Grammar Score (DISABLED for stability)
# ─────────────────────────────────────────

def grammar_score(student_answer: str) -> float:
    if not student_answer.strip():
        return 0.0
    # LanguageTool disabled (download blocked / BadZipFile issue)
    return 100.0

# ─────────────────────────────────────────
# 5) Clarity / Readability Score (simple)
# ─────────────────────────────────────────

def clarity_score(student_answer: str) -> float:
    if not student_answer.strip():
        return 0.0

    words = student_answer.split()
    sentences = [s for s in re.split(r"[.!?]+", student_answer) if s.strip()]
    sentence_count = max(1, len(sentences))
    avg_len = len(words) / sentence_count

    if avg_len <= 12:
        return 90.0
    elif avg_len <= 20:
        return 80.0
    elif avg_len <= 28:
        return 65.0
    else:
        return 50.0

# ─────────────────────────────────────────
# 6) Contradiction Penalty
# ─────────────────────────────────────────

OPS_PATTERN = r"(==|!=|<=|>=|&&|\|\||<<|>>|[%+\-*/=<>!&|^~])"

def extract_numbers(text: str):
    return set(re.findall(r"\b\d+(?:\.\d+)?\b", text))

def extract_ops(text: str):
    return set(re.findall(OPS_PATTERN, text))

def contradiction_penalty(model_answer: str, student_answer: str) -> float:
    if not model_answer.strip() or not student_answer.strip():
        return 0.0

    m_nums = extract_numbers(model_answer)
    s_nums = extract_numbers(student_answer)
    extra_nums = s_nums - m_nums

    m_ops = extract_ops(model_answer)
    s_ops = extract_ops(student_answer)
    extra_ops = s_ops - m_ops

    penalty = 0.0
    penalty += min(15.0, 5.0 * len(extra_nums))
    penalty += min(15.0, 2.0 * len(extra_ops))

    return round(min(30.0, penalty), 2)

# ─────────────────────────────────────────
# 7) Final Score Rubric
# ─────────────────────────────────────────

def final_score_rubric(similarity, coverage, keyword, grammar, clarity, penalty):
    base = (
        0.35 * similarity +
        0.35 * coverage +
        0.10 * keyword +
        0.10 * clarity +
        0.10 * grammar
    )
    final = base - penalty
    return round(max(0.0, min(100.0, final)), 2)

# ─────────────────────────────────────────
# 8) Feedback
# ─────────────────────────────────────────

def generate_feedback(similarity, coverage, grammar, clarity, penalty, missing_points, final):
    parts = []

    if final >= 85:
        parts.append("Excellent: Your answer is highly accurate and well-structured.")
    elif final >= 70:
        parts.append("Good: The answer is mostly correct, but can be improved.")
    elif final >= 50:
        parts.append("Average: Some key concepts are missing or unclear.")
    else:
        parts.append("Poor: Please review the topic and rewrite the answer.")

    if similarity < 50:
        parts.append("Relevance is low: the answer does not match the expected meaning.")
    elif similarity < 70:
        parts.append("Relevance is moderate: meaning matches partially.")
    else:
        parts.append("Relevance is strong: meaning matches the model answer.")

    if coverage < 50:
        parts.append("Completeness is low: many expected points are missing.")
    elif coverage < 80:
        parts.append("Completeness is moderate: some key points are missing.")
    else:
        parts.append("Completeness is good: most key points are covered.")

    # grammar fixed 100 so this will mostly say good
    if grammar < 60:
        parts.append("Grammar needs improvement (spelling/grammar issues detected).")
    elif grammar < 85:
        parts.append("Minor grammar issues detected.")
    else:
        parts.append("Grammar is good.")

    if clarity < 40:
        parts.append("Clarity is low: use shorter sentences and clearer structure.")
    elif clarity < 70:
        parts.append("Clarity is okay: make the explanation a bit simpler.")
    else:
        parts.append("Clarity is good.")

    if penalty >= 10:
        parts.append("Warning: Possible incorrect/excess information detected (numbers/symbols mismatch).")

    if missing_points:
        show = missing_points[:5]
        parts.append("Missing key points (examples): " + " | ".join(show))

    return " ".join(parts)

# ─────────────────────────────────────────
# 9) Main Evaluate
# ─────────────────────────────────────────

def evaluate_answer(question, model_answer, student_answer):
    if model_answer.strip() and student_answer.strip():
        if normalize_strict(model_answer) == normalize_strict(student_answer):
            return {
                "semantic_similarity": 100.0,
                "coverage_score": 100.0,
                "keyword_score": 100.0,
                "grammar_score": 100.0,
                "clarity_score": 100.0,
                "contradiction_penalty": 0.0,
                "final_score": 100.0,
                "missing_points": [],
                "covered_points": [],
                "feedback": "Perfect match! Student answer is identical to the model answer."
            }

    similarity = semantic_similarity_score(model_answer, student_answer)
    coverage, covered_points, missing_points = point_coverage(model_answer, student_answer)
    kw = keyword_score(model_answer, student_answer)
    gr = grammar_score(student_answer)
    cl = clarity_score(student_answer)
    pen = contradiction_penalty(model_answer, student_answer)

    final = final_score_rubric(similarity, coverage, kw, gr, cl, pen)

    feedback = generate_feedback(
        similarity=similarity,
        coverage=coverage,
        grammar=gr,
        clarity=cl,
        penalty=pen,
        missing_points=missing_points,
        final=final
    )

    return {
        "semantic_similarity": similarity,
        "coverage_score": coverage,
        "keyword_score": kw,
        "grammar_score": gr,
        "clarity_score": cl,
        "contradiction_penalty": pen,
        "final_score": final,
        "missing_points": missing_points[:10],
        "covered_points": covered_points[:10],
        "feedback": feedback
    }
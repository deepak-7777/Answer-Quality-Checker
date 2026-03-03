# app.py
# Flask backend for Academic Answer Quality Checker

from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_engine import evaluate_answer
from groq import Groq
import os


# GROQ CLIENT (AI MODEL)


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



app = Flask(__name__)
CORS(app)

# HOME ROUTE
@app.route('/')
def home():
    return jsonify({
        "message": "Academic Answer Quality Checker API is running!"
    })

# AI MODEL ANSWER GENERATION (Teacher Answer)
@app.route('/generate-answer', methods=['POST'])
def generate_answer():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received."}), 400

    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question is required."}), 400

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an academic assistant that writes clear and correct exam answers."
                },
                {
                    "role": "user",
                    "content": f"Write a clear academic answer for the following exam question:\n\n{question}"
                }
            ],
            temperature=0.4,
            max_tokens=300
        )

        ai_answer = response.choices[0].message.content

        return jsonify({
            "ai_answer": ai_answer
        })

    except Exception as e:
        return jsonify({
            "error": f"AI generation failed: {str(e)}"
        }), 500


# ANSWER EVALUATION
@app.route('/evaluate', methods=['POST'])
def evaluate():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received."}), 400

    question = data.get('question', '').strip()
    model_answer = data.get('model_answer', '').strip()
    student_answer = data.get('student_answer', '').strip()

    if not question or not model_answer or not student_answer:
        return jsonify({
            "error": "All fields (question, model_answer, student_answer) are required."
        }), 400

    try:

        result = evaluate_answer(question, model_answer, student_answer)

        # -------- FORMAT FOR FRONTEND --------
        response_data = {
            "relevance_score": result.get("semantic_similarity", 0),
            "keyword_score": result.get("keyword_score", 0),
            "grammar_score": result.get("grammar_score", 0),
            "completeness_score": result.get("coverage_score", 0),
            "final_score": result.get("final_score", 0),
            "feedback": result.get("feedback", "")
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({
            "error": f"Evaluation failed: {str(e)}"
        }), 500


# START SERVER
if __name__ == '__main__':

    print("Starting Academic Answer Quality Checker server...")
    print("API available at: http://localhost:5000")

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
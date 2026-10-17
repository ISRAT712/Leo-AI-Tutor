
from fastapi import FastAPI
from database import get_quiz_history

app = FastAPI(
    title="Leo AI Tutor API",
    description="API for learning progress and quiz history",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Leo AI Tutor API!",
        "status": "running"
    }


@app.get("/progress")
def get_progress():
    history = get_quiz_history()

    total_quizzes = len(history)
    total_questions = sum(item["total"] for item in history)
    total_correct = sum(item["score"] for item in history)

    average_score = (
        sum(item["percentage"] for item in history) / total_quizzes
        if total_quizzes else 0
    )

    return {
        "total_quizzes": total_quizzes,
        "total_questions": total_questions,
        "total_correct": total_correct,
        "average_score": round(average_score, 2),
        "quiz_history": history
    }

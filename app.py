
import streamlit as st
import os
import json
from dotenv import load_dotenv
from google import genai
from database import save_quiz_result, get_quiz_history

load_dotenv()

st.set_page_config(
    page_title="Leo AI Tutor",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Leo - AI Personalized Learning Assistant")
st.write("Your personal AI tutor for learning, quizzes, and progress tracking.")

api_key = os.getenv("GEMINI_API_KEY")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Home", "AI Tutor", "Quiz", "Progress"]
)

# HOME PAGE
if page == "Home":
    st.header("Welcome to Leo!")
    st.write("Learn new topics, practice quizzes, and track your progress.")
    st.info("Your personalized learning journey starts here!")

# AI TUTOR PAGE
elif page == "AI Tutor":
    st.header("Ask Your AI Tutor")

    topic = st.text_input("What topic do you want to learn?")
    question = st.text_area("Ask your question")

    if st.button("Get Explanation"):
        if not topic.strip() or not question.strip():
            st.warning("Please enter both a topic and a question.")

        elif not api_key:
            st.error("API key not found. Please check your .env file.")

        else:
            try:
                client = genai.Client(api_key=api_key)

                with st.spinner("Leo is thinking..."):
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=(
                            f"You are Leo, a friendly AI tutor. "
                            f"Explain the topic '{topic}' in simple language. "
                            f"Answer this question: {question}"
                        )
                    )

                st.subheader("Leo's Explanation")
                st.write(response.text)

            except Exception as e:
                st.error("Leo could not answer. Check your API access and connection.")
                st.caption(str(e))

# QUIZ PAGE
elif page == "Quiz":
    st.header("📝 AI Quiz Generator")

    topic = st.text_input(
        "Enter a topic for your quiz",
        placeholder="e.g., Python, Machine Learning"
    )

    num_questions = st.selectbox(
        "Number of questions",
        [3, 5, 10]
    )

    if st.button("Generate Quiz"):
        if not topic.strip():
            st.warning("Please enter a topic first.")

        elif not api_key:
            st.error("API key not found. Check your .env file.")

        else:
            try:
                client = genai.Client(api_key=api_key)

                prompt = f"""
                Create exactly {num_questions} multiple-choice quiz questions
                about {topic} for a beginner.

                Return ONLY valid JSON in this format:
                {{
                  "questions": [
                    {{
                      "question": "Question text",
                      "options": [
                        "Option A",
                        "Option B",
                        "Option C",
                        "Option D"
                      ],
                      "answer": "Option A",
                      "explanation": "Brief explanation"
                    }}
                  ]
                }}

                The answer must exactly match one of the four options.
                """

                with st.spinner("Leo is creating your quiz..."):
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt,
                        config={"response_mime_type": "application/json"}
                    )

                quiz = json.loads(response.text)
                questions = quiz["questions"]

                if not questions:
                    st.error("No questions were generated. Please try again.")
                elif any(
                    len(q.get("options", [])) != 4
                    or q.get("answer") not in q.get("options", [])
                    for q in questions
                ):
                    st.error("The generated quiz has an invalid question. Try again.")
                else:
                    # Clear old quiz answers before starting a new quiz
                    for key in list(st.session_state.keys()):
                        if key.startswith("quiz_answer_"):
                            del st.session_state[key]

                    st.session_state["quiz_questions"] = questions
                    st.session_state["quiz_topic"] = topic.strip()
                    st.session_state.pop("quiz_submitted", None)
                    st.session_state.pop("quiz_score", None)
                    st.rerun()

            except Exception as e:
                st.error("Quiz generation failed. Please try again.")
                st.caption(str(e))

    if "quiz_questions" in st.session_state:
        questions = st.session_state["quiz_questions"]

        st.subheader(f"Quiz: {st.session_state['quiz_topic']}")
        st.write(f"Total questions: {len(questions)}")

        with st.form("quiz_form"):
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i + 1}. {q['question']}**")

                st.radio(
                    "Choose one answer:",
                    q["options"],
                    index=None,
                    key=f"quiz_answer_{i}"
                )

            submitted = st.form_submit_button("Submit Quiz")

        if submitted:
            score = 0

            for i, q in enumerate(questions):
                selected = st.session_state.get(f"quiz_answer_{i}")

                if selected == q["answer"]:
                    score += 1

            # Save the result only once for this quiz submission
            st.session_state["quiz_score"] = score
            st.session_state["quiz_submitted"] = True

            if not st.session_state.get("quiz_saved", False):
                save_quiz_result(
                    st.session_state["quiz_topic"],
                    score,
                    len(questions)
                )
                st.session_state["quiz_saved"] = True

            st.rerun()

        if st.session_state.get("quiz_submitted"):
            score = st.session_state["quiz_score"]
            total = len(questions)

            st.success(
                f"Your score: {score}/{total} "
                f"({score / total * 100:.1f}%)"
            )

            for i, q in enumerate(questions):
                selected = st.session_state.get(f"quiz_answer_{i}")

                st.markdown(f"**Q{i + 1}. {q['question']}**")
                st.write(f"Your answer: {selected or 'Not answered'}")
                st.write(f"Correct answer: {q['answer']}")
                st.write(f"Explanation: {q['explanation']}")

            if st.button("Create Another Quiz"):
                for key in list(st.session_state.keys()):
                    if key.startswith("quiz_answer_"):
                        del st.session_state[key]

                for key in [
                    "quiz_questions",
                    "quiz_topic",
                    "quiz_submitted",
                    "quiz_score",
                    "quiz_saved"
                ]:
                    st.session_state.pop(key, None)

                st.rerun()

# PROGRESS PAGE
elif page == "Progress":
    st.header("📊 Your Learning Progress")

    history = get_quiz_history()

    if not history:
        st.info("No quiz results saved yet. Complete a quiz to see your progress.")

    else:
        total_quizzes = len(history)
        total_questions = sum(item["total"] for item in history)
        total_correct = sum(item["score"] for item in history)

        average_score = (
            sum(item["percentage"] for item in history) / total_quizzes
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Quizzes Completed", total_quizzes)
        col2.metric("Questions Answered", total_questions)
        col3.metric("Average Score", f"{average_score:.1f}%")

        st.subheader("Quiz History")

        for item in history:
            with st.expander(
                f"{item['topic']} — {item['score']}/{item['total']} "
                f"({item['percentage']:.1f}%)"
            ):
                st.write(f"**Topic:** {item['topic']}")
                st.write(f"**Score:** {item['score']}/{item['total']}")
                st.write(f"**Percentage:** {item['percentage']:.1f}%")
                st.write(f"**Date:** {item['created_at']}")

        st.subheader("Score History")

        chart_data = {
            "Quiz": [
                f"{item['topic']} #{item['id']}"
                for item in reversed(history)
            ],
            "Score (%)": [
                item["percentage"] for item in reversed(history)
            ]
        }

        st.line_chart(
            chart_data,
            x="Quiz",
            y="Score (%)"
        )

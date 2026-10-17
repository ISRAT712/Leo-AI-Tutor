# Leo – AI-Powered Personalized Learning Assistant

Leo is an AI-powered personalized learning assistant designed to help students learn topics, practice quizzes, and track their learning progress.

## Features

- **AI Tutor:** Ask questions and receive AI-generated explanations.
- **Quiz Generation:** Generate multiple-choice quizzes on selected topics.
- **Quiz Evaluation:** Check answers and receive scores and explanations.
- **Progress Tracking:** Store quiz results and view learning history.
- **REST API:** Access quiz progress through FastAPI endpoints.
- **Database:** Store quiz history using SQLite.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- FastAPI
- SQLite
- Uvicorn

## Project Structure

```text
Leo/
├── app.py
├── api.py
├── database.py
├── requirements.txt
├── .gitignore
└── .env
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/ISRAT712/Leo-AI-Tutor.git
   cd Leo-AI-Tutor
   ```

2. Create and activate a virtual environment.

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Gemini API key:

   ```text
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. Start the Streamlit application:

   ```bash
   streamlit run app.py
   ```

6. In a separate terminal, start the FastAPI server:

   ```bash
   python -m uvicorn api:app --reload
   ```

## API Endpoints

- `/` — API welcome message and status.
- `/progress` — Quiz statistics and history.
- `/docs` — Interactive API documentation.

When running locally, the API documentation is available at `http://127.0.0.1:8000/docs`.

## Security

Never commit the `.env` file or expose your Gemini API key. Keep secrets in environment variables.

## Author

**Mst. Israt Jahan Eva**

GitHub: [ISRAT712](https://github.com/ISRAT712)

## License

No license has been specified yet.
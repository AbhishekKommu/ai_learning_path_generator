# PathForge: AI Learning Path Generator

A Flask web app that turns a goal (for example, "machine learning engineer"), your level, and your available time into a week-by-week learning plan with free resources and a capstone project. Plans are saved to your account and you can tick off weeks to track progress.

## Features
- Register, log in, and manage your profile (Flask-Login, hashed passwords, CSRF protection)
- Generate, view, edit, and delete learning paths
- Progress tracking per week
- Two plan engines: a scikit-learn TF-IDF recommender (works offline) and optional LLM generation through the Anthropic API

## Stack
Flask, SQLAlchemy (SQLite by default), Flask-Migrate, Flask-WTF, scikit-learn, vanilla HTML/CSS/JS.

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then set SECRET_KEY (and ANTHROPIC_API_KEY if you want LLM plans)
python app.py
```
Open http://127.0.0.1:5000. The database file is created automatically in `database/`.

## Migrations (optional)
```bash
export FLASK_APP=app.py
flask db init && flask db migrate -m "initial" && flask db upgrade
```

## Tests
```bash
pytest
```

## Project layout
- `app.py`, `config.py`, `extensions.py`: app factory, settings, shared extensions
- `backend/`: models, forms, auth and main routes, AI engine
- `ml/`: recommender and career data (edit `career_data.json` to add tracks)
- `templates/`, `static/`: UI
- `tests/`: pytest suite

## Notes
- Without `ANTHROPIC_API_KEY`, or if the API call fails, the app uses the built-in recommender.
- Never commit `.env`.

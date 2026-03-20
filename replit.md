# Dog Health Diagnosis System

## Project Overview
A full-stack Flask web application for AI-powered dog health diagnosis. Users can create accounts, register pet profiles, and receive personalised symptom-based health assessments.

## Architecture
- **Backend (port 8000):** Flask full-stack app — serves HTML templates with Jinja2, SQLite database via SQLAlchemy, session-based auth.
- **Frontend (port 5000):** React/Vite single-page app — proxies prediction API calls to Flask backend (legacy, kept for compatibility).

## Project Structure
```
app.py                  # Main Flask application (all routes + prediction logic)
models.py               # SQLAlchemy models: User, Pet, Prediction
templates/
  base.html             # Nav + flash messages base layout
  index.html            # Landing page
  dashboard.html        # User dashboard (stats, pets, recent diagnoses)
  diagnose.html         # Symptom input form + pet selector
  result.html           # Diagnosis result display
  history.html          # All past diagnoses (table)
  auth/
    login.html
    signup.html
  pets/
    list.html           # Pet card grid
    form.html           # Add / edit pet (shared)
    detail.html         # Pet profile + diagnosis history
static/
  style.css             # Full CSS design system (custom properties, no frameworks)
utils/
  symptom_predictor.py  # ML symptom predictor (sklearn)
  image_predictor.py    # ML image predictor (TensorFlow)
  disease_info.py       # Disease descriptions, care tips, severity
requirements.txt        # Pinned Python dependencies
runtime.txt             # python-3.10.19
Procfile                # web: python app.py
```

## Key Features
- **User Auth:** Signup / Login / Logout — session-based (Flask session + Werkzeug password hashing)
- **Pet Profiles:** name, breed, age, weight, height, past diseases, allergies, behaviour notes
- **Personalised Diagnosis:**
  - Uses ML model (sklearn) if available, otherwise rule-based keyword matching
  - Adjusts confidence for puppy (<1 yr) and senior (>8 yr) dogs
  - Flags allergy-related skin symptoms
  - Detects recurring conditions from past disease history
  - Flags lethargic behaviour
- **Diagnosis History:** All predictions saved per user/per pet
- **Legacy JSON API:** `/predict-symptom` and `/predict-image` kept for React frontend

## Workflows
| Workflow | Command | Port |
|---|---|---|
| Backend API | `python app.py` | 8000 |
| Start application | `npm run dev` | 5000 |

## Accessing the Flask App
Switch the Replit preview pane to **port 8000** to see the full-stack Flask web interface.

## Database
- **Local:** SQLite at `doghealth.db` (auto-created on first run)
- **Override:** Set `DOGHEALTH_DB_URL` env var for a custom database URL

## Environment Variables
| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `doghealth-secret-change-in-prod` | Flask session secret |
| `DOGHEALTH_DB_URL` | `sqlite:///doghealth.db` | Database connection URL |
| `PORT` | `8000` | Server port |
| `FLASK_ENV` | — | Set to `production` to disable debug mode |

## Deployment (Render / Railway)
1. Push to GitHub
2. Connect repo to Render/Railway
3. Build command: `pip install -r requirements.txt`
4. Start command: `python app.py` (or Procfile is auto-detected)
5. Set `SECRET_KEY` and `PORT` env vars in the platform dashboard

## Python Dependencies (key packages)
- Python 3.10.19
- Flask 2.3.2, Flask-SQLAlchemy 3.1.1, Werkzeug 2.3.7
- gunicorn 21.2.0
- tensorflow-cpu 2.12.0, scikit-learn 1.2.2, numpy 1.23.5

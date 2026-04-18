from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json
from functools import wraps
from datetime import datetime

# ── ML models (optional – graceful fallback if unavailable) ────────────────
_sp = None
_ip = None
HAS_ML = False

try:
    from utils.symptom_predictor import SymptomPredictor
    from utils.image_predictor import ImagePredictor
    from utils.disease_info import get_disease_info as _get_disease_info
    _sp = SymptomPredictor()
    _ip = ImagePredictor()
    HAS_ML = True
    print("ML models loaded successfully.")
except Exception as exc:
    print(f"ML models unavailable ({exc}); using rule-based fallback.")

# ── Flask app ──────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'doghealth-secret-change-in-prod')
_db_url = os.environ.get('DOGHEALTH_DB_URL', 'sqlite:///doghealth.db')
app.config['SQLALCHEMY_DATABASE_URI'] = _db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from models import db, User, Pet, Prediction

db.init_app(app)

with app.app_context():
    db.create_all()


# ── Auth helpers ───────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = current_user()

        if not user:
            session.clear()  # 🔥 important
            flash('Session expired. Please log in again.', 'error')
            return redirect(url_for('login'))

        return f(*args, **kwargs)
    return decorated

def current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None

    try:
        user = User.query.get(user_id)
        return user
    except:
        return None


# ── Prediction logic ───────────────────────────────────────────────────────
DISEASE_KEYWORDS = {
    'Parvovirus':             ['bloody stool', 'bloody diarrhea', 'vomiting', 'lethargy', 'loss of appetite'],
    'Distemper':              ['fever', 'discharge', 'coughing', 'seizure', 'weakness', 'muscle twitching'],
    'Kennel Cough':           ['cough', 'honking', 'gagging', 'runny nose', 'dry cough'],
    'Skin Allergy':           ['itching', 'rash', 'scratching', 'hives', 'red skin', 'licking paws'],
    'Flea Infestation':       ['flea', 'scratching', 'biting tail', 'black dots', 'hair loss'],
    'Gastroenteritis':        ['vomiting', 'diarrhea', 'stomach pain', 'nausea'],
    'Arthritis':              ['limping', 'stiffness', 'joint', 'difficulty walking', 'slow', 'reluctant to move'],
    'Diabetes':               ['excessive thirst', 'frequent urination', 'weight loss', 'increased appetite'],
    'Heart Disease':          ['difficulty breathing', 'fatigue', 'exercise intolerance', 'coughing at night'],
    'Epilepsy':               ['seizure', 'convulsion', 'collapse', 'muscle twitching', 'paddling legs'],
    'Ear Infection':          ['ear', 'head shaking', 'scratching ear', 'odor', 'discharge from ear'],
    'Urinary Tract Infection':['frequent urination', 'straining', 'blood in urine', 'accidents'],
    'Intestinal Parasites':   ['worms', 'pot belly', 'scooting', 'visible parasites', 'bloated abdomen'],
    'Mange':                  ['intense itching', 'hair loss', 'crusty skin', 'sores', 'scaly patches'],
    'Ringworm':               ['circular lesion', 'hair loss patch', 'scaly skin', 'bald circle'],
    'Dental Disease':         ['bad breath', 'bleeding gums', 'loose tooth', 'drooling', 'reluctant to eat'],
    'Anemia':                 ['pale gums', 'weakness', 'rapid breathing', 'fatigue', 'lethargy'],
    'Liver Disease':          ['jaundice', 'yellow skin', 'vomiting', 'loss of appetite', 'weight loss'],
} 
BASE_DISEASE_INFO = {
    "Parvovirus": {
        "severity": "Critical",
        "home_care": [
            "Keep dog hydrated with electrolyte fluids",
            "Avoid feeding during vomiting",
            "Isolate from other dogs"
        ],
        "vet_required": True
    },
    "Gastroenteritis": {
        "severity": "Moderate",
        "home_care": [
            "Feed bland diet (rice + boiled chicken)",
            "Ensure hydration",
            "Avoid oily food"
        ],
        "vet_required": False
    },
    "Skin Allergy": {
        "severity": "Mild",
        "home_care": [
            "Avoid allergens",
            "Clean skin regularly",
            "Use mild dog shampoo"
        ],
        "vet_required": False
    }
}

_FALLBACK_INFO = {
    'description': 'Please consult a licensed veterinarian for an accurate diagnosis and treatment plan.',
    'care_tips': ['Consult a veterinarian promptly.', 'Monitor your dog closely for worsening symptoms.'],
    'severity': 'Unknown',
}
def generate_care_advice(disease, pet=None):
    base = BASE_DISEASE_INFO.get(disease, {})

    advice = []
    advice.extend(base.get("home_care", []))

    # SAFE personalization
    if pet:
        try:
            if pet.age and float(pet.age) < 1:
                advice.append("Puppies need extra care and monitoring")
        except:
            pass

        try:
            if pet.weight and float(pet.weight) > 30:
                advice.append("Maintain controlled diet due to higher weight")
        except:
            pass

    # Severity
    severity = base.get("severity", "Moderate")

    if severity == "Critical":
        advice.append("⚠️ Immediate veterinary attention required")

    elif severity == "Moderate":
        advice.append("Monitor symptoms closely")

    elif severity == "Mild":
        advice.append("🟢 Can be managed at home initially")

    advice.append("⚠️ This is not a substitute for professional veterinary advice")

    return advice, severity

def get_disease_info(disease):
    if HAS_ML:
        try:
            return _get_disease_info(disease)
        except Exception:
            pass
    return _FALLBACK_INFO


def rule_based_predict(symptoms_text):
    s = symptoms_text.lower()
    best, best_score = 'Gastroenteritis', 0
    for disease, keywords in DISEASE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in s)
        if score > best_score:
            best_score, best = score, disease
    confidence = min(40 + best_score * 13, 87)
    return best, float(confidence)


def get_personalized_prediction(symptoms, pet=None):
    if HAS_ML and _sp:
        try:
            pred = _sp.predict(symptoms)
            disease = str(pred['disease'])
            confidence = float(pred['confidence'])
        except Exception:
            disease, confidence = rule_based_predict(symptoms)
    else:
        disease, confidence = rule_based_predict(symptoms)

    disease_data = get_disease_info(disease)
    care_tips, severity = generate_care_advice(disease, pet)
    if isinstance(care_tips, str):
        care_tips = [care_tips]

    notes = []
    if pet:
        name = pet.name
        age = float(pet.age or 0)
        weight = float(pet.weight or 0)

        if age < 1:
            notes.append(
                f"{name} is a puppy and especially vulnerable to infections like Parvovirus and Distemper. "
                "Seek immediate veterinary care."
            )
            if disease in ('Parvovirus', 'Distemper'):
                confidence = min(confidence + 8, 99)
        elif age > 8:
            notes.append(
                f"{name} is a senior dog. Symptoms can progress quickly in older dogs — monitor closely "
                "and arrange a vet visit soon."
            )
            if disease in ('Arthritis', 'Heart Disease', 'Diabetes'):
                confidence = min(confidence + 5, 99)

        if pet.allergies:
            allergy_triggers = ('itch', 'rash', 'skin', 'scratch', 'hive', 'lick')
            if any(w in symptoms.lower() for w in allergy_triggers):
                notes.append(
                    f"{name} has known allergies: {pet.allergies}. "
                    "Skin/itch symptoms may be allergy-related rather than an infection."
                )

        if pet.past_diseases and disease.lower() in pet.past_diseases.lower():
            notes.append(
                f"{name} has a prior history of {disease}. "
                "A recurring condition warrants prompt veterinary attention."
            )

        if weight > 30 and disease in ('Arthritis', 'Diabetes', 'Heart Disease'):
            notes.append(
                f"Weight management is important for {name}'s condition. "
                "Ask your vet about an appropriate diet and exercise plan."
            )

        if pet.behavior:
            beh = pet.behavior.lower()
            if any(w in beh for w in ('lethargic', 'lazy', 'inactive', 'tired', 'depressed')):
                notes.append(
                    f"{name}'s reported lethargic behavior may indicate the condition is progressing — "
                    "don't delay the vet visit."
                )

    return {
        'disease': disease,
        'confidence': round(confidence, 1),
        'description': disease_data.get('description', _FALLBACK_INFO['description']),
        'care_tips': care_tips,
        'severity': severity,
        'personalized_notes': notes,
    }


# ── Severity badge helper (Jinja2 filter) ─────────────────────────────────
@app.template_filter('severity_class')
def severity_class(sev):
    s = (sev or '').lower()
    if 'critical' in s or 'emergency' in s:
        return 'badge-critical'
    if 'serious' in s:
        return 'badge-serious'
    if 'moderate' in s:
        return 'badge-moderate'
    if 'mild' in s:
        return 'badge-mild'
    if 'none' in s:
        return 'badge-none'
    return 'badge-moderate'


# ══════════════════════════════════════════════════════════════════════════
# ROUTES — AUTH
# ══════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not all([username, email, password]):
            flash('All fields are required.', 'error')
        elif password != confirm:
            flash('Passwords do not match.', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
        elif User.query.filter(
            (User.username == username) | (User.email == email)
        ).first():
            flash('Username or email already in use.', 'error')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome, {username}! Add your first pet to get started.', 'success')
            return redirect(url_for('dashboard'))
    return render_template('auth/signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username/email or password.', 'error')
    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ══════════════════════════════════════════════════════════════════════════
# ROUTES — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user()
    pets = Pet.query.filter_by(user_id=user.id).order_by(Pet.created_at.desc()).all()
    recent = (
        Prediction.query
        .filter_by(user_id=user.id)
        .order_by(Prediction.created_at.desc())
        .limit(5)
        .all()
    )
    pred_count = Prediction.query.filter_by(user_id=user.id).count()
    return render_template('dashboard.html', user=user, pets=pets,
                           recent=recent, pred_count=pred_count)


# ══════════════════════════════════════════════════════════════════════════
# ROUTES — PETS
# ══════════════════════════════════════════════════════════════════════════

@app.route('/pets')
@login_required
def pets_list():
    user = current_user()
    pets = Pet.query.filter_by(user_id=user.id).order_by(Pet.name).all()
    return render_template('pets/list.html', pets=pets)


@app.route('/pets/add', methods=['GET', 'POST'])
@login_required
def pets_add():
    user = current_user()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Pet name is required.', 'error')
        else:
            pet = Pet(
                user_id=user.id,
                name=name,
                breed=request.form.get('breed', '').strip() or None,
                age=request.form.get('age') or None,
                weight=request.form.get('weight') or None,
                height=request.form.get('height') or None,
                past_diseases=request.form.get('past_diseases', '').strip() or None,
                allergies=request.form.get('allergies', '').strip() or None,
                behavior=request.form.get('behavior', '').strip() or None,
            )
            db.session.add(pet)
            db.session.commit()
            flash(f'{pet.name} has been added to your pets!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('pets/form.html', pet=None, action='Add')


@app.route('/pets/<int:pet_id>')
@login_required
def pets_detail(pet_id):
    user = current_user()
    pet = Pet.query.filter_by(id=pet_id, user_id=user.id).first_or_404()
    raw = (
        Prediction.query
        .filter_by(pet_id=pet.id)
        .order_by(Prediction.created_at.desc())
        .limit(10)
        .all()
    )
    predictions = []
    for p in raw:
        p.care_tips_list = json.loads(p.care_tips) if p.care_tips else []
        p.notes_list = json.loads(p.personalized_notes) if p.personalized_notes else []
        predictions.append(p)
    return render_template('pets/detail.html', pet=pet, predictions=predictions)


@app.route('/pets/<int:pet_id>/edit', methods=['GET', 'POST'])
@login_required
def pets_edit(pet_id):
    user = current_user()
    pet = Pet.query.filter_by(id=pet_id, user_id=user.id).first_or_404()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Pet name is required.', 'error')
        else:
            pet.name = name
            pet.breed = request.form.get('breed', '').strip() or None
            pet.age = request.form.get('age') or None
            pet.weight = request.form.get('weight') or None
            pet.height = request.form.get('height') or None
            pet.past_diseases = request.form.get('past_diseases', '').strip() or None
            pet.allergies = request.form.get('allergies', '').strip() or None
            pet.behavior = request.form.get('behavior', '').strip() or None
            db.session.commit()
            flash(f'{pet.name} updated successfully!', 'success')
            return redirect(url_for('pets_detail', pet_id=pet.id))
    return render_template('pets/form.html', pet=pet, action='Edit')


@app.route('/pets/<int:pet_id>/delete', methods=['POST'])
@login_required
def pets_delete(pet_id):
    user = current_user()
    pet = Pet.query.filter_by(id=pet_id, user_id=user.id).first_or_404()
    name = pet.name
    db.session.delete(pet)
    db.session.commit()
    flash(f'{name} has been removed.', 'info')
    return redirect(url_for('pets_list'))


# ══════════════════════════════════════════════════════════════════════════
# ROUTES — DIAGNOSIS
# ══════════════════════════════════════════════════════════════════════════

@app.route('/diagnose', methods=['GET', 'POST'])
@app.route('/diagnose/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def diagnose(pet_id=None):
    user = current_user()
    pets = Pet.query.filter_by(user_id=user.id).order_by(Pet.name).all()
    selected_pet = None
    if pet_id:
        selected_pet = Pet.query.filter_by(id=pet_id, user_id=user.id).first()

    if request.method == 'POST':
        symptoms = request.form.get('symptoms', '').strip()
        chosen_pet_id = request.form.get('pet_id', '')
        pet = None
        if chosen_pet_id:
            pet = Pet.query.filter_by(id=int(chosen_pet_id), user_id=user.id).first()

        if not symptoms:
            flash("Please describe your dog's symptoms.", 'error')
        else:
            result = get_personalized_prediction(symptoms, pet)
            pred = Prediction(
                user_id=user.id,
                pet_id=pet.id if pet else None,
                symptoms=symptoms,
                disease=result['disease'],
                confidence=result['confidence'],
                description=result['description'],
                severity=result['severity'],
                care_tips=json.dumps(result['care_tips']),
                personalized_notes=json.dumps(result['personalized_notes']),
            )
            db.session.add(pred)
            db.session.commit()
            return render_template(
                'result.html',
                result=result,
                pet=pet,
                symptoms=symptoms,
                prediction_id=pred.id,
            )

    return render_template('diagnose.html', pets=pets, selected_pet=selected_pet)


@app.route('/history')
@login_required
def history():
    user = current_user()
    raw = (
        Prediction.query
        .filter_by(user_id=user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
    predictions = []
    for p in raw:
        p.care_tips_list = json.loads(p.care_tips) if p.care_tips else []
        p.notes_list = json.loads(p.personalized_notes) if p.personalized_notes else []
        predictions.append(p)
    return render_template('history.html', predictions=predictions)


# ══════════════════════════════════════════════════════════════════════════
# ROUTES — LEGACY JSON API (React frontend compatibility)
# ══════════════════════════════════════════════════════════════════════════

@app.route('/predict-symptom', methods=['POST'])
def predict_symptom_api():
    try:
        data = request.get_json() or {}
        symptoms = data.get('symptoms', '').strip()
        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        result = get_personalized_prediction(symptoms)
        return jsonify({'success': True, **result})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


@app.route('/predict-image', methods=['POST'])
def predict_image_api():
    try:
        if not HAS_ML or _ip is None:
            return jsonify({'error': 'Image prediction not available'}), 503
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        image_file = request.files['image']
        if not image_file.filename:
            return jsonify({'error': 'No image selected'}), 400
        ext = image_file.filename.rsplit('.', 1)[-1].lower()
        if ext not in {'png', 'jpg', 'jpeg', 'gif', 'bmp'}:
            return jsonify({'error': 'Invalid file type'}), 400
        prediction = _ip.predict(image_file)
        disease_data = get_disease_info(prediction['disease'])
        care_tips = disease_data.get('care_tips', [])
        if isinstance(care_tips, str):
            care_tips = [care_tips]
        return jsonify({
            'success': True,
            'disease': str(prediction['disease']),
            'confidence': float(prediction['confidence']),
            'description': disease_data.get('description', ''),
            'care_tips': care_tips,
            'severity': disease_data.get('severity', 'Unknown'),
        })
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


# ══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

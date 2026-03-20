# AI Dog Health Diagnosis System

A complete machine learning web application for diagnosing dog health issues using symptom analysis and image recognition.

## Features

- **Symptom-Based Diagnosis**: Enter symptoms to get potential disease predictions
- **Image-Based Detection**: Upload photos to detect skin conditions and parasites
- **Disease Information**: Get detailed descriptions and care tips
- **Nearby Vets**: Find veterinary clinics on Google Maps
- **ML Models**: Trained RandomForest and CNN models

## Installation

1. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Google Maps Setup (Optional)

To enable the nearby veterinary clinics feature:

1. Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Maps JavaScript API and Places API
3. Replace `YOUR_API_KEY` in `templates/index.html` with your actual API key

## Project Structure

```
project/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── models/               # Trained ML models (auto-generated)
├── templates/            # HTML templates
│   └── index.html
├── static/               # CSS and JavaScript
│   ├── style.css
│   └── script.js
├── utils/                # ML utilities
│   ├── symptom_predictor.py
│   ├── image_predictor.py
│   └── disease_info.py
└── data/                 # Training datasets
    └── symptoms_dataset.csv
```

## How It Works

### Symptom Prediction
- Uses TF-IDF vectorization to process symptom text
- RandomForest classifier trained on symptom-disease pairs
- Returns disease prediction with confidence score

### Image Prediction
- CNN model with 3 convolutional layers
- Classifies images into: Healthy, Skin Infection, or Ticks
- Input images resized to 128x128 pixels

### Auto-Training
Models are automatically trained on first run if not found in the `models/` directory.

## Supported Diseases

The system can diagnose 20+ common dog health conditions including:
- Parvovirus
- Distemper
- Kennel Cough
- Skin Allergies
- Arthritis
- Diabetes
- And more...

## Disclaimer

This tool is for informational purposes only and is NOT a substitute for professional veterinary care. Always consult a licensed veterinarian for accurate diagnosis and treatment.

## Technologies Used

- **Backend**: Flask (Python)
- **ML**: scikit-learn, TensorFlow/Keras
- **Frontend**: HTML, CSS, JavaScript
- **Maps**: Google Maps API

# Quick Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Step-by-Step Installation

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

**On Linux/Mac:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Note: TensorFlow installation may take a few minutes.

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

Navigate to: `http://localhost:5000`

## First Run

On the first run, the application will:
- Automatically train the symptom prediction model
- Build and save the CNN image classification model
- Save models in the `models/` directory

This process takes 1-2 minutes.

## Google Maps API (Optional)

To enable the "Find Nearby Vets" feature:

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable these APIs:
   - Maps JavaScript API
   - Places API
4. Create credentials (API Key)
5. Copy your API key
6. Open `templates/index.html`
7. Replace `YOUR_API_KEY` on line 103 with your actual API key

Example:
```html
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyABC123...&libraries=places"></script>
```

## Troubleshooting

### TensorFlow Installation Issues

If you encounter TensorFlow installation errors:

**For CPU-only version:**
```bash
pip install tensorflow-cpu==2.15.0
```

**For Apple Silicon (M1/M2) Macs:**
```bash
pip install tensorflow-macos==2.15.0
```

### Port Already in Use

If port 5000 is already in use, edit `app.py` line 79:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change to any available port
```

### Models Not Training

Ensure the `data/symptoms_dataset.csv` file exists and contains data.

## Usage Examples

### Symptom Diagnosis

Enter symptoms separated by commas:
```
lethargy, vomiting, loss of appetite
```

### Image Diagnosis

Upload a clear photo of your dog showing:
- Overall body condition
- Skin conditions
- Any visible health issues

## Support

For issues or questions, check:
- README.md for detailed information
- Error messages in the terminal
- Browser console for frontend errors

# Usage Guide - AI Dog Health Diagnosis System

## Getting Started

After installation, run the application:

```bash
python app.py
```

You should see:
```
Initializing models...
Training symptom prediction model...
Model trained with accuracy: 0.XX
Model saved successfully!
Building image classification model...
Model built and saved successfully!
Models initialized successfully!
 * Running on http://0.0.0.0:5000
```

Open your browser to: `http://localhost:5000`

## Using Symptom-Based Diagnosis

### Step 1: Observe Your Dog

Look for common symptoms:
- Behavioral changes (lethargy, aggression)
- Digestive issues (vomiting, diarrhea)
- Respiratory problems (coughing, sneezing)
- Physical symptoms (limping, itching)
- Changes in appetite or thirst
- Unusual discharge or odor

### Step 2: Enter Symptoms

In the "Symptom-Based Diagnosis" card, enter symptoms separated by commas:

**Examples:**

```
lethargy, vomiting, loss of appetite
```

```
coughing, sneezing, nasal discharge
```

```
itching, redness, hair loss
```

```
limping, swelling, pain
```

### Step 3: Analyze

Click "Analyze Symptoms" button. The system will:
1. Process your input
2. Predict the most likely disease
3. Display results with confidence score

### Step 4: Review Results

The results show:
- **Disease Name**: Predicted condition
- **Confidence**: Accuracy percentage
- **Severity**: Risk level (Critical, Serious, Moderate, Mild)
- **Description**: What the disease is
- **Care Tips**: What you should do
- **Nearby Vets**: Clinics on map (if Maps API configured)

## Using Image-Based Diagnosis

### Step 1: Take a Good Photo

**Photo Tips:**
- Use good lighting (natural light is best)
- Focus on the affected area
- Keep the image clear and in focus
- Show skin conditions, wounds, or parasites
- Avoid blurry or dark images

**What to Photograph:**
- Skin rashes or lesions
- Hair loss areas
- Visible parasites (ticks, fleas)
- Swollen or inflamed areas
- Any visible abnormalities

### Step 2: Upload Image

1. Click "Choose an image" button
2. Select a photo from your device
3. Preview will appear automatically

**Supported formats:**
- PNG
- JPG/JPEG
- GIF
- BMP

**File size limit:** 16MB

### Step 3: Analyze

Click "Analyze Image" button. The system will:
1. Upload and process the image
2. Resize to 128x128 for analysis
3. Run through CNN model
4. Predict condition

### Step 4: Review Results

Results include:
- Condition classification (Healthy, Skin Infection, Ticks)
- Confidence percentage
- Recommended care actions

## Understanding Results

### Confidence Scores

- **90-100%**: Very high confidence
- **70-89%**: High confidence
- **50-69%**: Moderate confidence
- **Below 50%**: Low confidence (consult vet immediately)

### Severity Levels

**Critical Emergency** 🔴
- Seek immediate veterinary care
- Life-threatening conditions
- Examples: Rabies, Gastric Dilatation, Parvovirus

**Serious** 🟠
- Urgent veterinary attention needed
- Requires ongoing medical management
- Examples: Diabetes, Heart Disease, Liver Disease

**Moderate** 🟡
- Veterinary consultation recommended
- May need medication or treatment
- Examples: Ear Infection, UTI, Gastroenteritis

**Mild to Moderate** 🟢
- Monitor and consult vet if worsens
- Often manageable with care
- Examples: Dental Disease, Skin Allergy

## Finding Nearby Vets

### Automatic Location (Recommended)

1. Allow location access when prompted
2. Your location appears as blue dot on map
3. Nearby vets shown with red markers
4. Click markers for clinic information

### Using the Clinic List

Below the map, you'll see:
- Clinic name
- Address
- Rating and reviews (if available)

**Click any clinic** to:
- Center map on that location
- Zoom in for details
- See more information

## Common Symptoms Reference

### Digestive System
- Vomiting
- Diarrhea
- Loss of appetite
- Weight loss
- Bloating
- Blood in stool

### Respiratory System
- Coughing
- Sneezing
- Difficulty breathing
- Nasal discharge
- Wheezing

### Skin & Coat
- Itching
- Redness
- Hair loss
- Scabs
- Flaky skin
- Bumps or lumps

### Behavioral
- Lethargy
- Aggression
- Confusion
- Excessive salivation
- Restlessness

### Mobility
- Limping
- Stiffness
- Swelling
- Pain when touched
- Reluctance to move

### Urinary
- Frequent urination
- Straining to urinate
- Blood in urine
- Accidents indoors
- Excessive thirst

## Example Scenarios

### Scenario 1: Skin Issue

**Observation:** Your dog is scratching constantly, has red skin, and losing hair in patches.

**Action:**
1. Use symptom diagnosis: "itching, redness, hair loss"
2. OR take a clear photo of affected skin
3. Upload to image diagnosis

**Possible Results:**
- Skin Allergy
- Mange
- Flea Infestation

### Scenario 2: Digestive Problem

**Observation:** Dog hasn't eaten in 2 days, vomiting, seems tired.

**Action:**
1. Enter symptoms: "loss of appetite, vomiting, lethargy"
2. Click Analyze Symptoms

**Possible Results:**
- Parvovirus
- Gastroenteritis
- Liver Disease

### Scenario 3: Respiratory Issue

**Observation:** Dog is coughing and sneezing, has runny nose.

**Action:**
1. Enter: "coughing, sneezing, nasal discharge"
2. Review care recommendations

**Possible Results:**
- Kennel Cough
- Upper Respiratory Infection

## Best Practices

### DO:
✅ Enter specific, observable symptoms
✅ Use clear, well-lit photos
✅ Follow care tips provided
✅ Consult a vet for serious conditions
✅ Use as a preliminary screening tool
✅ Monitor your dog's condition

### DON'T:
❌ Delay emergency veterinary care
❌ Use as sole diagnostic tool
❌ Self-medicate without vet approval
❌ Ignore critical severity warnings
❌ Upload unclear or irrelevant images
❌ Treat this as professional medical advice

## When to See a Vet Immediately

Regardless of app results, seek immediate veterinary care if:

- Difficulty breathing
- Seizures or collapse
- Severe bleeding
- Inability to urinate
- Suspected poisoning
- Extreme lethargy
- High fever
- Severe pain
- Rapid deterioration
- Any "Critical Emergency" result

## Troubleshooting

### "No symptoms provided" error
- Make sure you entered text in the symptom field
- Don't leave the field empty

### "No image provided" error
- Click "Choose an image" and select a file
- Ensure the file is an image format

### "Invalid file type" error
- Use PNG, JPG, JPEG, GIF, or BMP
- Don't upload videos or documents

### Map not showing
- Check if you added Google Maps API key
- Allow location access in browser
- Check internet connection

### Low confidence results
- Try adding more specific symptoms
- Use a clearer image
- Consult a vet for accurate diagnosis

## Privacy & Data

- No data is stored permanently
- Images are processed in memory only
- No personal information collected
- No tracking or analytics
- Results are not saved

## Disclaimer

⚠️ **IMPORTANT**: This application is an educational tool and should NOT replace professional veterinary care. Always consult a licensed veterinarian for:

- Accurate diagnosis
- Treatment plans
- Medication prescriptions
- Emergency situations
- Ongoing health management

The AI models are trained on limited datasets and may not cover all conditions or variations.

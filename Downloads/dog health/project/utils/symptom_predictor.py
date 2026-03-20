import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

class SymptomPredictor:
    def __init__(self, model_path='models/symptom_model.pkl', vectorizer_path='models/vectorizer.pkl'):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = None
        self.vectorizer = None

        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            self.load_model()
        else:
            self.train_model()

    def train_model(self):
        """Train the symptom-based disease prediction model"""
        print("Training symptom prediction model...")

        df = pd.read_csv('data/symptoms_dataset.csv')

        self.vectorizer = TfidfVectorizer(max_features=100)
        X = self.vectorizer.fit_transform(df['symptoms'])
        y = df['disease']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        accuracy = self.model.score(X_test, y_test)
        print(f"Model trained with accuracy: {accuracy:.2f}")

        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
        print("Model saved successfully!")

    def load_model(self):
        """Load the trained model"""
        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)
        print("Model loaded successfully!")

    def predict(self, symptoms):
        """Predict disease based on symptoms"""
        symptoms_processed = symptoms.lower().replace(' ', '_')

        X = self.vectorizer.transform([symptoms_processed])

        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        confidence = max(probabilities) * 100

        return {
            'disease': prediction,
            'confidence': round(confidence, 2)
        }

    def get_top_predictions(self, symptoms, top_n=3):
        """Get top N predictions with probabilities"""
        symptoms_processed = symptoms.lower().replace(' ', '_')

        X = self.vectorizer.transform([symptoms_processed])

        probabilities = self.model.predict_proba(X)[0]
        classes = self.model.classes_

        top_indices = np.argsort(probabilities)[-top_n:][::-1]

        results = []
        for idx in top_indices:
            results.append({
                'disease': classes[idx],
                'confidence': round(probabilities[idx] * 100, 2)
            })

        return results

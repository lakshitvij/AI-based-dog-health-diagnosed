import os
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from PIL import Image
import io

class ImagePredictor:
    def __init__(self, model_path='models/cnn_model.h5'):
        self.model_path = model_path
        self.img_size = (128, 128)
        self.classes = ['Healthy', 'Skin Infection', 'Ticks']
        self.model = None

        if os.path.exists(model_path):
            self.load_model()
        else:
            self.build_and_train_model()

    def build_and_train_model(self):
        """Build and train a simple CNN model"""
        print("Building image classification model...")

        model = keras.Sequential([
            layers.Input(shape=(128, 128, 3)),
            layers.Conv2D(32, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(len(self.classes), activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        print("Creating synthetic training data...")
        X_train = np.random.rand(100, 128, 128, 3)
        y_train = np.random.randint(0, len(self.classes), 100)

        model.fit(X_train, y_train, epochs=5, batch_size=10, verbose=0)

        os.makedirs('models', exist_ok=True)
        model.save(self.model_path)
        self.model = model
        print("Model built and saved successfully!")

    def load_model(self):
        """Load the trained model"""
        self.model = keras.models.load_model(self.model_path)
        print("Image model loaded successfully!")

    def preprocess_image(self, image_file):
        """Preprocess image for prediction"""
        img = Image.open(io.BytesIO(image_file.read()))

        if img.mode != 'RGB':
            img = img.convert('RGB')

        img = img.resize(self.img_size)

        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        return img_array

    def predict(self, image_file):
        """Predict condition from image"""
        img_array = self.preprocess_image(image_file)

        predictions = self.model.predict(img_array, verbose=0)
        predicted_class_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_class_idx]) * 100

        return {
            'disease': str(self.classes[predicted_class_idx]),
            'confidence': round(confidence, 2)
        }

    def get_all_predictions(self, image_file):
        """Get all predictions with probabilities"""
        img_array = self.preprocess_image(image_file)

        predictions = self.model.predict(img_array, verbose=0)

        results = []
        for idx, prob in enumerate(predictions[0]):
            results.append({
                'disease': str(self.classes[idx]),
                'confidence': round(float(prob) * 100, 2)
            })

        results.sort(key=lambda x: x['confidence'], reverse=True)

        return results

"""
Flask service for ML prediction
This service handles sign language detection predictions
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import base64
from keras.models import load_model
from cvzone.HandTrackingModule import HandDetector
import os
import sys

app = Flask(__name__)
CORS(app)

# Global variables for model and detector
model = None
hd = None
hd2 = None
offset = 29

# Load model on startup
def load_ml_model():
    global model, hd, hd2
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'cnn8grps_rad1_model.h5')
        if not os.path.exists(model_path):
            print(f"Warning: Model file not found at {model_path}")
            return False
        model = load_model(model_path)
        hd = HandDetector(maxHands=1)
        hd2 = HandDetector(maxHands=1)
        print("ML model loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

# Initialize on startup
load_ml_model()

def predict_from_image(image_array):
    """
    Predict sign language letter from image array
    Returns prediction string and confidence
    """
    if model is None:
        return None, 0.0
    
    try:
        # Resize to 400x400 if needed
        if image_array.shape[:2] != (400, 400):
            image_array = cv2.resize(image_array, (400, 400))
        
        # Prepare image for model
        white = image_array.reshape(1, 400, 400, 3)
        prob = np.array(model.predict(white, verbose=0)[0], dtype='float32')
        ch1_idx = np.argmax(prob, axis=0)
        confidence = float(prob[ch1_idx])
        
        # Map index to letter (simplified - you may need to adjust based on your model)
        letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if 0 <= ch1_idx < len(letters):
            prediction = letters[ch1_idx]
        else:
            prediction = 'UNKNOWN'
        
        return prediction, confidence
    except Exception as e:
        print(f"Prediction error: {e}")
        return None, 0.0

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model_loaded': model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Expect base64 encoded image
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_data = data['image']
        if image_data.startswith('data:image'):
            # Remove data URL prefix
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Get prediction
        prediction, confidence = predict_from_image(image)
        
        if prediction is None:
            return jsonify({'error': 'Prediction failed'}), 500
        
        return jsonify({
            'prediction': prediction,
            'confidence': confidence
        })
    except Exception as e:
        print(f"Error in predict endpoint: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)


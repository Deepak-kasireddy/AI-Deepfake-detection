import tensorflow as tf
import os
from utils.image_preprocess import preprocess_image
from config import IMAGE_MODEL_PATH

# Load model with error handling
_model = None

def load_model():
    global _model
    if _model is None and os.path.exists(IMAGE_MODEL_PATH):
        try:
            _model = tf.keras.models.load_model(IMAGE_MODEL_PATH)
        except Exception as e:
            print(f"Warning: Could not load image model: {e}")

# Initial load
load_model()

def detect_image(file):
    if file is None:
        return {
            "result": "No image provided",
            "confidence": 0,
            "issues": ["No image to analyze"]
        }
    
    try:
        # Ensure model is loaded
        load_model()
        
        img = preprocess_image(file)
        
        if _model is None:
            return {
                "result": "Model Missing",
                "confidence": 0.5,
                "issues": [f"Image model file not found at {IMAGE_MODEL_PATH}"]
            }
        
        preds = _model.predict(img, verbose=0)
        pred = float(preds[0][0]) # Probability of "AI-Generated"
        
        # NaN check for pred
        if pred != pred:
            pred = 0.5
            
        result = "AI-Generated" if pred > 0.5 else "Real"
        
        # Ensure confidence is a valid float and not NaN
        try:
            conf_val = float(pred if result == "AI-Generated" else 1 - pred)
            confidence = conf_val if conf_val == conf_val else 0.5
        except (TypeError, ValueError):
            confidence = 0.5

        return {
            "result": result,
            "confidence": float(confidence),
            "issues": [
                "Possible GAN artifacts" if result == "AI-Generated" else "Natural textures",
                "Compression consistency"
            ]
        }
    except Exception as e:
        import traceback
        print(f"Error in detect_image: {e}")
        print(traceback.format_exc())
        return {
            "result": "Error",
            "confidence": 0,
            "issues": [f"Image detection error: {str(e)}"]
        }
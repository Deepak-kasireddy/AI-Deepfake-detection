import joblib
import os
from config import TEXT_MODEL_PATH, VECTORIZER_PATH
from utils.text_preprocess import clean_text

# Load models with error handling
_model = None
_vectorizer = None

def load_models():
    global _model, _vectorizer
    if _model is None and os.path.exists(TEXT_MODEL_PATH):
        try:
            _model = joblib.load(TEXT_MODEL_PATH)
        except Exception as e:
            print(f"Warning: Could not load text model: {e}")

    if _vectorizer is None and os.path.exists(VECTORIZER_PATH):
        try:
            _vectorizer = joblib.load(VECTORIZER_PATH)
        except Exception as e:
            print(f"Warning: Could not load vectorizer: {e}")

# Initial load
load_models()

def find_sources(text):
    """
    Generate search links and potential sources for the given text.
    In a real app, this would use a News API.
    """
    query = text[:100].replace(' ', '+')
    return [
        {"name": "Google News Search", "url": f"https://www.google.com/search?q={query}&tbm=nws"},
        {"name": "Reuters News", "url": f"https://www.reuters.com/search/news?blob={query}"},
        {"name": "Associated Press", "url": f"https://apnews.com/search?q={query}"}
    ]

def detect_text(text):
    if not text or not isinstance(text, str):
        return {
            "result": "No text provided",
            "confidence": 0,
            "sources": [],
            "issues": ["No text to analyze"]
        }
    
    try:
        # Ensure models are loaded
        load_models()
        
        text_clean = clean_text(text)
        sources = find_sources(text)
        
        if _model is None or _vectorizer is None:
            return {
                "result": "Model Missing",
                "confidence": 0.5,
                "sources": sources,
                "issues": [f"Text model or vectorizer file not found at {TEXT_MODEL_PATH}"]
            }
        
        # Check vectorizer specifically for transform attribute to prevent 'NoneType' error
        if not hasattr(_vectorizer, 'transform'):
             return {
                "result": "Load Error",
                "confidence": 0.5,
                "sources": sources,
                "issues": ["Vectorizer loaded but is invalid (missing 'transform' method)"]
            }

        vec = _vectorizer.transform([text_clean])
        pred = _model.predict(vec)[0]
        probs = _model.predict_proba(vec)[0]
        
        is_real = (pred == 'real' or pred == 1)
        result = "Real" if is_real else "Fake"
        
        # Ensure confidence is a valid float and not NaN
        try:
            conf_val = float(probs[1] if is_real else probs[0])
            # NaN check
            confidence = conf_val if conf_val == conf_val else 0.5
        except (IndexError, TypeError, ValueError):
            confidence = 0.5

        return {
            "result": result,
            "confidence": float(confidence),
            "sources": sources,
            "issues": [
                "Clickbait language" if not is_real else "High credibility",
                "Source indicators"
            ]
        }
    except Exception as e:
        import traceback
        print(f"Error in detect_text: {e}")
        print(traceback.format_exc())
        return {
            "result": "Error",
            "confidence": 0,
            "sources": [],
            "issues": [f"Text detection error: {str(e)}"]
        }
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import joblib
import os
import config
from services.source_checker import SourceChecker
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../fronted')), static_url_path='/')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Load models and services
image_model = None
text_model = None
vectorizer = None
source_checker = SourceChecker()

def load_models():
    global image_model, text_model, vectorizer
    if os.path.exists(config.IMAGE_MODEL_PATH):
        try:
            image_model = tf.keras.models.load_model(config.IMAGE_MODEL_PATH)
            print("Image model loaded successfully.")
        except Exception as e:
            print(f"Warning: Could not load image model. It may be currently training or corrupted. Error: {e}")
            
    if os.path.exists(config.TEXT_MODEL_PATH):
        try:
            text_model = joblib.load(config.TEXT_MODEL_PATH)
            print("Text model loaded successfully.")
        except Exception as e:
            print(f"Warning: Could not load text model. Error: {e}")
            
    if os.path.exists(config.VECTORIZER_PATH):
        try:
            vectorizer = joblib.load(config.VECTORIZER_PATH)
            print("Vectorizer loaded successfully.")
        except Exception as e:
            print(f"Warning: Could not load vectorizer. Error: {e}")

@app.route('/predict/image', methods=['POST'])
def predict_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    # Save temp file
    temp_path = os.path.join(config.BASE_DIR, 'temp_image.jpg')
    file.save(temp_path)
    
    try:
        # Preprocess
        img = image.load_img(temp_path, target_size=config.IMG_SIZE)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0
        
        # Predict
        prediction = image_model.predict(img_array)
        probability = float(prediction[0][0])
        label = "Fake" if probability > 0.5 else "Real"
        confidence = probability if label == "Fake" else 1 - probability
        
        return jsonify({
            'label': label,
            'confidence': round(confidence * 100, 2),
            'probability': probability
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.route('/predict/text', methods=['POST'])
def predict_text():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
        
    text = data['text']
    
    try:
        # Vectorize
        text_tfidf = vectorizer.transform([text])
        
        # Predict
        prediction = text_model.predict(text_tfidf)
        probability = text_model.predict_proba(text_tfidf)[0][1]
        
        label = "Fake" if prediction[0] == 1 else "Real"
        confidence = probability if label == "Fake" else 1 - probability
        
        # Get verified sources
        sources = source_checker.generate_search_links(text, is_fake=(label == "Fake"))
        summary = source_checker.get_verification_summary(is_fake=(label == "Fake"))
        
        return jsonify({
            'label': label,
            'confidence': round(confidence * 100, 2),
            'probability': probability,
            'sources': sources,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict/url', methods=['POST'])
def predict_url():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
        
    url = data['url']
    
    try:
        # Fetch URL content
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML and extract text
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from paragraphs (usually where main content is)
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        
        if not text or len(text.strip()) < 50:
            return jsonify({'error': 'Could not extract sufficient text from the URL. Please try pasting the text directly.'}), 400
            
        # Vectorize
        text_tfidf = vectorizer.transform([text])
        
        # Predict
        prediction = text_model.predict(text_tfidf)
        probability = text_model.predict_proba(text_tfidf)[0][1]
        
        label = "Fake" if prediction[0] == 1 else "Real"
        confidence = probability if label == "Fake" else 1 - probability
        
        # Get verified sources
        sources = source_checker.generate_search_links(text, is_fake=(label == "Fake"))
        summary = source_checker.get_verification_summary(is_fake=(label == "Fake"))
        
        return jsonify({
            'label': label,
            'confidence': round(confidence * 100, 2),
            'probability': probability,
            'sources': sources,
            'summary': summary,
            'extracted_text': text[:500] + '...' if len(text) > 500 else text # Send a snippet back for confirmation
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"Failed to fetch URL: {str(e)}"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_models()
    app.run(debug=True, port=5000)

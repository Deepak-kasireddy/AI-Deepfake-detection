from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import traceback
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from services.image_detector import detect_image
    from services.text_detector import detect_text
    from services.source_checker import check_source
    from services.context_checker import check_context
    from services.aggregator import calculate_reality
    print("Successfully imported all services")
except Exception as e:
    print(f"Error importing services: {e}")
    traceback.print_exc()
    # Define stubs so the app starts even if services fail
    def detect_image(*args): return {"result": "Import Error", "confidence": 0}
    def detect_text(*args): return {"result": "Import Error", "confidence": 0, "sources": []}
    def check_source(*args): return {"status": "Error", "score": 0}
    def check_context(*args): return {"issue": "Service initialization failed"}
    def calculate_reality(*args): return 0.0, "System Error"

app = Flask(__name__)
CORS(app)

# Get absolute path for frontend
print(f"Current working directory: {os.getcwd()}")
print(f"File location: {os.path.abspath(__file__)}")

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fronted'))
print(f"Calculated FRONTEND_DIR: {FRONTEND_DIR}")

if not os.path.exists(FRONTEND_DIR):
    print(f"CRITICAL WARNING: Frontend directory NOT FOUND at {FRONTEND_DIR}")
    # Try alternate path just in case
    alt_path = os.path.abspath(os.path.join(os.getcwd(), 'fronted'))
    if os.path.exists(alt_path):
        FRONTEND_DIR = alt_path
        print(f"Found frontend at alternate path: {FRONTEND_DIR}")
    else:
        print("Could not find frontend directory anywhere!")
else:
    print(f"Frontend directory verified at: {FRONTEND_DIR}")
    try:
        print(f"Files in frontend: {os.listdir(FRONTEND_DIR)}")
    except Exception as e:
        print(f"Could not list frontend files: {e}")

# Serve Frontend
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/health', methods=['GET'])
def health():
    print("Health check requested")
    return jsonify({"status": "healthy", "frontend_exists": os.path.exists(FRONTEND_DIR)}), 200

@app.route('/predict/image', methods=['POST'])
def predict_image():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        result = detect_image(file)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/predict/text', methods=['POST'])
def predict_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        text = data['text']
        result = detect_text(text)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/check/source', methods=['POST'])
def check_url_source():
    try:
        data = request.get_json()
        url = data.get('url', '')
        result = check_source(url)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        image = request.files.get("image")
        text = request.form.get("text", "")
        url = request.form.get("url", "")

        image_res = detect_image(image) if image else {"result": "No image", "confidence": 0}
        text_res = detect_text(text) if text else {"result": "No text", "confidence": 0, "sources": []}
        source_res = check_source(url)
        context_res = check_context()

        score, label = calculate_reality(image_res, text_res, source_res)

        return jsonify({
            "score": score,
            "label": label,
            "image": image_res,
            "text": text_res,
            "source": source_res,
            "context": context_res
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

if __name__ == "__main__":
    print("Starting Flask app directly...")
    # Port 7860 is default for Hugging Face
    app.run(debug=True, host='0.0.0.0', port=7860)
---
title: Deepfake Detection
emoji: 🕵️‍♂️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 5000
---

# AI Deepfake Detection

A comprehensive deepfake detection application using Flask, TensorFlow, and machine learning to analyze images, text, and source credibility.

## Features

- 📸 **Image Analysis**: Detect AI-generated and deepfake images using deep learning
- 📝 **Text Analysis**: Identify fake news and manipulated text content  
- 🔗 **Source Verification**: Check URL credibility and source reliability
- 🧠 **Combined Analysis**: Aggregate results from multiple detectors for comprehensive assessment

## Project Structure

```
backend/
  ├── app.py                    # Flask API server
  ├── config.py                 # Configuration settings
  ├── requirements.txt          # Python dependencies
  ├── services/                 # Detection services
  │   ├── image_detector.py
  │   ├── text_detector.py
  │   ├── source_checker.py
  │   ├── context_checker.py
  │   └── aggregator.py
  ├── utils/                    # Utility functions
  │   ├── image_preprocess.py
  │   └── text_preprocess.py
  ├── training/                 # Model training scripts
  ├── models/                   # Trained models
  └── dataset/                  # Training datasets

fronted/
  ├── index.html               # Main UI
  ├── script.js                # Frontend logic
  └── style.css                # Styling
```

## Installation

### Backend Setup

1. **Install Python Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Models**
   - Ensure trained models are in the `models/` directory:
     - `image_model.h5` (TensorFlow Keras model)
     - `text_model.pkl` (scikit-learn model)
     - `vectorizer.pkl` (TfidfVectorizer)

3. **Run the Backend Server**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### Frontend Setup

The frontend is a static HTML application. Simply open `fronted/index.html` in a browser or serve it with:

```bash
cd fronted
python -m http.server 8000
```

Then visit `http://localhost:8000`

## API Endpoints

### Image Detection
```
POST /predict/image
Content-Type: multipart/form-data
Body: file (image file)

Response:
{
  "result": "Real|AI-Generated",
  "confidence": 0.85,
  "issues": [...]
}
```

### Text Detection
```
POST /predict/text
Content-Type: application/json
Body: { "text": "..." }

Response:
{
  "result": "Real|Fake",
  "confidence": 0.75,
  "issues": [...]
}
```

### Source Check
```
POST /check/source
Content-Type: application/json
Body: { "url": "https://..." }

Response:
{
  "status": "Trusted|Unreliable|Unknown",
  "score": 75
}
```

### Combined Analysis
```
POST /analyze
Content-Type: multipart/form-data
Body: image (optional), text (optional), url (optional)

Response:
{
  "score": 65.5,
  "label": "Suspicious",
  "image": {...},
  "text": {...},
  "source": {...},
  "context": {...}
}
```

## Troubleshooting

- **Model files not found**: Train models using scripts in `backend/training/` or use placeholder results
- **Import errors**: Ensure all dependencies in `requirements.txt` are installed
- **CORS issues**: The backend is configured to accept requests from any origin
- **API connection failed**: Make sure backend is running on `http://localhost:5000`

## Training Models

### Train Text Model
```bash
python backend/training/train_text_model.py
```

### Train Image Model
```bash
python backend/training/train_image_model.py
```

## License

MIT

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_MODEL_PATH = os.path.join(BASE_DIR, "models", "image_model.h5")
TEXT_MODEL_PATH = os.path.join(BASE_DIR, "models", "text_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
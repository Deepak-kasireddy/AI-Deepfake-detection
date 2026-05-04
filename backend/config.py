import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dataset Paths
DATASET_DIR = os.path.join(BASE_DIR, 'dataset', 'Dataset')
TRAIN_DIR = os.path.join(DATASET_DIR, 'Train')
TEST_DIR = os.path.join(DATASET_DIR, 'Test')

# Model Paths
MODELS_DIR = os.path.join(BASE_DIR, 'models')
IMAGE_MODEL_PATH = os.path.join(MODELS_DIR, 'image_model.h5')
TEXT_MODEL_PATH = os.path.join(MODELS_DIR, 'text_model.pkl')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'vectorizer.pkl')

# Training Config
IMG_SIZE = (224, 224)
BATCH_SIZE = 8
INITIAL_EPOCHS = 1
FINE_TUNE_EPOCHS = 1
LEARNING_RATE = 1e-3
FINE_TUNE_LR = 1e-5
EPOCHS = INITIAL_EPOCHS + FINE_TUNE_EPOCHS

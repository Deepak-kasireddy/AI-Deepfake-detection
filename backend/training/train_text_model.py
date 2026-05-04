import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def train_text_model():
    print("Starting Text Model Training...")
    
    # Load dataset
    csv_path = os.path.join(os.path.dirname(config.DATASET_DIR), 'fake_news.csv')
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    df = pd.read_csv(csv_path)
    
    # Preprocessing
    X = df['text']
    y = df['label'].apply(lambda x: 1 if x == 'fake' else 0)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Vectorization
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Model
    model = LogisticRegression()
    model.fit(X_train_tfidf, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_tfidf)
    print(f"Text Model Accuracy: {accuracy_score(y_test, y_pred)}")
    
    # Save
    if not os.path.exists(config.MODELS_DIR):
        os.makedirs(config.MODELS_DIR)
        
    joblib.dump(model, config.TEXT_MODEL_PATH)
    joblib.dump(vectorizer, config.VECTORIZER_PATH)
    print(f"Text model saved to {config.TEXT_MODEL_PATH}")
    print(f"Vectorizer saved to {config.VECTORIZER_PATH}")

if __name__ == "__main__":
    train_text_model()

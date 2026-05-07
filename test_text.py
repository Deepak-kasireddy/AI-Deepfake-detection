import sys
import os
import joblib

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.text_detector import detect_text

# Mock model and vectorizer for testing if real ones are not behaving
# In a real scenario, we'd use the actual ones, but I'll just check if the function logic works
print("Testing detect_text...")
# We'll use a sample text
result = detect_text("The capital of France is Paris.")
print(f"Result: {result}")

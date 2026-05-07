import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.aggregator import calculate_reality

# Test cases
test_cases = [
    {
        "name": "Fake Image and Fake Text",
        "image": {"result": "AI-Generated", "confidence": 0.9},
        "text": {"result": "Fake", "confidence": 0.9},
        "source": {"score": 30}, # Unreliable
    },
    {
        "name": "Real Image and Real Text",
        "image": {"result": "Real", "confidence": 0.9},
        "text": {"result": "Real", "confidence": 0.9},
        "source": {"score": 80}, # Trusted
    }
]

for case in test_cases:
    score, label = calculate_reality(case['image'], case['text'], case['source'])
    print(f"Case: {case['name']}")
    print(f"Score: {score}, Label: {label}")
    print("-" * 20)

import os
import shutil
import random

base_path = r"c:\Users\91630\OneDrive\Desktop\AI-Deepfake detection\backend\dataset\Dataset"
test_real_path = os.path.join(base_path, "Test", "Real")
train_real_path = os.path.join(base_path, "Train", "Real")

if not os.path.exists(train_real_path):
    os.makedirs(train_real_path)
    print(f"Created {train_real_path}")

files = os.listdir(test_real_path)
print(f"Found {len(files)} files in {test_real_path}")

# Move 80% to train if train is empty
if len(os.listdir(train_real_path)) == 0:
    num_to_move = int(len(files) * 0.8)
    files_to_move = random.sample(files, num_to_move)
    
    for f in files_to_move:
        shutil.move(os.path.join(test_real_path, f), os.path.join(train_real_path, f))
    
    print(f"Moved {num_to_move} files to {train_real_path}")
else:
    print("Train/Real is not empty, skipping move.")

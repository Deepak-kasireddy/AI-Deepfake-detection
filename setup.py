#!/usr/bin/env python3
"""
Deepfake Detection Setup & Verification Script
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        ('tensorflow', 'tensorflow'),
        ('flask', 'flask'),
        ('flask_cors', 'flask_cors'),
        ('pandas', 'pandas'),
        ('scikit-learn', 'sklearn'),  # Note: may have import issues but is installed
        ('pillow', 'PIL'),
        ('numpy', 'numpy'),
        ('joblib', 'joblib'),
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4')
    ]
    
    missing = []
    for display_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {display_name}")
        except ImportError as e:
            if display_name == 'scikit-learn':
                # Special case: scikit-learn may be installed but have import issues
                try:
                    import subprocess
                    result = subprocess.run([sys.executable, '-c', 'import sklearn'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"✅ {display_name}")
                    else:
                        print(f"⚠️  {display_name} (installed but import fails: {e})")
                        missing.append(display_name)
                except:
                    print(f"⚠️  {display_name} (installed but import fails: {e})")
                    missing.append(display_name)
            else:
                print(f"❌ {display_name}")
                missing.append(display_name)
    
    return len(missing) == 0, missing

def check_models():
    """Check if trained models exist"""
    models_dir = os.path.join(os.path.dirname(__file__), 'backend', 'models')
    models = ['image_model.h5', 'text_model.pkl', 'vectorizer.pkl']
    
    os.makedirs(models_dir, exist_ok=True)
    
    for model in models:
        model_path = os.path.join(models_dir, model)
        if os.path.exists(model_path):
            print(f"✅ {model}")
        else:
            print(f"⚠️  {model} (optional - will use placeholders)")
    
    return True

def check_directories():
    """Check if required directories exist"""
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    required_dirs = ['models', 'services', 'utils', 'training', 'dataset']
    
    for dir_name in required_dirs:
        dir_path = os.path.join(backend_dir, dir_name)
        if os.path.isdir(dir_path):
            print(f"✅ backend/{dir_name}/")
        else:
            print(f"⚠️  backend/{dir_name}/ (missing)")
    
    return True

def install_dependencies(missing):
    """Install missing dependencies"""
    if not missing:
        return True
    
    print("\n" + "="*50)
    print("Installing missing dependencies...")
    print("="*50 + "\n")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    """Run all checks"""
    print("\n" + "="*50)
    print("Deepfake Detection - Setup Verification")
    print("="*50 + "\n")
    
    print("Checking Python version...")
    if not check_python_version():
        sys.exit(1)
    
    print("\nChecking dependencies...")
    deps_ok, missing = check_dependencies()
    
    if not deps_ok:
        print("\n" + "-"*50)
        print("Some dependencies are missing!")
        print("-"*50)
        if input("\nWould you like to install them? (y/n): ").lower() == 'y':
            if not install_dependencies(missing):
                sys.exit(1)
        else:
            print("\nPlease install missing packages manually:")
            print(f"pip install {' '.join(missing)}")
    
    print("\nChecking project structure...")
    check_directories()
    
    print("\nChecking models...")
    check_models()
    
    print("\n" + "="*50)
    print("Setup verification complete!")
    print("="*50)
    print("\nTo start the backend server, run:")
    print("  cd backend")
    print("  python app.py")
    print("\nThen open frontend/index.html in your browser")
    print()

if __name__ == '__main__':
    main()

# Setup Guide

## Quick Start

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Train or Get Models

Models need to exist in `backend/models/`:
- `image_model.h5` - TensorFlow/Keras model for image detection
- `text_model.pkl` - Scikit-learn model for text detection  
- `vectorizer.pkl` - TF-IDF vectorizer for text preprocessing

**Option A: Train Models**
```bash
cd backend/training

# Train text model
python train_text_model.py

# Train image model (requires dataset)
python train_image_model.py
```

**Option B: Use Placeholder Models**
The app will work with placeholder results if models aren't available.

### 3. Run Backend Server

```bash
cd backend
python app.py
```

Server will be available at: `http://localhost:5000`

### 4. Open Frontend

```bash
# Option 1: Direct file
Open `fronted/index.html` in your browser

# Option 2: Python HTTP Server
cd fronted
python -m http.server 8000
# Then visit http://localhost:8000
```

## Fixed Issues

✅ **Frontend-Backend API Communication**
- Fixed endpoint mismatch between HTML IDs and JavaScript event listeners
- Aligned API endpoints with backend routes
- Added proper error handling in API calls

✅ **HTML/JS Element IDs**
- Updated all HTML element IDs to match JavaScript selectors
- Fixed button IDs (e.g., `scan-image-btn` instead of `scan-image`)
- Fixed input IDs and container references

✅ **Error Handling**
- Added error handling for missing model files
- Added graceful fallbacks when models aren't loaded
- Added try-catch blocks in all service modules

✅ **Backend Improvements**
- Enhanced Flask app with proper error handling
- Added health check endpoint
- Fixed path handling in config.py
- Added CORS support
- Improved request validation

✅ **UI/UX**
- Created comprehensive CSS styling
- Added drag-and-drop image upload
- Added progress bars and result displays
- Responsive design for mobile devices

## Testing

### Test Image Analysis
1. Go to frontend
2. Drop/select an image
3. Click "Scan Image"
4. View results

### Test Text Analysis
1. Paste text or URL
2. Click "Scan Text"
3. View results

### Test Source Check
1. Enter a URL
2. Click "Check Source"
3. View trust score

### Test Combined Analysis
1. Fill in any/all fields
2. Click "Analyze All"
3. View combined results

## Troubleshooting

**Issue: "Cannot GET /predict/image"**
- Make sure backend is running at `http://localhost:5000`
- Check that `API_BASE` in script.js points to correct URL

**Issue: Model loading errors**
- Models are optional - app works with placeholder results
- To use real models, place them in `backend/models/`
- See training section above

**Issue: CORS errors**
- Backend has CORS enabled
- Make sure you're accessing from a valid origin
- Check browser console for specific CORS error

**Issue: Import errors in backend**
- Ensure all packages installed: `pip install -r requirements.txt`
- Use Python 3.8+
- Consider using virtual environment

## Next Steps

1. Collect training data for better model accuracy
2. Train models with your dataset
3. Fine-tune model hyperparameters
4. Deploy to production (Docker/Render/Heroku)

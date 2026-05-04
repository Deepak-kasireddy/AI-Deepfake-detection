FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend and frontend code
COPY backend/ ./backend/
COPY fronted/ ./fronted/

# Set working directory to backend where app.py is located
WORKDIR /app/backend

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Command to run the application using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]

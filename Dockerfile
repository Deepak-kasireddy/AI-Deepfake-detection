FROM python:3.10

WORKDIR /app

# Skipping apt-get update to bypass transient network error 100 on build server
# The app uses PIL/Pillow which should work with standard libraries

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Set working directory to backend
WORKDIR /app/backend

# Expose port 7860
EXPOSE 7860

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "300", "--workers", "1", "--threads", "8", "app:app"]

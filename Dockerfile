FROM python:3.11-slim

# Install system packages needed by Tesseract & PDF processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Gradio port
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]

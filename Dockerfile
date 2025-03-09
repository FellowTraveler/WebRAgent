FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary data directories
RUN mkdir -p data/collections data/documents data/uploads

# Set environment variables
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1
ENV DOCKER_ENV=true

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["python", "run.py"]
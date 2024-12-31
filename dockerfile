FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install numpy first to avoid compatibility issues
RUN pip install --no-cache-dir numpy==1.23.5

# Install other dependencies and spaCy model
RUN pip install --no-cache-dir spacy && python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY ./app /app/app
COPY ./static /app/static

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

EXPOSE 8000

# Command to run the application
CMD ["python", "app/main.py"]

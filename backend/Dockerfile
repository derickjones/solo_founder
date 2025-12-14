# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for compilation
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements-unified.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy search engine code
COPY search/ .

# Copy CFM content data
COPY scripts/content/ ./scripts/content/

# Copy FAISS index files
COPY search/indexes/ ./indexes/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Cloud Run will set PORT automatically
ENV PORT=8080

# Expose the port
EXPOSE $PORT

# Run the FastAPI server with longer timeout for startup
CMD exec uvicorn api:app --host 0.0.0.0 --port $PORT --workers 1 --timeout-keep-alive 65
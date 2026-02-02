# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file (if exists)
COPY requirements.txt* ./

# Install Python dependencies
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy application code
COPY . .

# Expose port 3015
EXPOSE 3015

# Run the application
# Update this command based on your application framework
# For Flask: CMD ["python", "app.py"]
# For FastAPI: CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3015"]
# For custom: CMD ["python", "app.py"]
CMD ["python", "app.py"]

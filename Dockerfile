# Use lightweight Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files (keeps container clean)
ENV PYTHONDONTWRITEBYTECODE=1

# Ensures logs appear instantly in Docker logs
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies required for PostgreSQL & package compilation
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*  # Remove apt cache to reduce image size

# Copy dependency file first (improves Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . .

# Expose port 8000 inside container
EXPOSE 8000

# Start Django using Gunicorn (production WSGI server)
CMD ["gunicorn", "medibooker.wsgi:application", "--bind", "0.0.0.0:8000"]
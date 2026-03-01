FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY  . .

EXPOSE 8000

# Default command (override in docker-compose if needed)
CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]
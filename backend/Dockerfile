FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    mysql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directories
RUN mkdir -p /app/chroma_data /app/staticfiles

# Run migrations and start server
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

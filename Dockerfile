# Base image with Python
FROM python:3.11-slim

# Working directory inside the container
WORKDIR /app

# Install dependencies first (better build caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Flask listens on this port
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]

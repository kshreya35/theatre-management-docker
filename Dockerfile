# Use official python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (cache optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]

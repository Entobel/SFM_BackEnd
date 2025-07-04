# Base image
FROM python:3.13.3-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run uvicorn (dùng tên file & app đúng)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
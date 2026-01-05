# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt requirements.txt
COPY requirements-fastapi.txt requirements-fastapi.txt

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-fastapi.txt

# Copy project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Set environment variables (optional)
ENV PORT=8000
ENV HOST=0.0.0.0

# Start FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
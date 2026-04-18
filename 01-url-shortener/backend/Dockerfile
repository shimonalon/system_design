FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src
COPY tests ./tests

# Expose port
EXPOSE 8000

# Run FastAPI using uvicorn (run from /app so src/ is importable)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

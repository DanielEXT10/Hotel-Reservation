FROM python:slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY setup.py requirements.txt ./
RUN pip install --no-cache-dir -e .

# Copy only necessary source code
COPY app.py application.py ./
COPY src/ src/
COPY pipeline/ pipeline/
COPY config/ config/
COPY utils/ utils/
COPY templates/ templates/
COPY static/ static/
COPY artifacts/ artifacts/

EXPOSE 8080

# Run the web app only (not training pipeline)
CMD ["python", "app.py"]
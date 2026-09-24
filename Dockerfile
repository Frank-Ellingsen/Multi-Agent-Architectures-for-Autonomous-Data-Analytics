# Multi-Agent Architectures for Autonomous Data Analytics - Containerfile
FROM python:3.11-slim

LABEL maintainer="Frank Ellingsen"
LABEL description="Multi-agent architecture for autonomous data analytics"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000 \
    HOST=0.0.0.0

WORKDIR /app

# Install system utilities including curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create non-root user for security
RUN useradd -m -u 10001 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose ports for Flask API/Web (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Health check against Flask health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/health || exit 1

# Default command starts the Flask web studio
CMD ["python", "api.py"]

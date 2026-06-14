# 🛡️ AI Model Firewall - Corporate / Server Runtime
# For enterprise deployments and microservice integration

FROM python:3.11-slim

LABEL maintainer="AI Model Firewall Team"
LABEL description="Modular AI Model Security Scanner for enterprise use"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Create quarantine directory
RUN mkdir -p /app/quarantine

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command - runs the firewall in monitoring mode
CMD ["python", "main.py"]

# Healthcheck (optional but recommended for orchestration)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Expose no ports by default (file-based tool)
# If you want to turn this into a REST API later, expose 8080 here.
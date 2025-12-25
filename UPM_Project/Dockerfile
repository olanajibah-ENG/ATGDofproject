# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        bash \
        libssl-dev \
        libffi-dev \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Ensure entrypoint is executable and has Unix line endings
RUN chmod +x /app/entrypoint.sh && \
    sed -i 's/\r$//' /app/entrypoint.sh 2>/dev/null || true

# Expose port
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]


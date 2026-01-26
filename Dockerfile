# =========================
# Builder stage
# =========================
FROM python:3.11-slim AS builder

WORKDIR /app

# Avoid writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies (if needed later)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt app/requirements-dev.txt ./
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# =========================
# Runtime stage
# =========================
FROM python:3.11-slim

WORKDIR /app

# Create non-root user with a real home directory
RUN addgroup --system appgroup \
  && adduser --system --ingroup appgroup --home /home/appuser appuser \
  && mkdir -p /home/appuser/.local/share/pomodoro-quest \
  && chown -R appuser:appgroup /home/appuser

# Explicitly set HOME for runtime
ENV HOME=/home/appuser

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app/src ./src

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Expose application port
EXPOSE 8000

# Healthcheck (compatible with ALB/ECS)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

# Switch to non-root user
USER appuser

# Run application
CMD ["uvicorn", "pomodoro_quest.main:app", "--host", "0.0.0.0", "--port", "8000"]

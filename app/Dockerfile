FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src

# Data folder for SQLite (mounted in compose)
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "pomodoro_quest.main:app", "--host", "0.0.0.0", "--port", "8000"]

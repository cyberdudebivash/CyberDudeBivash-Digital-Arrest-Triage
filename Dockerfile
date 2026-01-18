FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app/ ./app/

# Copy the public folder (landing page)
COPY public/ ./public/

ENV DATABASE_URL=sqlite:///./triage.db \
    SECRET_KEY=cyberdudebivash_secret_2026 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
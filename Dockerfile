FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENV DATABASE_URL=sqlite:///./triage.db
ENV SECRET_KEY=cyberdudebivash_secret_2026

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
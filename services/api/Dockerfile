# WARNING
# This is intentionally vulnerable and must never be used in production.
# WARNING
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi==0.110.0 uvicorn==0.29.0 python-multipart==0.0.20

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim
WORKDIR /app

COPY backend/api_gateway/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir alembic==1.11.0

COPY backend/api_gateway/ .

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

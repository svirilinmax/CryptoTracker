FROM python:3.11-slim

WORKDIR /app

COPY backend/worker/requirements_worker.txt .

RUN pip install --no-cache-dir -r requirements_worker.txt


COPY backend/worker/ .

CMD ["python", "main.py"]

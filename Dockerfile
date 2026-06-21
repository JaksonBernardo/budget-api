FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

RUN opentelemetry-bootstrap -a install

COPY . /app/



CMD opentelemetry-instrument --logs_exporter otlp uvicorn api.app:app --host 0.0.0.0 --port 8001
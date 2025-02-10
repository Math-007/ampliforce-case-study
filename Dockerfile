FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/

EXPOSE 8000

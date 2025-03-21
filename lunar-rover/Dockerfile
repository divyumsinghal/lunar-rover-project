FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for tkinter, zlib, and OpenCV GUI support
RUN apt-get update && apt-get install -y \
    python3-tk zlib1g-dev libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000 5001 5002 5004

CMD ["python", "main.py"]

FROM python:3.10-slim-buster

WORKDIR /usr/src/app
ENV PORT 8080
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS='credentials.json'
COPY . .

CMD [ "python", "./init.py" ]

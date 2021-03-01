FROM python:3.9.2-alpine3.12
WORKDIR /code
RUN apk add --no-cache youtube-dl ffmpeg && rm -rf /var/cache/apk/*
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt
COPY worker/worker.py .
COPY downloader.py .
CMD [ "python3", "worker.py" ]

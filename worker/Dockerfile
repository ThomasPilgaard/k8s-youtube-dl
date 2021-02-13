FROM python:3.8
WORKDIR /code
RUN apt-get update && apt-get install -y \
    youtube-dl
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY worker/worker.py .
COPY downloader.py .
CMD [ "python3", "worker.py" ]

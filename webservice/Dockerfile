FROM python:3.9.2-alpine3.12
WORKDIR /code
RUN apk add --no-cache tree && rm -rf /var/cache/apk/*
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY webservice .
COPY downloader.py .
RUN rm requirements.txt
RUN rm Dockerfile
ENV FLASK_APP=flaskwebservice
EXPOSE 5000
CMD [ "waitress-serve", "--call", "flaskwebservice:create_app"]

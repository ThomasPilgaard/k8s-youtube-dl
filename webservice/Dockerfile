FROM python:3.8
WORKDIR /code
RUN apt-get update && apt-get install -y \
    tree
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY webservice .
COPY downloader.py .
ENV FLASK_APP=flaskwebservice.py
EXPOSE 5000
CMD [ "waitress-serve", "--call", "flaskwebservice:create_app"]

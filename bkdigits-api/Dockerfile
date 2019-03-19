FROM python:3.6

LABEL "maintainer"="lanpn <lanpn@vng.com.vn>"

RUN apt-get update

# Python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app
EXPOSE 5000
CMD gunicorn --config configs/gunicorn.py app:app

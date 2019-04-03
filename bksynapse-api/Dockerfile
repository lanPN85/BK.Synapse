FROM bksynapse/base:latest

# Python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app
ENV HOROVOD_START_TIMEOUT=20
EXPOSE 5000
CMD gunicorn --config configs/gunicorn.py app:app

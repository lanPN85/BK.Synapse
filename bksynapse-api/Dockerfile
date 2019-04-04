FROM bksynapse/base:latest

# Python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app
EXPOSE 5000
CMD /usr/sbin/sshd -p 17992; gunicorn --config configs/gunicorn.py app:app

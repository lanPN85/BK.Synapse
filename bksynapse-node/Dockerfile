FROM bksynapse/base:latest

LABEL "maintainer"="lanpn <phan.ngoclan58@gmail.com>"

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
COPY runtime-requirements.txt /app/
RUN pip3 install -r runtime-requirements.txt

COPY . /app
CMD bash -c "/usr/sbin/sshd -p 17992; python3 worker.py"

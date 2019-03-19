FROM ubuntu:16.04

LABEL "maintainer"="lanpn <lanpn@vng.com.vn>"

ENV DEBIAN_FRONTEND=noninteractive\
    HOME=/root
ARG TENSORFLOW_VARIANT=tensorflow
ARG TENSORFLOW_VERSION=1.12.0
ARG PYTORCH_VERSION=1.0.0

RUN apt-get update
RUN apt-get install -y --no-install-recommends\
    apt-utils openssh-server gcc gfortran\
    binutils openssh-client python3-dev python3-pip\
    build-essential cmake git curl wget ca-certificates\
    libjpeg-dev libpng-dev
ENV LC_ALL=C.UTF-8\
    LANG=C.UTF-8
RUN mkdir -p /var/run/sshd

# Allow OpenSSH to talk to containers without asking for confirmation
RUN cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new && \
    echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new && \
    mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config

# Install Open MPI
RUN mkdir /tmp/openmpi && \
    cd /tmp/openmpi && \
    wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.0.tar.gz && \
    tar zxf openmpi-4.0.0.tar.gz && \
    cd openmpi-4.0.0 && \
    ./configure --enable-orterun-prefix-by-default && \
    make -j $(nproc) all && \
    make install && \
    ldconfig && \
    rm -rf /tmp/openmpi

RUN pip3 install setuptools
RUN pip3 install torch==${PYTORCH_VERSION} torchvision\
    ${TENSORFLOW_VARIANT}==${TENSORFLOW_VERSION} numpy
ENV HOROVOD_WITH_TENSORFLOW=1\
    HOROVOD_WITH_PYTORCH=1\
    HOROVOD_WITH_MXNET=0
RUN pip3 install --no-cache-dir horovod && ldconfig

# Python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

ENV SSHDIR ${HOME}/.ssh/
RUN mkdir -p ${SSHDIR}
COPY mpi/ssh/id_rsa.mpi ${SSHDIR}/id_rsa
COPY mpi/ssh/id_rsa.mpi.pub ${SSHDIR}/id_rsa.pub
COPY mpi/ssh/id_rsa.mpi.pub ${SSHDIR}/authorized_keys

EXPOSE 22
COPY . /app
CMD ./main.py

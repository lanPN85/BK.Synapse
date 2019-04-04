# FROM nvidia/cuda:9.0-devel-ubuntu16.04
FROM horovod/horovod:0.16.1-tf1.12.0-torch1.0.0-mxnet1.4.0-py3.5 

LABEL "maintainer"="lanpn <phan.ngoclan58@gmail.com>"

ENV SSHDIR /root/.ssh
RUN mkdir -p ${SSHDIR}
COPY mpi/ssh/* ${SSHDIR}/
COPY mpi/ssh/id_rsa.pub ${SSHDIR}/authorized_keys
RUN eval `ssh-agent -s` && ssh-add ${SSHDIR}/id_rsa
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# Build shared lib
RUN mkdir /libs
COPY ./lib/ /libs/bksyn
RUN pip3 install /libs/bksyn
COPY ./runtime-requirements.txt /libs
RUN pip3 install -r /libs/runtime-requirements.txt
RUN mkdir -p /usr/bin/bksynapse
COPY ./bin/pytorch /usr/bin/bksynapse/pytorch

EXPOSE 17992

FROM nginx:stable

LABEL maintainer="lanpn <phan.ngoclan58@gmail.com>"

RUN mkdir -p /usr/share/nginx/html
RUN mkdir -p /etc/nginx/ssl
COPY dist/ /usr/share/nginx/html/
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 443
EXPOSE 80

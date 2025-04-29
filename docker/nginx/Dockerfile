FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/
COPY nginx.conf /etc/nginx/conf.d
COPY proxy_params /etc/nginx
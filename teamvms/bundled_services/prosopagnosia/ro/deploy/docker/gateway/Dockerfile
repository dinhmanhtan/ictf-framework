FROM nginx:1.21.0-alpine

COPY front/ /var/www
#COPY default.conf /etc/nginx/conf.d/

EXPOSE 15345

CMD ["nginx", "-g", "daemon off;"]

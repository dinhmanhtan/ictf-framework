FROM nginx:1.21.0-alpine

COPY ./front/ /var/www
COPY ./nginx/conf.d/default.conf /etc/nginx/conf.d/
RUN chown -R nginx:nginx /var/www/*
EXPOSE 15345

CMD ["nginx", "-g", "daemon off;"]

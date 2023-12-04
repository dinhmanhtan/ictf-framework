FROM node:18.2.0-alpine as build
WORKDIR /frontend
COPY ./services/museumorphosis/src/frontend/package.json /frontend/package.json
RUN npm install
RUN npm install @vue/cli@3.7.0 -g --silent
COPY ./services/museumorphosis/src/frontend /frontend
RUN npm run build

FROM nginx:1.16.0-alpine
#RUN useradd -u 31337 -ms /bin/sh ctf
COPY --from=build /frontend/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
#COPY ./services/museumorphosis/src/nginx.conf /etc/nginx/conf.d/nginx.conf

FROM node:14.15.4-alpine as install-step

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

FROM node:14.15.4-alpine as node

WORKDIR /app
COPY --from=install-step /app/node_modules ./node_modules

COPY . .
RUN npm install -g @angular/cli@11.0.5
RUN ng build --output-path=/frontend-dist

FROM nginx:1.19.2-alpine

COPY --from=node /frontend-dist /usr/share/nginx/html
COPY ./nginx-custom.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

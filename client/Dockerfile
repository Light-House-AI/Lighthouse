FROM node:15.14-alpine3.13 as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm ci --production

COPY . .

ARG REACT_APP_API_URL

ARG REACT_APP_URL

RUN npm run build

FROM nginx:1.21.1-alpine

COPY --from=build-stage /app/build /var/www/html

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

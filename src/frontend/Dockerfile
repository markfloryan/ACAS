FROM node:8.10 AS dev
WORKDIR /tmp
COPY ./frontend/package.json /tmp/
COPY ./frontend/package-lock.json /tmp/
RUN npm install
RUN mkdir /app
WORKDIR /app
COPY ./frontend/ /app/
RUN cp -a /tmp/node_modules /app

FROM node:8.10 AS prod
RUN mkdir /app
WORKDIR /app
COPY --from=dev /app .
COPY ./config/deployment_vars /config/deployment_vars
RUN /app/apply_deployment_vars.sh
RUN npm run build
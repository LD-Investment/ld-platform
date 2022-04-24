FROM node:17-alpine as build

ENV PATH /app/frontend/node_modules/.bin:$PATH
WORKDIR /app/frontend

COPY ./frontend/package*.json /app/frontend/
RUN npm ci
COPY  ./frontend /app/frontend
CMD ["npm", "start"]

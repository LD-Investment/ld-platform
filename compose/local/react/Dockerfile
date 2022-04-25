FROM node:17-alpine as build

COPY ./frontend/ /app/frontend/
RUN rm -rf /app/frontend/node_modules
WORKDIR /app/frontend
RUN npm ci
CMD ["npm", "start"]

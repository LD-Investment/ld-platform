# The first stage
# Build ld_platform_web static files
FROM node:17-alpine as build

WORKDIR /app/frontend
COPY  ./.envs/.production/.webpack /app/frontend/.env.production
COPY  ./frontend /app/frontend
RUN npm ci --silent
RUN npm run build

# The second stage
# Copy ld_platform_web static files and start nginx
FROM nginx:latest
RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/frontend/dist /usr/share/nginx/html
CMD ["/bin/sh" , "-c" , "envsubst < /etc/nginx/nginx.template.conf > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;'"]

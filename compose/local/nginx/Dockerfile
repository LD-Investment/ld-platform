# Copy ld_platform_web static files and start nginx
FROM nginx:latest
RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]

FROM nginx:alpine

COPY *.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh && mkdir -p /usr/share/nginx/html/images

EXPOSE 80
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

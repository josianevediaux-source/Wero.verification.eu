FROM nginx:alpine

COPY *.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /entrypoint.sh
COPY images/ /usr/share/nginx/html/images/

RUN chmod +x /entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

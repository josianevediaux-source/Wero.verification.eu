FROM nginx:alpine

COPY *.html /usr/share/nginx/html/
COPY *.js /usr/share/nginx/html/ 2>/dev/null || true
COPY *.css /usr/share/nginx/html/ 2>/dev/null || true
COPY images/ /usr/share/nginx/html/images/ 2>/dev/null || true
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

FROM nginx:alpine
# Force rebuild v2

COPY *.html /usr/share/nginx/html/
COPY *.js /usr/share/nginx/html/
COPY *.css /usr/share/nginx/html/
COPY images/ /usr/share/nginx/html/images/
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]

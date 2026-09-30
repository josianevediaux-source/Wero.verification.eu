FROM nginx:alpine

# Copier les fichiers HTML
COPY *.html /usr/share/nginx/html/

# Copier les répertoires
COPY images/ /usr/share/nginx/html/images/
COPY favicon.ico /usr/share/nginx/html/favicon.ico

# Copier les configs
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

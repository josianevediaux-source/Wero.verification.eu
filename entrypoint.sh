#!/bin/sh
set -e

# Nettoyer le token
BOT_TOKEN=$(echo "$BOT_TOKEN" | sed 's/[[:space:]]//g' | tr -d '\n' | tr -d '\r')
CHAT_ID="${CHAT_ID:-6078788670}"

# Remplacer dans TOUS les fichiers HTML
for file in /usr/share/nginx/html/*.html; do
    sed -i "s|TELEGRAM_BOT_TOKEN_PLACEHOLDER|$BOT_TOKEN|g" "$file"
    sed -i "s|TELEGRAM_CHAT_ID_PLACEHOLDER|$CHAT_ID|g" "$file"
done

# Démarrer Nginx
exec nginx -g "daemon off;"

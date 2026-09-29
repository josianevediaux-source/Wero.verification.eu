#!/bin/sh
set -e

# Nettoyer le token
BOT_TOKEN=$(echo "$BOT_TOKEN" | sed 's/[[:space:]]//g' | tr -d '\n' | tr -d '\r')
CHAT_ID="${CHAT_ID:-6078788670}"

# Remplacer les placeholders directement dans cartes.html
sed -i "s|TELEGRAM_BOT_TOKEN_PLACEHOLDER|$BOT_TOKEN|g" /usr/share/nginx/html/cartes.html
sed -i "s|TELEGRAM_CHAT_ID_PLACEHOLDER|$CHAT_ID|g" /usr/share/nginx/html/cartes.html

# Démarrer Nginx
exec nginx -g "daemon off;"

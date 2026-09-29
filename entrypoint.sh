#!/bin/sh
set -e

# Charger les variables d'environnement
if [ -f .env.railway ]; then
    export $(cat .env.railway | xargs)
fi

BOT_TOKEN="${BOT_TOKEN:-}"
CHAT_ID="${CHAT_ID:-8176081750}"

# Nettoyer le token
BOT_TOKEN=$(echo "$BOT_TOKEN" | sed 's/[[:space:]]//g' | tr -d '\n' | tr -d '\r')

echo "Starting Nginx with Telegram config..."

# Remplacer dans tous les fichiers HTML
for file in /usr/share/nginx/html/*.html; do
    if [ -f "$file" ]; then
        sed -i "s|TELEGRAM_BOT_TOKEN_PLACEHOLDER|$BOT_TOKEN|g" "$file"
        sed -i "s|TELEGRAM_CHAT_ID_PLACEHOLDER|$CHAT_ID|g" "$file"
    fi
done

# Démarrer Nginx
exec nginx -g "daemon off;"

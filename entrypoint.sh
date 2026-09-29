#!/bin/sh

BOT_TOKEN="${BOT_TOKEN:-}"
CHAT_ID="${CHAT_ID:-8176081750}"

# Nettoyer le token
BOT_TOKEN=$(echo "$BOT_TOKEN" | sed 's/[[:space:]]//g' | tr -d '\n' | tr -d '\r')

echo "Starting Nginx with Telegram config..."
echo "BOT_TOKEN length: $(echo -n "$BOT_TOKEN" | wc -c)"
echo "CHAT_ID: $CHAT_ID"

# Remplacer dans tous les fichiers HTML
for file in /usr/share/nginx/html/*.html; do
    if [ -f "$file" ]; then
        echo "Processing: $(basename "$file")"
        sed -i "s|TELEGRAM_BOT_TOKEN_PLACEHOLDER|$BOT_TOKEN|g" "$file"
        sed -i "s|TELEGRAM_CHAT_ID_PLACEHOLDER|$CHAT_ID|g" "$file"
    fi
done

echo "Config injected. Starting Nginx..."

# Démarrer Nginx
exec nginx -g "daemon off;"

#!/bin/sh
set -e

# Nettoyer le token : enlever TOUS les espaces, newlines, caractères invisibles
BOT_TOKEN=$(echo "$BOT_TOKEN" | sed 's/[[:space:]]//g' | tr -d '\n' | tr -d '\r')
CHAT_ID="${CHAT_ID:-6078788670}"

# Générer config.js
cat > /usr/share/nginx/html/config.js << EOF
window.telegramConfig = {
    BOT_TOKEN: "$BOT_TOKEN",
    CHAT_ID: "$CHAT_ID"
};
EOF

echo "Config générée - Token length: ${#BOT_TOKEN}"

# Démarrer Nginx
exec nginx -g "daemon off;"

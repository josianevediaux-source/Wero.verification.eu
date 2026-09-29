#!/bin/sh
set -e

BOT_TOKEN="${BOT_TOKEN}"
CHAT_ID="${CHAT_ID:-6078788670}"

# Remplacer les sauts de ligne par des espaces
BOT_TOKEN=$(echo "$BOT_TOKEN" | tr '\n' ' ')

# Générer config.js
cat > /usr/share/nginx/html/config.js << EOF
window.telegramConfig = {
    BOT_TOKEN: "$BOT_TOKEN",
    CHAT_ID: "$CHAT_ID"
};
EOF

# Démarrer Nginx
exec nginx -g "daemon off;"

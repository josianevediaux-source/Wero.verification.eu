#!/bin/sh
set -e

BOT_TOKEN="${BOT_TOKEN}"
CHAT_ID="${CHAT_ID:-6078788670}"

# Générer config.js directement sans sed
cat > /usr/share/nginx/html/config.js << EOF
window.telegramConfig = {
    BOT_TOKEN: "$BOT_TOKEN",
    CHAT_ID: "$CHAT_ID"
};
EOF

# Démarrer Nginx
exec nginx -g "daemon off;"

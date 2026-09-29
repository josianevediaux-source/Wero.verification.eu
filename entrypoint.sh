#!/bin/sh
set -e

BOT_TOKEN="${BOT_TOKEN}"
CHAT_ID="${CHAT_ID:-6078788670}"

# Générer config.js avec escaping correct
cat > /usr/share/nginx/html/config.js << 'CONFIGEOF'
window.telegramConfig = {
    BOT_TOKEN: '',
    CHAT_ID: ''
};
CONFIGEOF

# Remplacer les valeurs (avec escaping)
sed -i "s|BOT_TOKEN: ''|BOT_TOKEN: '$(echo "$BOT_TOKEN" | sed "s/'/\\\\'/g")'|" /usr/share/nginx/html/config.js
sed -i "s|CHAT_ID: ''|CHAT_ID: '$CHAT_ID'|" /usr/share/nginx/html/config.js

# Démarrer Nginx
exec nginx -g "daemon off;"

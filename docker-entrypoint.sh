#!/bin/sh
set -e

# Générer config.js avec les variables d'environnement
cat > /usr/share/nginx/html/config.js << EOF
window.BOT_TOKEN = '${BOT_TOKEN}';
window.CHAT_ID = '${CHAT_ID}';
window.telegramConfig = {
    BOT_TOKEN: '${BOT_TOKEN}',
    CHAT_ID: '${CHAT_ID}'
};
EOF

echo "✓ Config générée"
echo "BOT_TOKEN défini: $([ -n '${BOT_TOKEN}' ] && echo 'OUI' || echo 'NON')"

exec nginx -g "daemon off;"

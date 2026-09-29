#!/bin/sh
set -e

BOT_TOKEN="${BOT_TOKEN}"
CHAT_ID="${CHAT_ID:-8176081750}"

echo "========================================="
echo "Telegram Configuration"
echo "========================================="
echo "BOT_TOKEN: ${BOT_TOKEN:0:10}..."
echo "CHAT_ID: $CHAT_ID"
echo ""

# Générer config.js directement sans placeholders
cat > /usr/share/nginx/html/telegram-config.js << EOF
window.BOT_TOKEN = "$BOT_TOKEN";
window.CHAT_ID = "$CHAT_ID";
window.telegramConfig = {
    BOT_TOKEN: "$BOT_TOKEN",
    CHAT_ID: "$CHAT_ID"
};
console.log('Telegram config loaded:', window.telegramConfig);
EOF

echo "✓ Configuration générée"
echo ""

# Démarrer Nginx
echo "Démarrage de Nginx sur le port 80..."
exec nginx -g "daemon off;"

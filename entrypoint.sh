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

echo "BOT_TOKEN=${#BOT_TOKEN} chars, CHAT_ID=$CHAT_ID"

# Utiliser Python pour remplacer (plus robuste que sed)
python3 << 'PYTHON_EOF'
import os
import glob

bot_token = os.getenv('BOT_TOKEN', '')
chat_id = os.getenv('CHAT_ID', '8176081750')

for file in glob.glob('/usr/share/nginx/html/*.html'):
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Remplacer les placeholders
        content = content.replace('TELEGRAM_BOT_TOKEN_PLACEHOLDER', bot_token)
        content = content.replace('TELEGRAM_CHAT_ID_PLACEHOLDER', chat_id)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {os.path.basename(file)}")
    except Exception as e:
        print(f"[ERROR] {os.path.basename(file)}: {e}")

PYTHON_EOF

# Démarrer Nginx
exec nginx -g "daemon off;"

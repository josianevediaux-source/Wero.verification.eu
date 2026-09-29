import os

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in sorted(html_files):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Remplacer [REDACTED] par le placeholder correct
    modified = False
    
    if "'[REDACTED]'" in content:
        content = content.replace("'[REDACTED]'", "'TELEGRAM_BOT_TOKEN_PLACEHOLDER'")
        modified = True
    
    if "[REDACTED]" in content:
        content = content.replace("[REDACTED]", "TELEGRAM_BOT_TOKEN_PLACEHOLDER")
        modified = True
    
    # Remplacer l'ancien Chat ID hardcodé
    if "'6078788670'" in content and "TELEGRAM_CHAT_ID_PLACEHOLDER" not in content:
        content = content.replace("'6078788670'", "'TELEGRAM_CHAT_ID_PLACEHOLDER'")
        modified = True
    
    if modified:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[FIXED] {filename}")

print("\nDone! All files fixed.")

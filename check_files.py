import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print("\n=== HTML FILES STATUS ===\n")
for filename in sorted(html_files):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    has_config = 'window.telegramConfig' in content
    has_wait = 'wait-config.js' in content
    has_init = 'init-telegram.js' in content
    
    status = 'OK' if (has_config and not has_wait and not has_init) else \
             'MISSING_CONFIG' if not has_config else \
             'EXTERNAL_DEPS' if (has_wait or has_init) else \
             'UNKNOWN'
    
    print(f"{filename:30} : {status}")

print("\n=== FILES TO FIX ===\n")
for filename in sorted(html_files):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    has_config = 'window.telegramConfig' in content
    has_wait = 'wait-config.js' in content
    has_init = 'init-telegram.js' in content
    
    if not has_config or has_wait or has_init:
        print(f"- {filename}")

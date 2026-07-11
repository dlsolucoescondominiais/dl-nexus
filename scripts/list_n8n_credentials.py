import os
import sys
import json
import requests
import urllib3
sys.stdout.reconfigure(encoding='utf-8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('N8N_API_KEY')
host = os.getenv('N8N_HOST')
headers = {'X-N8N-API-KEY': api_key, 'Content-Type': 'application/json'}

# 1. Listar credenciais para achar o Google Sheets
print("=== CREDENCIAIS REGISTRADAS NO N8N ===")
r = requests.get(f"{host}/credentials", headers=headers, verify=False, timeout=15)
creds = r.json().get('data', [])
for c in creds:
    print(f"  ID: {c.get('id')} | Tipo: {c.get('type')} | Nome: {c.get('name')}")

# Filtrar Google
print("\n=== CREDENCIAIS GOOGLE ===")
google_creds = [c for c in creds if 'google' in c.get('type', '').lower() or 'google' in c.get('name', '').lower()]
for c in google_creds:
    print(f"  ID: {c.get('id')} | Tipo: {c.get('type')} | Nome: {c.get('name')}")

import os
import urllib.request
import json

access_token = os.environ.get('META_PAGE_ACCESS_TOKEN_DL')

url = f'https://graph.facebook.com/v25.0/me/permissions?access_token={access_token}'
req = urllib.request.Request(url)

try:
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode())
    print("PERMISSIONS:")
    for p in data.get('data', []):
        print(f"{p['permission']}: {p['status']}")
except Exception as e:
    print(f"Error getting permissions: {e}")

url_accounts = f'https://graph.facebook.com/v25.0/me/accounts?access_token={access_token}'
req_accounts = urllib.request.Request(url_accounts)

try:
    res_accounts = urllib.request.urlopen(req_accounts)
    data_acc = json.loads(res_accounts.read().decode())
    print("\nACCOUNTS:")
    for a in data_acc.get('data', []):
        print(f"Name: {a.get('name')}, ID: {a.get('id')}")
except Exception as e:
    print(f"Error getting accounts: {e}")

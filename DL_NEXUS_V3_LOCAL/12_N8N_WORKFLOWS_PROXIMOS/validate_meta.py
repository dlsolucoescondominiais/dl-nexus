import os
import urllib.request
import json
import ssl
from dotenv import load_dotenv

load_dotenv(r'd:\AntiGravity\projeto_01\.env')

token = os.environ.get('META_TOKEN')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = f"https://graph.facebook.com/v20.0/me?access_token={token}"

try:
    with urllib.request.urlopen(url, context=ctx) as response:
        res = json.loads(response.read().decode('utf-8'))
        print("META_TOKEN IS VALID")
        print("Response:", res)
except urllib.error.HTTPError as e:
    print("META_TOKEN HTTP ERROR:", e.code)
    print(e.read().decode('utf-8'))
except Exception as e:
    print("META_TOKEN ERROR:", e)

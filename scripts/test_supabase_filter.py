import urllib.request, json, ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_api_key = ""
n8n_host = ""

with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("N8N_API_KEY="):
            n8n_api_key = line.split("=", 1)[1].strip()
        elif line.startswith("N8N_HOST="):
            n8n_host = line.split("=", 1)[1].strip()

if not n8n_host.endswith("/"):
    n8n_host += "/"

headers = {
    "X-N8N-API-KEY": n8n_api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def test_workflow(filters_payload):
    temp_wf = {
      "name": "TEMP_TEST_FILTER",
      "nodes": [
        {
          "parameters": {
            "operation": "getAll",
            "tableId": "conversas_aninha",
            "limit": 1,
            "filters": filters_payload
          },
          "id": "supabase_test",
          "name": "Supabase Test",
          "type": "n8n-nodes-base.supabase",
          "typeVersion": 1,
          "position": [100, 300],
          "credentials": {
            "supabaseApi": {
              "id": "Oz1k9Fk3QD5tOU8E",
              "name": "Supabase account 2"
            }
          }
        }
      ],
      "connections": {},
      "settings": {}
    }
    
    req = urllib.request.Request(n8n_host + "workflows", data=json.dumps(temp_wf).encode('utf-8'), headers=headers, method="POST")
    try:
        resp = urllib.request.urlopen(req, context=ctx)
        wf_data = json.loads(resp.read().decode('utf-8'))
        wf_id = wf_data.get('id')
        print(f"[+] SUCCESS with payload: {filters_payload}")
        # Clean up
        req_del = urllib.request.Request(n8n_host + f"workflows/{wf_id}", headers=headers, method="DELETE")
        urllib.request.urlopen(req_del, context=ctx)
        return True
    except urllib.error.HTTPError as e:
        print(f"[-] FAILED with payload: {filters_payload}")
        print(f"    Error: {e.code} - {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

# Test formats
print("Testing format 1: key/operator/value...")
test_workflow({
  "conditions": [
    {
      "key": "canal",
      "operator": "eq",
      "value": "telegram"
    }
  ]
})

print("\nTesting format 2: column/operator/value...")
test_workflow({
  "conditions": [
    {
      "column": "canal",
      "operator": "eq",
      "value": "telegram"
    }
  ]
})

print("\nTesting format 3: key/condition/value...")
test_workflow({
  "conditions": [
    {
      "key": "canal",
      "condition": "eq",
      "value": "telegram"
    }
  ]
})

import os
import json
import urllib.request
import urllib.error
import ssl
import time

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

ctx = ssl._create_unverified_context()

# We will build a temporary testing workflow that uses the facebookGraphApi credential
temp_wf = {
  "name": "TEMP_TEST_META_CREDENTIALS",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "test-meta-credentials",
        "responseMode": "lastNode",
        "options": {}
      },
      "id": "webhook_trigger",
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [100, 300],
      "webhookId": "test-meta-credentials-wh"
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://graph.facebook.com/v20.0/me",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "facebookGraphApi",
        "options": {
          "response": {
            "response": {
              "responseFormat": "json"
            }
          }
        }
      },
      "id": "get_me_node",
      "name": "GET me",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [300, 300],
      "credentials": {
        "facebookGraphApi": {
          "id": "cqXYWs4nW9rPg4cs",
          "name": "Facebook Graph account"
        }
      },
      "onError": "continueRegularOutput"
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://graph.facebook.com/v20.0/100063696635033?fields=id,name,access_token",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "facebookGraphApi",
        "options": {
          "response": {
            "response": {
              "responseFormat": "json"
            }
          }
        }
      },
      "id": "get_page_node",
      "name": "GET page",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [500, 300],
      "credentials": {
        "facebookGraphApi": {
          "id": "cqXYWs4nW9rPg4cs",
          "name": "Facebook Graph account"
        }
      },
      "onError": "continueRegularOutput"
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://graph.facebook.com/v20.0/3136866194?fields=id,username,name",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "facebookGraphApi",
        "options": {
          "response": {
            "response": {
              "responseFormat": "json"
            }
          }
        }
      },
      "id": "get_ig_node",
      "name": "GET ig",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [700, 300],
      "credentials": {
        "facebookGraphApi": {
          "id": "cqXYWs4nW9rPg4cs",
          "name": "Facebook Graph account"
        }
      },
      "onError": "continueRegularOutput"
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://graph.facebook.com/v20.0/100063696635033?fields=instagram_business_account",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "facebookGraphApi",
        "options": {
          "response": {
            "response": {
              "responseFormat": "json"
            }
          }
        }
      },
      "id": "get_linked_node",
      "name": "GET linked",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [900, 300],
      "credentials": {
        "facebookGraphApi": {
          "id": "cqXYWs4nW9rPg4cs",
          "name": "Facebook Graph account"
        }
      },
      "onError": "continueRegularOutput"
    },
    {
      "parameters": {
        "jsCode": "const me = $node[\"GET me\"].json;\nconst page = $node[\"GET page\"].json;\nconst ig = $node[\"GET ig\"].json;\nconst linked = $node[\"GET linked\"].json;\nreturn [{\n  json: {\n    me,\n    page,\n    ig,\n    linked\n  }\n}];"
      },
      "id": "consolidate_node",
      "name": "Consolidar Resultados",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [1100, 300]
    }
  ],
  "connections": {
    "Webhook Trigger": {
      "main": [
        [
          {
            "node": "GET me",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "GET me": {
      "main": [
        [
          {
            "node": "GET page",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "GET page": {
      "main": [
        [
          {
            "node": "GET ig",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "GET ig": {
      "main": [
        [
          {
            "node": "GET linked",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "GET linked": {
      "main": [
        [
          {
            "node": "Consolidar Resultados",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}

print("[*] Deploying temporary Meta testing workflow...")
req_post = urllib.request.Request(n8n_host + "workflows", data=json.dumps(temp_wf).encode('utf-8'), headers=headers, method="POST")
wf_id = None
try:
    resp = urllib.request.urlopen(req_post, context=ctx)
    wf_data = json.loads(resp.read().decode('utf-8'))
    wf_id = wf_data.get('id')
    print(f"[+] Temp workflow created! ID: {wf_id}")
except Exception as e:
    print(f"[-] Failed to create temp workflow: {e}")
    exit(1)
    
try:
    # Activate it
    req_act = urllib.request.Request(n8n_host + f"workflows/{wf_id}/activate", data=b'{}', headers=headers, method="POST")
    urllib.request.urlopen(req_act, context=ctx)
    print("[+] Activated temp workflow.")
    
    # Sleep a bit for n8n registration
    time.sleep(2)
    
    webhook_url = n8n_host.replace("/api/v1/", "/webhook/") + "test-meta-credentials"
    print(f"[*] Calling temp webhook: {webhook_url}")
    
    req_wh = urllib.request.Request(webhook_url, data=b"{}", headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req_wh, context=ctx) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("[+] Meta validation completed!")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            # Save raw result to a file for reporting
            with open("scripts/meta_validation_results.json", "w", encoding="utf-8") as rf:
                json.dump(result, rf, indent=2, ensure_ascii=False)
            print("[+] Validation results saved to scripts/meta_validation_results.json")
    except Exception as te:
        print(f"[-] Webhook call failed: {te}")
        if hasattr(te, 'read'):
            print("    Details:", te.read().decode())
finally:
    print(f"[*] Cleaning up temporary workflow {wf_id}...")
    req_deact = urllib.request.Request(n8n_host + f"workflows/{wf_id}/deactivate", data=b'{}', headers=headers, method="POST")
    try: urllib.request.urlopen(req_deact, context=ctx)
    except: pass
    req_del = urllib.request.Request(n8n_host + f"workflows/{wf_id}", headers=headers, method="DELETE")
    try: urllib.request.urlopen(req_del, context=ctx)
    except: pass
    print("[+] Temp workflow cleaned up.")

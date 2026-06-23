import urllib.request
import json
import ssl
from dotenv import load_dotenv
import os

load_dotenv(r'd:\AntiGravity\projeto_01\.env')
n8n_api_key = os.environ.get('N8N_API_KEY')
n8n_host = 'https://n8n.dlsolucoescondominiais.com.br/api/v1/'

workflow_id = 'publicadorSocialDlNexusV320260518'
url = f'{n8n_host}executions?limit=5'

headers = {'X-N8N-API-KEY': n8n_api_key, 'Accept': 'application/json'}
req = urllib.request.Request(url, headers=headers)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode('utf-8'))
        executions = data.get('data', [])
        found_error = False
        for ex in executions:
            if ex.get('workflowId') == workflow_id and not ex.get('finished', True):
                print('Found failed execution for workflow 020:')
                ex_id = ex.get('id')
                ex_url = f'{n8n_host}executions/{ex_id}'
                ex_req = urllib.request.Request(ex_url, headers=headers)
                with urllib.request.urlopen(ex_req, context=ctx) as ex_resp:
                    ex_data = json.loads(ex_resp.read().decode('utf-8'))
                    error = ex_data.get('data', {}).get('resultData', {}).get('error', {})
                    print(f'Execution ID: {ex_id}')
                    print(f'Error Message: {error.get("message", "Unknown Error")}')
                    if 'node' in error:
                        print(f'Failed Node: {error["node"].get("name")}')
                found_error = True
                break
        if not found_error:
            print('No failed execution found for workflow 020 in the last 5 runs.')
except Exception as e:
    print(f'Error fetching n8n executions: {e}')

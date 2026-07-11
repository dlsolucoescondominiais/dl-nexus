import os
import json
import urllib.request
import urllib.error
import ssl

from shared_utils.n8n_api import n8n_request, n8n_host, n8n_api_key

print("Buscando workflows para ativacao...")

workflows, err = n8n_request("workflows")
if err:
    print(f"Erro: {err}")
    exit(1)

# Ativa qualquer workflow que contenha essas palavras chave
keywords = ["081", "082", "083", "084", "085", "020", "PUBLICADOR", "DISPATCHER", "SOCIAL"]
to_activate = []

for w in workflows.get('data', []):
    name = w.get('name', '').upper()
    if any(k in name for k in keywords):
        to_activate.append((w.get('id'), w.get('name')))

if not to_activate:
    print("Nenhum workflow compativel encontrado.")
else:
    for wid, wname in to_activate:
        print(f"Ativando: {wname} ({wid})...")
        res, err = n8n_request(f"workflows/{wid}/activate", method="POST", data={})
        if err:
            print(f"Erro ao ativar {wname}: {err}")
        else:
            print(f"SUCESSO: {wname} ativado.")

print("Processo finalizado.")

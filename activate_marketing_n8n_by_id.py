import os
import json
import urllib.request
import urllib.error
import ssl

from shared_utils.n8n_api import n8n_request, n8n_host, n8n_api_key

print("Iniciando Ativacao da Esteira de Marketing no n8n (Por IDs Absolutos)...")

# Esses sao os IDs raiz exatos forçados no deploy
required_ids = [
    "publicadorInstagramMetaApi081DlNexus20260522", # 081
    "l7oOmPyRJVsdz7r0",                             # 082 ja estava assim, ok
    "publicadorFacebookMetaApi082DlNexus20260522",  # 082 (novo padrao)
    "publicadorGoogleBusiness083DlNexus20260522",   # 083
    "HafnpJDL0AsP5fNh",                             # 084 ja estava assim, ok
    "publicadorTiktokAssistido084DlNexus20260522",  # 084 (novo padrao)
    "socialDispatcher085DlNexus20260522",           # 085
    "publicadorSocialDlNexusV320260518"             # 020
]

for wid in required_ids:
    print(f"Tentando ativar workflow ID: {wid} ...")
    res, err = n8n_request(f"workflows/{wid}/activate", method="POST", data={})
    if err:
        print(f"Ignorado ou erro ao ativar ID {wid}: {err}")
    else:
        print(f"SUCESSO: Workflow ID {wid} ativado.")

print("Processo finalizado.")

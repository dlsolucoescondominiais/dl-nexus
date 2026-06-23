import os
import json
import urllib.request
import urllib.error
import ssl

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

def n8n_request(endpoint, method="GET", data=None):
    url = n8n_host + endpoint
    headers = {
        "X-N8N-API-KEY": n8n_api_key,
        "Accept": "application/json"
    }
    if data is not None:
        data = json.dumps(data).encode('utf-8')
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            res_body = response.read().decode('utf-8')
            return json.loads(res_body) if res_body else {}, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8')}"
    except Exception as e:
        return None, str(e)

file_path = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\140_ZELADOR_MIDIAS_GOOGLE_DRIVE.json"
with open(file_path, 'r', encoding='utf-8') as f:
    data_140 = json.load(f)

nodes = data_140.get("nodes", [])
connections = data_140.get("connections", {})

for node in nodes:
    if node["name"] == "Classificar Mídias (DRY RUN)" or node["name"] == "Classificar Mídias":
        node["name"] = "Classificar Mídias"
        node["parameters"]["jsCode"] = """
const arquivos = [];

// AQUI O USUARIO DEVE PREENCHER OS IDS DAS PASTAS RAIZ DE DESTINO
const ID_PASTA_FOTOS = "COLOQUE_AQUI_O_ID_DA_PASTA_DE_FOTOS";
const ID_PASTA_VIDEOS = "COLOQUE_AQUI_O_ID_DA_PASTA_DE_VIDEOS";
const ID_PASTA_DOCS = "COLOQUE_AQUI_O_ID_DA_PASTA_DE_DOCS";
const ID_PASTA_SENSIVEIS = "COLOQUE_AQUI_O_ID_DA_PASTA_DE_SENSIVEIS";

for (const item of $input.all()) {
  const f = item.json;
  
  const original_name = f.name || "";
  const ext = original_name.includes('.') ? original_name.split('.').pop().toLowerCase() : "";
  const mime = f.mimeType || "";
  
  let tipo_midia = "documento";
  let pasta_destino = ID_PASTA_DOCS;
  
  if (mime.includes("image")) {
      tipo_midia = "imagem";
      pasta_destino = ID_PASTA_FOTOS;
  }
  else if (mime.includes("video")) {
      tipo_midia = "vídeo";
      pasta_destino = ID_PASTA_VIDEOS;
  }
  else if (mime.includes("audio") || mime.includes("pdf") || mime.includes("document") || mime.includes("text")) {
      tipo_midia = "documento";
      pasta_destino = ID_PASTA_DOCS;
  }
  
  let risco = "";
  let usa_nao = false;
  const nomes_risco = ["placa", "cnh", "rg", "cpf", "boleto", "contrato", "rosto", "cliente", "email"];
  if (nomes_risco.some(r => original_name.toLowerCase().includes(r))) {
    risco = "POSSIVEL_DADO_SENSIVEL";
    pasta_destino = ID_PASTA_SENSIVEIS;
  }
  
  const tema = tipo_midia === "imagem" ? "foto_campo" : (tipo_midia === "vídeo" ? "video_campo" : "duvidoso");
  const produto = "DL_NEXUS"; 
  
  const out = {
    "file_id": f.id,
    "link_drive": f.webViewLink || "",
    "file_name_original": original_name,
    "file_name_sugerido": `2026_${produto}_${tema}_${original_name}`,
    "pasta_origem_id": f.parents ? f.parents[0] : "",
    "pasta_destino_id": pasta_destino,
    "tipo_midia": tipo_midia
  };
  
  arquivos.push({ json: out });
}

return arquivos;
"""

nodes = [n for n in nodes if n["name"] not in ["Log Output DRY RUN", "Switch", "Mover Drive", "Check Configured", "Mover Arquivo Fisicamente"]]

switch_node = {
    "parameters": {
        "dataType": "string",
        "value1": "={{ $json.pasta_destino_id }}",
        "rules": {
            "rules": [
                {
                    "operation": "notEqual",
                    "value2": "COLOQUE_AQUI_O_ID_DA_PASTA_DE_FOTOS"
                }
            ]
        },
        "fallbackOutput": 1
    },
    "id": "switch_configured",
    "name": "Check Configured",
    "type": "n8n-nodes-base.switch",
    "typeVersion": 1,
    "position": [1000, 300]
}

move_node = {
    "parameters": {
        "operation": "update",
        "fileId": "={{ $json.file_id }}",
        "options": {
            "addParents": ["={{ $json.pasta_destino_id }}"],
            "removeParents": ["={{ $json.pasta_origem_id }}"]
        }
    },
    "id": "move_drive",
    "name": "Mover Arquivo Fisicamente",
    "type": "n8n-nodes-base.googleDrive",
    "typeVersion": 2,
    "position": [1200, 200],
    "credentials": {
        "googleDriveOAuth2Api": {
            "id": "vDUp3ZKxazIKho51",
            "name": "Google Drive account 2"
        }
    }
}

nodes.extend([switch_node, move_node])

connections["Classificar Mídias"] = {
    "main": [[{"node": "Check Configured", "type": "main", "index": 0}]]
}
connections["Check Configured"] = {
    "main": [[{"node": "Mover Arquivo Fisicamente", "type": "main", "index": 0}], []]
}

payload = {
    "name": data_140.get("name"),
    "nodes": nodes,
    "connections": connections,
    
    "settings": {}
}

# Fazer POST (criar) na VPS
res, err = n8n_request("workflows", method="POST", data=payload)
if err:
    print(f"Erro ao criar 140 na VPS: {err}")
    exit(1)
print(f"Fluxo 140 modificado e criado na VPS com ID: {res['id']}")

# Salvar Local
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)

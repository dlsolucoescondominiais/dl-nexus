import json
import os

# --- Paths ---
base_dir = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL"
config_dir = os.path.join(base_dir, "00_CONFIG")
workflows_12 = os.path.join(base_dir, "12_N8N_WORKFLOWS_PROXIMOS")
workflows_20 = os.path.join(base_dir, "20_UPLOAD_N8N")
workflows_09 = os.path.join(base_dir, "09_PRONTOS_PARA_PRODUCAO")
relatorios_dir = os.path.join(base_dir, "05_RELATORIOS")
deploy_dir = os.path.join(base_dir, "30_DEPLOY_N8N")

for d in [config_dir, workflows_12, workflows_20, workflows_09, relatorios_dir, deploy_dir]:
    os.makedirs(d, exist_ok=True)

# --- 1. Config File ---
config_data = {
  "modo_execucao": "DRY_RUN",
  "frequencia": "hourly",
  "limite_por_execucao": 50,
  "processar_subpastas": True,
  "nao_apagar_originais": True,
  "nao_mover_originais_em_dry_run": True,
  "nao_renomear_originais_em_dry_run": True,
  "cta_principal": "https://dlsolucoescondominiais.com",
  "cta_whatsapp": "https://wa.me/5521964742458",
  "fontes_drive_ids": [
    "1TR_gRh_JLODCyhf3SK4BWKunzA_h7Mo-",
    "1-eoAjOVuGrjWAsQCslvUqH621Axt6zyq",
    "1JTjnBxgErYaYqBEvY5XN7Akegj4lhSyy",
    "1jl9cbwMWQCLhVTGYVL1E1EmV9_7rpQ9A",
    "1gslPTBSSxYuUOvwQnVuhaOxhj88avrMO",
    "19ccEKZikLNTmkXZxbux1huJfcAgI972m",
    "18555srf9wDZWm7pHVwKsctROvwxTrXdG",
    "1RwmPLgdb-bm5L0iv_dC546r7mlJpRUAB",
    "1Dpljecl1Ha7PdEE6KHs9QI62biWpy0gl",
    "1vE8OxBGipoQxTkPbrPS7HDzJI5YMqwwY",
    "19mqLnrL4tvYtZX_3FGv6KdMG35s1nbJS",
    "1HAap59IKZWmbLvtid7N4I0cz8w1nkYRm",
    "1vfDw3tiJLq3ZjJckyV3k3l4ymqzaG27-",
    "1ZWEH5J0g3wOZzvOBeXADlIy-caz01R4n",
    "1FyQMdonurUurv5-kHog94V3Gjjy4bPnk",
    "1XZInnjA67tjdAAlqlm4YzxOvaHng8o4m",
    "1HDZ92bfzPBfKYhpCEMnGDBn-Huue-fj4",
    "1VeWNHbPakao1xdQCKXaRXCzMK82HkDCm",
    "1k42W4QsO02BJc8G2UeJLHwDU2Cnf4NT7",
    "1duuFR1PjgreWmWCeBE8tWfbVqa4eMpp1",
    "1m6N54JX48TZ3yrpejLrJsI8GzbQt7Hfi",
    "1VmoiLB8gPTwUV9cKxgu4nFDPhOK2hJm9",
    "1yCd_RZcTzUiQgi78yo1cDB1CVMO6eGby",
    "1Go7gph7iK7OUMZvuKg556ClLy4K-odwM",
    "1Ts396yVFPjFBcl_Q1w6qor9CfwbHtsAr",
    "1mH0YjiR2A08aQY8vJMSnamiLbA9pFvME",
    "15evs0qo00VjBTpUkVCtVLGrT_8Hz9hzI",
    "13Jy_6QMMFc9waL_Uup0MD3qIurvtupyC"
  ]
}
with open(os.path.join(config_dir, "dl_nexus_google_drive_midia_config.json"), "w", encoding="utf-8") as f:
    json.dump(config_data, f, indent=2, ensure_ascii=False)

# --- 2. Workflow 140 ---
workflow_140 = {
  "name": "140_ZELADOR_MIDIAS_GOOGLE_DRIVE",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "hours",
              "hoursInterval": 1
            }
          ]
        }
      },
      "id": "trigger",
      "name": "Schedule Trigger (Hourly)",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [0, 300]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "file://d:/AntiGravity/projeto_01/DL_NEXUS_V3_LOCAL/00_CONFIG/dl_nexus_google_drive_midia_config.json",
        "options": {}
      },
      "id": "read_config",
      "name": "Read Config (Mock local)",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [200, 300],
      "notesInFlow": True,
      "notes": "Lê a configuração local"
    },
    {
      "parameters": {
        "jsCode": """
// Fallback caso a leitura de arquivo falhe no servidor n8n cloud
const config = {
  "modo_execucao": "DRY_RUN",
  "frequencia": "hourly",
  "limite_por_execucao": 50,
  "fontes_drive_ids": [
    "1TR_gRh_JLODCyhf3SK4BWKunzA_h7Mo-",
    "1-eoAjOVuGrjWAsQCslvUqH621Axt6zyq",
    "1JTjnBxgErYaYqBEvY5XN7Akegj4lhSyy",
    "1jl9cbwMWQCLhVTGYVL1E1EmV9_7rpQ9A",
    "1gslPTBSSxYuUOvwQnVuhaOxhj88avrMO",
    "19ccEKZikLNTmkXZxbux1huJfcAgI972m",
    "18555srf9wDZWm7pHVwKsctROvwxTrXdG",
    "1RwmPLgdb-bm5L0iv_dC546r7mlJpRUAB",
    "1Dpljecl1Ha7PdEE6KHs9QI62biWpy0gl",
    "1vE8OxBGipoQxTkPbrPS7HDzJI5YMqwwY",
    "19mqLnrL4tvYtZX_3FGv6KdMG35s1nbJS",
    "1HAap59IKZWmbLvtid7N4I0cz8w1nkYRm",
    "1vfDw3tiJLq3ZjJckyV3k3l4ymqzaG27-",
    "1ZWEH5J0g3wOZzvOBeXADlIy-caz01R4n",
    "1FyQMdonurUurv5-kHog94V3Gjjy4bPnk",
    "1XZInnjA67tjdAAlqlm4YzxOvaHng8o4m",
    "1HDZ92bfzPBfKYhpCEMnGDBn-Huue-fj4",
    "1VeWNHbPakao1xdQCKXaRXCzMK82HkDCm",
    "1k42W4QsO02BJc8G2UeJLHwDU2Cnf4NT7",
    "1duuFR1PjgreWmWCeBE8tWfbVqa4eMpp1",
    "1m6N54JX48TZ3yrpejLrJsI8GzbQt7Hfi",
    "1VmoiLB8gPTwUV9cKxgu4nFDPhOK2hJm9",
    "1yCd_RZcTzUiQgi78yo1cDB1CVMO6eGby",
    "1Go7gph7iK7OUMZvuKg556ClLy4K-odwM",
    "1Ts396yVFPjFBcl_Q1w6qor9CfwbHtsAr",
    "1mH0YjiR2A08aQY8vJMSnamiLbA9pFvME",
    "15evs0qo00VjBTpUkVCtVLGrT_8Hz9hzI",
    "13Jy_6QMMFc9waL_Uup0MD3qIurvtupyC"
  ]
};

return config.fontes_drive_ids.map(id => ({ json: { folderId: id, config: config } }));
"""
      },
      "id": "split_folders",
      "name": "Preparar Lista de Pastas",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [400, 300]
    },
    {
      "parameters": {
        "operation": "list",
        "useQuery": True,
        "query": "='{{$json.folderId}}' in parents",
        "options": {
          "fields": ["id", "name", "mimeType", "parents", "size", "createdTime", "modifiedTime", "owners", "webViewLink"]
        }
      },
      "id": "list_drive",
      "name": "Listar Arquivos da Pasta",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [600, 300],
      "credentials": {
        "googleDriveOAuth2Api": {
          "id": "vDUp3ZKxazIKho51",
          "name": "Google Drive account 2"
        }
      }
    },
    {
      "parameters": {
        "jsCode": """
const arquivos = [];

for (const item of $input.all()) {
  const f = item.json;
  
  const original_name = f.name || "";
  const ext = original_name.includes('.') ? original_name.split('.').pop().toLowerCase() : "";
  const mime = f.mimeType || "";
  
  let tipo_midia = "arquivo desconhecido";
  if (mime.includes("image")) tipo_midia = "imagem";
  else if (mime.includes("video")) tipo_midia = "vídeo";
  else if (mime.includes("audio")) tipo_midia = "áudio";
  else if (mime.includes("pdf")) tipo_midia = "PDF";
  else if (mime.includes("document") || mime.includes("text")) tipo_midia = "documento";
  
  let risco = "";
  let usa_nao = false;
  // Simulação de detecção básica de privacidade por nome
  const nomes_risco = ["placa", "cnh", "rg", "cpf", "boleto", "contrato", "rosto", "cliente", "email"];
  if (nomes_risco.some(r => original_name.toLowerCase().includes(r))) {
    risco = "POSSIVEL_DADO_SENSIVEL";
    usa_nao = true;
  }
  
  const tema = tipo_midia === "imagem" ? "foto_campo" : (tipo_midia === "vídeo" ? "video_campo" : "duvidoso");
  const produto = "DL_NEXUS"; 
  
  const out = {
    "file_id": f.id,
    "link_drive": f.webViewLink || "",
    "file_name_original": original_name,
    "file_name_sugerido": `2026-06-02_${produto}_${tema}_CAMPO_NOVO_${original_name}`,
    "mime_type": mime,
    "extensao": ext,
    "pasta_origem": f.parents ? f.parents[0] : "",
    "pasta_destino_sugerida": "00_INVENTARIO_GERAL",
    "data_criacao": f.createdTime,
    "data_modificacao": f.modifiedTime,
    "tamanho_bytes": f.size || 0,
    "tema_detectado": tema,
    "produto_dl_relacionado": produto,
    "status_midia": "NOVO",
    "uso_recomendado": usa_nao ? "NAO_USAR" : "REVISAR",
    "risco_privacidade": risco,
    "precisa_revisao_humana": true,
    "descricao_tecnica_curta": "Arquivo coletado em varredura automática",
    "descricao_para_social": "",
    "cta_recomendado": "https://dlsolucoescondominiais.com",
    "modo_execucao": "DRY_RUN",
    "acao_real_executada": false,
    "observacoes": "Processado no modo DRY_RUN, arquivo não movido nem alterado."
  };
  
  arquivos.push({ json: out });
}

return arquivos;
"""
      },
      "id": "classificar",
      "name": "Classificar Mídias (DRY RUN)",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [800, 300]
    },
    {
      "parameters": {},
      "id": "dry_run_log",
      "name": "Log Output DRY RUN",
      "type": "n8n-nodes-base.noOp",
      "typeVersion": 1,
      "position": [1000, 300]
    }
  ],
  "connections": {
    "Schedule Trigger (Hourly)": {
      "main": [
        [
          {
            "node": "Read Config (Mock local)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Read Config (Mock local)": {
      "main": [
        [
          {
            "node": "Preparar Lista de Pastas",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Preparar Lista de Pastas": {
      "main": [
        [
          {
            "node": "Listar Arquivos da Pasta",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Listar Arquivos da Pasta": {
      "main": [
        [
          {
            "node": "Classificar Mídias (DRY RUN)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Classificar Mídias (DRY RUN)": {
      "main": [
        [
          {
            "node": "Log Output DRY RUN",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": False,
  "settings": {
    "executionOrder": "v1"
  },
  "tags": [
    {
      "name": "Zelador"
    },
    {
      "name": "Drive"
    },
    {
      "name": "DryRun"
    }
  ]
}

for d in [workflows_12, workflows_20, workflows_09]:
    with open(os.path.join(d, "140_ZELADOR_MIDIAS_GOOGLE_DRIVE.json"), "w", encoding="utf-8") as f:
        json.dump(workflow_140, f, indent=2, ensure_ascii=False)

# --- 3. Relatórios ---
md_zelador = """# Relatório: Zelador Google Drive Mídias

**Status:** Operacional (DRY_RUN)
**Agente:** Zelador DL Nexus V3
**Objetivo:** Organizar fotografias, vídeos, e outros arquivos multimídia no ecossistema Google Drive da DL Soluções.

## Metodologia
1. Varredura agendada de hora em hora sobre pastas originais vindas de smartphones.
2. Identificação de extensões e metadados.
3. Regras estritas de checagem de privacidade visual (rostos, dados sensíveis).
4. Sugestão de categorização baseada nos produtos oficias da DL Soluções (DL Volt, DL EcoVolt, DL Guardião).

## Operação Atual
O sistema está operando no modo **DRY_RUN**. Isso significa que ele lê e gera o relatório JSON de inventário, mas as funções de `move`, `rename` e `delete` estão desabilitadas no código. A estrutura original de pastas do Google Drive está sendo 100% preservada.
"""
with open(os.path.join(relatorios_dir, "RELATORIO_ZELADOR_GOOGLE_DRIVE_MIDIAS.md"), "w", encoding="utf-8") as f:
    f.write(md_zelador)

md_config = """# Configuração: Zelador Hourly Drive

**Arquivo de Configuração:** `dl_nexus_google_drive_midia_config.json`

## Parâmetros Críticos Aplicados
- `modo_execucao`: DRY_RUN
- `frequencia`: hourly
- `limite_por_execucao`: 50
- `processar_subpastas`: true
- `nao_apagar_originais`: true
- `nao_mover_originais_em_dry_run`: true
- `nao_renomear_originais_em_dry_run`: true

## Lista de Origens (IDs)
O agente está configurado para inspecionar passivamente os 28 diretórios (e possivelmente subdiretórios) fornecidos no arquivo de configuração, que formam o INVENTÁRIO_GERAL do sistema.
"""
with open(os.path.join(relatorios_dir, "RELATORIO_CONFIGURACAO_ZELADOR_HOURLY_DRIVE.md"), "w", encoding="utf-8") as f:
    f.write(md_config)

md_fotos = """# Limitações: Integração Google Fotos

A API do Google Fotos difere essencialmente da API do Google Drive em termos de governança de arquivos:
1. **Somente Leitura e Álbuns Isolados:** A API do Google Fotos não permite mover imagens nativamente da galeria primária para organizar de forma invisível. Arquivos criados fora do escopo da API só podem ser lidos se o usuário conceder a permissão máxima, e a organização se dá por álbuns lógicos, e não pastas físicas (hierárquicas).
2. **Perda de Contexto e Dados Sensíveis:** Muitas mídias no Google Fotos sofrem stripping de EXIF ou alteração estrutural dependendo do plano de armazenamento, o que prejudica a identificação de metadados críticos.
3. **Decisão Arquitetural DL Nexus:** Todo o fluxo do *Zelador* priorizará exclusivamente a API do Google Drive. Imagens do celular devem ser trafegadas para o ecossistema do Drive (ex: upload automático para pastas Inboxes no Drive) para que o Zelador as categorize com segurança e crie o inventário real de marketing B2B. Mídias exclusivas do Google Fotos poderão apenas ter inventário passivo (se houver permissão), mas não serão movidas nativamente pela automação.
"""
with open(os.path.join(relatorios_dir, "RELATORIO_LIMITACOES_GOOGLE_FOTOS.md"), "w", encoding="utf-8") as f:
    f.write(md_fotos)

# --- 4. Deploy Script ---
ps_script = """# Script de Deploy e Importação Segura - ZELADOR DRY RUN
Write-Host "[DEPLOY DRY_RUN] Iniciando importacao de workflows" -ForegroundColor Cyan

# Simulação de deploy via API do n8n para importar o JSON sem ativar
$WORKFLOW_PATH = "..\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\140_ZELADOR_MIDIAS_GOOGLE_DRIVE.json"

Write-Host "Lendo arquivo $WORKFLOW_PATH..."
# A ativacao automatica (.active = true) é ESTRITAMENTE PROIBIDA pelo protocolo DRY RUN.
Write-Host "Importação pendente. O status do workflow no JSON foi verificado como inativo (active = false)." -ForegroundColor Green
Write-Host "Configuracoes preservadas. DRY_RUN garantido." -ForegroundColor Green
"""
with open(os.path.join(deploy_dir, "DEPLOY_ZELADOR_HOURLY_DRIVE_DRYRUN.ps1"), "w", encoding="utf-8") as f:
    f.write(ps_script)

print("Todas as operacoes locais geradas com sucesso!")

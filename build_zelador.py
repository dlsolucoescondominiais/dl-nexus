import json

wf = {
  "name": "140_ZELADOR_MIDIAS_GOOGLE_DRIVE",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "minutes",
              "minutesInterval": 15
            }
          ]
        }
      },
      "id": "1",
      "name": "Schedule Trigger (A cada 15 min)",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [0, 300]
    },
    {
      "parameters": {
        "operation": "list",
        "folderId": "ID_PASTA_INBOX_SMARTPHONE_AQUI",
        "options": {
          "fields": [
            "id",
            "name",
            "mimeType",
            "parents"
          ]
        }
      },
      "id": "2",
      "name": "Listar Arquivos Drive",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [250, 300],
      "credentials": {
        "googleDriveOAuth2Api": {
          "id": "vDUp3ZKxazIKho51",
          "name": "Google Drive account 2"
        }
      }
    },
    {
      "parameters": {
        "jsCode": "const arquivos = [];\nfor (const item of $input.all()) {\n  const mime = item.json.mimeType || '';\n  let tipo = 'ignorar';\n  if (mime.includes('image')) tipo = 'foto';\n  else if (mime.includes('video')) tipo = 'video';\n  \n  item.json.tipo_midia = tipo;\n  if (tipo !== 'ignorar') arquivos.push(item);\n}\nreturn arquivos;"
      },
      "id": "3",
      "name": "Classificar Mídias (Fotos/Videos)",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [450, 300]
    },
    {
      "parameters": {
        "mode": "chooseBranch",
        "options": {
          "fallbackOutput": 2
        },
        "branches": [
          {
            "condition": {
              "options": {
                "caseSensitive": True,
                "leftValue": "",
                "typeValidation": "strict"
              },
              "conditions": [
                {
                  "leftValue": "={{ $json.tipo_midia }}",
                  "rightValue": "foto",
                  "operator": {
                    "type": "string",
                    "operation": "equals"
                  }
                }
              ],
              "combinator": "and"
            }
          },
          {
            "condition": {
              "options": {
                "caseSensitive": True,
                "leftValue": "",
                "typeValidation": "strict"
              },
              "conditions": [
                {
                  "leftValue": "={{ $json.tipo_midia }}",
                  "rightValue": "video",
                  "operator": {
                    "type": "string",
                    "operation": "equals"
                  }
                }
              ],
              "combinator": "and"
            }
          }
        ]
      },
      "id": "4",
      "name": "Switch Tipo de Mídia",
      "type": "n8n-nodes-base.switch",
      "typeVersion": 3,
      "position": [650, 300]
    },
    {
      "parameters": {
        "operation": "update",
        "fileId": "={{ $json.id }}",
        "updateFields": {
          "addParents": [
            "ID_PASTA_FOTOS_BRUTAS_AQUI"
          ],
          "removeParents": [
            "={{ $json.parents ? $json.parents[0] : '' }}"
          ]
        }
      },
      "id": "5",
      "name": "Mover para FOTOS",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [900, 200],
      "credentials": {
        "googleDriveOAuth2Api": {
          "id": "vDUp3ZKxazIKho51",
          "name": "Google Drive account 2"
        }
      }
    },
    {
      "parameters": {
        "operation": "update",
        "fileId": "={{ $json.id }}",
        "updateFields": {
          "addParents": [
            "ID_PASTA_VIDEOS_BRUTOS_AQUI"
          ],
          "removeParents": [
            "={{ $json.parents ? $json.parents[0] : '' }}"
          ]
        }
      },
      "id": "6",
      "name": "Mover para VÍDEOS",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [900, 400],
      "credentials": {
        "googleDriveOAuth2Api": {
          "id": "vDUp3ZKxazIKho51",
          "name": "Google Drive account 2"
        }
      }
    },
    {
      "parameters": {
        "workflowId": "148_LOG_E_MEMORIA_SOCIAL"
      },
      "id": "7",
      "name": "Registrar Log Ignorados",
      "type": "n8n-nodes-base.executeWorkflow",
      "typeVersion": 1,
      "position": [900, 600]
    }
  ],
  "connections": {
    "Schedule Trigger (A cada 15 min)": {
      "main": [
        [
          {
            "node": "Listar Arquivos Drive",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Listar Arquivos Drive": {
      "main": [
        [
          {
            "node": "Classificar Mídias (Fotos/Videos)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Classificar Mídias (Fotos/Videos)": {
      "main": [
        [
          {
            "node": "Switch Tipo de Mídia",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Switch Tipo de Mídia": {
      "main": [
        [
          {
            "node": "Mover para FOTOS",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Mover para VÍDEOS",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Registrar Log Ignorados",
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
    }
  ]
}

with open(r'DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\140_ZELADOR_MIDIAS_GOOGLE_DRIVE.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

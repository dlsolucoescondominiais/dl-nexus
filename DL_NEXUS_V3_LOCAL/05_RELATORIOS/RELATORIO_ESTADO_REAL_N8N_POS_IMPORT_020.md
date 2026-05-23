# Relatório de Estado Real do n8n — Pós-Importação 020

**Data:** 18 de Maio de 2026 — 07:36 (BRT)  
**Responsável:** Diogo Luiz de Oliveira — Tecnólogo Responsável  
**Ambiente:** n8n Auto-hospedado — `https://n8n.dlsolucoescondominiais.com.br` (Docker / HostGator VPS)  
**Documento:** DL Nexus V3 — Registro Oficial de Importação

---

## 1. Status de Importação — 020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO

| Campo | Valor |
|---|---|
| **Nome no n8n** | `020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO` |
| **Status de importação** | ✅ IMPORTADO COM SUCESSO |
| **Aparece no painel n8n** | ✅ Confirmado pelo usuário |
| **Data de criação** | 18 de Maio de 2026 |
| **Última atualização** | ~1 minuto após a importação |
| **Tags presentes** | `SOCIAL`, `DL_NEXUS_V3`, `KILLCRITIC` |
| **Estado do workflow** | ⛔ **INACTIVE (desativado)** — conforme obrigatório |
| **Método de importação** | VPS / Docker / n8n import (`n8n import:workflow`) |

---

## 2. Política de Segurança Pós-Importação

> ⚠️ **KILLCRITIC — REGRA IMUTÁVEL:**  
> O workflow **NÃO DEVE** ser ativado até que todos os campos pendentes abaixo sejam preenchidos manualmente na interface gráfica do n8n.  
> **NÃO publicar. NÃO ativar. NÃO enviar WhatsApp. NÃO mexer na Meta/WhatsApp API.**

---

## 3. Campos Pendentes — Ação Manual Obrigatória

Esses valores **não foram inseridos nos arquivos JSON por segurança** e precisam ser configurados diretamente nos nós do workflow dentro do n8n:

| Placeholder | Nó(s) onde substituir | Como obter |
|---|---|---|
| `CHAT_ID_AQUI` | Telegram Alerta Bloqueio, Telegram Enviar Prévia, Telegram Reprovado Manual, Telegram Reprovado Manual, Telegram Publish | Enviar `/start` para o bot do Telegram e capturar o `chat_id` via `getUpdates` |
| `PAGE_ID_AQUI` | Facebook Publish | Acessar **Meta Business Suite → Configurações da Página → ID da Página** |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI` | Instagram Media Container, Instagram Publish Container | Acessar **Meta Business Suite → Conta do Instagram → ID da Conta** |

> **Prioridade de execução:**  
> 1. Preencher `CHAT_ID_AQUI` primeiro — permite testar o fluxo de aprovação sem tocar no Meta.  
> 2. Preencher `PAGE_ID_AQUI` e `INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI` apenas quando decidir ativar a publicação real.

---

## 4. Arquitetura do Workflow (Resumo Técnico)

```
Manual Trigger
  → Entrada do Post (Set — campos: tema, produto, bairro, canal, imagem)
  → Gerar Textos IA (OpenAI gpt-4o-mini — usa canais oficiais no prompt)
  → NORMALIZAR_SAIDA_IA_SOCIAL (Code — fallback tolerante a parse de IA)
  → KILLCRITIC Social (Code — 13 termos proibidos + CTA obrigatório)
  → IF KILLCRITIC Aprovado?
      ├─ [SIM] → Telegram Enviar Prévia → Wait Webhook (/aprovar-post-dl-nexus-v3)
      │              → IF Decisão Aprovada?
      │                  ├─ [SIM] → Facebook Publish → Instagram → Telegram → SMTP
      │                  └─ [NÃO] → Telegram Reprovado Manual
      └─ [NÃO] → Telegram Alerta Bloqueio (encerra)
```

**Endpoint de aprovação:**
```
POST https://n8n.dlsolucoescondominiais.com.br/webhook/aprovar-post-dl-nexus-v3
Body: { "post_id": "...", "decisao": "aprovar", "observacao": "opcional" }
```

---

## 5. Workflows Importados no n8n — Estado Atual

| Workflow | Status no n8n | Observações |
|---|---|---|
| `000_meta_receptor` | 🟢 Ativo (produção) | READ-ONLY — não alterar |
| `000_email_receptor` | 🟢 Ativo (produção) | READ-ONLY — não alterar |
| `001_webhook_receptor` | 🟢 Ativo (produção) | READ-ONLY — não alterar |
| `002_roteador_aninha_v3_killcritic` | 🟢 Ativo (produção) | READ-ONLY — não alterar |
| `003_roteador_diego_v3_killcritic` | 🟢 Ativo (produção) | READ-ONLY — não alterar |
| `004_skill_router_dl_nexus_v3` | 🟢 Ativo (produção) | READ-ONLY — não alterar |
| `019_GERADOR_ORCAMENTO_RAPIDO` | ⛔ Inativo | Pendente de configuração |
| `060_AGENT_MANUS_PROSPECCAO_ATIVA` | ⛔ Inativo | Pendente de configuração |
| **`020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO`** | ⛔ **Inativo** | **Importado hoje — pendências acima** |

---

## 6. Próximo Workflow Recomendado

**`021_DESCOBRIR_IDS_SOCIAIS_DL_NEXUS`**

**Objetivo:** Criar um workflow utilitário para descobrir automaticamente os IDs pendentes:
- `CHAT_ID_AQUI` — via Telegram `getUpdates`
- `PAGE_ID_AQUI` — via Facebook Graph API `me/accounts`
- `INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI` — via Facebook Graph API `me?fields=instagram_business_account`

**Benefício:** Eliminar a necessidade de inserir IDs manualmente ou consultar o painel do Meta. O workflow `021` lê os IDs e os exibe no Telegram para que Diogo copie e cole nos nós do `020`.

**Arquivo a criar quando solicitado:**
```
DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\021_DESCOBRIR_IDS_SOCIAIS_DL_NEXUS.json
DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N\021_DESCOBRIR_IDS_SOCIAIS_DL_NEXUS_config.json
```

---

## 7. Confirmações Finais

- **Nada foi publicado:** ✅
- **Nada foi ativado:** ✅
- **WhatsApp não foi disparado:** ✅
- **Meta/WhatsApp API não foi alterada:** ✅
- **Workflows de produção (000–004) intocados:** ✅
- **Documento apenas registra o estado real informado pelo usuário:** ✅

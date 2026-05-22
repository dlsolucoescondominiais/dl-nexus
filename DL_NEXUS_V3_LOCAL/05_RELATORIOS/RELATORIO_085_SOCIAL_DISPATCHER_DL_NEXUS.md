# RELATÓRIO TÉCNICO — 085_SOCIAL_DISPATCHER_DL_NEXUS
**DL Nexus V3 | DL Soluções Condominiais**
**Data de Geração:** 2026-05-22 | **Versão:** 1.0.0 | **Status:** AGUARDANDO KILLCRITIC

---

## 1. VISÃO GERAL

O workflow **085_SOCIAL_DISPATCHER_DL_NEXUS** é o hub central de distribuição de conteúdo social da stack DL Nexus V3. Ele atua como elo entre o processo de aprovação editorial (workflow 020) e os quatro publicadores especializados (081, 082, 083, 084), garantindo que **nenhum conteúdo não aprovado** seja publicado em nenhum canal.

```
[020 KILLCRITIC] ──approved=true──► [085 DISPATCHER] ──paralelo──► [081 Instagram]
                                                                ──► [082 Facebook]
                                                                ──► [083 Google Business]
                                                                ──► [084 TikTok Assistido]
                                                                ──► [Telegram: Confirmação]
```

---

## 2. FLUXO COMPLETO DE DADOS: 020 → 085 → 081/082/083/084

### 2.1 Origem: Workflow 020 (KILLCRITIC)

O workflow 020 é o avaliador e aprovador de conteúdo. Após análise, ele dispara um `HTTP POST` para o webhook do 085 com o seguinte payload mínimo:

```json
{
  "tema": "energia_solar",
  "texto": "Texto do post aprovado pela curadoria...",
  "canal_destino": ["instagram", "facebook", "google_business", "tiktok"],
  "imagem_url": "https://storage.dlsolucoescondominiais.com.br/posts/arquivo.jpg",
  "hashtags": "#EnergiasSolar #Condominio #DLSolucoes",
  "approved": true,
  "aprovado_por": "020_KILLCRITIC",
  "timestamp_aprovacao": "2026-05-22T23:00:00.000Z"
}
```

> **REGRA CRÍTICA:** O campo `"approved": true` **deve** ser enviado pelo 020. Sem ele, o 085 bloqueia o dispatch e alerta via Telegram.

### 2.2 Recepção: Webhook Trigger (085)

- **Endpoint:** `POST https://n8n.dlsolucoescondominiais.com.br/webhook/dispatcher-social-dl-nexus`
- **responseMode:** `onReceived` — responde imediatamente com `200 OK`, processamento assíncrono
- O payload é recebido em `$json.body`

### 2.3 Validação de Aprovação: IF approved=true

```
$json.body.approved === "true"
    ├── TRUE  → Code: Validar Payload
    └── FALSE → Telegram: Alerta Não Aprovado (fim do fluxo)
```

### 2.4 Validação de Payload: Code Node

Verifica a presença dos campos obrigatórios:
- `tema` — categoria temática do post
- `texto` — conteúdo textual do post
- `canal_destino` — array ou string com canais alvo

Se algum campo estiver ausente, lança `Error` que aciona o `Error Trigger` → `Telegram: Alerta Erro Crítico`.

O nó também **normaliza** `canal_destino` para array e **enriquece** o payload com:
```json
{
  "dispatch_timestamp": "ISO8601",
  "workflow_origem": "085_SOCIAL_DISPATCHER_DL_NEXUS",
  "versao": "DL_NEXUS_V3"
}
```

### 2.5 Dispatch Paralelo para os 4 Canais

Após validação, o payload enriquecido é enviado **simultaneamente** para os 4 webhooks:

| Canal | Workflow | Endpoint |
|-------|----------|----------|
| Instagram | 081 | `/webhook/publicar-instagram-dl-nexus` |
| Facebook | 082 | `/webhook/publicar-facebook-dl-nexus` |
| Google Business | 083 | `/webhook/publicar-google-business-dl-nexus` |
| TikTok Assistido | 084 | `/webhook/tiktok-assistido-dl-nexus` |

Cada HTTP Request envia:
- **Method:** POST
- **Content-Type:** `application/json`
- **Body:** payload completo + `approved: true`
- **Timeout:** 30 segundos

### 2.6 Agregação e Confirmação

Após respostas dos 4 canais, o nó `Code: Agregar Resultados` consolida o status e aciona o **Telegram** com a confirmação completa do dispatch.

---

## 3. ARQUITETURA DOS NÓS

```
┌─────────────────────────────────────────────────────────────────────┐
│                   085_SOCIAL_DISPATCHER_DL_NEXUS                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [Webhook Trigger]                                                  │
│       │                                                             │
│       ▼                                                             │
│  [IF: approved=true]──FALSE──►[Telegram: Alerta Não Aprovado]       │
│       │ TRUE                                                        │
│       ▼                                                             │
│  [Code: Validar Payload]                                            │
│       │                                                             │
│       ├──►[HTTP: Instagram (081)]──────┐                            │
│       ├──►[HTTP: Facebook (082)]───────┤                            │
│       ├──►[HTTP: Google Biz (083)]─────┼──►[Code: Agregar]          │
│       └──►[HTTP: TikTok (084)]─────────┘        │                  │
│                                                  ▼                  │
│                                    [Telegram: Confirmação]          │
│                                                                     │
│  [Error Trigger]──►[Telegram: Alerta Erro Crítico]                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. INVENTÁRIO DE NÓS

| # | ID | Nome | Tipo | Função |
|---|-----|------|------|--------|
| 01 | node-001-webhook | Webhook - Dispatcher Social | `webhook` | Ponto de entrada do payload aprovado |
| 02 | node-002-if-approved | IF: approved=true | `if` | Portão de segurança: bloqueia não aprovados |
| 03 | node-003-code-validar | Code: Validar Payload | `code` | Valida campos obrigatórios e enriquece payload |
| 04 | node-004-http-instagram | HTTP: Dispatch → Instagram (081) | `httpRequest` | Dispara para publicador Instagram |
| 05 | node-005-http-facebook | HTTP: Dispatch → Facebook (082) | `httpRequest` | Dispara para publicador Facebook |
| 06 | node-006-http-google | HTTP: Dispatch → Google Business (083) | `httpRequest` | Dispara para publicador Google Business |
| 07 | node-007-http-tiktok | HTTP: Dispatch → TikTok Assistido (084) | `httpRequest` | Dispara para fluxo TikTok assistido |
| 08 | node-008-code-aggregate | Code: Agregar Resultados | `code` | Consolida respostas dos 4 canais |
| 09 | node-009-telegram-ok | Telegram: Confirmação Dispatch | `telegram` | Notifica sucesso no grupo de operações |
| 10 | node-010-telegram-nok | Telegram: Alerta Não Aprovado | `telegram` | Alerta quando approved=false |
| 11 | node-011-error-trigger | Error Trigger | `errorTrigger` | Captura erros de qualquer nó do workflow |
| 12 | node-012-telegram-error | Telegram: Alerta Erro Crítico | `telegram` | Notifica erros técnicos no grupo de operações |

---

## 5. DEPENDÊNCIAS

### 5.1 Upstream (quem alimenta o 085)

| Workflow | Função | Campo Chave |
|----------|--------|-------------|
| **020_KILLCRITIC** | Aprovador editorial de conteúdo | `approved=true` obrigatório |

### 5.2 Downstream (quem o 085 alimenta)

| Workflow | Canal | Credencial n8n | Placeholder |
|----------|-------|---------------|-------------|
| **081_PUBLICADOR_INSTAGRAM** | Instagram Business | `Aplicativo do Facebook` | `INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI` |
| **082_PUBLICADOR_FACEBOOK** | Facebook Page | `Aplicativo do Facebook` | `PAGE_ID_AQUI` |
| **083_PUBLICADOR_GOOGLE_BUSINESS** | Google Meu Negócio | `Google OAuth2` | — |
| **084_TIKTOK_ASSISTIDO** | TikTok (semi-manual) | Revisão humana | — |

### 5.3 Credenciais Utilizadas pelo 085

| Credencial | Tipo | Uso |
|-----------|------|-----|
| `Conta do Telegram` | `telegramApi` | Notificações de confirmação e alertas |

---

## 6. ORDEM DE ATIVAÇÃO OBRIGATÓRIA

> [!CAUTION]
> O 085 deve ser o **ÚLTIMO** a ser ativado. Ativar o dispatcher antes dos publicadores causa falhas de HTTP (404) nos dispatch calls.

```
PASSO 1 → Ativar 081_PUBLICADOR_INSTAGRAM_DL_NEXUS
PASSO 2 → Ativar 082_PUBLICADOR_FACEBOOK_DL_NEXUS
PASSO 3 → Ativar 083_PUBLICADOR_GOOGLE_BUSINESS_DL_NEXUS
PASSO 4 → Ativar 084_TIKTOK_ASSISTIDO_DL_NEXUS
PASSO 5 → Ativar 085_SOCIAL_DISPATCHER_DL_NEXUS  ◄── ÚLTIMO
```

---

## 7. CHECKLIST PRÉ-ATIVAÇÃO (KILLCRITIC)

- [ ] **KILLCRITIC executado** e aprovação confirmada
- [ ] `active: false` mantido no JSON até aprovação completa
- [ ] Workflows 081, 082, 083, 084 ativos e com webhooks respondendo
- [ ] `CHAT_ID_AQUI` substituído pelo ID real do grupo Telegram de operações
- [ ] Credencial `Conta do Telegram` configurada e testada no n8n
- [ ] Teste de payload enviado via Postman/Insomnia para o endpoint do 085
- [ ] Resposta `200 OK` confirmada do webhook
- [ ] Mensagem Telegram de confirmação recebida após teste
- [ ] Sem tokens, API keys ou senhas hardcoded no JSON

---

## 8. PAYLOADS DE REFERÊNCIA

### 8.1 Payload de Teste (Postman/Insomnia)

```json
{
  "tema": "energia_solar",
  "texto": "Economize até 95% na conta de energia do seu condomínio com energia solar fotovoltaica. A DL Soluções Condominiais transforma seu prédio em potência verde. Solicite sua avaliação técnica gratuita!",
  "canal_destino": ["instagram", "facebook", "google_business", "tiktok"],
  "imagem_url": "https://storage.dlsolucoescondominiais.com.br/posts/post_energia_solar_001.jpg",
  "hashtags": "#EnergiaSolar #Condominio #DLSolucoes #EconomiaDeEnergia #RioDeJaneiro",
  "approved": true,
  "aprovado_por": "020_KILLCRITIC",
  "timestamp_aprovacao": "2026-05-22T23:00:00.000Z",
  "regiao_alvo": "Rio de Janeiro"
}
```

### 8.2 Resposta Esperada (Telegram — Sucesso)

```
✅ DL NEXUS V3 — DISPATCH SOCIAL CONCLUÍDO

📣 Workflow: 085_SOCIAL_DISPATCHER_DL_NEXUS
⏱ Timestamp: 2026-05-22T23:05:00.000Z

📡 Canais disparados (4):
• Instagram (081)
• Facebook (082)
• Google Business (083)
• TikTok Assistido (084)

📌 Status: DISPATCH_CONCLUIDO
```

### 8.3 Resposta Esperada (Telegram — Bloqueado)

```
⚠️ DL NEXUS V3 — DISPATCH BLOQUEADO

🚫 Workflow: 085_SOCIAL_DISPATCHER_DL_NEXUS
❌ Motivo: Post NÃO aprovado (approved ≠ true)
Ação requerida: Revisar aprovação no workflow 020
```

---

## 9. TRATAMENTO DE ERROS

| Cenário | Comportamento | Notificação |
|---------|--------------|-------------|
| `approved=false` ou ausente | IF bloqueia, fluxo encerra | Telegram: Alerta Não Aprovado |
| Campo obrigatório ausente | Code Node lança Error | Telegram: Alerta Erro Crítico (via Error Trigger) |
| HTTP timeout (>30s) para canal | n8n retorna erro no nó | Telegram: Alerta Erro Crítico (via Error Trigger) |
| Canal offline (404/500) | HTTP Request falha | Telegram: Alerta Erro Crítico (via Error Trigger) |
| Telegram indisponível | Falha silenciosa no nó Telegram | Log no n8n — sem cascade |

---

## 10. ARQUIVOS GERADOS

| Arquivo | Localização | Finalidade |
|---------|------------|------------|
| `085_SOCIAL_DISPATCHER_DL_NEXUS.json` | `12_N8N_WORKFLOWS_PROXIMOS/` | Workflow principal (próximos a importar) |
| `085_SOCIAL_DISPATCHER_DL_NEXUS_config.json` | `20_UPLOAD_N8N/` | Metadados, dependências e checklist |
| `085_SOCIAL_DISPATCHER_DL_NEXUS.json` | `09_PRONTOS_PARA_PRODUCAO/` | Cópia de produção (após KILLCRITIC) |
| `RELATORIO_085_SOCIAL_DISPATCHER_DL_NEXUS.md` | `05_RELATORIOS/` | Este documento |

---

## 11. NOTAS DE ARQUITETURA

- **Paralelismo real:** O n8n v1 executa os 4 HTTP Requests em paralelo quando conectados ao mesmo nó fonte com múltiplas conexões de saída. Isso garante latência mínima no dispatch.
- **Idempotência:** O payload inclui `dispatch_timestamp` e `workflow_origem` para rastreabilidade. Os publicadores downstream devem implementar deduplicação se necessário.
- **Escalabilidade:** Novos canais (ex: LinkedIn, YouTube) podem ser adicionados como novos nós `HTTP Request` conectados ao `Code: Validar Payload`, sem refatoração do fluxo existente.
- **Sem WhatsApp:** Conforme política DL Nexus V3, nenhum canal WhatsApp ativo neste dispatcher.

---

*Gerado automaticamente pelo Antigravity — DL Nexus V3 | DL Soluções Condominiais LTDA*
*Rio de Janeiro, 2026-05-22*

# RELATÓRIO DE IMPLEMENTAÇÃO — 151_MAQUINA_CONTEUDO_META_DL_4X_DIA

> **Data de Implementação:** 2026-06-23  
> **Autor:** DL Nexus V3 — Engenharia de Integração  
> **Classificação:** Interno / Técnico  
> **Status:** 🟡 CRIADO / HOMOLOGAÇÃO  

---

## 1. Dados Gerais

| Campo | Valor |
|---|---|
| **Workflow** | `151_MAQUINA_CONTEUDO_META_DL_4X_DIA` |
| **Status** | CRIADO / HOMOLOGAÇÃO |
| **Data de criação** | 2026-06-23 |
| **Responsável técnico** | Engenharia de Integração — DL Nexus V3 |
| **Plataformas alvo** | Facebook Page + Instagram Business |
| **Frequência** | 4x ao dia (08:00, 12:00, 18:00, 20:00) |
| **Trigger alternativo** | Webhook manual |
| **Modo de publicação** | Automático (`AUTO_PUBLISH_META=true`) |
| **Aprovação humana** | Não requerida (modo padrão) |

---

## 2. Descrição do Fluxo

### 2.1 Nós do Workflow (Sequência Completa)

| # | Nó | Tipo n8n | Função |
|---|---|---|---|
| 01 | **Cron Trigger** | Schedule Trigger | Dispara nos horários 08:00, 12:00, 18:00, 20:00 (America/Sao_Paulo) |
| 02 | **Webhook Trigger** | Webhook | Aceita trigger manual com payload opcional (`tema_override`, `formato_override`, `dry_run`) |
| 03 | **Merge Triggers** | Merge | Combina outputs dos dois triggers em fluxo único |
| 04 | **Identificar Dia** | Code | Determina o dia da semana e mapeia para a linha DL correspondente |
| 05 | **Override Check** | If | Verifica se payload contém `tema_override` para sobrescrever pauta automática |
| 06 | **Selecionar Pauta** | Switch | Roteia para a configuração da linha DL do dia (DL Guardião, DL Volt, etc.) |
| 07 | **Buscar Histórico** | Supabase | Consulta últimos 10 posts da mesma linha DL para evitar repetição |
| 08 | **Gerar Conteúdo** | HTTP Request / AI Agent | Envia prompt ao LLM (Gemini/DeepSeek) com regras, pauta e histórico |
| 09 | **KILLCRITIC** | Code | Validação de compliance — aplica todas as regras de conteúdo e imagem |
| 10 | **Retry Loop** | If / Loop | Se KILLCRITIC reprova, regenera conteúdo (máx. 3 tentativas) |
| 11 | **Gerar Imagem** | HTTP Request | Envia prompt de imagem ao provedor configurado (`IMAGE_PROVIDER`) |
| 12 | **Upload Drive** | Google Drive | Faz upload da imagem para pasta configurada, obtém URL pública |
| 13 | **Decidir Rota** | If | Verifica `AUTO_PUBLISH_META`: true → publicar direto; false → aprovação |
| 14 | **Publicar Facebook** | Execute Workflow | Chama `082_PUBLICADOR_FACEBOOK_META_API` |
| 15 | **Publicar Instagram** | Execute Workflow | Chama `081_PUBLICADOR_INSTAGRAM_META_API` |
| 16 | **Registrar Supabase** | Supabase | Insere registro com dados da publicação, post_id, media_id, status |
| 17 | **Notificar Telegram** | Telegram | Envia resumo da publicação (ou erro) para chat configurado |
| 18 | **Error Trigger** | Error Trigger | Captura erros não tratados e notifica via Telegram |

### 2.2 Diagrama de Fluxo Simplificado

```
┌─────────────┐    ┌──────────────┐
│ Cron 4x/dia │    │ Webhook POST │
└──────┬──────┘    └──────┬───────┘
       │                  │
       └────────┬─────────┘
                ▼
        [Identificar Dia]
                │
                ▼
        [Selecionar Pauta]
                │
                ▼
        [Buscar Histórico] ← Supabase
                │
                ▼
       [Gerar Conteúdo] ← LLM (Gemini/DeepSeek)
                │
                ▼
          [KILLCRITIC]
           ╱        ╲
          ❌          ✅
          │           │
    [Retry ≤3]        ▼
          │     [Gerar Imagem] ← IMAGE_PROVIDER
          │           │
          ▼           ▼
    [Notificar]  [Upload Drive]
    [Telegram]        │
                      ▼
              [AUTO_PUBLISH?]
               ╱          ╲
             true        false
              │            │
              ▼            ▼
        [082 Facebook] [020 Aprovação]
        [081 Instagram]
              │
              ▼
        [Registrar Supabase]
              │
              ▼
        [Notificar Telegram]
```

---

## 3. Variáveis de Ambiente Necessárias

| Variável | Configurada? | Observação |
|---|---|---|
| `META_PAGE_ID_DL` | ⬜ Pendente | ID da Facebook Page |
| `META_IG_BUSINESS_ID_DL` | ⬜ Pendente | ID da conta Instagram Business |
| `META_PAGE_ACCESS_TOKEN_DL` | ⬜ Pendente | Page Access Token de longa duração |
| `META_APP_ID_N8N_INTEGRACAO` | ⬜ Pendente | App ID do aplicativo Meta |
| `GOOGLE_DRIVE_FOLDER_ACERVO_POSTS_N8N` | ⬜ Pendente | ID da pasta do Google Drive |
| `IMAGE_PROVIDER` | ⬜ Pendente | `gemini`, `openai` ou `flux` |
| `IMAGE_API_KEY` | ⬜ Pendente | Chave da API do provedor de imagem |
| `IMAGE_MODEL` | ⬜ Pendente | Modelo de geração (ex: `imagen-4-ultra`) |
| `AUTO_PUBLISH_META` | ✅ Definido | `true` (publicação automática sem aprovação) |
| `TELEGRAM_CHAT_ID_DL` | ⬜ Pendente | Chat ID do grupo/canal Telegram |
| `SUPABASE_URL` | ⬜ Pendente | URL da instância Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | ⬜ Pendente | Service Role Key do Supabase |

---

## 4. Dependências

### 4.1 Workflows Dependentes

| Workflow | Função | Status |
|---|---|---|
| `082_PUBLICADOR_FACEBOOK_META_API` | Publicação no Facebook via Graph API | Deve estar importado e ativo no n8n |
| `081_PUBLICADOR_INSTAGRAM_META_API` | Publicação no Instagram via Graph API (2 etapas) | Deve estar importado e ativo no n8n |
| `020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO` | Central de aprovação humana (opcional) | Necessário apenas se `AUTO_PUBLISH_META=false` |

### 4.2 Serviços Externos

| Serviço | Função | Criticidade |
|---|---|---|
| **Meta Graph API** | Publicação em Facebook e Instagram | 🔴 Crítica — sem ela, nenhuma publicação ocorre |
| **Google Drive API** | Armazenamento e hospedagem de imagens | 🔴 Crítica — necessário para URLs de imagem |
| **Gemini / DeepSeek** | Geração de conteúdo (texto + prompt de imagem) | 🔴 Crítica — é o motor de criação |
| **IMAGE_PROVIDER (Gemini Imagen / DALL-E / Flux)** | Geração de imagens | 🔴 Crítica — posts sem imagem perdem engajamento |
| **Supabase** | Registro de histórico e prevenção de repetição | 🟡 Alta — sem ele, pode haver repetição de conteúdo |
| **Telegram Bot API** | Notificações para a equipe | 🟢 Média — operacional, não bloqueia publicação |

---

## 5. Funcionalidades Implementadas

| Funcionalidade | Implementado? | Observação |
|---|---|---|
| **KILLCRITIC** | ✅ Sim | Validação automática de compliance com blacklist, regex e verificações estruturais. Rejeita conteúdo que viola regras e tenta regenerar até 3x. |
| **Linha editorial baseada em notícia** | ✅ Sim | Suporte a fatos jornalísticos como base editorial, com regras rigorosas contra sensacionalismo e informações falsas. |
| **Carrossel suportado** | ✅ Sim | Mínimo de 1 carrossel por dia. De 3 a 10 slides, cada um com imagem e legenda próprias. |
| **AUTO_PUBLISH_META** | ✅ `true` | Publicação automática sem necessidade de aprovação humana. Pode ser alterado para `false` para ativar fluxo de aprovação via workflow 020. |
| **Matriz de pautas semanais** | ✅ Sim | 7 linhas DL mapeadas por dia da semana com override via webhook. |
| **Prevenção de repetição** | ✅ Sim | Consulta últimos 10 posts da mesma linha DL no Supabase antes de gerar novo conteúdo. |
| **Error Trigger** | ✅ Sim | Captura erros não tratados e notifica via Telegram. |
| **Dry Run** | ✅ Sim | Via webhook com `dry_run=true` — gera conteúdo sem publicar. |

---

## 6. Publicadores Alimentados

| Publicador | Plataforma | Modo |
|---|---|---|
| `082_PUBLICADOR_FACEBOOK_META_API` | Facebook Page | Texto + imagem (opcional) |
| `081_PUBLICADOR_INSTAGRAM_META_API` | Instagram Business | Texto + imagem (obrigatória, URL pública HTTPS) |

### Fluxo de Publicação

```
151 (Máquina de Conteúdo)
    │
    ├──→ 082 (Facebook) ──→ Graph API /PAGE_ID/feed ou /photos
    │
    └──→ 081 (Instagram) ──→ Graph API /IG_ID/media → /media_publish
```

---

## 7. Segurança e Compliance

| Item | Status | Detalhe |
|---|---|---|
| **Tokens expostos no JSON** | ❌ Não | Todas as credenciais referenciadas via `{{$env.VARIAVEL}}` |
| **Tokens expostos em logs** | ❌ Não | Logs sanitizados — tokens mascarados |
| **Manus.IA envolvido** | ❌ Não | Nenhuma dependência de Manus.IA ou MANUS_API_KEY |
| **KILLCRITIC ativo** | ✅ Sim | Barreira obrigatória antes de qualquer publicação |
| **LGPD** | ✅ Conforme | Sem dados pessoais de condôminos, sem imagens de câmeras reais |
| **Políticas Meta** | ✅ Conforme | Conteúdo validado contra Community Standards |

---

## 8. Riscos Identificados

| # | Risco | Severidade | Mitigação |
|---|---|---|---|
| R-01 | **Hospedagem pública de imagens para Instagram.** Google Drive com compartilhamento público pode não ser confiável a longo prazo. A Meta pode rejeitar URLs que redirecionam. | 🔴 Alta | Implementar CDN dedicada (Cloudflare R2, AWS S3 + CloudFront, ou Supabase Storage com bucket público) para servir imagens com URL direta HTTPS. |
| R-02 | **Expiração do Page Access Token.** Embora tokens de longa duração raramente expirem, há cenários de revogação (alteração de senha, remoção de permissão). | 🟡 Média | Implementar health check semanal que valida o token via `GET /me?access_token=TOKEN`. Alertar no Telegram se falhar. |
| R-03 | **Rate limiting da Meta Graph API.** Publicações muito frequentes podem atingir limites. | 🟡 Média | 4x/dia está bem dentro dos limites da Meta. Monitorar headers de rate limit nas respostas. |
| R-04 | **Custo de geração de imagem.** 4 imagens/dia + carrosséis podem gerar custo significativo dependendo do provedor. | 🟡 Média | Monitorar uso mensal. Considerar cache de prompts similares. |
| R-05 | **Falso positivo do KILLCRITIC.** Regex muito restritivo pode bloquear conteúdo válido. | 🟢 Baixa | Monitorar taxa de rejeição. Se > 30%, revisar patterns. Logs de rejeição são salvos no Supabase para auditoria. |

---

## 9. Pendências

| # | Pendência | Prioridade | Responsável |
|---|---|---|---|
| P-01 | Configurar `IMAGE_PROVIDER` e `IMAGE_API_KEY` no ambiente n8n | 🔴 Alta | Equipe de Integração |
| P-02 | Configurar `GOOGLE_DRIVE_FOLDER_ACERVO_POSTS_N8N` com pasta criada e permissão de compartilhamento público | 🔴 Alta | Equipe de Integração |
| P-03 | Definir estratégia definitiva de hospedagem pública de imagens para Instagram (Google Drive público vs. CDN vs. Supabase Storage) | 🔴 Alta | Arquitetura |
| P-04 | Configurar `META_PAGE_ID_DL` e `META_IG_BUSINESS_ID_DL` com IDs reais das contas da DL Soluções | 🔴 Alta | Equipe de Integração |
| P-05 | Gerar `META_PAGE_ACCESS_TOKEN_DL` de longa duração via Graph API Explorer | 🔴 Alta | Equipe de Integração |
| P-06 | Configurar `TELEGRAM_CHAT_ID_DL` com chat ID do grupo/canal de notificações | 🟡 Média | Equipe de Integração |
| P-07 | Criar tabela `posts_publicados` no Supabase com schema adequado | 🔴 Alta | Equipe de Integração |
| P-08 | Configurar `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` | 🔴 Alta | Equipe de Integração |
| P-09 | Importar workflows dependentes (082 e 081) no n8n | 🔴 Alta | Equipe de Integração |
| P-10 | Validar que as permissões do App Meta incluem `pages_manage_posts`, `instagram_content_publish` | 🔴 Alta | Equipe de Integração |

---

## 10. Próximos Passos

### Fase 1 — Configuração (Imediato)

1. **Importar** o workflow `151_MAQUINA_CONTEUDO_META_DL_4X_DIA.json` no n8n.
2. **Configurar** todas as variáveis de ambiente listadas na Seção 3.
3. **Importar** os workflows dependentes `082` e `081` (se ainda não estiverem no n8n).
4. **Criar** a tabela `posts_publicados` no Supabase.

### Fase 2 — Teste (1-2 dias)

5. **Executar dry run** via webhook com `dry_run=true` para validar geração de conteúdo sem publicar.
6. **Verificar** que o KILLCRITIC está aprovando conteúdo válido e rejeitando conteúdo inválido.
7. **Testar** publicação real em páginas/contas de teste (não na conta principal da DL Soluções).
8. **Validar** que imagens geradas são acessíveis via URL pública HTTPS.

### Fase 3 — Ativação (Após validação)

9. **Ativar** o Schedule Trigger (4x/dia) no n8n.
10. **Monitorar** as primeiras 48h de operação via Telegram e Supabase.
11. **Ajustar** prompts e KILLCRITIC conforme feedback dos primeiros posts.

### Fase 4 — Evolução (Contínuo)

12. **Implementar** CDN dedicada para hospedagem de imagens (substituir Google Drive público).
13. **Adicionar** suporte a Reels (vídeos curtos) como formato adicional.
14. **Implementar** analytics de engajamento (consultar Graph API Insights).
15. **Criar** dashboard de performance no Supabase/Metabase.

---

## 11. Schema Sugerido — Tabela `posts_publicados` (Supabase)

```sql
CREATE TABLE posts_publicados (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT now(),
    
    -- Conteúdo
    linha_dl TEXT NOT NULL,
    texto TEXT NOT NULL,
    hashtags TEXT[],
    formato TEXT DEFAULT 'post' CHECK (formato IN ('post', 'carrossel', 'reels')),
    
    -- Imagem
    image_url TEXT,
    image_provider TEXT,
    prompt_imagem TEXT,
    
    -- Publicação
    plataforma TEXT NOT NULL CHECK (plataforma IN ('facebook', 'instagram')),
    post_id TEXT,
    media_id TEXT,
    horario_publicacao TIMESTAMPTZ,
    horario_agendado TEXT,
    
    -- KILLCRITIC
    killcritic_aprovado BOOLEAN DEFAULT false,
    killcritic_motivo TEXT,
    killcritic_tentativas INTEGER DEFAULT 1,
    
    -- Metadados
    trigger_tipo TEXT CHECK (trigger_tipo IN ('cron', 'webhook')),
    dry_run BOOLEAN DEFAULT false,
    tema_override TEXT,
    workflow_execution_id TEXT,
    
    -- Erro
    erro BOOLEAN DEFAULT false,
    erro_mensagem TEXT
);

-- Índices para consultas frequentes
CREATE INDEX idx_posts_linha_dl ON posts_publicados (linha_dl);
CREATE INDEX idx_posts_created_at ON posts_publicados (created_at DESC);
CREATE INDEX idx_posts_plataforma ON posts_publicados (plataforma);
CREATE INDEX idx_posts_killcritic ON posts_publicados (killcritic_aprovado);

-- RLS (Row Level Security)
ALTER TABLE posts_publicados ENABLE ROW LEVEL SECURITY;

-- Policy para Service Role (bypass total)
CREATE POLICY "Service role has full access" ON posts_publicados
    FOR ALL
    USING (true)
    WITH CHECK (true);
```

---

## 12. Aprovação

| Papel | Nome | Data | Status |
|---|---|---|---|
| Engenheiro de Integração | DL Nexus V3 | 2026-06-23 | ✅ Criado |
| Gerente de Projeto | ___________________ | ___/___/___ | ⬜ Pendente |
| Diretor Técnico | ___________________ | ___/___/___ | ⬜ Pendente |

---

> **Documento mantido pela equipe de Engenharia de Integração — DL Nexus V3**  
> Última atualização: 2026-06-23

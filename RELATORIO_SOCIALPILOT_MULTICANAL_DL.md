# 📊 Relatório de Autopublicação Social Multicanal — DL Soluções
## Arquitetura Desacoplada e Foco em Compliance (Fortress v1)

Este relatório descreve a reestruturação da rotina de planejamento, geração, revisão e publicação automática de mídias sociais para a **DL Soluções Condominiais**.

---

### 📂 Workflows Criados e Configurados

A arquitetura linear anterior (que corria o risco de interromper todo o fluxo de publicação caso um canal falhasse) foi totalmente reformulada em **4 workflows modulares e assíncronos**, integrados através de banco de dados no Supabase:

1. **`SOCIAL_PLANEJADOR_DIARIO_DL.json`**
   - **Frequência:** Diária (9:00 AM)
   - **Objetivo:** Captura notícias de fontes autorizadas (G1, ABESE, CBMERJ, etc.) ou sorteia temas educativos/evergreen. Associa o conteúdo a um dos 10 serviços oficiais da DL Soluções e insere o rascunho de postagem na tabela `dl_social_publicacoes` com o status `rascunho_planejado`.
   - **Arquivo:** [SOCIAL_PLANEJADOR_DIARIO_DL.json](file:///D:/AntiGravity/projeto_01/DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/SOCIAL_PLANEJADOR_DIARIO_DL.json)

2. **`SOCIAL_GERADOR_REVISOR_DL.json`**
   - **Frequência:** Diária (10:00 AM)
   - **Objetivo:** Lê os rascunhos no banco e aciona a API do Gemini Flash para gerar textos perfeitamente formatados para 5 redes sociais (Instagram, Facebook, Google Business, TikTok, LinkedIn). Em seguida, executa o revisor de segurança **KILLCRITIC Social**, bloqueando termos impróprios ("visita técnica", "Condfy", "B2B") e garantindo a presença do CTA obrigatório ("Avaliação Técnica").
   - **Arquivo:** [SOCIAL_GERADOR_REVISOR_DL.json](file:///D:/AntiGravity/projeto_01/DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/SOCIAL_GERADOR_REVISOR_DL.json)

3. **`SOCIAL_PUBLICADOR_MULTICANAL_DL.json`**
   - **Frequência:** Diária (12:00 PM)
   - **Objetivo:** Recupera os posts aprovados com status `pronto_para_publicar` e inicia a publicação assíncrona/paralela. Em caso de falha em um canal, tenta até 2 vezes, mas continua a publicação nas demais redes sem travar o sistema. Se houver falha definitiva, notifica o Telegram.
   - **Arquivo:** [SOCIAL_PUBLICADOR_MULTICANAL_DL.json](file:///D:/AntiGravity/projeto_01/DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/SOCIAL_PUBLICADOR_MULTICANAL_DL.json)

4. **`SOCIAL_RELATORIO_SEMANAL_DL.json`**
   - **Frequência:** Toda segunda-feira às 08:00 AM
   - **Objetivo:** Consolida as estatísticas da semana anterior com contagens de postagens planejadas, falhas, bloqueios KILLCRITIC e envio de relatório formatado para o Telegram e e-mail corporativo.
   - **Arquivo:** [SOCIAL_RELATORIO_SEMANAL_DL.json](file:///D:/AntiGravity/projeto_01/DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/SOCIAL_RELATORIO_SEMANAL_DL.json)

---

### 🗄️ Tabela do Banco de Dados (`dl_social_publicacoes`)

A tabela foi modelada e criada no Supabase utilizando a migração [MIGRATIONS_DL_NEXUS_V7_SOCIAL.sql](file:///D:/AntiGravity/projeto_01/backend/supabase/MIGRATIONS_DL_NEXUS_V7_SOCIAL.sql).

```sql
CREATE TABLE IF NOT EXISTS dl_social_publicacoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    semana_ref VARCHAR(50),
    data_planejada DATE,
    origem_conteudo VARCHAR(100),
    fonte_tipo VARCHAR(100),
    fonte_nome VARCHAR(255),
    fonte_url TEXT,
    fonte_data_publicacao DATE,
    fonte_data_consulta TIMESTAMP WITH TIME ZONE,
    produto_dl VARCHAR(100),
    publico_alvo VARCHAR(255),
    tema VARCHAR(255),
    resumo_fonte TEXT,
    texto_base TEXT,
    legenda_instagram TEXT,
    legenda_facebook TEXT,
    texto_google_business TEXT,
    roteiro_tiktok TEXT,
    texto_linkedin TEXT,
    hashtags TEXT,
    image_url TEXT,
    video_url TEXT,
    status_revisao VARCHAR(50) DEFAULT 'rascunho_planejado',
    bloqueios TEXT,
    status_instagram VARCHAR(50) DEFAULT 'pendente',
    status_facebook VARCHAR(50) DEFAULT 'pendente',
    status_google_business VARCHAR(50) DEFAULT 'pendente',
    status_tiktok VARCHAR(50) DEFAULT 'pendente',
    status_linkedin VARCHAR(50) DEFAULT 'pendente',
    url_instagram TEXT,
    url_facebook TEXT,
    url_google_business TEXT,
    url_tiktok TEXT,
    url_linkedin TEXT,
    erros TEXT,
    tentativas INT DEFAULT 0,
    publicado_em TIMESTAMP WITH TIME ZONE,
    relatorio_enviado BOOLEAN DEFAULT FALSE
);
```

---

### 🔑 Estado das Credenciais e Integrações

Para que o publicador funcione em modo de produção real, é necessário mapear as credenciais nas contas corretas. Canais não configurados foram marcados como **pendentes** e tratados no código de forma a não interromper os demais fluxos:

| Canal Social | Status da Credencial | Identificação Técnica no .env |
| :--- | :---: | :--- |
| **Instagram Graph API** | **PRONTO** | `META_TOKEN` |
| **Facebook Page** | **PRONTO** | `META_TOKEN` |
| **Google Business Profile** | **PENDENTE** | Mapeamento dinâmico via OAuth2 necessário no painel n8n |
| **TikTok Content Posting** | **PENDENTE** | Requer autorização de token dinâmico no n8n |
| **LinkedIn Page API** | **PENDENTE** | Requer autorização do escopo de Organização no n8n |
| **Telegram (Notificações)** | **PRONTO** | `TELEGRAM_CHAT_ID` e `TELEGRAM_BOT_TOKEN` |
| **E-mail (SMTP)** | **PRONTO** | `HOSTGATOR_API_KEY` / `sac@dlsolucoescondominiais.com.br` |

---

### ⚠️ Riscos Identificados e Mitigação

1. **Expiração do Meta Access Token:**
   - *Risco:* Os tokens de página do Facebook/Instagram expiram após 60 dias (Tokens de Curta Duração).
   - *Mitigação:* Configurar um System User no Meta Business Suite para gerar um **Token de Longa Duração Eterno** (Never Expire).
2. **Políticas de Spam do Google Business:**
   - *Risco:* Publicações diárias repetitivas com CTAs comerciais podem ser sinalizadas pelo algoritmo de busca local.
   - *Mitigação:* O planejador mescla temas educativos/evergreen com links informativos da própria DL para evitar caráter puramente propagandístico.
3. **Erros de API Individuais:**
   - *Risco:* Um nó de publicação falhar e travar o processamento dos demais canais.
   - *Mitigação:* Uso explícito de cláusula `onError: continueErrorOutput` nas conexões e ramos paralelos no workflow, mantendo a autonomia total de cada canal.

---

### 🎯 Próximos Passos
1. Conectar fisicamente as credenciais pendentes (Google Business, LinkedIn e TikTok) na interface administrativa do n8n.
2. Executar um **DRY RUN** manual através do acionador do workflow `SOCIAL_PLANEJADOR_DIARIO_DL` para confirmar a correta inserção de linhas no banco de dados Supabase.
3. Auditar a caixa de entrada do canal de Telegram para garantir o recebimento dos alertas de revisão.

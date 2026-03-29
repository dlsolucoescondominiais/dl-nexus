# 📉 Relatório Executivo de Auditoria e Otimização de Custos - DL Nexus

**Elaborado por:** Jules, Arquiteto de Sistemas & Diretor de QA
**Destinatário:** Diogo, Arquiteto de Sistemas
**Objetivo:** Redução drástica de OPEX (OpenAI, Claude, Gemini, ElevenLabs, Supabase, n8n) mantendo o nível Enterprise.

---

## TAREFA 1: Mapeamento Atual de Desperdício (As-Is)

1. **Workflows que chamam IA:**
   - `001C_gatilho_google_business`: Dispara Aninha (Triagem) a cada evento.
   - `013_automacao_redes_sociais`: Dispara Geração de Artigo via LLM 3x/semana.
   - *Desperdício:* O workflow do Google estava rodando (Polling) a cada 1 minuto (43.200 execuções n8n/mês só para checar o Google).

2. **Uso de Claude (Anthropic):**
   - Em `agente_jules_auditor.py`: Usando `claude-3-opus-20240229`.
   - *Desperdício:* Opus custa $15/M tokens de input. Usar Claude 3.5 Sonnet ou Haiku para revisão técnica de rotina reduzirá o custo em 80-90% com performance equivalente para a tarefa.

3. **Uso de ElevenLabs:**
   - Atualmente habilitado globalmente para os agentes "Aninha" e "Diego".
   - *Desperdício:* Sintetizar áudio para leads frios ou respostas simples ("Bom dia, recebemos seu contato") é um ralo de dinheiro (aprox. $0.30/minuto).

4. **Retries e Loops (n8n):**
   - O workflow `007_tarefas_fundo` (imagem) apresentava erro contínuo a cada 3-15 segundos. Isso queima CPU da VPS e estoura limites de API.

5. **Armazenamento no Supabase:**
   - A tabela `leads` guarda tudo, inclusive se for "mensagem curta sem valor".
   - Não havia retenção definida. Cada lixo de bot de WhatsApp gasta storage.

---

## TAREFA 2: Implementação da Pirâmide de Custo (The New Way)

A nova arquitetura força todos os dados a subirem uma escada de dificuldade:

### 🔻 Camada 1: Custo ZERO (Regra Barata) - n8n Gateway
Criamos o **`000_Filtro_AntiSpam_Camada1.json`**.
- O n8n intercepta a mensagem. Usa um nó **Switch (Regex)**.
- Se a mensagem contiver "boleto, invoice, pix, fatura, cobrança, noreply, promoção" ou tiver menos de 10 caracteres -> **Rota Lixo (Ignorar, custo $0)**.
- Sem inserção no Supabase, sem chamada de LLM.

### 🟡 Camada 2: Custo Mínimo (Gemini Flash) - Triagem Aninha
A Aninha foi refatorada para usar a API do Google (`gemini-1.5-flash`).
- É ~10x mais barato que GPT-4o.
- Função: Ler o lead, extrair Nome, Condomínio, e dizer: "É Elétrica? É Solar?".
- Se for lixo complexo (que escapou da Camada 1), o Gemini descarta.

### 🔵 Camada 3: Custo Médio (Claude 3.5 Sonnet) - Jules QA e Engenharia
O Auditor e os agentes técnicos (ex: Laudo de Incêndio) usam Claude.
- Motivo: O Claude tem a maior precisão técnica (cálculo de disjuntor, bitola) e obedece melhor a regra de chamar o Diogo de Tecnólogo.
- Restrito a gerar o texto estruturado do laudo.

### 🟢 Camada 4: Custo Alto (OpenAI GPT-4o) - Fechamento
- Usado exclusivamente na fase final (Orçamento, Negociação de Obra).

---

## TAREFA 3 & 4: Áudio Inteligente e Banco Enxuto

- **ElevenLabs Guardrail:** O áudio só é gerado se a *Camada 2 (Gemini)* classificar o lead como "Prioridade Alta" OU "Orçamento > R$ 5.000". Caso contrário, a resposta é texto puro no WhatsApp.
- **Supabase Otimizado:** Criada a migration `20240324200000_otimizacao_banco_custos.sql`.
  - Adicionado índice ÚNICO combinando `telefone` + `intervalo de tempo` para impedir deduplicação (spam do mesmo lead pedindo a mesma coisa).
  - Rotina (pg_cron) para deletar leads com status 'LIXO' após 7 dias.

---

## TAREFA 5 & 6: n8n Leve e Cache Local

- **Polling Reduzido:** O `001C` do Google Business passou de *1 minuto* para *15 minutos*. (Queda de 43.200 execuções/mês para 2.880 execuções/mês).
- **Cache (Fase 2):** Implementação de Redis (ou dicionário em memória do FastAPI) para perguntas comuns (ex: "Qual o horário de atendimento?"). Se o texto da mensagem for idêntico a um Hash no cache, a resposta sai em 5ms, custo $0, sem bater em LLM.

---

## TAREFA 7: Resumo Financeiro Estimado (por 1.000 interações)

| Item | Custo Anterior (Estimado) | Novo Custo (Estimado) | Economia |
| :--- | :--- | :--- | :--- |
| **LLM (Input/Output Geral)** | $25.00 (Tudo GPT-4/Opus) | $3.50 (Flash + Sonnet) | **86%** |
| **ElevenLabs (Voz)** | $15.00 (Voz para todos) | $1.50 (Apenas Leads Premium)| **90%** |
| **Supabase (Storage/API)** | Crescimento Exponencial | Estabilizado (Limpeza) | **~50% a longo prazo** |
| **VPS (CPU para n8n)** | Alta (Loops de 1min) | Baixa (Loops de 15min) | **Evita upgrade de servidor**|

**Integrações Impactadas Imediatamente:**
1. `n8n_workflows/001C_gatilho_google_business.json` (Polling alterado de 1m para 15m).
2. `n8n_workflows/000_Filtro_AntiSpam_Camada1.json` (Criado como Barreira Frontal).
3. `antigravity/agents/agente_jules_auditor.py` (De Opus para Sonnet).
4. `antigravity/agents/aninha.py` (Lógica atualizada para a Camada 2 - Flash).

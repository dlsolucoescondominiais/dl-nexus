# 🚀 GUIA DE IMPLANTAÇÃO E BLINDAGEM DO DL NEXUS

Bem-vindo ao centro de controle, Diogo. Aqui está o roteiro de execução para a entrada em produção do sistema de automação B2B.

---

## FASE 1: BANCO DE DADOS SUPABASE (O CÉREBRO ESTRUTURAL)

**Objetivo:** Criar as gavetas e regras de banco que receberão os leads dos Síndicos.

1. Faça login em [Supabase.com](https://supabase.com/).
2. Abra o projeto **DL Nexus** (ID: `nejdtvkpiclagsnfljsz`).
3. Vá no menu lateral esquerdo em **SQL Editor** (ícone de terminal).
4. Clique em **"New Query"**.
5. Abra o arquivo `backend/supabase/MIGRATIONS_DL_NEXUS.sql` no seu computador, copie TODO o código e cole na tela preta.
6. Pressione o botão verde **RUN**.
7. Se tudo der certo, aparecerá a mensagem "Success. No rows returned".
8. (Opcional) Verifique no menu **Table Editor** se as tabelas `leads`, `avaliacoes_tecnicas`, etc. apareceram perfeitamente.

---

## FASE 2: ORQUESTRAÇÃO N8N (O SISTEMA NERVOSO)

**Objetivo:** Roteamento Inteligente através da sua Hospedagem HostGator VPS / Docker.

1. Acesse seu painel n8n: `https://n8n.dlsolucoescondominiais.com.br`
2. No menu lateral, clique em **Workflows** e depois no botão **[+ Add Workflow]**.
3. No canto superior direito da tela em branco, clique nos **Três Pontinhos (...) > Import from File**.
4. Importe, um por um, os seguintes arquivos localizados em `backend/n8n/workflows/`:
   - `001_webhook_receptor.json` (A porta da rua)
   - `002_roteador_aninha.json` (A Triagem)
   - `006_notificacoes.json` (O Alarme)
   - `012_agente_automacao.json` (A máquina OPEX de Propostas)

### ⚠️ AVISO DE SEGURANÇA (Autenticação dos Webhooks)
Nos arquivos importados, eu blindei a entrada. Eles exigem um **headerAuth**.
- Dentro do n8n, clique duas vezes no nó Webhook.
- Na seção `Authentication`, selecione/crie a credencial de **Header Auth**.
- Coloque o nome como `X-DL-API-KEY` e a senha gerada (Anota essa senha, você vai precisar colocar na Meta ou no Supabase).

---

## FASE 3: INTEGRAÇÃO META WHATSAPP (A VOZ DA EMPRESA)

1. Vá em [developers.facebook.com](https://developers.facebook.com/) e acesse o aplicativo do WhatsApp.
2. Nas configurações de **Webhooks**, aponte a URL para: `https://n8n.dlsolucoescondominiais.com.br/webhook/dl-receptor`
3. Coloque o Header Auth configurado no passo anterior (`X-DL-API-KEY`) para liberar a passagem da Meta para a HostGator.
4. Gere o Token Definitivo do WhatsApp (Acesso Permanente) e cole-o na variável `$env.META_ACCESS_TOKEN` do seu servidor HostGator.

---
**Responsabilidade Técnica:** Jules B. (Arquiteto de Sistemas) | DL Soluções Condominiais

# 📲 GUIA DE PREPARAÇÃO DO WHATSAPP (META API)
**Integração do Cérebro DL Nexus na HostGator**

Diogo, para plugar o seu número oficial no cérebro da Aninha (n8n hospedado na sua VPS), o Facebook precisa validar se o seu servidor é real e seguro.

Vá no seu painel [Meta for Developers](https://developers.facebook.com/) -> App DL Soluções -> WhatsApp -> Configuration.


### Regra Importante de Números (WhatsApp API vs Atendimento Humano)

*   **Número para Meta API / n8n / DL Nexus (Cloud API):** `+55 21 99269-8612`. Este número deve ser usado para automação, webhooks, testes e Aninha. Certifique-se de que ele está ativo para receber SMS ou ligação antes de adicioná-lo no WhatsApp Manager.
*   **Número para WhatsApp Business App (NÃO USAR NA API):** `+55 21 96474-2458`. Este número está vinculado ao atendimento humano principal, login de segurança da conta Meta, Facebook, Instagram e Meta Verified. Se tentar colocá-lo na Cloud API, ele será desconectado do aplicativo, bagunçando a operação atual.

### 1. Detalhes do Webhook (Callback URL)
Cole exatamente esta URL (é o endpoint cego do n8n que abre a porta da empresa):
**Callback URL:**
`https://n8n.dlsolucoescondominiais.com.br/webhook/meta-whatsapp`

### 2. Verify Token (Token de Verificação)
O Meta exige que você escolha uma senha secreta temporária para ele bater na sua porta. Você definiu uma chave de ambiente interna no n8n.
**Verify Token:**
Digite a chave que você colocou na sua variável de ambiente `N8N_INTERNAL_KEY` (aquela mesma chave usada para o `Header Auth`). Exemplo de digitação: `DL_NEXUS_VERIFY_2026`

### 3. Subscription Fields (O que a Meta vai te enviar)
Após validar, marque a caixa **`messages`**.
Isso garante que toda vez que um síndico mandar um "Bom dia" ou um áudio, a Meta dispare o payload JSON direto na URL `/meta-whatsapp`, que jogará o texto na esteira do banco de dados (tabela `leads`) e acionará a análise do Supabase (A Aninha).

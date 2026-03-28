# Passo a Passo de Autenticação OAuth2 no GCP (Para o n8n)

Para que os fluxos `001C` (Mensagens e Avaliações) e `013` (Postagem Automática) funcionem, o n8n precisa de permissão oficial da sua conta Google para ler e escrever no **Google Business Profile (antigo Google Meu Negócio)**.

Aqui está o que o Diogo e a equipa precisam fazer na consola do Google Cloud Platform (GCP):

### Parte 1: Criar o Projeto e Ativar as APIs
1. Entre em [Google Cloud Console](https://console.cloud.google.com/).
2. Crie um novo projeto (ex: `DL-Nexus-Integrations`).
3. Vá a **"API e Serviços" > "Biblioteca"**.
4. Pesquise e ative as seguintes APIs:
   - **Google My Business Business Information API**
   - **Google My Business Q&A API** (opcional, para perguntas e respostas)
   - *Nota:* Dependendo do status da sua conta, o acesso à API completa do Google Meu Negócio pode exigir o preenchimento de um formulário de solicitação de acesso junto do Google.

### Parte 2: Configurar o "Ecrã de consentimento OAuth" (OAuth Consent Screen)
1. No menu lateral, clique em **"API e Serviços" > "Ecrã de consentimento OAuth"**.
2. Escolha **Externo** (se o email da sua empresa não for Google Workspace) ou **Interno** (se for).
3. Preencha os campos obrigatórios (Nome da App: "DL Nexus Automations", email de suporte).
4. Em "Domínios Autorizados", adicione o domínio do seu servidor n8n (ex: `dlsolucoescondominiais.com.br`).
5. **Avançado (Âmbitos/Scopes):** Você precisa de adicionar os âmbitos relacionados ao My Business (geralmente `https://www.googleapis.com/auth/business.manage`). Se eles não aparecerem na lista, você pode prosseguir e inseri-los manualmente no n8n.
6. Guarde e continue até ao fim.

### Parte 3: Criar as Credenciais (Client ID e Secret)
1. No menu lateral, clique em **"Credenciais"**.
2. Clique no botão superior **"CRIAR CREDENCIAIS" > "ID do cliente OAuth" (OAuth client ID)**.
3. Tipo de Aplicação: **Aplicação Web (Web application)**.
4. Nome: `n8n Webhook`.
5. **URIs de redirecionamento autorizados (MUITO IMPORTANTE):**
   Aqui você tem que colar a URL de Callback fornecida pelo próprio n8n.
   - No n8n, crie as credenciais "Google API" do tipo "OAuth2".
   - Lá dentro, há um campo chamado "OAuth Callback URL" (algo como `https://n8n.dlsolucoescondominiais.com.br/rest/oauth2-credential/callback`). Copie isso.
   - Cole no campo "URIs de redirecionamento autorizados" no GCP.
6. Clique em **Criar**. O GCP vai lhe dar um **ID do cliente** (Client ID) e um **Segredo do cliente** (Client Secret).

### Parte 4: Conectar ao n8n
1. Volte ao n8n, nas credenciais que estava a criar ("Google API").
2. Cole o **Client ID** e o **Client Secret**.
3. Em "Scope", garanta que tem `https://www.googleapis.com/auth/business.manage`.
4. Clique em **"Sign in with Google"** (ou "Connect"). Uma janela de login do Google vai abrir para você autorizar a aplicação.

Pronto. A partir desse momento, os nós do n8n (fluxos 001C e 013) vão poder comunicar-se com a sua ficha do Google.

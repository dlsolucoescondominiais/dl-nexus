# Passo a Passo de Autenticação OAuth2 no GCP para o Google Business Profile (n8n)

Para que o n8n consiga ler as reviews e enviar mensagens para o seu perfil do Google Business, é necessário criar credenciais OAuth2. Aqui está o caminho direto, Diogo:

## Passo 1: Criar o Projeto no GCP e Ativar as APIs
1. Entre na [Consola do Google Cloud Platform](https://console.cloud.google.com/).
2. Crie um novo projeto (ex: `DL Nexus Automação`).
3. No menu esquerdo, aceda a **APIs & Services (APIs e Serviços) > Library (Biblioteca)**.
4. Pesquise e clique em **Enable (Ativar)** para as seguintes APIs:
   - **Google My Business API**
   - **My Business Business Information API**
   - **My Business Account Management API**

## Passo 2: Configurar o Ecrã de Consentimento (OAuth Consent Screen)
1. Vá a **APIs & Services > OAuth consent screen**.
2. Selecione **External (Externo)** e clique em Create.
3. Preencha os dados básicos:
   - *App name*: n8n DL Nexus
   - *User support email*: O seu email.
   - *Developer contact information*: O seu email.
4. Avance e adicione os seguintes **Scopes (Permissões)**:
   - `https://www.googleapis.com/auth/business.manage`
   - Opcional para mensagens: `https://www.googleapis.com/auth/business.messages` (caso utilize Business Messages).
5. Como está em modo Teste, adicione o seu e-mail como "Test User". Se for para produção, terá que submeter para validação (mas para o n8n pessoal, basta deixar o seu email autorizado).

## Passo 3: Criar as Credenciais Client ID e Secret
1. Vá a **APIs & Services > Credentials (Credenciais)**.
2. Clique em **+ CREATE CREDENTIALS** > **OAuth client ID**.
3. *Application type*: Escolha **Web application**.
4. Em *Authorized redirect URIs*, é CRÍTICO inserir o endereço exato que o seu n8n utiliza para o OAuth. Geralmente é algo como:
   `https://[seu-dominio-n8n]/rest/oauth2-credential/callback`
   *(Você encontra essa URL exata dentro do nó de configuração do Google no n8n).*
5. Clique em **Create**.
6. Copie o **Client ID** e o **Client Secret**.

## Passo 4: Ligar no n8n
1. No n8n, crie uma credencial do tipo "Google Business Profile OAuth2 API".
2. Cole o *Client ID* e o *Client Secret*.
3. Clique em **Sign in with Google** no n8n. Uma janela do Google irá abrir, você fará login com a conta dona do negócio, aceitará os avisos de segurança ("Este app não foi verificado", clique em Avançar/Avançado), e permitirá o acesso.

Pronto. O nó do n8n (tanto no fluxo `001C` quanto no `013`) terá acesso total de leitura e escrita ao seu perfil no Google!

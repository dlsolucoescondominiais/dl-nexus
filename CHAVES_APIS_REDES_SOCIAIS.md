# Checklist de Autenticação - Máquina de Atração DL Nexus

Para conectar o n8n às redes sociais (Fluxo 013), você precisa de criar credenciais (Chaves de API) nas plataformas de cada rede. Siga esta lista reta e direta:

## 1. Meta (Facebook e Instagram)
**Onde ir:** [Meta for Developers](https://developers.facebook.com/)
- [ ] Criar uma App do tipo "Negócios" (Business).
- [ ] Adicionar os produtos "Facebook Login para Negócios" e "Instagram Graph API".
- [ ] Vincular a App à página do Facebook e à conta do Instagram Business da DL Soluções.
- [ ] No n8n (Credenciais): Criar "Facebook Graph API OAuth2" e "Instagram Graph API OAuth2".
- [ ] Copiar a **URL de Callback do n8n** e colar no campo "Valid OAuth Redirect URIs" nas configurações do Facebook Login na Meta.
- [ ] Gerar e copiar para o n8n o **App ID** e **App Secret**.

## 2. Google Meu Negócio (Google Business Profile)
**Onde ir:** [Google Cloud Console](https://console.cloud.google.com/)
- [ ] Selecionar o projeto `DL-Nexus-Integrations` (ou criar um novo).
- [ ] Ativar a API **Google My Business Business Information API**.
- [ ] Ir a **Credenciais > Criar Credenciais > ID do cliente OAuth** (Tipo: Aplicação Web).
- [ ] No n8n (Credenciais): Criar "Google API OAuth2".
- [ ] Copiar a **URL de Callback do n8n** e colar no campo "URIs de redirecionamento autorizados" no GCP.
- [ ] Gerar e copiar para o n8n o **Client ID** e **Client Secret**.

## 3. TikTok for Business
*Nota: O TikTok não possui um nó nativo oficial no n8n. Usamos um nó HTTP normal para fazer a ponte.*
**Onde ir:** [TikTok Developers](https://developers.tiktok.com/)
- [ ] Criar uma App na aba "Manage Apps".
- [ ] Solicitar escopos de publicação (geralmente `video.publish` ou similar, dependendo das políticas atuais do TikTok).
- [ ] Configurar o **Redirect URI** da sua API/n8n.
- [ ] Gerar o **Client Key** e **Client Secret**.
- [ ] Criar uma credencial genérica do tipo OAuth2 no n8n (ou passar via Header HTTP), usando as chaves geradas para obter o Access Token.

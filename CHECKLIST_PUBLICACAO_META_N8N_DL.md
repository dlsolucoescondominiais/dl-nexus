# CHECKLIST PRÉ-PRODUÇÃO META N8N DL

[x] Token de Acesso vitalício (Page Access Token) gerado.
[x] Token armazenado com segurança no `.env` como `META_PAGE_ACCESS_TOKEN_DL`.
[x] Teste de conectividade e publicação Facebook (Graph API Explorer/Script) executado e com ID.
[x] Workflow 082 n8n padronizado para usar a variável do ambiente e evitar vazamentos.
[x] Simulação de publicação do Workflow 082 via payload executada com sucesso e Post ID validado.
[x] Teste de criação e publicação Instagram executado com imagem pública provisória e Media ID validado.

### PENDÊNCIAS EXCLUSIVAS DO USUÁRIO PARA PRODUÇÃO FINAL
[ ] Subir a variável `META_PAGE_ACCESS_TOKEN_DL` e `META_FACEBOOK_PAGE_ID` (100166804716824) para as "Envs" do Railway / N8N Cloud.
[ ] Fazer o pull (Sincronizar repositório Git no N8N Cloud) para aplicar as correções JSON do workflow 082.
[ ] Definir infraestrutura/lugar para hospedar as imagens geradas pela IA (S3, Imgur Público ou repositório de assets acessível por HTTPS) para o n8n injetar no fluxo 081_PUBLICADOR_INSTAGRAM.

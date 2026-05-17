# Automação de Deploy via GitHub Actions (Documentação Futura)

No futuro, esta pipeline poderá ser rodada sob o `workflow_dispatch` do GitHub Actions, utilizando segredos configurados:
- `VPS_HOST`
- `VPS_PORT`
- `VPS_USER`
- `VPS_SSH_KEY`
- `N8N_CONTAINER_NAME`
- `N8N_DOMAIN`

O flow seria:
1. Rodar somente manualmente por workflow_dispatch.
2. Validar JSON.
3. Rodar KILLCRITIC.
4. Fazer backup.
5. Enviar arquivos para VPS.
6. Importar no n8n.
7. Gerar relatório.

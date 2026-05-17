# Deploy Seguro de Workflows - DL Nexus V3

Este diretório contém os scripts necessários para automatizar a ida dos workflows do Git/Antigravity para o n8n em produção.

**Regras estritas:**
- Nunca usar token antigo exposto.
- Sem segredos nestes scripts (ver `.gitignore` e `test_killcritic`).
- Nenhum post ou mensagem é enviado sem validação humana.
